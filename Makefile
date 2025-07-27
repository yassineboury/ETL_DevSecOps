# ETL DevSecOps Monorepo Makefile
.PHONY: help setup clean test build lint format install-deps

# Configuration
PYTHON := python3
PIP := pip3
VENV_DIR := venv
ETL_DIR := packages/etl-core
KENOBI_DIR := packages/kenobi-forge
SHARED_DIR := packages/shared

# Couleurs pour l'affichage
RED := \033[31m
GREEN := \033[32m
YELLOW := \033[33m
BLUE := \033[34m
RESET := \033[0m

help: ## Affiche cette aide
	@echo "$(BLUE)ETL DevSecOps Monorepo - Commandes disponibles:$(RESET)"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  $(GREEN)%-20s$(RESET) %s\n", $$1, $$2}'

setup: ## Installation complète de l'environnement
	@echo "$(YELLOW)🚀 Configuration de l'environnement ETL DevSecOps...$(RESET)"
	@if [ ! -d "$(VENV_DIR)" ]; then \
		echo "$(BLUE)Création de l'environnement virtuel...$(RESET)"; \
		$(PYTHON) -m venv $(VENV_DIR); \
	fi
	@echo "$(BLUE)Activation de l'environnement virtuel...$(RESET)"
	@. $(VENV_DIR)/bin/activate && \
		$(PIP) install --upgrade pip && \
		$(PIP) install -r requirements.txt || echo "requirements.txt non trouvé, création..."
	@$(MAKE) install-deps
	@echo "$(GREEN)✅ Configuration terminée!$(RESET)"

install-deps: ## Installation des dépendances de tous les modules
	@echo "$(YELLOW)📦 Installation des dépendances...$(RESET)"
	@. $(VENV_DIR)/bin/activate && \
		if [ -f "$(ETL_DIR)/requirements.txt" ]; then \
			echo "$(BLUE)Installation dépendances ETL Core...$(RESET)"; \
			$(PIP) install -r $(ETL_DIR)/requirements.txt; \
		fi && \
		if [ -f "$(KENOBI_DIR)/requirements.txt" ]; then \
			echo "$(BLUE)Installation dépendances Kenobi-Forge...$(RESET)"; \
			$(PIP) install -r $(KENOBI_DIR)/requirements.txt; \
		fi && \
		if [ -f "$(SHARED_DIR)/requirements.txt" ]; then \
			echo "$(BLUE)Installation dépendances Shared...$(RESET)"; \
			$(PIP) install -r $(SHARED_DIR)/requirements.txt; \
		fi

test: ## Exécute tous les tests
	@echo "$(YELLOW)🧪 Exécution des tests...$(RESET)"
	@. $(VENV_DIR)/bin/activate && \
		if [ -d "$(ETL_DIR)/tests" ]; then \
			echo "$(BLUE)Tests ETL Core...$(RESET)"; \
			cd $(ETL_DIR) && $(PYTHON) -m pytest tests/ -v; \
		fi && \
		if [ -d "$(KENOBI_DIR)/tests" ]; then \
			echo "$(BLUE)Tests Kenobi-Forge...$(RESET)"; \
			cd $(KENOBI_DIR) && $(PYTHON) -m pytest tests/ -v; \
		fi

lint: ## Vérifie la qualité du code
	@echo "$(YELLOW)🔍 Vérification qualité du code...$(RESET)"
	@. $(VENV_DIR)/bin/activate && \
		if command -v flake8 >/dev/null 2>&1; then \
			echo "$(BLUE)Linting avec flake8...$(RESET)"; \
			flake8 $(ETL_DIR) $(KENOBI_DIR) $(SHARED_DIR) --exclude=$(VENV_DIR); \
		fi && \
		if command -v black >/dev/null 2>&1; then \
			echo "$(BLUE)Vérification formatage avec black...$(RESET)"; \
			black --check $(ETL_DIR) $(KENOBI_DIR) $(SHARED_DIR); \
		fi

format: ## Formate le code automatiquement
	@echo "$(YELLOW)✨ Formatage du code...$(RESET)"
	@. $(VENV_DIR)/bin/activate && \
		if command -v black >/dev/null 2>&1; then \
			echo "$(BLUE)Formatage avec black...$(RESET)"; \
			black $(ETL_DIR) $(KENOBI_DIR) $(SHARED_DIR); \
		fi && \
		if command -v isort >/dev/null 2>&1; then \
			echo "$(BLUE)Tri des imports avec isort...$(RESET)"; \
			isort $(ETL_DIR) $(KENOBI_DIR) $(SHARED_DIR); \
		fi

build: ## Build tous les modules
	@echo "$(YELLOW)🔨 Build des modules...$(RESET)"
	@. $(VENV_DIR)/bin/activate && \
		if [ -f "$(ETL_DIR)/setup.py" ]; then \
			echo "$(BLUE)Build ETL Core...$(RESET)"; \
			cd $(ETL_DIR) && $(PYTHON) setup.py build; \
		fi && \
		if [ -f "$(KENOBI_DIR)/setup.py" ]; then \
			echo "$(BLUE)Build Kenobi-Forge...$(RESET)"; \
			cd $(KENOBI_DIR) && $(PYTHON) setup.py build; \
		fi

clean: ## Nettoie les fichiers temporaires
	@echo "$(YELLOW)🧹 Nettoyage...$(RESET)"
	@find . -type f -name "*.pyc" -delete
	@find . -type d -name "__pycache__" -delete
	@find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	@find . -type d -name "build" -exec rm -rf {} + 2>/dev/null || true
	@find . -type d -name "dist" -exec rm -rf {} + 2>/dev/null || true
	@echo "$(GREEN)✅ Nettoyage terminé!$(RESET)"

status: ## Affiche le statut du monorepo
	@echo "$(BLUE)📊 Statut ETL DevSecOps Monorepo:$(RESET)"
	@echo "$(YELLOW)Modules disponibles:$(RESET)"
	@if [ -d "$(ETL_DIR)" ]; then echo "  $(GREEN)✅ ETL Core$(RESET)"; else echo "  $(RED)❌ ETL Core$(RESET)"; fi
	@if [ -d "$(KENOBI_DIR)" ]; then echo "  $(GREEN)✅ Kenobi-Forge$(RESET)"; else echo "  $(RED)❌ Kenobi-Forge$(RESET)"; fi
	@if [ -d "$(SHARED_DIR)" ]; then echo "  $(GREEN)✅ Shared$(RESET)"; else echo "  $(RED)❌ Shared$(RESET)"; fi
	@echo "$(YELLOW)Environnement:$(RESET)"
	@if [ -d "$(VENV_DIR)" ]; then echo "  $(GREEN)✅ Virtual Environment$(RESET)"; else echo "  $(RED)❌ Virtual Environment$(RESET)"; fi

dev-etl: ## Mode développement ETL Core
	@echo "$(YELLOW)🔧 Mode développement ETL Core...$(RESET)"
	@. $(VENV_DIR)/bin/activate && cd $(ETL_DIR) && $(PYTHON) -m pip install -e .

dev-kenobi: ## Mode développement Kenobi-Forge
	@echo "$(YELLOW)🔧 Mode développement Kenobi-Forge...$(RESET)"
	@. $(VENV_DIR)/bin/activate && cd $(KENOBI_DIR) && $(PYTHON) -m pip install -e .

# Raccourcis
s: setup
t: test
l: lint
f: format
b: build
c: clean

# Affichage par défaut
.DEFAULT_GOAL := help
