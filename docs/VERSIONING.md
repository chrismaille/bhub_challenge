## Versioning Guide

### Commit Naming Conventions
This project uses [Semantic Versioning](https://semver.org/lang/pt-BR/). This means every time code are merged on `main`
branch, a new version is created, along with the respective updates in _Github Release_ page and _CHANGELOG.md_ file.

This is possible because [python-semantic-release](https://python-semantic-release.readthedocs.io/en/latest/#getting-started) will read all new commits and check for
`feat:`, `fix:` and `BREAKING CHANGE` text in commit messages to determine new version number.

So, best practice is to use the following convention on commit messages:

```text
<prefix>: <summary>

<optional>
<detailed description>
</optional>

<optional>BREAKING CHANGE: <description></optional>

Resolves <Jira-ID>
```
Simple Example:
```shell
# New Jira feature, code BHUB-123
feat: new feature added.

Resolves BHUB-123
```
Full Example:

```shell
# New Jira feature, code BHUB-123
feat: new feature added.

This feature add new functionality for customer experience with these changes:
* Add new API endpoint
* Add new fields on Customer model
* Update Documentation

BREAKING CHANGE: API authentication is now required.

Resolves BHUB-123
```

#### Determining new version number:

Consider the following commits for current version `1.0.0`:

Example 1:
```text
feat: new feature added.\nResolves BHUB-123
ci: code review.\nResolves BHUB-123
docs: update documentation.\nResolves BHUB-124
```
New version is `1.1.0` because the `feat:` commit message.

Example 2:
```text
fix: bug on old feature.\n\nResolves BHUB-125
docs: update documentation.\n\nResolves BHUB-126
ci: fix terraform.\n\nResolves BHUB-127
```
New version is `1.0.1` because the `fix:` commit message.

Example 3:
```text
feat: new feature added.\n\nResolves BHUB-123
fix: bug on old feature.\n\nResolves BHUB-125
docs: update documentation.\n\nResolves BHUB-126
ci: fix terraform.\n\nResolves BHUB-127
```
New version is `1.1.0` because the `feat:` precedes `fix:` message.

Example 4:
```text
feat: new feature added.\n\nResolves BHUB-123
fix: bug on old feature.\n\nResolves BHUB-125
docs: update documentation.\n\nResolves BHUB-126
ci: new feature added.\n\nBREAKING CHANGE: refactoring docker\n\nResolves BHUB-128
```
New version is `2.0.0` because the `BREAKING CHANGE` precedes both `feat:` and `fix:` messages.

Example 5:
```text
docs: update documentation.\n\nResolves BHUB-126
ci: fix terraform\n\nResolves BHUB-128
chore: fix black formatting.\n\nResolves BHUB-129
tests: fix unit tests.\n\nResolves BHUB-130
```
New version is still `1.0.0` because no eligible commit message was found. No new version will be created.

*******

### Github Actions

Github Actions is the main CI tool for this project. It is used to run tests,
lint code and deploy code to our environments. Current files are:

* `.github/workflows/pull_request.yml` - configures GitHub Actions to run unit tests, security scan and lint code.
* `.github/workflows/<ENV>.yml` - Build and push a new docker image for this project and start Deployment process for each environment. Also, in Production, will publish the new version.
