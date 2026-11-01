# Week 6 final evaluation review

## Executive summary

I reviewed the 487 records in [`evals_run_487_synthetic_judged.json`](./evals_run_487_synthetic_judged.json), checked the existing Week 6 audit materials, independently recomputed their observable counts, and closely reviewed a stratified sample of 20 cases (five from each question-style category).

This is an AI-assisted evidence review, **not human labeling**. In addition to the local review, the course's delegated browser calibration was performed by ChatGPT Work, an AI agent, not a human evaluator. The aggregate judge scores and browser-review labels are not independently validated human ground truth. The JSON contains questions, short reference answers, final answers, file names, tool names/arguments, and judge explanations; it does not contain the retrieved document bodies or the complete intermediate agent conversation. As a result, I can confirm some reference-answer omissions and observable trace properties, but cannot certify all 487 answers against their original documentation.

The clearest findings are:

1. **The original run's instruction prompt remains unproven.** The original 487-case judge used a prompt configuration that was not recorded in its output. The checked-in runner defaults to `SIMPLE_INSTRUCTIONS`; the initial checked-in instruction-judge formatter used `DEFAULT_INSTRUCTIONS`, but that binding has since been corrected to `SIMPLE_INSTRUCTIONS` for calibration. Do not treat either source snapshot alone as proof of the prompt used for the original generation.
2. **The answer-correctness judge has at least one strong apparent false positive:** case 7 is scored Good even though the answer does not state the reference's core behavior (empty drift columns prevent drift calculation and raise an error). Cases 4, 6, 12, and 85 have clear omissions consistent with their Bad correctness scores.
3. **The four exact repeated `get_file` calls are real trace properties**, not inferred from judge reasoning. Whether each repetition was wasteful cannot always be established without the missing intermediate conversation and retrieved contents. Case 180 is a notable missed-repeat candidate: its trajectory judge says Good despite the same telemetry file being fetched twice.
4. **The browser calibration is useful but limited.** ChatGPT Work reviewed 20 cases; 18 were classified and two were uncertain. Reported agreement is 72.2%, precision 72.7%, and recall 80%, with disagreements on cases 7, 11, 15, 16, and 18. Scores were visible to the reviewer, and reviewer-level labels were not saved in the app.
5. **No aggregate corrected accuracy rate is warranted.** Many judge scores cannot be re-adjudicated from the available snippets alone, and retrieval of the gold-reference file is not a prerequisite for a correct answer if another retrieved source supports it.

## Scope and method

- Parsed all 487 JSON records and checked the three judge labels, reference-file names, answer text, and recorded tool calls. The summary counts and exact-string flags below were recomputed from the JSON rather than copied from the audit CSV.
- Enumerated all 487 question/reference/answer records and checked their structure, saved labels, and observable text/tool signals. The detailed semantic answer-versus-reference review is the stratified 20-case sample below, not a manual adjudication of every answer.
- Performed an AI-assisted close review of 20 cases chosen to cover all four `question_type` values evenly, a mix of judge-label combinations, answer/reference alignments, and tool-path patterns. This purposive sample is **not a statistically representative sample** and is not human labeling.
- Read the existing [`week6_487_audit_report.md`](./week6_487_audit_report.md), [`week6_20_case_evidence_review.md`](./week6_20_case_evidence_review.md), and [`week6_487_case_triage.csv`](./week6_487_case_triage.csv). The existing CSV's observed-flag counts match the underlying JSON. Its case-1 “human” label is not treated here as independently verified ground truth.
- Recorded the browser-based ChatGPT Work review as the delegated calibration exercise for this course. Its summary metrics and disagreement list are reported as supplied; the reviewer labels were not saved in the app, and judge scores were visible during review.
- Did not call paid APIs, rerun evaluations, modify the agent, or commit/push.

The checked-in runner's default config is `SIMPLE_INSTRUCTIONS` in [`doc_agent.py`](../doc_agent.py), used by [`run_evals_synthetic.py`](./run_evals_synthetic.py). The instruction formatter in [`llm_judge_checks.py`](./llm_judge_checks.py) now also uses `SIMPLE_INSTRUCTIONS`; its original 487-case prompt is not captured in the results file, so the exact historical agent and judge prompts remain unverified.

## Recomputed all-case observations

### Judge labels

