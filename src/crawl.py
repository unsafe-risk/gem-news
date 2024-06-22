from urllib.robotparser import RobotFileParser
from requests import get

agent = "geminer/0.1"


def get_body(url: str) -> str:
    robots_url = 'https://' + url.lstrip('https://').split('/')[0] + '/robots.txt'

    rp = RobotFileParser()
    rp.set_url(robots_url)
    rp.read()

    if not rp.can_fetch(useragent=agent, url=url):
        raise Exception('This site reject crawl.')

    response = get(url)

    if response.status_code != 200:
        raise Exception('Failed to get body.')

    return response.text
