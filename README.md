# personal-assistant-cli
A modular command-line application for managing contacts and notes

## Start
```bash
python main.py
```
## Python Virtual Environment & PEP8 Linting Setup

This project uses a Python virtual environment (`venv`) and a `Makefile`
to automate common development tasks such as installing dependencies and
checking code style using PEP8 (via `flake8` or `pycodestyle`).

## 🚀 Requirements

-   Python 3.7+
-   Make
    -   macOS/Linux: installed by default\
    -   Windows: install Git Bash or Make for Windows

## 📦 Setup

### 1. Create the virtual environment

``` bash
make venv
```

This creates a virtual environment inside the `.venv/` directory and
installs the PEP8 checker.


### 2.Activating the Virtual Environment Manually

-   macOS/Linux:

    ``` bash
    source .venv/bin/activate
    ```

-   Windows:

    ``` bash
    venv\Scripts\activate
    ```

To deactivate:

``` bash
deactivate
```

### 3. Install dependencies

If your project contains a `requirements.txt` file:

``` bash
make install
```

This installs all required packages into the virtual environment.

## 🧹 Code Style Check (PEP8)

To check the project for PEP8 violations using `flake8`:

``` bash
make lint
```

This scans all Python files in the repository and reports any issues.

## 🧼 Clean Up

To remove the virtual environment:

``` bash
make clean
```

## 📁 Makefile Commands Overview

  -----------------------------------------------------------------------
  Command                                 Description
  --------------------------------------- -------------------------------
  `make venv`                             Create the Python virtual
                                          environment and install flake8

  `make install`                          Install project dependencies

  `make lint`                             Run flake8 for PEP8 code-style
                                          checks

  `make clean`                            Delete the virtual environment
  -----------------------------------------------------------------------

