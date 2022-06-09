## Welcome to Bhub Customer API Challenge

[![Lint](https://github.com/chrismaille/bhub_challenge/workflows/Lint/badge.svg)](https://github.com/chrismaille/bhub_challenge/actions)
[![Python](https://img.shields.io/badge/python-3.10-green)](https://www.python.org)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit)
[![Service Port](https://img.shields.io/badge/Port-8081-yellow)]()

### Project Guides

Use these guides to work on this project:
* DOs and DON'Ts: [REASONING.md](docs/REASONING.md)
* Installation Guide: [INSTALL.md](docs/INSTALL.md)
* Developing Guide: [DEVELOP.md](docs/DEVELOP.md)
* Versioning Guide: [VERSIONING.md](docs/VERSIONING.md)
* Profiling Guide: [PROFILING.md](docs/PROFILING.md)
* Deployment Guide: [DEPLOY.md](docs/DEPLOY.md)
* Credentials Guide: [SECRETS.md](SECRETS.md)

### Project Links

The links below works when you're running the App via docker. For Django
based authentication, please define your local superuser using the
[createsuperuser](https://docs.djangoproject.com/en/2.2/intro/tutorial02/)
command.

| Page         | Address                                                      | Use                         | Authenticated |
|:-------------|:-------------------------------------------------------------|:----------------------------|:--------------|
| Health-Check | [http://localhost:8081/health](http://localhost:8081/health) | Health-Check                | No            |
| Swagger UI   | [http://localhost:8081/docs](http://localhost:8081/docs)     | API Documentation (Swagger) | Yes (Django)  |
| Django Admin | [http://localhost:8081/admin](http://localhost:8081/admin)   | Django Admin                | Yes (Django)  |
