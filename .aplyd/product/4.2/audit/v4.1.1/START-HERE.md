# Generic product management agent bundle 4.1

Start here. This is a packaging and instruction update: checker 4.0, catalogue 3.0 and the Word guide are unchanged.

## Prepare once

Extract the ZIP. Identify the actual product, canonical workspace, authorised scope and current stage. Complete `PRODUCT-CONTEXT.md` and the context intake using actual sources. Resolve AI and personal-information applicability; load `AI-ASSURANCE.md` only when needed. Use the team's actual versioned Ready and Done checklists.

Map sourced records into the supported checker document. For input/schema or command details, open only the relevant section of `checker/README.md`. Run commands from `checker/` with Python 3.9 or later. Paths below refer to your working document, report and state directory.

## One working order

**check → summary → next → fix → check again**

1. **Check.** Use `loop` for this step: it runs the checks and creates or refreshes the durable queues that `next` reads.

   ```sh
   python3 -B quality_checker.py loop --document draft.json --report report.json --state-dir review-state --batch-size 3
   ```

2. **Summary.** Read the compact result before opening detailed evidence.

   ```sh
   python3 -B quality_checker.py summary --report report.json --state-dir review-state
   ```

3. **Next.** Select the next supported repair, reviewer task or owner question.

   ```sh
   python3 -B quality_checker.py next --state-dir review-state --queue all --limit 3
   ```

4. **Fix.** Inspect the exact criterion with `explain` when needed and load only its relevant sources and evidence. Repair supported draft gaps through `apply-revision`; obtain genuine review for reviewer work. Ask targeted questions only for missing facts or authority decisions. Record answers, preserve current unanswered batches and keep independent work moving. Never invent facts, evidence, owners or favourable verdicts; preserve approved, frozen and protected content.

5. **Check again.** Repeat the step-1 command, then return to summary and next. Continue until the selected stage's mandatory checks are satisfied, or retain the precise blocker and resume condition. A pause, time limit, empty queue or iteration count does not create success.

Exit 2 means unresolved work: continue to summary and next. Exit 3 means an input or command error: inspect the error and repair it first. Real-mode review uses the actual separately supplied trust store via `--trust-store` on the check step. Synthetic mechanics tests require `--allow-synthetic` and have a separate result.

## Load information only when needed

Do not load `audit/` by default. It contains historical verification paperwork, logs and reports, not project facts or current work instructions. Open it only for an explicit audit, integrity investigation or verification request; start with `audit/README.md`.

Do not recursively read the bundle, full catalogue, full reports, Word guide, synthetic examples, tests, verification harnesses or generated publication files. Use summary, next and explain first; load relevant guide sections or exact evidence on demand. `checker/ASSISTANT-WORKFLOW.txt` retains the full operating safeguards when detailed workflow guidance is needed.

All offline results are advisory. Documentation quality, owner approval, readiness, delivery and measured learning remain separate and need actual evidence. This bundle does not authorise coding, external messages, new services, publication or launch. Save and read back authorised canonical changes and report only evidenced completion.
