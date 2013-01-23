#!/usr/bin/env python
# -*- coding: utf-8 -*-


import sys, os, telnetlib, time, datetime
import PIL, Image, ImageDraw, ImageFont
width = 800
height = 420

def get_circuits(s='',find_par=''):
    pos = s.find(find_par)+len(find_par)
    return s[pos:pos+6].strip()

def send_mail(number,descr,alarm, send_email, busy=0, installed=0):
    import smtplib
    from email.MIMEText import MIMEText
    text = 'Здравствуйте \r\n'
    text += '\r\n Alarm for tg ' + str(number) + ' ' + descr
    text += '\r\n Alarm % ' + str(alarm)
    text += '\r\n details http://tgmonitor/tgmonitor/default/monitor'    
    text += '\r\n Busy/Installed  ' + str(busy) + '/' + str(installed)
    msg = MIMEText(text, "", "utf-8")
    msg['Subject'] = 'Alarm for tg ' + str(number) + ' ' + descr
    msg['From']='omeen@bk.ru'
    msg['To'] = send_email
    me='Emilius<omeen@bk.ru>'
    to='omeen@bk.ru'
    mailSrv=smtplib.SMTP("mail.ru",25)
    mailSrv.ehlo()
    mailSrv.login('omeen@bk.ru','passsswordd')      
    mailSrv.sendmail(me, to, msg.as_string())      
    mailSrv.close()


sys.path.append('/home/www-data/web2py')
from gluon import DAL, Field
db=DAL('sqlite://storage.sqlite', folder='/home/www-data/web2py/applications/tgmonitor/databases')
db.define_table('tg_load',
    Field('check_date','datetime'),
    Field('tg_number',length=17),
    Field('busy', 'integer'),
    Field('installed', 'integer')
    )


db.define_table('tg_list',
    Field('tg_group', length=12, default='group1'),
    Field('tg_number', length=17, notnull=True),
    Field('tg_descr', length=17),
    Field('tg_type', length=3, default='sip'),
    Field('color', length=16, default='black'),
    Field('alarm', 'integer', default=90),
    Field('alarm_email', length=20),
    Field('alarm_call_number', length=32),
    )

h=height-20    

for g in range(1,7):
    if os.path.isfile('/home/www-data/web2py/applications/tgmonitor/static/group'+str(g)+'.png')==False:
        im = Image.new('RGB', (width,height), (255,255,255))
        draw = ImageDraw.Draw(im)
        for i in range(11):
            draw.line((20,h/10*i, width-20, h/10*i), fill='black')
            draw.text((4,h/10*i), str(abs(i-10))+'0%', fill='black')
        for i in range(24):
            draw.text((30+i*60/2,h+5), str(i), fill='black')    
        im.save('/home/www-data/web2py/applications/tgmonitor/static/group'+str(g)+'.png')


#im = Image.open('/home/www-data/web2py/applications/tgmonitor/static/diagramm.png')
#draw = ImageDraw.Draw(im)

host = '10.200.66.70'
port = '6000'
tn = telnetlib.Telnet(host,port)
tn.write('LGI:op="monitor",PWD ="dspoftk",SER="10.200.11.20---O&M System";')
ans = tn.read_until('END')

last = db.tg_load.check_date.max()
last_date = db().select(last).first()[last]

t = datetime.datetime.now()

def get_last_busy(db,last_date,tg_number):
    my_result= db((db.tg_load.check_date==last_date) & (db.tg_load.tg_number==tg_number)).select()
    l_busy=0
    for row in my_result:
        l_busy = row.busy
    return l_busy

vert = 40
group = 'group1'

for row in db().select(db.tg_list.ALL):
    im = Image.open('/home/www-data/web2py/applications/tgmonitor/static/'+row.tg_group+'.png')
    draw = ImageDraw.Draw(im)
#    if group == row.tg_group:
#        vert += 20
#    else:
#        group = row.tg_group
#        vert = 40
#    draw.text((70,vert), row.tg_descr+' '+row.tg_number +'  '+ row.color, fill= 'black')
#    vert += 20
    if row.tg_type == 'sip':
        try:
            s = 'LST TG: TG=' + row.tg_number +', SC=NO, SOT=YES;'
            tn.write(s)
            ans = tn.read_until('END')
            _ins_num = get_circuits(ans, 'Stop Call Restriction  =')
            s = 'DSP TGCALL: TG=' + row.tg_number + ';'
            tn.write(s)
            ans = tn.read_until('END')
            _busy = get_circuits(ans, 'Calling number =')
            db.tg_load.insert(check_date=t, tg_number=row.tg_number, busy=_busy, installed=_ins_num)
            _busy=float(_busy)
            _ins_num = float(_ins_num)
            last_busy =int(get_last_busy(db, last_date, row.tg_number))
            last_busy=float(last_busy)
            line2_x = 30+(t.hour*60+t.minute)/2
            line2_y = h-int(h*_busy/_ins_num)
            line1_x = line2_x-3
            line1_y = h-int(h*last_busy/_ins_num)
            draw.line((line1_x,line1_y, line2_x, line2_y), fill=row.color)
        except:
            pass
    if row.tg_type == 'ss7':
        try:
            s ='DSP OFTK: LT=TG, TG=' + row.tg_number + ', DT=AT;'
            tn.write(s)
            ans = tn.read_until('END')
            _busy = get_circuits(ans, 'Busy                              ')
            _ins_num = get_circuits(ans, 'Installation number               ')
            db.tg_load.insert(check_date=t, tg_number=row.tg_number, busy=_busy, installed=_ins_num)
            _busy=float(_busy)
            _ins_num = float(_ins_num)
            last_busy =int(get_last_busy(db, last_date, row.tg_number))
            last_busy=float(last_busy)
            line2_x = 30+(t.hour*60+t.minute)/2
            line2_y = h-int(h*_busy/_ins_num)
            line1_x = line2_x-3
            line1_y = h-int(h*last_busy/_ins_num)
            draw.line((line1_x,line1_y, line2_x, line2_y), fill=row.color)
        except:
            pass
    if row.alarm:
        if _busy*100/_ins_num>row.alarm:
            #send_mail(number,descr,alarm, send_email)
            try:
                send_mail(row.tg_number,row.tg_descr,row.alarm, row.alarm_email, _busy, _ins_num)
            except:
                pass
    im.save('/home/www-data/web2py/applications/tgmonitor/static/'+row.tg_group+'.png')
    box = (line2_x-150, 0, line2_x, 420)
    newim4 = im.crop(box)
    newim4 = newim4.resize((400,320),Image.ANTIALIAS)
#    newim4 = newim4.resize((400,320),Image.BILINEAR)
    newdraw = ImageDraw.Draw(newim4)
    for p in range(11):
        newdraw.text((4,310/10*p), str(abs(p-10))+'0%', fill='black')
    
    newim4.save('/home/www-data/web2py/applications/tgmonitor/static/'+row.tg_group+'_4.png')


#db.tg_load.insert(check_date='',tg_number=3, busy=45, installed=60)
db.commit()
tn.close()
#im.save('/home/www-data/web2py/applications/tgmonitor/static/diagramm.png')





