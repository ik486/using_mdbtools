import os
import re
import sys 
import commands

class MDB2Python:
	""" This program convert tables in mdb file to python data structure
            it creates a directory named mdb_python and stores all data """
	def __init__(self, mdb_filename):
		self.mdb_filename = mdb_filename
		self.tables = None
		self.fd = None

	def getTableList(self):
		"""Returns table names as list"""
		if self.tables is not None: return self.tables
		cmd = "mdb-tables %s" % (self.mdb_filename)
		output = commands.getoutput(cmd)
		self.tables = output.split()
		return self.tables

	def getTableData(self, table_name):
		""" this function convets table data in to python list of lists
                    First value of the list is record no"""
		cmd = "mdb-array %s %s" % (self.mdb_filename, table_name)
		output = commands.getoutput(cmd)
		output = re.split("\n\{\s",output)[1:]
		if len(output):
			last = output.pop()
			last = re.split("\n}\n\};",last)[0]
			output.append(last)
		data = []
		for val in output:
			temp = re.findall("/\*[0-9 ]+\*/", val)
			val = val.replace(temp[0],"")
			recno = eval(temp.pop(0).strip()[2:-2].strip())
			val = re.split("\n\},",val)[0]
			vals = re.split(",\s*\n",val)
			out = [recno]
			for val in vals:
				val = val.strip()
				try:
					out.append(eval(val))
					continue
				except:
					if re.match("\{[a-z0-9-]{5,}\}", val):
						out.append(val[1:-1])
					else:
						out.append(val)
			data.append(out)
		return data
		
	def getFieldNames(self, table_name):
		""" this function convets table data in to python list of lists
                    First value of the list is record no"""
		cmd = "mdb-export %s %s" % (self.mdb_filename, table_name)
		output = commands.getoutput(cmd)
		return output.split("\n",1)[0].split(",")

	def xWrite(self, val=""):
		if self.fd is None: return False
		self.fd.write(val+"\n")
		return True


	def saveTableData(self, table_name):
		"""Creates a file named <table_name>.py in
                   mdb_python directory and stores table data
                   this includs filed_names, table_data, no_of_records etc"""

		commands.getoutput("mkdir -p mdb_python")
		self.fd = open("mdb_python/%s.py" % (table_name), "w")
		fields = mdb.getFieldNames(table_name)
		table_data = mdb.getTableData(table_name)
		no_of_records = len(table_data)
		self.xWrite('table_name = "%s"' % (table_name))
		self.xWrite('no_of_records = %d' % (no_of_records))
		self.xWrite('field_names = [')
		for field in fields:
			self.xWrite('\t"%s",' % (field))
		self.xWrite(']')
		self.xWrite('table_data = [')
		for row in table_data:
			self.xWrite('%s,' % (row))
		self.xWrite(']')
		self.fd.close()
		self.fd = None
		
		
		

if __name__ == '__main__':
	if len(sys.argv) < 2:
		print sys.argv[0], "<mdb-file>"
		sys.exit(0)
	mdb = MDB2Python(sys.argv[1])
	tables = mdb.getTableList()
	for table in tables:
		mdb.saveTableData(table)
