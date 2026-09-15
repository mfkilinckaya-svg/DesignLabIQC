import pandas as pd, numpy as np, json, math
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

plt.rcParams.update({'font.family': 'DejaVu Sans', 'font.size': 8,
                     'axes.linewidth': 0.6, 'xtick.major.width': 0.6, 'ytick.major.width': 0.6})
OUT = '/mnt/user-data/outputs/'

# ---- rebuild the source table ----
h = open('hier2.py', encoding='utf-8').read()
ns = {}
exec(h[:h.index('GRID=')], ns)
exec('def sources(a):\n' + h[h.index('def sources(a):') + len('def sources(a):\n'):h.index('def min_change')], ns)
sources, CV = ns['sources'], ns['CV']
F = {x['analyte']: x for x in json.load(open('final_assignment.json'))}

# ================= FIGURE 1 =================
SRC = ['BV EFLM (optimal)', 'BV EFLM (desirable)', 'BV EFLM (minimum)',
       'BV Ricos (optimal)', 'BV Ricos (desirable)', 'BV Ricos (minimum)',
       'Noklus', 'CLIA 2025', 'Rili-BAEK']
MK = {'BV EFLM (optimal)': ('o', 'white'), 'BV EFLM (desirable)': ('o', '0.6'), 'BV EFLM (minimum)': ('o', 'black'),
      'BV Ricos (optimal)': ('s', 'white'), 'BV Ricos (desirable)': ('s', '0.6'), 'BV Ricos (minimum)': ('s', 'black'),
      'Noklus': ('^', 'black'), 'CLIA 2025': ('D', 'white'), 'Rili-BAEK': ('v', '0.6')}

rows = []
for a in CV:
    worst = max(CV[a])
    for k, v in sources(a).items():
        rows.append(dict(analyte=a, source=k, sigma=v / worst))
s1 = pd.DataFrame(rows)
order = s1.groupby('analyte')['sigma'].apply(lambda s: s.max() / s.min()).sort_values(ascending=False).index.tolist()
ypos = {a: i for i, a in enumerate(order)}

fig, ax = plt.subplots(figsize=(6.7, 6.9))
for t in (3, 4, 6):
    ax.axvline(t, color='0.65', lw=0.6, ls='--', zorder=0)
    ax.text(t, -0.9, str(t), ha='center', va='bottom', fontsize=7, color='0.35')
for a in order:
    g = s1[s1.analyte == a]
    ax.plot([g.sigma.min(), g.sigma.max()], [ypos[a]] * 2, color='0.75', lw=0.7, zorder=1)
for _, r in s1.iterrows():
    m, fc = MK[r.source]
    ax.plot(r.sigma, ypos[r.analyte], marker=m, ms=4.2, mec='black', mfc=fc, mew=0.6, ls='none', zorder=3)
# mark the adopted source
for a in order:
    ad = F[a]['source']
    v = s1[(s1.analyte == a) & (s1.source == ad)]
    if len(v):
        ax.plot(v.sigma.iloc[0], ypos[a], marker='|', ms=11, color='black', mew=1.1, zorder=4)

ax.set_xscale('log')
ax.set_xticks([0.5, 1, 2, 3, 4, 6, 10, 20])
ax.get_xaxis().set_major_formatter(matplotlib.ticker.ScalarFormatter())
ax.set_yticks(range(len(order)))
ax.set_yticklabels(order, fontsize=7.5)
ax.invert_yaxis()
ax.set_ylim(len(order) - 0.3, -1.4)
ax.set_xlabel('Sigma metric (logarithmic scale)', fontsize=8)
for sp in ('top', 'right'):
    ax.spines[sp].set_visible(False)
handles = [Line2D([], [], marker=MK[s][0], ls='none', ms=4.2, mec='black', mfc=MK[s][1], mew=0.6, label=s) for s in SRC]
handles.append(Line2D([], [], marker='|', ls='none', ms=9, color='black', mew=1.1, label='adopted'))
ax.legend(handles=handles, loc='upper center', bbox_to_anchor=(0.5, -0.11), frameon=False,
          fontsize=6.8, ncol=4, handletextpad=0.4, columnspacing=1.0)
fig.tight_layout()
fig.savefig(OUT + 'Figure1_sigma_by_APS_source.tif', dpi=300, format='tiff', pil_kwargs={'compression': 'tiff_lzw'})
fig.savefig(OUT + 'Figure1_sigma_by_APS_source.png', dpi=300)
plt.close(fig)
print('Figure 1 done')

# ================= FIGURE 2 =================
def gser(x):
    t = .5; r = 2.; n = r
    for _ in range(200):
        t += 1; n *= x / t; r += n
        if abs(n) < abs(r) * 1e-16: break
    return r * math.exp(-x + .5 * math.log(x) - .5723649429247001)
def gcf(x):
    n = x + .5; a = 1 / 1e-300; i = 1 / n; o = i
    for s in range(1, 301):
        l = -s * (s - .5); n += 2; i = l * i + n
        if abs(i) < 1e-300: i = 1e-300
        a = n + l / a
        if abs(a) < 1e-300: a = 1e-300
        i = 1 / i; u = i * a; o *= u
        if abs(u - 1) < 1e-16: break
    return o * math.exp(-x + .5 * math.log(x) - .5723649429247001)
def erfc_(e):
    if e < 0: return 2 - erfc_(-e)
    t = e * e
    return 1 - gser(t) if t < 1.5 else gcf(t)
