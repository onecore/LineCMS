from ast import literal_eval as lite

def trythis(obj,failed):
    try:
        return lite(obj)
    except:
        return failed
    