| Dimension | Good | Bad | Good rate |
|---|---:|---:|---:|
| Answer correctness | 275 | 212 | 56.5% |
| Instruction following | 399 | 88 | 81.9% |
| Tool trajectory | 401 | 86 | 82.3% |

These are **the saved judges' labels**, not revised or human-verified scores. Of the 487 records, 195 are Good on all three dimensions, 6 are Bad on all three, and 286 have mixed labels.

### Corrected Instruction Following calibration

The separate [`evals_run_487_instruction_only_20_v2.json`](./evals_run_487_instruction_only_20_v2.json) contains Instruction Following results for 20 saved agent responses using the corrected `SIMPLE_INSTRUCTIONS` judge binding. This is a limited calibration, not a rerun of the 487-case evaluation and not human labeling.

| Result set | Good | Bad | Execution errors |
|---|---:|---:|---:|
| Previously reported baseline for this 20-case comparison | 15 | 5 | Not established by the available baseline artifact |
| Corrected instruction-only calibration | 20 | 0 | 0 |

The reported comparison says the scores changed from Bad to Good for cases **6, 7, 10, 15, and 20**. This baseline and changed-case list are recorded as reported, but could not be reproduced from the available earlier artifacts: [`evals_run_487_instruction_only_20.json`](./evals_run_487_instruction_only_20.json) contains 20 execution errors (`'RunUsage' object is not callable`) and no scores; matching the 20 questions in the v2 file to the original [`evals_run_487_synthetic_judged.json`](./evals_run_487_synthetic_judged.json) yields 18 Good and 2 Bad, with a different changed set (v2 rows 7 and 12). The 15/5 baseline and five-case delta therefore remain unverified against the saved source results.

A follow-up evidence review of the specified v2 cases found:

- **Cases 6, 7, 10, and 15: uncertain.** The saved answers and tool calls are visible, but retrieved document contents and intermediate agent messages are absent. Therefore the Good scores cannot be fully confirmed against the “documentation only” requirement or the adequacy of the underlying retrieval.
- **Case 20: supported for the core answer only.** Its answer states that Pre-built Tabs rely on related Metrics/Reports and that panels remain empty until the relevant Reports are added, matching the central reference. Additional details and complete instruction compliance remain unverified.

The corrected file contains **20 evaluated successfully and 0 execution errors**. These are corrected **judge outputs**, not human-verified ground truth. They do not establish that all 20 responses fully followed the instructions, nor do they revise the other 467 original instruction scores.

### Browser-based delegated calibration review

For the course's delegated calibration exercise, **ChatGPT Work (an AI agent, not a human evaluator)** reviewed 20 cases in the browser. The reported outcomes were:

| Measure | Reported result |
|---|---:|
| Cases reviewed | 20 |
| Classified | 18 |
| Uncertain | 2 |
| Agreement | 72.2% |
| Precision | 72.7% |
| Recall | 80% |
| Disagreements | 7, 11, 15, 16, 18 |

Agreement, precision, and recall are included as reported for the calibration; they have not been independently recomputed because the browser reviewer’s case-level labels were **not saved in the app**. Judge scores were visible to the reviewer during the review, so this was not a blind comparison and could be affected by anchoring. The two uncertain cases should not be treated as agreements or disagreements without the missing labels and metric denominators. This browser review is the delegated review used for the course, but it does not convert the results into human-labeled ground truth.

### Instruction evidence and configuration caveat

- The exact word `pip` appears in **31** answers; all 31 include `pip install`.
- In the original judged file, 15 of those 31 answers are scored Good for Instruction Following. The original judge prompt is not stored with the results, so the prompt-level reason for this pattern cannot be proven from that artifact alone.
- The checked-in runner defaults to `SIMPLE_INSTRUCTIONS`, which has no package-manager rule. The original generated responses' prompt/configuration is not recorded, however, so this source-level default does not prove which instructions were active in that run.
- Case 23 makes the possible conflict plain: its reference answer itself recommends `pip install`. Whether the original judge applied a prohibition against `pip` remains dependent on unavailable run provenance.
- Agent `checks` are self-reports, not independent evidence. For example, some self-checks say documentation was followed despite a visible `pip` mention.

### Tool paths