Phic = lambda e: .5 * erfc_(e / math.sqrt(2))
cdf = lambda e: 1 - Phic(e) if e >= 0 else Phic(-e)
insd = lambda k, d: cdf(k - d) - cdf(-k - d)
ped = lambda k, n, s: 1 - insd(k, s) ** n if s > 0 else 0.

def shift_for(k, n, want=0.90):
    lo, hi = 0., 30.
    if ped(k, n, hi) < want: return None
    for _ in range(80):
        mid = (lo + hi) / 2
        if ped(k, n, mid) < want: lo = mid
        else: hi = mid
    return hi

A = 'MCHC'
cvs = CV[A]; Ks = F[A]['K']; Ns = F[A]['n']
_u = pd.read_csv('tool_update_values.csv')
BIAS = [float(_u[(_u.analyte == A) & (_u.level == l)].bias.iloc[0]) for l in ('L1', 'L2', 'L3')]
panels = [('Biological variation, optimal tier', 0.63), ('External assessment limit (Noklus)', 10.0)]
fig, axes = plt.subplots(1, 2, figsize=(6.7, 3.3))
sty = [('-', 'black'), ('--', '0.35'), (':', '0.15')]
mks = ['o', 's', '^']
for pi, (ax, (title, tea)) in enumerate(zip(axes, panels)):
    xmax = max(max(cvs) * 1.5, tea / 2.2)
    for i, (k, n, lab) in enumerate(zip(Ks, Ns, ['L1', 'L2', 'L3'])):
        sh = shift_for(k, n)
        if sh is None: continue
        slope = sh + 1.65
        xs = np.linspace(0, min(xmax, tea / slope), 60)
        ax.plot(xs, tea - xs * slope, ls=sty[i][0], color=sty[i][1], lw=1.2,
                label=f'{lab}: K {k:g}, n {n}')
    sh0 = shift_for(Ks[0], Ns[0]); sl0 = sh0 + 1.65
    xf = np.linspace(0, min(xmax, tea / sl0), 60)
    ax.fill_between(xf, 0, tea - xf * sl0, color='0.88', zorder=0)
    for i, (c, b) in enumerate(zip(cvs, BIAS)):
        ax.plot(c, b, marker=mks[i], ms=5.5, mec='black', mfc='white', mew=0.9, ls='none', zorder=5)
        ax.annotate(['L1', 'L2', 'L3'][i], (c, b), textcoords='offset points',
                    xytext=(-9 if i == 2 else 0, 7 if i != 2 else -3),
                    ha='center', fontsize=7)
    ax.set_xlim(0, xmax); ax.set_ylim(0, max(tea, max(BIAS) * 1.25))
    ax.set_title(f'{title}\nTEa {tea:g}%', fontsize=8)
    ax.set_xlabel('Imprecision, CV (%)', fontsize=8)
    ax.legend(frameon=False, fontsize=6.8, handlelength=2.2,
              loc='lower right' if pi == 0 else 'upper right')
    for sp in ('top', 'right'): ax.spines[sp].set_visible(False)
axes[0].set_ylabel('Bias (%)', fontsize=8)
fig.tight_layout()
fig.savefig(OUT + 'Figure2_operating_specifications_MCHC.tif', dpi=300, format='tiff', pil_kwargs={'compression': 'tiff_lzw'})
fig.savefig(OUT + 'Figure2_operating_specifications_MCHC.png', dpi=300)
plt.close(fig)
print('Figure 2 done')

# ================= FIGURE 4 =================
ev = pd.read_csv('retro_events.csv')
pts = []
for a, g in ev.groupby('analyte'):
    n = len(g); k = int(g.out_pooled.sum())
    p = k / n
    lo = 0. if k == 0 else max(0., p - 1.96 * math.sqrt(p * (1 - p) / n))
    hi = min(1., p + 1.96 * math.sqrt(max(p * (1 - p), 1e-9) / n)) if k else 3.0 / n
    pts.append(dict(analyte=a, pred=F[a]['pfr'], obs=100 * p, lo=100 * lo, hi=100 * hi, n=n))
p4 = pd.DataFrame(pts)

fig, ax = plt.subplots(figsize=(5.2, 5.0))
mx = max(p4.pred.max(), p4.hi.max()) * 1.12
ax.plot([0, mx], [0, mx], color='0.4', lw=0.8, ls='--', zorder=1)
ax.errorbar(p4.pred, p4.obs, yerr=[p4.obs - p4.lo, p4.hi - p4.obs], fmt='none',
            ecolor='0.55', elinewidth=0.7, capsize=2, zorder=2)
ax.plot(p4.pred, p4.obs, marker='o', ms=4.6, mec='black', mfc='white', mew=0.8, ls='none', zorder=3)
for _, r in p4.iterrows():
    if r.lo > r.pred or r.hi < r.pred:
        ax.annotate(r.analyte, (r.pred, r.obs), textcoords='offset points', xytext=(5, 3), fontsize=6.5)
ax.set_xlim(0, mx); ax.set_ylim(0, mx)
ax.set_xlabel('Predicted false rejection per control event (%)', fontsize=8)
ax.set_ylabel('Observed rejection per control event (%)', fontsize=8)
for sp in ('top', 'right'): ax.spines[sp].set_visible(False)
fig.tight_layout()
fig.savefig(OUT + 'Figure4_observed_vs_predicted.tif', dpi=300, format='tiff', pil_kwargs={'compression': 'tiff_lzw'})
fig.savefig(OUT + 'Figure4_observed_vs_predicted.png', dpi=300)
plt.close(fig)
print('Figure 4 done')
print(p4.round(3).to_string(index=False))
