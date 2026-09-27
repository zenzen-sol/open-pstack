# Maana Data downstream

This fork lets Maana Data ship model-family and workflow changes without waiting for the community Open Pstack release schedule. `origin` is this fork and `upstream` is `https://github.com/ericlitman/open-pstack.git`. Cursor pstack remains the content source described in `UPSTREAM.md`.

## Downstream changes

Version `1.4.2-maana.1` adds the optional Sonnet, GPT-6 Astra, GPT-5.6 Luna, and GPT-5.6 Terra families from open-pstack PR #55. Setup derives the active family set from the final role map, so a Codex-only Astra, Sol, and Luna configuration does not probe or require Claude or Grok.

The implementation preserves the upstream first-run panel. Maana-specific role choices belong in each harness's pstack model sheet, not in plugin defaults.

## Updating

1. Fetch `upstream/main` and inspect its release notes and `UPSTREAM.md`.
2. Rebase downstream commits onto the selected upstream tag.
3. Drop any downstream change already absorbed upstream.
4. Keep remaining model-matrix changes in standalone commits.
5. Run the static, test, typecheck, manifest, plugin-validation, and installed-harness gates from `AGENTS.md`.
6. Tag the exact installed and live-verified commit before updating either harness.

## Returning to upstream

When upstream supports the model families and selected-provider setup we use, repoint the Codex and Claude marketplaces to `ericlitman/open-pstack`, verify the installed release in both harnesses, and archive this fork only after its downstream diff is empty.
