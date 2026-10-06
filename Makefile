PYTHON  := python3
PIP     := pip3
CONFIG  := config.json

.PHONY: install run debug clean lint lint-strict

# Install project dependencies (pygame). The assigned A-Maze-ing
# maze generator package is installed separately - see README.md.
install:
	$(PIP) install -r requirements.txt

# Run the game with the default configuration file.
# Override with: make run CONFIG=my_config.json
run:
	$(PYTHON) pac-man.py $(CONFIG)

# Run the game under Python's built-in debugger.
debug:
	$(PYTHON) -m pdb pac-man.py $(CONFIG)

# Remove caches and temporary files.
clean:
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	rm -rf .mypy_cache .pytest_cache .coverage

# Mandatory lint: flake8 + mypy with the flags required by the subject.
lint:
	flake8 .
	mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

# Optional stricter lint pass.
lint-strict:
	flake8 .
	mypy . --strict
