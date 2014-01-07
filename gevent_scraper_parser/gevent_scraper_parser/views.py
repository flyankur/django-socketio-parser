import os
from scrapely import Scraper
import pdb, urllib2, re
from bs4 import BeautifulSoup
from urlparse import urlparse, parse_qs

from django.conf import settings
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponse, Http404
from django.views.decorators.csrf import csrf_exempt
import random, requests, json

def scrapeData(url,webpage):
	# scraper = Scraper()
	# testUrl = ('http://london.craigslist.co.uk/search/moa?catAbb=moa&query=iphone&zoomToPosting=&minAsk=&maxAsk=')
	# testData = {'name': 'iPhone 5s GOLD brand new 64GB 02'}
	# scraper.train(testUrl, testData)

	# url2 = 'http://london.craigslist.co.uk/search/moa?catAbb=moa&query=iphone&zoomToPosting=&minAsk=9000&maxAsk='
	# data = scraper.scrape(url2)

	# webpage = 'ebay'
	# url = 'http://www.ebay.in/sch/i.html?_odkw=iphone+gold&_osacat=0&_from=R40&_trksid=p2045573.m570.l1313.TR0.TRC0.Xiphone+gold+32gb&_nkw=iphone+gold+32gb&_sacat=0'

	# webpage = 'craigslist'
	# url = 'http://london.craigslist.co.uk/search/moa?catAbb=moa&query=iphone&zoomToPosting=&minAsk=5000&maxAsk='

	#webpage = 'kickstarter'
	#url = 'http://www.kickstarter.com/projects/702400282/maxstone-iphone-your-camera'

	# url = 'http://www.jabong.com/giordano-P6868-Black-Analog-Watch-183702.html'
	# webpage = 'asd'
	# url = 'http://www.zomato.com'
	page_data = urllib2.urlopen(url).read()
	soup = BeautifulSoup(page_data)
	page_text = soup.get_text()

	query_from_url = ''
	query_from_page = ''
	phone_nums = []
	fb_links = []
	tw_links = []
	li_links = []
	gp_links = []
	leads = []

	fb_re = re.compile(r'(\S*)facebook.com/\w+')
	tw_re = re.compile(r'(\S*)twitter.com/\w+')
	li_re = re.compile(r'(\S*)linkedin.com/\w+')
	gp_re = re.compile(r'(\S*)plus.google.com/(\+)*\w+')

	email_regex = re.compile(r'[\w\.-]+@[\w\.-]+')
	emails = email_regex.findall(page_text)

	page_links = soup.find_all('a')

	links=[]
	for page_link in page_links:
		link = page_link.get('href')
		links.append(link)

		if link is None:
			continue

		fb_match = fb_re.search(link)
		tw_match = tw_re.search(link)
		li_match = li_re.search(link)
		gp_match = gp_re.search(link)

		if fb_match is not None and link not in fb_links:
			fb_links.append(link)
		elif tw_match is not None and link not in tw_links:
			tw_links.append(link)
		elif li_match is not None and link not in li_links:
			li_links.append(link)
		elif gp_match is not None and link not in gp_links:
			gp_links.append(link)
		elif 'mailto:' in link:
			email = link.split(':')[1]
			if email not in emails:
				emails.append(email)

	if webpage == 'ebay':
		query_string = urlparse(url).query
		query_from_url = parse_qs(query_string)['_nkw'][0]

		query_from_page = str( soup.find(id='gh-ac')['value'] )

	elif webpage == 'kickstarter':
		website_block = soup.find('li', class_='links')
		if website_block is not None:
			website_link = str(website_block.find('a', class_='popup').get('href'))
		kickstarter_extra_response = requests.get(url=url + '/creator_bio.js')
		kickstarter_soup = BeautifulSoup(kickstarter_extra_response.text)
		kickstarter_links = kickstarter_soup.find_all('a')

		k_links=[]
		for kickstarter_link in kickstarter_links:
			k_link = kickstarter_link.get('href')
			if k_link is None:
				continue
			tw_match = tw_re.search(k_link)
			li_match = li_re.search(k_link)
			gp_match = gp_re.search(k_link)
			if tw_match is not None and k_link not in tw_links:
				tw_links.append(k_link)
			elif li_match is not None and k_link not in li_links:
				li_links.append(k_link)
			elif gp_match is not None and k_link not in gp_links:
				gp_links.append(k_link)


	elif webpage == 'craigslist':
		query_string = urlparse(url).query
		query_from_url = parse_qs(query_string)['query'][0]

		query_from_page = str( soup.find(id='query')['value'] )

		listings = soup.findAll('span',{'class':'pl'})
		for listing in listings:
			print "doing"
			listing_href = str(listing.contents[3].get('href'))
			listing_href_array = listing_href.split('/')
			listing_num = listing_href_array[len(listing_href_array) - 1].split('.')[0]

			listing_email_response = requests.get(url='http://craigslist.org/reply/' + listing_num)
			email_soup = BeautifulSoup(listing_email_response.text)

			email_input = email_soup.find("input", class_="anonemail")
			if email_input is not None:
				if 'subject' in parse_qs(urlparse(email_soup.find("a", class_="mailto").get('href')).query):
					subject = parse_qs(urlparse(email_soup.find("a", class_="mailto").get('href')).query)['subject'][0]
				else:
					subject = ''
				lead = {
					'email_address': email_input['value'],
					'subject': subject,
					'listing_link': listing_href
				}
				if lead not in leads:
					leads.append(lead)

			phone_block = email_soup.find('b',text="contact by phone:")
			if phone_block is not None:
				phone_num = phone_block.findNext().text
				# phone_num = phone_num.decode('unicode_escape').encode('ascii','ignore')
				# print phone_num
				if phone_num not in phone_nums:
					phone_nums.append( phone_num )


	response_json = {
		'query': {
			'url': query_from_url,
			'page': query_from_page
		},
		'emails': emails,
		'phone': phone_nums,
		'social_leads': {
			'facebook': fb_links,
			'twitter': tw_links,
			'linkedin': li_links,
			'googlePlus': gp_links,
		}
	}

	if webpage == 'craigslist':
		response_json['leads'] = leads

	if webpage == 'kickstarter':
		response_json['social_leads']['website'] = website_link

	# pdb.set_trace()
	return json.dumps(response_json)
