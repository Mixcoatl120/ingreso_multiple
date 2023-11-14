from flask import Flask,render_template,request,redirect,url_for,flash
from flask_sqlalchemy import SQLAlchemy
import datetime

db = SQLAlchemy()

class Usuario(db.Model):
    __tablename__ = 'usuarios'

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)

class Seguimiento(db.Model): #------------------Seguimiento----------------------
    __tablename__ = 'seguimiento'

    cve_unidad = db.Column(db.Integer)
    tipo_ingreso = db.Column(db.Integer)
    tipo_asunto = db.Column(db.Integer)
    materia = db.Column(db.Integer)
    tramite = db.Column(db.Integer)
    descripcion = db.Column(db.Integer)
    bitacora_expediente = db.Column(db.String(100), primary_key=True)
    cve_procedencia = db.Column(db.Integer)
    clave_proyecto = db.Column(db.String(100))
    cadena_valor = db.Column(db.Integer)
    rnomrazonsolcial = db.Column(db.String(255))
    tipopersonalidad = db.Column(db.Integer)
    dirgralfirma = db.Column(db.Integer)
    turnado_da = db.Column(db.Integer)
    llavepago = db.Column(db.String(100))
    totaltrami_pago = db.Column(db.Integer)
    couta_pago = db.Column(db.String(64))
    monto_total = db.Column(db.String(64))
    contenido = db.Column(db.Text)
    persona_ingresa = db.Column(db.Integer)
    observaciones = db.Column(db.Text)
    antecedente = db.Column(db.String(512))
    clave_documento = db.Column(db.String(128))
    fecha_documento = db.Column(db.Date)
    contrato_cnh = db.Column(db.String(64))
    con_copia = db.Column(db.Text)
    permiso_cre = db.Column(db.String(64))
    fsolicitud = db.Column(db.Date)
    fingreso_siset = db.Column(db.Date)
    estatus_tramite = db.Column(db.Integer)
    situacionactualtram = db.Column(db.Integer)
    nomreplegal = db.Column(db.String(255))

class Personal(db.Model): #------------------Personal----------------------
    __tablename__ = 'cat_personal'

    idpers = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(255))
    active = db.Column(db.String(2))
    login = db.Column(db.String(50))
    
    def __init__(self,idpers,nombre,active,login):
        self.idpers = idpers
        self.nombre = nombre
        self.active = active
        self.login = login

class IngresoAsea(db.Model): #------------------------- vista_ingreso asea------------------
    __tablename__ = 'ingreso_asea'
    fecha_ingreso_siset = db.Column(db.Date)
    fecha_ingreso = db.Column(db.Date)
    bitacora_folio = db.Column(db.String, primary_key=True)
    unidad = db.Column(db.Integer)
    razon_social = db.Column(db.String(255))

    
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:Asea2023@localhost/siset'
app.config['SECRET_KEY'] = 'MIXCOATL12O'
db.init_app(app)

@app.route('/')
def index():
    return render_template('formulario.html')

@app.route('/agregar_usuario', methods=['POST','GET'])
def agregar_usuario():
    nombre = request.form.get('nombre')
    email = request.form.get('email')
    rs = request.form.get('rs')
    usuarios = Usuario.query.all()
    print(rs)

    nuevo_usuario = Usuario(nombre=nombre, email=email)
    db.session.add(nuevo_usuario)
    db.session.commit()
    flash(f'Se ha agregado correctamente a {nombre}', 'success')  # Mensaje de éxito
    return render_template('formulario.html',usuarios=usuarios)

