#!/usr/bin/env python

import xml.sax, xapian, json, helpers

class DoxygenHandler (xml.sax.handler.ContentHandler):

    def __init__(self, directory):
        import os

        path = os.path.join(directory, helpers.index_path)
        action = xapian.DB_CREATE_OR_OVERWRITE

        self.database = xapian.WritableDatabase(path, action)
        self.document = None
        self.generator = None

        self.entity = {}
        self.field = ''
        self.content = ''


    def start_element(self, name, attributes):
        if name == 'doc':
            self.start_doc(name, attributes)
        if name == 'field':
            self.start_field(name, attributes)

    startElement = start_element

    def start_doc(self, name, attributes):
        self.document = xapian.Document()
        self.generator = xapian.TermGenerator()

        self.generator.set_document(self.document)
        self.generator.set_stemmer(xapian.Stem('en'))

    def start_field(self, name, attributes):
        self.field = attributes.get('name')


    def end_element(self, name):
        if name == 'doc':
            self.end_doc(name)
        if name == 'field':
            self.end_field(name)

    endElement = end_element

    def end_field(self, name):
        self.entity[self.field] = self.clean_up_content()
        self.content = ""

    def end_doc(self, name):
        type = self.entity['type']
        prefix = helpers.abbreviations[type]

        name = self.entity['name']
        keywords = self.entity['keywords']
        text = self.entity['text']

        self.generator.index_text(name, 100, prefix)
        self.generator.index_text(keywords, 100, prefix)

        self.generator.index_text(name, 100)
        self.generator.increase_termpos()
        self.generator.index_text(keywords, 100)
        self.generator.increase_termpos()
        self.generator.index_text(text)

        data = {'type': self.entity['type'],
                'name': self.entity['name'],
                'tag': self.entity['tag'],
                'url': self.entity['url'],
                'fragments': ''}
                
        json_data = json.dumps(data)

        self.document.add_value(helpers.sort_index, prefix)
        self.document.set_data(json_data)

        self.database.add_document(self.document)


    def characters(self, content):
        self.content += content

    def clean_up_content(self):
        self.content = self.content.strip()
        self.content = xml.sax.saxutils.unescape(self.content)
        return self.content


if __name__ == '__main__':

    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('--output', '-o', default='.')
    parser.add_argument('search_data', nargs='+')
    arguments = parser.parse_args()

    handler = DoxygenHandler(arguments.output)

    for input in arguments.search_data:
        print "Processing %s..." % input
        xml.sax.parse(input, handler)
