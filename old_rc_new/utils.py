'''
A set of utility methods that are used in different parts of the framework.
'''

import logging


months_dict = {'Mar': '03', 'Feb': '02', 'Aug': '08', 'Sep': '09', 'Apr': '04', 'Jun': '06', 'Jul': '07', 'Jan': '01', 'May': '05', 'Nov': '11', 'Dec': '12', 'Oct': '10'}


def fix_date(t,format):
	'''Formats the date from Jan/2001 into 2001/01/01 style'''
	if format == 'MMM-YY':
		return '20%s/%s/01'%(t[4:], months_dict[t[:3]])
	elif format == 'MM/YYYY':
		return '%s/%s/01'%(t[3:],t[:2])
	elif format == 'YYYY-MM':
		return '%s/%s/01'%(t[:4],t[5:])


def fix_dates(dates,format):
	return [fix_date(t,format) for t in dates]
		
def dygraph_date(ts):
	return '%s/%s/01'%(ts[:4],ts[4:])

def to_ts(date,format):
	'''Formats the date from Jan/2001 or simple ts style'''
	if format != 'YYYY/MM/DD':
		date = fix_date(date,format)
	return '%s%s'%(date[:4],date[5:7])


def create_time_stamps_month(fromym='200101',toym='201012'):
	'''
	Helper data structures for time stamps
	List of all time unites, i.e. every month. yyyymm
	'''
	time_stamps = []
	# A dictionary that serves as a lookup for the index of atime stamp
	time_stamps_index = {}

	min_year = fromym[:-2]
	min_month = fromym[-2:]
	max_year = toym[:-2]
	max_month = toym[-2:]

	i = 0 
	#add remaining months in the first year
	for m in range(int(min_month),13):
		ts = '%s%02d'%(min_year,m)
		time_stamps.append(ts)
		time_stamps_index[ts] = i
		i += 1
	#add intermediate years
	for y in range(int(min_year)+1,int(max_year)):
		for m in range(1,13):
			ts = '%s%02d'%(y,m)
			time_stamps.append(ts)
			time_stamps_index[ts] = i
			i += 1
	#last year
	for m in range(1,int(max_month)+1):
		ts = '%s%02d'%(max_year,m)
		time_stamps.append(ts)
		time_stamps_index[ts] = i
		i += 1

	return (time_stamps,time_stamps_index)

def create_time_stamps_day(fromymd='20010101',toymd='20101231'):
	'''
	Helper data structures for time stamps
	List of all time unites, i.e. every month. yyyymm
	'''

	import calendar

	time_stamps = []
	# A dictionary that serves as a lookup for the index of atime stamp
	time_stamps_index = {}

	min_year = int(fromymd[:4])
	min_month = int(fromymd[4:6])
	min_day = int(fromymd[6:8])
	max_year = int(toymd[:4])
	max_month = int(toymd[4:6])
	max_day = int(toymd[6:8])
	i = 0 
	#add remaining months in the first year
	for m in range(min_month,13):
		# calender.monthrange returns a tuple (day of the week, number of days in the month)
		nds = calendar.monthrange(min_year,m)[1]
		for d in range(min_day,nds+1):
			ts = '%s%02d%02d'%(min_year,m,d)
			time_stamps.append(ts)
			time_stamps_index[ts] = i
			i += 1
	#add intermediate years
	for y in range(min_year+1,max_year):
		for m in range(1,13):
			# calender.monthrange returns a tuple (day of the week, number of days in the month)
			nds = calendar.monthrange(y,m)[1]            
			for d in range(1,nds+1):
				ts = '%s%02d%02d'%(y,m,d)
				time_stamps.append(ts)
				time_stamps_index[ts] = i
				i += 1
	#to last month
	for m in range(1,max_month):
		nds = calendar.monthrange(max_year,m)[1]
		for d in range(1,nds+1):
			ts = '%s%02d%02d'%(max_year,m,d)
			time_stamps.append(ts)
			time_stamps_index[ts] = i
			i += 1
	#to last day
	for d in range(1,max_day+1):
		ts = '%s%02d%02d'%(max_year,max_month,d)
		time_stamps.append(ts)
		time_stamps_index[ts] = i
		i += 1


	return (time_stamps,time_stamps_index)
	
	
def computeMonthStartEndtime(ym):
	'''
	Returns the starting and end datetime object for the yyyymm passed. I.e. the first and last day of the month

	:arg ym: str, 'yyyymm' format
	:returns: tuple of datetime objects
	'''
	from datetime import datetime
	import calendar

	
	y = int(ym[:4])
	m = int(ym[4:])

	start = datetime(y, m, 1)
	# days in the given month 
	# calender.monthrange returns a tuple (day of the week, number of days in the month)
	d = calendar.monthrange(y,m)[1]

	end = datetime(y, m, d)

	return (start,end)

def numberOfMonths(ymStart,ymEnd):
	'''Returns the number of months between the parameters.

	:arg ymStart: str, 'yyyymm' format
	:arg ymEnd: str, 'yyyymm' format
	:returns: int, number of month
	'''
	months = 0
	months += (int(ymEnd[:4])-(int(ymStart[:4])+1)) * 12
	if int(ymEnd[:4])==int(ymStart[:4]):
		#same year
		months += (int(ymEnd[4:])-int(ymStart[4:]))+1
	else:
		months += 12-int(ymStart[4:])+1
		months += int(ymEnd[4:])

	return months



def movingAverage(array, WINDOW=5):
	try:
		import numpy as N
	except:
		logging.warning("Moving average can't be computed (Numpy not installed)")
		return
	
	
	weightings = N.repeat(1.0, WINDOW) / WINDOW
	return N.convolve(array, weightings)[WINDOW-1:-(WINDOW-1)]    


