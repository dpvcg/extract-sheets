from __future__ import print_function
import pickle
import os.path
import sys, getopt
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']

# The ID and range of a sample spreadsheet.
MYSHEET = '13d1eRXZZBCw84vYGoCJeMU08rzkkzadDzxY3n2iOi8k'
MYTAB = 'Base_Ontology'

def main(argv):
    """First argument should be the name of the Tab in the spreadsheet you want to parse (in quotes), e.g. 'Base Ontology'
    """
    if(len(argv) < 1):
        exit('ERROR: no ontology to parse provided')
    else:
        MYTAB = argv[0]
        # print(MYTAB)
        MYRANGE = MYTAB+'!A:Q'
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

    service = build('sheets', 'v4', credentials=creds)

    # Call the Sheets API
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=MYSHEET,
                                range=MYRANGE).execute()
    values = result.get('values', [])

    classes = []
    properties = []
    
    if not values:
        print('No data found.')
    else:
        for row in values:
            if(len(row)):
                if(row[0]=='Class'):
                    # print('Class: '+str(row))
                    classes.append(row)

                    
                if(row[0]=='Property'):
                    # print('Property: '+str(row))
                    properties.append(row)

        print('<h4>Classes</h4>')
        print('<table border="1"><tr><th>Classes:</th></tr>')
        for i in (list(zip(*classes))[1]):
            print('<tr><td><a href="#'+str(i)+'">'+str(i)+'</a></td></tr>')
        print("</table>")

        print('<h4>Properties</h4>')
        print('<table border="1"><tr><th>Properties:</th></tr>')
        for i in (list(zip(*properties))[1]):
            print('<tr><td><a href="#'+str(i)+'">'+str(i)+'</a></td></tr>')
        print("</table>")


        for i in classes:
            print('<h4>Class: <a id="'+i[1]+'">'+i[1]+'<a></h4>')

            print('<div>')
            print(i[2])
            print('</div>')
            print('<ul>')
            print('<li> <b>Status</b>: '+str(i[12])+' (')
            if(len(i)>11 and i[11]):
                print('created: '+ str(i[11]))
            if(len(i)>15 and i[15]):
                print('approved: '+ str(i[15]))
            if(len(i)>14 and i[14]):
                print('proposed by: '+ str(i[14]))
            print(')</li>')
            if(i[5]):
                print('<li> <b>Superclasses</b>: ')
                scs = i[5].split(',')
                for sc in scs:
                    print('<a id="'+sc+'">'+sc+'<a>')
                print('</li>')
                print('<br/>')

            props=""
            for j in properties:
               if (i[1] in j[3]):
                   props += ('<a href="#'+str(j[1])+'">'+str(j[1])+'</a>')
            if len(props):
                print('<li> <b>Properties</b>: ')
                print(props)
                print('</li>')
            print('<li> <b>Used with</b>: ')            
            for j in properties:
               if (i[1] in j[4]):
                   print('<a href="#'+str(j[1])+'">'+str(j[1])+'</a>')
            print('</li>')
            print('</ul>')

        for i in properties:
            print('<h4>Property: <a id="'+i[1]+'">'+i[1]+'<a></h4>')

            print('<div>')
            print(i[2])
            print('</div>')
            print('<ul>')
            print('<li> <b>Status</b>: '+str(i[12])+' (')
            if(len(i)>11 and i[11]):
                print('created: '+ str(i[11]))
            if(len(i)>15 and i[15]):
                print('approved: '+ str(i[15]))
            if(len(i)>14 and i[14]):
                print('proposed by: '+ str(i[14]))
            print(')</li>')
            if(i[5]):
                print('<li> <b>Superproperties</b>: ')
                sps = i[5].split(',')
                for sp in sps:
                    print('<a id="'+sp+'">'+sp+'<a>')
                print('</li>')
                print('<br/>')

            print('<li> <b>Domain</b>: '+i[3])            
            print('</li>')
            print('<li> <b>Range</b>: '+i[4])            
            print('</li>')
            print('</ul>')

        for c in classes:
            print('<code>')
            print(c[1]+' a rdfs:Class ; dct:description "'+ c[2] + '" .')
            print('<br/>')
            if(c[5]):
                print(c[1]+' rdfs:subClassOf "'+ c[5] + '" .')
                print('<br/>')
            if(len(c)>11 and c[11]):
                print(c[1]+' dct:created "'+ c[11] + '"^^xsd:date .')
            if(len(c)>15 and c[15]):
                print(c[1]+' dct:date-accepted "'+ c[15] + '"^^xsd:date .')
            if(len(c)>14 and c[14]):
                print(c[1]+' dct:creator "'+ c[14] + '" .')

            print('</code><br/>')
            
        for c in properties:
            print('<code>')
            print(c[1]+' a rdfs:Property ; dct:description "'+ c[2] + '" .')
            print('<br/>')
            print(c[1]+' rdfs:domain ' + c[3] + ' .')
            print('<br/>')
            print(c[1]+' rdfs:range ' + c[4] + ' .')
            print('<br/>')
            print('</code><br/>')


            
            
if __name__ == '__main__':
    main(sys.argv[1:])
