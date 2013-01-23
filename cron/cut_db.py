#!/usr/bin/env python
# -*- coding: utf-8 -*-


import sys, os, telnetlib, time, datetime
import PIL, Image, ImageDraw, ImageFont

sys.path.append('/home/www-data/web2py')
from gluon import DAL, Field
db=DAL('sqlite://storage.sqlite', folder='/home/www-data/web2py/applications/tgmonitor/databases')

db.define_table('tg_load',
    Field('check_date','datetime'),
    Field('tg_number',length=17),
    Field('busy', 'integer'),
    Field('installed', 'integer')
    )


t3 = datetime.datetime.now() - datetime.timedelta(3)
db(db.tg_load.check_date < t3).delete()
db.commit()

if os.path.isfile('/home/www-data/web2py/applications/tgmonitor/static/group1.png')==True:
    os.remove('/home/www-data/web2py/applications/tgmonitor/static/group1.png')
if os.path.isfile('/home/www-data/web2py/applications/tgmonitor/static/group2.png')==True:
    os.remove('/home/www-data/web2py/applications/tgmonitor/static/group2.png')
if os.path.isfile('/home/www-data/web2py/applications/tgmonitor/static/group3.png')==True:
    os.remove('/home/www-data/web2py/applications/tgmonitor/static/group3.png')
if os.path.isfile('/home/www-data/web2py/applications/tgmonitor/static/group4.png')==True:
    os.remove('/home/www-data/web2py/applications/tgmonitor/static/group4.png')
if os.path.isfile('/home/www-data/web2py/applications/tgmonitor/static/group5.png')==True:
    os.remove('/home/www-data/web2py/applications/tgmonitor/static/group5.png')
if os.path.isfile('/home/www-data/web2py/applications/tgmonitor/static/group6.png')==True:
    os.remove('/home/www-data/web2py/applications/tgmonitor/static/group6.png')


