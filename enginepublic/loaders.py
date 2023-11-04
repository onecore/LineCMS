from datetime import datetime


def loadblogs(count: int, category=None) -> tuple:
    pass


def loadproducts(count: int, category=None) -> tuple:
    pass


def dateformatter(epoch,split=False):
    d =  datetime.fromtimestamp(int(epoch))
    sd =  d.strftime("%b %d,%Y  %I:%M %p")
    if split:
        return str(sd).split("  ")
    return sd