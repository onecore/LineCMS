
import time, shutil, settings

def backup_db():
    try:
        fname = f"db-{time.time()}"
        shutil.copyfile("dbase/sand", f"engine/backups/db/{fname}")
        return {"status":1, "fname":fname}
    except:
        return {"status":0}

def backup_res():
    m_fname = f"res-{time.time()}"
    try:
        for folder,path in settings.backup_res_folders.items():
            fname = f"{folder}-{time.time()}"
            shutil.copytree(path,f"engine/backups/resources/{m_fname}/{fname}")
            
        return {"status":1, "fname":m_fname}
    except:
        return {"status":0}
