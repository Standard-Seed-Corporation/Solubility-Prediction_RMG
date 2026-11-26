"""Fix the four HHC / HHC-acid SMILES in input/solubility_data_no_stereo.csv
so they match manuscript Table 1 (adds the missing ring carbon).
Run from the repo root:  python fix_hhc_smiles.py"""
path = "input/solubility_data_no_stereo.csv"
fixes = {
    "[C@]([C@@H](C)CC2)": "[C@](C[C@@H](C)CC2)",   # 9(S)-HHC and 9(S)-HHC acid
    "[C@]([C@H](C)CC2)":  "[C@](C[C@H](C)CC2)",    # 9(R)-HHC and 9(R)-HHC acid
}
text = open(path).read()
total = 0
for old, new in fixes.items():
    n = text.count(old)
    print(f"{old} -> {new}: {n} rows")
    text = text.replace(old, new)
    total += n
assert total == 216, f"expected 216 rows (4 solutes x 18 solvents x 3 T), got {total}"
open(path, "w").write(text)
print("Done. 216 rows fixed.")