- All **487/487** traces begin with `search` and include at least one `get_file`.
- The records contain **522 search calls** and **1,080 `get_file` calls**. There are 32 records with more than one search (29 with two searches and three with three); none has more than three searches.
- The exact gold-reference file appears in a `get_file` call in **230** cases; it does not in **257**. A missing gold-file fetch alone is not evidence of a bad trajectory or unsupported answer.
- There are **four cases with an exactly repeated `(tool name, arguments)` call**: 42, 180, 251, and 417. These are observable repetitions; the trace alone does not establish whether the later call was useless.
- The log omits intermediate agent messages and returned document contents. Therefore it cannot establish whether the agent explained each tool call, whether a search result justified a retrieval, or whether a supposedly extra file was actually relevant.

## Confirmed and uncertain judge issues

“Confirmed” below means that the supplied answer/reference text or tool log itself demonstrates the point. It does not certify the corresponding underlying documentation claim.

### Strong evidence of a correctness-judge miss

- **Case 7 — likely false Good:** the reference says empty columns in reference/current data prevent distribution-drift calculation and raise an error. The answer instead discusses missing column definitions and empty datasets; it never states that behavior. This is a substantial reference mismatch, despite the saved correctness score of Good.
- **Cases 4, 6, 12, and 85 — Bad correctness is supported by the visible reference comparison:** respectively, the answer omits sorting `Length` to find the longest failed output; omits the required `item_features` list and its numerical/embedding meaning; omits the relevant/irrelevant/partially-relevant labels and question placeholder; and omits the allowed-value validation behavior and `None` result. These are not merely wording differences.

### Plausible but not confirmed score errors

- **Case 18:** the answer includes connecting to Cloud and creating a project, the reference's core steps, but correctness is scored Bad. The extra setup and current Cloud details cannot be checked against the source text here, so this is a likely disagreement with the judge rather than a proven false negative.
- **Case 10:** the answer gives export formats and the reference mentions rendering in an interactive notebook plus other export options. Whether the answer's specific formats and API calls are accurate requires the source document; the Bad score is unresolved.
- **Cases 3, 33, 42, 180, 251, and 417:** the saved trajectory decisions are not fully verifiable from call names alone. Cases 42, 180, 251, and 417 do contain exact repeated calls; case 180's Good score is a potential false negative, but repeated calls are not automatically wasteful.
- **Cases 28 and 85:** the answers include broad claims beyond the short references. Whether those claims are supported by the retrieved documentation cannot be determined from the JSON.

## Diverse 20-case review

Assessment notation: **C/I/T** = answer correctness / instruction following / trajectory. “Supported” means the judge's label is supported by the available record; “mismatch” means the record strongly points the other way; “uncertain” means the evidence is insufficient. Instruction assessments are qualified by the runner/judge prompt discrepancy above. The sample has five cases from each question style.

