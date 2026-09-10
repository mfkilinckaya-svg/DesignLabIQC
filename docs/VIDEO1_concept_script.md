# Supplementary Video 1 — How a control rule should be built

**Length:** 4 min 35 s. **Language:** English narration and captions; subtitles in `videos/Supplementary_Video_1_control_rule_concept.srt`.
**Purpose:** explain the reasoning the spreadsheet and the tool implement, so that a viewer understands *why* the rule is derived from measured imprecision, before seeing *how* the tool does it.

The structure follows the columns of `Kontrolregler_v1.1_template.xlsx` left to right; the active column is highlighted in a strip at the top of every scene. All numbers shown are computed from the deposited data (`data/`). The narration is synthetic (Piper TTS); the video is fully generated from `videos/source/` and can be regenerated.

This file is the script *as recorded*.

---

## Scene 1 (0:00–0:22)

**On screen.** Two control charts, Laboratory A and B, same 40 results (last 12 shifted by 2 SD). A: limits at ±7 SD of the observed scatter (assigned range) — the shift passes. B: limits at ±2.5 SD — the shift is caught, with some noise.

**Caption card.** *Two laboratories. Same analyser. Same results. Different limits.*

**Narration.**
Every laboratory that runs a control material has to decide where to put the limits. Put them wide and nothing ever fails: the chart looks calm, but a real shift would pass unnoticed. Put them tight and the chart flags something every week, most of it noise. The question is not whether to have limits. It is where they come from.

---

## Scene 2 (0:22–0:54)

**On screen.** Illustrative package-insert card (assigned value, assigned range = target ± 6 %) beside column P `= target × percentage / 100`. Then a bar chart: SD defined in the LIS ÷ SD observed, median per parameter (1.3× neutrophils to 7.1× MPV).

**Caption card.** *The assigned range is a promise about the material. It is not a measurement of your analyser.*

**Narration.**
Most limits are taken from the control manufacturer's assigned range. That range is set to cover many laboratories, many analysers and many lots. It is deliberately wide. On our own analysers, the range defined in the laboratory system was between one and a half and seven times wider than the scatter we actually observed. A limit seven times wider than the noise cannot detect a shift of one or two standard deviations. It is not a control; it is a formality.

---

## Scene 3 (0:54–1:23)

**On screen.** Column D highlighted. MCHC level 1, 1 154 results, three analysers, four lots with their targets. Points collapse into one strip per analyser (lot target subtracted); CV 1.41 / 1.40 / 1.38 %; XR1 picked → column D = 1.41.

**Caption card.** *CV = your own scatter, pooled within lot, worst analyser.*

**Narration.**
The alternative starts with one number: the coefficient of variation your own analyser actually produces, on the control level you actually run. We compute it within each control lot, so that a change of target at a lot change does not inflate it, and we pool across the lots. Where three analysers share a rule, we take the highest CV. That is the conservative choice: a rule that works on the worst analyser works on the others.

---

## Scene 4 (1:23–1:54)

**On screen.** Column E: list of traceable sources for MCHC (EFLM optimal 0.6, desirable 1.3, minimum 1.9, Ricos minimum 1.9, Noklus 10 %). Column F `= E / D = 10 / 1.41 = 7.09 SD`; normal curve at 0 with the allowable-error line at 7.09 SD.

**Caption card.** *TEa ÷ CV = how many standard deviations you have to spend.*

**Narration.**
The second number is the allowable total error: how much a result may be wrong before it matters clinically. This is a specification, not a measurement, and it comes from published sources: biological variation, external quality schemes, regulators. Dividing it by your CV gives the allowable error in standard deviations. This is the sigma metric. It says how much room there is between the noise of the method and the point where the error becomes a problem.

---

## Scene 5 (1:54–2:25)

**On screen.** Column H `= F − G − 1.65`. The curve slides right until 5 % of its area crosses the allowable-error line; the distance is labelled critical shift = 5.44 SD. Second panel: EFLM minimum → 1.35 SD − 1.65 = −0.30 SD, already 9 % outside with no shift.

