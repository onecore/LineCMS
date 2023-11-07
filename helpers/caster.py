from ast import literal_eval as lite

def trythis(obj,failed):
    if obj is None:
        print("None >>>>")
        return failed
    
    try:
        return lite(obj)
    except:
        return failed
    