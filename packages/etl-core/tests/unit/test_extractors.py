"""
Tests unitaires pour les extracteurs ETL selon Kenobi.
"""

from unittest.mock import Mock, patch

import pytest
import requests
from etl.extractors.gitlab.test_gitlab_connection import (
    GitLabConnectionError,
    GitLabExtractor,
    check_gitlab_oncf_connection,
)


class TestGitLabExtractor:
    """Tests de la classe GitLabExtractor."""

    def test_init_with_params(self):
        """Test initialisation avec paramètres explicites."""
        extractor = GitLabExtractor(
            gitlab_url="https://test.gitlab.com", gitlab_token="test-token", timeout=10
        )

        assert extractor.gitlab_url == "https://test.gitlab.com"
        assert extractor.gitlab_token == "test-token"
        assert extractor.timeout == 10
        assert "Private-Token" in extractor.session.headers
        assert extractor.session.headers["Private-Token"] == "test-token"

    @patch.dict(
        "os.environ",
        {"GITLAB_URL": "https://env.gitlab.com", "GITLAB_TOKEN": "env-token"},
    )
    def test_init_with_env_vars(self):
        """Test initialisation avec variables d'environnement."""
        extractor = GitLabExtractor()

        assert extractor.gitlab_url == "https://env.gitlab.com"
        assert extractor.gitlab_token == "env-token"
        assert extractor.timeout == 5  # défaut US-001

    def test_init_missing_url_raises_error(self):
        """Test erreur si GITLAB_URL manquante."""
        with pytest.raises(GitLabConnectionError, match="GITLAB_URL non définie"):
            GitLabExtractor(gitlab_token="token")

    def test_init_missing_token_raises_error(self):
        """Test erreur si GITLAB_TOKEN manquante."""
        with pytest.raises(GitLabConnectionError, match="GITLAB_TOKEN non définie"):
            GitLabExtractor(gitlab_url="https://test.com")


class TestGitLabONCFConnection:
    """Tests de la fonction test_gitlab_oncf_connection."""

    @patch("etl.extractors.gitlab.test_gitlab_connection.GitLabExtractor")
    @patch("etl.extractors.gitlab.test_gitlab_connection.time.time")
    def test_connection_success(self, mock_time, mock_extractor_class):
        """Test connexion réussie selon US-001."""
        # Mock time.time pour contrôler le temps avec suffisamment de valeurs
        mock_time.side_effect = [
            0.0,
            2.5,
            2.5,
            2.5,
            2.5,
        ]  # Plus de valeurs pour les logs

        # Mock de l'extracteur
        mock_extractor = Mock()
        mock_extractor.gitlab_url = "https://gitlab.oncf.net"  # String, pas Mock
        mock_extractor.timeout = 5
        mock_extractor_class.return_value = mock_extractor

        # Mock de la réponse API
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "id": 123,
            "username": "test.user",
            "name": "Test User",
            "email": "test.user@oncf.ma",
        }
        mock_extractor.session.get.return_value = mock_response

        result = check_gitlab_oncf_connection()

        # Vérifications
        assert result["success"] is True
        assert result["user"]["id"] == 123
        assert result["user"]["username"] == "test.user"
        assert result["user"]["name"] == "Test User"
        assert result["user"]["email"] == "test.user@oncf.ma"
        assert result["connection"]["gitlab_url"] == "https://gitlab.oncf.net"
        assert result["connection"]["response_time_sec"] == 2.5
        assert result["connection"]["status_code"] == 200

        # Vérification de l'appel API
        mock_extractor.session.get.assert_called_once()
        call_args = mock_extractor.session.get.call_args
        assert "/api/v4/user" in call_args[0][0]
        assert call_args[1]["timeout"] == 5

    @patch("etl.extractors.gitlab.test_gitlab_connection.GitLabExtractor")
    @patch("etl.extractors.gitlab.test_gitlab_connection.time.time")
    def test_connection_http_error(self, mock_time, mock_extractor_class):
        """Test erreur HTTP 401 Unauthorized."""
        mock_time.side_effect = [0.0, 1.0, 1.0, 1.0, 1.0]  # Plus de valeurs

        # Mock de l'extracteur
        mock_extractor = Mock()
        mock_extractor.gitlab_url = "https://gitlab.oncf.net"
        mock_extractor.timeout = 5
        mock_extractor_class.return_value = mock_extractor

        # Mock de la réponse d'erreur
        mock_response = Mock()
        mock_response.status_code = 401
        mock_response.json.return_value = {"message": "Unauthorized"}
        mock_extractor.session.get.return_value = mock_response

        with pytest.raises(
            GitLabConnectionError, match="Erreur HTTP 401: Unauthorized"
        ):
            check_gitlab_oncf_connection()

    @patch("etl.extractors.gitlab.test_gitlab_connection.GitLabExtractor")
    @patch("etl.extractors.gitlab.test_gitlab_connection.time.time")
    def test_connection_timeout(self, mock_time, mock_extractor_class):
        """Test timeout selon US-001 (5 secondes max)."""
        mock_time.side_effect = [0.0, 5.2, 5.2, 5.2, 5.2]  # Plus de valeurs

        # Mock de l'extracteur
        mock_extractor = Mock()
        mock_extractor.gitlab_url = (
            "https://gitlab.oncf.net"  # AJOUT: gitlab_url manquait !
        )
        mock_extractor.timeout = 5
        mock_extractor_class.return_value = mock_extractor

        # Mock du timeout
        mock_extractor.session.get.side_effect = requests.exceptions.Timeout()

        with pytest.raises(GitLabConnectionError, match="Timeout après 5.2s"):
            check_gitlab_oncf_connection()

    @patch("etl.extractors.gitlab.test_gitlab_connection.GitLabExtractor")
    @patch("etl.extractors.gitlab.test_gitlab_connection.time.time")
    def test_response_time_under_5_seconds(self, mock_time, mock_extractor_class):
        """Test que le temps de réponse respecte la limite US-001 (< 5s)."""
        mock_time.side_effect = [0.0, 3.2, 3.2, 3.2, 3.2]  # Plus de valeurs

        # Mock de l'extracteur
        mock_extractor = Mock()
        mock_extractor.gitlab_url = "https://gitlab.oncf.net"
        mock_extractor.timeout = 5
        mock_extractor_class.return_value = mock_extractor

        # Mock réponse rapide (3.2s)
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "id": 456,
            "username": "fast.user",
            "name": "Fast User",
            "email": "fast@oncf.ma",
        }
        mock_extractor.session.get.return_value = mock_response

        result = check_gitlab_oncf_connection()

        # Vérification temps < 5s selon US-001
        assert result["connection"]["response_time_sec"] == 3.2
        assert result["connection"]["response_time_sec"] < 5.0
