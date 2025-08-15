🌊 Wave Energy Investigation — Turn Students into Wave Detectives!

A mini-project that generates realistic, synthetic wave-climate datasets for Irish coasts and guides learners through a gamified investigation of wave energy with quizzes, charts, economics, and a final report. Perfect for Youth Academy sessions, STEM outreach, or anyone curious about how H²T (height² × period) shapes wave power.

Table of Contents

What’s inside

Installation

Quick Start

Outputs

How it works

Gameplay Flow

Customize / Tweak

Troubleshooting

Example Session

Contributing

License

requirements.txt

What’s inside

Folder: Wave Energy Investigation/

generate_wave_data.py
Creates monthly 2024 wave-climate spreadsheets (.xlsx) for 8 coastal sites + a Loop Head baseline:
Belmullet (NW), Malin Head (N), Dunmore East (SE), Old Head Kinsale (S), Brandon Bay (SW), Aran Islands (W), Achill Island (W), Fastnet Rock (SW)
Each file includes: Significant Wave Height (m) and Average Wave Period (s) with seasonal realism.

wave_investigation.py
An interactive terminal game where learners become Wave Energy Detectives:

Short quiz on wave physics 🧠

Analyze chosen/random sites from the generated Excel files

Auto-create power plots, seasonal charts, wave roses

Explore environmental (CO₂ savings, reef habitat) & economic (costs, jobs, payback) factors

Export a professional text report with rankings & recommendations

Installation

From your repo root:

# (Optional) Create & activate a virtual environment
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS / Linux
source .venv/bin/activate

# Install dependencies
pip install pandas numpy matplotlib openpyxl


openpyxl enables reading/writing the Excel files.

Quick Start
# 1) Go to the project folder
cd "Wave Energy Investigation"

# 2) Generate the monthly datasets
python generate_wave_data.py

# 3) Run the interactive investigation/game
python wave_investigation.py


You’ll be asked for your name, how many locations to analyze (3–8), and which advanced analyses to run. The game saves charts and (optionally) a final report.

Outputs

After running, you’ll see files like:

Excel datasets
Belmullet_Northwest_Wave_2024.xlsx, Aran_Islands_Wave_2024.xlsx, …
Loop_Head_Wave_2024.xlsx (baseline)

Charts (per analyzed location)

\<Location\>_wave_power_analysis.png — monthly power (kW/m) + climate overlay

\<Location\>_seasonal_wave_analysis.png — storm vs calm seasons (Winter, Spring, Summer, Autumn)

\<Location\>_wave_rose.png — directional wave climate (N, NE, …)

Final report (optional)
Wave_Detective_Report_<Your_Name>.txt — executive summary, H²T rankings, recommendations, and per-site details (power, seasonality, direction, environment, economics).

How it works

Core physics

Wave power scales with height squared and period
P ∝ H² × T

Teaching-friendly power density approximation used in the game:
P ≈ 0.49 × H² × T (kW per meter of wave crest)

Site suitability (educational heuristic)

Quick index H²T with a commercial threshold of H²T > 20.

Workflow (Mermaid)

flowchart LR
A[generate_wave_data.py] -->|creates *_Wave_2024.xlsx| B[wave_investigation.py]
B --> C[Quiz & Basics]
B --> D[Analyze Locations]
D --> E[Charts: Power / Seasonal / Rose]
D --> F[Env & Economic Insights]
D --> G[Rankings & Suitability (H²T)]
G --> H[Text Report Export]


⚠️ Educational note: Numbers are illustrative. Real projects require multi-year spectra, extremes/survivability, grid studies, ecology, finance, etc.

Gameplay Flow

Tutorial → short quiz (earn points)

Choose 3–8 locations (manual or random)

For each location:

Summary: H, T, H²T, kW/m, MWh, homes powered

ASCII mini-bars per month

Pick an advanced analysis:

Seasonal patterns

Wave direction (rose)

Environmental impact

Economic feasibility (30 MW)

Continue

Auto-generates charts & stores findings

Device selection mini-game → more points

Final rank → optional report export

Customize / Tweak

