#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys, os, telnetlib, time, datetime


def get_circuits(s='',find_par=''):
    pos = s.find(find_par)+35
    return s[pos:pos+6].strip()



sys.path.append('/home/www-data/web2py')
from gluon import DAL, Field
db=DAL('sqlite://storage.sqlite', folder='/home/www-data/web2py/applications/tgmonitor/databases')
db.define_table('tg_load',
    Field('check_date','datetime'),
    Field('tg_number',length=17),
    Field('busy', 'integer'),
    Field('installed', 'integer')
    )


host = '10.200.66.70'
port = '6000'
tn = telnetlib.Telnet(host,port)
tn.write('LGI:op="monitor",PWD ="dspoftk",SER="10.100.100.104---O&M System";')
ans = tn.read_until('END')


tn.write('DSP OFTK: LT=TG, TG=44, DT=AT;')
ans = tn.read_until('END')


_busy = get_circuits(ans, 'Busy')
_ins_num = get_circuits(ans, 'Installation number')


last = db.tg_load.check_date.max()
last_date = db().select(last).first()[last]

my_result= db((db.tg_load.check_date==last_date) & (db.tg_load.tg_number=='44')).select()
for row in my_result:
    last_busy=row.busy







db.tg_load.insert(check_date=datetime.datetime.now(), tg_number=44, busy=_busy, installed=_ins_num)
#db.tg_load.insert(check_date='',tg_number=3, busy=45, installed=60)
db.commit()

#draw diagramm

import PIL, Image, ImageDraw, ImageFont

width = 800
height = 420

if os.path.isfile('/home/www-data/web2py/applications/tgmonitor/cron/44.png')==False:
    im = Image.new('RGB', (width,height), (255,255,255))
    im.save('/home/www-data/web2py/applications/tgmonitor/cron/44.png')

im = Image.open('/home/www-data/web2py/applications/tgmonitor/cron/44.png')
draw = ImageDraw.Draw(im)

h=height-20
for i in range(11):
    draw.line((20,h/10*i, width-20, h/10*i), fill='black')
    draw.text((4,h/10*i), str(abs(i-10))+'0%', fill='black')

for i in range(24):
    draw.text((30+i*60/2,h+5), str(i), fill='black')    

t = datetime.datetime.now()
_busy=float(_busy)
_ins_num = float(_ins_num)


line2_x = 30+(t.hour*60+t.minute)/2
line2_y = h-int(h*_busy/_ins_num)

last_busy=float(last_busy)
line1_x = line2_x-2
line1_y = h-int(h*last_busy/_ins_num)

draw.line((line1_x,line1_y, line2_x, line2_y), fill='red')

draw.point((30+(t.hour*60+t.minute)/2,  h-int(h*_busy/_ins_num)), fill='red')

#center_x=30+(t.hour*60+t.minute)/2
#center_y=h-int(h*_busy/_ins_num)
#draw.ellipse((center_x-2,center_y-2, center_x+2, center_y+2), fill='blue')

im.save('/home/www-data/web2py/applications/tgmonitor/cron/44.png')




#close all
tn.close()
