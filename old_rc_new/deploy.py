#!/usr/local/python
"""
Converts all dygraph files and 'deploys' them to data folder
"""
import os,argparse
import old_to_new

def main():
	parser = argparse.ArgumentParser(
		description="""Convert data for new report card. 
		"""
	)

	parser.add_argument(
		'-c', '--comscore',
		metavar="",
		type=str, 
		default='./input/comscore',
		help='<path> to the comscore files'
	)
	parser.add_argument(
		'-m', '--monthlystats',
		metavar='',
		type=str, 
		default="./input/StatisticsMonthly.csv",
		help='Monthly statistics file'
	)
	parser.add_argument(
		'-p', '--pageviews',
		metavar='',
		type=str, 
		default="./input/PageViewsPerMonthPopularWikisNormalized.csv",
		help='Page views file'
	)
	parser.add_argument(
		'-d', '--deploy',
		metavar='',
		type=bool, 
		default=False,
		help='Copies created files from output folder to datasources folder'
	)

	args = parser.parse_args()
	
	# read config passed as argument

	if os.path.exists(args.comscore): 
		old_to_new.comscore_directory = args.comscore
	else:
		print "%s doesn't exist"%(args.comscore)
		parser.print_help()
		return
	if os.path.isfile(args.monthlystats): 
		old_to_new.monthly_stats = args.monthlystats
	else:		
		print "%s doesn't exist"%(args.monthlystats)
		parser.print_help()
		return
	if os.path.isfile(args.pageviews): 
		old_to_new.page_views = args.pageviews
	else:		 
		print "%s doesn't exist"%args.pageviews
		parser.print_help()
		return
	

	old_to_new.create_all()

	# make sure all dates are correct, they come formatted in all kinds of ways...
	os.system('./fix-dates.sh %s/*.csv'%old_to_new.output_folder)
	try:
		os.system('rm %s/*.csv~'%old_to_new.output_folder)
	except Exception:
		pass

	if args.deploy:
		print 'Deploying data files to datasources directory'
		try:
			os.system("cp %s/*.csv ../../data/datasources/rc"%old_to_new.output_folder)
		except Exception:
			pass

	
if __name__ == "__main__":
	main()