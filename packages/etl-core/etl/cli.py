"""
Entry-point selon FORGE-KENOBI.md
Interface CLI pour les outils ETL DevSecOps ONCF.
"""

import logging
import sys

import typer
from rich.console import Console
from rich.table import Table

from etl.extractors.gitlab.test_gitlab_connection import (
    GitLabConnectionError,
    check_gitlab_oncf_connection,
)

# Configuration logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

app = typer.Typer(
    name="etl-cli", help="ETL DevSecOps ONCF - Outils de ligne de commande"
)
console = Console()


@app.command("test-gitlab")
def test_gitlab_command(
    gitlab_url: str | None = typer.Option(
        None, "--url", help="URL GitLab ONCF (défaut: variable GITLAB_URL)"
    ),
    gitlab_token: str | None = typer.Option(
        None, "--token", help="Token GitLab (défaut: variable GITLAB_TOKEN)"
    ),
    verbose: bool = typer.Option(
        False, "--verbose", "-v", help="Mode verbeux avec détails"
    ),
) -> None:
    """
    Teste la connexion à GitLab ONCF selon US-001.

    Vérifie l'authentification et récupère les informations utilisateur.
    Timeout: 5 secondes maximum.
    """
    if verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    console.print("\n🔍 [bold blue]Test de connexion GitLab ONCF[/bold blue]")
    console.print("=" * 50)

    try:
        with console.status("[bold green]Connexion en cours..."):
            result = check_gitlab_oncf_connection(gitlab_url, gitlab_token)

        if result["success"]:
            console.print("✅ [bold green]Connexion réussie ![/bold green]\n")

            # Tableau des informations utilisateur
            user_table = Table(title="Informations Utilisateur GitLab ONCF")
            user_table.add_column("Propriété", style="cyan", no_wrap=True)
            user_table.add_column("Valeur", style="magenta")

            user = result["user"]
            user_table.add_row("ID", str(user.get("id", "N/A")))
            user_table.add_row("Username", user.get("username", "N/A"))
            user_table.add_row("Nom complet", user.get("name", "N/A"))
            user_table.add_row("Email", user.get("email", "N/A"))

            console.print(user_table)

            # Informations de connexion
            connection = result["connection"]
            console.print("\n📊 [bold cyan]Statistiques de connexion:[/bold cyan]")
            console.print(f"   • URL: {connection['gitlab_url']}")
            console.print(f"   • Temps de réponse: {connection['response_time_sec']}s")
            console.print(f"   • Code HTTP: {connection['status_code']}")

            console.print(
                "\n🎉 [bold green]Test de connexion terminé avec succès[/bold green]"
            )
            sys.exit(0)

    except GitLabConnectionError as e:
        console.print(f"\n❌ [bold red]Erreur de connexion:[/bold red] {str(e)}")
        console.print("\n💡 [yellow]Vérifiez:[/yellow]")
        console.print("   • Variable GITLAB_URL définie")
        console.print("   • Variable GITLAB_TOKEN valide")
        console.print("   • Connexion réseau à GitLab ONCF")
        sys.exit(1)

    except Exception as e:
        console.print(f"\n💥 [bold red]Erreur inattendue:[/bold red] {str(e)}")
        if verbose:
            console.print_exception()
        sys.exit(1)


def main() -> None:
    """Point d'entrée principal du CLI."""
    app()


if __name__ == "__main__":
    main()
