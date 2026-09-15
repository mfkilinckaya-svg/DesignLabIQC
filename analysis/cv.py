import pandas as pd, numpy as np

d = pd.read_csv('parsed_raw.csv')
d['tidspunkt'] = pd.to_datetime(d['tidspunkt'])
key = ['folder','instrument','level','lot','tidspunkt','verdi']
d = d.drop_duplicates(subset=key)
d = d[(d.tidspunkt >= '2026-01-01') & (d.tidspunkt < '2026-08-01')].copy()
d.to_csv('parsed_dedup.csv', index=False)

# pooled within-lot CV per analyte/level/instrument
def pooled(g):
    ss = 0.0; df = 0; wsum = 0.0; nsum = 0
    for lot, gl in g.groupby('lot'):
        v = gl['verdi'].dropna().values
        if len(v) < 2: continue
        m = v.mean(); s = v.std(ddof=1)
        ss += (len(v)-1)*s*s; df += len(v)-1
        wsum += len(v)*m; nsum += len(v)
    if df <= 0 or nsum == 0: return pd.Series({'cv':np.nan,'n':nsum,'mean':np.nan})
    sd = np.sqrt(ss/df); mean = wsum/nsum
    return pd.Series({'cv':100*sd/mean if mean else np.nan,'n':nsum,'mean':mean})

res = d.groupby(['folder','level','instrument']).apply(pooled, include_groups=False).reset_index()

# highest CV per analyte/level (conservative)
sel = res.loc[res.groupby(['folder','level'])['cv'].idxmax()].reset_index(drop=True)

# user's final seven-month CV table
user = {
 'WBC':      (2.38,1.91,1.75), 'RBC':      (1.08,0.77,0.73),
 'Hb':       (1.04,0.70,0.65), 'Htc':      (1.60,1.13,1.12),
 'MCV':      (1.07,0.83,0.81), 'MCH':      (1.05,0.88,0.75),
 'MCHC':     (1.41,1.13,1.04), 'RDW':      (0.95,0.72,0.65),
 'PLT':      (4.23,2.47,1.56), 'PLT-F':    (2.28,3.49,1.94),
 'MPV':      (2.41,1.63,1.25), 'Neutrophil':(3.40,2.77,2.49),
 'Lymph':    (3.66,2.67,1.91), 'Mono':     (8.16,7.43,5.71),
 'eos':      (6.69,6.71,6.92), 'Basophil': (4.47,3.43,3.04),
 'Retikulosit':(3.50,3.43,4.76),'Ret-He':  (1.11,1.15,1.46),
 'NRBC#':    (9.65,5.42,3.64),
}

print(f"{'Analyte':13s} {'Lvl':4s} {'calc':>7s} {'yours':>7s} {'diff':>7s} {'instr':>6s} {'n':>6s}")
print('-'*60)
rows=[]
for f in sorted(user):
    for i,lv in enumerate(['L1','L2','L3']):
        r = sel[(sel.folder==f)&(sel.level==lv)]
        if r.empty:
            print(f'{f:13s} {lv:4s} {"--":>7s}'); continue
        r = r.iloc[0]
        u = user[f][i]
        diff = r['cv'] - u
        flag = '  <<<' if abs(diff) > 0.15 else ''
        print(f"{f:13s} {lv:4s} {r['cv']:7.2f} {u:7.2f} {diff:+7.2f} {r['instrument']:>6s} {int(r['n']):6d}{flag}")
        rows.append(dict(analyte=f, level=lv, cv_calc=round(r['cv'],3), cv_user=u,
                         diff=round(diff,3), instrument=r['instrument'], n=int(r['n']),
                         mean=round(r['mean'],4)))
pd.DataFrame(rows).to_csv('cv_comparison.csv', index=False)
res.to_csv('cv_all_instruments.csv', index=False)