| Case | Question style | Judge C/I/T | Independent evidence review |
|---:|---|---|---|
| 68 | context_assumer | G/G/G | **C supported:** the answer describes using a context manager and `create_trace_event`, matching the reference. **I conditional mismatch:** it adds `pip install tracely`; that violates the judge's `DEFAULT_INSTRUCTIONS`, but not a restriction visible in the runner's default `SIMPLE_INSTRUCTIONS`. **T supported:** search then retrieve the matching tracing document. |
| 37 | context_assumer | G/G/G | **C supported:** the answer explains `DataDefinition`, column types, and roles as asked. The added auto-mapping claim is not verifiable from the reference excerpt. **I/T supported on available evidence:** a matching data-definition file and a related summary preset were fetched. |
| 10 | context_assumer | B/B/G | **C uncertain:** the answer directly addresses exporting, but HTML/JSON/dictionary/workspace details need checking against the source; the reference excerpt does not establish them. **I uncertain:** no active instruction violation is proven from the record. **T supported:** search followed by two output/exploration documents. |
| 28 | context_assumer | B/G/B | **C/I uncertain:** the answer lists general security, portability, and deployment benefits not present in the short reference; source support is unavailable. **T questionable:** three searches and four file fetches are visible, but they are within the configured maximum and their relevance cannot be fully assessed. |
| 35 | context_assumer | G/B/G | **C supported for the core:** it passes current and reference datasets to `report.run`, matching the reference. **I conditional mismatch:** its code uses spaces around `=`, contrary to `DEFAULT_INSTRUCTIONS`' formatting rule; that rule is absent from the runner's default prompt. **T supported:** both retrieved files concern data drift. |
| 85 | direct_inquirer | B/B/G | **C supported:** it does not mention allowed output values or that invalid output yields `None`; instead it gives generic LLM evaluation approaches. **I uncertain:** the answer also contains `pip`, but the active prompt provenance is unresolved. **T supported:** three LLM-evaluation documents were fetched after a relevant search. |
| 2 | direct_inquirer | G/G/G | **C supported for the core:** it creates a `Report` with `DataDriftPreset` and runs it against two datasets. Whether the keyword arguments and extra `include_tests` suggestion are valid requires the source. **T supported:** report and drift-preset documents were retrieved. |
| 4 | direct_inquirer | B/G/G | **C supported:** the answer gives general test-debugging advice but omits the reference's concrete instruction to sort `Length` and inspect the longest response. **I uncertain:** whether the applicable prompt required a Python example depends on retrieved source content that is not present. **T uncertain:** three retrieved files are related broadly to testing/debugging, but the gold example file was not retrieved. |
| 33 | direct_inquirer | G/B/B | **C supported:** the answer accurately states syntax validation and per-input Boolean output. **I uncertain:** the question asks what the function does, and no response-level breach is demonstrated. **T plausible mismatch:** after the initial targeted search, it makes two additional searches (one broad, one similar) before retrieving the exact descriptor file. |
| 6 | direct_inquirer | B/B/G | **C supported:** the answer misses the named `item_features` requirement and introduces ranking/additional-data claims not in the reference. **I uncertain:** source text is needed to assess other instruction rules. **T supported:** the recommendation preset and metric-customization files are at least topically related. |
| 18 | frustrated_beginner | B/G/B | **C likely mismatch:** the response does say connect to Cloud and create a project, matching the reference's core; its extra account/setup details may still contain errors. **I conditional mismatch:** it mentions `pip`, subject to the prompt discrepancy. **T uncertain:** the two fetched Cloud documents look relevant, but their contents are unavailable. |
| 5 | frustrated_beginner | G/G/G | **C supported for the requested metrics:** it names `mean_error` and `error std`. Additional baseline interpretations are not independently source-checked. **T supported:** the metric file was retrieved directly. |
| 12 | frustrated_beginner | B/G/G | **C supported:** it substitutes generic descriptors for the requested relevance classification and omits the three labels and question placeholder. **I questionable:** the final answer does not address the specific requested method. **T uncertain:** the retrieved descriptor and text-evaluation files are related, but the reference's specific source was not fetched. |
| 3 | frustrated_beginner | G/G/B | **C supported:** the answer gives `id_column="Id"` and `timestamp="Date"` as in the reference. **T plausible mismatch:** it additionally retrieves a custom-metric file after the directly relevant data-definition file; whether that was necessary is not proven. |
| 7 | frustrated_beginner | G/B/G | **C mismatch (strong):** it does not state that empty drift columns stop calculation and raise an error, despite that being the reference's core. **I uncertain:** no separate, observable violation is established. **T uncertain:** retrieved files are adjacent to data definitions/testing, but not the cited drift explainer. |
| 1 | hurried_developer | G/G/G | **C supported:** the requested notebook link is present. **I conditional mismatch:** it adds a `pip install` command and places it in a Python-fenced block; the package restriction is not in the runner's default instructions. **T supported:** the example and related LLM-judge files were retrieved. |
| 14 | hurried_developer | G/G/G | **C supported for the core:** it explains passing multiple regression mappings as a list. The code API details are not source-verified. **I uncertain:** code-style rules depend on which prompt actually generated the record. **T supported:** data-definition and regression-preset files were fetched. |
| 27 | hurried_developer | B/G/G | **C plausible:** it describes presets but does not clearly show the reference's alternative of composing a custom `Report` metric-by-metric; it also adds Cloud/project steps. Source verification is needed before calling those additions erroneous. **T supported:** preset and evaluation API files are pertinent. |
| 42 | hurried_developer | G/G/B | **C supported:** `DO_NOT_TRACK`, the disable confirmation, and unsetting the variable match the reference. **T judge label supported as a concern:** the telemetry file is fetched twice, with a second search between fetches. The duplicate is real; its usefulness is not fully observable. |
| 23 | hurried_developer | G/B/G | **C supported against the supplied reference:** both requested packages are included, and the answer follows the reference's package-install approach. **I disputed:** it uses `pip`, but the reference itself uses `pip`; the judge's prohibition conflicts with that gold answer and may not have been active for the agent. **T supported:** installation and Cloud setup documents were retrieved. |

