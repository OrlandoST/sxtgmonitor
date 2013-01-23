# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

#########################################################################
## This is a samples controller
## - index is the default action of any application
## - user is required for authentication and authorization
## - download is for downloading files uploaded in the db (does streaming)
## - call exposes all registered services (none by default)
#########################################################################

def index():
#    sqlgrid = SQLFORM.grid(db.tg_load, fields = [
#        db.tg_load.check_date,
#        db.tg_load.tg_number,
#        db.tg_load.busy,
#        db.tg_load.installed], 
#        orderby = ~db.tg_load.check_date,
#        editable=False,
#        details=False,
#        deletable=False,
#        create=False,
#        )
    sqlgrid = SQLFORM.grid(db.tg_load,left=db.tg_list.on(db.tg_load.tg_number == db.tg_list.tg_number) , fields = [
        db.tg_load.check_date,
        db.tg_load.tg_number,
        db.tg_list.tg_descr,
        db.tg_load.busy,
        db.tg_load.installed],
        orderby = ~db.tg_load.check_date,
        editable = False,
        details = False,
        deletable = False,
        create = False)    
    response.flash = ("Welcome to tg monitor!")
    return dict(sqlgrid = sqlgrid)

def monitor():
    html=''
    tg_list = SQLFORM.grid(db.tg_list)
    #
    curd = Crud(db)
    last = db.tg_load.check_date.max()
    last_date = db().select(last).first()[last]
    #html += str(last_date.day)
    query = ((db.tg_load.tg_number == '44') & (db.tg_load.check_date == last_date))
    load = curd.select(db.tg_load, query)
    return dict(message=html, tg_list='', load='')

def monitor4():
    html=''
    tg_list = SQLFORM.grid(db.tg_list)
    curd = Crud(db)
    last = db.tg_load.check_date.max()
    last_date = db().select(last).first()[last]
    query = ((db.tg_load.tg_number == '44') & (db.tg_load.check_date == last_date))
    load = curd.select(db.tg_load, query)
    return dict(tg_list='', load='') 
    
def get_diagram4():
    html = ''
    crud = Crud(db)
    #last = db.tg_load.check_date.max()
    #last_date = db().select(last).first()[last]
    
    #query = (db.tg_list.tg_group == 'group1')
    #tg_list = crud.select(db.tg_list, query)
    #html += str(tg_list)
    rows =db(db.tg_list.tg_group == 'group1').select()
    for row in rows:
        #html +=row.tg_number+'<br>'
        html += '<font color="'+row.color+'"><b>' + row.tg_descr + '</b></font>'
        html += ' ' +row.tg_number + '<br>'
    html += '<br>'
    #
    html += '<img src = "../static/group1_4.png">'
    #html += '<img src =' + "{{=URL('static','group1_4.png')}}" + '>'
    html += '<br><br>'
    rows =db(db.tg_list.tg_group == 'group2').select()
    for row in rows:
        #html +=row.tg_number+'<br>'
        html += '<font color="'+row.color+'"><b>' + row.tg_descr + '</b></font>'
        html += ' ' +row.tg_number + '<br>'
    html += '<br>'
    html += '<br>'
    html += '<img src = "../static/group2_4.png">'
    html += '<br><br>'
    rows =db(db.tg_list.tg_group == 'group3').select()
    for row in rows:
        #html +=row.tg_number+'<br>'
        html += '<font color="'+row.color+'"><b>' + row.tg_descr + '</b></font>'
        html += ' ' +row.tg_number + '<br>'
    html += '<br>'
    html += '<br>'
    html += '<img src = "../static/group3_4.png">'
    html += '<br><br>'
    rows =db(db.tg_list.tg_group == 'group4').select()
    for row in rows:
        #html +=row.tg_number+'<br>'
        html += '<font color="'+row.color+'"><b>' + row.tg_descr + '</b></font>'
        html += ' ' +row.tg_number + '<br>'
    html += '<br>'
    html += '<br>'
    html += '<img src = "../static/group4_4.png">'
    html += '<br><br>'
    rows =db(db.tg_list.tg_group == 'group5').select()
    for row in rows:
        #html +=row.tg_number+'<br>'
        html += '<font color="'+row.color+'"><b>' + row.tg_descr + '</b></font>'
        html += ' ' +row.tg_number + '<br>'
    html += '<br>'
    html += '<br>'
    html += '<img src = "../static/group5_4.png">'
    html += '<br><br>'
    rows =db(db.tg_list.tg_group == 'group6').select()
    for row in rows:
        #html +=row.tg_number+'<br>'
        html += '<font color="'+row.color+'"><b>' + row.tg_descr + '</b></font>'
        html += ' ' +row.tg_number + '<br>'
    html += '<br>'
    html += '<br>'
    html += '<img src = "../static/group6_4.png">'
    return html
        
