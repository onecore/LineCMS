"""
LineCMS - Content Management System (Product & Blogging) for Rapid website development
Website: www.linecms.com
Author: S. Jangra & Mark A.R. Pequeras
"""
import json
import settings as temple
from flask import jsonify, url_for, session
from ast import literal_eval as lite
import dataengine as de
from helpers import dataparser

ps = de.SandEngine()

def ks_badge_insert(v) -> str:
    """badgify strings

    Args:
        v: list
    Returns:
        str: badged string
    """    
    q = ""
    if "," in v:
        if v:
            i = str(v).split(",")
            for cat in i:
                q += f"<badge class='badge {temple.sc_badge_insert}'>{cat}</badge>&nbsp"
    return q

def ks_include_adminbutton() -> str:
    """admin button

    Returns:
        str: html button (bootstrap)
    """
    v = f"&nbsp&nbsp<a href='{temple.route_dashboard}' class='btn {temple.sc_admin_button}' style='color:white'>Owner Dashboard</a>"
    if "authenticated" in session:
        if session['authenticated']:
            return v
    return ""

def ks_html2text(v) -> str:
    """html to plain

    Args:
        v: str
    Returns:
        str: html to text
    """    
    from lxml import html
    if v:
        return html.fromstring(v).text_content()
    return ""

def ks_html2text_truncate(v,custom=[]) -> str:
    """html to plain with truncate

    Args:
        v: str
        custom: concat right and left e.g [:210,210:]
    Returns:
        str: html to text with truncated txt
    """    
    from lxml import html
    if v:
        ret = html.fromstring(v).text_content()
        trunc = ret[:210] + (ret[210:] and '..')
        if custom:
            trunc = ret[custom[0]] + (ret[custom[1]] and '..')
        return trunc
    return ""

def ks_tolist(v) -> list:
    "cast to list"  
    return lite(v)

def ks_todict(v) -> dict:
    "cast to dict"
    try:
        return lite(v)
    except:
        return {}

def ks_getdictkeys(v) -> list:
    "returns list of keys from a dict with k/v"
    o = []
    p = jsonify(v)
    for k, v in p.items():
        o.append(k)
    return lite(o)

def ks_variantcount(v) -> int:
    "return variant's length"
    if len(v) > 2:
        p = lite(v)
        return len(p.keys())
    return 0

def ks_tojson(v) -> dict:
    "python dict obj to json"
    return json.dumps(v)

def link_for(theme, path):
    "returns static path"
    return url_for("static",filename=f"SYSTEM/{theme}/{path}")

def version():
    "returns string version/date built"
    return temple.cms_version, temple.cms_date
    
# public

def load_blogs(counts=[0,5], single=None) -> tuple:
    """_summary_

    Args:
        count (int [offset,offset], optional): modifies limit. Defaults to 5.
        single (str, optional): blog route, loads single blog post. Defaults to None.

    Returns:
        tuple: _description_
    """
    if single:
        _d = ps.get_blog_single(single)
        _p = dataparser.Obj("blog",_d)
        return _p
    else:
        _d = ps.get_blog_listings(quer=counts)
        print(_d)
        return _d


def load_products(single=False,search=None, category=None, counts=[0,3]) -> tuple: 
    """Load Products (Jinja usage) inline loader for template usage
    Args:
        single (str, optional): product_id. Defaults to False.
        search (str, optional): string search. Defaults to None.
        category (str, optional): categorize search_. Defaults to None.
        offset (int, optional): offset search. Defaults to 0.
        per_page (int, optional): per_page for navigation. Defaults to 3.

    Returns:
        single: returns class Obj
        ** else: returns tuple
    """
    if single:
        _p = dataparser.Obj('product',ps.get_product_single(single))
        return _p
    products = ps.get_product_listings(custom={"s":search,"c":category,"off":counts[0],"perp":counts[1]})
    return products