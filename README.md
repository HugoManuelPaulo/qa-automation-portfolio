# QA Automation Portfolio

[![Automated QA Tests](https://github.com/HugoManuelPaulo/qa-automation-portfolio/actions/workflows/tests.yml/badge.svg)](https://github.com/HugoManuelPaulo/qa-automation-portfolio/actions/workflows/tests.yml)

A compact, deterministic QA automation project demonstrating browser testing, API validation, maintainable test design and CI reporting.

## What this project demonstrates

- UI automation with **Selenium WebDriver** and the **Page Object Model**
- API functional and contract checks with **Requests** and **PyTest**
- Positive, negative and validation scenarios
- Test categorization with `api` and `ui` markers
- Automated execution in **GitHub Actions**
- A downloadable self-contained HTML test report
- A **Postman** collection with response assertions

The application and API under test run locally during the test session. This keeps the suite reliable and avoids failures caused by unavailable third-party demo services.

## Test coverage

| Layer | Scenarios |
| --- | --- |
| UI | Successful login, invalid credentials, required-field validation |
| API | List users, retrieve user, missing resource, valid creation, payload validation |

## Project structure

```text
app/                 Local browser test fixture
pages/               Selenium page objects
tests/api/           API behavior and contract tests
tests/ui/            Browser-based user-journey tests
postman/             Importable Postman collection
.github/workflows/   Continuous integration pipeline
```

## Run locally

Requirements: Python 3.11+ and Google Chrome.

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
pytest -v --html=report.html --self-contained-html
```

Run only one layer:

```bash
pytest -m api -v
pytest -m ui -v
```

## Quality approach

The suite separates browser actions from assertions, uses explicit waits instead of fixed sleeps, validates status codes and response contracts, and produces evidence on every CI run. The tests are intentionally self-contained so failures point to product behavior rather than an unstable external dependency.

