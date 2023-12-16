
import time, shutil, settings, os
from datetime import datetime

def backup_db():
    try:
        fname = f"db-{datetime.now()}"
        shutil.copyfile("dbase/sand", f"engine/backups/db/{fname}")
        return {"status":1, "fname":fname}

    except:
        return {"status":0}

def backup_res():
    m_fname = f"res-{datetime.now()}"
    try:
        for folder,path in settings.backup_res_folders.items():
            fname = f"{folder}-{datetime.now()}"
            shutil.copytree(path,f"engine/backups/resources/{m_fname}/{fname}")

        out_f = f"engine/backups/resources/{m_fname}"
        shutil.make_archive(f"{out_f}","zip",out_f)
        shutil.rmtree(out_f)
        return {"status":1, "fname":m_fname+".zip"}
    except:
        return {"status":0}
