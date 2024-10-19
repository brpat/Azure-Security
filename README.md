# Azure-Security
Collection of python tools to help audit Azure environments. Plus learning the Azure SDK



## Installation

In order to download all dependencies and run the project without any issues, download and setup Poetry following the documentation here: https://python-poetry.org/docs/#installation

**Clone Project and Install Dependencies**
```bash
git clone git@github.com:brpat/Azure-Security.git

poetry install
```

## Authentication
For local development purposes use DefaultAzureCredential authentication with .env with Service Princpals. If using within CI/CD pipeline, ensure credentials are injected from build environment variables and not hardcoded.

```bash
cd Azure-Security
touch .env
```

```bash
AZURE_CLIENT_ID=EXAMPLECLIENTID
AZURE_CLIENT_SECRET=EXAMPLEAPPSECRET
AZURE_TENANT_ID=EXAMPLETENANTID
```
Reference: https://learn.microsoft.com/en-us/azure/developer/python/sdk/authentication/overview

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