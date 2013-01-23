# -*- coding: utf-8 -*-

#########################################################################
## This scaffolding model makes your app work on Google App Engine too
## File is released under public domain and you can use without limitations
#########################################################################

## if SSL/HTTPS is properly configured and you want all HTTP requests to
## be redirected to HTTPS, uncomment the line below:
# request.requires_https()

db = DAL('sqlite://storage.sqlite')

db.define_table('tg_load',
    Field('check_date','datetime'),
    Field('tg_number',length=17),
    Field('busy', 'integer'),
    Field('installed', 'integer')
    )

db.define_table('group_descr2',
    Field('tg_group', length=17, unique= True, default = 'group1', requires = IS_IN_SET(['group1','group2','group3','group4','group5','group6'])),
    Field('group_description', length=200),
    )

db.define_table('tg_list',
    #Field('tg_group', 'reference group_descr', requires = IS_IN_DB(db,'group_descr.group_description',db.group_descr._format,multiple=False)),
    Field('tg_group', length=12, default='group1', requires = IS_IN_SET(['group1','group2','group3','group4', 'group5', 'group6'])),
    Field('tg_number', length=17, notnull=True),
    Field('tg_descr', length=17),
    Field('tg_type', length=3, default='sip', requires=IS_IN_SET(['sip','ss7'])),
    Field('color', length=16, default='black', requires = IS_IN_SET(['black', 'blue', 'green', 'red', 'indigo', 'brown'])),
    Field('alarm', 'integer'),
    Field('alarm_email', length=20),
    )

## by default give a view/generic.extension to all actions from localhost
## none otherwise. a pattern can be 'controller/function.extension'
response.generic_patterns = ['*'] if request.is_local else []
## (optional) optimize handling of static files
# response.optimize_css = 'concat,minify,inline'
# response.optimize_js = 'concat,minify,inline'

#########################################################################
## Here is sample code if you need for
## - email capabilities
## - authentication (registration, login, logout, ... )
## - authorization (role based authorization)
## - services (xml, csv, json, xmlrpc, jsonrpc, amf, rss)
## - old style crud actions
## (more options discussed in gluon/tools.py)
#########################################################################

from gluon.tools import Auth, Crud, Service, PluginManager, prettydate
auth = Auth(db)
crud, service, plugins = Crud(db), Service(), PluginManager()

## create all tables needed by auth if not custom tables
auth.define_tables(username=True, signature=False)

## configure email
mail=auth.settings.mailer
mail.settings.server = 'mail.mastertel.ru:25'
mail.settings.sender = 'e.omin@mastertel.ru'
mail.settings.login = 'e.omin@mastertel.ru:6yhn9ijn'

## configure auth policy
auth.settings.registration_requires_verification = False
auth.settings.registration_requires_approval = True
auth.settings.reset_password_requires_verification = False
#my policy
auth.settings.actions_disabled.append('register')
auth.settings.actions_disabled.append('request_reset_password')
auth.settings.actions_disabled.append('retrieve_username')
#auth.settings.actions_disabled(['register', 'change_password','request_reset_password'])

## if you need to use OpenID, Facebook, MySpace, Twitter, Linkedin, etc.
## register with janrain.com, write your domain:api_key in private/janrain.key

#from gluon.contrib.login_methods.rpx_account import use_janrain
#use_janrain(auth,filename='private/janrain.key')

#########################################################################
## Define your tables below (or better in another model file) for example
##
## >>> db.define_table('mytable',Field('myfield','string'))
##
## Fields can be 'string','text','password','integer','double','boolean'
##       'date','time','datetime','blob','upload', 'reference TABLENAME'
## There is an implicit 'id integer autoincrement' field
## Consult manual for more options, validators, etc.
##
## More API examples for controllers:
##
## >>> db.mytable.insert(myfield='value')
## >>> rows=db(db.mytable.myfield=='value').select(db.mytable.ALL)
## >>> for row in rows: print row.id, row.myfield
#########################################################################

## after defining tables, uncomment below to enable auditing
# auth.enable_record_versioning(db)
