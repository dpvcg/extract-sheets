from bs4 import BeautifulSoup
import re


def bs_preprocess(html):
    """remove distracting whitespaces and newline characters"""
    pat = re.compile('(^[\s]+)|([\s]+$)', re.MULTILINE)
    html = re.sub(pat, '', html)       # remove leading and trailing whitespaces
    html = re.sub('\n', ' ', html)     # convert newlines to spaces
    # this preserves newline delimiters
    html = re.sub('[\s]+<', '<', html) # remove whitespaces before opening tags
    html = re.sub('>[\s]+', '>', html) # remove whitespaces after closing tags
    return html 


def pretty_print():
    with open("/tmp/dpvcg.html", "r") as fd:
        data = bs_preprocess(fd.read())
        soup = BeautifulSoup(data, 'lxml')
    # remove all inline CSS
    for tag in soup():
        for attribute in ("class", "style"):
            del tag[attribute]
    # remove all scripts and styles defined in head (or elsewhere)
    for script in soup(["script", "style"]):
        script.extract()
    # remove pesky spans separating words and paragraphs
    for span in soup.find_all('span'):
        try:
            if span.previous_sibling.name == "span":
                span.previous_sibling.append(span.string)
                span.decompose()
        except Exception as E:
            pass
    # add W3C stylesheet
    w3c_css = (
        # "w3c.css",
        "https://www.w3.org/StyleSheets/TR/2016/W3C-WD",
        )
    link = '<link rel="stylesheet" href="{css}" type="text/css">'
    s = "".join((link.format(css=css) for css in w3c_css))
    w3c_soup = BeautifulSoup(s, 'lxml')
    soup.head.insert(0, w3c_soup)

    with open("/tmp/dpvcg.html", "w") as fd:
        fd.write(soup.prettify())


if __name__ == "__main__":
    pretty_print()
