from selenium import webdriver
import time


class lat_long(object):
	def __init__(self, locations):
		self.locations = locations

	def get_lat_longs(self):
		data = self.locations

		driver = webdriver.Chrome('/usr/local/bin/chromedriver')  # Optional argument, if not specified will search path.
		#http://chromedriver.chromium.org/downloads  <- download chromedriver
		driver.get('https://www.latlong.net/countries.html')
		
		crash = 1
		results = []
		skipped = []
		for i,row in enumerate(data): #enumerate는 i가 몇번째인지. row는 해당 행의 내용 전부를 가져옴(csv파일 확인)
			print(i) #횟수출력
			search = driver.find_element_by_id('keyword') #해당 웹의 HTML코드에서 id설정한 것 부르기.
			search_term = row #해당 파일의 location의 정보를 가져온다.
			search.clear() #search를 clear해주어야 하는 것 같다.
			try:
				search.send_keys(search_term) #해당 place(id)의 위치에 send_keys함수를 통해 인자를 전달
			except:
				print('Skiped %s' %search_term)
				print(row)
				skipped.append(row)
				continue

			search.submit() #아마 이 부분이 입력된 값에 대한 결과를 확인하기 위해 사용
			#http://www.latlong.net/에서는 Find버튼을 누르는 행동이라고 생각해도 좋다.
			time.sleep(2) #결과 출력을 기다려야 하기에 기다린다.
			lat_split = list()
			try:
				check = driver.find_element_by_class_name('col-8').text.split('\n')[2]
				if check != "No place found.":
					lat = driver.find_element_by_tag_name('tbody')
					lat_split = lat.text.split('\n')[1].split()
				else:
					continue
			except:
				alert = driver.switch_to_alert() #alert창 다루기 (알림창)
				alert.accept() #alert확인
				driver.switch_to_default_content()
				print('Couldnt find %s' %search_term)
				print(row)
				skipped.append(row)
				continue
	
			#lat_long = lat.text.strip('() ').split(',') #strip으로 '() '를 제거 / ,를 기준으로 분류
			lat_long_clean = [float(lat_split[-2]), float(lat_split[-1])]

			try:
				driver.refresh() #웹페이지 새로고침
			except:
				print(skipped)
			crash +=1
			
			print(lat_long_clean)
			results.append(lat_long_clean)
		
		driver.close()
		return results
