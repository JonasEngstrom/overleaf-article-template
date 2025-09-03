#!/usr/bin/env python3

import os
import sys
import argparse
import re
import asyncio
import requests

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
        self.parsed_file = self.parse_file(raw_file)
        self.response_dict = {}
    
    def check_if_file_exists(self, file_path: str) -> None:
        """Exit if file does not exist."""
        not os.path.isfile(file_path) and sys.exit(f'File {file_path} does not exist.')
    
    def read_file_contents(self, file_path: str) -> None:
        """Read file contents."""
        with open(file_path, 'r') as read_file:
            raw_file = read_file.readlines()
        
        return raw_file
    
    def parse_file(self, raw_file: list) -> dict:
        """Parse LaTeX file reference list."""
        number_pattern = re.compile('(?<=CSLLeftMargin{)([0-9]*)')
        url_pattern = re.compile('(?<=url{)(.*)(?=}})')
        cached_number = None
        return_dict = {}

        for line in raw_file:
            number = re.search(number_pattern, line)
            url = re.search(url_pattern, line)

            try:
                cached_number = int(number.group())
                return_dict[cached_number] = None
            except:
                pass

            try:
                return_dict[cached_number] = url.group()
            except:
                pass
        
        return return_dict
    
    async def get_request(self, number: int, url: str) -> None:
        """Make an HTTP get request to a URL in a dict, by number key."""
        try:
            response = requests.get(url)
            self.response_dict[number] = {'url': url, 'response': response}
        except:
            self.response_dict[number] = {'url': None, 'response': None}
    
    async def get_all_requests(self) -> None:
        """Make parallel HTTP get requests."""
        await asyncio.gather(*[self.get_request(number, url) for number, url in self.parsed_file.items()])
    
    def get_issns(self) -> None:
        """Extract ISSNs from HTTP resonpses."""
        issn_pattern = re.compile('issn.*([0-9]{4}-[0-9]{4})', re.IGNORECASE)
        for number, data in self.response_dict.items():
            if data['response']:
                data['issn'] = re.search(issn_pattern, data['response'].text)
                if data['issn']:
                    data['issn'] = data['issn'].group(1)
            else:
                data['issn'] = None
        self.response_dict[number] = data

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

    reference_checker = ReferenceChecker(args.file)

def run_script(name: str = __name__) -> None:
    """Run the main function if file is run as a script.
    
    Args:
        name: the __name__ attribute of the script. Defaults to __name__
    """
    if name == '__main__':
        main()

run_script()
