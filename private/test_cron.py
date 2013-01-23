#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys, time
sys.path.append('/home/www-data/web2py')
from gluon import DAL, Field

def append():
    db=DAL('sqlite://storage.sqlite', folder='/home/www-data/web2py/applications/tgmonitor/databases')
    db.define_table('tg_load',
        Field('check_date','datetime'),
        Field('tg_number','integer', notnull=True),
        Field('busy', 'integer'),
        Field('installed', 'integer')
        )

    db.tg_load.insert(check_date='',tg_number=2, busy=45, installed=60)
    db.commit()

while 1:
    time.sleep(60)
    append()

