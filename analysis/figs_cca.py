import json, math
import numpy as np, pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from scipy.stats import norm

R = "../results/"
OUT = "../figures/cca/"
panel = json.load(open("panel_from_tool.json"))

plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 8, "axes.linewidth": 0.6,
                     "xtick.major.width": 0.6, "ytick.major.width": 0.6, "pdf.fonttype": 42, "ps.fonttype": 42,
                     "legend.fontsize": 7, "axes.labelsize": 8, "axes.titlesize": 8.5})
MM = 1 / 25.4

# British spelling for labels
REN = {"Hemoglobin": "Haemoglobin", "Hematocrit": "Haematocrit", "Reticulocyte hemoglobin": "Reticulocyte haemoglobin",
       "Ret-He": "Reticulocyte haemoglobin", "Reticulocytes, abs.": "Reticulocytes", "Platelets, fluorescent": "Platelets fluorescent"}
def nm(s):
    s = REN.get(s, s)
    return s.replace(", abs.", " abs.")

# Okabe–Ito
OI = {"blue": "#0072B2", "orange": "#E69F00", "green": "#009E73", "sky": "#56B4E9", "verm": "#D55E00", "purple": "#CC79A7", "yellow": "#F0E442", "black": "#000000"}

def save(fig, name):
    fig.savefig(OUT + name + ".pdf")
    fig.savefig(OUT + name + ".eps")
    fig.savefig(OUT + name + ".tif", dpi=1000, pil_kwargs={"compression": "tiff_lzw"})
    fig.savefig(OUT + name + "_preview.png", dpi=150)
    plt.close(fig)

# ---------------- Figure 1: sigma by APS source ----------------
SRC = [("BV EFLM (optimal)",   "o", OI["blue"],   "none"),
       ("BV EFLM (desirable)", "o", OI["blue"],   "half"),
       ("BV EFLM (minimum)",   "o", OI["blue"],   "full"),
       ("BV Ricos (optimal)",  "s", OI["orange"], "none"),
       ("BV Ricos (desirable)","s", OI["orange"], "half"),
       ("BV Ricos (minimum)",  "s", OI["orange"], "full"),
       ("Noklus",              "^", OI["green"],  "full"),
       ("CLIA 2025",           "D", OI["purple"], "full"),
       ("Rili-BAEK",           "v", OI["verm"],   "full")]
order = [a["name"] for a in panel]  # tool order = Table 2 order
fig, ax = plt.subplots(figsize=(190 * MM, 120 * MM))
ys = np.arange(len(order))[::-1]
for a, y in zip(panel, ys):
    cvmax = max(l["cv"] for l in a["levels"])
    sig = {o["label"]: o["value"] / cvmax for o in a["teaOptions"]}
    vals = list(sig.values())
    ax.plot([min(vals), max(vals)], [y, y], color="#BBBBBB", lw=0.8, zorder=1)
    for lab, mk, col, fill in SRC:
        if lab in sig:
            fc = col if fill == "full" else ("white" if fill == "none" else col)
            alpha = 0.45 if fill == "half" else 1
            ax.scatter(sig[lab], y, marker=mk, s=22, facecolor=fc, edgecolor=col, linewidths=0.8, alpha=alpha, zorder=3)
    ax.scatter(a["tea"] / cvmax, y, marker="|", s=90, color="black", linewidths=1.6, zorder=4)
for x, lab in [(3, "3"), (4, "4"), (6, "6")]:
    ax.axvline(x, color="#999999", lw=0.6, ls=":", zorder=0)
    ax.text(x, len(order) - 0.3, lab, ha="center", va="bottom", fontsize=7, color="#666666")
ax.set_xscale("log"); ax.set_xlim(0.35, 30)
ax.set_xticks([0.5, 1, 2, 3, 4, 6, 10, 20]); ax.set_xticklabels(["0.5", "1", "2", "3", "4", "6", "10", "20"])
ax.set_yticks(ys); ax.set_yticklabels([nm(n) for n in order])
ax.set_ylim(-0.7, len(order) - 0.3)
ax.set_xlabel("Sigma metric (logarithmic scale)")
ax.grid(axis="y", color="#EEEEEE", lw=0.5)
for s in ["top", "right"]: ax.spines[s].set_visible(False)
handles = []
for lab, mk, col, fill in SRC:
    fc = col if fill == "full" else ("white" if fill == "none" else col)
    handles.append(Line2D([], [], marker=mk, ls="", markerfacecolor=fc, markeredgecolor=col, alpha=0.45 if fill == "half" else 1, markersize=5, label=lab))
