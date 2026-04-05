import openai
import time
from loguru import logger

class LLMInterface:
    def __init__(self):
        openai.api_key = os.getenv("OPENAI_API_KEY")
        
    def generate_root_causes(self, log_snippet):
        """Generate root cause hypotheses using GPT-3.5"""
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a root cause analysis expert."},
                    {"role": "user", "content": f"Explain likely causes for this log pattern: {log_snippet}"}
                ],
                temperature=0.7,
                max_tokens=500
            )
            return [self._parse_response(response.choices[0].message.content)]
        except openai.error.RateLimitError:
            logger.warning("OpenAI rate limit exceeded, retrying...")
            time.sleep(10)
            return self.generate_root_causes(log_snippet)
        except Exception as e:
            logger.error(f"LLM generation failed: {str(e)}")
            return []
    
    def _parse_response(self, response_text):
        """Parse LLM response into structured format"""
        lines = response_text.strip().split("\n")
        return {
            "priority": 1,
            "confidence": 0.85,
            "explanation": lines[0].strip()
        }

---