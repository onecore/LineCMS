"""
LineCMS - Content Management System (Product & Blogging) for Rapid website development
Website: www.linecms.com
Author: S. Jangra & Mark A.R. Pequeras
"""
from datetime import datetime


def loadblogs(count: int, category=None) -> tuple:
    pass

def loadproducts(count: int, category=None) -> tuple:
    pass

def dateformatter(epoch,split=False) -> str:
    'parse epoch time to readable date'
    d =  datetime.fromtimestamp(int(epoch))
    sd =  d.strftime("%b %d,%Y  %I:%M %p")
    if split:
        return str(sd).split("  ")
    return sd