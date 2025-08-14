import os, json, datetime, urllib.parse, requests, pathlib

# ---- Edit your topics here (you can change later) ----
QUERIES = [
    '("numerical modeling" OR "numerical modelling") (ocean OR coastal) CROCO',
    '("numerical modeling" OR "numerical modelling") (ocean OR coastal) ROMS',
    '("numerical modeling" OR "numerical modelling") (ocean OR coastal) FVCOM',
    '("numerical modeling" OR "numerical modelling") (ocean OR coastal) "MIKE 21"',
    '("numerical modeling" OR "numerical modelling") (ocean OR coastal) "MIKE 3"',
    '("numerical modeling" OR "numerical modelling") (ocean OR coastal) "Delft3D"',
    '("numerical modeling" OR "numerical modelling") (ocean OR coastal) "Wavewatch"',
]

# Show results from the last year (adjust if you want)
YEAR_FROM = max(datetime.date.today().year - 1, 2024)
MAX_OPENALEX_PER_QUERY = 5

def scholar_link(query: str, year_from: int) -> str:
    base = "https://scholar.google.com/scholar?"
    params = {
        "q": query,
        "hl": "en",
        "as_ylo": str(year_from),
        "scisbd": "1",  # sort by date
        "as_sdt": "1,5",
        "as_vis": "1",
    }
    return base + urllib.parse.urlencode(params)

def fetch_openalex(query: str, per_page: int):
    # Free API to list recent papers (no scraping)
    url = "https://api.openalex.org/works"
    params = {
        "search": query,
        "filter": f"from_publication_date:{YEAR_FROM}-01-01",
        "sort": "publication_date:desc",
        "per_page": str(per_page),
    }
    try:
        r = requests.get(url, params=params, timeout=25)
        r.raise_for_status()
        out = []
        for w in r.json().get("results", []):
            title = w.get("title") or "Untitled"
            date = (w.get("publication_date") or "")[:10]
            venue = (w.get("host_venue") or {}).get("display_name") or ""
            doi = w.get("doi")
            oa = (w.get("open_access") or {}).get("oa_url")
            landing = (w.get("primary_location") or {}).get("landing_page_url")
            link = oa or (f"https://doi.org/{doi.split('doi.org/')[-1]}" if doi else landing)
            out.append({"title": title, "date": date, "venue": venue, "link": link})
        return out
    except Exception:
        return []

def build():
    today = datetime.date.today().isoformat()
    records = []
    for q in QUERIES:
        rec = {
            "query": q,
            "scholar_url": scholar_link(q, YEAR_FROM),
            "openalex": fetch_openalex(q, MAX_OPENALEX_PER_QUERY),
        }
        records.append(rec)

    # Write JSON (machine-readable)
    data_dir = pathlib.Path("data")
    data_dir.mkdir(parents=True, exist_ok=True)
    (data_dir / "papers.json").write_text(
        json.dumps({"date": today, "year_from": YEAR_FROM, "items": records}, indent=2),
        encoding="utf-8"
    )

    # Write Markdown page (human-readable, Jekyll will render it)
    md_dir = pathlib.Path("papers")
    md_dir.mkdir(parents=True, exist_ok=True)
    lines = [
        "---",
        "layout: page",
        "title: Latest Research (auto-updated)",
        "permalink: /papers/",
        "---",
        f"_Last update: **{today}** · Showing results since **{YEAR_FROM}**_",
        "",
    ]
    for rec in records:
        lines.append(f"## {rec['query']}")
        lines.append(f"[Google Scholar (sorted by date)]({rec['scholar_url']})")
        if rec["openalex"]:
            lines.append("")
            lines.append("**Recent items (OpenAlex):**")
            for it in rec["openalex"]:
                venue = f" · {it['venue']}" if it['venue'] else ""
                date = f" · {it['date']}" if it['date'] else ""
                link = it["link"] or rec['scholar_url']
                lines.append(f"- [{it['title']}]({link}){venue}{date}")
        lines.append("")
    (md_dir / "index.md").write_text("\n".join(lines), encoding="utf-8")

if __name__ == "__main__":
    build()
