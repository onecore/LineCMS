"""
SandCMS - Content Management System (Product & Blogging) for Rapid website development
Website: www.sandcms.com
Initial: 04/1/23
Author: S. Jangra & Mark A.R. Pequeras
"""
import os

templates_list = []

themes = os.listdir("templates/SYSTEM")


for theme in themes:
    if "." not in theme:
        templates_list.append(theme)


def loadtemplatedb():
    pass


def template():
    pass
