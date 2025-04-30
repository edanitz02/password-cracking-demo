VENV_DIR := venv
PYTHON := $(VENV_DIR)/bin/python
PIP := $(VENV_DIR)/bin/pip

.PHONY: all install plainText setHashed setSaltedHashed dictionary clean

all: install setPlainText dictionary

install:
	test -d $(VENV_DIR) || python3 -m venv $(VENV_DIR)
	$(PIP) install --upgrade pip
	$(PIP) install psycopg2-binary
	$(PIP) install python-dotenv 
	$(PYTHON) attacks/generateRainbow.py attacks/passwords.txt attacks/rainbow.csv

setPlainText: 
	$(PYTHON) databaseSetup/plainText.py databaseSetup/accounts.sql

setHashed:
	$(PYTHON) databaseSetup/hash.py databaseSetup/accounts.sql

setSaltedHashed:
	$(PYTHON) databaseSetup/saltHash.py databaseSetup/accounts.sql

dictionary:
	$(PYTHON) attacks/dictionary.py attacks/passwords.txt

brute:
	$(PYTHON) attacks/bruteForce.py 3

rainbow:
	$(PYTHON) attacks/rainbow.py attacks/rainbow.csv

johnTest:
	$(PYTHON) johnTest/john.py johnTest/john.txt

clean:
	rm -rf $(VENV_DIR)
