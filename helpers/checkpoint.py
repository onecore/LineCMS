"""
LineCMS - Content Management System (Product & Blogging) for Rapid website development
Website: www.linecms.com
Author: S. Jangra & Mark A.R. Pequeras
"""

from functools import wraps
from flask import g, request, redirect, url_for,session
import dataengine, settings

installed = False
_de = dataengine.SandEngine()

if settings.installed_check:
    cred = _de.get_cred()
    if cred:
        installed = True
    else:
        installed = False

def onlylogged(f):
    @wraps(f)
    def checkpoint(*args, **kwargs):
        """Uses for all Dashboard routes, Checks for session and install status"""
        if not installed:
            return redirect("/install")

        if "authenticated" not in session:
            return redirect("login")
        else:
            _cred = _de.get_cred()
            _cred_data = _cred[0]
            if _cred_data[0] == session['authenticated'][0] and _cred_data[1] == session['authenticated'][1]:
                return f(*args, **kwargs)
            return redirect("login")

    return checkpoint