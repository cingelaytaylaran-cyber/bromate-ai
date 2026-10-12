import os
import dotenv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import google.generativeai as genai

# Load key from environment (GitHub Secrets / local .env)
dotenv.load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

class BromateAgent:
    def __init__(self):
        self.driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install())
        )
        self.model = genai.GenerativeModel("gemini‑flash")

    def go_to(self, url: str):
        self.driver.get(url)
        return f"Opened: {url} | Page title: {self.driver.title}"

    def close(self):
        self.driver.quit()

    def run_task(self, prompt: str):
        """Basic agent loop: send task → get plan → execute"""
        system_prompt = """
        You are Bromate‑AI, a browser automation agent.
        Reply only with one command: go_to:<url>
        """
        full_prompt = system_prompt + "\nUser task: " + prompt
        resp = self.model.generate_content(full_prompt)
        text = resp.text.strip()
        if text.startswith("go_to:"):
            url = text.split("go_to:")[1].strip()
            return self.go_to(url)
        return "Unknown command"

if __name__ == "__main__":
    agent = BromateAgent()
    print(agent.run_task("Go to github.com"))
    input("Press Enter to close…")
    agent.close()
