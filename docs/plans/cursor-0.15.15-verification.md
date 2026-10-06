# Cursor 0.15.15 candidate verification

This review candidate branches from `a5d5239162bba47ff5a322e798c4f2303e9699eb` on `codex/gpt-only-routing`. It imports Cursor `df581122cde17e6e27686b5a448bde23e4ad4318`, version 0.15.15. The candidate distribution version is `1.5.0-maana.1`. [Fork issue #3](https://github.com/zenzen-sol/open-pstack/issues/3) tracks the work. No upstream contribution is included.

The plugin Git tree is `308fdae33b7fe7dd7b9f5cf64e4b4977df9560d6`. The SHA-256 of its sorted relative-path/file-hash index is `e80b46dff6e3a5e4902e3d83b7fcc552b5de4b45f0ad50be6eb159871bd7cdff`. Checkout dependencies are excluded from that index. The source audit and TSV ledger account for all 65 source paths. Cursor's 11 guide changes stay external reference material; the native manifests are adapted separately. Portable first-run panel defaults remain the existing four families, while configured GPT routes and optional families remain intact.

## Completed checks

- `bun install --frozen-lockfile` completed without a lockfile change. With Bun 1.3.5 and CI's Node 22.23.2, all 160 Bun tests passed. Strict watch-pr, runner, and plan-checker typechecks passed.
- Ten Python tests passed. Real temporary Git repositories prove add/modify/delete accounting, no checkout mutation, unchanged pstack trees under unrelated Cursor commits, duplicate-pin refusal, merge safety, and notice deduplication. The notice CLI remains read-only without `--write` and sends one structured request with it.
- All ten merge-helper probes passed on the actual pinned 65-path range. They checked imported bytes, stale HEAD refusal, dirty mapped paths, exclusions, executable modes, no-op rows, unmapped metadata, and failed binary merges. Ranges without both adapted and verbatim changes report an explicit fixture-test requirement rather than crashing.
- The existing static routing and shipping checks passed. All four distribution manifests parsed; strict Claude plugin and marketplace manifest validation passed. New skill relative links resolved. The README mirror matched the pinned source. The catalog contains 58 skills and 24 principles. `git diff --check` passed.
- The detector reported 65 changed paths against the old fork pin and zero after the candidate pin advanced. The workflow YAML parsed with only `workflow_dispatch`; the daily schedule remains commented out. No workflow, notice automation, tag, release, or rollout was run.

The first local full-suite run used Node 22.15.0 and reproduced the two existing TypeScript-entry runtime-guard failures. The one stale 30-minute checker expectation was updated to hourly. The final run with Node 22.23.2 passed all tests; runtime-guard implementation was not changed.

## Isolated runtime observations

These are CLI smokes, not the installed desktop-app release gates. The committed [smoke record](cursor-0.15.15-isolated-smokes.json) contains candidate identity, load mode, tools/commands, and observed responses.

Claude Code 2.1.259 loaded the candidate inline from `--plugin-dir` and reported pstack version `1.5.0-maana.1`. User/project settings and ambient MCPs were restricted for the fixture sessions. Explicit `/pstack:poteto-help` read the candidate setup and recipe files and explained preserving `inherit-parent` and `codex:gpt-6-sol@high` while proposing lower supported effort. It did not run setup or write files. A model-side Skill invocation of this typed-only help was refused as expected. The final benchmark smoke invoked `pstack:benchmark-checklist` through the Skill tool and rejected a claimed 10x speedup based on an errored single run, with no limiter or successful-work proof.

An earlier benchmark probe used Claude Plan mode, which attempted a plan-file Write outside the fixture. The restricted tool surface rejected it, and no file was written. The final probe used default permission mode with only Read and Skill, avoiding that scaffold. This was a harness-mode observation, not a plugin source change.

Standalone Codex CLI 0.145.0 rejected the configured parent model. The app-bundled 0.160.0 accepted the same requested model and completed a read-only fixture-local help run without model substitution. It read the candidate help and recipes and explained role preservation and budget selection. The fixture initially linked only help, so an optional setup-reference lookup failed; the fixture layout was corrected afterward. This is limited source-backed help evidence, not setup or native model-dispatch proof. Codex did not expose a served-model report. No shared Codex plugin installation was changed.

## Remaining release gates

The subsequently authorized installed checks are recorded in [the installed verification record](cursor-0.15.15-installed-verification.md). Most controlled setup and local Autopilot checks passed. Normal Claude-to-Codex executable compatibility and scheduled-wake approval remain blocked; both shared plugins were restored to `1.4.2-maana.2`. The items below describe the original gate list, not a claim that no installed testing occurred.

- Install the exact candidate in controlled Codex and Claude user surfaces, then exercise the changed behavior from those surfaces. Inline Claude and fixture-local Codex reads do not satisfy the full installed-app gate.
- Live-prove budget selection and existing GPT-only setup with parent-specific probes in temporary configuration, including unsupported models and failed probes leaving both the sheet and integration unchanged. Do not use the real user's files as a migration fixture.
- Exercise fresh-agent follow-ups, code-ready/fix-round review, hourly change-only ticks, required live/performance lanes, and the retained disarm/lease/expected-head rules. Unit and static checks do not establish those workflows end to end.
- GitHub CI passed on candidate commit `bd1c3513e9994fd0ea8806cadf95e65375df0849`: [verification run](https://github.com/zenzen-sol/open-pstack/actions/runs/37403140148). The manual update workflow has not run on GitHub, and cannot be treated as verified merely because local detection/tests pass.
- Review and merge only after required live evidence exists. Tag the exact merged candidate and read back the release before refreshing either shared installation. Daily scheduling remains a separate approval and code change.

## Shared-machine rollout after approval

Use a verified release tag as the marketplace ref. Refresh only `open-pstack`, then reinstall its candidate plugin through the harness's normal marketplace operations. The current Codex CLI supports `codex plugin marketplace upgrade open-pstack --json` followed by `codex plugin add pstack@open-pstack --json`. Claude currently uses the local checkout as its marketplace source; select the verified candidate there, update its plugin, and reload plugins. Open fresh Maana and DealTeam tasks and read back the installed version and exact payload.

Leave `~/.codex/pstack-models.md`, all of `~/.codex/AGENTS.md`, parent-specific model integrations, and project-local verification skills unchanged. Do not copy model sheets between harnesses or run setup on them as an incidental content update. The shared installed caches remained `1.4.2-maana.2` during this implementation.
