# Maana Data downstream

This fork lets Maana Data ship model-family and workflow changes without waiting for the community Open Pstack release schedule. `origin` is this fork and `upstream` is `https://github.com/ericlitman/open-pstack.git`. Cursor pstack remains the content source described in `UPSTREAM.md`.

## Downstream changes

Version `1.4.2-maana.2` incorporates the optional Sonnet, GPT-6 Astra, GPT-5.6 Luna, and GPT-5.6 Terra families from open-pstack PR #55. It also adds optional GPT-6 Sol and GPT-6 Luna families for the Maana Data GPT-only route. Setup derives the active family set from the final role map, so a Codex-only Astra, Sol 6, and Luna 6 configuration does not probe or require Claude or Grok.

The native-default candidate uses a host-specific first-run map. Explicit role choices remain in each harness's pstack model sheet and project overrides.

## Installing the current branch

Use the immutable fork tag `v1.5.0-maana.3` with the [README installation instructions](README.md#install). Preserve existing model sheets and project overrides. Codex defaults to OpenAI; Claude Code defaults to Anthropic. Cross-provider use remains explicit.

## Updating directly from Cursor

Cursor's `cursor/plugins/pstack` tree is the content source. Community Open Pstack releases do not gate this fork's updates. Keep that remote available only for optional cross-harness fixes.

1. Run the direct-Cursor checker and pin the selected full source SHA. See `UPSTREAM.md`.
2. Branch from the current fork tip and keep source imports, harness changes, GPT routing, and release metadata separable.
3. Apply the audit in an isolated checkout, review every adapted hunk, and record each source path as imported, adapted, or intentionally retained/excluded.
4. Preserve provider-qualified GPT support, configured roles and panel order, native MCP roles, no fallback, and no implicit timeout. Do not copy Cursor's Opus/Grok defaults over the user's configuration.
5. Run the static, test, typecheck, manifest, plugin-validation, and installed-harness gates from `AGENTS.md`. Keep the PR draft until live evidence exists.
6. After review and exact-candidate live proof, tag the merged commit and refresh the shared machine installation. Open fresh Maana and DealTeam tasks and verify the installed candidate. Leave global instructions, model sheets, and project verification skills unchanged.

## Current candidate

`1.5.0-maana.3` imports Cursor pstack 0.15.15 at `df581122cde17e6e27686b5a448bde23e4ad4318`. It retains optional model families and defaults unconfigured roles to the current host provider. Scheduled Autopilot wake-ups are disabled in this core candidate. It is installed as a shared local candidate for DealTeam and Codeslaw, not a published release. See docs/plans/native-default-adoption.md. The operator-approved daily update-check schedule runs at 08:17 UTC and reports changes without auto-upgrading; manual detection is read-only unless its caller explicitly enables the notice input.
