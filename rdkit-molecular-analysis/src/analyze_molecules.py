"""Calculate simple molecular descriptors with RDKit."""
from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Iterable

from rdkit import Chem
from rdkit.Chem import Crippen, Descriptors, Lipinski, rdFingerprintGenerator


@dataclass(frozen=True)
class MoleculeRecord:
    name: str
    smiles: str
    molecular_weight: float
    logp: float
    tpsa: float
    rotatable_bonds: int
    fingerprint_bits: int


def analyze_molecule(name: str, smiles: str) -> MoleculeRecord:
    molecule = Chem.MolFromSmiles(smiles)
    if molecule is None:
        raise ValueError(f"Invalid SMILES for {name}: {smiles}")
    generator = rdFingerprintGenerator.GetMorganGenerator(radius=2, fpSize=2048)
    fingerprint = generator.GetFingerprint(molecule)
    return MoleculeRecord(
        name=name,
        smiles=smiles,
        molecular_weight=round(Descriptors.MolWt(molecule), 3),
        logp=round(Crippen.MolLogP(molecule), 3),
        tpsa=round(Descriptors.TPSA(molecule), 3),
        rotatable_bonds=Lipinski.NumRotatableBonds(molecule),
        fingerprint_bits=fingerprint.GetNumOnBits(),
    )


def analyze_examples(molecules: Iterable[tuple[str, str]]) -> list[MoleculeRecord]:
    return [analyze_molecule(name, smiles) for name, smiles in molecules]


def main() -> None:
    examples = [("Caffeine", "Cn1c(=O)c2c(ncn2C)n(C)c1=O"), ("Aspirin", "CC(=O)Oc1ccccc1C(=O)O"), ("Acetaminophen", "CC(=O)NC1=CC=C(O)C=C1")]
    for record in analyze_examples(examples):
        print(asdict(record))


if __name__ == "__main__":
    main()
