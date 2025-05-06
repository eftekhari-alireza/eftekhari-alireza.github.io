# Tidal Harmonic Analysis

This repository contains tools for performing tidal harmonic analysis on sea surface height (SSH) data. The analysis helps identify and calculate the amplitude and phase of tidal constituents, which represent different astronomical forces contributing to tidal patterns.

*Helping to understand and predict coastal hazards through advanced tidal analysis*

## Overview

Tidal harmonic analysis decomposes tidal observations into constituent components, each with a specific frequency determined by astronomical calculations. This helps in understanding and predicting tidal patterns.


(This script)**: Determining tidal constituents


## Features

- Loads and preprocesses sea surface height (SSH) data
- Handles missing data through linear interpolation
- Identifies 12 standard tidal constituents including:
  - Semidiurnal components (M2, S2, N2, K2)
  - Diurnal components (K1, O1, P1, Q1)
  - Long-period components (Mf, Mm, Ssa)
  - Shallow water component (M4)
- Creates a design matrix for linear regression analysis
- Fits a linear model to determine constituent amplitudes and phases
- Calculates model fit statistics (R-squared)
- Generates visualizations of top tidal constituents
- Saves results and model parameters for future use

## Requirements

- Python 3.x
- NumPy
- Pandas
- Matplotlib
- scikit-learn

## Usage

1. Ensure your SSH data is in CSV format
2. Update the `file_path` variable in the script to point to your data file
3. Run the script:

```python
python tidal_constituents.py
```

## Input Data Format

The script expects SSH data in a CSV file with the following characteristics:
- Single column of sea surface height values
- No header by default (use `has_header=True` to specify if header exists)
- Time series with consistent time intervals (hourly data recommended)

## Output

The script produces the following outputs in the `./tidal_analysis_results` directory:

1. **tidal_constituents.csv**: A CSV file containing:
   - Constituent names
   - Frequencies (cycles per hour)
   - Periods (hours)
   - Amplitudes
   - Phases (degrees)
   - Cosine and sine coefficients

2. **model_parameters.npz**: A NumPy archive containing:
   - Model parameters (cosine and sine coefficients)
   - Intercept value
   - Frequencies
   - Constituent names

3. **top_constituents.png**: A bar chart visualization of the highest amplitude constituents

## Example Results

The script outputs a summary of the top 5 tidal constituents by amplitude, which typically includes:
- M2 (Principal lunar semidiurnal, ~12.42 hour period)
- S2 (Principal solar semidiurnal, ~12.00 hour period)
- N2 (Larger lunar elliptic semidiurnal, ~12.66 hour period)
- K1 (Lunar diurnal, ~23.93 hour period)
- O1 (Lunar diurnal, ~25.82 hour period)

## Educational Notes

Tidal constituent analysis is based on the understanding that tides result from a combination of astronomical forces, each with characteristic frequencies. The amplitude of each constituent indicates its contribution to the overall tide, while the phase tells us when each constituent's peak occurs relative to a reference time.


## 📚 Citations

If you use this code in your research, please cite:

```bibtex
@software{tidal_harmonic_analysis,
  author = {Eftekhari, Alireza},
  title = {Tidal Harmonic Analysis},
  url = {https://github.com/eftekhari-alireza/eftekhari-alireza.github.io/tree/main/Tidal-Harmonic-Analysis},
  year = {2025},
}
```

## 📧 Contact

Alireza Eftekhari - a.eftekhari2@universityofgalway.ie

Project Link: [https://github.com/eftekhari-alireza/eftekhari-alireza.github.io/tree/main/Tidal-Harmonic-Analysis](https://github.com/eftekhari-alireza/eftekhari-alireza.github.io/tree/main/Tidal-Harmonic-Analysis)
