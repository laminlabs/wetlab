import pertdb
import pytest


def test_smiles_normalization_on_create():
    """
    On create: sodium acetate 'CC(=O)[O-].[Na+]' should normalize to acetic acid
    without the counterion, have a valid InChIKey, MolWt, and MolFormula.
    """

    # Skip cleanly if RDKit isn't available in the test env
    if not getattr(pertdb.models, "RDKIT_AVAILABLE", False):
        pytest.skip("RDKit not available; skipping SMILES normalization tests.")

    salt_smiles = "CC(=O)[O-].[Na+]"  # sodium acetate (salted form)
    c = pertdb.Compound(name="Sodium acetate (test)", smiles=salt_smiles)
    c.save()  # save() should ensure normalization has run

    assert c.canonical_smiles is not None
    # No salts/solvents (no dot-fragment) after FragmentParent()
    assert "." not in c.canonical_smiles
    # RDKit canonical SMILES for acetic acid is typically "CC(=O)O"
    assert c.canonical_smiles == "CC(=O)O"

    # Derived fields should be populated
    assert c.inchikey is not None and len(c.inchikey) > 0
    assert c.molweight is not None and c.molweight > 0
    # Acetic acid molecular formula
    assert c.molformula in {"C2H4O2"}  # explicit, but keeps it readable


def test_smiles_normalization_on_update():
    """
    update_smiles() should reprocess and refresh canonical fields.
    """
    if not getattr(pertdb.models, "RDKIT_AVAILABLE", False):
        pytest.skip("RDKit not available; skipping SMILES normalization tests.")

    # Start with methane
    c = pertdb.Compound(name="Update test", smiles="C")
    c.save()
    assert c.canonical_smiles == "C"

    # Update to tert-butanol — canonical typically "CC(C)(C)O"
    c.update_smiles("CC(C)(C)O")
    c.refresh_from_db()

    assert c.canonical_smiles == "CC(C)(C)O"
    assert c.inchikey is not None and len(c.inchikey) > 0
    assert c.molweight is not None and c.molweight > 0
    assert c.molformula is not None and len(c.molformula) > 0
