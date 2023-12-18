"""
LineCMS - Content Management System (Product & Blogging) for Rapid website development
Website: www.linecms.com
Author: S. Jangra & Mark A.R. Pequeras
"""

defaults = {
'uploads_products': 'static/dashboard/uploads/products', 
'inputs_dashboard_settings': set(['sitename']), 
'uploads_allowedext': set(['ico', 'svg', 'jpeg', 'gif', 'jpg', 'png']), 
'route_product': '/product', 'cms_debug': False, 
'cms_version': '1.4', 
'uploads_dashboard': 'static/dashboard/uploads/dashboard',
'product_similar_noimage_set': 'ni.jpeg',
'product_similar_load': 7,
'inputs_dashboard_minumum_length': 5,
'render_blog_single': 'blog.html',
'order_error_countries': ['CA', 'US'],
'order_novariant_selected': 'Available variants',
'sc_admin_button': 'bg-primary',
'uploads_blog': 'static/dashboard/uploads/blog',
'order_payment_method': ['card'], 
'render_product_list': 'product-list.html',
'route_dashboard': '/dashboard',
'route_product_list': '/product-list',
'route_blog_list': '/blog-list',
'__name__': '__main__', 
'dbase_path': 'dbase/sand',
'sc_badge_insert': ['bg-secondary'],
'logging_enabled': False, 
'render_product_single': 'product.html',
'route_blog': '/blog', 
'render_blog_list': 'blog-list.html',
'order_template_notracking_message' : "Not supplied",
'order_template_noadditional_message' : "Not supplied"
}