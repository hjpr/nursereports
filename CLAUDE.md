# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

```bash
# Install dependencies
uv sync

# Run development server (http://localhost:3000)
reflex run

# Run tests
pytest nursereports/tests/

# Run a single test file
pytest nursereports/tests/states/test_state.py
```

Requires a `.env` file with: `api_url`, `api_key`, `jwt_secret`, `service_role` (Suplex/Supabase), `GROQ_KEY`, `MAILGUN_URL`, `MAILGUN_API_KEY`.

## Architecture

**Stack:** Reflex (Python full-stack reactive framework) + Supabase (Postgres + Auth) + Tailwind CSS v4. Package management via `uv`.

### State Hierarchy

Reflex uses a class-based state tree. The inheritance chain determines what vars/events are accessible:

```
Suplex (rx.State subclass)
  └── AuthState          # JWT access/refresh tokens in secure cookies
        └── UserState    # User claims (from JWT), user info, saved hospitals, report history
              └── BaseState    # Router utilities, login redirect, SSO token parsing
                    └── PageState        # Page-specific computed vars
                    └── ReportState      # Multi-step report form data
                    └── HospitalState    # Hospital analytics and pay data aggregation
                    └── SearchState      # Hospital search
                    └── NavbarState      # Feedback modal state
                    └── OnboardState     # User onboarding flow
```

Child states inherit all vars from parents. `user_claims` in `UserState` is the primary computed var that validates JWT and extracts user identity.

### Authentication Flow

1. Supabase email/password or SSO
2. SSO redirect parses tokens from URL fragment in `event_state_handle_sso_redirect()`
3. Tokens stored in secure, strict same-site cookies via `AuthState`
4. Protected pages use `on_load=[BaseState.event_state_requires_login, ...]`
5. Token refresh happens transparently on expiration

### Routing

Pages use `@rx.page(route="/path", on_load=[...])` decorator. All pages are imported in `nursereports/nursereports.py` — importing a page auto-registers its route. Dynamic routes use `{param}` syntax (e.g., `/hospital/{cms_id}`).

### Report Submission Flow

Multi-step form across 3 pages (compensation → staffing → assignment), all sharing `ReportState`. Hospital info is loaded from URL params. After submission, Groq LLM generates an AI summary stored alongside the report.

### Backend Layer

Database access uses the `suplex` library directly within state classes via `self.query().table(...).select(...).execute()`. There is no separate `server/supabase/` wrapper layer. Server utilities are in `nursereports/server/`: `exceptions/` (custom exception types), `mailgun/` (email sending), `middleware/` (Reflex middleware).

### Key Files

- `rxconfig.py` — Reflex + Suplex configuration
- `nursereports/nursereports.py` — App entry point, imports all pages
- `nursereports/states/` — All state classes
- `nursereports/client/pages/` — All page components (~26 routes)
- `nursereports/client/components/dicts.py` — Large UI data dictionaries (state/city mappings, etc.)
- `nursereports/server/exceptions/exceptions.py` — `RequestFailed` and other custom exceptions
