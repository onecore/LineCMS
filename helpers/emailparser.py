from ast import literal_eval as le
import dataengine
import settings
from flask import render_template
from jinja2 import Template

d = dataengine.knightclient()
log = d.log

def data(which,order,company):
    fulfilled = {
                "COMPANYNAME":company['sitename'],"COMPANYNUMBER":"","COMPANYEMAIL":"","TRACKINGLINK":"",
                "ORDERNUMBER":"","ORDERTOTAL":"","ORDERDATE":"","CUSTOMERADDRESS":"","CUSTOMERNAME":""
                }
    
    placed = {
                "COMPANYNAME":"","COMPANYNUMBER":"","COMPANYEMAIL":"",
                "ORDERNUMBER":"","ORDERTOTAL":"","ORDERDATE":"","CUSTOMERADDRESS":"","CUSTOMERNAME":""
            }
    
    w = {"fulfilled":fulfilled,"placed":placed}
    return w[which]

def parse_send(**kwargs) -> bool:    
    if kwargs:
        try:
            temps = {"fulfilled": kwargs['ps'][9],"placed": kwargs['ps'][10]}
            t_settings = le(kwargs['ps'][12])
            template = Template(temps[kwargs['which']])
            rendered = template.render(data(kwargs['which'],kwargs['order'],kwargs['company']))
            print(rendered)
                
        except Exception as e:
            print(">>>",e)
            return False
        