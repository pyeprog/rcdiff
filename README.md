# Recursive Diff

A command-line utility to compare two directories recursively and identify differences in files.

## Features

- Compare directory structures recursively
- Display files that exist in one directory but not the other
- Show number of differing lines for files present in both directories
- Filter hidden files (configurable)
- Ignore files by extension/postfix

## Installation

### From PyPI

```bash
pip install rcdiff
```

### Build with uv

If you have [uv](https://docs.astral.sh/uv/) installed:

```bash
# Clone the repository
git clone <repository-url>
cd refactor-tool

# Build and install
uv pip install -e .

# Or build the distribution
uv build
```

## Usage

```bash
rcdiff <dir1> <dir2> [options]
```

### Arguments

- `dir1` — First directory to compare
- `dir2` — Second directory to compare

### Options

- `--exclude_hidden_files` — Exclude hidden files (default behavior)
- `--include_hidden_files` — Include hidden files in comparison
- `--ignore_postfixes POSTFIX [POSTFIX ...]` — File extensions to ignore (default: `.pyc`)

### Examples

```bash
# Basic comparison
rcdiff ./old_code ./new_code

# Include hidden files
rcdiff ./old_code ./new_code --include_hidden_files

# Ignore multiple file types
rcdiff ./old_code ./new_code --ignore_postfixes .pyc .log .tmp
```

## Output

Displays a formatted table with:
- **file** — Relative file path
- **in [dir1]** — Whether file exists in first directory (y/empty)
- **in [dir2]** — Whether file exists in second directory (y/empty)
- **diff lines** — Number of differing lines (only shown if differences exist)

### Example Output

```
┏━━━━━━━━━━━━━━┳━━━━━━━━━┳━━━━━━━━━┳━━━━━━━━━━━┓
┃ file         ┃ in old  ┃ in new  ┃ diff lines ┃
┡━━━━━━━━━━━━━━╇━━━━━━━━━╇━━━━━━━━━╇━━━━━━━━━━━┩
│ main.py      │ y       │ y       │ 5          │
│ config.json  │ y       │         │            │
│ test.py      │         │ y       │            │
└──────────────┴─────────┴─────────┴────────────┘
```