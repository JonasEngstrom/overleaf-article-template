#!/usr/bin/env python3

import os
import sys
import argparse

default_file_path = os.path.join('overleaf', 'main.tex')

class ReferenceChecker:
    """Check References Against the LiU Journal Check Up Database
    
    Takes a LaTeX file and checks the references against the LiU Journal
    Checkup Database to help in determining whether all references are from
    serious journals."""

    def __init__(self, file_path: str) -> None:
        """Initialize ReferenceChecker object.
        
        Args:
            file_path: Path of LaTeX file to scan for references.
        """
        self.check_if_file_exists(file_path)
        raw_file = self.read_file_contents(file_path)
    
    def check_if_file_exists(self, file_path: str) -> None:
        """Exit if file does not exist."""
        not os.path.isfile(file_path) and sys.exit(f'File {file_path} does not exist.')
    
    def read_file_contents(self, file_path: str) -> None:
        """Read file contents."""
        with open(file_path, 'r') as read_file:
            raw_file = read_file.readlines()
        
        return raw_file

def main() -> None:
    """Execute script."""
    parser = argparse.ArgumentParser(
        description='Checks references in a LaTeX file against the LiU Journal Check Up database.',
        epilog='Jonas Engström, 2025-09-03',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument(
        '-f',
        '--file',
        default=default_file_path,
        help='LaTeX file path',
        metavar='LaTeX File'
    )
    args = parser.parse_args()

def run_script(name: str = __name__) -> None:
    """Run the main function if file is run as a script.
    
    Args:
        name: the __name__ attribute of the script. Defaults to __name__
    """
    if name == '__main__':
        main()

run_script()
