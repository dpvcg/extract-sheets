from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from bs4 import BeautifulSoup
import re

# If modifying these scopes, delete the file token.pickle.
SCOPES = [
    'https://www.googleapis.com/auth/spreadsheets.readonly',
    'https://www.googleapis.com/auth/drive.file',
    'https://www.googleapis.com/auth/drive.readonly',
    'https://www.googleapis.com/auth/drive.metadata.readonly',
]

# The ID and range of a sample spreadsheet.
DOCID = '1Z3Eb5rZjrdWcE5u5o0CYzA_LPyGaTqmg84ecGve_ZLA'


def download_data(DOC):
    """Download data from Google Sheets"""
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', SCOPES)
            creds = flow.run_local_server()
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('drive', 'v3', credentials=creds)
    file_export = service.files().export(fileId=DOC, mimeType="text/html")
    file_export = file_export.execute()
    with open("/tmp/dpvcg.html", "wb") as fd:
        fd.write(file_export)


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
        "w3c.css",
        "https://www.w3.org/StyleSheets/TR/2016/W3C-WD"
        )
    link = '<link rel="stylesheet" href="{css}" type="text/css">'
    s = "".join((link.format(css=css) for css in w3c_css))
    w3c_soup = BeautifulSoup(s, 'lxml')
    soup.head.insert(0, w3c_soup)

    with open("/tmp/dpvcg.html", "w") as fd:
        fd.write(soup.prettify())


if __name__ == "__main__":
    download_data(DOCID)
    pretty_print()
