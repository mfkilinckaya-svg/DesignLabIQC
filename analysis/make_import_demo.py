"""Build the small import file used in Supplementary Video 2 from the deposited measurements."""
import pandas as pd
d = pd.read_csv('../data/qc_measurements_2026-01_2026-07.csv')
d = d[d.analyte.isin(['MCHC', 'Leukocytes', 'Platelets fluorescent'])]
out = d[['analyte', 'level', 'lot', 'analyser', 'result']].rename(columns={'analyser': 'instrument'})
out.to_csv('../docs/import_demo.csv', index=False)
print(len(out), 'rows written to docs/import_demo.csv')
