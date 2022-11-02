# MUI Data Grid

This is an unofficial toolbox to make integrating a Python web application with Material UI's data grid simpler.

## Documentation

- [Material-UI Data Grid](https://mui.com/x/react-data-grid/)

## Requirements

- Python 3.7+

## Installation

### Pip

```sh
python -m pip install -U 'mui-data-grid'
```

or with extras:

```sh
python -m pip install -U 'mui-data-grid[flask]'
python -m pip install -U 'mui-data-grid[sqlalchemy]'
python -m pip install -U 'mui-data-grid[flask, sqlalchemy]'
```

### Poetry

```sh
poetry add mui-data-grid
```

## Usage

### Integrations

#### Flask

```python
#!/usr/bin/env python
# examples/main.py

from flask import Flask, jsonify
from flask.wrappers import Response

from mui.v5.integrations.flask import get_grid_models_from_request

app = Flask(__name__)

FILTER_MODEL_KEY = "filter_model"
SORT_MODEL_KEY = "sort_model[]"
PAGINATION_MODEL_KEY = None  # stored inline in the query string, not encoded as an obj


@app.route("/")
def print_sorted_details() -> Response:
    # models will return default values if the keys don't exist,
    # so you can choose what features you integrate, and when.
    models = get_grid_models_from_request(
        filter_model_key=FILTER_MODEL_KEY,
        pagination_model_key=PAGINATION_MODEL_KEY,
        sort_model_key=SORT_MODEL_KEY,
    )
    return jsonify(
        {
            # sort_model is a list[GridSortItem]
            SORT_MODEL_KEY: [model.dict() for model in models.sort_model],
            # filter_model is GridFilterModel
            FILTER_MODEL_KEY: models.filter_model.dict(),
            # pagination_model is a GridPaginationModel
            # providing a consistent interface to pagination parameters
            PAGINATION_MODEL_KEY: models.pagination_model,
        }
    )


if __name__ == "__main__":
    app.run()
```

#### SQLAlchemy

Documentation coming soon!
