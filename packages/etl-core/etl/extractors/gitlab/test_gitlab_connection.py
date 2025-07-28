"""
GitLab extractor - SPC-GEN-01: snake_case
Module pour extraire les données depuis GitLab ONCF avec authentification sécurisée.
"""

import logging
import os
import time
from typing import Any, Dict, Optional
from urllib.parse import urljoin

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from etl.core.errors import ETLError

logger = logging.getLogger(__name__)


class GitLabConnectionError(ETLError):
    """Erreur de connexion à GitLab ONCF."""

    pass


class GitLabExtractor:
    """Extracteur GitLab ONCF avec authentification par token."""

    def __init__(
        self,
        gitlab_url: Optional[str] = None,
        gitlab_token: Optional[str] = None,
        timeout: int = 5,
    ) -> None:
        """
        Initialise l'extracteur GitLab ONCF.

        Args:
            gitlab_url: URL de l'instance GitLab (défaut: variable GITLAB_URL)
            gitlab_token: Token d'authentification (défaut: variable GITLAB_TOKEN)
            timeout: Timeout en secondes (défaut: 5s selon US-001)
        """
        self.gitlab_url = gitlab_url or os.getenv("GITLAB_URL")
        self.gitlab_token = gitlab_token or os.getenv("GITLAB_TOKEN")
        self.timeout = timeout

        if not self.gitlab_url:
            raise GitLabConnectionError("GITLAB_URL non définie")
        if not self.gitlab_token:
            raise GitLabConnectionError("GITLAB_TOKEN non définie")

        # Configuration session avec retry selon SPC-GEN-05
        self.session = requests.Session()
        retry_strategy = Retry(
            total=3,
            backoff_factor=1,  # 1-4-9s avec jitter
            status_forcelist=[408, 429, 500, 502, 503, 504],
            raise_on_status=False,
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        self.session.mount("http://", adapter)
        self.session.mount("https://", adapter)

        # Headers d'authentification
        self.session.headers.update(
            {"Private-Token": self.gitlab_token, "User-Agent": "supratours-etl/1.0.0"}
        )


def check_gitlab_oncf_connection(
    gitlab_url: Optional[str] = None, gitlab_token: Optional[str] = None
) -> Dict[str, Any]:
    """
    Teste la connexion à GitLab ONCF selon US-001.

    Args:
        gitlab_url: URL GitLab (optionnel, utilise GITLAB_URL par défaut)
        gitlab_token: Token (optionnel, utilise GITLAB_TOKEN par défaut)

    Returns:
        Dict contenant les informations de connexion et utilisateur

    Raises:
        GitLabConnectionError: En cas d'erreur de connexion
    """
    start_time = time.time()

    try:
        extractor = GitLabExtractor(gitlab_url, gitlab_token)

        # Test connexion via /api/v4/user selon US-001
        # Note: gitlab_url est garantie non-None après init de GitLabExtractor
        assert extractor.gitlab_url is not None, "gitlab_url ne peut pas être None"
        api_url = urljoin(extractor.gitlab_url.rstrip("/") + "/", "api/v4/user")

        logger.info(
            "Test connexion GitLab ONCF",
            extra={
                "gitlab_url": extractor.gitlab_url,
                "api_endpoint": "/api/v4/user",
                "timeout": extractor.timeout,
            },
        )

        response = extractor.session.get(api_url, timeout=extractor.timeout)
        elapsed_time = time.time() - start_time

        if response.status_code == 200:
            user_data = response.json()

            # Logs de succès sans token selon US-001
            logger.info(
                "Connexion GitLab ONCF réussie",
                extra={
                    "user_id": user_data.get("id"),
                    "username": user_data.get("username"),
                    "name": user_data.get("name"),
                    "email": user_data.get("email"),
                    "response_time_sec": round(elapsed_time, 3),
                    "status_code": response.status_code,
                },
            )

            return {
                "success": True,
                "user": {
                    "id": user_data.get("id"),
                    "username": user_data.get("username"),
                    "name": user_data.get("name"),
                    "email": user_data.get("email"),
                },
                "connection": {
                    "gitlab_url": extractor.gitlab_url,
                    "response_time_sec": round(elapsed_time, 3),
                    "status_code": response.status_code,
                },
            }
        else:
            error_msg = f"Erreur HTTP {response.status_code}"
            try:
                error_detail = response.json().get("message", "")
                if error_detail:
                    error_msg += f": {error_detail}"
            except Exception:
                pass

            logger.error(
                "Échec connexion GitLab ONCF",
                extra={
                    "status_code": response.status_code,
                    "response_time_sec": round(elapsed_time, 3),
                    "error": error_msg,
                },
            )

            raise GitLabConnectionError(error_msg)

    except requests.exceptions.Timeout:
        elapsed_time = time.time() - start_time
        error_msg = f"Timeout après {elapsed_time:.1f}s"
        logger.error(
            "Timeout connexion GitLab ONCF", extra={"timeout_sec": elapsed_time}
        )
        raise GitLabConnectionError(error_msg)

    except requests.exceptions.ConnectionError as e:
        elapsed_time = time.time() - start_time
        error_msg = f"Erreur de connexion: {str(e)}"
        logger.error(
            "Erreur réseau GitLab ONCF",
            extra={"error": str(e), "elapsed_sec": round(elapsed_time, 3)},
        )
        raise GitLabConnectionError(error_msg)

    except Exception as e:
        elapsed_time = time.time() - start_time
        error_msg = f"Erreur inattendue: {str(e)}"
        logger.error(
            "Erreur inattendue GitLab ONCF",
            extra={"error": str(e), "elapsed_sec": round(elapsed_time, 3)},
        )
        raise GitLabConnectionError(error_msg)
