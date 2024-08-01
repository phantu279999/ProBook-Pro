from src.process_action.base import Base


class Category(Base):
	def __init__(self, config):
		Base.__init__(self, config)
		self.config = config.action['Category']


class CategoryNews(Base):
	def __init__(self, config):
		Base.__init__(self, config)
		self.config = config.action['CategoryNews']


