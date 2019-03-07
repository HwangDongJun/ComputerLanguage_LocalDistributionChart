import urllib
import urllib.request
import json

from GraphQL_crawler import graphql_api_crawler
from NextGraphQL_crawler import next_graphql_api_crawler
from selenium_lat_long import lat_long


class loca_info(object):
	def __init__(self, headers, lang):
		self.headers = headers
		self.lang = lang

	def get_loca_info(self):
		loca_data = graphql_api_crawler(self.headers, self.lang)
		loca_json = loca_data.run_query()
		
		if loca_json['data']['search']['nodes'] == list():
			return list()
		
		nodes = loca_json['data']['search']['nodes']

		loca_names = list()
		for node in nodes:
			if node == dict() or node['location'] == None or node['location'] == 'Error: Unable to resolve':
				continue
			loca_names.append(node['location'])
		
		#미리 쓰이는 것들 사전준비
		next_page = True
		next_loca_json = dict()
		for i in range(10): #현재로는 정해진 것이 없기에 10번까지만 반복을 진행
			if i == 0:
				next_page = loca_json['data']['search']['pageInfo']['hasNextPage']
			else:
				next_page = next_loca_json['data']['search']['pageInfo']['hasNextPage']

			cursor = loca_json['data']['search']['pageInfo']['endCursor']
			if next_page:
				next_loca_data = next_graphql_api_crawler(self.headers, self.lang, cursor)
				next_loca_json = next_loca_data.next_run_query()
				
				if next_loca_json['data']['search']['nodes'] == list():
					break

				next_nodes = next_loca_json['data']['search']['nodes']

				for node in next_nodes:
					if node == dict() or node['location'] == None or node['location'] == 'Error: Unable to resolve':
						continue
					loca_names.append(node['location'])
		
		send_loca_names = lat_long(loca_names)
		lati_long = send_loca_names.get_lat_longs()

		return lati_long
