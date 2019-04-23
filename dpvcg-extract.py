from __future__ import print_function
import pickle
import os.path
import sys, getopt
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

import html
from collections import namedtuple
from dataclasses import dataclass
from typing import List

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']

# The ID and range of a sample spreadsheet.
DOCID = '13d1eRXZZBCw84vYGoCJeMU08rzkkzadDzxY3n2iOi8k'
SHEET = 'BaseOntology'

# These are the columns in the sheet
FIELDS = (
    "type", "term", "description", "domain", "range", "super", "sub",
    "related_terms", "related_how", "comments",
    "source", "created", "status", "rdfs_comments", "contributor", "approved", "resolution")
Template = namedtuple('Template', FIELDS)


def download_data(SHEET_NAME):
    """Download data from Google Sheets"""
    creds = None
    SHEET_RANGE = SHEET_NAME + '!A:Q'
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

    service = build('sheets', 'v4', credentials=creds)

    # Call the Sheets API
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=DOCID,
                                range=SHEET_RANGE).execute()
    values = result.get('values', [])

    
    if not values:
        print('No data found.')

    return values


def extract_classes_properties(data):
    """Extract classes and properties from downloaded data"""

    def _extract_data(row):
        # ensure that the row contains a field for every column
        # this function can also be used for data cleaning
        # remove surrounding whitespaces
        row = [item.strip().replace('\n', ' ') for item in row]
        if len(row) < len(FIELDS):
            row += [''] * (len(FIELDS) - len(row))
        return row
    
    classes = []
    properties = []
    for row in data:
        # if row is not empty
        if(len(row)):
            # if row is about a Class
            if(row[0]=='Class'):
                classes.append(Template(*_extract_data(row)))
            # if row is about a Property
            elif(row[0]=='Property'):
                properties.append(Template(*_extract_data(row)))
    return classes, properties


def document_toc(classes, properties):
    if classes:
        print('<h4>Classes</h4>')
        print('<table border="1"><tr><th>Classes:</th></tr>')
        for item in classes:
            print(f'<tr><td><a href="#{item.term}">{item.term}</a></td></tr>')
        print("</table>")

    if properties:
        print('<h4>Properties</h4>')
        print('<table border="1"><tr><th>Properties:</th></tr>')
        for item in properties:
            print(f'<tr><td><a href="#{item.term}">{item.term}</a></td></tr>')
        print("</table>")


def document_classes(classes, properties):
    """Generate documentation for classes"""
    for cl in classes:
        print(f'<h4>Class: <a id="{cl.term}">{cl.term}<a></h4>')
        print(f'<div>{cl.description}</div>')
        print('<ul>')
        print('<li><b>Status</b>: ')
        if cl.status:
            print(f'{cl.status} ')
        props = []
        if cl.created:
            props.append(f'created: {cl.created}')
        if cl.approved:
            props.append(f'approved: {cl.approved}')
        if cl.contributor:
            props.append(f'proposed by: {cl.contributor}')
        if props:
            print('(' + '; '.join(props) + ')</li>')
        if cl.super:
            print('<li> <b>Superclasses</b>: ')
            scs = cl.super.split(',')
            for sc in scs:
                print(f'<a href="#{sc}">{sc}<a>')
            print('</li>')
            print('<br/>')
        # TODO: add sub-classes

        domains = []
        for prop in properties:
           if (cl.term in prop.domain):
               domains.append(f'<a href="#{prop.term}">{prop.term}</a>')
        ranges = []
        for prop in properties:
           if (cl.term in prop.range):
               ranges.append(f'<a href="#{prop.term}">{prop.term}</a>')
        if domains or ranges:
            if domains:
                print('<li> <b>In Domain Of</b>: ')     
                print(', '.join(domains))
                print('</li>')
            if ranges:
                print('<li> <b>In Range Of</b>: ')     
                print(', '.join(ranges))       
                print('</li>')
        print('</ul>')


def document_properties(classes, properties):
    """Generate documentation for properties"""
    for prop in properties:
        print(f'<h4>Property: <a id="{prop.term}">{prop.term}<a></h4>')
        print(f'<div>{prop.description}</div>')
        print('<ul>')
        print('<li><b>Status</b>: ')
        if prop.status:
            print(f'{prop.status} ')
        props = []
        if prop.created:
            props.append(f'created: {prop.created}')
        if prop.approved:
            props.append(f'approved: {prop.approved}')
        if prop.contributor:
            props.append(f'proposed by: {prop.contributor}')
        if props:
            print('(' + '; '.join(props) + ')</li>')
        if prop.super:
            print('<li> <b>SuperProperties</b>: ')
            sprops = prop.super.split(',')
            for sp in sprops:
                print(f'<a id="#{sp}">{sp}<a>')
            print('</li>')
            print('<br/>')
        # TODO: add sub-properties

        if prop.domain:
            print(f'<li> <b>Domain</b>: {prop.domain}</li>')
        if prop.range: 
            print(f'<li> <b>Range</b>: {prop.range}</li>')
        print('</ul>')


def generate_rdf(classes, properties):
    """Generate the RDF/OWL file for this ontology"""
    code = []
    for cl in classes:
        serialization = []
        serialization.append(f'{cl.term} a rdfs:Class')
        serialization.append(f'    dct:description "{cl.description}"@en')
        if cl.super:
            serialization.append(f'    rdfs:subClassOf {cl.super}')
        if cl.created:
            serialization.append(f'    dct:created "{cl.created}"^^xsd:date')
        if cl.approved:
            serialization.append(f'    dct:date-accepted "{cl.approved}"^^xsd:date')
        if cl.contributor:
            serialization.append(f'    dct:creator "{cl.contributor}"')
        code.append(serialization)
        
    for prop in properties:
        serialization = []
        serialization.append(f'{prop.term} a rdfs:Property')
        serialization.append(f'    dct:description "{prop.description}"@en')
        serialization.append(f'    rdfs:domain {prop.domain}')
        serialization.append(f'    rdfs:range {prop.range}')
        # TODO: add superproperty
        if prop.created:
            serialization.append(f'    dct:created "{prop.created}"^^xsd:date')
        if prop.approved:
            serialization.append(f'    dct:date-accepted "{prop.approved}"^^xsd:date')
        if prop.contributor:
            serialization.append(f'    dct:creator "{prop.contributor}"')
        code.append(serialization)

    print('<h2>RDF</h2>')
    print('<code><pre>')
    print(html.escape('@prefix dct: <http://purl.org/dc/terms/> .'))
    print(html.escape('@prefix dpv: <http://w3.org/ns/dpv#> .'))
    print(html.escape('@prefix dpv-gdpr: <http://w3.org/ns/dpv-gdpr#> .'))
    print(html.escape('@prefix rdfs: http://www.w3.org/2000/01/rdf-schema#> .'))
    print(html.escape('@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .'))
    print('')
    for item in code:
        print(' ;\n'.join(item) + ' .\n\n')
    print('</pre></code>')


def main():
    """First argument should be the name of the Tab in the spreadsheet you want to parse (in quotes), e.g. 'Base Ontology'
    """
    data = download_data(SHEET)
    classes, properties = extract_classes_properties(data)

    # generate HTML
    document_toc(classes, properties)
    document_classes(classes, properties)
    document_properties(classes, properties)
    generate_rdf(classes, properties)

            
if __name__ == '__main__':
    if(len(sys.argv) < 1):
        exit('ERROR: no ontology to parse provided')
    else:
        SHEET = sys.argv[1]
    main()
