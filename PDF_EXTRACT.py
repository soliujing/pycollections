
import shutil
import sys
import PyPDF2,os

def getAttachments(reader):
	"""
	Retrieves the file attachments of the PDF as a dictionary of file names
	and the file data as a bytestring.
	:return: dictionary of filenames and bytestrings
	"""
	catalog = reader.trailer["/Root"]
	fileNames = catalog['/Names']['/EmbeddedFiles']['/Names']
	attachments = {}
	for f in fileNames:
		if isinstance(f, str):
			name = f
			dataIndex = fileNames.index(f) + 1
			fDict = fileNames[dataIndex].getObject()
			fData = fDict['/EF']['/F'].getData()
			name = fDict['/F']
			attachments[name] = fData

	return attachments

from os.path import expanduser
FILE_PATH_HOME = expanduser("~")

FILE_PATH_PWD = FILE_PATH_HOME + "/.CITY_REJ_PWD"

FILE_PATH_WORK = FILE_PATH_HOME + "/Downloads/"

WorkisExist = os.path.exists(FILE_PATH_WORK)
if not WorkisExist:
	sys.exit("Error: work folder does not exist !!!")

FILE_PATH_OUT = FILE_PATH_WORK + "OUTPUT/"
FILE_PATH_TEMP = FILE_PATH_WORK + ".TEMP/"

isExist = os.path.exists(FILE_PATH_OUT)
if not isExist:
    os.makedirs(FILE_PATH_OUT)

isExist = os.path.exists(FILE_PATH_TEMP)
if not isExist:
    os.makedirs(FILE_PATH_TEMP)

with open(FILE_PATH_PWD) as f:
    lines = f.read() 
    PASSWORD = lines.split('\n', 1)[0]


files = [f for f in os.listdir('.') if os.path.isfile(f)]
files = filter(lambda f: f.endswith(('.pdf','.PDF')), files)

for each_file in files:
	ENCRYPTED_FILE_PATH = FILE_PATH_WORK + each_file
	with open(ENCRYPTED_FILE_PATH, mode='rb') as f:        
		reader = PyPDF2.PdfFileReader(f)
		if reader.isEncrypted:
			try:
				reader.decrypt(PASSWORD)
				dictionary = getAttachments(reader)
				# print(dictionary)
				for fName, fData in dictionary.items():
					with open(fName, 'wb') as outfile:
						outfile.write(fData)
			except NotImplementedError:
				command=f"qpdf --password='{PASSWORD}' --decrypt '{ENCRYPTED_FILE_PATH}' '{FILE_PATH_TEMP}{each_file}';"
				os.system(command)            
				with open(FILE_PATH_TEMP+each_file, mode='rb') as fp:
					reader = PyPDF2.PdfFileReader(fp)
					# print(f"Number of page: {reader.getNumPages()}")
				# print(f"Number of page: {reader.getNumPages()}")
					dictionary = getAttachments(reader)
					# print(dictionary)
					for fName, fData in dictionary.items():
						with open(FILE_PATH_OUT+fName, 'wb') as outfile:
							outfile.write(fData)

isExist = os.path.exists(FILE_PATH_TEMP)
if isExist:
    shutil.rmtree(FILE_PATH_TEMP)
