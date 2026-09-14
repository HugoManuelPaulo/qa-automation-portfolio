# QualityCart — E-commerce QA Automation

[![Automated QA Tests](https://github.com/HugoManuelPaulo/qa-automation-portfolio/actions/workflows/tests.yml/badge.svg)](https://github.com/HugoManuelPaulo/qa-automation-portfolio/actions/workflows/tests.yml)

A portfolio-grade QA automation framework for a deterministic e-commerce application. It demonstrates browser journeys, API contracts, maintainable test architecture and CI evidence without depending on unstable third-party demo sites.

## Business risks covered

| Area | Automated scenarios |
| --- | --- |
| Authentication | Successful login, invalid credentials, required-field validation |
| Product discovery | Catalog rendering, keyword/category search, empty results |
| Cart | Add product, item count, quantity changes, price recalculation |
| Checkout | Customer journey and order confirmation |
| Product API | List, filter, retrieve and missing-resource behavior |
| Order API | Creation, server-side totals and invalid payload rejection |
| User API | Read/create contracts and negative validation |

## Engineering approach

- **Python, Selenium WebDriver and PyTest**
- **Page Object Model** separating browser actions from assertions
- API functional, negative and contract checks with **Requests**
- Data-driven validation using pytest.mark.parametrize
- Stable data-testid selectors and explicit waits
- Automatic screenshots when UI tests fail
- Self-contained HTML report on every CI run
- GitHub Actions execution on pushes and pull requests
- Importable Postman collection with response assertions

## Structure

    app/                  Deterministic e-commerce application and API fixture
    pages/                Page Object Model classes
    tests/ui/             End-to-end browser journeys
    tests/api/            API contract and behavior tests
    postman/              Postman API collection
    .github/workflows/    Continuous integration pipeline

## Run locally

Requirements: Python 3.11+ and Google Chrome.

    python -m venv .venv
    source .venv/bin/activate  # Windows: .venv\\Scripts\\activate
    pip install -r requirements.txt
    pytest -v --html=report.html --self-contained-html

Run a test layer independently:

    pytest -m api -v
    pytest -m ui -v

## CI evidence

Every push runs the complete API and browser suite in headless Chrome. GitHub Actions retains the HTML report and any failure screenshots as downloadable artifacts, making results auditable by reviewers.

## Test credentials

    Email: demo@example.com
    Password: Quality123

This project was designed and implemented as a practical demonstration of QA automation, risk-based coverage and maintainable test engineering.
