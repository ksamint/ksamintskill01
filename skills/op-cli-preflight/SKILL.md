---
name: op-cli-preflight
description: Check local 1Password CLI access before credential-dependent Codex work. Route persistent Service Account setup and delegated-session failures to 1auto-cli01; use desktop sign-in for personal-account authentication.
---

# 1Password CLI preflight

Run `python3 scripts/check.py --check` for a quick status check. For persistent automatic access, an unavailable Service Account token, or `RequestDelegatedSession` errors, read [1auto-cli01](../1auto-cli01/SKILL.md) before retrying sign-in. For desktop personal-account authentication, run `python3 scripts/check.py --signin` once when needed. Status `0` confirms CLI access; nonzero means access is unavailable. Inspect the helper's actual error handling before interpreting an unavailable result as a timeout or an account error.

The desktop app controls personal-account authentication. The script does not cache session tokens, copy secrets, change security settings, or bypass local approval. If access still needs local confirmation, continue independent work and report the exact blocker. For unattended deployments, use an existing approved, vault-scoped service account; creating or broadening one is a separate access change.
