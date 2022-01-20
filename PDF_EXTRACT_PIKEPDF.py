# %%
import os,pikepdf

from os.path import expanduser
FILE_PATH_HOME = expanduser("~")

###### BASIC CONFIG ######
FILE_PATH_PWD = FILE_PATH_HOME + "/.CITY_REJ_PWD"
FILE_PATH_WORK = FILE_PATH_HOME + "/Downloads/"
FILE_PATH_OUT = FILE_PATH_WORK + "OUTPUT/"
FILE_PATH_TEMP = FILE_PATH_WORK + ".TEMP/"

isExist = os.path.exists(FILE_PATH_PWD)
if not isExist:
	exit("Error: password file [~/.CITY_REJ_PWD] does not exist !!!")

isExist = os.path.exists(FILE_PATH_WORK)
if not isExist:
	exit("Error: work folder does not exist !!!")

isExist = os.path.exists(FILE_PATH_OUT)
if not isExist:
    os.makedirs(FILE_PATH_OUT)

isExist = os.path.exists(FILE_PATH_TEMP)
if not isExist:
    os.makedirs(FILE_PATH_TEMP)

# read password
with open(FILE_PATH_PWD) as f:
    lines = f.read() 
    PASSWORD = lines.split('\n', 1)[0]

# get list of pdf files
files = [f for f in os.listdir('.') if os.path.isfile(f)]
files = filter(lambda f: f.endswith(('.pdf','.PDF')), files)

# %%
from pathlib import Path
for each_file in files:
	ENCRYPTED_FILE_PATH = FILE_PATH_WORK + each_file
	with pikepdf.Pdf.open(ENCRYPTED_FILE_PATH, password=PASSWORD) as pdf:
		##### attach new file to test multiple attachments
		# filespec = pikepdf.AttachedFileSpec.from_filepath(pdf, Path('/Users/jing_liu/Downloads/PDF_EXTRACT.py'))
		# pdf.attachments['PDF_EXTRACT.py'] = filespec

		for file_tag, file_details in pdf.attachments.items():
			#print filename
			print("FILENAME:" + file_details.filename)
			print("MIMETYPE:" + file_details.get_file().mime_type)

			with open(FILE_PATH_OUT+file_details.filename, 'wb') as outfile:
				outfile.write(file_details.get_file().read_bytes())

		# pdf.save(FILE_PATH_TEMP+each_file)    


