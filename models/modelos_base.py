# Usemos la siguiente convencion:
#
# Los nombres de cada tabla seran en minusculas, separados con _ y en plural.
#
# Los nombres de los atributos seran en minusculas y singular, a menos de que se trate de una lista, en ese caso
# se intentara tomar un nombre distinto al de una tabla
#
# Si un atributo tiene como referencia a un record de otra tabla, se le agregara el sufijo _<tabla> si es dificil
# identificar que se trata de una referencia, si no es asi, se adoptara la convencion normal de atributos

######################################################################################################################
#
# Tablas principales de los modulos
# Se definira antes que las tablas de autenticacion porque son necesarias para estas
#
######################################################################################################################

response.files.append("http://ajax.googleapis.com/ajax/libs/jqueryui/1.7.2/jquery-ui.js")

# Tabla de Sedes, necesaria para las Dependencias

db.define_table(
    'sedes',
    Field('nombre', 'string', unique=True, notnull=True, label=T('Nombre de la Sede'))
)

# Tabla de Dependencias, Incluira la Direccion, los laboratorios y sus secciones y las coordinaciones

db.define_table(
    #Nombre de la entidad
    'dependencias',
    #Atributos;
    Field('nombre', 'string', notnull=True, label=T('Nombre')),

    Field('email', 'string', requires=IS_EMAIL(error_message='Debe tener un formato válido. EJ: example@org.com'), label=T('Correo')),

    # Auto-Referencia
    Field('unidad_de_adscripcion', 'reference dependencias', requires=False, label=T('Unidad de Adscripción')),

    Field('id_sede', 'reference sedes', requires=IS_IN_DB(db, db.sedes.id, '%(nombre)s'), label=T('Sede')),

    Field('ext_USB', 'list:integer', label=T('Extension Telefonica USB')),

    Field('ext_interna', 'string', label=T('Extension Telefonica Interna')),

    Field('fax', 'integer', label=T('Fax')),

    Field('pagina_web', 'string', label=T('Pagina Web')),

    Field('id_jefe_dependencia', 'integer', label=T('Responsable')),

    Field("codigo_registro", "string", label=T("Código de Registro")),
)

# Auto-Referencia, se definira cual dependencia es la unidad de adscripcion, esta sera una relacion de 0-1 a muchos
# una dependencia tendra adscrita varias, pero cada dependencia tendra o ninguna o una dependencia 'jefe'

# Se define fuera de la tabla para asegurar su existencia antes de ser referenciada

db.dependencias.unidad_de_adscripcion.requires = IS_EMPTY_OR(IS_IN_DB(db, db.dependencias.id, '%(nombre)s', zero=None))
db.dependencias._plural = 'Dependencias'
db.dependencias._singular = 'Dependencia'

#######################################################################################################################
#
# Tablas de Autenticacion de Usuarios
#
#######################################################################################################################

# Aqui se crearan las tablas de autenticacion, antes de ser estas definidas por web2py.
# Despues de auth = Auth(db) pero antes de auth.define_tables(username=True)
# (En el archivo 'db.py', la linea auth.define_tables(username=True) fue eliminada para ser usada aqui)

# La tabla de auth_membership funcionara como la tabla de roles, asociaremos a esta una referencia a las dependencias.
auth.settings.extra_fields['auth_membership'] = [
    Field('dependencia_asociada', 'string',
          label=T('Dependencia Asociada al Rol')),
    Field('f_personal_membership', 'string', label=T('Ci'))
]


# Definimos todas las tablas de web2py por defecto con las modificaciones hechas

auth.define_tables()

db.auth_membership.dependencia_asociada.requires = IS_IN_DB(db, db.dependencias.id, '%(nombre)s', zero=None)
db.auth_membership.dependencia_asociada.type = 'reference dependencias'
db.dependencias.id_jefe_dependencia.requires = IS_IN_DB(db, db.auth_user, '%(first_name)s %(last_name)s | %(email)s')
db.dependencias.id_jefe_dependencia.type = 'reference auth_user'

#######################################################################################################################
#
# Tabla principal del modulo de t_personal. Englobara la info de cada persona en la unidad de laboratorios. Es necesaria
# para el funcionamiento de cualquier otro modulo
#
#######################################################################################################################
def date_widget(f,v):
    wrapper = DIV()
    inp = SQLFORM.widgets.date.widget
    jqscr = SCRIPT("jQuery(document).ready(function(){jQuery('#%s').datepicker({dateFormat:'yy-mm-dd'});});" % inp['_id'],_type="text/javascript")
    wrapper.components.extend([inp,jqscr])
    return wrapper



