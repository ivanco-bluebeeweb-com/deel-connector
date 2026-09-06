# Deel Connector — Auth & Credentials

## Credential Standard Compliance
- **Scheme:** `Authorization: Bearer <api_token>`
- **Storage:** Securely held in encrypted Imperal secrets store under `deel_connections`.
- **Sanitization:** All error strings and logging traces run through `_sanitize_msg()` to prevent token leakage.
- **Isolation:** Multi-tenant support keyed by UUID `connection_id` with active default selection.
