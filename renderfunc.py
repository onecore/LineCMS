"""
Inline functions for Jinja
"""
import templater as temple
import json
from flask import jsonify


def ks_include_adminbutton() -> str:
    "Includes Admin button if session exists"
    c = temple.ks_admin_button
    v = "&nbsp&nbsp<a href='"+temple.route_dashboard+"' class='btn " + \
        c+"'"+"style='color:white'"+">Owner Dashboard</a>"
    return v


def ks_badge_insert(v) -> str:
    "bootstrap badge inserter (single/multi)"
    q = ""
    if v:
        i = str(v).split(",")
        for cat in i:
            q += "<badge class='badge {c}'>".format(
                c=temple.ks_badge_insert)+cat+"</badge>&nbsp"
    return q


def ks_html2text(v) -> str:
    """parses html to text"""
    from lxml import html
    if v:
        return html.fromstring(v).text_content()
    else:
        return ""


def ks_html2text_truncate(v) -> str:
    "parses html to text with truncation"
    from lxml import html
    if v:
        ret = html.fromstring(v).text_content()
        trunc = ret[:210] + (ret[210:] and '..')
        return trunc
    else:
        return ""


def ks_tolist(v) -> list:
    "evaluate parsed string to python list type"
    return eval(v)

def ks_todict(v) -> dict:
    "evaluate parsed string to python dict type"
    return eval(v)


def ks_getdictkeys(v) -> list:
    "returns list of keys from string dict"
    o = []
    p = jsonify(v)

    for k, v in p.items():
        o.append(k)
    return eval(o)


def ks_variantcount(v) -> int:
    "return variant's length"
    if len(v) > 2:
        p = eval(v)
        return len(p.keys())
    return 0


def ks_tojson(v) -> dict:
    "python dict obj to json"
    return json.dumps(v)

