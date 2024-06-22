import google.generativeai as genai
from src.template import template
from src.crawl import get_body


class NewsGenerator:
    model: genai.GenerativeModel
    builder: list[str]

    def __init__(self, api_key: str, model: str):
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel(model)
        self.builder = []

    def make_header(self, title: str):
        self.builder.append(f'# {title}\n\n')

    def generate(self, url: str):
        try:
            body = get_body(url)
        except Exception as e:
            print(f'Error: {e}')
            return

        if body is None or len(body) == 0:
            return

        chat = self.model.start_chat()
        chat.send_message('''You are a curator of a newsletter about programming method, programming language, database, development, etc.
                          I give you a article or repository about programming and development. You must write in korean.
                          You must write a summary, description, features, usage, recommendation, external links, and caution in markdown script.
                          Write in this format, you can skip optional parts. If you write optional parts, you must remove (optional) or (Optional) in the title:
                          ''' + template)
        resp = chat.send_message(body)

        self.builder.append(''.join([f.text for f in resp.parts]))

    def make_trailer(self):
        self.builder.append('\n## 주의\n\n - 이 글은 Gemini Flash를 이용하여 생성한 것으로, 사실과 다를 수 있습니다.\n\n')

    def __str__(self) -> str:
        return ''.join(self.builder)
