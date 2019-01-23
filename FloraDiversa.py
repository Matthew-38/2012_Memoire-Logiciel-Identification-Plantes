# encoding: UTF-8
'''(Re)Written on 22 June 2012 by Matthew O'Toole'''
Term,PlantProfiles,GUI,divisorsList,Imported,Settings=[{},{}],{},[],[],False,{'log mode':'f','name':'Flora Diversa','mode file':'language.csv','language':1,"colour strictness":255,"dependency":"Status Bar Only","error tolerance":2}
#Possible Settings# dependency: "Dependency Notification", "Status Bar Only", "Disable Dependencies"; "error tolerance":0-999; "log mode":'t','f','tf'; "colour strictness":0-764
try:
    # for Python2
    from Tkinter import *
    import tkColorChooser, tkFont
    import tkMessageBox as MsgBox
    from tkFileDialog import askopenfilename,asksaveasfilename
except ImportError:
    # for Python3
    from tkinter import *
    import tkinter.colorchooser as tkColorChooser
    import tkinter.font as tkFont
    import tkinter.messagebox as MsgBox
    from tkinter.filedialog import askopenfilename,asksaveasfilename
    unicode=str  # In Python 3, there is one and only one string type. Its name is str and it's Unicode. This line is to make it compatible with Python 2, which has two types. See line 351
import codecs, random,re, time
from os import walk
from subprocess import call #For windows: Change this to os.startfile
from PIL import Image, ImageTk #@UnresolvedImport @Reimport
from operator import attrgetter
class SettingsMgr():
	def __init__(self,filename='settings.txt'):
		try:
			fin=codecs.open(filename, 'r', encoding='UTF-8')
			for line in fin:
				if line.split(':')[0] in Settings and ':' in line:
					Settings[line.split(':')[0]]=line.split(':')[1].strip()
			fin.close()
			global Imported
			Imported=True
		except IOError: pass
	def window(self):
		self.rt=Toplevel()
		self.rt.title(Settings["name"]+"- Settings")
		self.rt.wm_attributes("-topmost",1)
		self.colSt=IntVar()
		self.colSt.set(Settings["colour strictness"])
		Scale(self.rt,variable=self.colSt,relief="solid",to=0,from_=764,label="Colour Error Tol.",command=self.updatecolSt).grid(column=1,row=1,rowspan=3,columnspan=2,sticky='nesw')
		self.ColEx=[Label(self.rt,text="Max"),Label(self.rt,text="Control", bg='#888888'),Label(self.rt,text="Min")]
		for i in range(3): self.ColEx[i].grid(column=3,row=i+1,sticky='nesw')
		def cgCol(*event): 
			self.ColEx[1].config(bg=tkColorChooser.askcolor(color=self.ColEx[1].cget("bg"),title="Choose Control Colour")[1])
			self.updatecolSt(event=self.colSt.get())
		self.ColEx[1].bind("<Button-1>",cgCol)
		self.errTol=IntVar(); self.errTol.set(Settings["error tolerance"])
		Scale(self.rt,variable=self.errTol,orient='horizontal',relief="solid",to=99,label="Plant Error Tol.").grid(column=1,row=4,rowspan=2,columnspan=3,sticky='nesw')
		self.notifyVar=StringVar(); self.notifyVar.set(MasterCharacters.depEff.get())
		Label(self.rt,text="Dependency Notification",wraplength=100).grid(column=1,row=7,rowspan=2,sticky='nesw')
		for i,t in [(7,"Dependency Notification"),(8,"Status Bar Only"),(9,"Disable Dependencies")]:Radiobutton(self.rt,value=t,text=t,variable=self.notifyVar).grid(column=2,row=i,columnspan=2,sticky='nsw')
		Button(self.rt,text="Set",command=self.setAllOpt).grid(column=1,row=10,sticky='nesw')
		Button(self.rt,text="Save",command=self.setNsave).grid(column=2,row=10,sticky='nesw')
		Button(self.rt,text="Close",command=self.rt.destroy).grid(column=3,row=10,sticky='nesw')
	def updatecolSt(self,event):
		dif=int(event)//3
		col=[int(self.ColEx[1].cget('bg')[1:3],16),int(self.ColEx[1].cget('bg')[3:5],16),int(self.ColEx[1].cget('bg')[5:7],16)]
		self.ColEx[0].config(bg="#"+''.join([hex(min(255,col[i]+dif))[2:].zfill(2) for i in range(3)]))
		self.ColEx[2].config(bg="#"+''.join([hex(max(0,col[i]-dif))[2:].zfill(2) for i in range(3)]))
	def setAllOpt(self,*event):
		for opt,val in [("colour strictness",self.colSt.get()),("error tolerance",self.errTol.get()),("dependency",self.notifyVar.get())]:Settings[opt]=val
		MasterCharacters.depEff.set(self.notifyVar.get())
	def setNsave(self,*event):
		self.setAllOpt(); self.saveSettings()
	def setOpt(self, opt, val): Settings[opt]=val
	def saveSettings(self,filename='settings.txt'):
		fout=codecs.open(filename, 'w+', encoding='UTF-8')
		fout.write('Settings file for %s. Possible options include: '%Settings['name']+', '.join([opt for opt in Settings]))
		for opt in Settings: fout.write(u"\n%s:%s"%(opt,Settings[opt]))
		fout.close()
		if fout.closed: Logger.log('Settings saved to file %s correctly'%filename)
SetMgr=SettingsMgr()
class LogManager():
	def __init__(self):
		if 'f' in Settings['log mode']:		
			try: 
				fin=codecs.open('log.txt', 'r', encoding='UTF-8')
				date=fin.readline()
				if int(time.localtime().tm_mon)!=int(date.split('-')[1]): raise Exception('Outdated File')#Clear file
				fin.close()
			except (IOError,Exception):
				try :fin.close()
				except:pass
				fout=codecs.open('log.txt', 'w+', encoding='UTF-8')
				dt=time.localtime()
				fout.write(u'%s Log File. Automatically generated on %s-%s-%s at %s:%s:%s'%(Settings['name'],dt.tm_year,dt.tm_mon,dt.tm_mday,dt.tm_hour,dt.tm_min,dt.tm_sec))
				fout.write(u'\nThis file is automatically generated and updated by %s and gets deleted/replaced every month (to limit the size).\n%s\n'%(Settings['name'],'*'*50))
				fout.close()
			dt=time.localtime()
			fa=codecs.open('log.txt', 'a+', encoding='UTF-8')
			fa.write(u'\n%s\n%s Log Date: %s-%s-%s at %s:%s:%s\n%s\n\n'%('*'*50,Settings['name'],dt.tm_year,dt.tm_mon,dt.tm_mday,dt.tm_hour,dt.tm_min,dt.tm_sec,'*'*50))
			if 'f' not in Settings['log mode']: fa.write(u'Logging settings disabled\n')
			if Imported:fa.write(u'Settings file imported\n')
			fa.close()
	def log(self,*txt):
		if len(txt)>1:txt=' '.join(txt)
		else: txt=txt[0]
		if 't' in Settings['log mode']: print(txt)
		if 'f' in Settings['log mode']:
			fa=codecs.open('log.txt', 'a+', encoding='UTF-8')
			fa.write(txt+'\n')
			fa.close()
Logger=LogManager()
class BaseWindow(Frame):
	def __init__(self, master=None):
		Frame.__init__(self, master)
		self.grid()
root=Tk()
root.title(Settings["name"].strip())
italic=tkFont.Font(root=root,family="system",size="8",slant="italic");small=tkFont.Font(family="Arial",size='6');bold=tkFont.Font(root=root,family="Arial",size="8",weight='bold')
class ExtraFunctions():
	'''Contained functions include: stripList(lst, item=(' ,\n'))\n is_float(strIn)\n'''
	def __init__(self):
		try:
			fin=codecs.open(Settings['mode file'], 'r', encoding='UTF-8')
			i=0
			for line in fin:
				data=line.strip().split('\t')
				if data[0] in Term[0]: Logger.log("Error in file [%s] on line %i - contains duplicate entry for %s"%(Settings['mode file'],i,data[0]))
				else:Term[0][data[0]]=data
				i+=1
		except IOError as error: Logger.log("The following error was encountered while trying to load %s\n%s"%(Settings['mode file'],str(error)))
	def importFileList(self,folder):
		fileList=[]
		for root, dirs, files in walk(top=folder, topdown=True): #@UnusedVariable
			for i in range(len(files)): fileList.append(root+'/'+files[i])
		return fileList
	def stripList(self, lst, item=(' ,\n')):
		newLst=[]
		for thing in lst:
			newLst.append(thing.strip(item))
		return newLst
	def is_float(self, strIn):
		try:
			float(strIn)
			return True
		except ValueError:
			return False
	def compareFloats(self, f1, f2, sign):
		f1=float(f1); f2=float(f2)
		if sign=='>' and f1>f2:return True
		if sign=='<' and f1<f2: return True
		elif f1==f2: return True
		return False
	def profileReader(self,filename,avoidHash=True):
		fin=codecs.open(filename, encoding='UTF-8')
		linez,cf, sspp={},{},{}#@ToDO: add more for other things that can be multiple, like common names in english
		lines=fin.read().split('\n')
		Logger.log( "importing %s"%filename)
		for line in lines:
			try:
				if '#' in line or len(line)<4: pass #Don't need to do anything here!
				elif 'Similar Plants' in line: #@type: cf=[sp2]=what is different in sp2
					if 'none' not in line.lower(): 
						for i in range(0,len(line.split('\t')[1].split(',')),2): cf[line.split('\t')[1].split(',')[i].strip()]=line.split('\t')[1].split(',')[i+1].strip()
				elif 'Subspecies' in line: #@type: sspp[n]=details
					if 'none' not in line.lower(): 
						for i in range(0,len(line.split('\t')[1].split(',')),2): sspp[line.split('\t')[1].split(',')[i].strip()]=line.split('\t')[1].split(',')[i+1].strip()
				else: linez[line.split('\t')[0]]=self.stripList(line.split('\t')[1].split(','))
			except: 
				Logger.log("Error on line %s in file %s! Check capitalisation, commas and spacing (tabs). Error details:\n"%(line,filename))
				raise
		return linez,cf,sspp
	def appendErrorTerm(self,term, fileName='UnknownChars.txt'):
		fin=codecs.open(fileName, encoding='UTF-8')
		for line in fin:
			if term in line: return 0
		fapp=codecs.open(fileName, encoding='UTF-8', mode='a')
		fapp.write(term+'\n')
		fapp.close()
		return 'done'+term
	def importProfile(self):
		GUI[3].statusSet('Loading file...')
		if MsgBox.askyesno("Confirm Setting Replacement", "Do you really want to import a .csv file and replace any altered settings?"):
			MasterCharacters.resetAllChars()
			MsgBox.showwarning("File Type Warning","Please select only a valid plant profile in the following dialog.\nElse the programme may experience unexpected errors and will have to restart!")
			filename=askopenfilename(title='Import File',parent=root,initialdir="",defaultextension=".csv",filetypes=[('Plant Profiles', '.csv'),('All Files', '.*')])
			if filename.split('.')[-1]!='csv': MsgBox.showwarning("Invalid File Format", "This is not a valid file. Importing non-profile files can cause unexpected errors!")
			else:
				MsgBox.showinfo("Limited Scope", "The file %s will now import, setting options where possible.\n\nHowever, due to the possibility of the file having more than one acceptable alternative per character, only the first alternative will be set.\n(his does not affect the file itself unless you export!)"%filename)
				GUI[3].statusSet('File loaded.')
				fin=codecs.open(filename,encoding='UTF-8')
				for line in fin:
					if '#' not in line and len(line)>2:
						MasterCharacters.setChar(line.split('\t')[0],self.stripList(line.split('\t')[1].split(',')))
				MasterCharacters.updateDivs()
		GUI[3].statusSet('Ready')
	def wheelBinder(self,items):
		for item in items:
			item.bind('<4>', CharFrame.rollWheel)
			item.bind('<5>', CharFrame.rollWheel)
			item.bind('<MouseWheel>', CharFrame.rollWheel)
	def updateAffVals(self,possLstItems, grp): #@type possLstItems: These are profiles, not names 
		for char in grp:
			results=[0,0,0,0]
			for plant in PlantProfiles:
				if char in PlantProfiles[plant].data:
					results[3]+=1
					if plant in [pos.name for pos in possLstItems]: results[1]+=1
					for val in grp[char].val.get().split(';'):
						if val in PlantProfiles[plant][char]: 
							results[2]+=1
							if plant in [pos.name for pos in possLstItems]: results[0]+=1
			grp[char].inst.affVar.set("%i(%i)/%i(%i)"%tuple(results))
	def getCol(self, colour):
		if colour=='unsure': return '#000000'
		if colour[0]!='#' and len(colour) in (6,3):return '#'+colour
		return colour
