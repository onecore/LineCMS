"""
LineCMS - Content Management System (Product & Blogging) for Rapid website development
Website: www.linecms.com
Author: S. Jangra & Mark A.R. Pequeras
"""
import os
from engine.editor import get_templates
from settings import cms_version
from flask import jsonify
# from settings import uploads_temporary_autodelete
import zipfile, shutil
from pathlib import Path
templates_list = [theme for theme in get_templates()]


def procfiles(temp,folder):
    # verify version or legit theme (base on theme.py)
    temp_f = os.listdir(temp)
    theme = False
    theme_p = False
    for conts in temp_f:
        try:
            if os.path.isdir(os.path.join(temp,conts)):
                sub = os.path.join(temp,conts)
                if "html" in os.listdir(sub) and "resources" in os.listdir(sub):
                    theme = conts
                    theme_p = sub
        except: pass

    if theme:
        try:
            temp = shutil.move(f"{theme_p}/html", f'templates/SYSTEM/{theme}') # future usage var
            stat = shutil.move(f"{theme_p}/resources", f'static/SYSTEM/{theme}') # future usage var
            l = [th for th in get_templates()]
            return jsonify({'status':1,'theme':theme,'list':l})
        except:
            return 0

    return 0


    

def unpack_theme(temp,filename) -> bool:
    try:
        fp = os.path.join(temp,filename)
        with zipfile.ZipFile(fp, 'r') as zip_ref:
            zip_ref.extractall(temp)

        return procfiles(temp,filename)

    except Exception as e:
        print(e)
        return 0
    










