import os
import sys
import pandas as pd

from get_certification import git_certification
from get_location import loca_info

def lang_location(argv):
	if len(argv) < 3:
		print("Type as shown : python3 main.py userID:userPWD language")
		sys.exit(0)
	
	user_cert = argv[1]
	Ucert = git_certification(user_cert)
	cert_info = Ucert.get_info2base64()

	header = {'Authorization' : ('Basic ' + cert_info)}

	info_loca = loca_info(header, argv[2])
	loca_list = info_loca.get_loca_info()

	if len(loca_list) == 0:
		print("list empty")
		sys.exit(0)
	
	df = pd.DataFrame.from_records(loca_list, columns=['latitude', 'longitude'])
	df.to_csv('LocationData_' + argv[2] + '.csv')

if __name__ == '__main__':
	sys.exit(lang_location(sys.argv))
