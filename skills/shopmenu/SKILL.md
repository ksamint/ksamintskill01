---
name: shopmenu
description: Query the ShopMenu restaurant menu API, list shops and brands, search dishes and prices, and identify shops in 沧州黄骅 from their addresses. Use for ShopMenu or shopdatafetch data and the menu_agent trial shop dataset.
---

# ShopMenu

Use `python3 scripts/query.py <endpoint>` from this skill directory for read-only API queries. It retrieves the API key from this Mac's login Keychain into process memory and prints JSON responses. Secrets belong in Keychain, never skill files, shell arguments, logs or generated artifacts.

Read [references/api.md](references/api.md) for endpoints, fields, location filtering and the local trial dataset. Fetch live lists when asked for current coverage; recorded counts and shops are snapshots.

Credential reference: Keychain service `com.codex.shopmenu.api-key`, account `shopmenu`, login Keychain `/Users/af/Library/Keychains/login.keychain-db`. Retrieval is trusted for `/usr/bin/security` and was verified without a prompt on 2026-10-14. If access fails, report the error; unlocking the Keychain stays under the user's control.

The key authorizes requests to `http://129.211.210.83` only. The helper rejects other hosts and redirects. This API currently uses HTTP, so transport is unencrypted; Keychain protects the stored credential at rest.