In wave_investigation.py:

device_width = 30 (m)

capacity_factor = 0.35

Electricity price, CAPEX/OPEX, jobs in calculate_economic_factors

Seasonal definitions & color palettes in plotting helpers

Directional weights in create_wave_rose (tuned to Irish coasts)

In generate_wave_data.py:

Loop Head baseline monthly H/T

Location height/period factors (exposure, bathymetry)

Random variation bands (±15% for H, ±10% for T)

Troubleshooting

“No wave data files found!”
Run python generate_wave_data.py first (the game looks for *_Wave_2024.xlsx in the current directory).

Excel read/write errors
Install openpyxl: pip install openpyxl

Matplotlib backend warnings
Safe to ignore for non-interactive runs; charts are saved as .png.

Emoji/UTF-8 issues
If your terminal can’t render emojis, the game still works fine.

Example Session
🌊 WAVE ENERGY DETECTIVE CHALLENGE - MARINE ENGINEERING EDITION 🌊
Welcome young marine engineers! ...

Please enter your name, Wave Energy Detective: Aisling
...
How many locations would you like to investigate? (3-8)
Number of locations: 4
...
🌊 WAVE CLIMATE ANALYSIS:
  • Average wave height: 2.7 m
  • Average wave period: 9.8 s
  • Wave power potential (H²T): 71.7
  • Average power density: 35.9 kW/m
  • Annual energy (30m device): 330.2 MWh
  • Could power approximately 78 homes

Contributing

Ideas & improvements welcome! Nice first issues:

CLI flags (e.g., --random N, --report)

CSV export for monthly power

Uncertainty bands & multi-year variability

Hooks for real station metadata (bathymetry, grid distance, constraints)

License

Add a license file (e.g., MIT) to clarify reuse.

requirements.txt
pandas
numpy
matplotlib
openpyxl


Happy investigating — may your waves be tall, your periods long, and your devices storm-proof! 🌊🔎⚡

You said:
explain they can do it on google colab freely and write a very engaging .md file 
ChatGPT said:
Thought for 14s
🌊 Wave Energy Investigation — Run it FREE on Google Colab!

Turn learners into Wave Energy Detectives with two Python scripts that generate realistic (synthetic) wave-climate datasets for Ireland and guide an interactive, gamified investigation of wave power, seasonality, directionality, environment, and economics.
Built for Youth Academy sessions, STEM outreach, and curious minds who want to see H²T (height² × period) come alive.








🚀 TL;DR (Colab Quickstart — Free, No Setup)

You can run everything directly in Google Colab (free) without installing anything locally.

Open https://colab.research.google.com → New Notebook

In the first cell, install dependencies:

!pip install -q pandas numpy matplotlib openpyxl


Upload the two scripts from this repo (folder Wave Energy Investigation/):

from google.colab import files
uploaded = files.upload()  # Choose generate_wave_data.py and wave_investigation.py


Generate data files (Excel):

!python generate_wave_data.py


Run the interactive game (works with input() in Colab):

!python -u wave_investigation.py


(Optional) Save outputs to your Google Drive:

from google.colab import drive
drive.mount('/content/drive')
!mkdir -p /content/drive/MyDrive/wave_outputs
!cp -n *.xlsx *.png *.txt /content/drive/MyDrive/wave_outputs/ 2>/dev/null || true


(Optional) Download files to your computer:

import glob
from google.colab import files
for f in glob.glob('*.xlsx') + glob.glob('*.png') + glob.glob('*.txt'):
    files.download(f)


💡 Tip: If prompts ever look stuck, re-run with !python -u wave_investigation.py (unbuffered I/O) — Colab handles interactive input just fine.

📁 What’s in the folder

generate_wave_data.py
Creates 2024 monthly wave-climate .xlsx files for 8 Irish sites + Loop Head baseline:
Belmullet (NW), Malin Head (N), Dunmore East (SE), Old Head Kinsale (S), Brandon Bay (SW), Aran Islands (W), Achill Island (W), Fastnet Rock (SW)
Each dataset has:

Significant Wave Height (m)

