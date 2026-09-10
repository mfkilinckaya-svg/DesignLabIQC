# Data dictionary

## `data/qc_measurements_2026-01_2026-07.csv`

One row per control measurement. 75,124 rows. Three Sysmex XR-Series analysers (XR1, XR2, XR3), three control levels (XR CHECK L1, L2, L3), four control lots, 1 January – 31 July 2026. Exported from the laboratory information system (Beaker, Epic), deduplicated, operator identifiers removed. Results that the LIS had excluded from its statistics before export (n = 202) are not present; they are counted per block in `beaker_defined_vs_observed.csv`.

| Column | Type | Meaning |
|---|---|---|
| `analyte` | text | Parameter name as used in the manuscript. 19 values; NRBC abs. is deposited but excluded from the analysis (no traceable allowable error). |
| `unit` | text | Reporting unit. |
| `timestamp` | ISO datetime | Time the control was measured. |
| `analyser` | XR1 / XR2 / XR3 | Instrument. Platelets fluorescent, Reticulocytes and Reticulocyte hemoglobin are measured on XR2 and XR3 only. |
| `level` | L1 / L2 / L3 | Control level. |
| `lot` | integer | Control lot number; the last two digits encode the level (…01, …02, …03). |
| `result` | number | Measured value in `unit`. RDW-CV was stored by the LIS in Excel percentage format and has been rescaled to per cent. |
| `target_in_force` | number | The target value the LIS was using for this measurement, derived as the midpoint of the LIS acceptance range shown with the result. Changes within a lot when the laboratory updated the target. |
| `sd_defined_in_lis` | number | The SD the LIS was using, derived as (range width)/4, because the LIS displays target ± 2 SD. |
| `lis_limit_low`, `lis_limit_high` | number | The LIS acceptance range as displayed (target ± 2 SD). |
| `lis_rule_outcome` | text | The Westgard rules evaluated by the LIS and their outcome, verbatim (Norwegian: *Bestått* = passed, *Mislyktes* = failed). |
| `lis_rejected` | 0/1 | 1 if any LIS rule failed on this measurement. 65 of 75,124. |

## `data/beaker_defined_vs_observed.csv`

One row per control block as summarised by the LIS (analyte × analyser × level × lot × export file). 1,200 rows.

| Column | Meaning |
|---|---|
| `folder`, `file` | Source analyte folder and monthly export file. |
| `instrument`, `level`, `lot` | As above. |
| `inkludert`, `ekskludert` | Number of results included in / excluded from the LIS statistics for that block. |
| `mean_beregnet`, `sd_beregnet`, `cv_beregnet` | Mean, SD and CV calculated by the LIS from the included results. |
| `mean_angitt`, `sd_angitt`, `cv_angitt` | Target mean, SD and CV *defined* in the LIS for that block. |
| `zstat` | LIS z-statistic of the block mean against the defined target. |

The ratio `sd_angitt / sd_beregnet` is the "defined SD versus observed SD" figure reported in the manuscript.

## `data/measured_cv_target_offset.csv`

One row per analyte × level. The values loaded into the rule-design tool.

| Column | Meaning |
|---|---|
| `analyte`, `level` | As above. |
| `instrument` | The analyser with the highest pooled within-lot CV, whose CV is carried forward. |
| `cv` | That CV, per cent. |
| `n` | Number of results contributing to it. |
| `target` | n-weighted pooled mean of all analysers over the study period. |
| `maxdev` | Largest deviation of any analyser mean from that target, in SD units. |
| `bias` | The same, expressed as per cent of target (`maxdev × cv`), as loaded into the tool's *Bias / offset* field. |

## `results/`

| File | Content |
|---|---|
| `final_TEa_and_rules.csv` | Adopted allowable-error source and value, K and n per level, sigma, combined Pfr and Ped, per parameter (manuscript Table 2). |
| `retrospective_rejection_rates.csv` | Per parameter, per event and per measurement, rejection rate with the adopted rules under the shared target as it stood (B), re-centred on the pooled mean (C) and analyser-specific (D) (manuscript Table 3 and Supplementary Table S2). |
| `sigma_spread_by_APS_source.csv` | Per parameter, the lowest and highest TEa and sigma across compared sources and the fold difference (manuscript Figure 1). |
| `instrument_deviation.csv` | Per analyte × level × analyser: n, observed mean, target, deviation in per cent and in SD units (manuscript Figure 3). |
| `deviation_decomposition.csv` | Per analyte × level: worst-case deviation, common component, residual, and fraction removable by re-centring. |
| `cv_verification.csv` | Comparison of the CV computed by the deposited scripts against the laboratory's independent spreadsheet calculation. |
