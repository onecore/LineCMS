"""
LineCMS - Content Management System (Product & Blogging) for Rapid website development
Website: www.linecms.com
Author: S. Jangra & Mark A.R. Pequeras
"""
import os
import zipfile, shutil
from flask import jsonify
from engine.editor import get_templates


templates_list = [theme for theme in get_templates()]


def procfiles(temp: str,folder: str) -> bool or dict:
    """verify unpacked theme files based on theme.py and some other res.

    Args:
        temp (str): temp folder
        folder (str): theme folder

    Returns:
        bool or dict: dict if success
    """
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


    

def unpack_theme(temp: str,filename: str) -> bool:
    """unpack compressed uploaded file

    Args:
        temp (str): temporary folder
        filename (str): filename

    Returns:
        bool: if error
        dict: if success (jsonified)
        
    """
    try:
        fp = os.path.join(temp,filename)
        with zipfile.ZipFile(fp, 'r') as zip_ref:
            zip_ref.extractall(temp)
        return procfiles(temp,filename)
    except Exception as e:
        return 0
    










