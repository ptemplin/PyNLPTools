from web.scrape.wikiscraper import WikiScraper

if __name__ == '__main__':
    for page in ('Canada', 'Japan', 'China', 'Germany', 'Egypt'):
        scraper = WikiScraper()
        print(scraper.scrape(page))
