#!/usr/bin/env python3

import os
import sys

class ReferenceChecker:
    """Check References Agains the LiU Journal Check Up Database
    
    Takes a LaTeX file and checks the references against the LiU Journal
    Checkup Database to help in determining whether all references are from
    serious journals."""

    def __init__(self, file_path: str = os.path.join('overleaf', 'main.tex')) -> None:
        """Initialize ReferenceChecker object.
        
        Args:
            file_path: Path of LaTeX file to scan for references.
        """

        # Exit if file does not exist.
        not os.path.isfile(file_path) and sys.exit(f'File {file_path} does not exist.')

def main() -> None:
    """Execute script."""
    pass

def run_script(name: str = __name__) -> None:
    """Run the main function if file is run as a script.
    
    Args:
        name: the __name__ attribute of the script. Defaults to __name__
    """
    if name == '__main__':
        main()

run_script()
