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

UPLOAD_FOLDER_PRODUCTS = 'static/dashboard/uploads/products'
UPLOAD_FOLDER_BLOG = 'static/dashboard/uploads/blog'


class knightclient:

    connection = sqlite3.connect("db/knightstudio", check_same_thread=False)
    # cursor = connection.cursor()

    def themeset(self, theme):
        _c = self.connection.cursor()
        q = f"UPDATE control SET theme = '{theme}'"
        _c.execute(q)
        self.connection.commit()

    def themeget(self):
        """Product settings db table has to be premade"""
        _c = self.connection.cursor()
        _q = "SELECT theme FROM control"
        _fetch = _c.execute(_q)
        _r = _fetch.fetchone()
        return _r

    def url_gen(self, content) -> str:
        """
        content: string format url
        Generates encoded friendly url (removes whitespaces and some symbols)
        """
        remove_sym = re.sub(r'[^\w]', ' ', content)
        v = urllib.parse.quote_plus(str(random.randint(10, 50))+remove_sym)
        _v = str(v).replace("+", "-")
        g.new_blog_url = _v
        return _v

    def productsettings_set(self, sk, pk, ck) -> tuple:
        try:
            _c = self.connection.cursor()
            _q = """UPDATE productsetting SET secretkey = "{sk}", publishablekey = "{pk}", currency = "{ck}" WHERE id = 1; """.format(
                sk=sk, pk=pk, ck=ck)
            _c.execute(_q)
            self.connection.commit()
            return True
        except:
            return False

    def productsettings_get(self) -> tuple:
        """Product settings db table has to be premade"""
        _c = self.connection.cursor()
        _q = "SELECT * FROM productsetting where id=1"
        _fetch = _c.execute(_q)
        _r = _fetch.fetchone()
        return _r

    def productimagesupdater(self, imgcat: str, data: dict, newimage: str, filename: str) -> tuple:
        """
        Loads data from product table
        pars: variants, images, mainimage
        trigger: uploader (images)
        """
        _c = self.connection.cursor()
        m_fetch = _c.execute(
            "SELECT {sel} FROM products WHERE product_id='{m}'".format(
                sel=imgcat, m=data['p_id'])
            )
        try:
            _old = m_fetch.fetchone()
            _dblist_ = eval(_old[0])
            if filename not in _dblist_:  # new file add to db
                ic("not in list adding now")
                ic("old: ", _dblist_)
                _dblist_.append(filename)
                _inserts = """UPDATE products SET images = "{i}" WHERE product_id = '{product_id}'""".format(
                    i=_dblist_, product_id=data['p_id'])
                ic("new ", _dblist_)
                _c.execute(_inserts)
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
            count = count - 1

        if len(pr) < count:
            self.mr_fetch = _c.execute(
                "SELECT * FROM products ORDER BY random() LIMIT {l};".format(l=count))
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
            _c = self.connection.cursor()
            _inserts = """UPDATE products SET variants = '{variants}' WHERE product_id = '{product_id}'""".format(
                variants=variants, product_id=product_id)
            _c.execute(_inserts)
            self.connection.commit()
            return True
        except Exception as e:
            print(f"productimagesmod() error: {e}")
            return False

    def delete_pr(self, value) -> bool:
        q = """DELETE FROM products WHERE product_id = '{value}';""".format(
            value=value)
        _c = self.connection.cursor()

        try:
            _c.execute(q)
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
        _c = self.connection.cursor()

        try:
            _c.execute(q)
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
        _c = self.connection.cursor()

        try:
            _c.execute(q)
            self.connection.commit()
            self.log("Blog deleted")
            return True
        except Exception as e:
            print(e)
            return False

    def product_update(self, d) -> bool:
        _c = self.connection.cursor()
        params = f"""UPDATE products SET body = "{d['body']}",category = "{d['category']}",images = "{d['images']}", mainimage = "{d['mainimage']}", price = "{d['price']}", product_url = "{d['product_url']}", product_urlsystem = "{d['product_urlsystem']}",  seo_description = "{d['seo_description']}", seo_keywords = "{d['seo_keywords']}",  title = "{d['title']}",  variant_details = "{d['variant_details']}", variants = "{d['variants']}", hidden = "{d['hidden']}" WHERE product_id = "{d['id']}";"""
        ic(params)
        try:
            _c.execute(params)
            self.connection.commit()
            ic("Product Update success")
            return d['product_urlsystem']
        except Exception as e:
            print("Error ", e)
            return False

    def product_publish(self, d) -> bool:
        _c = self.connection.cursor()
        try:
            ts = self.timestamp(routeStyle=1)
            tso = self.timestamp(routeStyle=0)
            ugen = self.url_gen(ts+" "+d['title'])
            params = "INSERT INTO products (title,category,variants,product_url,product_urlsystem,seo_description,seo_keywords,images,mainimage,variant_details,timestamp,hidden,product_id,body,price) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)"
            vals = (d['title'], d['category'], str(d['variants']), d['product_url'], ugen,
                    d['seo_description'], d['seo_keywords'], str(d['images']), d['mainimage'], str(d['variant_details']), ts, "0", d['id'], d['body'], d['price'])
            _c.execute(params, vals)
            self.connection.commit()
            return ugen
        except Exception as e:
            print("Error ", e)
            return False

    def product_manage(self):
        pass

    def delete_image_partial(self, data):
        _c = self.connection.cursor()

        try:
            os.remove(os.path.join(UPLOAD_FOLDER_BLOG, data['image']))
        except:
            pass

        q = "UPDATE blog SET image = '' WHERE route = '{r}';".format(
            r=data['route'])
        _c.execute(q)
        self.connection.commit()
        print("Done")

    def get_product_single(self, route):
        _c = self.connection.cursor()
        self.m_fetch = _c.execute(
            "SELECT * FROM products WHERE product_urlsystem='{m}'".format(m=route))
        self.m_data = self.m_fetch.fetchone()
        return self.m_data

    def get_product_listings(self, page=0, result=10):
        _c = self.connection.cursor()
        self.m_fetch = _c.execute("SELECT * FROM products ORDER BY id DESC")
        self.m_data = self.m_fetch.fetchall()
        return self.m_data

    def blog_publish(self, dicts) -> bool:
        _c = self.connection.cursor()
        try:
            ts = self.timestamp(routeStyle=1)
            tso = self.timestamp(routeStyle=0)
            params = "INSERT INTO blog (title,message,image,timestamp,hidden,route,category) VALUES (?,?,?,?,?,?,?)"
            vals = (dicts['title'], dicts['body'], dicts['image'],
                    tso, "0", self.url_gen(ts+" "+dicts['title']), dicts['category'])
            _c.execute(params, vals)
            self.connection.commit()
            return True
        except Exception as e:
            print("Error ", e)
            return False

    def blog_update(self, dicts) -> bool:
        _c = self.connection.cursor()
        try:
            q = "UPDATE blog SET title = '{title}',message = '{message}', image = '{image}',hidden = '{hidden}', category = '{category}' WHERE route = '{route}';".format(
                title=dicts['title'], message=dicts['body'], image=dicts['image'], hidden=dicts['hidden'], category=dicts['category'], route=dicts['route'])
            _c.execute(q)
            self.connection.commit()
            return True
        except Exception as e:
            print("Error ", e)
            return False

    def blog_manage(self):
        pass

    def get_blog_single(self, route) -> tuple:
        _c = self.connection.cursor()
        self.m_fetch = _c.execute(
            "SELECT * FROM blog WHERE route='{m}'".format(m=route))
        self.m_data = self.m_fetch.fetchone()
        return self.m_data

    def get_blog_listings(self, page=0, result=10) -> list:
        _c = self.connection.cursor()
        self.m_fetch = _c.execute("SELECT * FROM blog ORDER BY id DESC")
        self.m_data = self.m_fetch.fetchall()
        return self.m_data

    def get_blog_cat_lists(self) -> list:
        _c = self.connection.cursor()
        self.m_fetch = _c.execute("SELECT category FROM blog")
        self.m_data = self.m_fetch.fetchall()
        cats = {}
        for cat in self.m_data:
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
            _c = self.connection.cursor()
            a = {
                "dlogs": """DELETE FROM logging""",
                }
            _c.execute(a[action])
            return True
        except:
            return False

    def knightclientapiv2(self, action) -> bool:
        _c = self.connection.cursor()
        print(action)
        _where = action['where']
        _action = action['action']

        try:
            a = {
                "blog_0": """UPDATE blog SET hidden = '0' WHERE route = '{r}';""".format(r=_where),
                "blog_1": """UPDATE blog SET hidden = '1' WHERE route = '{r}';""".format(r=_where),
                }
            _c.execute(a[str(_action)])
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
        _c = self.connection.cursor()
        try:
            q = "DELETE FROM blog WHERE route = {id};".format(id=route)
            _c.execute(q)
            self.log("Blog post deleted #id "+id)
        except Exception as e:
            self.log("Unable to delete blog post, "+str(e))

    def delete(self, table, id):
        _c = self.connection.cursor()
        try:
            q = "DELETE FROM {table} WHERE id = {id};".format(
                table=table, id=id)
            _c.execute(q)
            self.log("Message deleted #id "+id)
        except Exception as e:
            self.log("Unable to delete message, "+str(e))

    def log(self, message) -> bool:
        _c = self.connection.cursor()
        try:
            params = "INSERT INTO logging (log,timestamp) VALUES (?,?)"
            vals = (message, self.timestamp())
            _c.execute(params, vals)
            self.connection.commit()
            return True
        except Exception as e:
            print("Error ", e)
            return False

    def closedb(self):
        """
        Need to be close out of scope
        """
        self.connection.close()

    def update_data_uploads(self, table, column, newvalue, where, whereequal):
        """
        Update existing data
        """
        _c = self.connection.cursor()
        q = "UPDATE {table} SET {column} = '{value}' WHERE {where} = '{whereequal}';".format(
            table=table, column=column, value=newvalue, where=where, whereequal=whereequal
        )
        _c.execute(q)
        self.connection.commit()
        return {"status": "success"}

    def update_websitesettings(self, dicts, owner) -> bool:
        """
        Website settings
        """
        _c = self.connection.cursor()
        try:
            q = "UPDATE control SET sitename = '{sitename}',sitedescription = '{sitedescription}',footercopyright = '{footercopyright}',meta_description = '{meta_description}',meta_keywords = '{meta_keywords}' WHERE owner = '{owner}';".format(
                sitename=dicts['sitename'], sitedescription=dicts['description'], footercopyright=dicts['footercopyright'], meta_description=dicts['meta_description'], meta_keywords=dicts['meta_keywords'], owner=owner)
            _c.execute(q)
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
        _c = self.connection.cursor()
        try:
            data = eval(data)
            copy_data = data.copy()
            del data['module']
            se = json.dumps(data)
            q = """UPDATE modules SET '{module}' = '{new}'""".format(
                module=copy_data['module'], new=se)
            _c.execute(q)
            self.connection.commit()
            self.log("KSEngine Module update success "+copy_data['module'])
            return True
        except Exception as e:
            print(e)
            self.log("KSEngine Module update failed "
                     + copy_data['module']+" "+str(e))
            return False

    def update_credential(self, uname, newpwd) -> bool:
        """
        Only for Account password update
        """
        _c = self.connection.cursor()
        try:
            q = "UPDATE users SET passw = '{value}' WHERE username = '{uname}';".format(
                value=newpwd, uname=uname)
            _c.execute(q)
            self.connection.commit()
            return True
        except Exception as e:
            print("update_credential() error ", e)
            return False

    def get_messages(self) -> tuple:
        _c = self.connection.cursor()
        self.m_fetch = _c.execute(
            "SELECT * FROM messages ORDER BY id DESC")
        self.m_data = self.m_fetch.fetchall()
        return self.m_data

    def get_logs(self) -> tuple:
        _c = self.connection.cursor()
        self.m_fetch = _c.execute(
            "SELECT * FROM logging ORDER BY id DESC")
        self.m_data = self.m_fetch.fetchall()

        return self.m_data

    def get_cred(self, username, passw) -> tuple:
        _c = self.connection.cursor()
        self.gc_fetch = _c.execute("SELECT * FROM users")
        self.gc_data = self.gc_fetch.fetchall()

        return self.gc_data

    def load_modules_settings(self) -> tuple:
        _c = self.connection.cursor()
        self.ld = _c.execute("SELECT * FROM modules")
        self.ld_all = self.ld.fetchall()
        return self.ld_all

    def load_data_index(self, which) -> tuple:
        """
        Loads data from DB, function calls in main page
        """
        _c = self.connection.cursor()
        self.fetch_control = _c.execute("SELECT * FROM control")
        self.site_data = self.fetch_control.fetchall()
        self.fetch_msg = _c.execute("SELECT * FROM messages")
        self.site_msgs = self.fetch_msg.fetchall()
        # site_type:
        # 0 - Restaurant (Single Menu)
        # 1 - Restaurant (Multi Menu)
        # 2 - Article/Blog style
        # 3 - Shopping site
        # 4 - Business
        # 99 - Load ALL
        all_data = {  # 0 - Off, 1 - On
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
        }
        # adds menu_list in dict if either single, multi, otherwise False
        if "0" in all_data['site_type']:  # single
            self.menu = _c.execute("SELECT * FROM menu_single")
            all_data['menu_list'] = self.menu.fetchall()
        elif "1" in all_data['site_type']:  # multi
            self.menu = _c.execute("SELECT * FROM menu")
            all_data['menu_list'] = self.menu.fetchall()
        # Add more condition depends on site_type
        return all_data

    def insert_data(self, quer):
        pass
        pass
