# Haematology IQC rule design from laboratory imprecision

Data, code and tools accompanying the manuscript

> *Deriving haematology control rules from laboratory imprecision: the decisive role of the allowable error source.*
> Submitted to *Clinica Chimica Acta*, 2026.

The central claim is that internal quality control rules should be derived from the imprecision a laboratory actually measures and from a target taken from its own pooled analyser mean, not from manufacturer-assigned ranges; and that for several haematology parameters whether a rule looks attainable at all depends more on the chosen allowable-error source than on the analyser.

## What is here

| Folder | Content |
|---|---|
| `excel/` | **`Kontrolregler_v1.1_template.xlsx`** — the laboratory's rule-design spreadsheet (Norwegian). Blank template with all formulas: TEa in SD units, critical shift, Pfr, Ped, combined Pfr/Ped across three levels, action limit, and the SD to enter in the LIS. This is the primary tool; the HTML below implements the same formulas. `BV_CVI_CVG_input_template.xlsx` — template for entering CVI/CVG from the EFLM and Ricos biological-variation databases; computes the optimal/desirable/minimum TEa tiers. |
| `tool/` | **`iqc-rule-designer.html`** — single-file browser tool, no installation, no network. Preloaded with the 18-parameter panel, measured imprecision, pooled targets and adopted rules. Accepts a control-result export (`.xlsx`/`.csv`) and recomputes CV, pooled target and analyser offset. `iqc-rule-designer.jsx` — source. |
| `data/` | `qc_measurements_2026-01_2026-07.csv` — all 75,124 control results, 19 parameters, three Sysmex XR-Series analysers, 1 Jan–31 Jul 2026 (operator identifiers removed). `beaker_defined_vs_observed.csv` — per control block, the SD defined in the LIS against the SD observed. `measured_cv_target_offset.csv` — the per-level values loaded into the tool. See `docs/DATA_DICTIONARY.md`. |
| `analysis/` | Python scripts that reproduce every number in the manuscript from `data/`: parsing (`parse.py`), imprecision (`cv.py`), analyser deviation and its decomposition (`deviation.py`), APS-source hierarchy and rule selection (`hier2.py`), figures (`fig3.py`, `figs.py`). |
| `results/` | Outputs of the analysis: final TEa source and rule per parameter, retrospective rejection rates under three target configurations, sigma spread across APS sources, analyser deviations. |
| `figures/` | Figures 1–4 of the manuscript. Root: grayscale, 300 dpi TIFF with PNG previews (original submission). `cca/`: colour versions as vector PDF and 1000 dpi TIFF, produced by `analysis/figs_cca.py`. |
| `docs/` | Data dictionary; scripts (as recorded) of the two supplementary videos; `import_demo.csv` used in Video 2. |
| `videos/` | **Supplementary Video 1** (concept, 4:35) and **Supplementary Video 2** (tool walkthrough, 4:24), MP4 1080p with English narration and captions, plus `.srt` subtitles. `source/video_sources.zip` regenerates both videos. |

## Reproducing the analysis

```bash
pip install pandas numpy openpyxl matplotlib
cd analysis
python parse.py        # expects the raw Beaker exports under data/Data/<analyte>/*.xlsx (not deposited; see note)
python cv.py
python deviation.py
python hier2.py        # ~20 min: exhaustive rule search per parameter
python figs.py && python fig3.py
python figs_cca.py      # colour vector figures from results/ and the tool's panel data
```

The raw monthly Beaker exports are not deposited because they carry operator names; the deduplicated, anonymised result set they reduce to is `data/qc_measurements_2026-01_2026-07.csv`, and every script downstream of `parse.py` runs from that file.

## Using the tool on your own data

Open `tool/iqc-rule-designer.html` in a browser. Prepare an export with columns `analyte, level, lot, instrument, result` (an example of the expected shape is the deposited measurements file) and load it with **Import results**. The tool computes, per parameter and level, the pooled within-lot CV of the worst analyser, the pooled mean across analysers as the target, and each analyser's offset from that target in SD units; select an allowable-error source, and read off sigma, critical shift, false rejection (with and without the offset) and detection for the rule shown. **Search rules** finds the K per level that keeps the combined false rejection within the budget while meeting the detection requirement. **Export** writes the rules and the SD to enter in your LIS.

## Citation

If you use the data or tools, please cite the manuscript above and this repository:

> Kilinckaya M. Haematology IQC rule design from laboratory imprecision: data, analysis code and rule-design tools. Zenodo; 2026. https://doi.org/10.5281/zenodo.22685381

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.22685381.svg)](https://doi.org/10.5281/zenodo.22685381)

## Licence

Code (`analysis/`, `tool/*.jsx`, `tool/*.html`): MIT. Data, spreadsheets, figures and documents: CC BY 4.0. See `LICENSE`.
