## Credentials Guide

Use this guide on how to work with credentials with this project.

### Settings and Secrets

On the [Install Guide](INSTALL.md) we said we manage all Project
Configuration between *Project Settings* and *Project Secrets*. What
this means?

Suppose in this project, we will need to make a call for a 3rd party
API. To do this we need to define, *per environment*, these
configurations:

* The **Service URL**, for the 3rd party API
* The **Access Token**, for the 3rd party API.
* The **Timeout** in seconds, for the 3rd party API.

We will end with something like this:

| Configuration          | Develop                       | Staging                       | Production                |
|:-----------------------|:------------------------------|:------------------------------|:--------------------------|
| 3rd Party URL          | `https://service.com/api/dev` | `https://service.com/sandbox` | `https://api.service.com` |
| 3rd Party Access Token | `123-abc`                     | `foo-bar`                     | `456-789`                 |
| 3rd Party Timeout      | 30                            | 30                            | 5                         |


Every configuration which *is not a sensible info and we can safely
commit in the Project*, we will call it a **Project Settings**. The
**Timeout** and **Service URL** configurations are *Project Settings*.

Every configuration which *is a sensible info and we cannot commit in
the Project at all*, we will call it a **Project Secrets**. The **Access
Token** configuration is a *Project Secret*.

### How Project Settings Work?

First you need to add these settings on the `pyproject.toml` file. We
will do this to our **Timeout** and **Url** settings, adding the
`project.` prefix:

```toml
[environment]
project.3rd_party_timeout = 30

[environment.dev]
project.3rd_party_url = "https://service.com/api/dev/"

[environment.stg]
project.3rd_party_url = "https://service.com/sandbox/"

[environment.prd]
project.3rd_party_url = "https://api.service.com"
project.3rd_party_timeout = 5
```

The `[environment]` table will store the global settings - these
settings will be using in any Environment. That's why we do not need to
define a `dev` or `stg` setting for Timeout.

The `[environment.<ENV>]` tables will create or override a setting
previously defined in `[environment]`. We doing this to override the 30
seconds timeout for the Production setting and to define individually
the service urls.

Every setting must have a prefix, the default is `project.`. Example:
`project.service_timeout`, `project.service_url`, etc...

### How Project Secrets Work?

First we can add a **fake** value in `pyproject.toml`, like settings:

```toml
[environment]
project.3rd_party_access_token = ""
```

Then you will add the real value inside `.env` file. We will do this to
our **Access Token** setting, using his SCREAMING_UPPER_CASE version and
adding the `PROJECT_` prefix:

```dotenv
ENV="prd"
PROJECT_3_RD_PARTY_ACCESS_TOKEN="456-789"
```

Every secret must have a prefix, the default is `PROJECT_`. Example:
`PROJECT_SERVICE_TIMEOUT`, `PROJECT_SERVICE_URL`, etc...

### How this Project will read this data?

On Django Settings file, you will see something like this:

```python
from stela import settings

SERVICE_TIMEOUT = settings["project.3rd_party_timeout"]
SERVICE_TOKEN = settings["project.3rd_party_access_token"]
```

To read **Timeout**, [Stela](https://github.com/chrismaille/stela) will
do this:

1. First, it will try to find an environment variable using the setting
   SCREAMING_SNAKE_CASE name: for the `project.3rd_party_timeout`, Stela
   will look for `PROJECT_3_RD_PARTY_TIMEOUT` environment variable.
2. This variable did not exist in `.env` file, so Stela will return the
   value from `pyproject.toml` for the current environment (which we
   defined as `prd` in `.env` file). If this secret not exists in toml,
   Stela will raise a `KeyError`.
3. The SERVICE_TIMEOUT will be 5 seconds.

To read **Access Token**, [Stela](https://github.com/chrismaille/stela)
will do this:

1. First, it will try to find an environment variable using the setting
   SCREAMING_SNAKE_CASE name: for the `project.3rd_party_access_token`,
   Stela will look for `PROJECT_3_RD_PARTY_ACCESS_TOKEN` environment
   variable.
2. This variable did exists in `.env` file, so Stela will return the
   value from memory, ignoring the value in toml.
3. The SERVICE_TOKEN will be "456-789".

### Add Project Secrets in AWS

For the purpose of this challenge, all variables configured in Github Secrets
will be added as environment variables inside the Fargate container.
