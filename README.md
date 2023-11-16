# Jarvis

## Warning

__THIS IS A BUGGY AND EXPERIMENTAL PROTOTYPE. It is more than likely not a good idea to try to run this in your actual house. This gives GPT the ability to do a lot of stuff with Home Assistant, and there are no guardrails. A lot of work needs to be done if this was to be an actual useful assistant that doesn't hallucinate a bunch and help with decent accuracy.__

## About

Experimenting with giving OpenAI's GPT direct access to Home Assistant and seeing if it can be the all powerful Jarvis.

Findings so far:

- Use `gpt-4-1106-preview` or `gpt-3.5-turbo-1106` for parallelism.
- GPT-4 is of course smarter than GPT-3.5 and GPT-3.5 needs a little more 'literal' interpretations.
- Sending all of Home Assistant's JSON response is just way too many tokens - results need to be filtered out.

## How To Use

1. set up a .env file with ACCESS_TOKEN, HOME_ASSISTANT_URL
2. Run the project with `python app/main.py`