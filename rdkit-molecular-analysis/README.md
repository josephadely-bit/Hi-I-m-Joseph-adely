# RDKit Molecular Analysis

An introductory cheminformatics project using **RDKit** to calculate molecular descriptors and Morgan fingerprints for a small, transparent set of example molecules. The goal is to demonstrate reproducible scientific Python practices and developing familiarity with molecular representations—not to claim advanced drug-discovery expertise.

## What it demonstrates

- SMILES parsing and molecule validation
- Molecular weight, logP, TPSA, and rotatable-bond calculations
- Morgan fingerprint generation
- CSV export for downstream analysis
- Automated tests for descriptor calculations and invalid input handling

## Run locally

```bash
cd rdkit-molecular-analysis
python -m venv .venv
source .venv/bin/activate       # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python -m src.analyze_molecules
pytest -q
```

The sample molecules are intentionally embedded in the source so the project runs without downloading a dataset. The next iteration could use a licensed public bioactivity dataset and add a descriptor-to-property modeling workflow.

## Structure

```text
rdkit-molecular-analysis/
├── src/analyze_molecules.py
├── tests/test_analyze_molecules.py
├── requirements.txt
└── README.md
```
