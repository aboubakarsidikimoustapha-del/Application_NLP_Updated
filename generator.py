import streamlit as st
import torch
from transformers import pipeline

# ==============================================================================
#                     Logique de Génération Multilingue
# ==============================================================================

@st.cache_resource
def get_text_generator(lang="fr"):
    """
    Charge et met en cache le modèle de génération de texte approprié pour la langue.
    """
    if lang == "en":
        model_name = "gpt2"
    else:  # Français par défaut
        model_name = "dbddv01/gpt2-french-small"
        
    return pipeline(
        "text-generation",
        model=model_name,
        torch_dtype=torch.bfloat16
    )

def generate_text(prompt, lang="fr", max_length=150):
    """Génère du texte à partir d'un prompt dans la langue choisie."""
    generator = get_text_generator(lang)
    generated_text = generator(prompt, max_length=max_length, num_return_sequences=1)
    return generated_text[0]['generated_text']
