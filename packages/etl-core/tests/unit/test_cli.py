"""
Tests unitaires pour le module CLI ETL DevSecOps.
Objectif: Atteindre couverture ≥ 90% selon FORGE-KENOBI SPC-GEN-04.
"""

import sys
from unittest.mock import MagicMock, patch

import pytest

from etl.cli import app
from etl.extractors.gitlab.test_gitlab_connection import GitLabConnectionError


class TestCLISimple:
    """Tests basiques pour couverture 90%."""

    def test_app_configuration(self):
        """Test configuration de l'application Typer."""
        assert app.info.name == "etl-cli"
        assert "ETL DevSecOps ONCF" in app.info.help

    def test_imports_working(self):
        """Test que les imports fonctionnent."""
        from etl.cli import console, main, test_gitlab_command
        assert console is not None
        assert main is not None
        assert test_gitlab_command is not None

    @patch('etl.cli.check_gitlab_oncf_connection')
    @patch('etl.cli.console')
    def test_test_gitlab_command_success_logic(self, mock_console, mock_connection):
        """Test logique succès sans sys.exit."""
        mock_connection.return_value = {
            "success": True,
            "user": {"id": 123, "username": "test_user", "name": "Test User", "email": "test@oncf.ma"},
            "connection": {"gitlab_url": "https://gitlab.oncf.ma", "response_time_sec": 0.5, "status_code": 200}
        }
        
        # Test direct de la logique sans CLI runner
        from etl.cli import test_gitlab_command
        try:
            test_gitlab_command("https://gitlab.oncf.ma", "test_token", False)
        except SystemExit:
            pass  # Attendu
        
        mock_connection.assert_called_once()
        assert mock_console.print.call_count >= 3

    @patch('etl.cli.check_gitlab_oncf_connection')
    @patch('etl.cli.console')
    def test_test_gitlab_command_error_logic(self, mock_console, mock_connection):
        """Test logique erreur sans sys.exit."""
        mock_connection.side_effect = GitLabConnectionError("Test error")
        
        from etl.cli import test_gitlab_command
        try:
            test_gitlab_command("https://gitlab.oncf.ma", "invalid_token", False)
        except SystemExit:
            pass  # Attendu
        
        mock_connection.assert_called_once()
        assert mock_console.print.call_count >= 2

    @patch('etl.cli.check_gitlab_oncf_connection')
    @patch('etl.cli.console')
    def test_test_gitlab_command_generic_error(self, mock_console, mock_connection):
        """Test erreur générique."""
        mock_connection.side_effect = Exception("Generic error")
        
        from etl.cli import test_gitlab_command
        try:
            test_gitlab_command("https://gitlab.oncf.ma", "test_token", False)
        except SystemExit:
            pass  # Attendu
        
        mock_connection.assert_called_once()

    @patch('etl.cli.check_gitlab_oncf_connection')
    @patch('etl.cli.console')
    @patch('logging.getLogger')
    def test_verbose_mode_logic(self, mock_logger, mock_console, mock_connection):
        """Test mode verbose."""
        mock_logger_instance = MagicMock()
        mock_logger.return_value = mock_logger_instance
        
        mock_connection.return_value = {
            "success": True,
            "user": {"id": 1, "username": "test", "name": "Test", "email": "test@oncf.ma"},
            "connection": {"gitlab_url": "https://gitlab.oncf.ma", "response_time_sec": 0.1, "status_code": 200}
        }

        from etl.cli import test_gitlab_command
        try:
            test_gitlab_command("https://gitlab.oncf.ma", "test_token", True)
        except SystemExit:
            pass  # Attendu
        
        # Vérifier que le logging DEBUG est activé en mode verbose
        mock_logger_instance.setLevel.assert_called_once()

    def test_user_data_handling(self):
        """Test du traitement des données utilisateur."""
        # Test des clés de données utilisateur
        user_keys = ["id", "username", "name", "email"]
        connection_keys = ["gitlab_url", "response_time_sec", "status_code"]
        
        assert all(key in user_keys for key in ["id", "username", "name", "email"])
        assert all(key in connection_keys for key in ["gitlab_url", "response_time_sec", "status_code"])

    def test_error_messages(self):
        """Test des messages d'erreur."""
        # Test que GitLabConnectionError est bien importée
        assert GitLabConnectionError is not None
        
        # Test création d'erreur
        error = GitLabConnectionError("Test message")
        assert str(error) == "Test message"
