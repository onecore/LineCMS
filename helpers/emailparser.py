"""
SandCMS - Content Management System (Product & Blogging) for Rapid website development
Website: www.sandcms.com
Author: S. Jangra & Mark A.R. Pequeras
"""
from ast import literal_eval as le
import dataengine
from jinja2 import Template
from decimal import Decimal
from flask import current_app

d = dataengine.SandEngine()
logger = d.log

sk, pk, ck, _, wk, wsk,shipstatus,shiprates,shipcountries,_,_,_,_,sender,_ = d.productsettings_get()

def price(price) -> int:
    "parces stripe int into decimal (unlike float this keeps the 2 decimal places)"
    o = round(Decimal(price)*100) 
    return o

def data(which,order,company,shipstatus=False,tracking=False,additional=False) -> dict:
    """adds all the jinja templating values"""
    formatter = {
                "COMPANYNAME":company['sitename'],"COMPANYNUMBER":company['sitenumber'],"COMPANYEMAIL":company['siteemail'],
                "ORDERNUMBER":order['ordernumber'],"ORDERTOTAL":order['amount_total'],"ORDERDATE":order['created'],"CUSTOMERADDRESS":order['address'],"CUSTOMERNAME":order['customer_name']
            }
    if tracking:
        formatter['TRACKINGLINK'] = tracking
    
    if additional:
        formatter['ADDITIONAL'] = additional

    return formatter

def parse_send(**kwargs) -> bool:
    "parses data into email friendly format"   
     
    with current_app.app_context(): # Cannot import from flask app obj without this
        from app import sendmail        
        
    if kwargs:
        try:
            tracking,additional,shipstatus = False,False,False

            temps = {"fulfilled": kwargs['ps'][9],"placed": kwargs['ps'][10]}
            subobj = {"fulfilled": f"Hi {kwargs['order']['customer_name']} Your order is on the way! ", "placed": f"Hi {kwargs['order']['customer_name']} Your order is placed! "}
            
            # t_settings = le(kwargs['ps'][12])
            if "template" in kwargs: # Change template to Custom template
                if kwargs['template']:
                    temps[kwargs['which']] = kwargs['template']
            
            if "tracking" in kwargs:
                tracking = kwargs['tracking']
            
            if "additional" in kwargs:
                additional = kwargs['additional']

            if "shipstatus" in kwargs:
                shipstatus = kwargs['shipstatus']

            template = Template(temps[kwargs['which']])
            rendered = template.render(data(kwargs['which'],kwargs['order'],kwargs['company'],shipstatus=shipstatus,tracking=tracking,additional=additional)) # tracking is False (perfect for fulfilled call)
            
            subject = subobj[kwargs['which']]
            recip = kwargs['order']['customer_email']
            sendr = le(kwargs['ps'][13])['email']
            sendmail(subject=subject,reciever=recip,html=rendered,sender=sendr)
                
        except Exception as e:
            print("err: ",e)
            return False
        