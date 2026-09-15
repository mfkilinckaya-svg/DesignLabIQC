import pandas as pd, numpy as np

NAME = {'WBC':'Leukocytes','RBC':'Erythrocytes','Hb':'Hemoglobin','Htc':'Hematocrit',
        'MCV':'MCV','MCH':'MCH','MCHC':'MCHC','RDW':'RDW-CV','PLT':'Platelets',
        'PLT-F':'Platelets, fluorescent','MPV':'MPV','Neutrophil':'Neutrophils, abs.',
        'Lymph':'Lymphocytes, abs.','Mono':'Monocytes, abs.','eos':'Eosinophils, abs.',
        'Basophil':'Basophils, abs.','Retikulosit':'Reticulocytes, abs.','Ret-He':'Ret-He'}

d = pd.read_csv('parsed_dedup.csv')
d = d[d.folder.isin(NAME)].copy()
d['analyte'] = d.folder.map(NAME)
d['target'] = (d.ref_lo + d.ref_hi) / 2          # target in force
d['sd_defined'] = (d.ref_hi - d.ref_lo) / 4      # Beaker range is target +/- 2 SD
d = d.dropna(subset=['verdi','target'])

# Some analytes (RDW-CV) are stored in Excel percentage format, so the raw cell is
# 100x smaller than the reference range. Rescale where the ratio says so.
for an, g in d.groupby('analyte'):
    ratio = (g.target / g.verdi).median()
    if 50 < ratio < 200:
        d.loc[d.analyte == an, 'verdi'] *= 100
        print(f'[scale] {an}: values multiplied by 100 (target/value ratio was {ratio:.1f})')

d['dev'] = d.verdi - d.target

# pooled within-lot, within-instrument SD per analyte/level (common yardstick)
def pooled_sd(g):
    ss = 0.0; df = 0
    for _, gl in g.groupby(['instrument','lot']):
        v = gl['verdi'].values
        if len(v) < 2: continue
        ss += ((v - v.mean())**2).sum(); df += len(v) - 1
    return np.sqrt(ss/df) if df > 0 else np.nan

sd_ref = d.groupby(['analyte','level']).apply(pooled_sd, include_groups=False).rename('sd_pooled')

rows = []
for (an, lv, ins), g in d.groupby(['analyte','level','instrument']):
    sp = sd_ref.loc[(an, lv)]
    mdev = g.dev.mean()
    mtar = g.target.mean()
    rows.append(dict(analyte=an, level=lv, instrument=ins, n=len(g),
                     mean_observed=g.verdi.mean(), target=mtar,
                     deviation=mdev,
                     deviation_pct=100*mdev/mtar if mtar else np.nan,
                     deviation_sd=mdev/sp if sp else np.nan,
                     sd_pooled=sp))
dev = pd.DataFrame(rows)
dev.to_csv('instrument_deviation.csv', index=False)

print('=== Deviation of each analyser mean from the target in force (SD units) ===\n')
piv = dev.pivot_table(index=['analyte','level'], columns='instrument', values='deviation_sd')
piv['max_abs'] = piv.abs().max(axis=1)
piv['spread'] = piv[[c for c in piv.columns if c.startswith('XR')]].max(axis=1) - \
                piv[[c for c in piv.columns if c.startswith('XR')]].min(axis=1)
print(piv.round(2).to_string())

print('\n=== Summary ===')
a = dev.deviation_sd.abs()
print(f'n analyte-level-instrument combinations: {len(dev)}')
print(f'|deviation| median {a.median():.2f} SD, IQR {a.quantile(.25):.2f}-{a.quantile(.75):.2f}, max {a.max():.2f} SD')
for t in (0.5, 1.0, 1.5, 2.0):
    print(f'  |deviation| > {t} SD: {(a>t).sum()} ({100*(a>t).mean():.0f}%)')

print('\n=== Mean signed deviation by analyser (systematic direction) ===')
print(dev.groupby('instrument')['deviation_sd'].agg(['mean','median','count']).round(3).to_string())

print('\n=== Largest 12 absolute deviations ===')
top = dev.reindex(dev.deviation_sd.abs().sort_values(ascending=False).index).head(12)
print(top[['analyte','level','instrument','n','mean_observed','target','deviation_pct','deviation_sd']].round(3).to_string(index=False))
