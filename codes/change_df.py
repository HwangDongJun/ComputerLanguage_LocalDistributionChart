import json
import pandas as pd
import os

path_dir = '/home/dnlab/github/ComputerLanguage_LocalDistributionChart/codes/'
file_list = os.listdir(path_dir)

def change_language_name(start, end, lang):
	set_dict = dict()
	st = 1
	for i in range(start, end):
		set_dict[i] = (lang + str(st))
		st += 1
    
	return set_dict

#append한 csv파일에서 language마다 하나로 묶어주는 함수이지만 현재 사용하지 않습니다.
def change_df_info(langs, df, sizes):
	sta = 0; end = 0; count = 0
	for si in sizes:
		end = (sta + si)
		df_dict = change_language_name(sta, end, langs[count])
		df.rename(index=df_dict, inplace=True)
		sta = end
		count += 1

	df.index.names = ['language']
	return df


if __name__ == "__main__":
	regular = ".csv"
	names = list()
	for name in file_list:
		if regular in name and name != "Result_lang_data.csv":
			names.append(name)

	'''
	현재로서는 LocationData_language.csv파일로 만들어진 파일이 전부 합쳐져 json파일의 최종적인 형태로 만들어진다. 	  하지만 Kibana를 사용한 형태에서는 서로간의 구분이 힘들기 때문에 (실제로 내 실력이 여기까지...) 하나의 파일로만 	만드는 방향으로 진행하는 것이 좋다. (location.json파일도 'a'로 이어서 써지기 때문에 새롭게 만들려면 일단      	  삭제 해야 한다.)
	'''

	len_list = list()
	lang_list = list()
	new_df = pd.core.frame.DataFrame()
	
	#각 이름에 맞는 csv파일을 불러와 행으로 합치는 과정
	for n in names:
		df = pd.read_csv('./' + n, index_col=0)
		len_list.append(len(df.index.tolist()))
		lang_list.append(n[n.index("_")+1:n.index(".")])
		if len(new_df.index.tolist()) == 0:
			new_df = df
		else:
			new_df = new_df.append(df, ignore_index=True)
	''' ↑↑↑ 코드를 의미
	실제로 kibana를 돌려보니 현재 내가 실행하는 elasticsearch방법으로는 laguage로 구별을 하지 않는다.
	방법이야 여러가지 있겠지만 일단 여기서 중지.
	그래서 아래와 같이 모든 csv파일을 합칠필요는 없어보인다.
	각각의 csv파일을 보여주는 과정을 진행하는 것이 현재까지는 맞는 것으로 보인다. 이상.
	'''
	temp1 = list()
	for j in range(len(new_df.index)):
		temp2 = list()
		temp_dict = dict()
		temp_dict["lat"] = new_df.loc[[j]].iloc[0,0]
		temp_dict["lon"] = new_df.loc[[j]].iloc[0,1]
		temp2.append(temp_dict)
		temp1.append(temp2)

	loc_df = pd.DataFrame.from_records(temp1, columns=["location"])
	new_df = pd.concat([new_df,loc_df], axis=1)

	#result_df = pd.core.frame.DataFrame()
	#result_df = change_df_info(lang_list, new_df, len_list)
	#result_df.to_csv('Result_lang_data.csv')
	
	index = 0
	for lan in lang_list:
		for v in range(len_list[lang_list.index(lan)]):
			first_dict = { "index" : { "_index" : "locations", "_type" : "latlon", "_id" : str(index) } }

			lat = new_df.loc[[v]].iloc[0,0]
			lon = new_df.loc[[v]].iloc[0,1]
			second_dict = {"language" : lan, "latitude" : lat, "longitude" : lon, "geo_location" : {"lat" : lat, "lon" : lon} }
			#a는 이어쓰기니까 반드시 해당 파일은 삭제하고 다시 실행할것.
			with open('./lang_conf/location.json', 'a', encoding="utf-8") as fw:
				json.dump(first_dict, fw)
				fw.write("\n")
				json.dump(second_dict, fw)
				fw.write("\n")
			index += 1
