import os
from dotenv import load_dotenv

load_dotenv()

class GeminiDocumentGenerator:
    def __init__(self):
        self.api_key = os.getenv("GEMINI_API_KEY")
        self.model_name = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")

        if not self.api_key:
            raise RuntimeError(
                "GEMINI_API_KEY is missing. Add it to your .env file."
            )

        try:
            from google import genai
        except ImportError as exc:
            raise RuntimeError(
                "google-genai is not installed. Run: pip install -r requirements.txt"
            ) from exc

        self.client = genai.Client(api_key=self.api_key)

    def generate_document(
        self,
        document_type: str,
        parties: str,
        terms: str,
        effective_date: str,
    ) -> str:
        prompt = f"""
You are the drafting assistant inside a student project called LegalEase.

Create a structured draft of the requested legal document.

Document type: {document_type}
Parties involved: {parties}
Terms and conditions: {terms}
Effective date: {effective_date}

Requirements:
- Use clear professional language.
- Include a title.
- Include the parties and effective date.
- Organize the document with numbered sections and headings.
- Convert the supplied terms into appropriate clauses.
- Include signature blocks where appropriate.
- Do not invent names, dates, amounts, addresses, or facts that were not supplied.
- If important information is missing, use [TO BE COMPLETED] rather than inventing it.
- Return only the document draft, without Markdown code fences.
- Add a short final notice saying this is an AI-generated draft and should be reviewed by a qualified legal professional before use.
"""

        response = self.client.models.generate_content(
            model=self.model_name,
            contents=prompt,
        )

        text = getattr(response, "text", None)
        if not text:
            raise RuntimeError("Gemini returned an empty response.")

        return text.strip()
