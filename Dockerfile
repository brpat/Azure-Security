FROM ubuntu:22.04

SHELL ["/bin/bash", "-c"]

RUN apt-get -y update && apt-get install -y python3.10 python3-pip

RUN update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.10 1

# Install Azure CLI, used for Default Azure Auth
RUN pip3 install azure-cli

COPY . /opt/app

WORKDIR /opt/app

# Load Environment vars,
RUN export $(xargs < .env)

RUN az --version

RUN pip3 install -r requirements.txt

CMD az login --service-principal -u "$AZURE_CLIENT_ID" -p "$AZURE_CLIENT_SECRET" -t "$AZURE_TENANT" && python3 main.py
# ENTRYPOINT ["python3", "main.py"]
# CMD ["python3", "modules/external_exposure.py"]