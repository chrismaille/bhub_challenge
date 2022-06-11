## Installation Guide

Please use this guide on how to install this project.

### Project Requirements

* [Python3.10](https://www.python.org)
* [Docker](https://www.docker.com)
* [Poetry](https://python-poetry.org/)

### Pre-Requisites

#### Pre-Requisites on Windows
1. Install Windows Subsystem for Linux 2 - **WSL2**:
[https://docs.microsoft.com/pt-br/windows/wsl/install-win10](https://docs.microsoft.com/pt-br/windows/wsl/install-win10)

2. Install **Docker Desktop for Windows** using this link:
[https://docs.docker.com/docker-for-windows/install/](https://docs.docker.com/docker-for-windows/install/). DO NOT INSTALL docker inside WSL, the Windows client will do that.

********

#### Pre-Requisites on Linux
These commands are meant for Ubuntu 20.04 running on host computer:

1. Install **Docker**:

```shell
# New installation
# DO NOT INSTALL docker inside WSL, the Windows client will do that.
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER # then restart bash
```

Do not upgrade an existing docker version, instead remove current docker
installation using this doc:
[https://docs.docker.com/engine/install/ubuntu/](https://docs.docker.com/engine/install/ubuntu/)
and then make a clean install. Make sure you have the latest version
installed.

********

### Clone and Configure

We recommend using SSH for Github operations as per [VERSIONING.md](VERSIONING.md) documentation.

Please clone this project using the following command:

```shell
# On Windows, please clone the repo inside Ubuntu Home folder or subfolder
$ wsl  # windows cmd or powershell
$ cd ~/path/to
$ git clone git@github.com:chrismaille/bhub_challenge.git
```

Please copy (do not rename) `env.example` to `.env` file:

```shell
cd ~/path/to/bhub_challenge
cp .env.example .env
```

### Build

On Local Terminal, run:

```bash
$ wsl # windows cmd or powershell
$ cd ~/path/to/bhub_challenge
$ docker compose build
```

********

### Remote development in VSCode:

1. Please install the following VS Code extensions:

* Remote Development
* Python
* Docker

2. On command-palette select "**Remote-Containers: Rebuild and Reopen in
   Container**"

3. On VSCode Activity Bar, select the *Run & Debug View*. On dropdown select
**Python:FastApi** and then click the _Play_ button.

#### References:
* [https://code.visualstudio.com/docs/remote/containers](https://code.visualstudio.com/docs/remote/containers)

*********

### Remote development in Pycharm Professional:

You need the
[PyCharm Professional Edition](https://www.jetbrains.com/pt-br/pycharm/)
to run these commands. They will not run on Community edition.

1. Please install the following PyCharm plugins:

* [Docker](https://plugins.jetbrains.com/plugin/7724-docker)
* [EnvFile](https://plugins.jetbrains.com/plugin/index?xmlId=net.ashald.envfile)

2. Create a new
   [**Remote Interpreter** for Docker-Compose](https://www.jetbrains.com/help/pycharm/using-docker-as-a-remote-interpreter.html), using Docker-Compose option.

3. On *Run/Debug* dropdown, select **Run Server (Uvicorn)** and click _Play_ button to start running.
