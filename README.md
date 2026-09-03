# Conseil des IAs

Système multi-agents où plusieurs LLM répondent à la même question,
relisent les réponses des autres, puis un arbitre synthétise.

## Architecture

1. **Tour 1** — chaque modèle répond indépendamment, sans voir les autres.
2. **Tour 2** — chacun reçoit les avis anonymisés du conseil et révise sa position.
3. **Synthèse** — un modèle arbitre identifie les désaccords et tranche.

## Composition du conseil

Des modèles de familles différentes, dont plusieurs non-occidentaux :
des modèles entraînés de façon similaire se trompent de la même façon,
et un consensus entre eux ne prouve rien.

## Utilisation

    pip install openai python-dotenv

Créer un fichier `.env` avec `OPENROUTER_API_KEY=...`, puis :

    python conseil.py

## État

Prototype. Code écrit avec assistance IA, architecture et choix de conception personnels.