handles.append(Line2D([], [], marker="|", ls="", color="black", markersize=9, markeredgewidth=1.6, label="Adopted"))
ax.legend(handles=handles, loc="upper center", bbox_to_anchor=(0.5, -0.12), ncol=5, frameon=False, handletextpad=0.3, columnspacing=1.2)
fig.tight_layout()
save(fig, "Figure_1")

# ---------------- Figure 2: OPSpecs MCHC ----------------
mchc = next(a for a in panel if a["name"] == "MCHC")
def d90(k, n):
    # shift (in SD) at which P(reject) = 0.9 for a 1:K rule with n measurements
    return k - norm.ppf(1 - 0.9 ** (1 / n))
LS = ["-", "--", ":"]
fig, axs = plt.subplots(1, 2, figsize=(190 * MM, 80 * MM))
for ax, (tea, title) in zip(axs, [(0.6275581316760657, "Biological variation, optimal tier"), (10.0, "External assessment limit (Noklus)")]):
    xmax = tea / 5 * 1.0 if tea < 1 else 4.3
    x = np.linspace(0, xmax, 200)
    for l, ls, col in zip(mchc["levels"], LS, [OI["blue"], OI["orange"], OI["green"]]):
        slope = d90(l["k"], l["n"]) + 1.65
        y = tea - slope * x
        ax.plot(x, np.clip(y, 0, None), ls=ls, color="black", lw=1, label=f'{l["label"]}: K {l["k"]:g}, n {l["n"]}')
        ax.scatter(l["cv"], 0.0, marker="o", s=30, facecolor="white", edgecolor=col, linewidths=1.2, zorder=4, clip_on=False)
        ax.annotate(l["label"], (l["cv"], 0.0), xytext=(0, 5), textcoords="offset points", ha="center", fontsize=7, color=col)
    ax.fill_between(x, 0, np.clip(tea - (d90(mchc["levels"][0]["k"], 2) + 1.65) * x, 0, None), color="#DDDDDD", zorder=0)
    ax.set_xlim(0, xmax if tea > 1 else 2.0); ax.set_ylim(0, tea * 1.08)
    ax.set_xlabel("Imprecision, CV (%)"); ax.set_ylabel("Bias (%)")
    ax.set_title(f"{title}\nTEa {tea:.2f}%" if tea < 1 else f"{title}\nTEa {tea:.0f}%")
    ax.legend(frameon=False, loc="upper right")
    for s in ["top", "right"]: ax.spines[s].set_visible(False)
fig.tight_layout()
save(fig, "Figure_2")

# ---------------- Figure 3: analyser deviation ----------------
dev = pd.read_csv(R + "instrument_deviation.csv")
dev["analyte"] = dev["analyte"].map(nm)
orderA = dev.groupby("analyte")["deviation_sd"].apply(lambda s: s.abs().max()).sort_values(ascending=False).index.tolist()
INST = {"XR1": ("o", OI["blue"]), "XR2": ("s", OI["orange"]), "XR3": ("^", OI["green"])}
fig, ax = plt.subplots(figsize=(190 * MM, 150 * MM))
y = 0; ticks = []; labs = []
for an in orderA:
    for lv in ["L1", "L2", "L3"]:
        sub = dev[(dev.analyte == an) & (dev.level == lv)]
        if len(sub):
            ax.plot([sub.deviation_sd.min(), sub.deviation_sd.max()], [y, y], color="#BBBBBB", lw=0.8, zorder=1)
            for _, r in sub.iterrows():
                mk, col = INST[r.instrument]
                ax.scatter(r.deviation_sd, y, marker=mk, s=16, facecolor=col, edgecolor="black", linewidths=0.3, zorder=3)
            ticks.append(y); labs.append(f"{an}  {lv}" if lv == "L1" else lv)
        y -= 1
    y -= 0.6
for x in [-2, -1, 1, 2]: ax.axvline(x, color="#CCCCCC", lw=0.6, ls=":", zorder=0)
ax.axvline(0, color="black", lw=0.7, zorder=0)
ax.set_yticks(ticks); ax.set_yticklabels(labs, fontsize=6.5)
ax.set_ylim(y + 0.6, 1); ax.set_xlabel("Deviation of the analyser mean from the target in force (SD units)")
for s in ["top", "right"]: ax.spines[s].set_visible(False)
ax.legend(handles=[Line2D([], [], marker=m, ls="", markerfacecolor=c, markeredgecolor="black", markeredgewidth=0.3, markersize=5, label=k) for k, (m, c) in INST.items()],
          loc="lower right", frameon=False)
