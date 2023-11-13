from flask import Flask,render_template,request,redirect,url_for,flash
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Usuario(db.Model):
    __tablename__ = 'usuarios'

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:Asea2023@localhost/users'
app.config['SECRET_KEY'] = 'MIXCOATL12O'
db.init_app(app)

@app.route('/')
def index():
    
    return render_template('index.html')

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
    return render_template('index.html',usuarios=usuarios)

if __name__ == '__main__':
    app.run()
