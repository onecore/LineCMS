"""
SandCMS - Content Management System (Product & Blogging) for Rapid website development
Website: www.sandcms.com
Author: S. Jangra & Mark A.R. Pequeras
"""

keys = {
		"orders" : ['id','fulfilled','customer_name', 'customer_email', 'amount_total', 'created', 'payment_status', 'customer_country', 'customer_postal', 'currency', 'items', 'session_id', 'notes','tracking','metadata', 'address', 'phone', 'shipping_cost','history','ordernumber','additional']
		}

def zipper(key: str,combinewith: list) -> dict:
	return dict(zip(keys[key],combinewith))

# public route
class Order:
	empty = [] # list of empty cols
	def __init__(self,key,lst) -> None:
		self.obj = zipper(key,lst)

		for column, contents in self.obj.items():
			if contents == None:
				contents = ""
				Order.empty.append(column)
			setattr(Order,column,contents)

	@classmethod
	def getempty(cls):
		return cls.empty

class Product(Order):
	def __init__(self, key, lst) -> None:
		super().__init__(key, lst)

class Blog(Order):
	def __init__(self, key, lst) -> None:
		super().__init__(key, lst)







	
	
	

		
	
	

		

	