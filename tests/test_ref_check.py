"""Unit tests for ref_check.py, Jonas Engström, 2025-09-03"""

import unittest
import os
import sys
from unittest.mock import patch, mock_open

import ref_check

class TestRefCheck(unittest.TestCase):
    """Test case for ref_check.py."""
    
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