## Remaining uncertainty

- The original versions/content of the 487 referenced documentation files are not included in the judged JSON or the three audit files. I did not treat a current online page or a short gold excerpt as proof of what the agent actually retrieved.
- The evaluation data does not record which instruction string/version was used for the original generation or original judge run. The current checked-in runner and corrected formatter both use `SIMPLE_INSTRUCTIONS`, but this does not retroactively establish the original run's configuration.
- A short reference answer cannot establish that extra information is wrong, nor that an answer is complete. This particularly limits adjudication of long answers and API snippets.
- Tool calls are logged without intermediate messages or returned file contents, limiting judgments about rationale, relevance, and true retrieval redundancy.
- The 20-case review is a targeted diagnostic sample, not a human-reviewed sample, not a random sample, and not a basis for estimating corrected overall accuracy.
- The browser calibration was also AI review, not human review. Since its individual labels were not retained and the judge scores were visible during review, the reported metrics and disagreement cases cannot be independently audited from the saved app data.

## Bottom line

The evaluation ran 487 synthetic cases through three judges: Answer Correctness, Instruction Following, and Tool Trajectory. Report those totals as judge outputs, not verified accuracy. The corrected 20-response Instruction Following calibration scored 20 Good, 0 Bad, and 0 execution errors; the earlier 15 Good/5 Bad comparison is reported but not reproducible from the available saved baseline, so that discrepancy remains explicit. The course's delegated browser calibration was performed by ChatGPT Work, an AI agent: 18 cases were classified, two were uncertain, and the reported agreement/precision/recall were 72.2%/72.7%/80%, with disagreements on cases 7, 11, 15, 16, and 18. Because labels were not saved and judge scores were visible during review, these figures cannot be independently reconstructed and are not human-verified ground truth. Missing document contents and unconfirmed original prompt provenance further limit conclusions.

### Lessons learned

- Persist the exact agent and judge instruction text (or immutable version/hash) with each run; the current runner default does not establish historical run configuration.
- Save case-level reviewer labels, uncertainty states, and a confusion matrix alongside aggregate agreement/precision/recall so the calibration can be audited and recomputed.
- Hide judge scores during independent review when possible to reduce anchoring; identify AI reviewers as AI and do not present their labels as human ground truth.
- Preserve retrieved document content or a versioned documentation snapshot and intermediate trace messages when source-grounded answer and trajectory verification is required.
- Separate execution errors from Good/Bad judge outcomes and score only successfully evaluated cases.

## Answer Correctness Judge V2 — Final Calibration

The original Answer Correctness Judge and V2 were compared on the same 20 saved agent responses corresponding to entries 1–20 of the original judged file. All case identities were verified. The V2 runner's output was completion-ordered, so results were aligned by question, reference answer, and saved agent response rather than by row position.

ChatGPT Work served as the delegated AI-assisted reviewer for this calibration. It classified 18 cases as Good or Bad; uncertain cases 9 and 10 were excluded from the metrics. These labels are not independently human-verified ground truth.

| Metric | Original | V2 |
|---|---:|---:|
| Agreement | 72.2% (13/18) | 88.9% (16/18) |
| Bad Precision | 71.4% (5/7) | 100% (6/6) |
| Bad Recall | 62.5% (5/8) | 75.0% (6/8) |

Changed scores:

- **Case 7:** Good → Bad.
- **Case 10:** Bad → Good; uncertain and excluded from metrics.
- **Case 15:** Bad → Good.
- **Case 18:** Bad → Good.

On this calibration sample, V2 improves agreement by 16.7 percentage points. This is diagnostic alignment evidence only: the same sample was used to develop V2, so the improvement is not independent evidence of generalization. No independently human-verified labels were used; ChatGPT Work was an AI-assisted delegated reviewer.

Keep the original correctness prompt as the default. V2 must remain explicitly selectable; this calibration does not justify silently changing default judge behavior. The original 487-case evaluation results remain unchanged.
