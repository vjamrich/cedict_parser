import json

import vertexai
from vertexai.preview.generative_models import GenerativeModel
import vertexai.preview.generative_models as generative_models


def generate_sentences(entries, hsk_clip):
    vertexai.init(project="hanzi-app", location="us-central1")
    # TODO use Gemini 1.5 because otherwise tokenization does work only sometimes
    model = GenerativeModel("gemini-1.0-pro-001")
    safety_settings = {
        generative_models.HarmCategory.HARM_CATEGORY_HATE_SPEECH: generative_models.HarmBlockThreshold.BLOCK_ONLY_HIGH,
        generative_models.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: generative_models.HarmBlockThreshold.BLOCK_ONLY_HIGH,
        generative_models.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: generative_models.HarmBlockThreshold.BLOCK_ONLY_HIGH,
        generative_models.HarmCategory.HARM_CATEGORY_HARASSMENT: generative_models.HarmBlockThreshold.BLOCK_ONLY_HIGH,
    }
    generation_config = {
        "max_output_tokens": 256,
        "temperature": 0.9,
        "top_p": 1
    }

    for entry in entries:
        hsk_2021 = None
        if entry.hsk is not None:
            hsk_2021 = entry.hsk["2021"]

        if hsk_2021 is None or hsk_2021 > hsk_clip:
            continue

        # TODO added traditional - check if it generates just a traditional translation or whole new sentence
        contents = f"""You are a chinese dictionary.
        For chinese word {entry.simplified} ({"; ".join(entry.meanings[0])}) generate example sentence in JSON format.
        Sentence to use words not harder than HSK{hsk_2021}
        {{
            "tokenised_simplified_sentence": <String>[],
            "tokenised_traditional_sentence": <String>[],
            "tokenised_pinyin": <String>[],
            "english_translation": String,
        }}
        """
        response = model.generate_content(
            contents=contents,
            generation_config=generation_config,
            safety_settings=safety_settings,
            stream=False,
        )
        response_json = json.loads(response.text)
        print(response_json)
        # TODO wrap in try catch blocks and count failures. Validate if a correct JSON file is returned. See, if it uses correct inputed word.
