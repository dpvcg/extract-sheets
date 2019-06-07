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

from rdf_serializer import serialize_rdf

# NOTE: there is a main() function, start reading from there
# There are times when it seems like a very bad imitation of PHP
# Ideally, I would have used templates (Jinja2) to write the data
# But given time constraints, I saved the lines to a list
# and then write them at the end to a file (persist)

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

filecontent = []


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
    # print(f'<dt><a href="rdf/{SHEET}.ttl">rdf/turtle serialization</a></dt>')
    pass


def document_classes(classes, properties):
    """Generate documentation for classes"""
    filecontent.append(f'<section id="{SHEET.lower()}-classes">')
    filecontent.append('<h3>Classes</h3>')
    if not classes:
        return
    classes.sort(key=lambda c: c.term)
    string = "<p>\n"
    string += ' | \n'.join((
        f'<code><a href="{item.term}">:{item.term.split(":")[1]}</a></code>'
        for item in classes))
    string += "\n</p>\n"
    filecontent.append(string)
    for cl in classes:
        term = cl.term.split(':')[1]
        termbank = []
        label = term[0]
        for i in range(1, len(term)):
            if term[i].isupper() and term[i-1].islower():
                termbank.append(label)
                label = ''
            label += term[i]
        termbank.append(label)
        label = ' '.join(termbank)

        filecontent.append('<section>')
        filecontent.append(f'<h4 id={cl.term}>{label}</h4>')
        filecontent.append('<table class="definition">')
        filecontent.append('<tbody>')
        filecontent.append('<tr>')
        filecontent.append('<th>Class:</th>')
        filecontent.append(f'<th><code><a href="#{cl.term}">{cl.term}</a></code></th>')
        filecontent.append('</tr>')
        filecontent.append('<tr>')
        filecontent.append('<td>Description:</td>')
        filecontent.append(f'<td>{cl.description}</td>')
        filecontent.append('</tr>')
        if cl.rdfs_comments:
            filecontent.append('<tr>')
            filecontent.append('<td>Comments:</td>')
            filecontent.append(f'<td>{cl.rdfs_comments}</td>')
            filecontent.append('</tr>')
        filecontent.append('<tr>')
        if cl.super:
            filecontent.append('<tr>')
            filecontent.append('<td>is SubClass of:</td>')
            scs = [f'<a href="#{sc}">{sc}</a>' for sc in cl.super.split(',')]
            scs = ' &cap; '.join(scs)
            filecontent.append(f'<td>{scs}</td>')
            filecontent.append('</tr>')
        if cl.sub:
            filecontent.append('<tr>')
            filecontent.append('<td>is Parent Class of:</td>')
            scs = [f'<a href="#{sc}">{sc}<a>' for sc in cl.sub.split(',')]
            scs = ', '.join(scs)
            filecontent.append(f'<td>{scs}</td>')
            filecontent.append('</tr>')
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
                domains.sort()
                filecontent.append('<tr>')
                filecontent.append('<td>in Domain of:</td>')
                filecontent.append(f'<td>{", ".join(domains)}</td>')
                filecontent.append('</tr>')
            if ranges:
                ranges.sort()
                filecontent.append('<tr>')
                filecontent.append('<td>in Range of:</td>')
                filecontent.append(f'<td>{", ".join(ranges)}</td>')
                filecontent.append('</tr>')
        if cl.source:
            filecontent.append('<tr>')
            filecontent.append('<td>Source:</td>')
            s = ', '.join((
                f'<a href="{s}">{s}</a>'
                for s in cl.source.split(',')))
            filecontent.append(f'<td>{s}</td>')
            filecontent.append('</tr>')
        if cl.status:
            filecontent.append('<tr>')
            filecontent.append('<td>Status:</td>')
            st = "\n".join(cl.status.split(";"))
            filecontent.append(f'<td>{st}</td>')
            filecontent.append('</tr>')
        if cl.created:
            filecontent.append('<tr>')
            filecontent.append('<td>Date Created:</td>')
            filecontent.append(f'<td>{cl.created}</td>')
            filecontent.append('</tr>')
        if cl.approved:
            filecontent.append('<tr>')
            filecontent.append('<td>Date Approved:</td>')
            filecontent.append(f'<td>{cl.approved}</td>')
            filecontent.append('</tr>')
        if cl.resolution:
            filecontent.append('<tr>')
            filecontent.append('<td>Approval Resolution:</td>')
            filecontent.append(f'<td><a href="{cl.resolution}">{cl.resolution}</a></td>')
            filecontent.append('</tr>')
        if cl.contributor:
            filecontent.append('<tr>')
            filecontent.append('<td>Contributor:</td>')
            filecontent.append(f'<td>{cl.contributor}</td>')
            filecontent.append('</tr>')
        if cl.comments:
            filecontent.append('<tr>')
            filecontent.append('<td>Notes:</td>')
            filecontent.append(f'<td>{cl.comments}</td>')
            filecontent.append('</tr>')
        if cl.related_terms:
            filecontent.append('<tr>')
            filecontent.append('<td>Related Terms:</td>')
            filecontent.append('<td>')
            for t in cl.related_terms.split(','):
                filecontent.append(f'{cl.related_how} {t}\n')
            filecontent.append('</td></tr>')
        filecontent.append('</tbody>')
        filecontent.append('</thead>')
        filecontent.append('</table>')
        filecontent.append('</section>')
    filecontent.append('</section>')

