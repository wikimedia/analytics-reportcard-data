'''Parses the input csv files in a awkward way.
'''
import os

import old_to_new

from utils import months_dict,fix_dates

from collections import OrderedDict

def parse_StatisticsMonthly(metric,next_metric,startindex=2,endindex=-2,n_lines='all'):
	'''Parses the excel_in_StatisticsMonthly_* file, extracts the `metric` passed as an argument and stores a dygraph csv file'''

	collect = False
	data = OrderedDict()


	if n_lines!='all':
		# account for the time labels
		n_lines+=1
	n_collected = 0

	with open(old_to_new.monthly_stats,'r') as f:

		for i,line in enumerate(f):

			if metric in line:
				print '%s found on line %s'%(metric,i+1)
				collect = True
			elif next_metric in line:
				collect = False

			elif collect:
				# linebreaks are '\r\n'
				vals = line[:-2].split(',')
				# filter the empty lines
				if len(vals) > 2:

					k = vals[1]
					if k != '':

						data[k] = vals[startindex:endindex]

						# print len(data[vals[1]])
						n_collected +=1
						if n_collected == n_lines:
							collect = False

	# reformat the time labels 
	data['project'] = fix_dates(data['project'],format='MM/YYYY')

	return data



def parse_PageViews(metric,next_metric,key_index=8,startindex=8,endindex=-1,n_lines='all',addTotal=False):
	'''Parses the excel_in_PageViewsPerMonthPopularWikisNormalized_* file, extracts the `metric` passed as an argument and stores a dygraph csv file.'''

	collect = False
	data = OrderedDict()
	
	n_collected = 0

	with open(old_to_new.page_views,'r') as f:

		for i,line in enumerate(f):

			if metric in line:
				print '%s found on line %s'%(metric,i+1)
				collect = True
			elif next_metric in line:
				collect = False

			if collect:
				# linebreaks are '\r\n'
				vals = line[:-1].split(',')
				# filter the empty lines
				if len(vals) > 2:				

					# print vals[startindex:endindex]
					k = vals[key_index]					
					
					if k not in data:

						if k == 'project':
							data[k] = vals[startindex:]	
						elif k != '':
							data[k] = vals[startindex:endindex]

						n_collected +=1
						if n_collected == n_lines:
							collect = False

	# for d,dd in data.items():
	# 	print d,dd

	# reformat the time labels 
	data['project'] = fix_dates(data['project'],format='MM/YYYY')

	return data

def write_dygraph_file(data,dygraph_fn):
	'''Writes a dygraph data file to disk'''

	# for k,v in data.items():		
	# 	print k, v


	# tests: all lists in the dictionary have to be of the same length
	if data.keys()[0]!='project':
		raise Exception('First key in orderedDict has to be the date (== project)')
	if len(data)<2:
		raise Exception('No data')
	if len(set([len(v) for v in data.values()])) != 1:
		print '\n'.join(map(str,data.values()[:5]))
		raise Exception('Data contains lists of different length:\n%s'%([len(v) for v in data.values()]))

	m = len(data.values()[0])

	fn = os.path.join(old_to_new.output_folder,'%s.csv'%dygraph_fn)

	with open(fn,'w') as o:
		
		labels = 'Date, %s\n'%(','.join(data.keys()[1:]))
		o.write(labels)
		for i in range(m):
			vals = '%s\n'%','.join([v[i] for v in data.values()])
			o.write(vals)


