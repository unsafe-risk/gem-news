from src.generative import NewsGenerator

api_key = '<YOUR_API_KEY>'
model = 'gemini-1.5-flash'

title = '[GDC] Weekly Newsletter #1'
urls = [
    "https://www.pingcap.com/event/tidb-public-beta-launch-and-ai-ecosystem-insights/",
    "https://blog.quastor.org/p/uber-tracks-billions-trips-1",
    "https://www.awelm.com/posts/simple-db/",
    "https://developer.confluent.io/what-is-apache-kafka/?utm_medium=marketingemail&utm_campaign=tm.campaigns_cd"
    ".general-welcome-4.0-nurture-email1-prg.global_&utm_source=marketo&utm_content=&utm_keyword=",
    "https://newsletter.systemdesigncodex.com/p/caching-at-multiple-levels",
    "https://medium.com/@sjksingh/postgresql-primary-key-dilemma-uuid-vs-bigint-52008685b744"
]


def main():
    generator = NewsGenerator(api_key, model)

    generator.make_header(title)
    for url in urls:
        generator.generate(url)
    generator.make_trailer()

    print(generator)


if __name__ == '__main__':
    main()