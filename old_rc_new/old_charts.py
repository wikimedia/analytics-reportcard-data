'''
Creates dygrap csv files for all metrics in the old report card
'''
try:
	from collections import OrderedDict
except ImportError:
	from ordereddict import OrderedDict

import parse_csv as p


# 	
# From monthly stat file
# 

def binary_files():

	dygraph_fn='rc_binary_files'
	metric="Binaries per month - Absolute"
	next_metric="Binaries per month - Indexed"

	n_lines = 20

	data = p.parse_StatisticsMonthly(metric,next_metric)

	# write dygraph file
	p.write_dygraph_file(data,dygraph_fn)


def article_count():

	dygraph_fn='rc_article_count'
	metric="Article count (official) - Absolute - Per Wiki"
	next_metric="Article count (official) - Absolute - Per Project"

	n_lines = 9

	data = p.parse_StatisticsMonthly(metric,next_metric,n_lines=n_lines)

	# write dygraph file
	p.write_dygraph_file(data,dygraph_fn)


def new_article_count():

	dygraph_fn='rc_new_article_count'
	metric="New articles per day - Absolute - Per Wiki"
	next_metric="New articles per day - Absolute - Per Project"

	n_lines = 25

	data = p.parse_StatisticsMonthly(metric,next_metric,n_lines=n_lines)

	# write dygraph file
	p.write_dygraph_file(data,dygraph_fn)


def edit_counts():
	dygraph_fn='rc_edits_count'
	metric="Edits per month - Absolute - Per Wiki"
	next_metric="Edits per month - Absolute - Per Project"

	n_lines = 25

	data = p.parse_StatisticsMonthly(metric,next_metric,n_lines=n_lines)

	# write dygraph file
	p.write_dygraph_file(data,dygraph_fn)


def new_editors_count():
	dygraph_fn='rc_new_editors_count'
	metric="New editors - Absolute - Per Wiki"
	next_metric="New editors - Absolute - Per Project"

	n_lines = 10

	data = p.parse_StatisticsMonthly(metric,next_metric,n_lines=n_lines)

	# write dygraph file
	p.write_dygraph_file(data,dygraph_fn)


def active_editors():
	dygraph_fn='rc_active_editors_count'
	metric="Active editors - Absolute - Per Wiki"
	next_metric="Active editors - Absolute - Per Project"

	# n_lines = 10 # only old report card entries
	n_lines = 25 # all countries so graph can be edited using the dataset-ui

	data = p.parse_StatisticsMonthly(metric,next_metric,n_lines=n_lines)

	# Update 05/01/12: not necessary anymore
	# hack hack, the total editors in that section is incorrect as of now as it should inlcude 'commons'. 
	# hackdata = p.parse_StatisticsMonthly(metric='Active editors - Absolute - Per Project',next_metric='Whatever....we only want 3 lines',n_lines=3)

	# # replace 'All projects'
	# data['Total'] = hackdata['All projects']

	# write dygraph file
	p.write_dygraph_file(data,dygraph_fn)

def very_active_editors():
	dygraph_fn='rc_very_active_editors_count'
	metric="Very active editors - Absolute - Per Wiki"
	next_metric="Very active editors - Absolute - Per Project"

	# n_lines = 10 # only old report card entries
	n_lines = 25 # all countries so graph can be edited using the dataset-ui

	data = p.parse_StatisticsMonthly(metric,next_metric,n_lines=n_lines)

	# Update 05/01/12: not necessary anymore
	# hack hack, the total editors in that section is incorrect as of now as it should inlcude 'commons'. 
	# hackdata = p.parse_StatisticsMonthly(metric='Very active editors - Absolute - Per Project',next_metric='Whatever....we only want 3 lines',n_lines=3)
	# replace 'All projects'
	# data['Total'] = hackdata['All projects']

	# write dygraph file
	p.write_dygraph_file(data,dygraph_fn)


def new_editors_absolute_per_project():
	dygraph_fn = 'rc_new_editors_count_project'
	metric = 'New editors - Absolute - Per Project'
	next_metric = 'New editors - Indexed - Per Wiki'
	n_lines = 12 # wikivoyage is 11
	data = p.parse_StatisticsMonthly(metric,next_metric,n_lines)
	p.write_dygraph_file(data,dygraph_fn)
	
	
def active_editors_absolute_per_project():
	dygraph_fn = 'rc_active_editors_count_project'
	metric = 'Active editors - Absolute - Per Project'
	next_metric = 'Active editors - Indexed - Per Wiki'
	n_lines = 12 # wikivoyage is 12
	data = p.parse_StatisticsMonthly(metric,next_metric,n_lines)
	p.write_dygraph_file(data,dygraph_fn)
	
	
def very_active_editors_absolute_per_project():
	dygraph_fn = 'rc_very_active_editors_count_project'
	metric = 'Very active editors - Absolute - Per Project'
	next_metric = 'Very active editors - Indexed - Per Wiki'
	n_lines = 12 # wikivoyage is 10
	data = p.parse_StatisticsMonthly(metric,next_metric,n_lines)
	p.write_dygraph_file(data,dygraph_fn)


# # 
# # From page view file
# # 

def page_requests():
	dygraph_fn='rc_page_requests'

	startindex=9
	endindex=-1
	n_items=8
	
	data = p.parse_PageViews(metric="Page view totals non-mobile + mobile",next_metric="=== Page view totals non-mobile ===",startindex=startindex,endindex=endindex)
	
	# hack hack, all projects is in different section
	hackdata = p.parse_PageViews(metric='=== Page view totals per project - non-mobile + mobile ===',next_metric='Whatever....',startindex=startindex,endindex=endindex)
	
	# construct a copy and rearrange the needed data
	copy_data = OrderedDict()
	
	copy_data['project'] = data['project']
	
	# add 'All projects' or 'Total' depending on what the input file wants
	if 'All projects' in hackdata:
		copy_data['Total'] = hackdata['All projects']
	else:
		copy_data['Total'] = hackdata['Total']
	copy_data['All projects'] = copy_data['Total']
	
	n_collected = 1
	for k,v in data.items()[1:]:
		if k != 'All projects':
			copy_data[k] = v
			n_collected += 1
			if n_collected==n_items:
				break
	
	p.write_dygraph_file(copy_data,dygraph_fn)



# dygraph_fn='rc_page_requests_mobile'
# metric="=== Page view totals mobile ==="
# next_metric="=== Page view totals per project - non-mobile + mobile ==="

# startindex=47
# endindex=-1
# key_index=23

# parse_rc_PageViews_csv(metric,next_metric,dygraph_fn,startindex=startindex,endindex=endindex,key_index=key_index)


def create_all():

	binary_files()
	article_count()
	new_article_count()
	edit_counts()
	new_editors_count()
	active_editors()
	very_active_editors()
	
	# added for Wikivoyage on 2012-12-05
	new_editors_absolute_per_project()
	active_editors_absolute_per_project()
	very_active_editors_absolute_per_project()
	
	page_requests()
