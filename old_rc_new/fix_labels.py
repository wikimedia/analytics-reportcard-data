#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys, json, yaml
from path import path
from bunch import *

GRAPH_NAMES = ('active_editors.json', 'active_editors_target.json', 'articles.json', 'articles_per_day.json', 'commons.json', 'edits.json', 'new_editors.json', 'pageviews.json', 'pageviews_mobile.json', 'pageviews_mobile_target.json', 'very_active_editors.json',)



sources = dict( (s.id, s) for s in [ bunchify(yaml.load( f.open('rU') )) for f in path('datasources').glob('*.yaml') ] )
graphs = [ bunchify(json.load( (path('graphs')/name).open('rU') )) for name in GRAPH_NAMES ]

for g in graphs:
    try:
        print "graph: %s" % g.id
        metrics = g.data.metrics
        source = sources[ metrics[0].source_id ]
        for i, label in enumerate(source.columns.labels[1:]):
            # if metrics[i].label == label: continue
            old = metrics[i].label
            print "  %s %s -> %s" % ('*' if old != label else ' ', old, label)
            metrics[i].label = label
        sys.stdout.write( "Writing graphs/%s.json ..." % g.id )
        json.dump( g.toDict(), path('graphs/%s.json' % g.id).open('w') )
        print 'ok!\n'
    except Exception as ex:
        raise
        print ex
        print

