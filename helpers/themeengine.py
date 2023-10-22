import os
import dataengine
import version

templates_list = []

themes = os.listdir("templates/SYSTEM")


for theme in themes:
    if "." not in theme:
        templates_list.append(theme)


def loadtemplatedb():
    pass


def template():
    pass