class PlantProfile(object):
	'''Stores the information of Plant Profiles. Input tuple of dictionaries/lists - the first is a dict for general data'''
	def __init__(self, dataIn):
		self.name,self.genus,self.species='','',''
		self.data={}
		self.cf,self.sspp=dataIn[1],dataIn[2]
		self.score0=0
		self.score1=0
		self.mismatches=[]
		self.massLoadData(dataIn[0])
	def massLoadData(self, dictIn):
		for item in dictIn.keys():
			self.data[item]=dictIn[item]
		self.loadName(self.data['Name'])
		self.setImages()
	def loadName(self,name):
		self.name=name[0]
		self.genus=name[0].split()[0]
		self.species=name[0].split()[1]
	def setImages(self):
		self.data['Images']=[]
		for posImg in EXT.importFileList('PlantProfiles'):
			if '_'.join(self.name.split()) in posImg and posImg.split('.')[-1].lower()=='jpg':
				self.data['Images'].append(posImg)
	def checkChars(self):
		for item in self.data:
			if item in MasterCharacters.dbl:
				for val in self.data[item]:
					if val not in MasterCharacters.dbl[item].posValues:
						EXT.appendErrorTerm(term="%s\t%s"%(item,val))
			elif item in MasterCharacters.mlt:
				for val in self.data[item]:
					if val not in MasterCharacters.mlt[item].posValues:
						EXT.appendErrorTerm(term="%s\t%s"%(item,val))
			elif item in MasterCharacters.int: pass
			else: EXT.appendErrorTerm(term="%s\t%s"%(item,str(self.data[item])))
	def __getitem__(self, *key):
		if key[0]=='score0':return self.score0 #@note: This is done for easy access, don't be confused; score[x] is NOT stored in self.data!!!
		elif key[0]=='score1':return self.score1
		else: return self.data[key[0]]
	def __setitem__(self, key, value, *otheropts):
		if key=='score0':self.score0=value #@note: This is done for easy access, don't be confused; score[x] is NOT stored in self.data!!!
		elif key=='score1':self.score1=value
		else:self.data[key]=value
	def __repr__(self, *args, **kwargs):
		return "<Plant Profile for %s:\n %s" %(self.name,str(self.data))

############################################################################################################################
EXT=ExtraFunctions()
class ScrlFrame(object): #frame: [ScrlFrame].subFrm
	'''A container Frame in a window of a canvas, at grid(x,y)'''
	def __init__(self, grd=(0,2)):
		self.cnv=Canvas(root, bg='#eee', height=500, width=450)
		self.cnv.grid(column=grd[0], columnspan=10, row=grd[1], rowspan=50, sticky='nesw')
		self.vscrl=Scrollbar(root, command=self.cnv.yview)
		self.vscrl.grid(column=grd[0]+10, row=grd[1], rowspan=50, sticky='ns')
		self.cnv.config(yscrollcommand=self.vscrl.set)
		self.subFrm=Frame(self.cnv)
		self.cnv.create_window(0,0,window=self.subFrm, width=450, anchor='nw')
		self.update()
		self.vscrl.bind('<4>', self.rollWheel)
		self.vscrl.bind('<5>', self.rollWheel)
		self.span=Label(self.subFrm,text="Plant Identification Characters",width=60,bg="#c2c899")
		self.span.grid(column=0,row=0,columnspan=6,sticky='nesw')
	def rollWheel(self,event):
		if event.num == 4 and self.vscrl.get()[0]>0:
			self.cnv.yview('scroll', -1, 'units')
			self.vscrl.set(self.vscrl.get()[0]+0.1,self.vscrl.get()[1]+0.1)
		elif event.num == 5 and self.vscrl.get()[1]<1:
			self.cnv.yview('scroll', 1, 'units')
			self.vscrl.set(self.vscrl.get()[0]-0.1,self.vscrl.get()[1]-0.11)
	def update(self):
		self.subFrm.update_idletasks()
		self.cnv.config(scrollregion=(0,0,self.subFrm.winfo_width(), self.subFrm.winfo_height()))
CharFrame=ScrlFrame(grd=(0,1))
DEFBG=CharFrame.vscrl.cget('bg')
class ToolTip(object):
	'''Generates a tooltip box'''
	def __init__(self, widget):
		self.widget = widget
		self.tipwindow = None
		self.id = None
		self.x = self.y = 0
	def showtip(self, text,img, tag):
		"Display text in tooltip window using a StringVar as text"
		self.text=StringVar()
		if type(text) in (str,unicode): self.text.set(text)
		else: self.text=text
		if self.tipwindow or not self.text.get(): return
		#x, y, cx, cy = self.widget.bbox(tag); #@UnusedVariable cx
		#x+= self.widget.winfo_rootx()+27
		#y+= cy + self.widget.winfo_rooty() +47
		self.tipwindow = tw = Toplevel(self.widget)
		tw.wm_overrideredirect(1)
		tw.wm_attributes("-topmost",1)
		tw.wm_geometry("+%d+%d" % (9999, 0))#normally x,y
		try:tw.tk.call("::tk::unsupported::MacWindowStyle","style", tw._w,"help", "noActivates")# For Mac OS
		except TclError:pass
		label = Label(tw, text=self.text.get(), textvariable=self.text,wraplength=250, justify=LEFT,background="#ffffe0", relief="raised", borderwidth=1,font=("tahoma", "8", "normal"))
		label.grid(column=0,row=0,sticky='nesw')#pack(ipadx=1)
		if img:
			ca=Canvas(tw,width=300,height=300,bg='#ffffe0')
			ca.grid(column=0,row=1)
			self.img=PhotoImage(file=img)
			ca.create_image(150,150,image=self.img,anchor='c')
			label.config(wraplength=300)
	def updatePos(self,event):
		if self.tipwindow:self.tipwindow.wm_geometry("+%d+%d" % (event.x_root+17, event.y_root+17))
	def hidetip(self):
		tw = self.tipwindow
		self.tipwindow = None
		if tw: tw.destroy()
class ToolTipManager():
	def procTxt(self,txt):
		strOut=StringVar()
		strOut.set(txt)
		for plant in PlantProfiles:
			if plant in txt and plant != txt: 
				strOut.set(', '.join(PlantProfiles[plant]["Common Name"]))
				return strOut
		if txt in Term[0] and len(Term[0][txt])>2: strOut.set(Term[0][txt][max(2,int(Settings["language"])+1)])
		else: EXT.appendErrorTerm(txt, "UndefinedToolTips.txt")
		return strOut #if above fails
	def makeTT(self,w,txt=None,img=None):
		if not txt: txt=w.cget("text")
		toolTip = ToolTip(w)
		def enter(event):
			if 'IMG' in self.procTxt(txt).get(): toolTip.showtip(self.procTxt(txt).get().split(';')[1],img=self.procTxt(txt).get().split(';')[0].split(':')[1], tag='insert')
			else: toolTip.showtip(self.procTxt(txt),img, 'insert')
		def leave(event):toolTip.hidetip()
		w.bind('<Enter>', enter)
		w.bind('<Leave>', leave)
		w.bind('<Motion>', toolTip.updatePos)
		return toolTip
	def makeMenuTT(self,w,txt=None,img=None):
		txtz=[]
		if txt:txtz=txt
		else: 
			for i in range(w.index('end')+1):
				if w.type(i)=='separator':txtz.append('')
				else: txtz.append(w.entrycget(i,'label'))
		if type(txtz) in (unicode,str):txtz=[txtz]
		toolTip = ToolTip(w)
		def enter(event,i):
			leave(event)
			if i!='none' and int(i) in range(len(txtz)):
				if 'IMG' in self.procTxt(txtz[int(i)]).get(): toolTip.showtip(self.procTxt(txtz[int(i)]).get().split(';')[1],img=self.procTxt(txtz[int(i)]).get().split(';')[0].split(':')[1], tag='insert')
				else: toolTip.showtip(self.procTxt(txtz[int(i)]),img, 'insert')
		def leave(event):toolTip.hidetip()
		def sbu(event):
			#Logger.log( txtz, root.call(event.widget, "index", "active"))
			enter(event,root.call(event.widget, "index", "active"))
		w.bind("<<MenuSelect>>",sbu, add=True)
		w.bind('<Leave>', leave, add=True)
		w.bind('<Unmap>', leave, add=True)
		w.bind('<Motion>', toolTip.updatePos, add=True)
		return toolTip
	def makeListTT(self,w,txt=None,img=None):
		if txt:txtz=[t for t in txt]
		else: txtz=list(w.get(0,'end'))
		toolTip = ToolTip(w)
		def leave(event):toolTip.hidetip()
		def enter(event):
			leave(event)
			if w.size()>w.nearest(event.y):
				toolTip.showtip(self.procTxt(txtz[w.nearest(event.y)]),img, 'insert')
				if 'IMG' in self.procTxt(txtz[w.nearest(event.y)]).get(): toolTip.showtip(self.procTxt(txtz[w.nearest(event.y)]).get().split(';')[1],img=self.procTxt(txtz[w.nearest(event.y)]).get().split(';')[0].split(':')[1], tag='insert')
				else: toolTip.showtip(self.procTxt(txtz[w.nearest(event.y)]),img, 'insert')
				toolTip.updatePos(event)
		w.bind('<Leave>', leave)
		w.bind('<Enter>', enter)
		w.bind('<Motion>', enter)
		return toolTip
