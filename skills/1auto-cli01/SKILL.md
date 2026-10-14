---
name: 1auto-cli01
description: Maintain automatic 1Password CLI access for local macOS Codex agents using vault-scoped Service Accounts and Keychain. Use for persistent CLI setup, expired authorization, missing automation credentials, or RequestDelegatedSession failures.
---

# 1auto-cli01

Reuse the approved 1Password credential channel and verify access in the agent's actual execution environment. A successful terminal session does not establish access for a separately running desktop app or another shell.

## Verify before using credentials

1. Run the existing [op-cli-preflight](../op-cli-preflight/SKILL.md) check:

   ```sh
   python3 "$HOME/.codex/skills/op-cli-preflight/scripts/check.py" --check
   ```

2. Confirm the active identity with `op whoami --format=json` or `op user get --me --format=json`. For automation, expect the intended active `SERVICE_ACCOUNT`, then use `op vault list --format=json` to confirm its accessible vaults. Inspect whether credential variables are set without printing their values or dumping the environment.
3. Use an explicit `--vault` with item commands. Service Accounts do not have access to built-in Personal/Private/Employee or default Shared vaults. Treat permission-denied and missing-item errors as scope issues before attempting sign-in.

If an explicitly authorized task requires a personal-only credential, use a separate subprocess with `OP_SERVICE_ACCOUNT_TOKEN` removed and the normal desktop sign-in flow. Preserve the caller's automation environment; the local shell loader would reintroduce the token if a new Codex shell were started instead. Local Touch ID remains under the user's control.

Completion: the intended identity can access the task's vault from a fresh agent shell. Report the precise scope; a successful `whoami` alone does not prove the required item is accessible.

## This Mac's established configuration

Verified on 2026-10-11; inspect the live configuration before repairing it:

| Setting | Recorded value |
| --- | --- |
| Service Account | `codex-local-readonly` |
| Granted permission | `read_items` in `Codex Automation` only |
| Keychain service / account | `com.codex.1password.service-account` / `codex` |
| Encrypted backup | Personal vault, item `Codex Local Read-only Service Account Token` |
| Shell loader | `~/.zshenv`, guarded by a nonempty `CODEX_THREAD_ID` |
| Environment | Loads `OP_SERVICE_ACCOUNT_TOKEN` only when a caller has not supplied one |
| Network | Sets missing `HTTPS_PROXY` to the existing local HTTP proxy `http://127.0.0.1:6152` |

The loader reads the token from login Keychain using `/usr/bin/security find-generic-password`; its output goes into the environment, never chat. Ordinary shells remain unaffected. These are local settings, not portable defaults. A locked login Keychain, stopped proxy, expired/revoked token, or inaccessible vault still needs resolution. Inspect the actual proxy with `scutil --proxy`.

## Diagnose desktop delegation failures

`RequestDelegatedSession: cannot setup session` is not proof that CLI integration is disabled. The desktop app may unlock cached local data while failing to contact 1Password servers to issue a delegated session.

- Identify whether the failing process is using a Service Account or desktop authentication. For an invalid Service Account token, diagnose token state, scope, and network access; desktop `op signin` will not repair that token.
- For desktop authentication, check Developer → Integrate with 1Password CLI. Inspect recent relevant entries in the app logs under `~/Library/Group Containers/2BUA8C4S2C.com.1password/Library/Application Support/1Password/Data/logs/`. Extract only delegation, HTTP, and proxy errors; redact identifiers and credential material.
- If logs show `HttpError`, failed proxy tests, or offline state, compare direct HTTPS connectivity with the configured proxy. Keep certificate validation enabled. On this Mac, direct TLS failed while the existing HTTP/SOCKS proxy worked; restarting 1Password restored delegation.
- After correcting the evidenced fault, reconnect or restart once when appropriate, let the user complete local unlock/Touch ID, and verify the intended identity and vault. If the same error persists, collect the new diagnostic evidence and report the blocker instead of looping sign-in attempts.

The existing preflight helper combines failed sign-in and timeout in one message and currently allows only 20 seconds for `op signin`. Check its actual code before interpreting that message. When necessary, use one bounded sign-in attempt with enough time for local confirmation, capture the real error, and keep stdout private.

Desktop CLI authorization expires after 10 minutes of inactivity and has a 12-hour hard ceiling. App auto-lock changes do not turn it into a 12-hour idle session. Service Account authentication uses its token rather than desktop biometric authorization; verify token validity instead of promising permanent availability.

## Provision or repair only within the authorized task

Reuse a suitable approved account first. Verify its vault scope and permissions through supported account metadata or administration UI; a working token does not establish that it is read-only. Create a separate account only when the requested scope requires it. Apply the host's approval rules at the consequential action; invoking this skill is not authorization to broaden access.

For authorized setup:

1. Establish the required vault and permissions. Prefer `read_items` for credential consumption. Check `op service-account create --help`; use explicit vault permissions and the requested expiry. Do not silently replace other accounts or grant write/create/share permissions.
2. Capture `op service-account create ... --raw` stdout in process memory. The token is returned once: prepare encrypted storage before creation, then retain the live token until at least one encrypted copy is verified. Store it in login Keychain and back it up to an appropriate 1Password vault. For `security -i`, send the command through captured stdin; for `op item create -`, send a JSON template through stdin. Capture tool output and verify the saved token privately. Keep tokens out of argv, plaintext files, shell history, skill files, and tool transcripts.
3. Back up the actual shell file before editing it. Load credentials only in the intended agent environment, preserve caller-supplied tokens/proxies, and use the machine's verified network route. Existing approved access to the intended vault is the prerequisite for setup, not a reason to copy unrelated secrets into it.
4. Verify shell syntax and behavior: a fresh agent shell loads the intended identity; an ordinary shell remains unaffected; an existing caller-supplied token remains unchanged. Verify access to the required vault without exposing secret values. Record nonsecret account, Keychain, backup, and loader references for future repair.

The login Keychain protects the stored token at rest; processes able to retrieve it can use its granted vault access. Provisioning credentials does not authorize deployment, publication, or other actions outside the user's task.

## Official references

- [Service Account setup and immutable permissions](https://developer.1password.com/docs/service-accounts/get-started/)
- [Service Accounts with CLI](https://developer.1password.com/docs/service-accounts/use-with-1password-cli/)
- [Desktop integration](https://developer.1password.com/docs/cli/app-integration/)
- [Desktop authorization limits](https://developer.1password.com/docs/cli/app-integration-security/)