def get_diagram():
    import datetime
    cur_time = datetime.datetime.now()
    if len(str(cur_time.minute)) == 1:
        c_t = str(cur_time.hour) + ':0' + str(cur_time.minute)
    else:
        c_t = str(cur_time.hour) + ':' + str(cur_time.minute)
    
    
    html = ''
    crud = Crud(db)
    last = db.tg_load.check_date.max()
    lst_d = db().select(last).first()[last]
    
    #query = (db.tg_list.tg_group == 'group1')
    #tg_list = crud.select(db.tg_list, query)
    #html += str(tg_list)
    html += '<center><b>'
    
    if len(str(lst_d.minute)) == 1:
        html += 'Last update: '+str(lst_d.year)+'-'+str(lst_d.month) + '-'+str(lst_d.day) +'    '+str(lst_d.hour)+':0'+str(lst_d.minute)
    else:
        html += 'Last update: '+str(lst_d.year)+' '+str(lst_d.month) + ' '+str(lst_d.day) +'    '+str(lst_d.hour)+':'+str(lst_d.minute)
    
    html += '    Current time: ' + c_t
    html += '</b>'
    rows = db(db.group_descr2.tg_group == 'group1').select()
    for row in rows:
        html += '<h4>' + row.group_description + ': </h4>'
    rows =db(db.tg_list.tg_group == 'group1').select()
    for row in rows:
        #html +=row.tg_number+'<br>'
        html += '<font color="'+row.color+'"><b>' + row.tg_descr + '</b></font>'
        html += ' ' +row.tg_number + '  ,'  
    html += '<br>'
    #
    html += '<img src = "../static/group1.png">'
    html += '<br><br>'
    
    rows = db(db.group_descr2.tg_group == 'group2').select()
    for row in rows:
        html += '<h4>' + row.group_description + ': </h4>'
    rows =db(db.tg_list.tg_group == 'group2').select()
    for row in rows:
        #html +=row.tg_number+'<br>'
        html += '<font color="'+row.color+'"><b>' + row.tg_descr + '</b></font>'
        html += ' ' +row.tg_number + '  ,'
    html += '<br>'
    html += '<img src = "../static/group2.png">'
    html += '<br><br>'
    #
    rows = db(db.group_descr2.tg_group == 'group3').select()
    for row in rows:
        html += '<h4>' + row.group_description + ': </h4>'
    rows =db(db.tg_list.tg_group == 'group3').select()
    for row in rows:
        #html +=row.tg_number+'<br>'
        html += '<font color="'+row.color+'"><b>' + row.tg_descr + '</b></font>'
        html += ' ' +row.tg_number + '  ,'
    html += '<br>'
    html += '<img src = "../static/group3.png">'
    html += '<br><br>'
    #
    rows = db(db.group_descr2.tg_group == 'group4').select()
    for row in rows:
        html += '<h4>' + row.group_description + ': </h4>'
    rows =db(db.tg_list.tg_group == 'group4').select()
    for row in rows:
        #html +=row.tg_number+'<br>'
        html += '<font color="'+row.color+'"><b>' + row.tg_descr + '</b></font>'
        html += ' ' +row.tg_number + '  ,'
    html += '<br>'
    html += '<img src = "../static/group4.png">'
    html += '<br><br>'
    #    
    rows = db(db.group_descr2.tg_group == 'group5').select()
    for row in rows:
        html += '<h4>' + row.group_description + ': </h4>'
    rows =db(db.tg_list.tg_group == 'group5').select()
    for row in rows:
        #html +=row.tg_number+'<br>'
        html += '<font color="'+row.color+'"><b>' + row.tg_descr + '</b></font>'
        html += ' ' +row.tg_number + '  ,'
    html += '<br>'
    html += '<img src = "../static/group5.png">'
    html += '<br><br>'
    #    
    rows = db(db.group_descr2.tg_group == 'group6').select()
    for row in rows:
        html += '<h4>' + row.group_description + ': </h4>'
    rows =db(db.tg_list.tg_group == 'group6').select()
    for row in rows:
        #html +=row.tg_number+'<br>'
        html += '<font color="'+row.color+'"><b>' + row.tg_descr + '</b></font>'
        html += ' ' +row.tg_number + '  ,'
    html += '<br>'
    html += '<img src = "../static/group6.png">'
    html += '<br><br>'
    return html

@auth.requires_login()
def config():
    sqlgrid=SQLFORM.grid(db.tg_list)
    return dict(sqlgrid=sqlgrid)

@auth.requires_login()
def description():
    sqlgrid = SQLFORM.grid(db.group_descr2, fields=[
        db.group_descr2.tg_group,
        db.group_descr2.group_description],
        create=False,
        searchable=False,
        deletable=False)
    return dict(sqlgrid = sqlgrid)

def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    """
    return dict(form=auth())


def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request,db)


def call():
    """
    exposes services. for example:
    http://..../[app]/default/call/jsonrpc
    decorate with @services.jsonrpc the functions to expose
    supports xml, json, xmlrpc, jsonrpc, amfrpc, rss, csv
    """
    return service()


@auth.requires_signature()
def data():
    """
    http://..../[app]/default/data/tables
    http://..../[app]/default/data/create/[table]
    http://..../[app]/default/data/read/[table]/[id]
    http://..../[app]/default/data/update/[table]/[id]
    http://..../[app]/default/data/delete/[table]/[id]
    http://..../[app]/default/data/select/[table]
    http://..../[app]/default/data/search/[table]
    but URLs must be signed, i.e. linked with
      A('table',_href=URL('data/tables',user_signature=True))
    or with the signed load operator
      LOAD('default','data.load',args='tables',ajax=True,user_signature=True)
    """
    return dict(form=crud())
