"""
LineCMS - Content Management System (Product & Blogging) for Rapid website development
Website: www.linecms.com
Author: S. Jangra & Mark A.R. Pequeras
"""

keys = {
		"orders" : ['id','fulfilled','customer_name', 'customer_email', 'amount_total', 'created', 'payment_status', 'customer_country', 'customer_postal', 'currency', 'items', 'session_id', 'notes','tracking','metadata', 'address', 'phone', 'shipping_cost','history','ordernumber','additional'],
		"mod" : ["popup","announcement","uparrow","socialshare","videoembed","custom","extras"],
		"product" : ["id","title","category","variants","product_url","product_urlsystem","seo_description","seo_keywords","images","mainimage","variant_details","timestamp","hidden","product_id","body","price","stock"],
		"site" : ["site_description","sitename","footer_copyright","logo","up_arrow","domain","social_share","pop_up","meta_description","meta_keywords","favicon","site_type","messages","site_phone","site_email","site_location"],
		"blog" : ["id","title","body","image","timestamp","hidden","url","category"],
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

class Site(Order):
	def __init__(self, key, lst) -> None:
		super().__init__(key, lst)

class Mod(Order):
	def __init__(self, key, lst) -> None:
		super().__init__(key, lst)







	
	
	

		
	
	

		

	