from models.interfaces import Email
import google.generativeai as genai
import os

gemini_api_key = os.getenv("GEMINI_API_KEY")
if not gemini_api_key:
    raise ValueError("GEMINI_API_KEY is not set")


class EmailCategorizer:
    def __init__(self, email: Email):
        self.email = email

    def categorize(self) -> str:
        """Categorize an email based on its content."""
        # Generate email category
        genai.configure(api_key=gemini_api_key)
        model = genai.GenerativeModel("gemini-2.0-flash")

        prompt = f"""
            DO NOT provide explanations, clarifications, or additional information.
            JUST return a single category name from the following list:

            - Urgent (requires immediate attention and action)
            - Important (needs attention but not immediate)
            - Draft (email is a draft or marked as draft)
            - Spam (irrelevant or unsolicited)

            Your task:
            1. Carefully read and understand the email content.  
            2. Look for implicit urgency indicators (e.g., payment deadlines, critical errors, client escalations, phrases like "as soon as possible", "immediate", or "critical").  
            3. Avoid misclassifying important or urgent emails as spam, even if they look suspicious.  
            4. Choose the **most appropriate category** for the email(s).

            Email(s) to categorize:
            {self.email}

            JUST return the category name (Urgent, Important, Draft, Spam). No explanations or extra text.
            """
        try:
            category = model.generate_content(prompt)
            return category.text
        except Exception as e:
            raise Exception(f"Error categorizing email: {e}")