Average Wave Period (s)

Seasonal realism (stormier winters, calmer summers)

wave_investigation.py
Interactive, terminal-based Wave Detective game:

Short quiz on wave physics 🧠

Analyze random or chosen locations

Auto-generate power plots, seasonal charts, wave roses

Explore environmental impacts (CO₂ savings, reef habitat)

Explore economics (costs, jobs, revenue, payback)

Export a professional text report (rankings by H²T, recommendations)

🧪 Local Setup (Optional)
# From your repo root
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS / Linux
source .venv/bin/activate

pip install pandas numpy matplotlib openpyxl

# Go to the folder and run:
cd "Wave Energy Investigation"
python generate_wave_data.py
python wave_investigation.py

🖼 Outputs You’ll Get

Excel datasets
Belmullet_Northwest_Wave_2024.xlsx, Aran_Islands_Wave_2024.xlsx, …
Loop_Head_Wave_2024.xlsx (baseline)

Charts (per analyzed location)

<Location>_wave_power_analysis.png — monthly kW/m + climate overlay

<Location>_seasonal_wave_analysis.png — storm vs calm seasons

<Location>_wave_rose.png — directional climate (N, NE, …)

Final report (optional)
Wave_Detective_Report_<Your_Name>.txt — executive summary, H²T rankings, recommendations, and per-site details.

⚙️ How it works (in plain English)

Wave power scales with height² and period → P ∝ H² × T

Teaching-friendly approximation used for power density:
P ≈ 0.49 × H² × T (kW per meter of wave crest)

Quick site suitability index: H²T, with a classroom threshold H²T > 20

Energy estimate combines average power, a nominal device width (30 m), hours/year, and capacity factor.

🧭 Educational note: Numbers are illustrative. Real projects need multi-year spectra, directional distributions, extreme/survivability analysis, grid studies, ecology, finance, etc.

flowchart LR
A[generate_wave_data.py] -->|creates *_Wave_2024.xlsx| B[wave_investigation.py]
B --> C[Quiz & Basics]
B --> D[Analyze Locations]
D --> E[Charts: Power / Seasonal / Rose]
D --> F[Env & Economic Insights]
D --> G[Rankings & Suitability (H²T)]
G --> H[Text Report Export]

🎮 Gameplay Flow

Tutorial → mini quiz (score points)

Choose 3–8 locations (manual or random)

For each location:

Summary: H, T, H²T, kW/m, MWh, homes powered

ASCII mini-bars by month

Pick an advanced analysis:

Seasonal patterns

Wave direction (rose)

Environmental impact

Economic feasibility (30 MW)

Continue

Charts saved automatically

Device selection mini-game → extra points

Final rank → optional report export

🎛 Customize / Tweak

In wave_investigation.py:

device_width = 30 (m)

capacity_factor = 0.35

Energy price, CAPEX/OPEX, jobs in calculate_economic_factors

Seasonal buckets and color palettes in plotting helpers

Directional weights in create_wave_rose (tuned for Irish coasts)

In generate_wave_data.py:

Loop Head baseline monthly H/T

Location height/period factors (exposure, bathymetry)

Random variation bands (default: ±15% for H, ±10% for T)

🧩 Troubleshooting (Colab & Local)

“No wave data files found!”
Run python generate_wave_data.py first — the game looks for *_Wave_2024.xlsx in the current directory.

Colab can’t see my files
Re-run the files.upload() cell or clone your repo into Colab:

!git clone https://github.com/<your-username>/<your-repo>.git
%cd "<your-repo>/Wave Energy Investigation"


Excel read/write error
Ensure openpyxl is installed: pip install openpyxl

Charts don’t appear inline
That’s expected — the game saves charts as .png files in the working folder.

Emoji/UTF-8 issues
If your terminal can’t render emojis, everything still runs fine.

🧾 requirements.txt (for convenience)
pandas
numpy
matplotlib
openpyxl

📜 License

Add a license (e.g., MIT) to clarify reuse.

Have fun, Detectives — may your waves be tall, your periods long, and your devices storm-proof! 🌊🔎
