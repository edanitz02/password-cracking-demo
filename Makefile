VENV_DIR := venv
PYTHON := $(VENV_DIR)/bin/python
PIP := $(VENV_DIR)/bin/pip

.PHONY: all install setDB run clean

all: install setDB run

install:
	test -d $(VENV_DIR) || python3 -m venv $(VENV_DIR)
	$(PIP) install --upgrade pip
	$(PIP) install psycopg2-binary
	$(PIP) install python-dotenv

setDB: 
	$(PYTHON) databaseSetup.py

run:
	$(PYTHON) bruteForce.py

clean:
	rm -rf $(VENV_DIR)
