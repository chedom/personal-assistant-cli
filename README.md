# personal-assistant-cli
A command-line Personal Assistant application developed in Python.
The tool provides a structured way to manage contacts and notes, offering a set of intuitive commands and color-styled output for improved readability.

## Features

### Contacts Management
- Add contacts with multiple phone numbers.
- Edit, search, and delete phone numbers.
- Store and update email, birthday, and address.
- Find contacts by partial match or pattern.
- Show upcoming birthdays within a number of days.
- List all contacts with color-styled output.

### Notes Management
- Create notes with title, body, and tags.
- Search notes by text or by tags.
- Edit title, body, or tags.
- Sort notes by tags.
- Delete notes.
- Display notes in detailed or preview format.

### CLI and User Experience
- Color styled output (errors, warnings, success messages, sections, parameters).
- Structured, colorized help command for easy navigation.
- Centralized styling system (`ui/output_util.py`).
- Error-handling decorator for consistent exception formatting.
- Persistent storage using repositories (pickle or JSON serializers).

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

## Start CLI assistant
Run the main command-line interface:
```bash
python main.py
```

## Run interactive demo
Start the demo script to see automated interactions.

During the demo, you can press the **SPACE** key to pause or resume execution:
```bash
python demo.py
```

## Usage

Type any command in the prompt:

```
Enter a command:
```

Examples:

```
add John 123456789
change John 123456789 987654321
phone John
all
find Jo
set-birthday John 12.04.1990
birthdays 7
delete-contact John
```

Notes examples:

```
add-note Buy milk
notes
note 1
edit-note-title 1 Updated title
find-notes milk
delete-note 1
```

To exit:
```
exit
```

To view help:
```
help
```

## Color Styling

The project uses `colorama` to highlight:
- Errors in red
- Success messages in green
- Warnings in yellow
- Validation messages in magenta
- Sections and commands in structured, readable formats

Centralized styling is implemented in:

```
ui/output_util.py
```

## Error Handling

All command functions are wrapped with the `input_error` decorator.  
It handles:
- AlreadyExistError
- NotFoundError
- KeyError
- ValueError
- IndexError

Errors are formatted consistently and displayed in color.

## Storage

Contacts and notes are stored using **repositories**.

By default, the data is serialized using **pickle**.  
You can also use the **JSON serializer** if needed.

```
storage/pickle_storage.py
```

Data is saved automatically on exit.

## Development Notes

- The application is fully modular.
- Commands are separated from business logic.
- Data validation is implemented at model level.
- Each model provides formatted and color-styled output.
- The help system is generated dynamically and styled for readability.