fig.tight_layout()
save(fig, "Figure_3")

# ---------------- Figure 4: observed vs predicted ----------------
obs = pd.read_csv(R + "retrospective_rejection_rates.csv")
pred = pd.read_csv(R + "final_TEa_and_rules.csv")
nev = dev.groupby(["analyte", "instrument"])["n"].max().groupby("analyte").sum()
obs["Analyte"] = obs["Analyte"].map(nm); pred["Analyte"] = pred["Analyte"].map(nm)
m = obs.merge(pred[["Analyte", "Pfr %"]], on="Analyte")
m["n"] = m["Analyte"].map(nev)
p = m["C_event"] / 100
m["ci"] = 1.96 * np.sqrt(p * (1 - p) / m["n"]) * 100
above = m[m["C_event"] - m["ci"] > m["Pfr %"]]
fig, ax = plt.subplots(figsize=(130 * MM, 105 * MM))
ax.plot([0, 3.2], [0, 3.2], ls="--", color="#777777", lw=0.8, zorder=0)
ax.errorbar(m["Pfr %"], m["C_event"], yerr=m["ci"], fmt="o", ms=4, color=OI["blue"], ecolor="#999999", elinewidth=0.7, capsize=2, zorder=3)
from adjustText import adjust_text
big = m[(m["C_event"] > 0.6) | (m["Pfr %"] > 0.8)]
small = m[~m.index.isin(big.index)]
texts=[]
for _, r in big.iterrows():
    hi = r.Analyte in above.Analyte.values
    texts.append(ax.text(r["Pfr %"], r.C_event, r.Analyte, fontsize=6.5, color=OI["verm"] if hi else "#333333", fontweight="bold" if hi else "normal"))
adjust_text(texts, x=big["Pfr %"].values, y=big["C_event"].values, ax=ax, expand=(1.2, 1.5),
            arrowprops=dict(arrowstyle="-", color="#999999", lw=0.5), only_move={"text": "xy", "points": "", "explode": "xy"})
ax.add_patch(plt.Rectangle((-0.03, -0.06), 0.62, 0.72, fill=False, ec="#888888", lw=0.6, ls="-"))
ins = ax.inset_axes([0.08, 0.56, 0.42, 0.42])
ins.plot([0, 0.7], [0, 0.7], ls="--", color="#777777", lw=0.7, zorder=0)
ins.errorbar(small["Pfr %"], small["C_event"], yerr=small["ci"], fmt="o", ms=3, color=OI["blue"], ecolor="#999999", elinewidth=0.6, capsize=1.5, zorder=3)
zero = small[small["C_event"] == 0]; nz = small[small["C_event"] > 0]
t2=[ins.text(r["Pfr %"], r.C_event, r.Analyte, fontsize=5.5, color="#333333") for _, r in nz.iterrows()]
ins.annotate("No rejections observed:\n" + ", ".join(zero.Analyte), (zero["Pfr %"].mean(), 0), xytext=(0.36, 0.62), fontsize=5.5, color="#555555", ha="left", va="top", arrowprops=dict(arrowstyle="-", color="#999999", lw=0.4))
adjust_text(t2, x=nz["Pfr %"].values, y=nz["C_event"].values, ax=ins, expand=(1.3, 1.8),
            arrowprops=dict(arrowstyle="-", color="#999999", lw=0.4), only_move={"text": "xy", "points": "", "explode": "xy"})
ins.set_xlim(-0.03, 0.62); ins.set_ylim(-0.06, 0.72); ins.tick_params(labelsize=6, length=2)
ins.set_title("Detail near the origin", fontsize=6.5, pad=2)
for sp in ["top", "right"]: ins.spines[sp].set_visible(False)
ax.set_xlim(-0.05, 1.8); ax.set_ylim(-0.1, 3.2)
ax.set_xlabel("Predicted false rejection per control event (%)"); ax.set_ylabel("Observed rejection per control event (%)")
for s in ["top", "right"]: ax.spines[s].set_visible(False)
fig.tight_layout()
try:
    from adjustText import adjust_text
except ImportError:
    pass
save(fig, "Figure_4")
print(m[["Analyte", "Pfr %", "C_event", "ci", "n"]].to_string())
