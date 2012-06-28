# Purpose

Script to transform the data created for the [old report card](stats.wikimedia.org/reportcard) by Erik Zachte into the format required by the [new report card](reportcard.wmflabs.org). The data is not generated nor aggregated, the scripts simply extract the necessary data points to generate the charts on the report card. This is a temporary solution while the new analytics platform is in development.

# Usage

	python deploy.py [-h] [-c] [-m] [-p] [-d]

	Convert data for new report card.

	optional arguments:
	  -h, --help            show this help message and exit
	  -c , --comscore       <path> to the comscore files
	  -m , --monthlystats   Monthly statistics file
	  -p , --pageviews      Page views file
	  -d , --deploy         Copies created files from output folder to datasources folder


# What is generated

## Charts from old report card

The input files and a list of graph data extracted from them.

* `excel_in_PageViewsPerMonthPopularWikisNormalized_*.csv` contains:
	*  Page Requests for All Wikimedia Projects (mobile & non-mobile) : lines 3-31
* `excel_in_StatisticsMonthly_*.csv` contains:
	* Binary Files : lines 521-535
	* Wikipedia Articles (per wiki) : lines 263-290
		* NOTE: Total is not displayed on old report card -> set 'visibility' to [0,1,1,1,1,1,1,1] on new report card
		* only 8 largest wiki's
	* New Wikipedia Articles Per Day (per wiki) : lines 349-376
		* only 8 largest wiki's
	* Wikipedia Edits Per Month (per wiki) : lines 435-462
		* only first 5 wiki's
	* New Editors Per Month for All Wikimedia Projects  : lines 2-29
		* only first 10 wiki's
	* Active Wikimedia Editors for All Wikimedia Projects (5+) : lines 89-116
		* only first 10 wiki's
		* Add the note : Aug 2010: Editors on Commons are no longer included in overall total, on the assumption that most also edit on one or more other projects. More precise detection of double counts between any projects and languages is planned for late 2010 (using Single User Login registration).
	* Very Active Editors for All Wikimedia Projects (100+) : lines 176-203
		* only first 10 wiki's
		* Add the note : Aug 2010: Editors on Commons are no longer included in overall total, on the assumption that most also edit on one or more other projects. More precise detection of double counts between any projects and languages is planned for late 2010 (using Single User Login registration).

The format of the comscore data has been made dygraph friendly by ErikZ (thanks), there are only cosmetic changes necessary.

* Replacing region codes by actual region names
* Only display selected web properties for comparison (`wikilytics_in_comscore_properties_uv.csv`)	


## Charts not in the old report card

* Targets
	* Active Editors
	* Mobile Page Requests
* Mobile Page Requests


## Directory structure

	input/
		excel_in_PageViewsPerMonthPopularWikisNormalized_*.csv
		excel_in_StatisticsMonthly_*.csv
		comscore/
			wikilytics_in_comscore_properties_uv.csv			
			wikilytics_in_comscore_regions_uv.csv
			wikilytics_in_comscore_regions_reach.csv
			wikilytics_in_dictionary_regions.csv
	


