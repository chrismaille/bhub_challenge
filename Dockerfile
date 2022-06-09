FROM python:3.10-slim-bullseye as build

RUN apt-get update && apt-get -y upgrade && \
    apt-get install locales git python3-psutil libssl-dev gcc g++ make -y wait-for-it \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

RUN pip install poetry>=1.1.12
# Uncomment if you want to use Celery
# RUN pip install setuptools==59.6.0   # Flower needs this version

# Add locales
RUN DEBIAN_FRONTEND=noninteractive apt-get install -y locales
RUN sed -i -e 's/# pt_BR.UTF-8 UTF-8/pt_BR.UTF-8 UTF-8/' /etc/locale.gen && \
    dpkg-reconfigure --frontend=noninteractive locales && \
    update-locale LANG=pt_BR.UTF-8
ENV LANG pt_BR.UTF-8

# Installing requirements
RUN poetry config virtualenvs.create false

# Install Application
WORKDIR /app/src
COPY . /app/src/
RUN poetry install

EXPOSE 8080

ENTRYPOINT ["sh", "/app/src/entrypoint.sh"]

FROM build as dev_container

# VSCode users:
# Before rebuild your devcontainer
# make sure poetry.lock is up-to-date
# (use command make update)

# For VSCode Docker Extension to work
# Please check https://aka.ms/vscode-remote/containers/non-root
USER root
ARG USERNAME=vscode
ARG USER_UID=1000
ARG USER_GID=$USER_UID
RUN groupadd --gid $USER_GID $USERNAME | true \
    && useradd --uid $USER_UID --gid $USER_GID -m $USERNAME | true \
    && apt-get update \
    && apt-get install -y sudo \
    && echo $USERNAME ALL=\(root\) NOPASSWD:ALL > /etc/sudoers.d/$USERNAME \
    && chmod 0440 /etc/sudoers.d/$USERNAME

# Let image ready for development
RUN apt-get -y upgrade
RUN apt-get install -y tar git curl build-essential libssl-dev zlib1g-dev libbz2-dev zip \
    libreadline-dev libsqlite3-dev wget curl llvm libncurses5-dev libncursesw5-dev \
    xz-utils tk-dev libffi-dev liblzma-dev python3-openssl libpq-dev libcurl4-openssl-dev

# Add AWS client v1
RUN curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
RUN unzip -o awscliv2.zip
RUN ./aws/install --update

# Add libs
RUN pip install -U localstack awscli-local

WORKDIR /app/src
USER $USERNAME
