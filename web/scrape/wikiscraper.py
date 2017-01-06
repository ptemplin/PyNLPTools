import urllib.request


class WikiScraper:
    """
    Scrapes the content of Wikipedia pages.
    """

    def __init__(self):
        pass

    def scrape(self, page_name='Web_crawler'):
        """
        Scrapes the content of the named Wikipedia page. Very messy implementation at the moment. Should use FSM.

        :param page_name: of the page to scrape
        :return: the content of the specified page
        """
        text = ''
        con = urllib.request.urlopen("http://en.wikipedia.org/wiki/" + page_name)
        contents = con.read().decode()
        # TODO: Replace this mess with a FSM
        in_body_tag = False
        in_body = False
        in_p = False
        in_link_tag = False
        in_sup_tag = False
        in_footnote = False
        in_b = False
        i = 0
        while i < len(contents):
            if contents[i] == '<':
                if contents[i:i+5] == '<body':
                    in_body_tag = True
                    i += 5
                elif contents[i:i+7] == '</body>':
                    in_body = False
                    i += 7
                elif contents[i:i+3] == '<p>':
                    in_p = True
                    i += 3
                elif contents[i:i+4] == '</p>':
                    in_p = False
                    i += 4
                elif contents[i:i+3] == '<b>':
                    in_b = True
                    i += 3
                elif contents[i:i+4] == '</b>':
                    in_b = False
                    i += 4
                elif contents[i:i+3] == '<a ':
                    in_link_tag = True
                    i += 3
                elif contents[i:i+4] == '</a>':
                    in_link = False
                    i += 4
                elif contents[i:i+5] == '<sup ':
                    in_sup_tag = True
                    i += 5
                elif contents[i:i+6] == '</sup>':
                    in_sup_tag = False
                    i += 6
                else:
                    i += 1
                continue
            elif contents[i] == '>':
                if in_body_tag:
                    in_body_tag = False
                    in_body = True
                elif in_link_tag:
                    in_link_tag = False
                elif in_sup_tag:
                    in_sup_tag = False
            else:
                if in_body and in_p and not in_link_tag and not in_sup_tag:
                    if contents[i] == '[':
                        in_footnote = True
                    elif contents[i] == ']':
                        in_footnote = False
                    else:
                        if not in_footnote:
                            text += contents[i]
            i += 1
        return text


if __name__ == '__main__':
    scraper = WikiScraper()
    user_input = input("Which page would you like to scrape?")
    print(scraper.scrape(user_input))
