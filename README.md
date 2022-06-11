## Welcome to Bhub Customer API Challenge

[![Lint](https://github.com/chrismaille/bhub_challenge/workflows/pull_request/badge.svg)](https://github.com/chrismaille/bhub_challenge/actions)
[![Python](https://img.shields.io/badge/python-3.10-green)](https://www.python.org)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit)
[![Service Port](https://img.shields.io/badge/Port-8081-yellow)]()

### Domain Models

[![](https://mermaid.ink/img/pako:eNrVVlFv2jAQ_itWnml_AG9A0g1BoYJ00iSk6LCv4JHYme1Mywj_fXZICjFk0t5aS1Gc7_vOPt-d7RwDKhkGwwBVyGGnINsIYtvkdR0vn6MVOVUPD9Xx_TsZheEqWq_JkOxBe9rK104my9dFfE_7Ps6penysKnIZlsosTzFDYW5MmuEak_FoMfuXnhzP364VBWeEFtrIDFVi-y-zC6mNIgZ-W7iLvXGlTSIgwy6ewg2MosjIDgVDRTbB82geDchTdH4v46_RahNcxKAUlCRHpaWANMmVFLLI9EXAwCBRuON2NjBcisQhVzxSnkHq3ikoZAkXNgqel5gBT7sQxdROt5fC91wbMIW2no8m8fSb9Xk8X05mUTggYTSP4ii8dt-NtE0lPSQKwS6h67fhGZ5p6xcYcoel1s7U7B2yyFk_yTBFn3TutEbbsou3-mv8h3WZ5FCmEphdcbxHIhXfcZsKG_OfBWrjJoR2yaeewu2tLmBModZ-ld2U4JNPXhlec3WGWs6UOVqvx9P5fLr4UufHJmz13U9Qq7_sjg-XiK2UKQFq-C_siXSz3_sjTakshPn_SG9BHHyiLmuHbxUIur9DNNN9mkD2VWpPgbrh7YPoucLcMcSph1JuSt-2c0jVIhcv5en-8Dxxl86niWN90Rx7SujlXgl1l-fg7nXxwRfctmAQ2B1k7xFmfxDqAGwCs7enySYY2i4DdXDnzsnqztNGjBupguEbpBoHARRGrktBg6FRBbai5j-jUZ3-Ak9Bm0A)](https://mermaid.live/edit#pako:eNrVVlFv2jAQ_itWnml_AG9A0g1BoYJ00iSk6LCv4JHYme1Mywj_fXZICjFk0t5aS1Gc7_vOPt-d7RwDKhkGwwBVyGGnINsIYtvkdR0vn6MVOVUPD9Xx_TsZheEqWq_JkOxBe9rK104my9dFfE_7Ps6penysKnIZlsosTzFDYW5MmuEak_FoMfuXnhzP364VBWeEFtrIDFVi-y-zC6mNIgZ-W7iLvXGlTSIgwy6ewg2MosjIDgVDRTbB82geDchTdH4v46_RahNcxKAUlCRHpaWANMmVFLLI9EXAwCBRuON2NjBcisQhVzxSnkHq3ikoZAkXNgqel5gBT7sQxdROt5fC91wbMIW2no8m8fSb9Xk8X05mUTggYTSP4ii8dt-NtE0lPSQKwS6h67fhGZ5p6xcYcoel1s7U7B2yyFk_yTBFn3TutEbbsou3-mv8h3WZ5FCmEphdcbxHIhXfcZsKG_OfBWrjJoR2yaeewu2tLmBModZ-ld2U4JNPXhlec3WGWs6UOVqvx9P5fLr4UufHJmz13U9Qq7_sjg-XiK2UKQFq-C_siXSz3_sjTakshPn_SG9BHHyiLmuHbxUIur9DNNN9mkD2VWpPgbrh7YPoucLcMcSph1JuSt-2c0jVIhcv5en-8Dxxl86niWN90Rx7SujlXgl1l-fg7nXxwRfctmAQ2B1k7xFmfxDqAGwCs7enySYY2i4DdXDnzsnqztNGjBupguEbpBoHARRGrktBg6FRBbai5j-jUZ3-Ak9Bm0A)

### Project Guides

Use these guides to work on this project:

* Premises Guide: [PREMISES.md](docs/PREMISES.md)
* Installation Guide: [INSTALL.md](docs/INSTALL.md)

### TLDR
1. Clone project on WSL2 or Linux. Make sure you have docker installed.
2. Go to project directory and run `make config_project`
3. On VS Code, in command-palette select "**Remote-Containers: Rebuild and Reopen in
   Container**. Then, on Activity Bar, select the *Run & Debug View*. On dropdown select
   **Python:Django** and then click the _Play_ button.
4. On Pycharm Professional, Create a new
   [**Remote Interpreter** for Docker-Compose](https://www.jetbrains.com/help/pycharm/using-docker-as-a-remote-interpreter.html)
   , using Docker-Compose option. Then, on *Run/Debug* dropdown, select **Run Server** and click _Play_ button to start running.

### Project Links

The links below works when you're running the App via docker. For django based authentication, please use the
following credentials:

* user: admin
* password: admin

| Page         | Address                                                        | Use                         | Authenticated |
|:-------------|:---------------------------------------------------------------|:----------------------------|:--------------|
| Health-Check | [http://localhost:8081/health](http://localhost:8081/health)   | Health-Check                | No            |
| Swagger UI   | [http://localhost:8081/swagger](http://localhost:8081/swagger) | API Documentation (Swagger) | Yes (Django)  |
| Django Admin | [http://localhost:8081/admin](http://localhost:8081/admin)     | Django Admin                | Yes (Django)  |
