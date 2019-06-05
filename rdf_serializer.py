"""serialize metadata from sheets into RDF files."""
import pickle

from rdflib import Graph
from rdflib.namespace import Namespace, NamespaceManager
from rdflib.namespace import DCTERMS

DPV = Namespace('http://w3.org/ns/dpv#')
ODRL = Namespace('http://w3.org/ns/odrl/2/')
SPL = Namespace('http://www.specialprivacy.eu/langs/usage-policy#')
SVD = Namespace('http://www.specialprivacy.eu/vocabs/data#')
SVPU = Namespace('http://www.specialprivacy.eu/vocabs/purposes#')
SVPR = Namespace('http://www.specialprivacy.eu/vocabs/processing#')
SVR = Namespace('http://www.specialprivacy.eu/vocabs/recipients#')
SVL = Namespace('http://www.specialprivacy.eu/vocabs/locations#')
SVDU = Namespace('http://www.specialprivacy.eu/vocabs/duration#')
DPVGDPR = Namespace('http://www.w3.org/ns/dpv-gdpr#')
DCT = DCTERMS

VOCABS = [
    "BaseOntology",
    "TechnicalOrganisationalMeasure",
    "PersonalDataCategory",
    "Processing",
    "Purpose",
    "RecipientsDataControllersDataSubjects",
    "LegalBasis",
    "Consent",
]

PREFIXES = {
    'rdf': 'http://www.w3.org/1999/02/22-rdf-syntax-ns#',
    'rdfs': 'http://www.w3.org/2000/01/rdf-schema#',
    'xsd': 'http://www.w3.org/2001/XMLSchema#',
    'owl': 'http://www.w3.org/2002/07/owl#',
    'dct': 'http://purl.org/dc/terms/',
    'dc': 'http://purl.org/dc/elements/1.1/',
    'dpv': 'http://w3.org/ns/dpv#',
    'dpv-gdpr': 'http://w3.org/ns/dpv-gdpr#',
    'time': 'http://www.w3.org/2006/time#',
    'odrl': 'http://w3.org/ns/odrl/2/',
    'spl': 'http://www.specialprivacy.eu/langs/usage-policy#',
    'svd': 'http://www.specialprivacy.eu/vocabs/data#'',
    'svpu': 'http://www.specialprivacy.eu/vocabs/purposes#',
    'svpr': 'http://www.specialprivacy.eu/vocabs/processing#',
    'svr': 'http://www.specialprivacy.eu/vocabs/recipients#',
    'svl': 'http://www.specialprivacy.eu/vocabs/locations#',
    'svdu': 'http://www.specialprivacy.eu/vocabs/duration#',
}


def validate_rdf(vocab):
    """Validate file. will throw errors."""
    g = Graph()
    # g.namespace_manager = namespace_manager
    g.parse(f'./rdf/{vocab}.ttl', format='ttl')
    g.serialize(f'./rdf/{vocab}.ttl', format='ttl')


def serialize_rdf(name, code):

    with open(f'./rdf/{SHEET}.ttl', 'w') as fd:
        for prefix in prefixes:
            fd.write(prefix)
            fd.write('\n')
        for item in code:
            fd.write(' ;\n'.join(item) + ' .\n\n')


def combine_graphs(vocabs):
    g = Graph()
    vocabs.remove('LegalBasis')
    for vocab in vocabs:
        g.parse(f'./rdf/{vocab}.ttl', format='ttl')
    g.serialize(f'./rdf/combined.ttl', format='ttl')



if __name__ == '__main__':
    for vocab in VOCABS:
        validate_rdf(vocab)
    combine_graphs(VOCABS)