import unittest
from unittest.mock import patch
from api import login


class TestLogin(unittest.TestCase):
    @patch('api.login.conn.cursor')
    @patch('api.login.conn.close')
    def test_successful_login(self, mock_close, mock_cursor):
        # Mock database cursor
        mock_fetchone = mock_cursor.return_value.fetchone
        mock_fetchone.return_value = ('test_user',)
        
        # Call the login function with a valid key
        result = login.login('test_key')
        
        # Assert that the function returns True
        self.assertTrue(result)
        
        # Assert that the cursor is used to execute the SQL query
        mock_cursor.assert_called_once()
        mock_cursor.return_value.execute.assert_called_once_with("SELECT * FROM users WHERE key = %s", ('test_key',))
        
        # Assert that the database connection is closed
        mock_close.assert_called_once()

    @patch('api.login.conn.cursor')
    @patch('api.login.conn.close')
    def test_invalid_key(self, mock_close, mock_cursor):
        # Mock database cursor
        mock_fetchone = mock_cursor.return_value.fetchone
        mock_fetchone.return_value = None
        
        # Call the login function with an invalid key
        result = login.login('invalid_key')
        
        # Assert that the function returns False
        self.assertFalse(result)
        
        # Assert that the cursor is used to execute the SQL query
        mock_cursor.assert_called_once()
        mock_cursor.return_value.execute.assert_called_once_with("SELECT * FROM users WHERE key = %s", ('invalid_key',))
        
        # Assert that the database connection is closed
        mock_close.assert_called_once()
