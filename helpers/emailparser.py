from ast import literal_eval as le
import dataengine
import settings
from flask import render_template
from jinja2 import Template
from decimal import Decimal
from flask_mail import Message, Mail
from flask import jsonify
from flask import current_app

# from app import sendmail
d = dataengine.knightclient()
logger = d.log

sk, pk, ck, _, wk, wsk,shipstatus,shiprates,shipcountries,_,_,_,_,sender,_ = d.productsettings_get() # wk is not needed



def price(price) -> int:
    "Stripe friendly price"
    o = round(Decimal(price)*100) # Decimal to keep 2 decimal places from html input, Float doesn't work as it doesn keep the decimals
    return o

def data(which,order,company,shipstatus,tracking=False):
    "tracking parameter only for fulfilled template"
    formatter = {
                "COMPANYNAME":company['sitename'],"COMPANYNUMBER":company['sitenumber'],"COMPANYEMAIL":company['siteemail'],
                "ORDERNUMBER":order['ordernumber'],"ORDERTOTAL":order['amount_total'],"ORDERDATE":order['created'],"CUSTOMERADDRESS":order['address'],"CUSTOMERNAME":order['customer_name']
            }
    if tracking:
        formatter['TRACKINGLINK'] = tracking
    return formatter

def parse_send(**kwargs) -> bool:    
    with current_app.app_context():
        from app import sendmail        
        
    if kwargs:
        try:
            temps = {"fulfilled": kwargs['ps'][9],"placed": kwargs['ps'][10]}
            subobj = {"fulfilled": f"Hi {kwargs['order']['customer_name']} Your order is on the way! ", "placed": f"Hi {kwargs['order']['customer_name']} Your order is placed! "}
            
            t_settings = le(kwargs['ps'][12])
            if "template" in kwargs: # Change template template
                temps[kwargs['which']] = kwargs['template']
                
            template = Template(temps[kwargs['which']])
            rendered = template.render(data(kwargs['which'],kwargs['order'],kwargs['company'],False))
            
            subject = subobj[kwargs['which']]
            recip = kwargs['order']['customer_email']
            sendr = le(kwargs['ps'][13])['email']
            
            sendmail(subject=subject,reciever=recip,html=rendered,sender=sendr)
                
        except Exception as e:
            return False
        