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
    'time': 'http://www.w3.org/2006/time#',
    'odrl': 'http://w3.org/ns/odrl/2/',
    'spl': 'http://www.specialprivacy.eu/langs/usage-policy#',
    'svd': 'http://www.specialprivacy.eu/vocabs/data#',
    'svpu': 'http://www.specialprivacy.eu/vocabs/purposes#',
    'svpr': 'http://www.specialprivacy.eu/vocabs/processing#',
    'svr': 'http://www.specialprivacy.eu/vocabs/recipients#',
    'svl': 'http://www.specialprivacy.eu/vocabs/locations#',
    'svdu': 'http://www.specialprivacy.eu/vocabs/duration#',
    'dpv': 'http://w3.org/ns/dpv#',
    'dpv-gdpr': 'http://w3.org/ns/dpv-gdpr#',
}


def validate_rdf(vocab):
    """Validate file. will throw errors."""
    g = Graph()
    # g.namespace_manager = namespace_manager
    g.parse(f'./docs/rdf/{vocab}.ttl', format='ttl')
    g.serialize(f'./docs/rdf/{vocab}.ttl', format='ttl')


def detect_prefixes(code):
    prefixes = set()
    keys = [(p, p + ':') for p in PREFIXES.keys()]
    for item in code:
        for line in item:
            for prefix, notation in keys:
                if notation in line:
                    prefixes.add(prefix)
    return prefixes


def serialize_rdf(name, code):
    prefixes = detect_prefixes(code)
    with open(f'./docs/rdf/{name}.ttl', 'w') as fd:
        for prefix in prefixes:
            fd.write(f"@prefix {prefix}: <{PREFIXES[prefix]}> .")
            fd.write('\n')
        fd.write('\n')
        for item in code:
            fd.write(' ;\n'.join(item) + ' .\n\n')
    validate_rdf(name)


def combine_graphs(vocabs=VOCABS):
    g = Graph()
    vocabs.remove('LegalBasis')
    for vocab in vocabs:
        g.parse(f'./docs/rdf/{vocab}.ttl', format='ttl')
    g.serialize(f'./docs/rdf/dpv.ttl', format='ttl')


if __name__ == '__main__':
    combine_graphs()