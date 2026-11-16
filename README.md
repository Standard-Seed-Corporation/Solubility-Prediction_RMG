# Automated Computational Screening of Temperature-Dependent Cannabinoid Solubility in Industrially Relevant Processing Solvents and Lipid Carrier Oils

[![SolProp ML Prediction](https://github.com/Standard-Seed-Corporation/Solubility-Prediction_RMG/actions/workflows/solprop_prediction.yml/badge.svg)](https://github.com/Standard-Seed-Corporation/Solubility-Prediction_RMG/actions/workflows/solprop_prediction.yml)
![Python](https://img.shields.io/badge/python-3.7-blue)
![License: MPL 2.0](https://img.shields.io/badge/license-MPL%202.0-brightgreen)

**Mohammadhu Rifaydheen Sakeer**¹, **Katukoliya Gamage Anuththara Samadhi**¹, **Sashika Kalana Prabhath Kotawalagedara**¹, **Pamalka Hansani Kaldera**¹, **Damilola Samuel Bodun**¹ ², **Evan Friedmann**³, **Kevin Kimmell**⁴, **Manny Maminakis**⁵, **David Aronson**¹, **Mike Woster**¹, **Suliman Sharif**¹ \*

¹ Standard Seed Corporation, Smyrna, DE, USA  
² Université Paris Cité, France  
³ Helma, USA  
⁴ Arvida Labs, USA  
⁵ Cannmatrix, USA

\* Corresponding author: Suliman Sharif — sharifsuliman1@gmail.com  
Pipeline developer: Mohammadhu Rifaydheen Sakeer — sakeermr5@gmail.com

---

This repository contains the **automated computational pipeline** developed for this study. It predicts the **temperature-dependent solid solubility** and **solvation thermodynamics** of cannabinoids in industrial processing solvents and lipid carrier oils, using the machine-learning models of [SolProp_ML](https://github.com/fhvermei/SolProp_ML) and running end to end on GitHub Actions.

Add solute–solvent–temperature systems to a CSV file, push, and the pipeline returns predicted solubilities, solvation free energies and enthalpies, and Abraham solute parameters, with no local installation required.

---

## Table of Contents

- [Overview](#overview)
- [Screening Design](#screening-design)
- [Features](#features)
- [How It Works](#how-it-works)
- [Repository Structure](#repository-structure)
- [Quick Start](#quick-start)
- [Input Format](#input-format)
- [Output Files](#output-files)
- [Running Locally](#running-locally)
- [Scope and Limitations](#scope-and-limitations)
- [Troubleshooting](#troubleshooting)
- [Citation](#citation)
- [License](#license)
- [Contact](#contact)
- [Acknowledgments](#acknowledgments)

---

## Overview

Cannabinoid extraction, purification, crystallization, and formulation all depend on how well each compound dissolves in the solvent or carrier being used, and on how that solubility changes with temperature. Experimental solubility data for cannabinoids are scarce and costly to collect across the many solvents used in industry, from hydrocarbon and supercritical extraction solvents to the edible oils and fatty acids used as carriers in final products.

This project builds a reproducible, fully automated screening pipeline around the machine-learning solubility models of Vermeire, Chung & Green (*J. Am. Chem. Soc.* 2022). Every solute–solvent–temperature combination is predicted in a single batch run, and the results are versioned alongside the inputs, so the screen can be rerun or extended with new compounds and solvents by editing one CSV file.

## Screening Design

The current dataset ([`input/solubility_data_no_stereo.csv`](input/solubility_data_no_stereo.csv)) is a full factorial screen:

| Dimension     | Count | Details |
|---------------|:-----:|---------|
| Solutes       | 19    | Major and minor cannabinoids — e.g. CBD, Δ⁹-THC, THCA, CBG, CBN, CBNA, and HHC epimers — plus two non-cannabinoid reference compounds (melatonin and acetazolamide) |
| Solvents      | 18    | See table below |
| Temperatures  | 3     | 273.15 K (0 °C), 298.15 K (25 °C), 323.15 K (50 °C) |
| **Systems**   | **1,026** | 19 × 18 × 3 |

**Solvents by application**

| Category                          | Solvents (SMILES) |
|-----------------------------------|-------------------|
| Hydrocarbon extraction solvents   | Propane (`CCC`), n-butane (`CCCC`), n-hexane (`CCCCCC`), n-heptane (`CCCCCCC`), n-octane (`CCCCCCCC`) |
| Supercritical / pressurized gases | Carbon dioxide (`O=C=O`), 1,1,1,2-tetrafluoroethane, R-134a (`FCC(F)(F)F`) |
| Alcohols                          | Methanol (`CO`), ethanol (`CCO`), isopropanol (`CC(C)O`) |
| Polar aprotic solvents            | Acetone (`CC(=O)C`), acetonitrile (`CC#N`), DMSO (`CS(=O)C`) |
| Fatty acids (carrier oil components) | Lauric acid (C12:0), palmitic acid (C16:0), oleic acid (C18:1), linoleic acid (C18:2) |
| MCT-oil surrogate                 | Octanoate ester (`CCCCCCCC(=O)OCC(=O)OCCCCCCCC`) |

> **Note:** SolProp_ML treats every solvent as a pure liquid. Results for propane, butane, CO₂ and R-134a assume liquid-phase conditions and do not account for pressure; real carrier oils are mixtures, which are represented here by their major individual components.

## Features

- **Batch predictions** — process any number of solute–solvent–temperature combinations from one or more CSV files.
- **Temperature-dependent solubility** — predicts log S across a range of temperatures.
- **Solvation thermodynamics** — solvation free energy (ΔG<sub>solv</sub>), solvation enthalpy (ΔH<sub>solv</sub>), and aqueous solubility (S<sub>aq</sub>).
- **Abraham solute parameters** — E, S, A, B, L descriptors for each solute.
- **Fully automated** — runs on GitHub Actions; results are committed back to the repository and published as downloadable artifacts.
- **Reproducible** — pinned model version (SolProp v1.2) and a fixed conda environment.

## How It Works

```
input/*.csv  ──►  GitHub Actions  ──►  SolProp_ML + trained models  ──►  output/*.csv
                       │
                       ├─ 1. Check out repository (model archive via Git LFS)
                       ├─ 2. Build conda environment from SolProp_ML
                       ├─ 3. Install SolProp v1.2 trained models (Gsolv, Hsolv, Saq)
                       ├─ 4. Run scripts/run_prediction_real.py on every input CSV
                       └─ 5. Upload artifact + commit results to output/
```

The workflow is defined in [`.github/workflows/solprop_prediction.yml`](.github/workflows/solprop_prediction.yml).

## Repository Structure

```
Solubility-Prediction_RMG/
├── .github/
│   └── workflows/
│       └── solprop_prediction.yml     # CI pipeline
├── input/
│   └── solubility_data_no_stereo.csv  # Solute–solvent–temperature systems
├── output/                            # Prediction results (auto-generated)
├── scripts/
│   └── run_prediction_real.py         # Batch prediction driver
├── SolProp_v1.2.zip                   # Trained ML models (stored in Git LFS)
├── .gitattributes                     # Git LFS configuration
├── .gitignore
├── LICENSE
└── README.md
```

## Quick Start

### 1. Add your molecules

Create or edit a CSV file in the `input/` folder (see [Input Format](#input-format)):

```csv
solvent,solute,temperature
CCO,CCCCCC1=CC(O)=C([C@H]2[C@H](C(C)=C)CCC(C)=C2)C(O)=C1,298.15
CCCCCC,CCCCCC1=CC(O)=C([C@H]2[C@H](C(C)=C)CCC(C)=C2)C(O)=C1,273.15
CCCCCCCC/C=C\CCCCCCCC(=O)O,CCCCCC1=CC(O)=C([C@H]2[C@H](C(C)=C)CCC(C)=C2)C(O)=C1,323.15
```

*(CBD in ethanol, n-hexane, and oleic acid.)*

### 2. Run the predictions

**Automatically** — commit and push any change inside `input/`:

```bash
git add input/
git commit -m "Add molecules for prediction"
git push
```

**Manually** — go to **Actions → SolProp ML Prediction (Real) → Run workflow**.

### 3. Collect the results

- **Repository:** results are committed to the `output/` folder at the end of each run.
- **Artifacts:** open the workflow run, scroll to **Artifacts**, and download `solprop-results-<run number>` (kept for 30 days).

A typical run takes 10–20 minutes, most of which is environment setup.

## Input Format

Each CSV file in `input/` is processed independently. Columns:

| Column        | Required | Description                                  | Example        |
|---------------|:--------:|----------------------------------------------|----------------|
| `solvent`     | Yes      | Solvent structure as a SMILES string         | `CCO`          |
| `solute`      | Yes      | Solute structure as a SMILES string          | `c1ccccc1`     |
| `temperature` | Yes      | Temperature in Kelvin                        | `298.15`       |

SolProp_ML also accepts optional reference-solubility and sublimation-property columns that improve accuracy when experimental data are available. See the [SolProp_ML documentation](https://github.com/fhvermei/SolProp_ML) for details.

**Common solvent SMILES**

| Solvent      | SMILES      | Solvent        | SMILES        |
|--------------|-------------|----------------|---------------|
| Water        | `O`         | Acetone        | `CC(=O)C`     |
| Methanol     | `CO`        | Acetonitrile   | `CC#N`        |
| Ethanol      | `CCO`       | Ethyl acetate  | `CCOC(C)=O`   |
| 1-Propanol   | `CCCO`      | Toluene        | `Cc1ccccc1`   |
| n-Hexane     | `CCCCCC`    | Cyclohexane    | `C1CCCCC1`    |

## Output Files

For every input file `<name>.csv`, the run produces timestamped files in `output/`:

| File                               | Contents                                                        |
|------------------------------------|-----------------------------------------------------------------|
| `<name>_results_<timestamp>.csv`   | Predicted solubility (log S) for each system                    |
| `<name>_detailed_<timestamp>.csv`  | Intermediate values used in the solubility calculation          |
| `<name>_properties_<timestamp>.csv`| ΔG<sub>solv</sub>, ΔH<sub>solv</sub>, S<sub>aq</sub>, and Abraham solute parameters |
| `<name>_log_<timestamp>.log`       | Execution log and model warnings                                |
| `<name>_summary_<timestamp>.txt`   | Short human-readable summary of the run                         |
| `<name>_error_<timestamp>.txt`     | Written only if processing that file failed                     |

## Running Locally

Requirements: [Miniconda/Anaconda](https://docs.conda.io/), Git, and Git LFS.

```bash
# 1. Clone this repository (with the LFS model archive)
git lfs install
git clone https://github.com/Standard-Seed-Corporation/Solubility-Prediction_RMG.git
cd Solubility-Prediction_RMG

# 2. Get SolProp_ML and create its environment
git clone https://github.com/fhvermei/SolProp_ML.git
conda env create -n env_solprop -f SolProp_ML/environment.yml
conda activate env_solprop
pip install git+https://github.com/bp-kelley/descriptastorus
pip install -e SolProp_ML

# 3. Install the trained models
unzip SolProp_v1.2.zip
mkdir -p SolProp_ML/solvation_predictor/trained_models
cp -r SolProp_v1.2/Machine_learning_models/{Gsolv,Hsolv,Saq} \
      SolProp_ML/solvation_predictor/trained_models/

# 4. Run predictions
export PYTHONPATH="$PYTHONPATH:$PWD/SolProp_ML"
python scripts/run_prediction_real.py
```

## Scope and Limitations

| Supported                                         | Not supported                         |
|---------------------------------------------------|---------------------------------------|
| Neutral organic molecules                         | Ions, salts, and charged species      |
| Elements H, B, C, N, O, S, P, F, Cl, Br, I        | Metals and organometallics            |
| Pure organic solvents and water                   | Solvent mixtures                      |
| Typical temperatures for liquid solvents          | Polymers and very large molecules     |

Predictions are model estimates. Accuracy is best for molecules similar to the training data; validate critical results experimentally.

## Troubleshooting

| Symptom                                           | Likely cause and fix                                                                 |
|---------------------------------------------------|--------------------------------------------------------------------------------------|
| Workflow does not start after a push              | Only changes in `input/`, `scripts/`, or the workflow file trigger a run. Use **Run workflow** instead. |
| `SolProp_v1.2.zip is not a real zip`              | Git LFS file was not downloaded. Check the organization's LFS storage/bandwidth quota. |
| Push of results fails with 403                    | Enable **Settings → Actions → General → Workflow permissions → Read and write**.     |
| `*_error_*.txt` appears in `output/`              | Check the SMILES in that input file — invalid or unsupported structures stop processing. |

## Citation

If you use this pipeline or its results, please cite this work:

> Sakeer, M. R.; Samadhi, K. G. A.; Kotawalagedara, S. K. P.; Kaldera, P. H.; Bodun, D. S.; Friedmann, E.; Kimmell, K.; Maminakis, M.; Aronson, D.; Woster, M.; Sharif, S. Automated Computational Screening of Temperature-Dependent Cannabinoid Solubility in Industrially Relevant Processing Solvents and Lipid Carrier Oils. *Manuscript in preparation*, 2026.

and the underlying solubility method:

> Vermeire, F. H.; Chung, Y.; Green, W. H. Predicting Solubility Limits of Organic Solutes for a Wide Range of Solvents and Temperatures. *J. Am. Chem. Soc.* **2022**, *144*, 10785–10797. https://doi.org/10.1021/jacs.2c01768

```bibtex
@article{vermeire2022solubility,
  title   = {Predicting Solubility Limits of Organic Solutes for a Wide Range of Solvents and Temperatures},
  author  = {Vermeire, Florence H. and Chung, Yunsie and Green, William H.},
  journal = {Journal of the American Chemical Society},
  volume  = {144},
  pages   = {10785--10797},
  year    = {2022},
  doi     = {10.1021/jacs.2c01768}
}
```

## License

This repository is released under the [Mozilla Public License 2.0 (MPL-2.0)](LICENSE).
© 2026 Standard Seed Artificial Intelligence Corporation.

In short: you may use, modify, and distribute this code, including in commercial and closed-source projects. If you modify files from this repository and distribute them, those modified files must remain under MPL-2.0 and their source must be made available. See the [full license text](https://www.mozilla.org/en-US/MPL/2.0/) for the exact terms.

SolProp_ML and the SolProp trained models are third-party software distributed under their own licenses; see the [SolProp_ML repository](https://github.com/fhvermei/SolProp_ML) for terms.

## Contact

- **Study:** Suliman Sharif (corresponding author) — sharifsuliman1@gmail.com
- **Pipeline and code:** Mohammadhu Rifaydheen Sakeer — sakeermr5@gmail.com

You can also open an issue in this repository.

## Acknowledgments

- [SolProp_ML](https://github.com/fhvermei/SolProp_ML) by Florence Vermeire and the Green Group at MIT
- [descriptastorus](https://github.com/bp-kelley/descriptastorus) for molecular descriptors
- [RMG — Reaction Mechanism Generator](https://rmg.mit.edu/) project
