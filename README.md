[![Build status](https://github.com/richard457/fullfillment/actions/workflows/tests.yml/badge.svg)](https://github.com/richard457/fullfillment/actions/workflows/tests.yml)
# Order Fullfilment project

This project is a simple Flask application managed using Poetry for dependency management.

## Prerequisites

- Python 3.12.5 or higher
- Poetry (https://python-poetry.org/)

## Setup

1. Clone the repository:
   ```
   git clone https://github.com/richard457/fullfillment.git
   cd flask-project
   ```

2. Install dependencies:
   ```
   poetry install
   ```

## Running the Application

To run the Flask application:

```
poetry run python app.py
```

To run the Test
```
poetry run python -m unittest tests.py
```

The application will start and be available at `http://127.0.0.1:5000/`.

## Project Structure

- `app.py`: Main application file
- `pyproject.toml`: Poetry configuration file
- `poetry.lock`: Lock file for dependencies

## Adding Dependencies

To add new dependencies to the project:

```
poetry add package-name
```

## Running Tests

(Add this section once you've set up tests for your project)

## Contributing

- N/A
## License

MIT