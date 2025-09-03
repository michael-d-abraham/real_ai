# real_ai
This is wheer im going to keep all of the hw assignments. This time im going to do it right lol and keep it organized. 


# simple_search — Reports CLI

This repository provides a small search library and a reports CLI for the Wolf-Goat-Cabbage (WGC) domain.

## Install (editable / development)

Create a virtual environment and install the package in editable mode:

```bash
python -m venv .venv
.venv/bin/pip install --upgrade pip
.venv/bin/pip install -e .
```

Installing editable (`pip install -e .`) makes the `run-reports` console script available locally.

## Run the reports CLI

There are two algorithms supported: `bfs` and `ids`.

Usage (help):

```bash
python -m run_reports -h
# or after installation
run-reports -h
```

Example: run BFS on the three built-in example start states:

```bash
python -m run_reports bfs
```

Run IDS:

```bash
python -m run_reports ids
```

Specify a custom start state using `--start` with 4 characters `L` or `R` (farmer, wolf, goat, cabbage). This is a global option available at the top-level and applies to both `bfs` and `ids` subcommands.

Examples:

```bash
# run BFS on a custom start
python -m run_reports bfs --start LLLL
# or after installation
run-reports ids --start RLRR
```

## Makefile helper

You can use the Makefile target to run both reports (it will create a `.venv` if missing):

```bash
make run_reports
```

This runs the CLI for both `bfs` and `ids` using the three built-in example start states and prints output to stdout.

## Where results are stored

Example combined results are available in `doc/results.md` (generated during development).

## Notes

- The package exposes the CLI entry point `run-reports` via `pyproject.toml`.
- To run the CLI after installation without `python -m`, use `run-reports bfs` or `run-reports ids`.

