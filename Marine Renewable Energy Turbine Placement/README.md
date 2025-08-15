# 🌊 Marine Renewable Energy — Turbine Placement (Ireland)

> Deploy **offshore wind turbines**, **wave energy converters**, and **tidal turbines** around Ireland on an interactive map. Spend a limited budget, place devices where the resource is strongest, then get a cinematic, typewriter‑style analysis: energy output, CO₂ savings, homes powered, device rankings, and strategy tips.

![Python](https://img.shields.io/badge/Python-3.9%2B-3776AB?logo=python)
![Jupyter/Colab](https://img.shields.io/badge/Runs_in-Jupyter%20%7C%20Colab-ffca28?logo=jupyter)
![ipyleaflet](https://img.shields.io/badge/Map-ipyleaflet-2ea44f)
![ipywidgets](https://img.shields.io/badge/UI-ipywidgets-8a2be2)

---

## Why this exists

Ireland has world‑class marine resources. This mini‑sim lets students and enthusiasts **feel** the trade‑offs: where to put what, how budget gates decisions, and why the **west** tends to win for wind/waves while **channels and sounds** shine for tidal.

---

## ✨ Features

* **Interactive map** (ipyleaflet over Ireland) — click to place devices
* **Three technologies**

  * Wind turbine (**4 MW**, **€3 M**, blue)
  * Wave converter (**1 MW**, **€2 M**, green)
  * Tidal turbine (**2 MW**, **€4 M**, red)
* **Budget & caps** — **€30 M** total and **max 10 devices**
* **Hidden resource model** — simple heuristics reward realistic zones:

  * More **westerly longitudes** → better **wind/wave** scores
  * A **Strangford‑like window** (approx 54.3–54.5°N, 5.6–5.4°W) → strong **tidal** score
* **Auto‑analysis** on **Finish**:

  * Annual MWh, CO₂ savings (≈ **0.45 t/MWh**), homes powered (≈ **4.2 MWh/home**)
  * Device rankings with quality tags (🌟/⚡/✓/\~/△)
  * Regional hints and strategy feedback
  * **Efficiency score** = MWh per €1 M spent

> Education‑first numbers. Not for siting permits or grid studies — but great for intuition and discussion.

---

## 🚀 Run it in Google Colab (free)

Colab supports ipywidgets and ipyleaflet. Do this in a new notebook:

```python
# 1) Install dependencies
!pip -q install ipyleaflet ipywidgets numpy

# 2) Enable widgets in Colab
from google.colab import output
output.enable_custom_widget_manager()

# 3) Get your code (replace with your repo)
!git clone https://github.com/<YOUR-USERNAME>/<YOUR-REPO>.git
%cd "<YOUR-REPO>/Marine Renewable Energy Turbine Placement"

# 4) Run the game (replace filename if needed)
from importlib import reload
import runpy
runpy.run_path("marine_turbine_placement.py")
```

Or import and launch the function directly (recommended):

```python
from marine_turbine_placement import run_marine_game  # <-- use your script name
run_marine_game()
```

> If the map doesn’t render, re‑run the **widget manager** cell and the **imports** (Colab can be picky about cell order).

---

## 💻 Run locally (Jupyter Notebook/Lab)

```bash
# in a fresh environment (recommended)
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS/Linux
source .venv/bin/activate

pip install ipyleaflet ipywidgets numpy

# Jupyter
pip install notebook  # or jupyterlab

# If using classic Notebook, enable widgets (Lab v3+ usually not needed)
jupyter nbextension enable --py widgetsnbextension --sys-prefix

jupyter notebook
```

Then in a notebook cell:

```python
from marine_turbine_placement import run_marine_game  # <-- use your script name
run_marine_game()
```

---

## 🎮 How to play

1. Pick a **Device** from the dropdown (Wind / Wave / Tidal).
2. **Click** on the map to place it (budget decreases, colored marker appears).
3. Repeat until you hit the **€30 M** budget or **10 devices**.
4. Click **Finish** to generate the in‑notebook report (animated).
5. Review **strategy insights**, **rankings**, **efficiency**, and **regional tips**.

---

## 🔢 Under the hood (light math)

* **Annual energy** per device uses a fixed rating and typical capacity factor:

  * Wind: 4 MW @ **40%** CF
  * Wave: 1 MW @ **30%** CF
  * Tidal: 2 MW @ **35%** CF
  * `annual_MWh ≈ MW × 8760 × CF × quality`
* **Quality** (0.5–1.3×) depends on where you click:

  * **Wind**: west of \~8.5°W improves; west of \~9.5°W is best
  * **Wave**: west of \~9°W improves; west of \~10°W is best
  * **Tidal**: small box around **Strangford** gives a big boost
* **CO₂ savings** ≈ `total_MWh × 0.45` tons/year
* **Homes powered** ≈ `total_MWh / 4.2`
* **Efficiency** ≈ `(total_MWh / € spent) × 1e6` (MWh per €1 M)

---

## 🧭 Strategy tips

* Push **wind and wave** further **west/southwest** for stronger atlantic exposure.
* Target **narrow channels/straits** for **tidal** (e.g., Strangford‑like windows).
* Mix technologies to balance resource patterns and stay under budget.
* Use your last euros wisely; sometimes one more wave unit beats a scattered turbine.

---

## 📁 Folder & file naming

```
Marine Renewable Energy Turbine Placement/
└── marine_turbine_placement.py        # or your chosen filename
```

> If your script has a different name, just update the import/path in the examples.

---

## 🧩 Troubleshooting

* **Blank map / no markers** → Re‑run `output.enable_custom_widget_manager()` in Colab; ensure ipywidgets installed.
* **Widgets don’t respond** → Restart the runtime/kernel and re‑run install + import cells.
* **Nothing happens on Finish** → Scroll up: the report prints into the **log panel** under the map.
* **Module not found** → Check the path and filename; `cd` into the correct folder in Colab.

---

## 🧪 Requirements

```txt
ipyleaflet
ipywidgets
numpy
```

*(Jupyter/Colab provides IPython, display utilities, and the notebook runtime.)*

---

## 🙌 For educators

* Run a **budget challenge** (most MWh/€) and compare efficiency scores.
* Ask learners to justify siting choices with **resource logic** (west winds, wave fetch, tidal constrictions).
* Extend the sim: add **maintenance costs**, **grid distance penalties**, or **exclusion zones**.

---

**Have fun — may your winds be steady, your waves energetic, and your tides slack at maintenance!** 🌬️🌊🌙
