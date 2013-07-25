#!/usr/bin/python

import os, urlparse, xapian, json, helpers

shortcuts = { # (fold)
        'p': 'Pose',
        'po': 'Pose',
        'pos': 'Pose',

        'm': 'Mover',
        'mo': 'Mover',
        'mov': 'Mover',

        'v': 'xyzVector',
        've': 'xyzVector',
        'vec': 'xyzVector'
}

if __name__ == '__main__':

    try: arguments = os.environ['QUERY_STRING']
    except KeyError: arguments = sys.argv[1]
    arguments = urlparse.parse_qs(arguments)

    raw_query = arguments.get('q', [''])[0]
    results = int(arguments.get('n', [20])[0])
    page = int(arguments.get('p', [1])[0])
    callback = arguments.get('cb', ['dummy'])[0]

    database = xapian.Database(helpers.index_path)

    parser = xapian.QueryParser()
    parser.set_stemmer(xapian.Stem("en"))
    parser.set_stemming_strategy(parser.STEM_SOME)

    for name, prefix in helpers.abbreviations.items():
        parser.add_prefix(name, prefix)

    raw_query = shortcuts.get(raw_query, raw_query)
    query = parser.parse_query(raw_query)

    enquire = xapian.Enquire(database)
    enquire.set_query(query)
    enquire.set_sort_by_value_then_relevance(helpers.sort_index, False)

    matches = enquire.get_mset(page * results, results)
    hits = matches.get_matches_estimated()
    first = min(page * results, hits)
    pages = (hits + results - 1) // results if results > 0 else 0

    if first + results > hits:
        results = hits - first

    response = {
            'hits': hits,
            'first': first,
            'count': results,
            'page': page,
            'pages': pages,
            'query': raw_query,
            'items': [] }

    for match in matches:
        item = json.loads(match.document.get_data())
        response['items'].append(item)

    print 'Content-Type:application/javascript;charset=utf-8\r\n'
    print '%s(%s)' % (callback, json.dumps(response))

