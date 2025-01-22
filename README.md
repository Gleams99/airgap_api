# airgap_api

## Environment Setup

Note: The instructions below are primarily aimed at MacOS and if being executed on other OS's then may need modifying.

### Poetry Setup (Preferred)

The project can be setup using [Poetry](https://python-poetry.org/docs/#installation).
If Poetry is installed follow the commands below else refer to the [pip setup](#pip-section) section.

```shell
# Create poetry virtual environment and install project dependencies
poetry install
```

### Pip Setup

The project can be setup without Poetry. Follow the steps below

```shell
# Create a python virtual environment
python3 -m venv .venv
# Activate the viirttual environment
source .venv/bin/activate
# Install project dependencies
.venv/bin/pip3 install -r requirements.txt
```

## Credential Setup

Valid Airgap API email, password and token are required for test execution.

Visit the [registration](https://airportgap.com/tokens/new) page to register and obtain a valid API token.

Execute the following commands to create an .env file ready for populating your values into.

```shell
touch .env
echo "AIRGAP_EMAIL=" >> .env
echo "AIRGAP_PASSWORD=" >> .env
echo "AIRGAP_TOKEN=" >> .env
```

Don't forget to edit the file to include your specific credentials.

## Test Execution

The tests within this repo can be executed using the below commands:

```shell
# Execute all API tests
poetry run pytest -m api

# Execute all airport endpoint API tests ini parallel
poetry run pytest -n auto -m airports

# Execute all token endpoint API tests
poetry run pytest -m tokens

# Execute all favorites endpoint API tests
poetry run pytest -m favorites
```

**Note:** If the pip setup was followed then instead of `poetry run pytest` in the command above, use `.venv/bin/pytest`.

E.g.
```shell
.venv/bin/pytest -m api
```

## Under the hood

### API Response Validation

- Pydantic models are being used to ensure the data contained within the API response body conforms to an expected structure.

### Enumerations of Airport Codes

- Enumerations have been defined that contain valid airport IATA codes. 

### Test Assertions

2 approaches are provided within test assertions.

- Fail Fast: In the situation where there is no point in continuing test execution because an API call failed then standard `assert` calls are made which will cause the test to fail fast.

- Show All Failures: The pytest-check package is used to allow for multiple checks to be performed during test execution but will result in a test failure result and detailed difference output upon test exiting if the checks fail.

### Base API Client

A base API client class has been developed that allows:

- Logging hook functions to be added
- Automatically retry an API call if a rate limit error is detected
- Supports argument forwarding allowing for maximum configuration
- Implements a generator for returning multiple page data

### Performance Tests

The logging being performed within the Base API Client includes the log output of the elapsed time of the API request.
This attribute of the Response object can be used to determine if an API call exceeds the allowed duration.

Additionally, specific API based performance tests can be implemented separately.

## Test Reports

A `report.html` is automatically generated upon test execution.

The report has been updated to include the doc strings of each test, which dettails the intention of the test and the steps being performed by the test.


## Gotchas

- Due to the same account being used within the `favorites` tests then executing tthem in parallel mode may result in test failures.
