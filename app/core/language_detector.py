from langdetect import detect

SYSTEM_PROMPTS = {
    "tr": "Türkçe olarak yanıt ver. Açık, anlaşılır ve profesyonel bir dil kullan.",
    "en": "Respond in English. Use clear, concise, and professional language.",
    "de": "Antworten Sie auf Deutsch. Verwenden Sie eine klare, prägnante und professionelle Sprache.",
    "es": "Responde en español. Utiliza un lenguaje claro, conciso y profesional.",
    "fr": "Répondez en français. Utilisez un langage clair, concis et professionnel."
}

def detect_language(text: str) -> str:
    """Detect the language of the input text."""
    try:
        lang = detect(text)
        return lang if lang in SYSTEM_PROMPTS else "en"
    except:
        return "en"  # Default to English if detection fails

def format_prompt(user_input: str, detected_lang: str) -> str:
    """Format the prompt with the appropriate system message."""
    system_prompt = SYSTEM_PROMPTS.get(detected_lang, SYSTEM_PROMPTS["en"])
    return f"<s>[INST] {system_prompt}\n\nUser: {user_input} [/INST]"
