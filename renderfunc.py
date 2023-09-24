import templater as temple


def ks_include_adminbutton():
    c = temple.ks_admin_button
    v = "&nbsp&nbsp<a href='"+temple.route_dashboard+"' class='btn " + \
        c+"'"+"style='color:white'"+">Owner Dashboard</a>"
    print(v, "<<<")
    return v


def ks_badge_insert(v):
    q = ""
    if v:
        i = str(v).split(",")
        for cat in i:
            q += "<badge class='badge {c}'>".format(
                c=temple.ks_badge_insert)+cat+"</badge>&nbsp"
    return q
