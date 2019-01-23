#!/usr/bin/python
# encoding: UTF-8
import codecs
from os import walk
def getFileVals(char):
	vals=[]
	fileList=[]
	for root, dirs, files in walk(top="PlantProfiles", topdown=True):
		for i in range(len(files)):
			if files[i].split('.')[-1].lower()=='csv': fileList.append(root+'/'+files[i])
	for profile in fileList:
		print profile
		fin=codecs.open(profile,encoding='UTF-8')
		for line in fin:
			if line.split('\t')[0]==char:
				if '#' not in line:
					for val in line.split('\t')[1].split(','):
						if val.strip() not in vals: vals.append(val.strip())
				break
	return vals
fin=codecs.open("Chars.csv",encoding='UTF-8')
cfin=[line for line in fin]
fin.close()
i=0
newVals={}
for line in cfin:
	i+=1
	if '#' not in line and line.split('\t')[0]=='Clr':
		char=line.split('\t')[1]
		newVals[i]="Clr\t%s\t%s"%(char, ','.join(getFileVals(char)))
print "Done gathering data..."
for item in newVals:
	print "Line number %i (%s) will become '%s'"%(item,cfin[item-1],newVals[item])
	if raw_input("Does this look ok?").lower() in ('','y'):
		if len(newVals[item].split('\t')[2])<2: print "There are no colours to add here anyway!"
		else: cfin[item-1]=newVals[item]+'\n'
	else: print "skipping...\n"
if raw_input("Finished editing. Are you sure you want to write changes to Chars.csv? This is final. It is recommended that you backup first!!!").lower() in ('','y'):
	fout=codecs.open('chars.csv',encoding='UTF-8',mode='wb')
	fout.write(''.join(cfin))
	fout.close
print 'Success. Have a nice day.'*int(fout.closed)
quit()