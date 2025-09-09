# A* Search for 8-Puzzle

Simple A* search implementation with multiple heuristics for solving 8-puzzle problems.

## Usage

Run A* search with different heuristics:

```bash
# UCS baseline (h=0)
python -m simple_search.reports.run_reports ucs

# A* with Manhattan Distance
python -m simple_search.reports.run_reports h1

# A* with Linear Conflict + Manhattan
python -m simple_search.reports.run_reports h2

## Custom Start States

Specify a custom 8-puzzle start state using `--start` with 9 digits (0-8):

```bash
# Run Manhattan Distance on custom puzzle
python -m simple_search.reports.run_reports --start 123405678 h1

# Run UCS on custom puzzle  
python -m simple_search.reports.run_reports --start 123405678 ucs
```

## Heuristics

- **ucs**: Uniform Cost Search (h=0) - baseline
- **h1**: Manhattan Distance - admissible and consistent
- **h2**: Linear Conflict + Manhattan - stronger admissible

## Help

```bash
python -m simple_search.reports.run_reports --help
```

