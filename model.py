from sqlalchemy import Column, String, Integer, ForeignKey, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref


Base = declarative_base()

class Category(Base):
	__tablename__ = 'Category'

	name = Column(String, primary_key=True)
	items = relationship("Item") 

	def __repr__(self):
		return "<Category(name='%s')>" % (self.name)

	# Serialize for jsonify
	@property
	def serialize(self):
		return {
           'Name'         : self.name,
           'Items'        : [i.serialize for i in self.items]
        }



class Item(Base):
	__tablename__ = 'Item'

	id = Column(String, primary_key=True)
	name = Column(String)
	discription = Column(String)
	photo = Column(String)
	category = Column(String, ForeignKey('Category.name'))
	create_time = Column(DateTime)

	def __repr__(self):
		return "<Item(name='%s', discription='%s', category='%s')>" % (
			self.name, self.discription, self.category)

	# Serialize for jsonify
	@property
	def serialize(self):
		return {
           'Name'         : self.name,
           'Discription'  : self.discription,
           'ID'           : self.id,
           'Photo'        : self.photo,
           'Create_time'  : self.create_time,
           
       }