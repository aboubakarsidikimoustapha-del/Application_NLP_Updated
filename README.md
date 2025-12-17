# Système de Génération et Résumé de Texte

Ce projet est une application NLP (Natural Language Processing) développée dans le cadre du cours DSC559.

## Fonctionnalités

- **Résumé de texte** : Propose des résumés extractifs (baseline) et abstractifs (modèles Transformers).
- **Génération de texte** : Génère du texte à partir d'un prompt en utilisant des modèles de type GPT-2.
- **Support Multilingue** : L'application prend en charge le **français** et l'**anglais**.

L'interface est construite avec Streamlit et les modèles de NLP proviennent de la bibliothèque Hugging Face Transformers.

## Installation

1. Clonez ce dépôt.
2. Assurez-vous d'avoir Python 3.8+ installé.
3. Installez les dépendances nécessaires en exécutant la commande suivante :

```bash
pip install -r requirements.txt
```

## Lancement de l'application

Pour démarrer l'application, exécutez la commande suivante à la racine du projet :

```bash
streamlit run app.py
```

L'application devrait s'ouvrir automatiquement dans votre navigateur.
