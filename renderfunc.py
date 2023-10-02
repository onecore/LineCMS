"""
Inline functions for Jinja
"""
import templater as temple


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
    from lxml import html
    return html.fromstring(v).text_content()


def ks_tolist(v) -> list:
    return eval(v)
