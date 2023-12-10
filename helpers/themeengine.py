"""
SandCMS - Content Management System (Product & Blogging) for Rapid website development
Website: www.sandcms.com
Author: S. Jangra & Mark A.R. Pequeras
"""
import os
from engine.editor import get_templates
from settings import cms_version
# from settings import uploads_temporary_autodelete
import zipfile, shutil
from pathlib import Path
templates_list = [theme for theme in get_templates()]


def procfiles(temp,folder):
    folders = {'resources':False,'html':False}
    extracted = os.path.join(temp,folder)
    fname_we = Path(temp)
    woe = fname_we.with_suffix('')

    for folder,bools in folders.items():
        print(temp+"/"+folder)
        if os.path.isdir(temp+"/"+woe+"/"+folder):
            print(temp+"/"+folder)
            folders[folder] = True
            print(folders)
    print(folders)



    shutil.rmtree(os.path.join(temp,folder)) # delete

    return False


    

def unpack_theme(temp,filename) -> bool:
    try:
        fp = os.path.join(temp,filename)
        with zipfile.ZipFile(fp, 'r') as zip_ref:
            zip_ref.extractall(temp)
        procfiles(temp,filename)
    except:
        return False
    










