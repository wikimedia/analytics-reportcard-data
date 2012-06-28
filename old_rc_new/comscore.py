'''
Adapts dygrap csv files comscore data

ErikZ supplied dygraph friendly files for comescore.

All that needs to be done is 
	* crop the amount of data to match what is being shown in the report card
	* replace region codes with region names

'''

import os

import old_to_new
from utils import fix_dates


comscore_properties_fn = ''
comscore_regions_reach_fn = ''
comscore_regions_uv_fn = ''

comscore_regions_dictionary_fn = ''



comscore_regions_dictionary = {}
def initRegionsDict():
	"""
	target_language,region_code,region_name
	en,AS,Asia Pacific
	en,C,China
	en,EU,Europe
	en,I,India
	en,LA,Latin-America
	en,MA,Middle-East/Africa
	en,NA,North-America
	en,W,World
	fr,EU,L'Europe
	nl,EU,Europa
	"""
	comscore_regions_dictionary['AS'] = "Asia Pacific"
	comscore_regions_dictionary['C'] = "China"
	comscore_regions_dictionary['EU'] = "Europe"
	comscore_regions_dictionary['I'] = "India"
	comscore_regions_dictionary['LA'] = "Latin-America"
	comscore_regions_dictionary['MA'] = "Middle-East/Africa"
	comscore_regions_dictionary['NA'] = "North-America"
	comscore_regions_dictionary['W'] = "World"
	# for line in open(comscore_regions_dictionary_fn,'r'):
	# 	d = line[:-1].split(',')
	# 	comscore_regions_dictionary[d[1]] = d[2]


def replaceRegion(fn):
	data = open(fn,'r').read()
	for c,r in comscore_regions_dictionary.items():
		data = data.replace(c,r)
	return data


def processRegion(in_fn,out_fn):
	"""
	"""
	with open(os.path.join(old_to_new.output_folder,out_fn),'w') as out:
		for line in replaceRegion(in_fn).split('\n'):						
			field = line.split(',')
			if len(field)<2:
				continue
			# put the last column 'world' in first place
			field[1],field[-1]=field[-1],field[1]

			out.write(",".join(field)+'\n')	

	

def filterProperties(props):
	
	allprops = open(comscore_properties_fn,'r').read().split('\n')[0].split(',')

	indices = [0] + [i for i,p in enumerate(allprops) if p in props]

	o = open(os.path.join(old_to_new.output_folder,'rc_comscore_properties.csv'),'w')

	for line in open(comscore_properties_fn,'r'):

		fields = line[:-1].split(',')		

		o.write(','.join([fields[i] for i in indices])+'\n')
	


def create_all():
	global comscore_properties_fn,comscore_regions_reach_fn,comscore_regions_uv_fn,comscore_regions_dictionary_fn

	comscore_properties_fn = os.path.join(old_to_new.comscore_directory,'wikilytics_in_comscore_properties_uv.csv')
	comscore_regions_reach_fn = os.path.join(old_to_new.comscore_directory,'wikilytics_in_comscore_regions_reach.csv')
	comscore_regions_uv_fn = os.path.join(old_to_new.comscore_directory,'wikilytics_in_comscore_regions_uv.csv')
	comscore_regions_dictionary_fn = os.path.join(old_to_new.comscore_directory,'wikilytics_in_dictionary_regions.csv')


	initRegionsDict()

	processRegion(in_fn=comscore_regions_uv_fn,out_fn='rc_comscore_region_uv.csv')
	processRegion(in_fn=comscore_regions_reach_fn,out_fn='rc_comscore_region_reach.csv')
	

	filterProperties(['Total Internet','Google','Wikimedia'])