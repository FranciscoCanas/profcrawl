import argparse
import json
import os
from Distiller.distiller import Distiller

blacklist = []


def main(args):
    """
    Extracts summary keywords from a collection of scraped prof reviews.
    """
    make_path(args.target)
    docs = create_docs(args.path, args.target)
    extract_stats(docs, args.target)


def create_docs(path, target):
    """
    Creates a set of docs suitable for passing into Distiller from
    the reports at the path.
    Input (showing only relevant items):
    [
        {
            'name': # identifier,
            'url': # contains unique id: ShowRatings.jsp?tid=<id>
            'ratings':
                [
                    {
                        'comment': # blob of text
                    },
                    ...
                ]
        },
        ...
    ]

    Output:
    {
        'metadata': {
                        'base_url': 'The document's source URL (if any)'
                    },
        'documents': [
                    {
                        'id': 'The document's unique identifier (if any)',
                        'body': 'The entire body of the document in a single text blob.',
                    }, ...
                ]
    }
    """

    output = {}
    output['documents'] = []
    output['metadata'] = {}
    output['metadata']['base_url'] = 'http://www.ratemyprofessors.com/ShowRatings.jsp?tid='

    bu = output['metadata']['base_url']

    with open(path) as jfile:
        profs = json.load(jfile)
    jfile.close()

    for prof in profs:
        document = {}
        document['id'] = str(prof['url'].split('=')[1])
        print document['id']
        document['name'] = prof['name']
        document['body'] = ' '.join([rating['comment'] for rating in prof['ratings'] if rating.has_key('comment')])
        output['documents'].append(document)

    output_file = target + '/documents.json'

    with open(output_file, 'w') as docsfile:
        json.dump(output, docsfile)
    docsfile.close()
    return output_file

def extract_stats(documents, target):
    """
    Generates reports based on extracted keywords from the given
    documents, storing them in the folder at target.
    """
    nlp_args = {
        'black_list': ['professor', 'prof', 'class', 'course', 'teacher', 'teaching', 'university', 'school'],
        'normalize': True,
        'stem': True,
        'lemmatize': False,
        'pos_list': ['NN','NNP', 'ADJ'],
        'tfidf_cutoff': 0.002
    }

    d = Distiller(document_file=documents, target_path=target, nlp_args=nlp_args)


def make_path(path):
    """
    Ensures the target path for stat reports is created.
    """
    if not os.path.exists(os.path.dirname(path + '/')):
        os.makedirs(os.path.dirname(path + '/'))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Extract summary keywords from a collection of prof reviews"
                    "created by profcrawl.")
    parser.add_argument("-p", "--path", required=True,
                        help="Path to a prof reviews json created by profcrawl.")
    parser.add_argument("-t", "--target", required=True,
                        help="Path to target folder where reports will be"
                             "stored.")
    args = parser.parse_args()
    main(args)



