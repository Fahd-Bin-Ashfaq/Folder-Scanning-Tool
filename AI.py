# AISummary.py

import openai

# Paste your OpenAI API key here
openai.api_key = "your-openai-api-key"

def generate_summary(summary_text):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # Or "gpt-4" if you have access
            messages=[
                {"role": "system", "content": "You are an assistant that summarizes folder metadata."},
                {"role": "user", "content": summary_text}
            ],
            max_tokens=100,
            temperature=0.5
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Error: {e}"
