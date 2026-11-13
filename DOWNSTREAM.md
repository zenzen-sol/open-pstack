# Maana Data downstream

This fork ships the newest Cursor pstack without waiting for the community Open Pstack release schedule. `origin` is this fork and `upstream` is `https://github.com/ericlitman/open-pstack.git`. Cursor's `cursor/plugins/pstack` tree is the content source described in `UPSTREAM.md`. Open Pstack is the source of the cross-harness port.

## Current base

Version `1.21.0-maana.1` is Open Pstack 1.21.0, which imports Cursor pstack 0.15.36 at `2776ddd2355d6d6c8747d3964600f28daf62f049`, plus the downstream changes below.

## Downstream changes

Each change is its own commit, so it can be dropped when Open Pstack absorbs it.

- **Direct Cursor check.** `scripts/check-cursor-update.py` audits the `UPSTREAM.md` pin against `cursor/plugins` main. `.github/workflows/cursor-update-check.yml` runs it daily at 08:17 UTC and opens or updates one issue when pstack changed. It reports only and never upgrades.
- **Host-native default roles.** Each parent harness seeds first runs and missing roles from its own map: Claude Code uses Anthropic models only, Codex uses OpenAI models only, and Grok uses Grok only. Setup never probes a foreign command-line tool for a role the user did not configure. The maps are in the Role defaults section of `plugins/pstack/skills/poteto-mode/references/model-catalog.md`, generated from `scripts/runner/registry/models.ts`. Fable is in no default map. Cross-provider panels stay available as explicit choices in a model sheet.
- **Arena judge.** The judge may come from the parent's provider, but it is never the parent's own model. A Grok parent has no judge by default, because its only pool entry is its own model.
- **No alias-only sheet.** Setup stops without writing when every role is `inherit-parent` or `auto`, because there would be nothing to probe or smoke-test.

These changes supersede three records in `UPSTREAM.md` that describe Open Pstack's own defaults: the exclusion that keeps `bug-fix`, `perf-issue` and `hillclimb` on Sol, the `df58112` exclusion that keeps three-model panels, and the `ab1f702` sentence that the judge is never from the parent's provider. Keep those records as they are, so the next Open Pstack merge stays clean.

## Installing

Both harnesses install from this fork's `main`. If a marketplace named `open-pstack` is already registered from another source, remove it first.

Claude Code:

```text
/plugin marketplace add zenzen-sol/open-pstack
/plugin install pstack@open-pstack
/reload-plugins
```

Codex:

```shell
codex plugin marketplace add zenzen-sol/open-pstack --ref main
codex plugin add pstack@open-pstack
```

Existing model sheets and project overrides keep working. Run `/setup-pstack` again only to adopt the new defaults for roles you never configured.

## Taking a new pstack release

Two paths keep this fork current. Use whichever arrives first.

1. **Cursor moves first.** The daily check opens an issue here. Follow "Incorporate a change" in `UPSTREAM.md` in this repository: branch from this fork's `main`, run `scripts/upstream-audit.py` and `scripts/upstream-merge.py` against the `cursor` remote, keep every port adaptation in the ledger, and keep the downstream changes above. Update the pin in `UPSTREAM.md`.
2. **Open Pstack releases first.** Merge `upstream/main` into a branch from this fork's `main`, resolve conflicts in favor of the downstream changes above, and drop any downstream commit that Open Pstack now covers.

## Merging and releasing

This fork does not run Mergify or Unfret. A pull request stays a draft until the exact candidate is installed and the changed behavior passes a live test in every affected harness, with the installed version, surface, action and observed result recorded in the pull request. The operator then merges it and tags the merged commit as `v<open-pstack version>-maana.<n>` by hand. `scripts/release.py` targets Open Pstack and is not used here.
