# Supplementary Video 2 — Using the rule-design tool

**Length:** 4 min 24 s. **Language:** English narration and captions; subtitles in `videos/Supplementary_Video_2_tool_walkthrough.srt`.
**Purpose:** show that the spreadsheet's logic runs live in the browser tool, and walk through one parameter end to end on the laboratory's own data.
**Recording:** `tool/iqc-rule-designer.html` served locally and driven in headless Chromium at 1920 × 1080 (`videos/source/record2.py`), with a rendered cursor and caption bar; no browser chrome.

The walkthrough uses MCHC, because it is the parameter where the choice of specification matters most and where the target offset is largest. The import step uses `docs/import_demo.csv` (MCHC, Leukocytes and Platelets fluorescent from the deposited measurements; built by `analysis/make_import_demo.py`).

This file is the script *as recorded*.

---

## Scene 1 (0:00–0:30)

**On screen.** Page top (title, tabs, settings bar, Import/Export). Scroll to MCHC; cursor on the header badges σ, False alarms, Detection.

**Caption card.** *One file. Runs in the browser. Nothing leaves your computer.*

**Narration.**
This is the rule-design tool. It is a single file; you open it in a browser and it runs there, without installing anything and without sending data anywhere. It comes loaded with our eighteen-parameter panel. Each parameter has a header that summarises the state of its rule: the sigma metric, the combined false rejection rate, the same rate once an analyser offset is known, and the combined detection rate. Green means the criterion is met, red means it is not.

---

## Scene 2 (0:30–1:04)

**On screen.** MCHC level table; cursor moves across the column headers Target, CV, Bias / offset, Controls, Rule (K), Sigma, Critical shift, False alarm, Offset (SD), False alarm offset, Detection, Action limit, SD for LIS.

**Caption card.** *Every column is a spreadsheet column. Same formulas, live.*

**Narration.**
The table has one row per control level. The white boxes are inputs: target, CV, bias, number of controls and K. Everything else is calculated as you type. The columns are the same as in the spreadsheet: sigma, the critical shift, false rejection, detection, the action limit in concentration units and the SD to enter in the laboratory system. Two columns are new: the analyser's offset from the target in SD units, and the false rejection rate you actually get once that offset is included.

---

## Scene 3 (1:04–1:46)

**On screen.** “Same measurement, different specification” strip. Click BV EFLM (optimal): σ 0.4, critical shift −1.20, Detection 0 %, header red. Click Noklus: σ 7.1, everything back.

**Caption card.** *Same CV, same rule. Only the specification changed.*

**Narration.**
Here is the point of the whole study, in one control. This strip lists every allowable-error source we could trace for MCHC, computed from the same biological-variation data or taken from the published limit. Choose the tightest, and sigma falls below one; the critical shift is negative, and detection collapses to zero. The noise of the method already exceeds the allowable error, and no rule can work. Choose the external assessment limit, and the same analyser, the same CV and the same rule sit at sigma seven with full detection. Nothing about the measurement changed. Only the specification did. The tool shows you the consequence before you commit to a source.

---

## Scene 4 (1:46–2:25)

**On screen.** L1 K set to 2: False alarms 9.65 %, header red. Search for rules → K = 2.7 / 4 / 3.5, false alarms 1.49 %, detection 100 % → Apply. Cursor on the budget meter.

**Caption card.** *Search for rules: the smallest change to the rule that keeps the budget and meets detection.*

**Narration.**
You can set K by hand and see the effect immediately. Tighten level one to two SD, and the false rejection rate for the event jumps to almost ten per cent; the header turns red. Or you can let the tool search. The search looks for the rule set that stays within the false rejection budget, one and a half per cent per event by default, and meets the detection requirement for that parameter. Among those it picks the one closest to the rule you already have, so it does not rearrange a scheme that is already working. Here it moves level one only as far as it must, and pays for it by widening the other two. The meter shows how much of the budget each level is spending.

---

## Scene 5 (2:25–3:10)

**On screen.** Import results → docs/import_demo.csv. Status: “Imported 3 analytes, updated 3 in the panel”. MCHC L1: CV 1.41, target 32.98, bias 1.14 %; Offset (SD) 0.81; False alarm, offset 5.82 %; header “With offset 6.85 %”.

**Caption card.** *From an export to a rule: CV, target and offset, all from your own data.*

**Narration.**
The tool is not limited to our panel. Export your control results with analyte, level, lot, analyser and value, and load them. For each parameter and level it computes the pooled within-lot CV of each analyser and carries the highest forward; sets the target to the pooled mean of all your analysers; and reports how far the worst analyser sits from that target. That offset is written into the bias field, so the false rejection rate you see is the one you will actually get, not the one you would get if every analyser were perfectly centred. For MCHC, the worst analyser sits zero point eight SD from the pooled target, and the level-one false rejection rate with that offset is several times the nominal rate.

---

## Scene 6 (3:10–3:49)

**On screen.** Bias / offset at L1 changed from 1.14 to 2.61 % (the offset the worst analyser would have against the old LIS target 32.50): Offset (SD) 1.85, False alarm unchanged, False alarm offset up sharply, header With offset 36.4 %. Restored to 1.14.

**Caption card.** *Move the target, and the false alarm rate moves with it. The rule did not change.*

**Narration.**
Now suppose the target were the value the laboratory system had in force, 32.5, instead of the pooled mean of 32.98. The worst analyser would then sit almost half a unit further away, about two point six per cent. Enter that as the offset. The rule has not changed, the CV has not changed, and the plain false rejection column does not move, but the rate with the offset climbs sharply. That is what happened in our retrospective test: the same rules rejected two and a half per cent of control events against the old targets, and under one per cent once the targets were re-centred. The tool lets you see that before it happens.

---

## Scene 7 (3:49–4:11)

**On screen.** Export CSV; the file is shown as a table (one row per level with K, action limit, SD for LIS). Method and references tab.

**Caption card.** *Export gives you the SD to enter in your LIS. The Method tab documents every formula.*

**Narration.**
When you are satisfied, export. The file has one row per level with the rule, the action limit, and the SD to enter in your laboratory system so that its own three-SD rule lands on your limit. The Method and references tab inside the tool documents every calculation, with the same formulas as the spreadsheet and the references behind them.

---

## Closing card (4:14–4:24)

*iqc-rule-designer · single-file HTML · MIT licence · Repository DOI: to be added*
