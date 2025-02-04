import openai
import os
from dotenv import load_dotenv

# Load environment variables
dotenv_path = os.path.abspath("config/.env")
load_dotenv(dotenv_path)

# Debugging: Show API Key (Remove this after testing)
print("DEBUG: OpenAI Key Loaded:", os.getenv("OPENAI_API_KEY"))

# Get the OpenAI API key
api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    raise ValueError("⚠️ OpenAI API key not found. Please check your .env file.")

# Initialize OpenAI client with API key
client = openai.OpenAI(api_key=api_key)

def summarize_email(file_path):
    """Reads an email, sends it to OpenAI for summarization, and saves the result."""
    try:
        # Read email content
        with open(file_path, "r") as f:
            email_content = f.read()

        # Use OpenAI API for summarization (Updated for openai>=1.0.0)
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are an email summarization assistant."},
                {"role": "user", "content": f"Summarize this email: {email_content}"}
            ],
            max_tokens=50
        )

        summary = response.choices[0].message.content.strip()

        # Save the summary to a file
        with open("summary_output.txt", "w") as out_f:
            out_f.write(summary)

        print("✅ Summary saved to summary_output.txt")

    except openai.OpenAIError as e:
        print(f"⚠️ OpenAI API Error: {e}")

    except Exception as e:
        print(f"⚠️ An error occurred: {e}")

# Run the summarizer with an example email file
if __name__ == "__main__":
    summarize_email("email_example.txt")