**Caption card.** *Critical shift = TEa in SD − 1.65. The shift a rule must catch.*

**Narration.**
Not all of that room is available. If the method shifts, five per cent of results will exceed the allowable error once the shift reaches the allowable error minus one point six five standard deviations. That is the critical shift: the smallest shift the control rule has to catch. If it comes out negative, no rule can catch it, because the noise alone already exceeds the allowable error. That is what happens to MCHC under the tightest biological-variation specification.

---

## Scene 6 (2:25–3:06)

**On screen.** Columns I (n = 2) and J (K, slider). Leukocytes level 1 (critical shift 2.55 SD). Left: curve on target, tails outside ±K = Pfr. Right: curve shifted by 2.55 SD, area outside ±K = Ped. K sweeps 2.0 → 4.0 → 3.0 with both values live. Budget banner: combined Pfr < 1.5 % per event.

**Caption card.** *Pfr: rule fires, nothing wrong. Ped: rule fires, real shift. You cannot lower one without lowering the other.*

**Narration.**
A rule is a limit at K standard deviations and a count n of control results per event. Two things follow. The chance the rule fires when nothing is wrong, false rejection, P F R, depends only on K and n. The chance it fires when the critical shift has happened, error detection, P E D, depends on K, n and the critical shift. Tighten K and P E D goes up, but so does P F R. The whole design is choosing where on that trade-off to sit. We set a budget: false rejection under one and a half per cent per control event, combined across all three levels.

---

## Scene 7 (3:06–3:30)

**On screen.** Columns M, N: `= 1 − (1−K6)(1−K7)(1−K8)` = 1.49 % for three levels at 0.5 %. Three curves side by side; four control events drop in, one level lands outside → whole run rejected.

**Caption card.** *Any level can reject the run, so the budget is spent across all three.*

**Narration.**
The three levels are measured together, and any one of them can reject the run. So the probabilities combine. A rule that costs half a per cent at each level costs one and a half per cent for the event. That is why the budget is set per event, not per level, and why a level with plenty of sigma can be run tighter, spending the budget where detection matters most.

---

## Scene 8 (3:30–3:49)

**On screen.** Column O `= C × (D/100) × K = 32.98 × 0.0141 × 3 = ±1.40 g/dL`; column R `= O / 3 = 0.465`. Target line with the action limits; LIS ±3 SD ticks at 0.465 land exactly on the action limit.

**Caption card.** *The LIS thinks in ±3 SD. Give it the SD that puts 3 SD where your rule is.*

**Narration.**
The result is an action limit in the units of the measurement. Most laboratory systems apply a fixed three-standard-deviation rule, so the last step is to give the system an SD such that three of them equal your action limit. From then on the system is enforcing your rule under its own name.

---

## Scene 9 (3:49–4:25)

**On screen.** Manuscript Figure 3 on the left. Right: MCHC level 1 analyser means (XR1 33.14, XR2 33.20, XR3 32.61) around the old LIS target 32.50 with ±1.40 limits; the target slides to the pooled mean 32.98 and the out-of-limit results disappear. Whole panel: 2.44 % → 0.68 % of events.

**Caption card.** *The rule is only half. The target must come from the same data.*

**Narration.**
One more thing, which we only saw when we applied the rules back to seven months of data. The limits sit around a target. If the target was set elsewhere, by the manufacturer, or by a single analyser, your own analysers sit off-centre, and a tight rule fires on the offset, not on a fault. In our data the false rejection rate more than tripled for that reason alone. Setting the shared target to the pooled mean of the analysers brought it back within budget. The rule from your imprecision; the target from your mean. Both, from the same data.

---

## Closing card (4:25–4:35)

*Kontrolregler v1.1 · iqc-rule-designer · Repository DOI: 10.5281/zenodo.22685381 · github.com/mfkilinckaya-svg/DesignLabIQC*
