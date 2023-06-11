import openai

openai.api_key = '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'

response = openai.Completion.create(model="text-davinci-003", prompt="Say this is a test", temperature=0, max_tokens=7)