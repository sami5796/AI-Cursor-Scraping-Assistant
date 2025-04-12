#!/usr/bin/env python
# I'll just read the file to see its contents, not make any changes.
# When writing the scraper, modifiy the output field list to match the template  you're using.
from camoufox.sync_api import Camoufox
import time
from random import randrange
import random
from scrapy.http import HtmlResponse
import csv
from datetime import datetime


def scroll_down(page):
	"""A method for scrolling the page."""
	# Get scroll height.
	i=0
	while i < 20:
		page.mouse.wheel(0,20000)
		interval=randrange(3,5)
		time.sleep(interval)
		print(i)
		i=i+1
		
		
def accept_cookies(page):
	try:
		page.locator('xpath=//button[@id="onetrust-accept-btn-handler"]').click()
	except:
		pass
		
with Camoufox(humanize=True, 
	 geoip=True
	) as browser:
	page = browser.new_page()
	page.goto(url)
	page.wait_for_load_state()
	page.locator('xpath=//button[@id="collection-button"]').click()
	interval=randrange(5,10)
	time.sleep(interval)
	accept_cookies(page)
	
	html_page=page.content()
	response_sel = HtmlResponse(url="my HTML string", body=html_page, encoding='utf-8')
	articles=response_sel.xpath('//div[@class="product-item"]')
	print(len(articles))
	with open("output.txt", "a") as file:
		csv_file = csv.writer(file, delimiter="|")
	
		for product in articles:
			price=product.xpath('.//span[contains(@class, "price")]/text()').extract()[0].strip()
			fullprice=price
			product_code=product.xpath('.//div[@class="product-item-meta"]/@id').extract()[0].split('-')[-1]
			print(product_code)
			currency='EUR'
			country='ITA'
			product_url="https://www.hermes.com"+product.xpath('.//a/@href').extract()[0].strip()
			brand=website='HERMES'
			#print(brand)
			date=(datetime.now()).strftime("%Y%m%d")
			#print(date)
			try:
				gender=response_sel.xpath('//span[@class="header-title-parent"]/text()').extract()[0]
			except:
				gender = 'n.a.'
			try:
				category=response_sel.xpath('//span[@class="header-result-title"]/text()').extract()[0]
			except:
				category = 'n.a.'
	
			#print(product.xpath('.//figure').extract()[0])
			imageurl = "https:"+product.xpath('.//img/@src').extract()[0]
			title = product.xpath('.//span[@class="product-item-name"]/text()').extract()[0].strip()
			csv_file.writerow([product_code,gender,brand,category, fullprice, price, currency, country, date, product_url, imageurl, title, website ])
	file.close()
