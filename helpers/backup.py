"""
LineCMS - Content Management System (Product & Blogging) for Rapid website development
Website: www.linecms.com
Author: S. Jangra & Mark A.R. Pequeras
"""

import shutil, settings,os
from datetime import datetime

def show_backs_list() -> dict:
    """shows backups for database and resources

    Returns:
        dict: _description_
    """
    try:
        db_backs = [file for file in os.listdir("engine/backups/db/") if "." != file[0]]
        rs_backs = [file for file in os.listdir("engine/backups/resources/") if "." != file[0] and file.endswith(".zip")]
        return {"status":1,"db":db_backs,"rs":rs_backs}
    except Exception as e:
        return {"status":0,"db":[],"rs":[]}

def del_backs(f_type: str,file: str) -> dict:
    """Deletes backup file

    Args:
        f_type (str): backup type (db or rs)
        file (str): file to delete

    Returns:
        dict: response
    """
    if "r" in f_type: # resource
        try:
            os.remove("engine/backups/resources/"+file)    # remove folder
            return {"status":1}
        except Exception as e:
            return {"status":0}

    elif "d" in f_type: # database
        try:
            os.remove("engine/backups/db/"+file)    # remove folder
            return {"status":1}
        except Exception as e:
            return {"status":0}
    else:
        return {"status":0}

def backup_db() -> dict:
    """Compresses database file
    Returns:
        dict: response
    """
    try:
        now = datetime.now()
        dt_string = now.strftime("%d-%m-%Y-%H%M%S")
        shutil.copyfile("dbase/sand", f"engine/backups/db/{dt_string}")
        return {"status":1, "fname":dt_string,"type":"db"}
    except:
        return {"status":0}

def backup_res() -> dict:
    """Compresses resources file

    Returns:
        dict: response
    """
    now = datetime.now()
    dt_string = now.strftime("%d-%m-%Y-%H%M%S")
    try:
        for folder,path in settings.backup_res_folders.items():
            fname = f"{folder}-{datetime.now()}"
            shutil.copytree(path,f"engine/backups/resources/{dt_string}/{fname}")
        out_f = f"engine/backups/resources/{dt_string}"
        shutil.make_archive(f"{out_f}","zip",out_f) # create zip
        shutil.rmtree(out_f)    # remove folder
        return {"status":1, "fname":dt_string+".zip", "type":"zip"}
    except:
        return {"status":0}
