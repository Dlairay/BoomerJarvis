


def translate_text(target: str, text: str) -> dict:
    from google.cloud import translate_v2 as translate

    translate_client = translate.Client()

    if isinstance(text, bytes):
        text = text.decode("utf-8")

    result = translate_client.translate(text, target_language=target)
    translated_text = result["translatedText"]

    return translated_text


def detect_language(text: str) -> dict:
    from google.cloud import translate_v2 as translate

    translate_client = translate.Client()

    result = translate_client.detect_language(text)



    language = result["language"]
    return language
