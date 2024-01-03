"""
LineCMS - Content Management System (Product & Blogging) for Rapid website development
Website: www.linecms.com
Author: S. Jangra & Mark A.R. Pequeras
"""
import sqlite3
import datetime
import time
import urllib
import re
import random
import json
import os
import random
import settings
from flask import g
from ast import literal_eval as lite

UPLOAD_FOLDER_PRODUCTS = 'static/dashboard/uploads/products'
UPLOAD_FOLDER_BLOG = 'static/dashboard/uploads/blog'

class SandEngine:
    """Group of functions for database actions
    """
    connection = sqlite3.connect(settings.dbase_path, check_same_thread=False)

    def install_cred(self,uname: str,pwd: str) -> None:
        """Install login credential
        Args:
            uname (str): username
            pwd (str): password (raw)
        """
        params = "INSERT INTO users (username,passw) VALUES (?,?)"
        vals = (uname,pwd)
        c = self.connection.cursor()
        c.execute(params, vals)
        self.connection.commit()
        self.log(f"Welcome to LineCMS, Credentials Installed")

    def themeset(self, theme: str) -> None:
        """Sets selected theme

        Args:
            theme (str): theme name
        """
        try:
            c = self.connection.cursor()
            q = f"UPDATE control SET theme = '{theme}'"
            c.execute(q)
            self.connection.commit()
            self.log(f"Theme changed to {theme}")
        except Exception as err:
            self.log(f"Theme assignment error: {err}")

    def themeget(self) -> tuple:
        """Current selected theme

        Returns:
            tuple: assigned theme
        """
        c = self.connection.cursor()
        q = "SELECT theme FROM control"
        c.execute(q)
        return c.fetchone()
        
    def orderfulfill(self,data: dict) -> bool:
        """Mark order as Fulfilled
        fulfilled 1 = Manual (No Email)
        fulfilled 2 = Auto  (Sends email)

        Returns:
            bool: if success
        """
        try:
            c = self.connection.cursor()
            if "manual" in data:
                q = """UPDATE productorders SET tracking="{t}", fulfilled="2", additional="{a}"  where ordernumber='{o}';""".format(t=data['tracking'],o=str(data['ordernumber']),a=str(data['additional']))
            else:
                q = """UPDATE productorders SET tracking="{t}", fulfilled="1", additional="{a}"  where ordernumber='{o}';""".format(t=data['tracking'],o=str(data['ordernumber']),a=str(data['additional']))
            c.execute(q)
            self.connection.commit()
            return True    
        except Exception as err:
            self.log(f"Order fulfilment error: {err}")
            return False

    def orderhistory_get(self,onum: str) -> tuple:
        """loads order history

        Args:
            onum (str): order number

        Returns:
            tuple: order history
        """
        c = self.connection.cursor()
        q = f"SELECT history FROM productorders WHERE ordernumber='{onum}';"
        c.execute(q)
        return c.fetchone()

    def orderhistory_add(self,data: dict) -> bool:
        """Attach history to order

        Args:
            data (dict): contains history information
        Returns:
            bool: if success
        """
        c = self.connection.cursor()
        q = """UPDATE productorders SET history="{o}" where ordernumber="{orn}";""".format(o=str(data['obj']),orn=str(data['ordernumber']))
        c.execute(q)
        self.connection.commit()
        return True
    
    def url_gen(self, content: str) -> str:
        """_summary_

        Args:
            content (str): url to modify

        Returns:
            str: modified url str
        """
        remove_sym = re.sub(r'[^\w]', ' ', content)
        v = urllib.parse.quote_plus(str(random.randint(10, 50))+remove_sym)
        n = str(v).replace("+", "-")
        g.new_blog_url = n
        return n
    
    def productorders_get(self,q=False,total=False) -> tuple:
        """_summary_

        Args:
            q (bool, optional): query. Defaults to False.
            total (bool, optional): Length. Defaults to False.

        Returns:
            tuple: order
        """
        c = self.connection.cursor()
        if total:        
            c.execute("SELECT Count(*) FROM productorders")
            return c.fetchone()
        fetch = c.execute(q)
        return fetch.fetchall()
   
    def get_products_cat_lists(self) -> list:
        """Builds category list

        Returns:
            list: generated (seperated categories)
        """
        c = self.connection.cursor()
        m = c.execute("SELECT category FROM products")
        mf = m.fetchall()
        cats = {}
        for cat in mf:
            if not cat[0]:  # empty
                pass
            else:
                for itm in cat[0].split(","):
                    if itm in cats:
                        cats[itm] = cats[itm] + 1
                    else:
                        cats[itm] = 1
        return cats
    
    def productorders_single_get(self,ids: str,loadfulfill=False) -> tuple:
        """Load product Order

        Args:
            ids (str): load using order ID
            loadfulfill (bool, optional): load using order number. Defaults to False.

        Returns:
            tuple: order
        """
        c = self.connection.cursor()
        q = f"SELECT * FROM productorders WHERE id = {ids}"
        if loadfulfill:
            q = f"SELECT * FROM productorders WHERE ordernumber = '{loadfulfill}'"
        c.execute(q)
        return c.fetchone()
    
    def productorders_set(self,order: dict) -> str:
        """Set new order

        Args:
            order (dict): data generated by stripe

        Returns:
            str: Id and Timestamp
        """
        try:
            c = self.connection.cursor()
            params = "INSERT INTO productorders (fulfilled,customer_name,customer_email,amount_total,created,payment_status,customer_country,customer_postal,currency,items,session_id,metadata,address,phone,shipping_cost) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)"
            vals = ("0",order['customer_name'],order['customer_email'],order['amount_total'],order['created'],order['payment_status'],order['customer_country'],order['customer_postal'],order['currency'],order['items'],order['session_id'],str(order['metadata']),order['address'],order['phone'],order['shipping_cost'])
            c.execute(params, vals)   
            curr_id = c.lastrowid
            secq = "UPDATE productorders SET ordernumber='{o}' where id='{c}';".format(o=f"{curr_id}{order['created']}",c=curr_id)
            c.execute(secq)
            self.connection.commit()
            return f"{curr_id}{order['created']}"
        except Exception as err:
            self.log(f"Adding new order error: {err}")
            return False
        
    def productsettings_smtp(self,data: dict) -> bool:
        """Update SMTP Settings

        Args:
            data (dict): contains dict of data (smtp credentials)

        Returns:
            bool: if no error
        """        
        try:
            c = self.connection.cursor()
            q = f"""UPDATE productsetting SET smtp="{str(data)}";"""
            c.execute(q)
            self.connection.commit()
            return True
        except Exception as err:
            self.log(f"SMTP assignment error: {err}")
            return False
        
    def productstock_deduct(self,ids: str,isvariant=False) -> None:
        """Deduct Stock on success payment
        2 types of stock, Main product and Variant

        Args:
            ids (str): product_id
            isvariant (bool): to deduct on variant (dict) in db

        Returns:
            None: Not needed
        """        
        c = self.connection.cursor()

        if isvariant:
            pull = c.execute(f"SELECT variant_details FROM products WHERE product_id='{ids}';")
            dict_cast = None
            try:
                dict_cast = lite(pull.fetchone()[0])
            except:
                pass
            if dict_cast:
                try:
                    d = dict_cast[isvariant+"-ivar"]['instock']
                    dict_cast[isvariant+"-ivar"]['instock'] = int(d) - 1 # will update soon with dynamic from quantity
                    c.execute(f"""UPDATE products SET variant_details = "{str(dict_cast)}" WHERE product_id='{ids}';""")
                    self.connection.commit()
                except Exception as e:
                    pass

        else:
            pull = c.execute(f"SELECT stock FROM products WHERE product_id='{ids}';")
            pull_ = pull.fetchone()
            if pull_:
                if int(pull_[0]) > 1:
                    count_ = int(pull_[0]) - 1  # will update soon with dynamic from quantity
                    c.execute(f"UPDATE products SET stock = {count_} WHERE product_id = '{ids}';")
                    self.connection.commit()
                else:
                    pass
            
    def productsettings_temp(self,data: dict) -> bool:
        """Update template (Jinja style)

        Args:
            data (dict): Type of template with Html/Jinja syntax

        Returns:
            bool: if no error
        """
        try:
            _p = {"f":data['templates']['fulfilled'],"p":data['templates']['placed'],"a":data['templates']['abandoned']}
            c = self.connection.cursor()
            q = f"""UPDATE productsetting SET templates="{str(data['status'])}", template_fulfilled="{str(_p['f'])}", template_placed="{str(_p['p'])}", template_abandoned="{str(_p['a'])}";"""
            c.execute(q)
            self.connection.commit()
            return True
        except Exception as e:
            print(e)
            return False
         
    def productsettings_ship(self,data: dict) -> bool:
        """Shipping rates

        Args:
            data (dict): shipping data

        Returns:
            bool: if no error
        """
        try:
            c = self.connection.cursor()
            q = f"""UPDATE productsetting SET shipping_enable='{data['status']}', shipping_rates='{str(data['shipping'])}', shipping_countries="{data['countries']}";"""
            c.execute(q)
            self.connection.commit()
            return True
        except Exception as err:
            self.log(f"Shipping options error: {err}")
            return False
        
    def productsettings_str(self,data: dict) -> bool:
        """Save Shop data (API information)

        Args:
            data (dict): shop information (Stripe Api, etc..)

        Returns:
            bool: if no error
        """        
        try:
            c = self.connection.cursor()
            q = f"""UPDATE productsetting SET secretkey='{data['sk']}', publishablekey='{data['pk']}', currency='{data['ck']}', webhookkey='{data['wsk']}', signkey='{data['wsk']}';"""
            c.execute(q)
            self.connection.commit()
            return True
        except Exception as err:
            self.log(f"Product settings (STR) assignment error: {err}")
            return False

    def productsettings_set(self, sk: str, pk: str, ck: str, wk: str, wsk: str,s_enable: str,s_rates: str,s_countries: list) -> tuple:
        "Unused func, will delete soon"
        try:
            c = self.connection.cursor()
            q = """UPDATE productsetting SET secretkey = "{sk}", publishablekey = "{pk}", currency = "{ck}", webhookkey = "{wk}",signkey = "{wsk}", shipping_enable = "{se}", shipping_rates = '{sr}', shipping_countries = "{sc}" WHERE id = 1; """.format(
                sk=sk, pk=pk, ck=ck,wk=wk,wsk=wsk,se=s_enable,sr=s_rates,sc=s_countries)
            c.execute(q)
            self.connection.commit()
            return True
        except Exception as err:
            self.log(f"Product settings assignment: {err}")
            return False

    def productsettings_get(self) -> tuple:
        """Product settings (Mostly Stripe data)

        Returns:
            tuple: shop settings
        """
        c = self.connection.cursor()
        q = "SELECT * FROM productsetting where id=1"
        c.execute(q)
        _c = c.fetchone()
        if _c:
            return _c
        else:
            return [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0] # Empty

    def productimagesupdater(self, imgcat: str, data: dict, newimage: str, filename: str) -> tuple:
        c = self.connection.cursor()
        m_fetch = c.execute(
            "SELECT {sel} FROM products WHERE product_id='{m}'".format(
                sel=imgcat, m=data['p_id'])
            )
        try:
            _old = m_fetch.fetchone()
            _dblist_ = eval(_old[0])
            if filename not in _dblist_:  # new file add to db
                _dblist_.append(filename)
                _inserts = """UPDATE products SET images = "{i}" WHERE product_id = '{product_id}'""".format(
                    i=_dblist_, product_id=data['p_id'])
                c.execute(_inserts)
                self.connection.commit()
            return True
        except Exception as e:
            print(e)
            return False

    def productvariantsupdater(self, imgcat: str, data: dict, newimage: str) -> bool:
        """Variant image update

        Args:
            imgcat (str): image cat
            data (dict): product info
            newimage (str): file

        Returns:
            bool: if no error
        """
        variant_name = data['p_variant']+"-ivar"
        _c = self.connection.cursor()
        m_fetch = _c.execute(
            "SELECT {sel} FROM products WHERE product_id='{m}'".format(
                sel=imgcat, m=data['p_id'])
            )
        try:
            _old = m_fetch.fetchone()
            _new_ = eval(_old[0])
            _new_[variant_name] = newimage
            variants = json.dumps(_new_)
            _inserts = """UPDATE products SET variants = '{variants}' WHERE product_id = '{product_id}'""".format(
                variants=variants, product_id=data['p_id'])
            _c.execute(_inserts)
            self.connection.commit()
            return True
        except Exception as e:
            return False

    def productsimilar(self, count=5, category=0) -> list:
        """Groups similar categories (pull random if not enough)

        Args:
            count (int, optional): result. Defaults to 5.
            category (int, optional): target category. Defaults to 0.

        Returns:
            list: sorted products
        """
        categ_split = category.split(",")
        category = random.choice(categ_split)
        count = count
        pr = []
        _c = self.connection.cursor()
        self.m_fetch = _c.execute(
            "SELECT * FROM products WHERE category='{m}' LIMIT {l};".format(m=category, l=count))
        self.m_data = self.m_fetch.fetchall()

        for d in self.m_data:
            pr.append(d)

        if len(pr) < count:
            self.mr_fetch = _c.execute(
                "SELECT * FROM products ORDER BY random() LIMIT {l};".format(l=count-len(pr)))
            self.mr_data = self.mr_fetch.fetchall()
            for i in self.mr_data:
                pr.append(i)
        return pr

    def productimagesmod(self, variants: dict, product_id: str) -> bool:
        """
        Update file-not-found as empty and updates db
        trigger: product.variantimagemodifier
        """
        try:
            variants = json.dumps(variants)
            c = self.connection.cursor()
            inserts = """UPDATE products SET variants = '{variants}' WHERE product_id = '{product_id}'""".format(
                variants=variants, product_id=product_id)
            c.execute(inserts)
            self.connection.commit()
            return True
        except Exception as err:
            self.log(f"Product images modifier error: {err}")
            return False

    def delete_pr(self, value: str) -> bool:
        """deletes product

        Args:
            value (str): product id

        Returns:
            bool: true if success
        """        
        q = """DELETE FROM products WHERE product_id = '{value}';""".format(
            value=value)
        c = self.connection.cursor()

        try:
            c.execute(q)
            self.connection.commit()
            return True
        except Exception as err:
            self.log(f"Product deletion error: {err}")
            return False

    def delete_apip(self, table, column, value) -> bool:
        "@mark to be deleted"
        q = """DELETE FROM {tb} WHERE product_urlsystem = '{value}';""".format(
            tb=table, column=column, value=value)
        c = self.connection.cursor()

        try:
            c.execute(q)
            self.connection.commit()
            return True
        except Exception as e:
            return False

    def delete_api(self, table, column, value) -> bool:
        "@mark to be deleted"
        q = """DELETE FROM {tb} WHERE route = '{value}';""".format(
            tb=table, column=column, value=value)
        c = self.connection.cursor()

        try:
            c.execute(q)
            self.connection.commit()
            self.log("Blog post deleted")
            return True
        except Exception as e:
            print(e)
            return False

    def product_update(self, d: dict) -> bool:
        """updates product data

        Args:
            d (dict): product data

        Returns:
            bool: true if no error
        """        
        c = self.connection.cursor()
        q = f"""UPDATE products SET body = "{d['body']}",category = "{d['category']}",images = "{d['images']}", mainimage = "{d['mainimage']}", price = "{d['price']}", product_url = "{d['product_url']}", product_urlsystem = "{d['product_urlsystem']}",  seo_description = "{d['seo_description']}", seo_keywords = "{d['seo_keywords']}",  title = "{d['title']}",  variant_details = "{d['variant_details']}", variants = "{d['variants']}", hidden = "{d['hidden']}" WHERE product_id = "{d['id']}";"""
        try:
            c.execute(q)
            self.connection.commit()
            return d['product_urlsystem']
        except Exception as err:
            self.log(f"Product update error: {err}")
            return False

    def product_publish(self, d: dict) -> bool or str:
        """new product insert

        Args:
            d (dict): new product data

        Returns:
            str: if success (URL)
            bool: if not
        """
        c = self.connection.cursor()
        try:
            ts = self.timestamp(routeStyle=1)
            ugen = self.url_gen(ts+" "+d['title'])
            params = "INSERT INTO products (title,category,variants,product_url,product_urlsystem,seo_description,seo_keywords,images,mainimage,variant_details,timestamp,hidden,product_id,body,price,stock) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)"
            vals = (d['title'], d['category'], str(d['variants']), d['product_url'], ugen,
                    d['seo_description'], d['seo_keywords'], str(d['images']), d['mainimage'], str(d['variant_details']), ts, "0", d['id'], d['body'], d['price'],d['stock'])
            c.execute(params, vals)
            self.connection.commit()
            return ugen
        except Exception as err:
            self.log(f"Product publish error: {err}")

    def delete_image_partial(self, data: dict) -> None:
        """deletes uploaded yet changed image file (unused) (Blog publish)

        Args:
            data (dict): image data
        """
        c = self.connection.cursor()
        try:
            os.remove(os.path.join(UPLOAD_FOLDER_BLOG, data['image']))
        except:
            pass
        q = "UPDATE blog SET image = '' WHERE route = '{r}';".format(
            r=data['route'])
        c.execute(q)
        self.connection.commit()

    def get_product_single(self, route: str, checkout=False) -> tuple:
        """Load Product data (Single)

        Args:
            route (_type_): product route
            checkout (bool, optional): uses product_urlsystem instead of product_id. Defaults to False.

        Returns:
            tuple: product data
        """
        c = self.connection.cursor()
        if checkout:
            c.execute(
                "SELECT * FROM products WHERE product_id='{m}'".format(m=checkout))
        else:
            c.execute(
                "SELECT * FROM products WHERE product_urlsystem='{m}'".format(m=route))
        return c.fetchone()

    def get_product_listings(self, getcount=False,getcats=False,quer=[],custom={}) -> tuple:
        """Custom load products from db (product listings)

        Args:
            getcount (bool, optional): length. Defaults to False.
            getcats (bool, optional): categories. Defaults to False.
            quer (list, optional): custom db query. Defaults to [].
            custom (dict, optional): custom filter. Defaults to {}.

        Returns:
            tuple: _description_
        """
        c = self.connection.cursor()
        if custom:
            if custom['s']:
                if custom['c']:
                    c.execute("select * from products where hidden=0 AND category='{}' AND (title like '%{}%' OR body like '%{}%') order by id desc limit {},{}".format(custom['c'],custom['s'],custom['s'],custom['off'],custom['perp']))
                    return c.fetchall()
                c.execute("select * from products where hidden=0 AND (title like '%{}%' OR body like '%{}%') order by id desc limit {},{}".format(custom['s'],custom['s'],custom['off'],custom['perp']))
                return c.fetchall()
            if custom['c']:
                if custom['s']:
                    c.execute("select * from products where hidden=0 AND category='{}' AND (title like '%{}%' OR body like '%{}%') order by id desc limit {},{}".format(custom['c'],custom['s'],custom['s'],custom['off'],custom['perp']))
                c.execute("select * from products where hidden=0 AND category='{}' order by id desc limit {},{}".format(custom['c'],custom['off'],custom['perp']))
                return c.fetchall()
        if getcats:
            c.execute("select category from products order by id desc")
            return c.fetchall()
        if getcount:
            c.execute("SELECT Count(*) FROM products")
            return c.fetchone()
        if quer:
            c.execute("select * from products order by id desc limit {},{}".format(quer[0],quer[1]))
            return c.fetchall()
        c.execute("SELECT * FROM products ORDER BY id DESC")
        return c.fetchall()

    def blog_publish(self, dicts: dict) -> bool:
        """insert new blog data
        Args:
            dicts (dict): new blog data

        Returns:
            bool: true if no error
        """
        c = self.connection.cursor()
        try:
            ts = self.timestamp(routeStyle=1)
            tso = self.timestamp(routeStyle=0)
            params = "INSERT INTO blog (title,message,image,timestamp,hidden,route,category) VALUES (?,?,?,?,?,?,?)"
            vals = (dicts['title'], dicts['body'], dicts['image'],
                    tso, "0", self.url_gen(ts+" "+dicts['title']), dicts['category'])
            c.execute(params, vals)
            self.connection.commit()
            return True
        except Exception as err:
            self.log(f"Blog publish error: {err}")
            return False

    def blog_update(self, dicts: dict) -> bool:
        """update existing blog data
        Args:
            dicts (dict): new blog data

        Returns:
            bool: true if no error
        """
        c = self.connection.cursor()
        try:
            q = "UPDATE blog SET title = '{title}',message = '{message}', image = '{image}',hidden = '{hidden}', category = '{category}' WHERE route = '{route}';".format(
                title=dicts['title'], message=dicts['body'], image=dicts['image'], hidden=dicts['hidden'], category=dicts['category'], route=dicts['route'])
            c.execute(q)
            self.connection.commit()
            print("Blog updated")
            return True
        except Exception as err:
            self.log(f"Blog update error: {err}")
            return False


    def get_blog_single(self, route: str) -> tuple:
        """load blog post

        Args:
            route (str): blog route

        Returns:
            tuple: blog data
        """
        c = self.connection.cursor()
        m = c.execute(
            "SELECT * FROM blog WHERE route='{m}'".format(m=route))
        return m.fetchone()

    def get_blog_listings(self,getcount=False,quer=[]) -> list:        
        """blog listings

        Args:
            page (int, optional): unused. Defaults to 0.
            result (int, optional): unused. Defaults to 10.
            getcount (bool, optional): length. Defaults to False.
            quer (list, optional): custom query. Defaults to [].

        Returns:
            list: tupled blog posts
        """
        c = self.connection.cursor()

        if getcount:
            fetch = c.execute("SELECT Count(*) FROM blog")
            return fetch.fetchone()
        
        if quer:
            c.execute("select * from blog order by id desc limit {},{}".format(quer[0],quer[1]))
            return c.fetchall()
        
        m = c.execute("SELECT * FROM blog ORDER BY id DESC")
        return m.fetchall()

    def get_blog_cat_lists(self) -> list:
        """creates a list of categories

        Returns:
            list: generated category list from blog
        """
        c = self.connection.cursor()
        m = c.execute("SELECT category FROM blog")
        mf = m.fetchall()
        cats = {}
        for cat in mf:
            if not cat[0]:  # empty
                pass
            else:
                for itm in cat[0].split(","):
                    if itm in cats:
                        cats[itm] = cats[itm] + 1
                    else:
                        cats[itm] = 1
        return cats
    

    def knightclientapi(self, action) -> bool:
        "needs a recode"
        try:
            c = self.connection.cursor()
            a = {
                "dlogs": """DELETE FROM logging""",
                }
            c.execute(a[action])
            return True
        except:
            return False

    def knightclientapiv2(self, action) -> bool:
        "needs a recode"
        c = self.connection.cursor()
        where = action['where']
        action = action['action']

        try:
            a = {
                "blog_0": """UPDATE blog SET hidden = '0' WHERE route = '{r}';""".format(r=where),
                "blog_1": """UPDATE blog SET hidden = '1' WHERE route = '{r}';""".format(r=where),
                }
            c.execute(a[str(action)])
            self.connection.commit()
            return True
        except Exception as e:
            return False

    def timestamp(self, routeStyle=False) -> str:
        """generates timestamp (returns only date if routeStyle)

        Args:
            routeStyle (bool, optional): only date if true. Defaults to False.

        Returns:
            str: _description_
        """
        _n = datetime.datetime.now()
        d_ = str(_n).split()
        dt = d_[0]
        t = time.strftime("%I:%M %p")
        ts = dt + " " + t
        if routeStyle:
            return dt
        return ts

    def message(self, dicts: dict) -> bool:
        """adds new visitor message

        Args:
            dicts (dict): message dict

        Returns:
            bool: true if no error
        """
        try:
            c = self.connection.cursor()
            params = "INSERT INTO messages (name,email,message,phone,timestamp) VALUES (?,?,?,?,?)"
            vals = (dicts['name'], dicts['email'],
                    dicts['message'], dicts['phone'], self.timestamp())
            c.execute(params, vals)
            self.connection.commit()
            return True
        except Exception as err:
            self.log(f"Visitor message error: {err}")
            return False

    def delete_blog(self, route: str) -> bool:
        """deletes blog post

        Args:
            route (str): blog route

        Returns:
            bool: true if no error
        """
        c = self.connection.cursor()
        try:
            q = "DELETE FROM blog WHERE route = {ids};".format(ids=route)
            c.execute(q)
            self.connection.commit()
            return True
        except Exception as e:
            self.log("Unable to delete blog post, "+str(e))
            return False

    def mvdelete(self, ids: str) -> bool:
        """delete visitor message 

        Args:
            ids (str): message id

        Returns:
            bool: true if no error
        """
        c = self.connection.cursor()
        try:
            q = "DELETE FROM messages WHERE id = {ids};".format(ids=ids)
            c.execute(q)
            self.connection.commit()
            return True
        except Exception as e:
            self.log("Unable to delete message, "+str(e))
            return False

    def log(self, message: dict) -> bool:
        """logger
        Args: 
            message (dict): message
        Returns:
            true: true if no error
        """
        if not settings.logging_enabled:
            return False 
        c = self.connection.cursor()
        try:
            params = "INSERT INTO logging (log,timestamp) VALUES (?,?)"
            vals = (message, self.timestamp())
            c.execute(params, vals)
            self.connection.commit()
            return True
        except Exception as e:
            return False

    def update_data_uploads(self, table, column, newvalue, where, whereequal) -> dict:
        """
        @mark to be deleted
        """
        c = self.connection.cursor()
        q = "UPDATE {table} SET {column} = '{value}' WHERE {where} = '{whereequal}';".format(
            table=table, column=column, value=newvalue, where=where, whereequal=whereequal
        )
        c.execute(q)
        self.connection.commit()
        return {"status": "success"}

    def update_websitesettings(self, dicts: dict, owner: str) -> bool:
        """_summary_

        Args:
            dicts (dict): new website data
            owner (str): needs to be removed (Useless arg)

        Returns:
            bool: true if no error
        """
        c = self.connection.cursor()
        try:
            q = "UPDATE control SET sitename = '{sitename}',sitedescription = '{sitedescription}',footercopyright = '{footercopyright}',meta_description = '{meta_description}',meta_keywords = '{meta_keywords}', sitenumber = '{sitenumber}', siteemail='{siteemail}', siteaddress='{siteaddress}';".format(
                sitename=dicts['sitename'], sitedescription=dicts['description'], footercopyright=dicts['footercopyright'], meta_description=dicts['meta_description'], meta_keywords=dicts['meta_keywords'],sitenumber=dicts['sitenumber'],siteemail=dicts['siteemail'],siteaddress=dicts['siteaddress'])
            c.execute(q)
            self.connection.commit()
            return True
        except Exception as e:
            print(e)
            return False

    def update_module(self, data) -> bool:
        """updates module

        Args:
            data (dict): module info

        Returns:
            bool: true if no error
        """        
        c = self.connection.cursor()
        try:
            data = eval(data)
            copy_data = data.copy()
            del data['module']
            se = json.dumps(data)
            q = """UPDATE modules SET '{module}' = '{new}'""".format(
                module=copy_data['module'], new=se)
            c.execute(q)
            self.connection.commit()
            return True
        except Exception as err:
            self.log(f"Module update error: {err}")
            return False

    def update_credential(self, uname: str, newpwd: str) -> bool:
        """website login update

        Args:
            uname (str): username
            newpwd (str): new password

        Returns:
            bool: true if success
        """
        c = self.connection.cursor()
        try:
            q = "UPDATE users SET passw = '{value}' WHERE username = '{uname}';".format(
                value=newpwd, uname=uname)
            c.execute(q)
            self.connection.commit()
            return True
        except Exception as err:
            self.log(f"Update credential error: {err}")
            return False

    def get_messages(self) -> tuple:
        """messages from visitors (if included)

        Returns:
            tuple: messages
        """
        c = self.connection.cursor()
        c.execute("SELECT * FROM messages ORDER BY id DESC")
        return c.fetchall()

    def get_logs(self) -> tuple:
        """Logging (Deployment / Debugging safe)

        Returns:
            tuple: Logging messages
        """
        c = self.connection.cursor()
        c.execute("SELECT * FROM logging ORDER BY id DESC")
        return c.fetchall()

    def get_cred(self, *args,**kwargs) -> tuple:
        """Account information (raw) / Credential will be updated soon for more sec.

        Returns:
            tuple: Account credentials (raw)
        """
        c = self.connection.cursor()
        c.execute("SELECT * FROM users")
        return c.fetchall()

    def load_modules_settings(self) -> tuple:
        """Loads module settings

        Returns:
            tuple: contains module name and status
        """
        c = self.connection.cursor()
        c.execute("SELECT * FROM modules")
        return c.fetchall()

    def load_data_index(self, load: bool) -> tuple:
        """Loads information (for Enginepublic templates usage)

        Args:
            load (bool): returns site desc.

        Returns:
            tuple: website information
        """
        c = self.connection.cursor()
        self.fetch_control = c.execute("SELECT * FROM control")
        self.site_data = self.fetch_control.fetchall()
        self.fetch_msg = c.execute("SELECT * FROM messages")
        self.site_msgs = self.fetch_msg.fetchall()

        if load:
            return self.site_data[0]
        
        all_data = {  
            "sitedescription": self.site_data[0][0],
            "sitename": self.site_data[0][1],
            "footercopyright": self.site_data[0][2],
            "logo": self.site_data[0][3],
            "uparrow": self.site_data[0][4],
            "domain": self.site_data[0][5],
            "socialshare": self.site_data[0][6],
            "popup": self.site_data[0][7],
            "meta_description": self.site_data[0][8],
            "meta_keywords": self.site_data[0][9],
            "favicon": self.site_data[0][10],
            "site_type": self.site_data[0][11],
            "messages": len(self.site_msgs),
            'sitenumber':self.site_data[0][16],
            'siteemail':self.site_data[0][17],
            'siteaddress':self.site_data[0][18],
        }
        return all_data

