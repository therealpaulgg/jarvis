# Jarvis

Experimenting with giving OpenAI's GPT direct access to Home Assistant and seeing if it can be the all powerful Jarvis.

Findings so far:

- Use `gpt-4-1106-preview` or `gpt-3.5-turbo-1106` for parallelism.
- GPT-4 is of course smarter than GPT-3.5 and GPT-3.5 needs a little more 'literal' interpretations.
- Sending all of Home Assistant's JSON response is just way too many tokens - results need to be filtered out.
