"""Unit tests for ref_check.py, Jonas Engström, 2025-09-03"""

import unittest
import os
import sys
from unittest.mock import patch, mock_open

import ref_check

class TestRefCheck(unittest.TestCase):
    """Test case for ref_check.py."""

    @classmethod
    def setUpClass(cls):
        """Load test fixture from file."""
        with open(os.path.join('tests', 'fixtures', 'ref_snippet.txt'), 'r') as file:
            cls.ref_snippet = file.readlines()
    
    @patch('os.path.isfile', return_value=False)
    def test_file_does_not_exist(self, _) -> None:
        """Test that __init__ exits if file does not exist."""
        with self.assertRaises(SystemExit):
            ref_check.ReferenceChecker('')
    
    @patch('os.path.isfile', return_value=True)
    def test_file_exists(self, _) -> None:
        """Test that __init__ does not exit if file exits."""
        with self.assertRaises(FileNotFoundError):
            ref_check.ReferenceChecker('')
    
    @patch('os.path.isfile', return_value=True)
    @patch('builtins.open', new_callable=mock_open, read_data='data')
    def test_read_file_contents(self, _1, _2) -> None:
        """Test that read_file_contents works correctly."""
        test_checker = ref_check.ReferenceChecker('')
        self.assertEqual(test_checker.read_file_contents(''), ['data'])
    
    @patch('os.path.isfile', return_value=True)
    @patch('builtins.open', new_callable=mock_open)
    def test_parse_file(self, _1, _2):
        """Test that file parses correctly."""
        test_checker = ref_check.ReferenceChecker('')
        self.assertEqual(test_checker.parse_file(self.ref_snippet), {1: 'http://www.tandfonline.com/doi/full/10.3109/00365513.2015.1025427', 2: 'https://onlinelibrary.wiley.com/doi/10.14814/phy2.14939'})

    @patch.object(sys, 'argv', ['ref_check.py'])
    def test_main(self):
        """Test main."""
        ref_check.main()

    def test_run_script(self):
        """Check that script is only run when it is __main__."""
        with patch('ref_check.main') as mock_main:
            ref_check.run_script('__main__')
            mock_main.assert_called_once()
        
        with patch('ref_check.main') as mock_main:
            ref_check.run_script('not_main')
            mock_main.assert_not_called()