ttMgr=ToolTipManager()
class Exporter():
	def __init__(self):
		GUI[3].statusSet("Exporting file...")
		self.editQ,self.filename,self.UnsureQ=IntVar(),StringVar(),IntVar()
		self.rt=Toplevel()
		self.rt.wm_attributes("-topmost",1)
		self.rt.grid()
		self.rt.title("%s - Export to CSV file"%Settings['name'])
		self.hlp=Message(self.rt, aspect=100,width=180,relief='groove',bd=4,textvariable=getTradStrVar("File Exporter:\nComplete the options opposite, values separated by commas (',') and click on Export to save them to a '.CSV' file.\nNote: not all options are possible (yet). The file will need editing afterwards!"))
		self.hlp.grid(column=0,row=2,rowspan=10,columnspan=2,sticky='nes')
		self.optNames=['Name','Common Name','Frequency','Subspecies','Data Source(s)','Similar Plants','Native Status','Soil Preference',"Description"]
		self.options=[]
		i=0
		for text in self.optNames:
			self.options.append(StringVar())
			self.options.append(Label(self.rt,justify='right',textvariable=getTradStrVar(text)))
			self.options[-1].grid(column=2,row=2+i,sticky='nes')
			self.options.append(Entry(self.rt,textvariable=self.options[i*3], width=20,bg='white'))
			self.options[-1].grid(column=3,row=2+i,sticky='nesw')
			i+=1
		self.chkUnsureQ=Checkbutton(self.rt, textvariable=getTradStrVar("Include unset options?"),indicatoron=1,variable=self.UnsureQ)
		self.chkUnsureQ.grid(column=2,row=11,columnspan=2,sticky='nesw')
		self.filenameLa=Label(self.rt,textvariable=getTradStrVar("Export Filename"))
		self.filenameLa.grid(column=0,row=12,sticky='nesw')
		self.filenameInput=Entry(self.rt, width=20, textvariable=self.filename,bg='white')
		self.filenameInput.grid(column=1,row=12,columnspan=2,sticky='nesw')
		self.filenameInput.bind('<Button-1>', self.dfltFileName)
		self.browseBu=Button(self.rt,textvariable=getTradStrVar("Browse"),command=self.browse)
		self.browseBu.grid(column=3,row=12,sticky='nesw')
		self.excelEditQ=Checkbutton(self.rt, textvariable=getTradStrVar("Edit File as spreadsheet when done?"),indicatoron=1,variable=self.editQ)
		self.excelEditQ.grid(column=1,row=13,columnspan=2,sticky='nesw')
		self.expBu=Button(self.rt,textvariable=getTradStrVar("Export"),command=self.export)
		self.expBu.grid(column=3,row=13,sticky='nesw')
		self.rt.bind("<Destroy>",self.onEnd)
	def export(self,*dmp):
		proc=1
		if not self.filename.get():
			MsgBox.showinfo("Missing Filename", "Because there was no filename entered, it will now default and be saved in the usr directory")
			proc=self.dfltFileName()
		if len(self.options[0].get().split(' '))!=2:
			MsgBox.showerror("Invalid Botanic Name", "Please enter a valid Botanic name [Genus species] first!")
			proc=0
		if proc:
			expStr="#Exported File. Depending on how you exported this file, it may need extensive editing. Make sure it is usable before copying it to PlantProfiles/ directory. Any lines without # must be complete in the following format: text [tab] text (=%s\t%s\n). Lines with a '#' in them are ignored. It is safe to remove this line. \n"
			for div in divisorsList:
				expStr+="\n#%s\n"%div.name
				for menu in div.dbls:
					if menu.selection.get() in ['unsure','']:
						if self.UnsureQ.get(): expStr+="%s\t%s# TODO: Edit/choose\n"%(menu.label,','.join(MasterCharacters.dbl[menu.label].posValues[1:]))
					else: expStr+="%s\t%s\n"%(menu.label,menu.selection.get())
				for menu in div.ints:
					if menu.selection.get() in ['',0,'0']:
						if self.UnsureQ.get(): expStr+="%s\t# TODO: Enter [min],max values here\n"%menu.label
					else: expStr+="%s\t%s\n"%(menu.label,menu.selection.get())
				for menu in div.mlts:
					if menu.selection.get() in ['unsure','']:
						if self.UnsureQ.get(): expStr+="%s\t%s# TODO: Edit/choose\n"%(menu.label,','.join(MasterCharacters.mlt[menu.label].posValues[1:]))
					else: expStr+="%s\t%s\n"%(menu.label,','.join(menu.selection.get().split(';')))
			expStr+="#Misc\n"
			for i in range(len(self.options[0::3])):
				expStr+="%s\t%s\n"%(self.optNames[i],self.options[i*3].get())
			fout=codecs.open(self.filename.get(), mode='w', encoding='UTF-8')
			fout.write(expStr)
			fout.close()
			if fout.closed:
				openexcel=''
				if self.editQ.get(): openexcel="\nNow attempting to open the file in Excel/Calc for editing..."
				MsgBox.showinfo("Export Successful", "File Exported to %s successfully.%s"%(self.filename.get(),openexcel))
				if self.editQ.get():
					try:call(["xdg-open",self.filename.get()])
					except: 
						try: os.startFile(self.filename.get()) #If Windows. Need to use different import!!! @UndefinedVariable
						except: Logger.log("Failed to open file: %s\n"%self.filename.get())
				self.rt.destroy()
			else: MsgBox.showerror("I/O Failure", "Failed to write file. Something went wrong. Check that the file doesn't already exist and that the location is writable!")
	def onEnd(self,*dmp): GUI[3].statusSet("Ready")
	def dfltFileName(self, *dmp):
		if len(self.options[0].get().split(' '))==2:
			self.filename.set("usr/%s_%s.csv"%(self.options[0].get().split(' ')[0].title(),self.options[0].get().split(' ')[1].lower()))
			return 1
		MsgBox.showerror("Invalid Botanic Name", "Please enter a valid Botanic name [Genus species] first!")
		return 0
	def browse(self,*dmp):
		self.filename.set(asksaveasfilename(title='Export File',parent=self.rt,initialfile=self.filename.get().split('/')[-1],initialdir="usr/",defaultextension=".csv",filetypes=[('Plant Profiles', '.csv'),('all files', '.*')]))
