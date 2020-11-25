from django.db import models
from bs4 import BeautifulSoup
import requests

# Create your models here.


class Oscar:
	def __init__(self, name):
		self.n = name
		self.x = name.split(' ')
		headers = {'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1 Safari/605.1.15"}
		source = requests.get(
			"https://oscar.gatech.edu/pls/bprod/bwckctlg.p_disp_course_detail?cat_term_in=202008&subj_code_in="
			+ self.x[0] + "&crse_numb_in="+self.x[1]).text
		self.soup = BeautifulSoup(source, "html.parser")
		self.reqs = []
		self.desc = ""
		self.credit = ""
		self.dec = {}
		if (self.getData()):
			self.process()
			self.process2()
			self.process3()
			self.process4()

	def getData(self):
		y = self.soup.find("table", class_="datadisplaytable")
		a = y.find_all("tr")[1].td.find_all(text=True)
		for r in a:
			if (r == "\n"):
				continue
			else:
				r.replace("\n", "")
				r = r.strip()
				self.reqs.append(r)
		self.desc = self.reqs[0]
		ind = (self.reqs[1]).index("Credit")
		self.credit = (self.reqs[1])[ind-6]

		if "Prerequisites:" in self.reqs:
			self.reqs = self.reqs[self.reqs.index("Prerequisites:")+1:]
			return True
		else:
			self.dec[1] = "NO PREREQUISITES"
			return False

	def process(self):
		i = len(self.reqs)-1
		while i >=0 :
			x = self.reqs[i]
			if (x == "Undergraduate Semester level"):
				self.reqs.remove(x)
			if (x.startswith("Minimum")):
				if (x.find(")") != -1):
					self.reqs[i] = self.reqs[i][18:]
				else:
					self.reqs[i] = self.reqs[i][19:]
			if (x == ""):
				self.reqs.remove(x)
			self.reqs[i].strip()
			i = i - 1
		# self.reqs = self.reqs[:-1]

	def process2(self):
		i = 0
		while(i < len(self.reqs)): 
			a =	self.reqs[i].find("Undergraduate Semester level")
			if (a != -1):
				self.reqs[i] = self.reqs[i][:a] + self.reqs[i][a+28:]
			self.reqs[i] = self.reqs[i].strip()
			i = i + 1		
    
	def process3(self):
		i = 0
		a = 1
		self.dec[a] = ""
		while i < len(self.reqs):
			
			if (self.reqs[i].find("(") != -1):
				if (self.dec[a] == ""):
					self.dec[a] = "("
				else:
					self.dec[a] = self.dec[a] + " / "+ "("

				while(self.reqs[i].find(")") == -1):
					i = i + 1
					if (self.reqs[i].find("or") != -1):
						self.dec[a] = self.dec[a] + " / " 
					elif(self.reqs[i].find("and") != -1):
						self.dec[a] = self.dec[a] + " & "
					else:
						self.dec[a] = self.dec[a] + str(self.reqs[i])
				self.dec[a] = self.dec[a] + ")"

			if (self.reqs[i].find("or") != -1):
				i = i + 1
				continue
			
			if (self.reqs[i].find("and") != -1):
				i = i + 1
				a = a + 1
				if (self.reqs[i].find(") and (")):
					self.dec[a] ="("
				else:
					self.dec[a] = ""
				continue

			if (self.dec[a] == ""):
				self.dec[a] = str(self.reqs[i])
			else:
				self.dec[a] = self.dec[a] +  " / " + str(self.reqs[i])			
			i = i + 1
	
	def process4(self):
		for i in range(len(self.dec)):
			y = self.dec[i+1].rfind("( / ")
			if (y != -1):
				self.dec[i+1] = self.dec[i+1].replace("( / ", "(")
			z = self.dec[i+1].rfind("( & ")
			if (z != -1):
				self.dec[i+1] = self.dec[i+1].replace("( & ", "(")
			a = self.dec[i+1].rfind(" / )")
			if (a != -1):
				self.dec[i+1] = self.dec[i+1].replace(" / )", ")")
			b = self.dec[i+1].rfind(" & )")
			if (b != -1):
				self.dec[i+1] = self.dec[i+1].replace(" & )", ")")
			if (self.dec[i + 1][-2] == "/"):
				self.dec[i + 1] = self.dec[i + 1][:-3]
