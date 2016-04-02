from bs4 import BeautifulSoup
import requests
import json

### Open djmag compilation and scrape top 100 list
url = 'http://djmag.com/top100clubs?year=2016'
r = requests.get(url)
data = r.text

pageSoup = BeautifulSoup(data,'html.parser')
clubTags = pageSoup.findAll('h1', { 'class' : 'typography--HEADING-TERTIARY' })

clubs = []
### scrape details from individual club site one by one
for clubTag in clubTags:
	club = {'name':'','address':'', 'capacity':0,'link':''}
	clubString = clubTag.a.string.split()
	club['rank'] = clubString[0]
	club['name'] = ' '.join(clubString[1:]).title()
	club['link'] = 'http://djmag.com' + clubTag.a['href']
	
	# open individual club page from link
	tempr = requests.get(club['link'])
	clubData = tempr.text
	clubSoup = BeautifulSoup(clubData,'html.parser')
	
	# scrape details from each club page
	clubAddress 	= clubSoup.find_all('div',{'class':'field--name-field-club-address'})	
	club['address'] 	= clubAddress[0].contents[1].contents[0].string

	clubCapacity 	= clubSoup.find_all('div',{'class':'field--name-field-club-capacity'})
	club['capacity'] 	= clubCapacity[0].contents[1].contents[0].string

	clubWebsite 	= clubSoup.find_all('div',{'class':'field--name-field-club-web'})
	club['website'] 	= clubWebsite[0].contents[1].contents[0].string if len(clubWebsite) else 'Website Not Listed'

	# Geocode: Address -> Lat long
	url="https://maps.googleapis.com/maps/api/geocode/json?address=%s" % club['address']

	geocodeResponse = requests.get(url)
	jsongeocode = json.loads(geocodeResponse.text)

	#store lat,lng info to make plotting easy
	club['lat'] = str(jsongeocode['results'][0]['geometry']['location']['lat'])
	club['lng'] = str(jsongeocode['results'][0]['geometry']['location']['lng'])

	# Add the club dict to the list
	clubs.append(club);

	clubStr = club['rank']+';'+club['name'] +';' + club['address'] +';' + club['capacity'] +';'+ club['website']+";"+club['lat']+";"+club['lng']	
	print(clubStr)

# write the list of club dicts to json file
with open('output2.json', 'w') as fp:
    json.dump(clubs, fp)