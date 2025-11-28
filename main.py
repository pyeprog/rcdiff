from pathlib import Path
import subprocess
from typing import Any
from rich.table import Table
from rich.console import Console
import argparse


def file_map(dir: Path, exclude_hidden_files: bool = True, ignore_postfixes: list[str] | None = None) -> dict[Path, Path]:
    ignore_postfixes = ignore_postfixes or []

    dir_path = Path(dir)
    start_idx = 0 if str(dir_path) == '.' else len(str(dir_path)) + 1

    file_map: dict[Path, Path] = {}
    for root, _, filenames in dir.walk():
        relative_root = Path(str(root)[start_idx:])
        if exclude_hidden_files and str(relative_root).startswith('.'):
            continue

        for filename in filenames:
            if any(filename.endswith(postfix) for postfix in ignore_postfixes):
                continue

            relative_path = relative_root / filename
            file_map[relative_path] = root / filename

    return file_map


def file_diff(file1: Path, file2: Path):
    completed_process = subprocess.run(["diff", str(file1), str(file2)], capture_output=True, text=True)
    return [line for line in completed_process.stdout.split('\n') if line]

def if_(pred: bool, first: Any, second: Any):
    return first if pred else second

def show_diff(dir1: Path, dir2: Path, exclude_hidden_files: bool = True, ignore_postfixes: list[str] | None = None):
    table = Table()
    table.add_column('file', style='royal_blue1')
    table.add_column(f'in {dir1.name}', style='purple', justify='center')
    table.add_column(f'in {dir2.name}', style='light_salmon3', justify='center')
    table.add_column('diff lines', style='chartreuse2', justify='center')

    file_map1 = file_map(dir1, exclude_hidden_files=exclude_hidden_files, ignore_postfixes=ignore_postfixes)
    file_map2 = file_map(dir2, exclude_hidden_files=exclude_hidden_files, ignore_postfixes=ignore_postfixes)

    files = sorted(list(set(file_map1.keys()).union(set(file_map2.keys()))))

    for file in files:
        is_in_dir1 = file in file_map1
        is_in_dir2 = file in file_map2
        diff_lines = ''

        if is_in_dir1 and is_in_dir2:
            if (n_diff_lines := len(file_diff(file_map1[file], file_map2[file]))) > 0:
                diff_lines = str(n_diff_lines)

        if diff_lines != '' or is_in_dir1 ^ is_in_dir2:
            table.add_row(str(file), if_(is_in_dir1, 'y', ''), if_(is_in_dir2, 'y', ''), diff_lines)

    Console().print(table)


def cli():
    parser = argparse.ArgumentParser(description="Compare two directories")
    parser.add_argument("dir1", type=Path, help="First directory")
    parser.add_argument("dir2", type=Path, help="Second directory")

    group = parser.add_mutually_exclusive_group()
    group.add_argument("--exclude_hidden_files", dest="exclude_hidden_files", action="store_true",
                       help="Exclude hidden files (default: True)")
    group.add_argument("--include_hidden_files", dest="exclude_hidden_files", action="store_false",
                       help="Do not exclude hidden files")
    parser.set_defaults(exclude_hidden_files=True)

    parser.add_argument("--ignore_postfixes", action="extend", nargs="+", default=[".pyc"],
                        help="Postfixes to ignore (can be provided multiple times or with multiple values)")

    args = parser.parse_args()

    show_diff(args.dir1, args.dir2, exclude_hidden_files=args.exclude_hidden_files, ignore_postfixes=args.ignore_postfixes)