########Declarations########
class Pview():
	'''A toplevel to desplay all plant information'''	
	def __init__(self, pname):
		self.rt=Toplevel()
		self.rt.title("%s - Viewing: %s"%(Settings['name'],pname))
		self.rt.wm_attributes("-topmost",1)
		self.plant=PlantProfiles[pname]
		hab="undefined"
		if "Habitat" in self.plant.data:hab=', '.join(self.plant['Habitat'])
		self.curImg,self.genData,self.genMu,self.infoVar=StringVar(),StringVar(),StringVar(),StringVar()
		self.labels=[Label(self.rt,text=pname),Label(self.rt,text=', '.join(self.plant['Common Name']),relief='sunken'), Label(self.rt,textvariable=getTradStrVar('Habitat')), Label(self.rt,text=hab,relief='sunken'), Menubutton(self.rt,textvariable=self.genMu,relief='raised',width=20),Label(self.rt,textvariable=self.genData,relief='sunken')]
		for i in range(0,len(self.labels),2):
			self.labels[i].grid(column=1,row=2+i//2,sticky='nesw')
			self.labels[i+1].grid(column=3,row=2+i//2,columnspan=4,sticky='nesw')
			ttMgr.makeTT(self.labels[i],txt=self.labels[i].cget('text'))
		self.labels[0].config(font=italic)
		self.genMenu=Menu(self.labels[4],tearoff=0)
		self.plantChars=[item for item in self.plant.data]
		self.plantChars.sort()
		for i in range(len(self.plantChars)):
			self.genMenu.add_radiobutton(value=self.plantChars[i],label=self.plantChars[i],variable=self.genMu,command=self.muSel)
			if i%20==0:self.genMenu.entryconfig(i, columnbreak=1)
		self.labels[4].config(menu=self.genMenu)
		self.genMu.set("Characters")
		self.ftrLst=Listbox(self.rt,exportselection=0,bg='white')
		self.ftrLst.grid(column=1,row=6,columnspan=2,rowspan=5,sticky='nesw')
		self.ftrLst.insert(0,"Species Description")
		for item in self.plant.sspp.keys(): self.ftrLst.insert('end',"Subspecies: %s"%item)
		for item in self.plant.cf.keys(): self.ftrLst.insert('end',"Similar-plant: %s"%item)
		self.info=Message(self.rt,textvariable=self.infoVar,aspect=50,width=270)
		self.info.grid(column=3,row=6,columnspan=4,rowspan=7,sticky='new')
		self.cfBu=Label(self.rt,text="Compare this species with: ")
		self.cfBu.grid(column=0,row=14,columnspan=3,sticky='nesw')
		self.cfSelected=StringVar();self.cfSelected.set('None')
		self.cfMenuBu=Menubutton(self.rt, textvariable=self.cfSelected,relief='raised')
		self.cfMenu=Menu(self.cfMenuBu, tearoff=0)
		for item in sorted([item for item in PlantProfiles.keys()]):
			if item!=pname:self.cfMenu.add_radiobutton(value=item,label=item,variable=self.cfSelected,command=self.updateCF)
		self.cfMenuBu.grid(column=3,row=14,columnspan=1,sticky='nesw')
		self.cfMenuBu.config(menu=self.cfMenu)
		self.cfBoxes=[]
		self.vscrlCF=Scrollbar(self.rt,command=self.yview)
		self.vscrlCF.grid(column=6,row=15,rowspan=3,sticky='nes')
		for i in range(3):
			self.cfBoxes.append(Listbox(self.rt,bg="white",yscrollcommand=lambda e1,e2, i=i,self=self, *args:self.yscroll((e1,e2),i=i),exportselection=0))
			self.cfBoxes[i].grid(column=i*2,row=15,rowspan=3, columnspan=2,sticky='nesw')
			hscrl=Scrollbar(self.rt,command=self.cfBoxes[i].xview,orient='horizontal')
			hscrl.grid(column=i*2,row=18,columnspan=2,sticky='new')
			self.cfBoxes[i].config(xscrollcommand=hscrl.set)
			self.cfBoxes[i].bind("<ButtonRelease-1>",lambda event=None,self=self,i=i:self.updateCFSel(i))
		self.buPrev=Button(self.rt,text="<<",command=lambda event=None,self=self,dr=-1:self.cngImg(event,dr))
		self.imgTtl=Label(self.rt,textvariable=self.curImg,relief='sunken')
		self.buNext=Button(self.rt,text=">>",command=lambda event=None,self=self,dr=1:self.cngImg(event,dr))
		self.buPrev.grid(column=8,row=1,sticky='nesw')
		self.imgTtl.grid(column=10,row=1,columnspan=16,sticky='nesw')
		self.buNext.grid(column=27,row=1,sticky='nesw')
		self.canv=Canvas(self.rt,width=500,height=500,bg='grey')
		self.canv.grid(column=8,row=2,columnspan=20,rowspan=22,sticky='nesw')
		self.ftrLst.bind("<Button-1>",self.lstSel)
		self.lstSel(event=None,i=0)
		self.imgTtl.bind("<Button-1>", self.openImg)
		self.setImg()
		ttMgr.makeMenuTT(self.genMenu)
	def yview(self,*args):
		for i in range(3): apply(self.cfBoxes[i].yview, args)
	def yscroll(self,args,i):
		for box in self.cfBoxes:
			if box.yview() != self.cfBoxes[i].yview():
				box.yview_moveto(args[0])
				self.vscrlCF.set(*args)
		self.updateCFSel(i)
	def updateCFSel(self, i):
		sel=self.cfBoxes[i].curselection()
		if len(sel)==1:
			for box in self.cfBoxes:
				box.selection_clear(0,END)
				box.selection_set(sel[0])
	def updateCF(self):
		for i in range(3):
			self.cfBoxes[i].delete(0,'end')
		lst1,lst2={},{}
		p2=PlantProfiles[self.cfSelected.get()]
		for item in self.plant.data:
			if item in lst1: Logger.log("Error found in comparing data. Debug Info: "+item) 
			else: 
				lst1[item]=[', '.join(self.plant[item])]
				if item in p2.data: lst1[item].append(', '.join(p2[item]))
				else:lst1[item].append("undefined")
		for item in p2.data:
			if item not in lst1:lst2[item]=["undefined",', '.join(p2[item])]
		i,cols=0,['#50a8f8','#3470d8','#90dc68','#b0e46c']
		ord1=[item for item in lst1.keys()]
		ord1.sort();
		ord1.insert(0, ord1.pop(ord1.index('Name')))
		ord1.insert(1, ord1.pop(ord1.index('Common Name')))
		for item in ord1:
			for txt,j in [(item,0),(lst1[item][0],1),(lst1[item][1],2)]:
				self.cfBoxes[j].insert('end', txt)
				self.cfBoxes[j].itemconfig('end',bg=cols[i%2])
			if str(lst1[item][0])==str(lst1[item][1]): 
				self.cfBoxes[1].itemconfig('end',fg='green')
				self.cfBoxes[2].itemconfig('end',fg='green')
			i+=1
		ord2=[item for item in lst2.keys()]
		ord2.sort();
		for item in ord2:
			for txt,j in [(item,0),(lst2[item][0],1),(lst2[item][1],2)]:
				self.cfBoxes[j].insert('end', txt)
				self.cfBoxes[j].itemconfig('end',bg=cols[2+i%2])
			if lst2[item][0]==lst2[item][1]: 
				self.cfBoxes[1].itemconfig('end',fg='green')
				self.cfBoxes[2].itemconfig('end',fg='green')
			i+=1
		for j in range(3):
			self.cfBoxes[j].itemconfig(0,bg='#FFF',fg="#000")
			self.cfBoxes[j].itemconfig(1,bg='#FFF',fg="#000")
	def muSel(self,*dmp):self.genData.set(", ".join(self.plant[self.genMu.get()]))
	def lstSel(self,event,i=None): 
		if i==None:i=self.ftrLst.nearest(y=event.y)
		self.ftrLst.selection_clear(0,'end')
		self.ftrLst.select_set(i)
		selLine=self.ftrLst.get(i).split(' ',1)[1]
		self.info.config(bg='grey')
		if selLine in self.plant.cf: self.infoVar.set(self.plant.cf[selLine])
		elif selLine in self.plant.sspp: self.infoVar.set(self.plant.sspp[selLine])
		else: self.infoVar.set(", ".join(self.plant['Description']))
	def cngImg(self,event,dr):
		i=dr+self.plant["Images"].index(self.curImg.get())
		if i>=len(self.plant["Images"]): i=0
		self.setImg(i)
	def setImg(self,i=0):
		if len(self.plant["Images"])>0: 
			self.curImg.set(self.plant["Images"][i])
			self.img=Image.open(self.curImg.get())
			self.img.thumbnail((500,500))
			self.img=ImageTk.PhotoImage(self.img)
			self.canv.create_image(250,250,image=self.img, anchor='c')
	def openImg(self,*dmp):
		try:call(["xdg-open",self.curImg.get()])
		except: 
			try: os.startFile(self.curImg.get()) #If Windows. Need to use different import!!! @UndefinedVariable
			except: Logger.log("Failed to open file: %s\n"%self.curImg.get())
class selGuide():
	''''''
	def __init__(self, parent, charName, posVals,imgs=None,msg='Click image to select character. Right click to cycle images (if possible)'):
		self.parent,self.charName,self.posVals,self.imgs=parent,charName,posVals,imgs
		self.selected=StringVar(); self.selected.set(parent.selection.get())
		self.rt=Toplevel(master=root)
		self.rt.title("%s - %s"%(Settings["name"],charName))
		self.rt.wm_attributes("-topmost",1)
		self.msg=Message(self.rt,bg='grey',width=500,aspect=250,text=msg)
		self.msg.grid(column=1,row=1,columnspan=4,rowspan=2,sticky='nesw')
		self.okBu=Button(self.rt,textvariable=getTradStrVar("Okay"),command=self.closeSaving)
		self.okBu.grid(column=5,row=1,sticky='nesw')
		self.cnclBu=Button(self.rt,textvariable=getTradStrVar("Cancel"), command=lambda event=None, self=self:self.rt.destroy())
		self.cnclBu.grid(column=5,row=2,sticky='nesw')
		self.optz=[[],[],[]]
		for i in range(len(posVals)):
			self.optz[0].append(Canvas(self.rt,width=150,height=125))
			self.optz[0][i].grid(column=1+i%5, row=3+(i//5)*2, sticky='nesw')
			self.optz[1].append(None)
			self.chImg(None, i, rand="off")
			self.optz[2].append(Radiobutton(self.rt,value=posVals[i],text=posVals[i],variable=self.selected))
			self.optz[2][i].grid(column=1+i%5, row=4+(i//5)*2, sticky='nesw')
			self.optz[0][i].bind("<Button-1>",lambda event, i=i,self=self:self.selected.set(self.posVals[i]))
			self.optz[0][i].bind("<Button-3>",lambda event ,i=i,self=self:self.chImg(event,i)) 
	def chImg(self,event, optInd, rand="on"):
		if self.imgs: imgs=self.imgs[optInd]
		else:
			files=EXT.importFileList("GddChars/")
			imgs=[]
			for filename in files:
				if '-'.join(self.charName.split(' '))+"_"+'-'.join(self.posVals[optInd].split(' ')) in filename:imgs.append(filename)
		if len(imgs)>0:
			if rand=="on":imgFile=random.choice(imgs)
			else: imgFile=imgs[0]
			img=Image.open(imgFile)
			img.thumbnail((150,125))
			self.optz[1][optInd]=ImageTk.PhotoImage(img)
			self.optz[0][optInd].create_image(75,62,image=self.optz[1][optInd], anchor='c')
	def closeSaving(self,*dmp):
		self.rt.destroy()
		self.parent.selection.set(self.selected.get())
		MasterCharacters.testPlants()
class Help():
	def __init__(self,opt):
		self.rt=Toplevel(root,width=800, height=600)
		self.rt.title("%s - %s"%(Settings["name"],opt))
		filename={"Help":"Help/Readme.txt","Overview":"Help/Overview.txt","About":"Help/About.txt", "DIY":"Help/DIYguide.txt","Data Sources":"Help/Sources.txt", "Licence":"Help/Licence.txt"}[opt]
		fin=codecs.open(filename,encoding="UTF-8")
		txt=fin.read()
		if opt=="About":
			self.rt.wm_overrideredirect(1)
			self.rt.config(relief='ridge',bd=8)
			self.ca=Canvas(self.rt,width=150,height=150)
			self.ca.grid(row=1,column=2, columnspan=2)#,sticky='nesw')
			img=Image.open("Help/Logo.jpg")
			img.thumbnail((150,150))
			self.pimg=ImageTk.PhotoImage(img)
			self.ca.create_image(75,75,image=self.pimg,anchor="c")
			self.La=Label(self.rt,text='Beta "Irish Trees and Shrubs" version')
			self.La.grid(row=2,column=0,columnspan=6)
			self.msg=Text(self.rt,bg='#ebf8fe',relief='ridge',wrap='word',bd=4, width=40, height=10)
			Button(self.rt,text="Close",command=self.rt.destroy).grid(column=2,row=5, sticky='e')
		else:self.msg=Text(self.rt,bg='#ebf8fe',relief='ridge',wrap='word',bd=4, width=100, height=30)
		self.msg.grid(column=0, row=3,columnspan=6, sticky='nesw')
		self.scrlMsg=Scrollbar(self.rt, command=self.msg.yview)
		self.scrlMsg.grid(column=6, row=3, sticky='nesw')
		self.msg.insert(END, txt)
		self.msg.config(yscrollcommand=self.scrlMsg.set, state='disabled')
		self.msg.bind('<4>', self.rollWheel)
		self.msg.bind('<5>', self.rollWheel)
		self.scrlMsg.bind('<4>', self.rollWheel)
		self.scrlMsg.bind('<5>', self.rollWheel)
	def rollWheel(self,event):
		if event.num == 4 and self.scrlMsg.get()[0]>0:
			self.msg.yview('scroll', -1, 'units')
			self.scrlMsg.set(self.scrlMsg.get()[0]+0.1,self.scrlMsg.get()[1]+0.1)
		elif event.num == 5 and self.scrlMsg.get()[1]<1:
			self.msg.yview('scroll', 1, 'units')
			self.scrlMsg.set(self.scrlMsg.get()[0]-0.1,self.scrlMsg.get()[1]-0.11)
def getTradStrVar(strIn):
	if strIn in Term[0]:
		Term[1][strIn]=StringVar()
		if len(Term[0][strIn]) > int(Settings['language']): Term[1][strIn].set(Term[0][strIn][int(Settings['language'])])
		else: Term[1][strIn].set(Term[0][strIn][-1])
		#a=StringVar()
		#a.set(Term[1][strIn].get()+'1#')
		return Term[1][strIn]
	EXT.appendErrorTerm(term=strIn, fileName='UnknownTerm.txt')
	strOut=StringVar()
	strOut.set(strIn)
	return strOut
#####GUI Classes#########
class PossiblePlants():
	def __init__(self,c,r):
		self.colours=['green','orange','red']
		self.title=Label(master=root,textvariable=getTradStrVar("Possible Species"))
		self.title.grid(column=c,row=r,sticky='nesw')
		self.scrl=Scrollbar(master=root)
		self.scrl.grid(column=c+10, row=r+1, rowspan=20, sticky='nes')
		self.xscrl=Scrollbar(master=root)
		self.xscrl.grid(column=c, row=r+21, columnspan=11, sticky="new")
		self.box=Listbox(master=root, cursor='center_ptr', yscrollcommand=self.scrl.set, xscrollcommand=self.xscrl.set, width=23, selectmode='single', exportselection=0)
		self.box.grid(column=c, columnspan=10,row=r+1, rowspan=20, sticky='nesw')
		self.box.bind('<Button-1>',self.selectPlant)
		self.scrl.config(command=self.box.yview)
		self.xscrl.config(command=self.box.xview, orient=HORIZONTAL)
	def updateList(self):
		self.box.delete(0, END) #It doesn't matter about selection!
		self.candidates=[]
		for plant in PlantProfiles.keys():
			if PlantProfiles[plant].score1>=-int(Settings["error tolerance"]):
				self.candidates.append(PlantProfiles[plant])
		self.candidates=sorted(self.candidates, reverse=True,key=attrgetter("score1","score0"))
		for candidate in self.candidates:
			self.box.insert(END,"%s: (%i,%i)"%(candidate.name,candidate.score0,candidate.score1))
			if candidate.score1>=-2: self.box.itemconfig(END, background=self.colours[abs(candidate.score1)])
			else: self.box.itemconfig(END, background=self.colours[2])#in the event that the error tolerance is changed
		GUI[1].showMismatch()
		EXT.updateAffVals(possLstItems=self.candidates,grp=MasterCharacters.dbl)
		EXT.updateAffVals(possLstItems=self.candidates,grp=MasterCharacters.mlt)
		EXT.updateAffVals(possLstItems=self.candidates,grp=MasterCharacters.int)
		MasterCharacters.updateDivs()
		if self.box.size()>0:self.tt=ttMgr.makeListTT(self.box)
	def selectPlant(self,event):
		if self.box.size()>0:
			plantLine=self.box.get(self.box.nearest(y=event.y))
			GUI[1].loadPlant(plantLine.split(':')[0])
class PlantPreview(): 
	'''Preview Canvas and snippet data besides'''
	def __init__(self,c,r):
		self.adjLaCol=[]
		self.natSelection, self.natData,self.rotateSetting,self.mismatchVar=StringVar(),StringVar(),IntVar(),IntVar()
		self.natSelection.set('Ireland')
		self.plant,i,self.snippitStuff=None,0,[]
		self.canv=Canvas(master=root,bg='#E1E1E1', height=250, width=250)
		self.canv.grid(column=c+4,row=r,columnspan=15,rowspan=25,sticky='nw')
		for text in 'Plant','Common\nNames','Frequency','SubSpecies':
			self.snippitStuff.append(StringVar())
			self.snippitStuff.append(Label(root,textvariable=getTradStrVar(text)))
			self.snippitStuff[-1].grid(column=c,row=r+i,sticky='nesw')
			ttMgr.makeTT(self.snippitStuff[-1],txt=text)
			self.snippitStuff.append(Label(root,textvariable=self.snippitStuff[i*3],relief='sunken', width=20))
			self.snippitStuff[-1].grid(column=c+1,row=r+i, columnspan=3,sticky='nesw')
			i+=1
		self.snippitStuff[2].config(font=italic)
		self.snippitStuff[5].config(height=3)
		self.natMenuBu=Menubutton(master=root, textvariable=self.natSelection, relief='raised',state='disabled') #@TODO: need to update terminology settings here, but it's ok for now
		ttMgr.makeTT(self.natMenuBu,txt='Native Status')
		self.natMenu=Menu(master=self.natMenuBu, tearoff=0)
		self.natMenuBu.config(menu=self.natMenu)
		self.natFlags=[PhotoImage(file="Help/Ireland.gif"),PhotoImage(file='Help/Britain.gif')]
		self.natMenu.add_radiobutton(value="Ireland", image=self.natFlags[0], compound='center', indicatoron=1, variable=self.natSelection, command=self.updateNat)
		self.natMenu.add_radiobutton(value="Britain", image=self.natFlags[1], compound='center', indicatoron=1, variable=self.natSelection, command=self.updateNat)
		self.natMenuBu.grid(column=c,row=i+r,sticky='nesw')
		self.natDataLa=Label(master=root,textvariable=self.natData,relief='sunken')
		self.natDataLa.grid(column=c+1,row=i+r,columnspan=3,sticky='nesw')
		self.rotateCkBu=Checkbutton(master=root,state='disabled',textvariable=getTradStrVar("Cycle Images"),indicatoron=1,variable=self.rotateSetting,command=self.changeImage)
		self.rotateCkBu.grid(column=c,row=i+r+1,columnspan=4,sticky='nsw')
		ttMgr.makeTT(self.rotateCkBu,txt="Cycle Images")
		self.mismatchOpt=Checkbutton(master=root,state='disabled',textvariable=getTradStrVar("Highlight Mismatching Characters"),indicatoron=1,variable=self.mismatchVar,command=self.showMismatch)
		self.mismatchOpt.grid(column=c,row=i+r+2,columnspan=4,sticky='nsw')
		ttMgr.makeTT(self.mismatchOpt,txt="Highlight Mismatching Characters")
		self.bu=Button(master=root,textvariable=getTradStrVar("View Details"), command=self.openPlantView,state='disabled')
		self.bu.grid(column=c,row=i+3+r,columnspan=4,sticky='nsw')
		ttMgr.makeTT(self.bu,txt="View Details")
	def clickCanv(self,event):
		self.rotateSetting.set(0)
		self.changeImage()
	def loadPlant(self,plant):
		self.img=None
		self.plant=PlantProfiles[plant]
		strV=["Name","Common Name","Frequency"]
		for i in range(0,len(self.snippitStuff)-3,3):
			self.snippitStuff[i].set('\n'.join(self.plant[strV[i//3]]))
		self.snippitStuff[-3].set('\n'.join(self.plant.sspp))
		if "Native Status" in self.plant.data and self.natSelection.get() in self.plant.data['Native Status']: self.natData.set(self.plant['Native Status'][self.plant['Native Status'].index(self.natSelection.get())+1])
		if not self.rotateSetting.get():self.changeImage()
		self.canv.bind("<Button-1>", self.clickCanv)
		self.showMismatch()
		self.natMenuBu.config(state='normal')
		self.bu.config(state='normal')
		self.mismatchOpt.config(state='normal')
		self.rotateCkBu.config(state='normal')
	def updateNat(self):
		self.natData.set('')
		if self.natSelection.get() in self.plant['Native Status']:
			self.natData.set(self.plant['Native Status'][self.plant['Native Status'].index(self.natSelection.get())+1])
	def changeImage(self,*dmp):
		if len(self.plant["Images"])>0:
			imgFile=random.choice(self.plant['Images'])
			self.img=Image.open(imgFile)
			self.img.thumbnail((250,250))
			self.img=ImageTk.PhotoImage(self.img)
			self.canv.create_image(0,0,image=self.img, anchor='nw')
		if self.rotateSetting.get(): root.after(3000, self.changeImage)
	def openPlantView(self, *dmp):
		Pview(self.plant.name)
	def showMismatch(self):
		for item in self.adjLaCol:
			item[0].labelw.config(bg=item[0].resetBu.cget('bg'))
			item[1].myLabel.config(bg='grey')
		self.adjLaCol=[]
		if self.mismatchVar.get():
			for div in divisorsList:
				for item in div.mlts:
					if item.label in self.plant.mismatches:
						item.labelw.config(bg='orange')
						div.myLabel.config(bg='orange')
						self.adjLaCol.append((div.mlts[div.mlts.index(item)],div))
				for item in div.ints:
					if item.label in self.plant.mismatches:
						item.labelw.config(bg='orange')
						div.myLabel.config(bg='orange')
						self.adjLaCol.append((div.ints[div.ints.index(item)],div))
				for item in div.dbls:
					if item.label in self.plant.mismatches:
						item.labelw.config(bg='orange')
						div.myLabel.config(bg='orange')
						self.adjLaCol.append((div.dbls[div.dbls.index(item)],div))
class SearchPackage():
	'''Package containing search engine and GUI'''
	def __init__(self, c,r):
		self.srchVar=StringVar()
		self.srchField=Entry(master=root, textvariable=self.srchVar)
		self.srchField.grid(column=c,row=r,columnspan=4,sticky='nesw')
		self.srchButton=Button(master=root, textvariable=getTradStrVar('Search'), command=self.search)
		self.srchButton.grid(column=c+4,row=r,columnspan=3,sticky='nesw')
		self.box=Listbox(master=root)
		self.box.grid(column=c,row=r+1,rowspan=20,columnspan=7,sticky='nesw')
		self.boxScroll=Scrollbar(master=root, command=self.box.yview)
		self.boxScroll.grid(column=c+6,row=r+1,rowspan=20,sticky='nes')
		self.box.config(yscrollcommand=self.boxScroll.set)
		self.box.bind('<Button-1>',self.selectPlant)
		self.srchField.bind('<Return>', self.callSearch)
		ttMgr.makeTT(self.srchField,txt="Enter a common or botanic name (part or whole). Capitalisation isn't important.")
	def callSearch(self,*dmp):
		self.srchButton.invoke()
	def selectPlant(self,event):
		if self.box.size()>0:
			plantLine=self.box.get(self.box.nearest(y=event.y))
			GUI[1].loadPlant(plantLine)
	def search(self):
		self.box.delete(0, END)
		srch=self.srchVar.get()
		for symb in ',./<>?[]{}#~@:;=+-_\|)(*&^%$£"!¬`':
			if symb in srch:
				raise Exception(ValueError, 'Punctuation found in search')
		if len(srch)>1:
			Terms=[srch,srch.lower(),srch[0].upper()+srch[1:]]
			Terms.extend((srch[0].upper()+srch[1:]).split())
			Terms.extend(srch.split())
			found=[]
			for plant in PlantProfiles.keys():
				for term in Terms:
					if term in plant: found.append(plant)
					for item in PlantProfiles[plant]['Common Name']:
						if term in item: found.append(plant)
			for item in found:
				if item not in self.box.get(0, END): self.box.insert(END, item)
class TopBar():
	'''Draws the menu items and status bar at the top, row=0'''
	def __init__(self):
		self.statusVar=StringVar()
		self.statusSet("Loading...")
		self.fileMenuBu=Menubutton(root,textvariable=getTradStrVar("File"),relief='raised', command=None,activebackground='#aaa') 
		self.fileMenu=Menu(self.fileMenuBu,tearoff=0,bg='#aaa',bd=5,activeborderwidth=3,relief='ridge')
		self.fileMenu.add_command(label="Reset Characters",underline=0,command=MasterCharacters.resetAllChars)
		self.fileMenu.add_command(label="Import File",underline=0,command=EXT.importProfile)
		self.fileMenu.add_command(label="Export to File",underline=0,command=self.callExporter)
		self.fileMenu.add_separator()
		self.fileMenu.add_command(label="Exit",underline=1,command=root.quit, accelerator='Alt+F4')
		self.fileMenuBu.config(menu=self.fileMenu)
		self.fileMenuBu.grid(column=0,row=0, columnspan=2,sticky='nesw')
		self.modeMenuBu=Menubutton(root,relief='raised',textvariable=getTradStrVar("Mode"),activebackground='#aaa')
		self.modeMenu=Menu(self.modeMenuBu,tearoff=0,bg='#aaa')
		self.modeMenu.add_command(label='Unavailable in Beta')
		self.modeMenuBu.config(menu=self.modeMenu)
		self.modeMenuBu.grid(column=2,row=0, columnspan=2,sticky='nesw')
		self.settingsMenuBu=Menubutton(root,relief='raised',textvariable=getTradStrVar("Settings"),activebackground='#aaa')
		self.settingsMenu=Menu(self.settingsMenuBu,tearoff=0, bg='#aaa')
		for opt in "Dependency Notification", "Status Bar Only", "Disable Dependencies":
			self.settingsMenu.add_radiobutton(value=opt,label=opt,variable=MasterCharacters.depEff,indicatoron=1)
		self.settingsMenu.add_separator()
		self.settingsMenu.add_command(label="Settings",command=SetMgr.window)
		self.settingsMenuBu.config(menu=self.settingsMenu)
		self.settingsMenuBu.grid(column=4,row=0, columnspan=2,sticky='nesw')
		self.helpMuBu=Menubutton(root,relief='raised',textvariable=getTradStrVar("Help"),activebackground='#aaa')
		self.helpMu=Menu(self.helpMuBu,tearoff=0,bg='#aaa')
		self.helpMu.add_command(label="Overview",underline=0,command=lambda event=None, self=self, opt="Overview":self.callHelp(opt))
		self.helpMu.add_command(label="Help",underline=0,command=lambda event=None, self=self, opt="Help":self.callHelp(opt))
		self.helpMu.add_separator()
		self.helpMu.add_command(label="Data Sources",underline=0,command=lambda event=None, self=self, opt="Data Sources":self.callHelp(opt))
		self.helpMu.add_command(label="Licence Information",underline=0,command=lambda event=None, self=self, opt="Licence":self.callHelp(opt))
		self.helpMu.add_command(label="DIY Guide",underline=0,command=lambda event=None, self=self, opt="DIY":self.callHelp(opt))
		self.helpMu.add_separator()
		self.helpMu.add_command(label="About",underline=0,command=lambda event=None, self=self, opt="About":self.callHelp(opt))
		self.helpMuBu.config(menu=self.helpMu)
		self.helpMuBu.grid(column=6,row=0,columnspan=2,sticky='nesw')
		#self.quitBu=Button(root, textvariable=getTradStrVar("Quit"))
		self.statusLa=Label(master=root, textvariable=getTradStrVar("Status:"), anchor='e')
		self.status=Label(master=root, textvariable=self.statusVar,relief='sunken', anchor='w')
		self.statusLa.grid(column=8,row=0, columnspan=2, sticky='nesw')
		self.status.grid(column=10,row=0, columnspan=20, sticky='nesw')
		for menu,menuBu in ((self.fileMenu,self.fileMenuBu),(self.settingsMenu,self.settingsMenuBu),(self.modeMenu,self.modeMenuBu),(self.helpMu,self.helpMuBu)):
			menu.bind('<Map>', lambda event, self=self, menuBu=menuBu: self.mapped(event, menuBu))
			menu.bind('<Unmap>', lambda event, self=self, menuBu=menuBu: self.mapped(event, menuBu))
		ttMgr.makeMenuTT(self.fileMenu)
		ttMgr.makeMenuTT(self.helpMu)
		ttMgr.makeMenuTT(self.settingsMenu)
		ttMgr.makeMenuTT(self.modeMenu)
		self.statusSet("Ready")
	def statusSet(self,txt='Ready'):
		self.statusVar.set(txt)
		Logger.log("Status: %s"%txt)
	def mapped(self, event, menuBu):
		menuBu.config(bg=DEFBG)
		if int(event.type)==19: menuBu.config(bg='#aaa')
	def callExporter(self): Exporter()
	def callHelp(self, opt):Help(opt)
#####Char types#############
class CharType_Menu(object):
	'''Builds a label, reset button and menu with radio options and an optional (gdd=True) guided selector
		Takes: caller, optList (all possible options including 'unsure') and label)
		Use item.gridify(grd=(c,r)) to set the grid layout'''
	def __init__(self, caller,optList, label, gdd=None): #@type optList: caller; List ([0]='unsure'); label:str 
		self.parent,self.optList,self.label, self.c, self.r, self.affVar, self.gdd=caller,optList,label,0,0, StringVar(),gdd
		self.affVar.set('0(0)/0(0)')
		self.selection=MasterCharacters.dbl[label].val
		MasterCharacters.dbl[label].inst=self
		self.labelw=Label(master=CharFrame.subFrm, textvariable=getTradStrVar(label), width=14, wraplength=100); 
		self.resetBu=Button(master=CharFrame.subFrm, textvariable=getTradStrVar('Reset'),activebackground='#eee', command=self.reset,width=4)
		self.menuBu=Menubutton(CharFrame.subFrm, relief='raised', textvariable=self.selection,activebackground='#eed')
		self.menu=Menu(self.menuBu,tearoff=0, bg='#ddd',bd=4,activeborderwidth=3, relief='ridge')
		self.menuBu.config(menu=self.menu)
		for j in range(len(optList)):
			self.menu.add_radiobutton(value=optList[j],label=optList[j],indicatoron=1,underline=0,variable=self.selection,command=self.updateSelected)
			if j%15==0: self.menu.entryconfig(j, columnbreak=1)
			if self.gdd=="Clr": self.menu.entryconfig(j,background=EXT.getCol(optList[j]))
		self.menu.insert_separator(1)
		if self.gdd=="Gdd":
			self.menu.insert_command(2,label="Chooser",command=self.openChooser)
			self.menu.insert_separator(3)
		elif self.gdd=="Clr": 
			self.menu.insert_command(2,label="Advanced",command=self.clrChooser)
			self.menu.insert_separator(3)
		self.affLabel=Label(master=CharFrame.subFrm, textvariable=self.affVar,font=small)
		CharFrame.update()
		self.menu.config(postcommand=self.update())
		EXT.wheelBinder([self.labelw,self.resetBu,self.menuBu,self.affLabel])
		self.menu.bind('<Map>', lambda event, self=self, menuBu=self.menuBu: self.mapped(event, menuBu),add=True)
		self.menu.bind('<Unmap>', lambda event, self=self, menuBu=self.menuBu: self.mapped(event, menuBu),add=True)
		ttMgr.makeTT(self.labelw,txt=self.label)
		ttLst=[item for item in self.optList]; ttLst.insert(1,'')
		if gdd!="Clr": ttMgr.makeMenuTT(self.menu,txt=ttLst)
		else:ttMgr.makeMenuTT(self.menu,txt=["unsure","","Advanced",""])
		ttMgr.makeTT(self.affLabel,txt="aff explanation")
	def clrChooser(self,*dmp):
		colour=tkColorChooser.askcolor(color='black',title="%s - Colour Chooser"%self.label, parent=root)
		if None not in colour:	self.selection.set(colour[1])
		self.updateSelected()
	def mapped(self, event, menuBu):
		menuBu.config(bg=DEFBG)
		if int(event.type)==19: menuBu.config(bg='#eed')
		else: menuBu.config(bg=DEFBG)
	def gridify(self, grd=False):
		if grd: self.c, self.r=grd[0], grd[1]
		self.labelw.grid(column=self.c, row=self.r, sticky='nesw')
		self.resetBu.grid(column=self.c+1, row=self.r, sticky='nesw')
		self.menuBu.grid(column=self.c+2, row=self.r, columnspan=2, sticky='nesw')
		self.affLabel.grid(column=self.c+4, row=self.r, sticky='nsw')
	def degridify(self):
		self.labelw.grid_forget()
		self.resetBu.grid_forget()
		self.menuBu.grid_forget()
		self.affLabel.grid_forget()
	def disable(self,state):
		for item in (self.labelw,self.resetBu,self.menuBu,self.affLabel):item.config(state=state)
	def update(self, *dmp):
		j=0
		for i in range(len(self.optList)+1+int(self.gdd!=None)*2): 
			txt=getTradStrVar(self.optList[i-j]).get()
			if self.menu.type(i)=='radiobutton':
				self.menu.entryconfigure(i, label=txt)
			else: j+=1
	def updateSelected(self):
		self.parent.updateSelectionCount()
		MasterCharacters.setChar(self.label, [self.selection.get()], caller=self)
		if self.gdd=='Clr': self.menuBu.config(fg=EXT.getCol(self.selection.get()))
		#self.menuBu.config(textvariable=getTradStrVar(self.selection.get())) 
	def reset(self, *dmp):
		self.selection.set('unsure')
		self.updateSelected()
	def openChooser(self,*dmp):
		Logger.log(str(selGuide(self,self.label,self.optList))) 
class CharType_List(object):
	'''Builds a label, reset button and list of multiple selection options
		Takes: caller, optList (all possible options including 'unsure') and label)
		Use item.gridify(grd=(c,r)) to set the grid layout'''
	def __init__(self, caller,optList, label): #@type optList: caller; List ([0]='unsure'); label:str 
		self.parent,self.optList,self.label, self.c, self.r, self.affVar=caller,optList,label,0,0,StringVar()
		self.selection=MasterCharacters.mlt[label].val
		self.affVar.set('0(0)/0(0)')
		MasterCharacters.mlt[label].inst=self
		self.labelw=Label(master=CharFrame.subFrm, textvariable=getTradStrVar(label),width=14,wraplength=100)
		self.resetBu=Button(master=CharFrame.subFrm, textvariable=getTradStrVar('Reset'),activebackground='#eee', command=self.reset,width=4)
		self.lstBox=Listbox(CharFrame.subFrm, selectmode=MULTIPLE, exportselection=0)
		self.scrlLstBox=Scrollbar(CharFrame.subFrm, command=self.lstBox.yview)
		CharFrame.update()
		for i in range(len(self.optList)):
			self.lstBox.insert(END, self.optList[i])
		self.lstBox.config(yscrollcommand=self.scrlLstBox.set,  height=min(len(optList), 4))
		self.affLabel=Label(master=CharFrame.subFrm, textvariable=self.affVar,font=small)
		self.update()
		self.lstBox.bind("<ButtonRelease-1>", self.updateSelection,add=True)
		#self.lstBox.bind("<Enter>", self.update) 
		self.lstBox.bind("<Leave>", self.updateSelection)
		self.reset()
		EXT.wheelBinder([self.labelw,self.resetBu,self.affLabel])
		ttMgr.makeTT(self.labelw,txt=self.label)
		ttMgr.makeListTT(self.lstBox,txt=self.optList)
		ttMgr.makeTT(self.affLabel,txt="aff explanation")
	def gridify(self, grd=False):
		if grd: self.c, self.r=grd[0], grd[1]
		self.labelw.grid(column=self.c, row=self.r, sticky='nesw')
		self.resetBu.grid(column=self.c+1, row=self.r, sticky='nesw')
		self.lstBox.grid(column=self.c+2, row=self.r, rowspan=self.lstBox.cget('height'), columnspan=2,sticky='nesw')
		self.scrlLstBox.grid(column=self.c+3, row=self.r,rowspan=self.lstBox.cget('height'), sticky='nes')
		self.affLabel.grid(column=self.c+4,row=self.r, sticky='nsw')
	def degridify(self):
		self.labelw.grid_forget()
		self.resetBu.grid_forget()
		self.lstBox.grid_forget()
		self.scrlLstBox.grid_forget()
		self.affLabel.grid_forget()
	def disable(self,state):
		for item in (self.labelw,self.resetBu,self.lstBox,self.scrlLstBox,self.affLabel):item.config(state=state)
	def updateSelected(self, *dmp):
		self.lstBox.select_clear(0, END)
		for item in self.selection.get().split(';'):self.lstBox.select_set(self.optList.index(item))
	def updateSelection(self, *dmp):
		'''return selection values as list'''
		#self.update()
		allSelected=[]
		for i in self.lstBox.curselection(): allSelected.append(self.optList[int(i)])
		if len(allSelected)==0: 
			self.lstBox.select_clear(1, END)
			self.selection.set('unsure')
		else: 
			self.selection.set(';'.join(allSelected))
			self.lstBox.selection_clear(0)
		MasterCharacters.setChar(self.label, self.selection.get().split(';'), caller=self)
	def reset(self):
		self.lstBox.selection_clear('0', END)
		self.lstBox.select_set(0)
		self.updateSelected()
	def update(self, *dmp):
		'''Update Language for each item in self.optList'''
		for i in range(self.lstBox.size()):
			sel=self.lstBox.selection_includes(i)
			label=self.lstBox.get(i)
			self.lstBox.delete(i)
			self.lstBox.insert(i,getTradStrVar(label).get())
			if sel:self.lstBox.select_set(i)
class CharType_Int(object): 
	'''Builds a label, reset button and text Input which takes integers.
	Takes: caller, label, unit=None
	Use item.gridify(grd=(c,r)) to set the grid layout'''
	def __init__(self, caller, label, unit=None):
		self.parent,self.unit,self.label, self.c, self.r,self.affVar=caller,unit,label,0,0,StringVar()
		self.selection=MasterCharacters.int[label].val
		self.affVar.set('0(0)/0(0)')
		MasterCharacters.int[label].inst=self
		self.labelw=Label(CharFrame.subFrm, textvariable=getTradStrVar(label), width=14, wraplength=100)
		self.resetBu=Button(CharFrame.subFrm, textvariable=getTradStrVar('Reset'),activebackground='#eee', command=self.reset,width=4)
		self.inputBox=Entry(CharFrame.subFrm, textvariable=self.selection,width=16)
		if self.unit: self.unitLabel=Label(CharFrame.subFrm, textvariable=getTradStrVar(unit))
		self.affLabel=Label(master=CharFrame.subFrm, textvariable=self.affVar,font=small)
		CharFrame.subFrm.update()
		self.reset()
		self.inputBox.bind("<Any-KeyRelease>", self.updateSelected)
		EXT.wheelBinder([self.labelw,self.resetBu,self.inputBox,self.affLabel])
		ttMgr.makeTT(self.labelw,txt=self.label)
		ttMgr.makeTT(self.affLabel,txt="aff explanation")
	def gridify(self, grd=False):
		if grd: self.c, self.r=grd[0], grd[1]
		self.labelw.grid(column=self.c, row=self.r, sticky='nesw')
		self.resetBu.grid(column=self.c+1, row=self.r, sticky='nesw')
		self.inputBox.grid(column=self.c+2, row=self.r,sticky='nesw')
		self.unitLabel.grid(column=self.c+3, row=self.r, sticky='nesw')
		self.affLabel.grid(column=self.c+4, row=self.r, sticky='nsw')
	def degridify(self):
		self.labelw.grid_forget()
		self.resetBu.grid_forget()
		self.inputBox.grid_forget()
		self.unitLabel.grid_forget()
		self.affLabel.grid_forget()
	def disable(self,state):
		for item in (self.labelw,self.resetBu,self.unitLabel,self.affLabel):item.config(state=state)
	def updateSelected(self, *dmp):
		if self.selection.get()!='': MasterCharacters.setChar(self.label, [self.selection.get()], caller=self) #This verifies that it is a float as well as updating stuff
	def reset(self):
		self.selection.set('0')
		self.updateSelected()
class CharType_Pic(object):
	def __init__(self,caller,label):
		self.parent,self.label, self.c, self.r,self.affVar=caller,label,0,0,StringVar()
		self.selection=StringVar()#MasterCharacters.int[label].val#todo
		self.affVar.set('0(0)/0(0)')
		self.labelw=Label(CharFrame.subFrm, textvariable=getTradStrVar(label), width=14, wraplength=100)
		self.resetBu=Button(CharFrame.subFrm, textvariable=getTradStrVar('Reset'),activebackground='#eee', command=self.reset,width=4)
		self.selBu=Button(CharFrame.subFrm,textvariable=self.selection,command=self.onclick)
		self.affLabel=Label(master=CharFrame.subFrm, textvariable=self.affVar,font=small)
		CharFrame.subFrm.update()
		self.reset()
	def reset(self,*event):self.selection.set("unsure")
	def onclick(self,*event):
		self.pLeft=[plant for plant in PlantProfiles]
		pUsed={}
		for plant in PlantProfiles.keys():
			imgs=[]
			for img in PlantProfiles[plant]["Images"]:
				if self.label.lower() in img: imgs.append(img)
			if len(imgs)>0: pUsed[self.pLeft.pop(self.pLeft.index(plant))]=sorted(imgs,key= lambda item:len(item))
		options=sorted(pUsed.keys())
		options.insert(0,"unsure")
		options.append("definitely not listed")
		imgs=[] #Redefined
		for i in range(len(options)):
			if options[i] in pUsed: imgs.append(pUsed[options[i]])
			else:imgs.append([])
		selGuide(self, charName=self.label, posVals=options, imgs=imgs, msg="Do any of these look like your sample? Hint: cycling of images may be possible by right-clicking")
	def gridify(self, grd=False):
		if grd: self.c, self.r=grd[0], grd[1]
		self.labelw.grid(column=self.c, row=self.r, sticky='nesw')
		self.resetBu.grid(column=self.c+1, row=self.r, sticky='nesw')
		self.selBu.grid(column=self.c+2, row=self.r,columnspan=2,sticky='nesw')
		#self.affLabel.grid(column=self.c+4, row=self.r, sticky='nsw')#Leave it out for now
	def degridify(self):
		self.labelw.grid_forget()
		self.resetBu.grid_forget()
		self.selBu.grid_forget()
		self.affLabel.grid_forget()
class Characters(object):
	'''stores all the characters neatly'''
	def __init__(self):
		self.depEff=StringVar()
		self.depEff.set(Settings["dependency"])
		self.dbl={} #@note: Should be just 1 name each; {name:DblcharStore,...}
		self.mlt={} #@note: Same as above except that it can have multiple selections
		self.int={}
	def addChar(self, charType, name, posValues, dependencies={}): #@type charType:str; names:List; posValues:List; dependencies:Dict;
		if charType in ('dbl','gdd','clr'):
			self.dbl[name]=BaseCharStorage(name, posValues, dep=dependencies)
		if charType=='mlt':
			self.mlt[name]=BaseCharStorage(name, posValues, dep=dependencies)
		if charType=='int':
			self.int[name]=BaseCharStorage(name, unit=posValues[0], dep=dependencies, val=0)
	def setChar(self, char, data, caller=None): #@type data: tuple/List of valued
		if char in self.dbl:
			if data[0] not in self.dbl[char].posValues and '#' not in data[0]: raise RuntimeError('%s not found in %s by character %s'%(data[0],self.dbl[char].posValues, char))
			self.dbl[char].val.set(data[0])
			if caller:
				caller.menuBu.config(bg='black')
				def b2n(obj):
					obj.menuBu.config(bg=root.cget('bg'))
				root.after(50, b2n, caller)
			#Dependency Resolution
			if data[0] in self.dbl[char].dependencies: 
				self.invokeDependantChange(dep=self.dbl[char].dependencies[data[0]])
		elif char in self.mlt:
			if data[0] not in self.mlt[char].posValues: raise RuntimeError('%s not found in %s by character %s'%(data[0],self.mlt[char].posValues, char))
			self.mlt[char].val.set(';'.join(data))
			if caller==None: self.mlt[char].inst.updateSelected() #So it doesn't recurse too deep
			#Dependency Resolution
			if data[0] in self.mlt[char].dependencies: 
				self.invokeDependantChange(dep=self.mlt[char].dependencies[data[0]])
		elif char in self.int:
			if data[0]=='unsure':
				self.setChar(char, 0, caller)
			elif not EXT.is_float(data[0]): 
				MsgBox.showwarning("Not A Valid Numeral", "What you entered for %s does not appear to be a number. Value reset."%char)
				if caller: caller.reset()
			else:
				self.int[char].val.set(data[0])
			#Dependency Resolution
			for depKey in self.int[char].dependencies.keys(): 
				if EXT.compareFloats(f1=data[0], f2=depKey[1:], sign=depKey[0]): #Must supply sign for it to work (<>=)
					self.invokeDependantChange(dep=self.int[char].dependencies[depKey])
		self.testPlants() #This also updates possiblePlants
	def invokeDependantChange(self,dep=[]):
		deps=[item for item in dep]
		for i in range(len(deps)//3): #@UnusedVariable
			dep=[deps.pop(0) for j in range(3)] #@UnusedVariable
			if self.depEff.get()!="Disable Dependencies":
				if dep[1]=='=':
					self.setChar(char=dep[0], data=[dep[2]])
					if self.depEff.get()=="Dependency Notification":MsgBox.showinfo(title="Dependency Related Change", message="Because of default dependencies, %s was set to %s"%(dep[0], dep[2]))
					GUI[3].statusSet("Dependency related change: %s set to %s"%(dep[0], dep[2]))
				elif dep[1]=='-':
					for grp in [self.dbl, self.int, self.mlt]:
						if dep[0] in grp:
							if grp[dep[0]].val.get()==dep[2]: 
								self.setChar(char=dep[0],data=['unsure'])
								if self.depEff.get()=="Dependency Notification":MsgBox.showinfo(title="Dependency Related Change", message="Because of default dependencies, %s was reset"%dep[0])
								GUI[3].statusSet("Dependency related change: %s reset"%dep[0])
							break
				elif dep[1]=='x':
					for div in divisorsList:
						for grp in div.mlts,div.ints,div.dbls:
							for item in grp:
								if dep[0] in item.label: item.disable(state=dep[2])
				elif dep[1]=='divx':
					for div in divisorsList:
						
						if dep[0] in div.name: div.disable(state=dep[2])
				for div in divisorsList:
					div.updateSelectionCount()
	def testPlants(self):
		vals=[1,-1]
		for plant in PlantProfiles.values():plant.score0,plant.score1,plant.mismatches=0,0,[]
		for div in divisorsList:
			if div.pic:
				if div.pic.selection.get()!='unsure':
					if div.pic.selection.get()=="definitely not listed":
						for plant in PlantProfiles.keys():
							if plant not in div.pic.pLeft: PlantProfiles[plant]["score1"]-=1
					else:
						for plant in PlantProfiles.keys():
							PlantProfiles[plant]["score%i"%int(plant not in div.pic.selection.get())]+=vals[int(plant not in div.pic.selection.get())]
		for plant in PlantProfiles.values():
			for char in self.dbl:
				if self.dbl[char].val.get()!='unsure':
					if char in plant.data:
						if "#" in self.dbl[char].val.get():
							dif=[]
							for val in plant[char]:
								if '#' not in val: val=EXT.getCol(colour=val)
								cval=val[1:3],val[3:5],val[5:]
								pval=self.dbl[char].val.get()[1:3],self.dbl[char].val.get()[3:5],self.dbl[char].val.get()[5:]
								dif.append(abs(int(cval[0],16)-int(pval[0],16))+abs(int(cval[1],16)-int(pval[1],16))+abs(int(cval[2],16)-int(pval[2],16)))
							plant["score%i"%int(min(dif)>Settings["col strictness"])]+=1-2*int(min(dif)>Settings["col strictness"])
						else:
							plant["score%i"%int(self.dbl[char].val.get() not in plant.data[char])]+=vals[int(self.dbl[char].val.get() not in plant.data[char])]
							if self.dbl[char].val.get() not in plant.data[char]: plant.mismatches.append(char) #Add as a mismatch for this plant
			for char in self.mlt:
				if self.mlt[char].val.get()!='unsure':
					if char in plant.data:
						for val in self.mlt[char].val.get().split(';'): #For some reason, it stops updating after 1 negative. val is incorrect???
							#Logger.log(self.mlt[char].val.get().split(';'))  #for debugging only
							plant["score%i"%int(val not in plant.data[char])]+=vals[int(val not in plant.data[char])]
							if val not in plant.data[char]:plant.mismatches.append(char)#Add as a mismatch for this plant
			for char in self.int:
				if self.int[char].val.get() not in [0,'0']:
					if char in plant.data:
						if len(plant[char])==1:
							x1=float(plant[char][0])*0.95
							x2=float(plant[char][0])*1.05
						elif len(plant[char])==2:
							x1=float(plant[char][0])*0.95
							x2=float(plant[char][1])*1.05
						else: raise Exception('int value greater than length 2 or no length: %s'%plant[char])
						plant["score%i"%int(float(self.int[char].val.get())<x1 or float(self.int[char].val.get())>x2)]+=vals[int(float(self.int[char].val.get())<x1 or float(self.int[char].val.get())>x2)]
						if float(self.int[char].val.get())<x1 or float(self.int[char].val.get())>x2: plant.mismatches.append(char)#Add as a mismatch for this plant
		if len(GUI)>1: GUI[0].updateList() #the 'if' makes sure it is first declared
	def resetAllChars(self,*dmp):
		GUI[3].statusSet("Resetting all characters, Please Wait...")
		def reset():
			for char in self.dbl:self.setChar(char, ['unsure'])
			for char in self.mlt:self.setChar(char, ['unsure'])
			for char in self.int:self.setChar(char, [0])
			for div in divisorsList: 
				if div.pic:div.pic.reset()
				div.updateSelectionCount()
		root.after_idle(reset)
		GUI[3].statusSet("Ready")
	def updateDivs(self,*dmp):
		for div in divisorsList: div.updateSelectionCount()
	def __str__(self):
		rtnVal="Characters Object\n  dbl: \n"
		for item in self.dbl.keys():
			rtnVal+='\t'+item+': '+str(self.dbl[item])+'\n'
		rtnVal+="  mlt: \n"
		for item in self.mlt.keys():
			rtnVal+='\t'+item+': '+str(self.mlt[item])+'\n'
		rtnVal+="  int: \n"
		for item in self.int.keys():
			rtnVal+='\t'+item+': '+str(self.int[item])+'\n'
		return rtnVal
class BaseCharStorage(object):
	def __init__(self,name,posValues=[],unit=None,dep=[],val="unsure"): #@type param:str, list, str, str
		self.name=name
		self.posValues=posValues #@note: None in the case of Int
		self.dependencies=dep
		if unit: 
			self.unit=unit #@note: Only in the case of Int 
		self.val=StringVar()
		self.val.set(val)
		self.inst=None
	def __str__(self):
		return str((self.name, self.posValues, self.dependencies, self.val.get()))
class Divisor(object):
	def __init__(self, name, default):
		self.name,self.dbls,self.mlts,self.ints,self.pic=name,[],[],[],None
		self.state,self.nbrSetVar,self.affVar=StringVar(),StringVar(),StringVar()
		self.state.set(default)
		self.nbrSetVar.set('Selected options: 0/0')
		self.affVar.set('0/0')
		self.myLabel=Label(master=CharFrame.subFrm, text="::: %s :::"%self.name, bg='grey',font=bold)
		self.treeCtrl=Button(master=CharFrame.subFrm, textvariable=self.state, command=self.toggleTreeCtrl,bg='grey')
		self.nbrSet=Label(master=CharFrame.subFrm, textvariable=self.nbrSetVar, bg='grey', width=20)
		self.affLabel=Label(master=CharFrame.subFrm, textvariable=self.affVar, bg='grey',font=small,width=11)
		EXT.wheelBinder([self.myLabel,self.treeCtrl,self.nbrSet,self.affLabel])
		ttMgr.makeTT(self.myLabel)
		ttMgr.makeTT(self.treeCtrl,txt="Expand/collapse tree")
		ttMgr.makeTT(self.nbrSet, txt="Number of character selected/total number of characters (in this section)")
		ttMgr.makeTT(self.affLabel,txt="Summary of maximum plants affected by this section")
	def toggleTreeCtrl(self, *dmp):
		if self.state.get()=='+':
			self.state.set('-')
			i=self.beginRow
			if self.pic: 
				self.pic.gridify(grd=(0,i))
				i+=1
			for item in self.dbls: 
				item.gridify(grd=(0,i))
				i+=1
			for item in self.mlts:
				item.gridify(grd=(0,i))
				i+=4
			for item in self.ints:
				item.gridify(grd=(0,i))
				i+=1
		else: 
			self.state.set('+')
			if self.pic:self.pic.degridify()
			for item in self.dbls: item.degridify()
			for item in self.mlts:item.degridify()
			for item in self.ints: item.degridify()
		self.updateSelectionCount() #is this line needed???
		CharFrame.update()
	def makeChar(self, charType, ref):
		if charType=='Dbl':
			self.dbls.append((CharType_Menu(caller=self,optList=MasterCharacters.dbl[ref].posValues,label=ref)))
		if charType in ('Gdd','Clr'):
			self.dbls.append((CharType_Menu(caller=self,optList=MasterCharacters.dbl[ref].posValues,label=ref,gdd=charType)))
		if charType=='Mlt':
			self.mlts.append((CharType_List(caller=self,optList=MasterCharacters.mlt[ref].posValues, label=ref)))
		if charType=='Int':
			self.ints.append((CharType_Int(caller=self,label=ref, unit=MasterCharacters.int[ref].unit)))
		if self.name in ['Leaf',u'Flower (♀/⚥)','Fruit','Seed']: 
			self.pic=CharType_Pic(self,label={'Leaf':"Leaves",u'Flower (♀/⚥)':'Flowers','Fruit':'Fruit','Seed':'Seed'}[self.name])
	def compilebyGrid(self, lastRowUsed):
		self.myLabel.grid(column=0, row=lastRowUsed, sticky='nesw')
		self.treeCtrl.grid(column=1, row=lastRowUsed, sticky='nesw')
		self.nbrSet.grid(column=2, row=lastRowUsed, columnspan=2, sticky='nesw')
		self.affLabel.grid(column=4, row=lastRowUsed, sticky='nsw')
		lastRowUsed+=1
		self.beginRow=lastRowUsed
		if self.pic:
			self.pic.gridify(grd=(0,lastRowUsed))
			lastRowUsed+=1
		for item in self.dbls: 
			item.gridify(grd=(0,lastRowUsed))
			lastRowUsed+=1
		for item in self.mlts: 
			item.gridify(grd=(0,lastRowUsed))
			lastRowUsed+=4
		for item in self.ints: 
			item.gridify(grd=(0,lastRowUsed))
			lastRowUsed+=1
		try:
			self.treeCtrl.config(width=self.dbls[0].resetBu.cget('width'))
		except IndexError: pass #It is ok, as long as one of them work, it sets the width ok
		self.toggleTreeCtrl()
		self.toggleTreeCtrl() #This makes sure that the grid has spaces reserved for them, and that they fix up correctly
		return lastRowUsed
	def updateSelectionCount(self):
		unsel, sel=0,0
		aff=[0,0,0,0]#Ensure there are no empty sequences; 
		bases=[]; bases.extend(self.dbls); bases.extend(self.mlts); bases.extend(self.ints)
		for item in bases:
			if item.selection.get() in ['unsure','0']: unsel+=1
			else:sel+=1
			if item.affVar.get(): aff.extend(re.findall('\d+',item.affVar.get()))
		self.nbrSetVar.set('Selected options: %i/%i'%(sel, sel+unsel))
		self.affVar.set("%s(%s)/%s(%s)"%(max(map(int,aff[0::4])),max(map(int,aff[1::4])),max(map(int, aff[2::4])),max(map(int, aff[3::4]))))
		#self.affVar.set("{}({})/{}({})".format"%s(%s)/%s(%s)"%(max(aff[0::4]),max(aff[1::4]),max(aff[2::4]),max(aff[3::4]))) #@TODO: consider an alternative algorithm
	def disable(self, state):
		if state=='disabled' and self.state.get()=='-': self.toggleTreeCtrl()
		for item in (self.myLabel,self.treeCtrl,self.nbrSet,self.affLabel):	item.config(state=state)
def importCharacters(filename="Chars.csv"):
	fin=codecs.open(filename, encoding='utf-8')
	lineNo=0
	for line in fin:
		lineNo+=1
		line=line.strip()
		if not '#' in line:
			data=line.split('\t')
			if data[0]=='Divisor':
				divisorsList.append(Divisor(data[1], data[2]))
			if data[0] in ('Dbl', 'Mlt', 'Int', 'Gdd','Clr'):
				deps={}
				if len(data)>4: raise RuntimeError('Unexpected data read from line %i of file %s' %(lineNo,filename))
				if len(data)==4:
					for dep in data[3][1:].split(','):
						if dep.split(':')[0] in deps: deps[dep.split(':')[0]].extend(dep.split(':')[1].split(' '))
						else: deps[dep.split(':')[0]]=dep.split(':')[1].split(' ')
				try:
					data[2]=EXT.stripList(data[2].split(','))
				except IndexError:
					raise RuntimeError('Error with line "%s" in char.csv; Check that the line is complete!'%line)
				if data[0]!='Int': data[2].insert(0,'unsure')
				MasterCharacters.addChar(data[0].lower(),data[1], data[2], deps)
				divisorsList[-1].makeChar(charType=data[0],ref=data[1])
	i=1 #adjust if necessary, this is the first line to be gridded
	for divisor in divisorsList: #Gridification
		i=divisor.compilebyGrid(i)
	for pp in PlantProfiles: #Character verification
		PlantProfiles[pp].checkChars()
def importProfiles(folder='PlantProfiles/'):
	for filename in EXT.importFileList(folder='PlantProfiles'):
		if filename.split('.')[-1]=='csv':
			PlantProfiles[' '.join(filename.split('/')[-1].split('.')[0].split('_'))]=PlantProfile(EXT.profileReader(filename))
MasterCharacters=Characters()
importProfiles()
importCharacters()
GUI.extend([PossiblePlants(c=11,r=2),PlantPreview(c=11,r=25),SearchPackage(c=23,r=2),TopBar()])
MasterCharacters.testPlants()
root.mainloop(0)