def document_properties(classes, properties):
    """Generate documentation for properties"""
    if not properties:
        return
    filecontent.append(f'<section id="{SHEET.lower()}-properties">')
    filecontent.append('<h3>Properties</h3>')
    properties.sort(key=lambda c: c.term)
    string = "<p>\n"
    string += ' | \n'.join((
        f'<code><a href="{item.term}">:{item.term.split(":")[1]}</a></code>'
        for item in properties))
    string += "\n</p>\n"
    filecontent.append(string)
    for cl in properties:
        term = cl.term.split(':')[1]
        termbank = []
        label = term[0]
        for i in range(1, len(term)):
            if term[i].isupper() and term[i-1].islower():
                termbank.append(label)
                label = ''
            label += term[i]
        termbank.append(label)
        label = ' '.join(termbank)

        filecontent.append('<section>')
        filecontent.append(f'<h4 id={cl.term}>{label}</h4>')
        filecontent.append('<table class="definition">')
        filecontent.append('<tbody>')
        filecontent.append('<tr>')
        filecontent.append('<th>Property:</th>')
        filecontent.append(f'<th><code><a href="#{cl.term}">{cl.term}</a></code></th>')
        filecontent.append('</tr>')
        filecontent.append('<tr>')
        filecontent.append('<td>Description:</td>')
        filecontent.append(f'<td>{cl.description}</td>')
        filecontent.append('</tr>')
        if cl.rdfs_comments:
            filecontent.append('<tr>')
            filecontent.append('<td>Comments:</td>')
            filecontent.append(f'<td>{cl.rdfs_comments}</td>')
            filecontent.append('</tr>')
        filecontent.append('<tr>')
        if cl.super:
            filecontent.append('<tr>')
            filecontent.append('<td>is Sub-Property of:</td>')
            scs = [f'<a href="#{sc}">{sc}<a>' for sc in cl.super.split(',')]
            scs = ', '.join(scs)
            filecontent.append(f'<td>{scs}</td>')
            filecontent.append('</tr>')
        if cl.sub:
            filecontent.append('<tr>')
            filecontent.append('<td>is Parent Property of:</td>')
            scs = [f'<a href="#{sc}">{sc}<a>' for sc in cl.sub.split(',')]
            scs = ', '.join(scs)
            filecontent.append(f'<td>{scs}</td>')
            filecontent.append('</tr>')
        if cl.domain:
            if 'union' in cl.domain:
                domains = [
                    f'<a href="{c.strip()}">{c.strip()}</a>'
                    for c in cl.domain.split('union')]
                domains = ' &cup; '.join(domains)
            else:
                domains = f'<a href="{cl.domain}">{cl.domain}</a>'
            filecontent.append('<tr>')
            filecontent.append('<td>Domain:</td>')
            filecontent.append(f'<td>{domains}</td>')
            filecontent.append('</tr>')
        if cl.range:
            filecontent.append('<tr>')
            filecontent.append('<td>Range:</td>')
            filecontent.append(f'<td><a href="{cl.range}">{cl.range}</a></td>')
            filecontent.append('</tr>')
        if cl.source:
            filecontent.append('<tr>')
            filecontent.append('<td>Source:</td>')
            s = ', '.join((
                f'<a href="{s}">{s}</a>'
                for s in cl.source.split(',')))
            filecontent.append(f'<td>{s}</td>')
            filecontent.append('</tr>')
        if cl.status:
            filecontent.append('<tr>')
            filecontent.append('<td>Status:</td>')
            st = "\n".join(cl.status.split(";"))
            filecontent.append(f'<td>{st}</td>')
            filecontent.append('</tr>')
        if cl.created:
            filecontent.append('<tr>')
            filecontent.append('<td>Date Created:</td>')
            filecontent.append(f'<td>{cl.created}</td>')
            filecontent.append('</tr>')
        if cl.approved:
            filecontent.append('<tr>')
            filecontent.append('<td>Date Approved:</td>')
            filecontent.append(f'<td>{cl.approved}</td>')
            filecontent.append('</tr>')
        if cl.resolution:
            filecontent.append('<tr>')
            filecontent.append('<td>Approval Resolution:</td>')
            filecontent.append(f'<td><a href="{cl.resolution}">{cl.resolution}</a></td>')
            filecontent.append('</tr>')
        if cl.contributor:
            filecontent.append('<tr>')
            filecontent.append('<td>Contributor:</td>')
            filecontent.append(f'<td>{cl.contributor}</td>')
            filecontent.append('</tr>')
        if cl.comments:
            filecontent.append('<tr>')
            filecontent.append('<td>Notes:</td>')
            filecontent.append(f'<td>{cl.comments}</td>')
            filecontent.append('</tr>')
        if cl.related_terms:
            filecontent.append('<tr>')
            filecontent.append('<td>Related Terms:</td>')
            filecontent.append('<td>')
            for t in cl.related_terms.split(','):
                filecontent.append(f'{cl.related_how} {t}\n')
            filecontent.append('</td></tr>')
        filecontent.append('</tbody>')
        filecontent.append('</thead>')
        filecontent.append('</table>')
        filecontent.append('</section>')
    filecontent.append('</section>')


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
        if cl.rdfs_comments:
            rdfs_comments = cl.rdfs_comments.replace('"', '\\"')
            serialization.append(f'    rdfs:comment "{rdfs_comments}"')
        if cl.source:
            for s in cl.source.split(','):
                if s.startswith('http'):
                    serialization.append(f'    rdfs:isDefinedBy <{s}>')
                else:
                    serialization.append(f'    rdfs:isDefinedBy "s"')
        if cl.related_terms:
            if not cl.related_how:
                related_how = 'rdfs:seeAlso'
            else:
                related_how = cl.related_how
            for t in cl.related_terms.split(','):
                serialization.append(f'    {related_how} {t}')
        if cl.status:
            serialization.append(f'    sw:term_status "{cl.status}"')
        code.append(serialization)
        
    for prop in properties:
        serialization = []
        serialization.append(f'{prop.term} a rdfs:Property')
        serialization.append(f'    dct:description "{prop.description}"@en')
        if prop.domain:
            if 'union' in prop.domain:
                domains = prop.domain.split(' union ')
                s = f'    rdfs:domain [ owl:unionOf (\n'
                for item in domains:
                    s += f'        {item}\n'
                s += f'        ) ]'
                serialization.append(s)
            else:
                serialization.append(f'    rdfs:domain {prop.domain}')
        if prop.range:
            if 'union' in prop.range:
                ranges = prop.range.split(' union ')
                s = f'    rdfs:range [ owl:unionOf (\n'
                for item in ranges:
                    s += f'        {item}\n'
                s += f'        ) ]'
                serialization.append(s)
            else:
                serialization.append(f'    rdfs:range {prop.range}')
        # TODO: add superproperty
        if prop.created:
            serialization.append(f'    dct:created "{prop.created}"^^xsd:date')
        if prop.approved:
            serialization.append(f'    dct:date-accepted "{prop.approved}"^^xsd:date')
        if prop.contributor:
            serialization.append(f'    dct:creator "{prop.contributor}"')
        if prop.rdfs_comments:
            rdfs_comments = prop.rdfs_comments.replace('"', '\\"')
            serialization.append(f'    rdfs:comment "{rdfs_comments}"')
        if prop.source:
            for s in prop.source.split(','):
                if s.startswith('http'):
                    serialization.append(f'    rdfs:isDefinedBy <{s}>')
                else:
                    serialization.append(f'    rdfs:isDefinedBy "s"')
        if prop.related_terms:
            if not prop.related_how:
                related_how = 'rdfs:seeAlso'
            else:
                related_how = prop.related_how
            for t in prop.related_terms.split(','):
                serialization.append(f'    {related_how} {t}')
        if prop.status:
            serialization.append(f'    sw:term_status "{prop.status}"')
        code.append(serialization)

    return code


