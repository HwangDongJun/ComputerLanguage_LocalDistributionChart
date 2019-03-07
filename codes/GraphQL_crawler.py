import requests

PATH = 'https://api.github.com/graphql'


class graphql_api_crawler(object):
	def __init__(self, headers, lang):
		self.headers = headers
		self.query = '''
		{
			search (query:"language:''' + lang  + '''", type:USER, last:100) {
				pageInfo {
					startCursor
					hasNextPage
					endCursor
				}
				nodes {
					... on User {
						location
					}
				}
			}
		}
		'''

	def run_query(self):
		request = requests.post(PATH, json={'query': self.query}, headers=self.headers)
		if request.status_code == 200:
				return request.json()
		else:
			raise Exception("Query failed to run by returning code of {}. {}".format(request.status_code, self.query))
