# Maana Data downstream

This fork lets Maana Data ship model-family and workflow changes without waiting for the community Open Pstack release schedule. `origin` is this fork and `upstream` is `https://github.com/ericlitman/open-pstack.git`. Cursor pstack remains the content source described in `UPSTREAM.md`.

## Downstream changes

Version `1.4.2-maana.2` incorporates the optional Sonnet, GPT-6 Astra, GPT-5.6 Luna, and GPT-5.6 Terra families from open-pstack PR #55. It also adds optional GPT-6 Sol and GPT-6 Luna families for the Maana Data GPT-only route. Setup derives the active family set from the final role map, so a Codex-only Astra, Sol 6, and Luna 6 configuration does not probe or require Claude or Grok.

The implementation preserves the upstream first-run panel. Maana-specific role choices belong in each harness's pstack model sheet, not in plugin defaults.

## Installing the current branch

Use the branch-specific [README installation instructions](README.md#install). The downstream changes live on `codex/gpt-only-routing`, while `main` remains at community version `1.4.1`. PR #2 remains a draft; sharing the branch does not mean the parent-specific role-sheet confirmation or mixed-panel smoke gates have passed. Each recipient must run setup in their own harness and confirm their own model choices.

## Updating

1. Fetch `upstream/main` and inspect its release notes and `UPSTREAM.md`.
2. Rebase downstream commits onto the selected upstream tag.
3. Drop any downstream change already absorbed upstream.
4. Keep remaining model-matrix changes in standalone commits.
5. Run the static, test, typecheck, manifest, plugin-validation, and installed-harness gates from `AGENTS.md`.
6. Tag the exact installed and live-verified commit before updating either harness.

## Returning to upstream

When upstream supports the model families and selected-provider setup we use, repoint the Codex and Claude marketplaces to `ericlitman/open-pstack`, verify the installed release in both harnesses, and archive this fork only after its downstream diff is empty.
