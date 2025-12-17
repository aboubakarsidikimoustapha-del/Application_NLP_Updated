import streamlit as st
from summarizer import extractive_summary, abstractive_summary
from generator import generate_text

# ==============================================================================
#                      Configuration & Internationalisation (i18n)
# ==============================================================================

st.set_page_config(
    page_title="Text Generator & Summarizer",
    page_icon="✍️",
    layout="wide"
)

# Dictionnaire pour les textes de l'interface
i18n = {
    "fr": {
        "page_title": "Générateur & Résumeur de Texte",
        "title": "🤖 Système de Génération et Résumé de Texte NLP",
        "description": "Une application pour générer et résumer des textes, basée sur des modèles Transformers.",
        "sidebar_lang": "Langue",
        "sidebar_nav": "Navigation",
        "feature_summary": "Résumé de Texte",
        "feature_generation": "Génération de Texte",
        "summary_header": "Résumé de Texte",
        "summary_desc": "Collez un texte ci-dessous pour le résumer.",
        "summary_type_label": "Choisissez le type de résumé",
        "summary_type_abs": "Abstractif (avancé, plus lent)",
        "summary_type_ext": "Extractif (baseline, plus rapide)",
        "summary_text_area": "Texte à résumer",
        "summary_placeholder": "Entrez votre texte ici...",
        "summary_button": "Lancer le résumé",
        "summary_result": "Résultat",
        "summary_spinner_abs": "Génération du résumé abstractif en cours...",
        "summary_spinner_ext": "Génération du résumé extractif en cours...",
        "warning_empty_text": "Veuillez entrer un texte à résumer.",
        "generation_header": "Génération de Texte",
        "generation_desc": "Entrez un début de phrase (prompt) pour que le modèle génère la suite.",
        "generation_prompt": "Votre prompt",
        "generation_placeholder": "Par exemple : 'Le futur de l'intelligence artificielle est...'",
        "generation_button": "Générer le texte",
        "generation_result": "Résultat",
        "generation_spinner": "Génération du texte en cours...",
        "warning_empty_prompt": "Veuillez entrer un prompt.",
        "footer_info": "Projet DSC559 – PROJET 3"
    },
    "en": {
        "page_title": "Text Generator & Summarizer",
        "title": "🤖 NLP Text Generation and Summarization System",
        "description": "An application to generate and summarize texts, based on Transformer models.",
        "sidebar_lang": "Language",
        "sidebar_nav": "Navigation",
        "feature_summary": "Text Summary",
        "feature_generation": "Text Generation",
        "summary_header": "Text Summary",
        "summary_desc": "Paste a text below to summarize it.",
        "summary_type_label": "Choose the summary type",
        "summary_type_abs": "Abstractive (advanced, slower)",
        "summary_type_ext": "Extractive (baseline, faster)",
        "summary_text_area": "Text to summarize",
        "summary_placeholder": "Enter your text here...",
        "summary_button": "Run Summary",
        "summary_result": "Result",
        "summary_spinner_abs": "Generating abstractive summary...",
        "summary_spinner_ext": "Generating extractive summary...",
        "warning_empty_text": "Please enter a text to summarize.",
        "generation_header": "Text Generation",
        "generation_desc": "Enter a starting phrase (prompt) for the model to continue.",
        "generation_prompt": "Your prompt",
        "generation_placeholder": "For example: 'The future of artificial intelligence is...'",
        "generation_button": "Generate Text",
        "generation_result": "Result",
        "generation_spinner": "Generating text...",
        "warning_empty_prompt": "Please enter a prompt.",
        "footer_info": "DSC559 Project – PROJECT 3"
    }
}

# ==============================================================================
#                                  Interface
# ==============================================================================

# --- Barre latérale ---
st.sidebar.title(i18n["fr"]["sidebar_lang"] + " / " + i18n["en"]["sidebar_lang"])
lang_choice = st.sidebar.selectbox("", ("Français", "English"))
lang_code = "fr" if lang_choice == "Français" else "en"
T = i18n[lang_code]  # Raccourci pour accéder aux textes de la langue choisie

st.sidebar.title(T["sidebar_nav"])
app_mode = st.sidebar.radio("", (T["feature_summary"], T["feature_generation"]))

# --- Contenu principal ---
st.title(T["title"])
st.markdown(T["description"])

# --- Page Résumé ---
if app_mode == T["feature_summary"]:
    st.header(T["summary_header"])
    st.markdown(T["summary_desc"])

    summary_type = st.selectbox(
        T["summary_type_label"],
        (T["summary_type_abs"], T["summary_type_ext"])
    )
    
    text_to_summarize = st.text_area(T["summary_text_area"], height=250, placeholder=T["summary_placeholder"])

    if st.button(T["summary_button"]):
        if text_to_summarize:
            st.subheader(T["summary_result"])
            spinner_text = T["summary_spinner_abs"] if "Abstractif" in summary_type or "Abstractive" in summary_type else T["summary_spinner_ext"]
            with st.spinner(spinner_text):
                is_abstractive = "Abstractif" in summary_type or "Abstractive" in summary_type
                if is_abstractive:
                    summary = abstractive_summary(text_to_summarize, lang=lang_code)
                else:
                    summary = extractive_summary(text_to_summarize, lang=lang_code)
                st.success(summary)
        else:
            st.warning(T["warning_empty_text"])

# --- Page Génération ---
elif app_mode == T["feature_generation"]:
    st.header(T["generation_header"])
    st.markdown(T["generation_desc"])

    prompt = st.text_input(T["generation_prompt"], placeholder=T["generation_placeholder"])

    if st.button(T["generation_button"]):
        if prompt:
            st.subheader(T["generation_result"])
            with st.spinner(T["generation_spinner"]):
                generated_text = generate_text(prompt, lang=lang_code)
                st.success(generated_text)
        else:
            st.warning(T["warning_empty_prompt"])

# --- Pied de page ---
st.sidebar.markdown("---")
st.sidebar.info(T["footer_info"])
