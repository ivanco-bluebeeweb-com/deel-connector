# Deel Connector — Preparation

## Product Scope
Build a comprehensive Imperal connector for **Deel** (C28. Payroll & Benefits Administration). The integration connects directly to the official **Deel REST API v2** (`https://api.letsdeel.com/rest/v2`), providing global workforce management across employees, contractors, contracts, payroll runs, departments, time-off requests, benefit plans, and direct deposits.

## Official API Specifications
- **API Version:** Deel REST API v2
- **Base URL:** `https://api.letsdeel.com/rest/v2`
- **Core Endpoints:**
  - `GET /rest/v2/people` — list employees and contractors with status filters and cursor pagination
  - `GET /rest/v2/people/{id}` — detailed employee / contractor profile
  - `GET /rest/v2/payroll/runs` — global payroll runs and payment status
  - `GET /rest/v2/departments` — departments and cost centers
  - `GET /rest/v2/time-off/requests` — leave and vacation requests
  - `GET /rest/v2/benefits` — global benefits and healthcare coverage
  - `GET /rest/v2/direct-deposits` — banking and payment routing
- **Authentication Model:** Bearer Token via `Authorization: Bearer <api_token>`
- **Mandatory Requirements:**
  - Strict error classification: HTTP 429 rate limits with Retry-After, HTTP 401/403 differentiation (Standard B8/B10).
  - Sanitization of Bearer tokens in error traces (Standard B8).
  - Multi-tenant connection tracking via `connection_id` (Standard B9).

## Delivery Gates
1. [x] Official API discovery completed with Deel REST API v2 specifications.
2. [x] Core endpoints and Bearer auth verified.
3. [x] Five mandatory specification documents authored.
4. [x] Client implemented with B8-B10 compliance, secret redaction, and 429/401 classification.
5. [x] Panel sidebar implemented conforming to UI_INTERFACE_STANDARD.md.
6. [x] Verification of functions, imports, and type hints passed.
7. [x] Deployment to Imperal platform completed.
8. [x] Tool pricing configured across all 35 tools before review submission.
