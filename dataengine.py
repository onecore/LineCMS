import sqlite3
import datetime
import time
import urllib


class knightclient:

    connection = sqlite3.connect("knightstudio", check_same_thread=False)
    cursor = connection.cursor()

    def url_gen(self, content):
        return urllib.parse.quote_plus(content)

    def product_publish(self, data):
        pass

    def product_manage(self):
        pass

    def get_product_single(self, route):
        pass

    def get_product_listings(self, page=0, result=10):
        pass

    def blog_publish(self, dicts):
        try:
            ts = self.timestamp(routeStyle=1)
            params = "INSERT INTO blog (title,message,image,timestamp,hidden,route,category) VALUES (?,?,?,?,?,?,?)"
            vals = (dicts['title'], dicts['body'], dicts['image'],
                    ts, "0", self.url_gen(ts+" "+dicts['title']), dicts['category'])
            self.cursor.execute(params, vals)
            self.connection.commit()
            return True
        except Exception as e:
            print("Error ", e)
            return False

    def blog_manage(self):
        pass

    def get_blog_single(self, route):
        pass

    def get_blog_listings(self, page=0, result=10):
        pass

    def knightclientapi(self, action):
        a = {
            "dlogs": """DELETE FROM logging""",
            }
        self.cursor.execute(a[action])
        return True

    def timestamp(self, routeStyle=False):
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

    def message(self, dicts):
        try:
            params = "INSERT INTO messages (name,email,message,phone,timestamp) VALUES (?,?,?,?,?)"
            vals = (dicts['name'], dicts['email'],
                    dicts['message'], dicts['phone'], self.timestamp())
            print(params, vals)
            self.cursor.execute(params, vals)
            self.connection.commit()
            return True
        except Exception as e:
            print("Error ", e)
            return False

    def delete(self, table, id):
        try:
            q = "DELETE FROM {table} WHERE id = {id};".format(
                table=table, id=id)
            self.cursor.execute(q)
            self.log("Message deleted #id "+id)
        except Exception as e:
            self.log("Unable to delete message, "+str(e))

    def log(self, message):
        try:
            params = "INSERT INTO logging (log,timestamp) VALUES (?,?)"
            vals = (message, self.timestamp())
            self.cursor.execute(params, vals)
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
        q = "UPDATE {table} SET {column} = '{value}' WHERE {where} = '{whereequal}';".format(
            table=table, column=column, value=newvalue, where=where, whereequal=whereequal
        )
        print(q)
        self.cursor.execute(q)
        self.connection.commit()
        return {"status": "success"}

    def update_websitesettings(self, dicts, owner):
        """
        Website settings
        """
        try:
            q = "UPDATE control SET sitename = '{sitename}',sitedescription = '{sitedescription}',footercopyright = '{footercopyright}',meta_description = '{meta_description}',meta_keywords = '{meta_keywords}' WHERE owner = '{owner}';".format(
                sitename=dicts['sitename'], sitedescription=dicts['description'], footercopyright=dicts['footercopyright'], meta_description=dicts['meta_description'], meta_keywords=dicts['meta_keywords'], owner=owner)
            print(q)
            self.cursor.execute(q)
            print("update success")
            self.connection.commit()
            return True
        except Exception as e:
            print("update_wsettings() error ", e)
            return False

    def update_module(self, data):
        """
        Update module data
        """
        import json
        try:
            data = eval(data)
            copy_data = data.copy()
            del data['module']
            se = json.dumps(data)

            q = """UPDATE modules SET '{module}' = '{new}'""".format(
                module=copy_data['module'], new=se)

            self.cursor.execute(q)
            self.connection.commit()
            self.log("KSEngine Module update success "+copy_data['module'])
            return True

        except Exception as e:
            print(e)
            self.log("KSEngine Module update failed "
                     + copy_data['module']+" "+str(e))
            return False

    def update_credential(self, uname, newpwd):
        """
        Only for Account password update
        """
        try:
            q = "UPDATE users SET passw = '{value}' WHERE username = '{uname}';".format(
                value=newpwd, uname=uname)
            print(q)
            self.cursor.execute(q)
            print("update success")
            self.connection.commit()
            return True
        except Exception as e:
            print("update_credential() error ", e)
            return False

    def get_messages(self):
        self.m_fetch = self.cursor.execute(
            "SELECT * FROM messages ORDER BY id DESC")
        self.m_data = self.m_fetch.fetchall()
        return self.m_data

    def get_logs(self):
        self.m_fetch = self.cursor.execute(
            "SELECT * FROM logging ORDER BY id DESC")
        self.m_data = self.m_fetch.fetchall()

        return self.m_data

    def get_cred(self, username, passw):
        self.gc_fetch = self.cursor.execute("SELECT * FROM users")
        self.gc_data = self.gc_fetch.fetchall()

        return self.gc_data

    def load_modules_settings(self):
        self.ld = self.cursor.execute("SELECT * FROM modules")
        self.ld_all = self.ld.fetchall()
        return self.ld_all

    def load_data_index(self, which):
        """
        Loads data from DB, function calls in main page
        """
        self.fetch_control = self.cursor.execute("SELECT * FROM control")
        self.site_data = self.fetch_control.fetchall()
        self.fetch_msg = self.cursor.execute("SELECT * FROM messages")
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
            self.menu = self.cursor.execute("SELECT * FROM menu_single")
            all_data['menu_list'] = self.menu.fetchall()
        elif "1" in all_data['site_type']:  # multi
            self.menu = self.cursor.execute("SELECT * FROM menu")
            all_data['menu_list'] = self.menu.fetchall()
        # Add more condition depends on site_type
        return all_data

    def insert_data(self, quer):
        pass
