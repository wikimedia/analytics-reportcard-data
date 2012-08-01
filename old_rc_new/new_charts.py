'''
Creates dygrap csv files for new metrics
'''
import os
try:
	from collections import OrderedDict
except:
	from ordereddict import OrderedDict

import parse_csv as p

def mobile_page_requests():

	dygraph_fn='rc_page_requests_mobile'
	metric="=== Page view totals mobile ==="
	next_metric="=== Page view totals per project - non-mobile + mobile ==="

	startindex=47
	endindex=-1
	key_index=23
	n_lines=8

	data = p.parse_PageViews(metric,next_metric,startindex=startindex,endindex=endindex,key_index=key_index,n_lines=n_lines)

	# Gett the mobile total
	metric="=== Page view totals per project - mobile ==="
	next_metric="end of file"

	startindex=32
	endindex=-1
	key_index=8
	n_lines=3

	totaldata = p.parse_PageViews(metric,next_metric,startindex=startindex,endindex=endindex,key_index=key_index,n_lines=n_lines)

	
	copydata = OrderedDict()

	copydata['project'] = data['project']
	#copydata['All projects'] = totaldata['All projects']
	copydata['Total'] = totaldata['Total']
	for k in data.keys()[1:]:
		copydata[k] = data[k]

	p.write_dygraph_file(copydata,dygraph_fn)



def create_all():

	mobile_page_requests()
