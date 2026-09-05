# Security — Enterprise AI Modernization Architect

## Status honesty

| Area | Status |
|------|--------|
| Secrets via environment / gitignore | **IMPLEMENTED** (Stage 1) |
| Input validation pattern (Pydantic) | **IMPLEMENTED** (health schemas) |
| Authentication / RBAC | **PLANNED** (Stage 12) |
| Policy-as-code / approval audit | **PLANNED** (Stage 12) |
| CI secret scanning | **PLANNED** (Stage 18) |
| Azure Key Vault / private networking | **FUTURE** / Stage 19 sketch |

---

## Assumptions (honest)

| Assumption | Implication |
|------------|-------------|
| Local Docker/Postgres credentials (`aima`/`aima`) are demo-only | Never reuse in real environments |
| Stage 1 API has no auth | Do not expose to untrusted networks |
| Synthetic data only (when Stage 3 lands) | No real customer PII in this repo |
| Secrets via environment | Never commit `.env` |

---

## Current controls (Stage 1)

1. `.gitignore` excludes `.env`, keys, secrets directories.
2. `.env.example` documents variables without real secrets.
3. `AIMA_LLM_API_KEY` loaded from env — empty by default; provider defaults to `stub`.
4. Pydantic validation on health response models (pattern for future inputs).
5. SQLAlchemy parameterized `SELECT 1` (no string-built SQL).

---

## Planned controls

- JWT/session auth
- Roles: `viewer`, `analyst`, `architect`
- Policy gates for high-impact recommendations
- Approval audit trail
- Production secrets in Azure Key Vault (Stage 19 docs)

## Threat notes

| Threat | Now | Later |
|--------|-----|-------|
| Secret leakage in git | gitignore | CI secret scan |
| Unauthenticated API | local-only assumption | Stage 12 auth |
| Dependency CVEs | pinned majors | Stage 18 security checks |
| Prompt injection / data exfil via LLM | N/A (no LLM calls yet) | tool allowlists, redaction, policy |

Related: [stages/STAGE_12.md](stages/STAGE_12.md), [ARCHITECTURE_DECISIONS.md](ARCHITECTURE_DECISIONS.md)