def main(pickled=False):
    """First argument should be the name of the Tab in the spreadsheet
    you want to parse (in quotes), e.g. 'Base Ontology'"""
    if pickled:
        print(f'loading data from file pickled/{SHEET}.')
        classes, properties = pickle.load(open(f'pickled/{SHEET}.pickle', 'rb'))
    else:
        # download data from Google Sheets using the API
        data = download_data(SHEET)
        # extract classes and properties from downloaded data
        classes, properties = extract_classes_properties(data)
        # pickles for offline working (in case SHEETS API is not working)
        # or when there's no internet connectivity - e.g. flights
        pickle.dump(
            (classes, properties),
            open(f'pickled/{SHEET}.pickle', 'wb'))

    # the contents are generated, stored in a list, and saved to a file
    document_classes(classes, properties)
    document_properties(classes, properties)
    with open(f'docs/{SHEET}.html', 'w') as fd:
        for line in filecontent:
            print(line, file=fd)
    # serialize the classes and properties in a RDF file
    rdf = generate_rdf(classes, properties)
    serialize_rdf(SHEET, rdf)

            
if __name__ == '__main__':
    if(len(sys.argv) < 1):
        exit('ERROR: no ontology to parse provided')
    else:
        SHEET = sys.argv[1]
    # parameter 2 controls whether to use pickled data as cache
    # if set, will load the data from the pickled files
    # and will not download data from spreadsheet
    pickled = False
    if(len(sys.argv) > 2):
        if sys.argv[2] == "--cache":
            pickled = True
    main(pickled)
