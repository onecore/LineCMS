"""
LineCMS - Content Management System (Product & Blogging) for Rapid website development
Website: www.linecms.com
Author: S. Jangra & Mark A.R. Pequeras
"""

import settings

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
'dbase_path': 'dbase/sand',
'sc_badge_insert': 'bg-secondary',
'logging_enabled': False, 
'render_product_single': 'product.html',
'route_blog': '/blog', 
'render_blog_list': 'blog-list.html'
}

default_settings = [ _s for _s in defaults.keys()]
user_settings = []

def svalidate():
    isdefault = settings.load_default
    isdefaultempty = settings.load_default_empty

    for setting in default_settings:
        setting_value = getattr(settings,str(setting))

        if type(setting_value) != type(defaults[setting]):
            print(f"\nSandCMS --> Settings Error: '{setting}' Type should be '{type(defaults[setting])}'\n")
            return False
        
        if isdefault:
            if setting == "load_default": continue
            setattr(settings,str(setting),defaults[str(setting)])
            print(f"Setting: Loaded Default value for '{setting}'")


        if not len(str(setting_value)): # Empty checks
            print (f"'{setting}'is empty")
            if isdefaultempty:
                setattr(settings,str(setting),defaults[str(setting)])
                print(f"Setting: '{setting}' value set to default")
                return True
            return True

    return True