@app.route('/folio',methods=['POST','GET'])
def Folio():
    if request.method == 'POST':
        # datos del formulario
        ti = request.form['ti']
        ta = request.form['ta']
        mat = request.form['mat']
        tra = request.form['tra']
        des = request.form['des']
        pro = request.form['pro']
        cp = request.form['cp']
        cv = request.form['cv']
        rs = request.form['rs']
        tp = request.form['tp']
        pit = request.form['pit']
        dg = request.form['dg']
        res = request.form['res']
        llp = request.form['llp']
        tt = request.form['tt']
        cup = request.form['cup']
        mot = request.form['mot']
        con = request.form['con']
        obs = request.form['obs']
        ant = request.form['ant']
        cd = request.form['cd']
        fd = request.form['fd']
        cnh = request.form['cnh']
        cc = request.form['cc']
        cre = request.form['cre']
        tec = request.form['tec']

        # Obtener la fecha actual
        fecha_actual = datetime.date.today()
        # Obtener fecha y hora
        fat = datetime.datetime.now()
        # Hora completa
        fecha_larga = fat.strftime("%d/%m/%y %H:%M:%S")
        # Obtener los últimos dos dígitos del año
        ao_corto = fecha_actual.year % 100
        # Imprimir la fecha con el mes y los últimos dos dígitos del año
        f = fecha_actual.strftime(f"%m/{ao_corto:02}")

        # subconsulta
        #         ||    Select     ||   MAX    ||        columnas             ||
        subquery = db.session.query(db.func.max(IngresoAsea.fecha_ingreso_siset)).subquery() # .subquery indica que sera una subconsulta para poder agregarla a la principal
    
        # Consulta principal 
        #       ||     select   ||     bitacora_folio     || where ||    fecha_ingreso_siset = subconsulta    ||order by ||  bitacora_folio         ||DESC || LIMIT                                
        query = db.session.query(IngresoAsea.bitacora_folio).filter(IngresoAsea.fecha_ingreso_siset == subquery).order_by(IngresoAsea.bitacora_folio.desc()).limit(1)
        result = query.scalar() # obtiene todas los resultados
        uld = int(result[:7]) + 1
        # folio
        folio = "0"+str(uld) +"/"+f

        if(fd != ""):
            # busca el id de la sesion iniciada
            idp = Personal.query.filter_by(login = tec).first()
            insert = Seguimiento(cve_unidad = 2,
                                tipo_ingreso = ti,
                                tipo_asunto = ta,
                                materia = mat,
                                tramite = tra,
                                descripcion = des,
                                bitacora_expediente = folio,
                                cve_procedencia = pro,
                                clave_proyecto = cp,
                                cadena_valor = cv,
                                rnomrazonsolcial = rs,
                                tipopersonalidad = tp,
                                nomreplegal = pit,
                                dirgralfirma = dg,
                                turnado_da = res,
                                llavepago = llp,
                                totaltrami_pago = tt,
                                couta_pago = cup,
                                monto_total = mot,
                                contenido = con,
                                persona_ingresa = 0,
                                observaciones = obs,
                                antecedente = ant,
                                clave_documento = cd,
                                fecha_documento = fd,
                                contrato_cnh = cnh,
                                con_copia = cc,
                                permiso_cre = cre,
                                fsolicitud = fecha_actual,
                                fingreso_siset = fecha_larga,
                                estatus_tramite = 1,
                                situacionactualtram = 9
        )
        else:
            # busca el id de la sesion iniciada
            idp = Personal.query.filter_by(login = tec).first()
            insert = Seguimiento(cve_unidad = 2,
                                tipo_ingreso = ti,
                                tipo_asunto = ta,
                                materia = mat,
                                tramite = tra,
                                descripcion = des,
                                bitacora_expediente = folio,
                                cve_procedencia = pro,
                                clave_proyecto = cp,
                                cadena_valor = cv,
                                rnomrazonsolcial = rs,
                                tipopersonalidad = tp,
                                nomreplegal = pit,
                                dirgralfirma = dg,
                                turnado_da = res,
                                llavepago = llp,
                                totaltrami_pago = tt,
                                couta_pago = cup,
                                monto_total = mot,
                                contenido = con,
                                persona_ingresa = 0,
                                observaciones = obs,
                                antecedente = ant,
                                clave_documento = cd,
                                fecha_documento = None,
                                contrato_cnh = cnh,
                                con_copia = cc,
                                permiso_cre = cre,
                                fsolicitud = fecha_actual,
                                fingreso_siset = fecha_larga,
                                estatus_tramite = 1,
                                situacionactualtram = 9
            )            
        db.session.add(insert)
        db.session.commit()
        db.session.close()

        flash(f'Se ha agregado correctamente el: {folio}', 'success')  # Mensaje de éxito
    
    return render_template('formulario.html',usuarios=insert,folio=folio)

if __name__ == '__main__':
    app.run()
