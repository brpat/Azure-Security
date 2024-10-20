# Azure-Security
Collection of python tools to help audit Azure environments. Plus learning the Azure SDK

## Run with Docker (Recommended)
Install Docker Desktop using instructions from the official docs [here](https://docs.docker.com/get-started/get-docker/)

Run the below commands to run app inside container.

Clone Repo
```
git clone git@github.com:brpat/Azure-Security.git azure-security
cd azure-security
```

Build image and run a container. Note I used the tag **azure-security-img** for my docker image but it can be named anything.
```
docker buildx build -t azure-security-img .

docker run -e AZURE_SUBSCRIPTION_ID=$AZURE_SUBSCRIPTION_ID \
-e AZURE_TENANT=$AZURE_TENANT \
-e AZURE_CLIENT_SECRET=$AZURE_CLIENT_SECRET \
-e AZURE_CLIENT_ID=$AZURE_CLIENT_ID azure-security-img
```


## Run with Poetry
You can also run this project directly on a system. You should still manage Python dependencies properly. In order to download all dependencies and run the project without any issues, download and setup Poetry following the documentation here: https://python-poetry.org/docs/#installation

**Clone Project and Install Dependencies**
```bash
git clone git@github.com:brpat/Azure-Security.git azure-security
cd azure-security

poetry install
```

## Authentication
For local development purposes use DefaultAzureCredential authentication with .env with Service Princpals. If using within CI/CD pipeline or inside Docker container, ensure credentials are injected from build environment variables and not hardcoded.

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

Docker

Pass in auth info from environment variables,
``` 
docker run -e AZURE_SUBSCRIPTION_ID=$AZURE_SUBSCRIPTION_ID \
-e AZURE_TENANT=$AZURE_TENANT \
-e AZURE_CLIENT_SECRET=$AZURE_CLIENT_SECRET \
-e AZURE_CLIENT_ID=$AZURE_CLIENT_ID azure-security-img
```