
import csv
import json

def write_json(countries):
	output = open('country-codes.json', 'w')	
	output.write('[\n')
        for country in countries.values():
                output.write('\t %s,\n' % (json.dumps(country, sort_keys=True)))
        output.write(']\n')	
	output.close()

def write_csv(countries):
	output = open('country-codes.csv' 'wb')
	fieldnames = countries.get('NL').keys()
	writer = csv.Dictwriter(output,fieldnames, quoting=csv.QUOTE_MINIMAL)
	for a2, country in countries:iteritems():
		writer.writerow(country)
	output.close()

def create_country_dict(json_data):
	countries = {}
	for country in json_data:
		a2 = country.get('a2')
		countries[a2] = country
		print country
	return countries

def create_continent_dict(fh):
	continents = {}
	for line in fh:
		continent, name = line.strip().split(',')
		continents[continent] = name.strip()
	fh.close()
	return continents

def main():
	#make a spare copy of country-codes.bak and then run on the CMD
	# python continent.py > country-codes.json
	fh1 = open('country-codes.bak', 'r')
	fh2 = open('a2_continent.csv', 'r')
	fh3 = open('continent_name.csv', 'r')

	json_data = json.load(fh1)
	fh1.close()

	countries = create_country_dict(json_data)
	continents = create_continent_dict(fh3)

	for line in fh2:
		a2, continent = line.strip().split(',')
		
		country  = countries.get(a2)
		if country:
			country['continent'] = continent
			country['continent_name'] = continents.get(continent)

	fh2.close()

	#print json.dumps(countries.values(), indent=4, separators=(',', ': '))
	print json.dumps(countries.values(), indent=-1,separators=(',', ': '))

	write_json(countries)
	write_csv(countries)

if __name__ == '__main__':
	main()
