"""
LineCMS - Content Management System (Product & Blogging) for Rapid website development
Website: www.linecms.com
Author: S. Jangra & Mark A.R. Pequeras
"""
import json
import settings as temple
from flask import jsonify, url_for, session
from ast import literal_eval as lite

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
    
