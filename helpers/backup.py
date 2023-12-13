
import time, shutil

def backup_db():
    print("backup")
    try:
        shutil.copyfile("dbase/sand", f"engine/backups/db/db-{time.time()}")
    except:
        return {"status":0}

def backup_res():
    pass