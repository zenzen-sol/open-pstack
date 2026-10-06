# Upstream synchronization

open-pstack tracks [Cursor's pstack](https://github.com/cursor/plugins/tree/main/pstack) while adapting Cursor-specific primitives for Claude Code and Codex.

## Current sync point

| Source | Value |
| --- | --- |
| Repository | `https://github.com/cursor/plugins.git` |
| Path | `pstack/` |
| Commit | `df581122cde17e6e27686b5a448bde23e4ad4318` |
| Upstream version | `0.15.15` |
| open-pstack version | `1.5.0-maana.3` |

The table above is the current Cursor sync point. This candidate imports Cursor 0.15.15 directly. Its release and shared-machine rollout remain gated by the exact-candidate live checks in `AGENTS.md`. `README-UPSTREAM.md` preserves the upstream pstack README verbatim. `CHANGES.md` and `NOTICE.md` describe the adaptations and provenance.

## Upstream-only exclusions

- Commits `799151d` and `6fecddb` add and relocate `make-bot-ui`. It depends on Cursor routines, webhook events, and UI primitives that Claude Code and Codex do not share.
- Four `disable-model-invocation: true` lines from `73f8be4` are not applied to `how`, `why`, `unslop`, or `typescript-best-practices`. Poteto-mode invokes those skills by name, and the flag blocks that route on Claude Code.
- The `23a56e2` default-model hunks for `bug-fix`, `perf-issue`, and `hillclimb` are not applied. Those frequent code-writing roles stay on `codex:gpt-5.6-sol@max` for cost.
- The Claude manifest does not take the logo field from `efa2a53` because Claude Code has no schema for it. The shared asset is exposed through the Codex manifest instead.

- Cursor 0.15.15 removes Sol from its defaults and permits model fallback in several skills. This port keeps GPT families, the configured panel, parent-owned dispatch, MCP-native roles, and named dropouts. Budget choices change only supported requested efforts.
- Cursor guide pages stay external reference material because their Custom Mode, cloud, routine, and installation surfaces are not implemented here. The adapted help skill links the pinned guide as context and routes to packaged fork skills.

## Check for changes

Use Cursor directly as the content source. Add its remote when absent:

```shell
git remote add cursor https://github.com/cursor/plugins.git
```

Fetch and inspect only commits that touched pstack after the recorded sync point:

```shell
git fetch cursor main
git log --oneline df581122cde17e6e27686b5a448bde23e4ad4318..cursor/main -- pstack
git diff --stat df581122cde17e6e27686b5a448bde23e4ad4318..cursor/main -- pstack
```

No output means the tracked pstack tree has not changed. `scripts/check-cursor-update.py` produces the full pinned audit without fetching or writing the checkout. The manual `.github/workflows/cursor-update-check.yml` fetches Cursor and uploads that audit. Its optional notice job deduplicates a bot-authored fork issue. The daily 08:17 UTC schedule is prepared as a comment and remains disabled until explicitly approved. Unrelated Cursor repository commits do not trigger a notice.

## Incorporate a change

1. Create or update a GitHub issue in `zenzen-sol/open-pstack` and branch from the current fork tip containing the GPT adaptations. Community Open Pstack is an optional source of harness fixes, not the release or content dependency.
2. Read each upstream pstack commit in order. Bring over its intent and content, then retain the Claude Code and Codex substitutions plus the GPT-routing policy documented in `CHANGES.md`. Pin a full source SHA before applying the audit with `scripts/upstream-merge.py` in an isolated checkout.
3. Keep one shared `plugins/pstack/skills/` tree. Put harness translation in the existing `codex-tools.md` and provider routing in `provider-dispatch.md`; do not fork a skill per harness.
4. Update the commit and version in this file, the affected provenance rows in `NOTICE.md`, and `README-UPSTREAM.md` when upstream changes it.
5. Run CI-equivalent checks locally, then run the installed Claude Code and Codex behavioral lanes required by the changed surface. Unit tests alone are not a release gate.
6. Keep the PR draft until the exact candidate passes the installed Codex and Claude surface gates. Merge only the reviewed candidate, tag that exact commit, then refresh the shared installation from the verified tag. Never update user model sheets or project-local verification skills as part of a content sync.

Cursor's version and open-pstack's version are independent. Cursor's version identifies the imported content; open-pstack's version identifies the cross-harness distribution.

The [0.15.15 path ledger](docs/plans/cursor-0.15.15-paths.tsv) accounts for all 65 changed source paths and records intentional retained adaptations. The [candidate verification record](docs/plans/cursor-0.15.15-verification.md) distinguishes completed checks from remaining live gates.
