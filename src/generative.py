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

    def generate(self, url: str) -> bool:
        try:
            body = get_body(url)
        except Exception as e:
            return False

        if body is None or len(body) == 0:
            return False

        chat = self.model.start_chat()
        chat.send_message('''You are a curator of a newsletter about programming method, programming language, database, development, etc.
                          I give you a article or repository about programming and development. You must write in korean.
                          You must write a summary, description, features, usage, recommendation, external links, and caution in markdown script.
                          Origin URL: ''' + url + '''.
                          Write in this format, you can skip unnecessary parts:
                          ''' + template)
        resp = chat.send_message(body)

        self.builder.append(''.join([f.text for f in resp.parts]))

        return True

    def make_trailer(self, urls: list[str] = None):
        self.builder.append('\n## 주의\n\n - 이 글은 Gemini Flash를 이용하여 생성한 것으로, 사실과 다를 수 있습니다.\n\n')
        if urls is not None:
            self.builder.append('## 출처\n\n')
            for i, url in enumerate(urls):
                self.builder.append(f' - [{url}]({url})\n')

    def __str__(self) -> str:
        return ''.join(self.builder)
