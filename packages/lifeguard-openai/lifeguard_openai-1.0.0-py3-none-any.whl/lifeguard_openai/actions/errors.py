import openai

from lifeguard_openai.settings import (
    LIFEGUARD_OPENAI_TOKEN,
    LIFEGUARD_OPENAI_MODEL,
    LIFEGUARD_OPENAI_TEMPERATURE,
    LIFEGUARD_OPENAI_TOP_P,
    LIFEGUARD_OPENAI_FREQUENCY_PENALTY,
    LIFEGUARD_OPENAI_PRESENCE_PENALTY,
    LIFEGUARD_OPENAI_MAX_TOKENS,
    LIFEGUARD_OPENAI_EXPLAIN_ERROR_PROMPT,
)

openai.api_key = LIFEGUARD_OPENAI_TOKEN


def explain_error(validation_response, _settings):
    traceback = validation_response.details.get("traceback", "")
    if traceback:
        response = openai.Completion.create(
            model=LIFEGUARD_OPENAI_MODEL,
            prompt=f"{LIFEGUARD_OPENAI_EXPLAIN_ERROR_PROMPT}\n\n{traceback}",
            temperature=LIFEGUARD_OPENAI_TEMPERATURE,
            top_p=LIFEGUARD_OPENAI_TOP_P,
            frequency_penalty=LIFEGUARD_OPENAI_FREQUENCY_PENALTY,
            presence_penalty=LIFEGUARD_OPENAI_PRESENCE_PENALTY,
            max_tokens=LIFEGUARD_OPENAI_MAX_TOKENS,
        )
        if response.choices:
            validation_response.details["explanation"] = response.choices[0].text
        else:
            validation_response.details["explanation"] = "No explanation available"
    else:
        validation_response.details["explanation"] = "No traceback available"
