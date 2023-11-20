"""
SandCMS - Content Management System (Product & Blogging) for Rapid website development
Website: www.sandcms.com
Author: S. Jangra & Mark A.R. Pequeras
"""

#**** Load Default values *****
load_default = False  # Override all settings value to Default (Not recommended if you have a modified source)
load_default_empty = False # Use Default value on empty setting

# Templating & System variables
sc_badge_insert = "bg-secondary"  # Blog-list view / fn blog_list_badge_category
sc_admin_button = "bg-primary"   # Admin button / fn admin_button

# Dashboard route (URL)
route_dashboard = "/dashboard"

# File / Products
render_product_single = "product.html"
render_product_list = "product-list.html"

# File / Blogs
render_blog_single = "blog.html"
render_blog_list = "blog-list.html"

# Route (URL) Products
route_product = "/product"
route_product_list = "/product-list"

# Route (URL) Blogs
route_blog = "/blog"
route_blog_list = "/blog-list"


# Misc Settings / Variables below
cms_debug = False  
cms_version = "1.4"

# Email template paths for (Abandoned, Placed, Fulfilled) templates in .HTML form (Do not add Leading slash)
# email_templates = "templates/email"
# email_templates_write = ["fulfilled","placed"] # Do not change as its act as iterable and needs some other modification

# Inputs List for inputs_dashboard_settings
# -"sitename"
# -"description"
# -"meta_description"
# -"meta_keywords"
# -"footercopyright"
# -"sitenumber"
# -"siteemail"
# -"siteaddress"
inputs_dashboard_settings = set(["sitename"]) # Form inputs that can be Empty
inputs_dashboard_minumum_length = 5 # Less than the value will return a required or not enough error

# Orders
order_error_countries = ['CA','US']
order_payment_method = ['card']  # check stripe for list of avail. method
order_novariant_selected = "Available variants"  # override default value (when no variant selected) / Also needs an update on JS side
order_template_notracking_message = "Not supplied" # will show in the email if theres no tracking added (unless Formatter removed)
order_template_noadditional_message = "Not supplied" # will show in the email if theres no additional added (unless Formatter removed)
order_template_manual = """ 
{{COMPANYNAME}}%0D%0A
Woo hoo! Your order is on its way. Your order details can be found below.%0D%0A%0D%0A
ORDER SUMMARY%0D%0A
Order #{{ORDERNUMBER}}%0D%0A
Order Date: {{ORDERDATE}}%0D%0A
Order Total: {{ORDERTOTAL}}%0D%0A
SHIPPED TO ADDRESS: {{CUSTOMERADDRESS}}%0D%0A%0D%0A

TRACK YOUR ORDER: {{TRACKINGLINK}}%0D%0A
ADDITIONAL INFO: {{ADDITIONAL}}
"""     # Template for manual fulfillment


# Uploads
uploads_allowedext = set(['png', 'jpg', 'jpeg', 'gif', 'svg', 'ico'])  # Allowed File Extentions in uploader
uploads_blog = 'static/dashboard/uploads/blog'   # Blog Uploads
uploads_products = 'static/dashboard/uploads/products' # Product Images / Main images and Variant images
uploads_dashboard = "static/dashboard/uploads/dashboard" # SandCMS Dashboard Uploads ()

# Database Path and File
dbase_path = "dbase/sand"

# Simple Logging
logging_enabled = False


# Products
product_similar_load = 7 # try to pull similar in this count (if similar runs out it will pull random product)
product_similar_noimage_set = "ni.jpeg" # Image file needs to be in '/static/dashboard/uploads/'
productlist_select_none = "Group by Categories" # Product listing (No value selected)