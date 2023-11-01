import dataengine
ps = dataengine.knightclient()

def parsetemplate(**kwargs):
    pass
    
    
def sendtemplate(**kwargs):
    print("Sending now...")
    if "obj" and "template" in kwargs:
        print(kwargs)
    