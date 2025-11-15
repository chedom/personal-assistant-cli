VENV = .venv
PYTHON = $(VENV)/bin/python
PIP = $(VENV)/bin/pip
FLAKE8 = $(VENV)/bin/flake8

.PHONY: venv install lint clean

# Create virtual environment
venv:
	python3 -m venv $(VENV)

# Install dependencies
install: venv
	$(PIP) install -r requirements.txt

# Run PEP8 checks
lint:
	$(FLAKE8) .

test:
	$(PYTHON) -m unittest discover -s tests -v

# Remove venv
clean:
	rm -rf $(VENV)
