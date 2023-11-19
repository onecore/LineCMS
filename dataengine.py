"""
SandCMS - Content Management System (Product & Blogging) for Rapid website development
Website: www.sandcms.com
Author: S. Jangra & Mark A.R. Pequeras
"""
import sqlite3
import datetime
import time
import urllib
import re
import random
from flask import g
import json
import os
from icecream import ic
import random
import settings

UPLOAD_FOLDER_PRODUCTS = 'static/dashboard/uploads/products'
UPLOAD_FOLDER_BLOG = 'static/dashboard/uploads/blog'


class SandEngine:

    connection = sqlite3.connect(settings.dbase_path, check_same_thread=False)
    # cursor = connection.cursor()

    def themeset(self, theme):
        c = self.connection.cursor()
        q = f"UPDATE control SET theme = '{theme}'"
        c.execute(q)
        self.connection.commit()

    def themeget(self):
        """Product settings db table has to be premade"""
        c = self.connection.cursor()
        q = "SELECT theme FROM control"
        fetch = c.execute(q)
        return fetch.fetchone()

    def orderlist(self,page,perpage,offset,search,status,initload=False):
        c = self.connection.cursor()

        try:
            pass
        except:
            return False
        
    def orderfulfill(self,data):
        try:
            c = self.connection.cursor()
            if "manual" in data:
                q = """UPDATE productorders SET tracking="{t}", fulfilled="2", additional="{a}"  where ordernumber='{o}';""".format(t=data['tracking'],o=str(data['ordernumber']),a=str(data['additional']))
            else:
                q = """UPDATE productorders SET tracking="{t}", fulfilled="1", additional="{a}"  where ordernumber='{o}';""".format(t=data['tracking'],o=str(data['ordernumber']),a=str(data['additional']))
            c.execute(q)
            self.connection.commit()
            return True    
        except Exception as t:
            return False
        
    def orderhistory_get(self,orn):
        c = self.connection.cursor()
        q = f"SELECT history FROM productorders WHERE ordernumber='{orn}';"
        c.execute(q)
        return c.fetchone()

        
    def orderhistory_add(self,data):
        c = self.connection.cursor()
        q = """UPDATE productorders SET history="{o}" where ordernumber="{orn}";""".format(o=str(data['obj']),orn=str(data['ordernumber']))
        c.execute(q)
        self.connection.commit()
        return True
    
    def url_gen(self, content) -> str:
        """
        content: string format url
        Generates encoded friendly url (removes whitespaces and some symbols)
        """
        remove_sym = re.sub(r'[^\w]', ' ', content)
        v = urllib.parse.quote_plus(str(random.randint(10, 50))+remove_sym)
        n = str(v).replace("+", "-")
        g.new_blog_url = n
        return n
    
    def productorders_get(self,q=False,total=False):
        c = self.connection.cursor()
        if total:        
            fetch = c.execute("SELECT Count(*) FROM productorders")
            return fetch.fetchone()
        
        fetch = c.execute(q)
        return fetch.fetchall()
   
    
    def productorders_single_get(self,ids,loadfulfill=False):
        c = self.connection.cursor()
        q = f"SELECT * FROM productorders WHERE id = {ids}"
        if loadfulfill:
            q = f"SELECT * FROM productorders WHERE ordernumber = '{loadfulfill}'"
        fetch = c.execute(q)
        return fetch.fetchone()
    
    def productorders_set(self,order):
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
        except Exception as e:
            return False
        
    def productsettings_smtp(self,data):
        "Updates productsettings shipping opt"
        try:
            c = self.connection.cursor()
            q = f"""UPDATE productsetting SET smtp="{str(data)}";"""
            c.execute(q)
            self.connection.commit()
            return True
        except Exception as e:
            print(e)
            return False
        
    def productsettings_temp(self,data):
        "Updates productsettings shipping opt"
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
         
    def productsettings_ship(self,data):
        "Updates productsettings shipping opt"
        try:
            c = self.connection.cursor()
            q = f"""UPDATE productsetting SET shipping_enable='{data['status']}', shipping_rates='{str(data['shipping'])}', shipping_countries="{data['countries']}";"""
            c.execute(q)
            self.connection.commit()
            return True
        except Exception as e:
            print(e)
            return False
        
    def productsettings_str(self,data):
        "Updates productsettings shipping opt"
        try:
            c = self.connection.cursor()
            q = f"""UPDATE productsetting SET secretkey='{data['sk']}', publishablekey='{data['pk']}', currency='{data['ck']}', webhookkey='{data['wsk']}', signkey='{data['wsk']}';"""
            c.execute(q)
            self.connection.commit()
            return True
        except Exception as e:
            print(e)
            return False

    def productsettings_set(self, sk, pk, ck, wk,wsk,s_enable,s_rates,s_countries) -> tuple:
        "Unused func, will delete soon"
        try:
            c = self.connection.cursor()
            q = """UPDATE productsetting SET secretkey = "{sk}", publishablekey = "{pk}", currency = "{ck}", webhookkey = "{wk}",signkey = "{wsk}", shipping_enable = "{se}", shipping_rates = '{sr}', shipping_countries = "{sc}" WHERE id = 1; """.format(
                sk=sk, pk=pk, ck=ck,wk=wk,wsk=wsk,se=s_enable,sr=s_rates,sc=s_countries)
            c.execute(q)
            self.connection.commit()
            return True
        except Exception as e:
            print("Error: ",e)
            return False

    def productsettings_get(self) -> tuple:
        """Product settings db table has to be premade"""
        c = self.connection.cursor()
        q = "SELECT * FROM productsetting where id=1"
        fetch = c.execute(q)
        return fetch.fetchone()

    def productimagesupdater(self, imgcat: str, data: dict, newimage: str, filename: str) -> tuple:
        """
        Loads data from product table
        pars: variants, images, mainimage
        trigger: uploader (images)
        """
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

    def productmainupdater(self, imgcat: str, data: dict, newimage: str, filename: str) -> tuple:
        """
        Loads data from product table
        pars: variants, images, mainimage
        trigger: uploader (main)
        """
        _c = self.connection.cursor()
        m_fetch = _c.execute(
            "SELECT {sel} FROM products WHERE product_id='{m}'".format(
                sel=imgcat, m=data['p_id'])
            )
        _old = m_fetch.fetchone()
        try:
            _inserts = """UPDATE products SET mainimage = "{mainm}" WHERE product_id = '{product_id}'""".format(
                mainm=filename, product_id=data['p_id'])
            _c.execute(_inserts)
            self.connection.commit()
            return True
        except Exception as e:
            print(e)
            return False

    def productvariantsupdater(self, imgcat: str, data: dict, newimage: str) -> tuple:
        """
        Loads data from product table
        pars: variants, images, mainimage
        trigger: uploader (variant)
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
            print(e)
            return False

    def productsimilar(self, count=5, category=0):
        """
        Loads similar products, adds random
        if category length is not enough to given count
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
        except Exception as e:
            print(f"productimagesmod() error: {e}")
            return False

    def delete_pr(self, value) -> bool:
        q = """DELETE FROM products WHERE product_id = '{value}';""".format(
            value=value)
        c = self.connection.cursor()

        try:
            c.execute(q)
            self.connection.commit()
            self.log("Product deleted")
            return True
        except Exception as e:
            print(e)
            return False

    def delete_apip(self, table, column, value) -> bool:
        print(table, column, value)
        q = """DELETE FROM {tb} WHERE product_urlsystem = '{value}';""".format(
            tb=table, column=column, value=value)
        c = self.connection.cursor()

        try:
            c.execute(q)
            self.connection.commit()
            self.log("Product deleted")
            return True
        except Exception as e:
            print(e)
            return False

    def delete_api(self, table, column, value) -> bool:
        print(table, column, value)
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

    def product_update(self, d) -> bool:
        c = self.connection.cursor()
        q = f"""UPDATE products SET body = "{d['body']}",category = "{d['category']}",images = "{d['images']}", mainimage = "{d['mainimage']}", price = "{d['price']}", product_url = "{d['product_url']}", product_urlsystem = "{d['product_urlsystem']}",  seo_description = "{d['seo_description']}", seo_keywords = "{d['seo_keywords']}",  title = "{d['title']}",  variant_details = "{d['variant_details']}", variants = "{d['variants']}", hidden = "{d['hidden']}" WHERE product_id = "{d['id']}";"""
        try:
            c.execute(q)
            self.connection.commit()
            return d['product_urlsystem']
        except Exception as e:
            print("Error ", e)
            return False

    def product_publish(self, d) -> bool:
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
        except Exception as e:
            print("Error ", e)
            return False

    def delete_image_partial(self, data):
        c = self.connection.cursor()
        try:
            os.remove(os.path.join(UPLOAD_FOLDER_BLOG, data['image']))
        except:
            pass
        q = "UPDATE blog SET image = '' WHERE route = '{r}';".format(
            r=data['route'])
        c.execute(q)
        self.connection.commit()

    def get_product_single(self, route, checkout=False):
        c = self.connection.cursor()
        if checkout:
            m = c.execute(
                "SELECT * FROM products WHERE product_id='{m}'".format(m=checkout))
        else:
            m = c.execute(
                "SELECT * FROM products WHERE product_urlsystem='{m}'".format(m=route))
        return m.fetchone()

    def get_product_listings(self, getcount=False,getcats=False,quer=[],custom={}):
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
        c.fetchall()

    def blog_publish(self, dicts) -> bool:
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
        except Exception as e:
            print("Error ", e)
            return False

    def blog_update(self, dicts) -> bool:
        c = self.connection.cursor()
        try:
            q = "UPDATE blog SET title = '{title}',message = '{message}', image = '{image}',hidden = '{hidden}', category = '{category}' WHERE route = '{route}';".format(
                title=dicts['title'], message=dicts['body'], image=dicts['image'], hidden=dicts['hidden'], category=dicts['category'], route=dicts['route'])
            c.execute(q)
            self.connection.commit()
            return True
        except Exception as e:
            print("Error ", e)
            return False


    def get_blog_single(self, route) -> tuple:
        c = self.connection.cursor()
        m = c.execute(
            "SELECT * FROM blog WHERE route='{m}'".format(m=route))
        return m.fetchone()

    def get_blog_listings(self, page=0, result=10,getcount=False,quer=[]) -> list:        
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
            print(e)
            self.log("API DB Update failed")
            return False

    def timestamp(self, routeStyle=False) -> str:
        """
        Returns timestamp
        """
        _n = datetime.datetime.now()
        d_ = str(_n).split()
        dt = d_[0]
        t = time.strftime("%I:%M %p")
        ts = dt + " " + t
        if routeStyle:
            return dt
        return ts

    def message(self, dicts) -> bool:
        try:
            params = "INSERT INTO messages (name,email,message,phone,timestamp) VALUES (?,?,?,?,?)"
            vals = (dicts['name'], dicts['email'],
                    dicts['message'], dicts['phone'], self.timestamp())
            self.cursor.execute(params, vals)
            self.connection.commit()
            return True
        except Exception as e:
            print("Error ", e)
            return False

    def delete_blog(self, route):
        c = self.connection.cursor()
        try:
            q = "DELETE FROM blog WHERE route = {id};".format(id=route)
            c.execute(q)
            self.connection.commit()
            self.log("Blog post deleted #id "+id)
            return True
        except Exception as e:
            self.log("Unable to delete blog post, "+str(e))
            return False

    def ddelete(self, table, id):
        c = self.connection.cursor()
        try:
            q = "DELETE FROM {table} WHERE id = {id};".format(
                table=table, id=id)
            c.execute(q)
            self.log("Message deleted #id "+id)
            self.connection.commit()
            return True
        except Exception as e:
            self.log("Unable to delete message, "+str(e))
            return False

    def log(self, message) -> bool:
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
            print("Error ", e)
            return False

    # def closedb(self):
    #     """
    #     Need to be close out of scope
    #     """
    #     self.connection.close()

    def update_data_uploads(self, table, column, newvalue, where, whereequal):
        """
        Update existing data
        """
        c = self.connection.cursor()
        q = "UPDATE {table} SET {column} = '{value}' WHERE {where} = '{whereequal}';".format(
            table=table, column=column, value=newvalue, where=where, whereequal=whereequal
        )
        c.execute(q)
        self.connection.commit()
        return {"status": "success"}

    def update_websitesettings(self, dicts, owner) -> bool:
        """
        Website settings
        """
        c = self.connection.cursor()
        try:
            q = "UPDATE control SET sitename = '{sitename}',sitedescription = '{sitedescription}',footercopyright = '{footercopyright}',meta_description = '{meta_description}',meta_keywords = '{meta_keywords}', sitenumber = '{sitenumber}', siteemail='{siteemail}', siteaddress='{siteaddress}' WHERE owner = '{owner}';".format(
                sitename=dicts['sitename'], sitedescription=dicts['description'], footercopyright=dicts['footercopyright'], meta_description=dicts['meta_description'], meta_keywords=dicts['meta_keywords'],sitenumber=dicts['sitenumber'],siteemail=dicts['siteemail'],siteaddress=dicts['siteaddress'],owner=owner)
            c.execute(q)
            self.connection.commit()
            return True
        except Exception as e:
            print("update_wsettings() error ", e)
            return False

    def update_module(self, data) -> bool:
        """
        Update module data
        """
        import json
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
        except Exception as e:
            print(e)
            return False

    def update_credential(self, uname, newpwd) -> bool:
        """
        Only for Account password update
        """
        c = self.connection.cursor()
        try:
            q = "UPDATE users SET passw = '{value}' WHERE username = '{uname}';".format(
                value=newpwd, uname=uname)
            c.execute(q)
            self.connection.commit()
            return True
        except Exception as e:
            print("update_credential() error ", e)
            return False

    def get_messages(self) -> tuple:
        c = self.connection.cursor()
        m = c.execute(
            "SELECT * FROM messages ORDER BY id DESC")
        return m.fetchall()

    def get_logs(self) -> tuple:
        c = self.connection.cursor()
        m = c.execute(
            "SELECT * FROM logging ORDER BY id DESC")
        return m.fetchall()

    def get_cred(self, username, passw) -> tuple:
        c = self.connection.cursor()
        m = c.execute("SELECT * FROM users")
        return m.fetchall()

    def load_modules_settings(self) -> tuple:
        c = self.connection.cursor()
        m = c.execute("SELECT * FROM modules")
        return m.fetchall()

    def load_data_index(self, which) -> tuple:
        """
        Loads data from DB, function calls in main page
        """
        c = self.connection.cursor()
        self.fetch_control = c.execute("SELECT * FROM control")
        self.site_data = self.fetch_control.fetchall()
        self.fetch_msg = c.execute("SELECT * FROM messages")
        self.site_msgs = self.fetch_msg.fetchall()

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

