import os
import sys
sys.path.append("mdb_python")


class StudyMDB:
	def __init__(self):
		files = os.listdir("mdb_python")
		self.tables = []
		for filename in files:
			if filename.endswith(".py"): self.tables.append(filename[:-3])

	def printTables(self):
		for table in tables:
			print table

	def printRow(self, no_row, tablename):
		obj_table = __import__(tablename)
		no_records = obj_table.no_of_records
		if no_row < 0 or no_row >= no_records:
			return None
		fieldList = obj_table.field_names
		table_data = obj_table.table_data
		for i, key in enumerate(fieldList):
			print "%-25s:%s" % (key, table_data[no_row][i+1])

	def noRecords(self, tablename):
		obj_table = __import__(tablename)
		print obj_table.no_of_records



if __name__ == '__main__':
	mdb = StudyMDB()
	mdb.printRow(0, "User")
		
		
