from datetime import datetime


def loadblogs(count: int, category=None) -> tuple:
    pass


def loadproducts(count: int, category=None) -> tuple:
    pass


def dateformatter(epoch):
    return datetime.fromtimestamp(int(epoch))