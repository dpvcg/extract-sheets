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

namespace_manager = NamespaceManager(Graph())
# namespace_manager.bind('dpv', DPV, override=True)
# namespace_manager.bind('odrl', ODRL, override=True)
# namespace_manager.bind('spl', SPL, override=True)
# namespace_manager.bind('svd', SVD, override=True)
# namespace_manager.bind('svpu', SVPU, override=True)
# namespace_manager.bind('svpr', SVPR, override=True)
# namespace_manager.bind('svr', SVR, override=True)
# namespace_manager.bind('svl', SVL, override=True)
# namespace_manager.bind('svdu', SVDU, override=True)
# namespace_manager.bind('dpv-gdpr', DPVGDPR, override=True)
# namespace_manager.bind('dct', DCT, override=True)

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


def validate_rdf(vocab):
    """Validate file. will throw errors."""
    g = Graph()
    # g.namespace_manager = namespace_manager
    g.parse(f'./rdf/{vocab}.ttl', format='ttl')
    g.serialize(f'./rdf/{vocab}.ttl', format='ttl')


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