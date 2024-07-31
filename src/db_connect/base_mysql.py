import datetime
import traceback
import mysql.connector

from src.config.config import config_mysql


class BaseMySQL:
	def __init__(self, config):
		self.config = config
		self.host = config['host']
		self.user = config['username']
		self.password = config['password']
		self.port = config['port']
		self.db = config['db']
		self.mydb = mysql.connector.connect(
			host=self.host, user=self.user, password=self.password, port=self.port, database=self.db
		)
		self.mycursor = self.mydb.cursor()

	def query(self, query):
		self.mydb = mysql.connector.connect(
			host=self.host, user=self.user, password=self.password, port=self.port, database=self.db
		)
		self.mycursor = self.mydb.cursor()
		self.mycursor.execute(query)
		rows = self.mycursor.fetchall()
		res = [
			dict((self.mycursor.description[i][0], value.isoformat() if isinstance(value, datetime.datetime) else value)
			for i, value in enumerate(row)) for row in rows
		]
		self.mydb.close()
		return res

	def execute(self, query):
		try:
			self.mydb = mysql.connector.connect(
				host=self.host, user=self.user, password=self.password, port=self.port, database=self.db
			)
			self.mycursor = self.mydb.cursor()
			self.mycursor.execute(query)
			self.mydb.commit()
			self.mydb.close()
			return True
		except:
			print(traceback.format_exc())
			return False


if __name__ == '__main__':
	db = BaseMySQL(config_mysql)
	print(db.query("select id, title from news_news;"))
