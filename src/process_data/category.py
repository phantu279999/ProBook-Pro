from src.process_data.base import Base


class Category(Base):
	def __init__(self, config):
		Base.__init__(self, config)
		self.config = config.action['Category']

	def get_data(self):
		...


class CategoryNews(Base):
	def __init__(self, config):
		Base.__init__(self, config)
		self.config = config.action['CategoryNews']


