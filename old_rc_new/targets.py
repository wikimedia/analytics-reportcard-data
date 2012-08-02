'''
Creates dygrap csv files for target/benchmarks
'''
import os

try: 
	from collections import OrderedDict
except ImportError:
	from ordereddict import OrderedDict

from collections import defaultdict

import old_to_new
import utils

def extractData(fn, sep,format,fields):
	'''
	:arg sep: seperater
	:arg format: format of date (which is on the first position)
	:arg fields: list of tuples ('name',index), e.g. ('target',2)
	'''
	data = defaultdict(lambda : defaultdict(str))
	# data = defaultdict(dict)
	for line in open(fn,'r'):
		# first pos is always data
		if line[-1]!='\n':
			line+='\n'

		vals = line[:-1].split(sep)
		ts = utils.to_ts(vals[0],format)

		for n,i in fields:
			data[n][ts] = str(vals[i])

	return data

def dygraphOutput(out_fn,tss,actual,target,a_names,t_names,error_bar=0,error_bar_names=['Target']):
	'''Saves a valid dygraph file in `out_fn`. 

	:arg actual: dict containing actual data points (can be multiple keys)
	:arg target: dict containing target data points (can be multiple keys)
	:arg a_names: ordered list of actual labels (have to correspond to keys in `actual`)
	:arg t_names: ordered list of target labels (have to correspond to keys in `target`)
	:arg t_names: optional int, width of error bar as percentage of max target['Target'] value
	'''

	with open(os.path.join(old_to_new.output_folder,out_fn),'w') as out:
		headers = ["Date"]+a_names+t_names #[f[0] for f in a_fields]+[f[0] for f in t_fields]
		out.write(','.join(headers)+'\n')


		if error_bar:
			
			maxTarget = max([float(a) for n in error_bar_names for a in target[n].values() if a!='']) 
			delta = maxTarget/100*error_bar


		# iterate ordered list of timestamps
		for ts in tss:
			if error_bar:
				# show error bar of target_error_bar percent for target line

				vals = [utils.dygraph_date(ts)]
				for n in a_names:
					if actual[n][ts] != '':					
						vals += [';'.join(3*[actual[n][ts]])]
					else:
						vals += ['']					

				for n in t_names:
					if target[n][ts] != '':
						if n in error_bar_names:			
							vals += ['%s;%s;%s'%(float(target[n][ts])-delta,target[n][ts],float(target[n][ts])+delta)]
						else:
							vals += [';'.join(3*[target[n][ts]])]
					else:
						vals += ['']	
					
				# vals += ['%s;%s;%s'%(int(target[n][ts])-delta,target[n][ts],int(target[n][ts])+delta) for n in t_names]
				
			else:
				vals = [utils.dygraph_date(ts)]+[actual[n][ts] for n in a_names]+[target[n][ts] for n in t_names]

			print ','.join(vals)
			out.write(','.join(vals)+'\n')

def active_editors_target(min_ts,max_ts):
	# input files

	metricfile = os.path.join(old_to_new.output_folder,'rc_active_editors_count.csv')
	# metricfile = '../data/datafiles/rc/rc_active_editors_count.csv'
	targetfile = '../misc/targets/editor_target.csv'

	# time range
	tss,tss_i = utils.create_time_stamps_month(fromym=min_ts,toym=max_ts) 

	target = extractData(targetfile, '\t','MMM-YY',[('Projected',1),('Target',2)])
	actual = extractData(metricfile, ',','YYYY/MM/DD',[('Total',1)])

	dygraphOutput('rc_active_editors_target.csv',tss,actual,target,['Total'],['Target','Projected'],error_bar=2)#,error_bar_names=['Target','Projected'])

def mobile_pageviews_target(min_ts,max_ts):
	# input files
	metricfile = '../datafiles/rc_page_requests_mobile.csv'
	targetfile = '../misc/targets/mobile_target.csv'

	# time range
	tss,tss_i = utils.create_time_stamps_month(fromym=min_ts,toym=max_ts) 

	target = extractData(targetfile, '\t','MMM-YY',[('Target',3)])
	actual = extractData(metricfile, ',','YYYY/MM/DD',[('Total',1)])

	dygraphOutput('rc_page_requests_mobile_target.csv',tss,actual,target,['Total'],['Target'],error_bar=4)

def create_all():

	active_editors_target(min_ts='200903',max_ts='201206')
	mobile_pageviews_target(min_ts='201006',max_ts='201206')

