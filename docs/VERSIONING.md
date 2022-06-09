## Versioning Guide

Use this guide on how to use VCS on this project.

********

### Installing Git
On Windows, you need to install Git for Windows and the git command line inside WSL. This
is because git must be available in Linux, but the IDEs use git Windows version.

#### Install Git for Windows
* Download [Git for Windows](https://https://git-scm.com/downloads/).
* Inside WSL, install git command line: `sudo apt install git`

#### Install Git for Linux
* Install git command line: `sudo apt install git`

********

### Configuring GitHub
```shell
git config --global user.name "Your Name"
git config --global user.email "Your Email"
```
We recommend you use Github anonymous email account. Example: `<your-user>@users.noreply.github.com`.
On _Windows_, run these config command on both _PowerShell_ and _WSL Bash_.

On _Windows_, make sure the Line Break format is Linux compatible (run on both _PowerShell_ and _WSL Bash_).
```shell
git config --global core.autocrlf false
```

#### Authentication

For authentication, you can use SSH or HTTPS. We recommend using SSH, adding an SSH Key in Linux.
On Windows, please create two keys: one via Powershell and another inside WSL Bash, and update both keys to Github.

Useful links:
* https://docs.github.com/pt/authentication/connecting-to-github-with-ssh/adding-a-new-ssh-key-to-your-github-account
* https://www.techrepublic.com/blog/10-things/how-to-generate-ssh-keys-in-openssh-for-windows-10/

******

### Clone Repository
Best practice is to clone the repository from the GitHub inside a common repository on your Home folder.
Example: `/home/$USER/bhub/`

This is **especially** important on Windows running WSL. Do not clone the repository on `%USER%\Documents\Bhub`
or similar folders (like **OneDrive** for example). Instead, clone it inside WSL folder, such as `\wsl$\Ubuntu\home\$USER\bhub`. Example:

```shell
(Powershell) > wsl  # enter WSL
(Ubuntu)     > mkdir -p ~/bhub
(Ubuntu)     > cd ~/bhub
(Ubuntu)     > git clone ...
```

If you use another drive to save projects, please move entire WSL to new drive: https://blog.iany.me/2020/06/move-wsl-to-another-drive/

********

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

Every pull request, except for the ones which source is from a protected branch, will call the Pull Request workflow.
Every push in a protected branch will call the Push workflow.
