# Azure-Security
Collection of python tools to help audit Azure environments. 



## Installation

In order to download all dependencies and run the project without any issues, download and setup Poetry following the documentation here: https://python-poetry.org/docs/#installation

**Install Dependencies**
```bash
git clone git@github.com:brpat/file-sentry.git

poetry install
```

## Usage

*Interactive
```python
cd Azure-Security
poetry shell 
python app/main.py
```

Non-Interactive (Service)
```python
cd Azure-Security
poetry run python3 main.py
```