db.define_table(
    #Nombre de la entidad
    't_Personal',
    #Atributos;
    Field('f_nombre',         'string',
          requires=IS_MATCH('^\w\w*[\s-]?\w*$',
                            error_message='Debe ser no vacío y contener sólo letras, guiones o espacios.'),
          notnull=True, label=T('Nombre')),

    Field('f_apellido',         'string',
          requires=IS_MATCH('^\w\w*[\s-]?\w*$',
                            error_message='Debe ser no vacío y contener sólo letras, guiones o espacios.'),

          notnull=True, label=T('Apellido')),

    Field('f_gremio',      'string',
          requires=IS_IN_SET(['Docente', 'Administrativo', 'Estudiante']), label=T('Gremio'),error_message='Por favor introduzca un valor'),

    Field('f_cargo',          'string',
          requires=IS_NOT_EMPTY(), label=T('Cargo'),error_message='Por favor introduzca un valor'),

    Field('f_ci',             'integer',
          requires=IS_MATCH('^\d*', error_message='Número de cedula inválido.'),
          notnull=True, label=T('Cédula')),
    Field('f_telefono',       'string', requires=IS_MATCH('\d{0,4}-?\d*'), label=T('Teléfono') ,error_message='Por favor introduzca un valor'),
    Field('f_celular',       'string', requires=IS_MATCH('\d{0,4}-?\d*'), label=T('Celular') ,error_message='Por favor introduzca un valor'),
    Field('f_contacto_emergencia',       'string', requires=IS_MATCH('\d{0,4}-?\d*'), label=T('Contacto de Emergencia'),error_message='Por favor introduzca un valor'),

    Field('f_email',          'string',
          requires=IS_EMAIL(error_message='Debe tener un formato válido. EJ: example@org.com'),
           label=T('Correo Electrónico')),
    Field('f_direccion',          'string',
          requires=IS_NOT_EMPTY(), label=T('Direccion') ,error_message='Por favor introduzca un valor'),
    Field('f_ubicacion',          'string',
          requires=IS_NOT_EMPTY(),  label=T('Ubicacion') ,error_message='Por favor introduzca un valor'),
    Field('f_pagina_web',     'string', requires=IS_URL() ,  label=T('Página web'), error_message='Ingrese un formato válido de url'),

    Field('f_estatus',        'string', requires=IS_IN_SET(['Activo', 'Jubilado']), label=T('Estatus') ,error_message='Por favor introduzca un valor'),
    Field('f_categoria',requires=IS_IN_SET(['Fijo', 'Contratado', 'Pasantía', 'Ayudantía']), label=T('Categoria') ,error_message='Por favor introduzca un valor'),
    ##Campos condicionales si la categoria es contratado, pasantia o ayudantia.
    Field('f_fecha_ingreso', 'date', label=T('Fecha de Ingreso')),
    Field('f_fecha_salida', 'date', label=T('Fecha de Salida')),
    ##
    Field('f_fecha_ingreso_usb','date',   label=T('Fecha de Ingreso a la USB')),
    Field('f_fecha_ingreso_ulab', 'date',   label=T('Fecha de Ingreso a la ULAB')),
    Field('f_fecha_ingreso_admin_publica', 'date', label=T('Fecha de Ingreso a la Administracion Pública')),
    Field('f_condicion', requires=IS_IN_SET(['En Funciones', 'Año Sabatico', 'Reposo', 'Permiso PreNatal', 'Permiso PostNatal']), label=T('Condición') ,error_message='Por favor introduzca un valor'),
    Field('f_unidad_jerarquica_superior', 'reference dependencias',  requires=IS_IN_DB(db, db.dependencias, '%(nombre)s'),  label=T('Unidad Jerarquica Superior') ,error_message='Por favor introduzca un valor'),
    Field('f_rol', 'reference auth_group', requires=IS_IN_DB(db, db.auth_group, '%(description)s'), label=T('Rol')),

    # #Referencias
     Field('f_usuario', 'reference auth_user',
           requires=IS_IN_DB(db, db.auth_user.id, '%(first_name)s %(last_name)s | %(email)s'), label=T('Usuario Asociado')),

    Field('f_dependencia', 'reference dependencias',
          requires=IS_IN_DB(db, db.dependencias, '%(nombre)s'), label=T('Dependencia')),
    Field('f_validado', 'boolean', default=False)
    )

db.t_Personal._plural = 'Personal'
db.t_Personal._singular = 'Personal'

db.t_Personal.f_fecha_salida.widget=SQLFORM.widgets.time.widget

db.auth_membership.f_personal_membership.type = 'reference t_Personal'
db.auth_membership.f_personal_membership.requires = IS_IN_DB(db, db.t_Personal.id, '%(f_ci)s', zero=None)

#######################################################################################################################
#
# Tablas Generales
#
#######################################################################################################################


# Tabla de Espacios Fisicos, incluira el nombre, la direccion de este y bajo que dependencia esta adscrito
db.define_table(
    'espacios_fisicos',
    #Atributos;
    Field('nombre', 'string', unique=True, notnull=True, label=T('Nombre')),

    Field('uso', 'string', notnull=True, label=T('Uso del espacio físico')),
    
    Field('dependencia', 'reference dependencias',
        requires=IS_IN_DB(db, db.dependencias.id, '%(nombre)s', zero=None), label=T('Dependencia')), 
        migrate=True)

db.espacios_fisicos._plural = 'Espacio Fisico'
db.espacios_fisicos._singular = 'Espacio Fisico'

# Tabla "es_encargado" mapea espacios fisicos a sus tecnicos encargados.
db.define_table(
    'es_encargado',
    #Atributos;
    Field('espacio_fisico', 'reference espacios_fisicos', 
            requires=IS_IN_DB(db, db.espacios_fisicos.id, '%(codigo)s', zero=None)), 

    Field('tecnico', 'reference t_Personal', 
            requires=IS_IN_DB(db, db.t_Personal.id, '%(f_email)s', zero=None))
    )
