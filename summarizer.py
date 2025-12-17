import streamlit as st
import torch
from transformers import pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
import re

# ==============================================================================
#                      Logique de Résumé Multilingue
# ==============================================================================

# --- Mots-vides pour le résumé extractif ---
STOP_WORDS_FR = [
    "a", "à", "alors", "au", "aucuns", "aussi", "autre", "avant", "avec", "avoir",
    "bon", "car", "ce", "cela", "ces", "ceux", "chaque", "ci", "comme", "comment",
    "dans", "des", "du", "dedans", "dehors", "depuis", "devrait", "doit", "donc",
    "dos", "début", "elle", "elles", "en", "encore", "essai", "est", "et", "eu",
    "faire", "fait", "faites", "fois", "font", "hors", "ici", "il", "ils", "je",
    "juste", "la", "le", "les", "leur", "là", "ma", "maintenant", "mais", "mes",
    "mien", "moins", "mon", "mot", "même", "ni", "nommés", "notre", "nous",
    "ou", "où", "par", "parce", "pas", "peut", "peu", "plupart", "pour", "pourquoi",
    "quand", "que", "quel", "quelle", "quelles", "quels", "qui", "sa", "sans",
    "ses", "seulement", "si", "sien", "son", "sont", "sous", "soyez", "sujet",
    "sur", "ta", "tandis", "tellement", "tels", "tes", "ton", "tous", "tout",
    "trop", "très", "tu", "voient", "vont", "votre", "vous", "vu", "ça", "étaient",
    "état", "étions", "été", "être"
]

def split_into_sentences(text):
    """Découpe le texte en phrases (agnostique à la langue)."""
    text = re.sub(r'([.!?])([A-Z])', r'\1 \2', text)
    sentences = re.split(r'(?<=[.!?])\s+', text)
    return [s.strip() for s in sentences if s.strip()]

# --- Résumé Abstractif ---

@st.cache_resource
def get_abstractive_summarizer(lang="fr"):
    """
    Charge et met en cache le modèle de résumé abstractif approprié pour la langue.
    """
    if lang == "en":
        model_name = "sshleifer/distilbart-cnn-12-6"
    else:  # Français par défaut
        model_name = "plguillou/t5-base-fr-sum-cnndm"
    
    return pipeline(
        "summarization",
        model=model_name,
        torch_dtype=torch.bfloat16
    )

def abstractive_summary(text, lang="fr", min_length=30, max_length=150):
    """Génère un résumé abstractif dans la langue choisie."""
    summarizer = get_abstractive_summarizer(lang)
    summary = summarizer(text, min_length=min_length, max_length=max_length, truncation=True)
    return summary[0]['summary_text']

# --- Résumé Extractif ---

def extractive_summary(text, lang="fr", num_sentences=3):
    """Génère un résumé extractif dans la langue choisie."""
    sentences = split_into_sentences(text)
    if not sentences or len(sentences) <= num_sentences:
        return text

    # Choisir les mots-vides en fonction de la langue
    stop_words = STOP_WORDS_FR if lang == "fr" else "english"

    vectorizer = TfidfVectorizer(stop_words=stop_words)
    try:
        tfidf_matrix = vectorizer.fit_transform(sentences)
    except ValueError:
        return "Le texte fourni est trop court ou ne contient pas de mots significatifs."

    sentence_scores = np.array(tfidf_matrix.sum(axis=1)).ravel()
    top_sentence_indices = sentence_scores.argsort()[-num_sentences:][::-1]
    top_sentence_indices.sort()

    summary = " ".join([sentences[i] for i in top_sentence_indices])
    return summary
