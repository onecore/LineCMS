"""
SandCMS - Content Management System (Product & Blogging) for Rapid website development
Website: www.sandcms.com
Author: S. Jangra & Mark A.R. Pequeras
"""

import shutil, settings
from datetime import datetime

def showlist() -> dict:
    pass

def del_back(type,file) -> dict:
    pass

def backup_db() -> dict:
    try:
        now = datetime.now()
        dt_string = now.strftime("%d-%m-%Y-%H%M%S")
        shutil.copyfile("dbase/sand", f"engine/backups/db/{dt_string}")
        return {"status":1, "fname":dt_string,"type":"db"}
    except:
        return {"status":0}

def backup_res() -> dict:
    now = datetime.now()
    dt_string = now.strftime("%d-%m-%Y-%H%M%S")
    try:
        for folder,path in settings.backup_res_folders.items():
            fname = f"{folder}-{datetime.now()}"
            shutil.copytree(path,f"engine/backups/resources/{dt_string}/{fname}")
        out_f = f"engine/backups/resources/{dt_string}"
        shutil.make_archive(f"{out_f}","zip",out_f)
        shutil.rmtree(out_f)
        return {"status":1, "fname":dt_string+".zip", "type":"zip"}
    except:
        return {"status":0}
