from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL


# initializations
app = Flask(__name__)

# Mysql Connection
app.config['MYSQL_HOST'] = 'localhost' 
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'flaskcrud'
mysql = MySQL(app)

# settings
app.secret_key = "mysecretkey"


@app.route('/')
def home():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM casos')
    data = cur.fetchall()
    cur.close()
    return render_template('gestor.html', casos = data)

@app.route('/singup')
def singup():
    
    return render_template('singup.html')


@app.route('/search_caso', methods=['POST'])
def search_caso():
    if request.method == 'POST':
        
        bcaso = request.form['bcaso']
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM casos WHERE caso= %s",(bcaso))
        mysql.connection.commit()
        return redirect(url_for('home'))


@app.route('/add_caso', methods=['POST'])
def add_caso():
    if request.method == 'POST':
        
        nombre = request.form['nombre']
        telefono = request.form['telefono']
        localidad = request.form['localidad']
        direccion = request.form['direccion']
        afectacion = request.form['afectacion']
        caso = request.form['caso']
        estado = request.form['estado']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO casos (nombre, telefono, localidad, direccion, afectacion, caso, estado) VALUES (%s, %s, %s, %s, %s, %s, %s)", (nombre, telefono, localidad, direccion, afectacion, caso, estado))
        mysql.connection.commit()
        flash('El caso a sido agregado.')
        return redirect(url_for('home'))


@app.route('/edit/<id>')
def get_caso(id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM casos WHERE id=%s',[id])
    data=cur.fetchall()
    cur.close()
    print(data[0])
    return render_template('edit-caso.html', case = data[0])

@app.route('/update/<id>', methods = ['POST'])
def update_case(id):
    if request.method == 'POST':
        nombre = request.form['nombre']
        telefono = request.form['telefono']
        localidad = request.form['localidad']
        direccion = request.form['direccion']
        afectacion = request.form['afectacion']
        caso = request.form['caso']
        estado = request.form['estado']
        cur = mysql.connection.cursor()
        cur.execute("""
            UPDATE casos
            SET nombre = %s,
                telefono = %s,
                localidad = %s,
                direccion = %s,
                afectacion = %s,
                caso = %s,
                estado = %s
            WHERE id = %s
        """,(nombre, telefono, localidad, direccion, afectacion, caso, estado,id))
        mysql.connection.commit()
        flash('Case update successfully')
        return redirect(url_for('home'))


@app.route('/delete/<string:id>')
def delete_caso(id):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM casos WHERE id ={0}' .format(id))
    mysql.connection.commit()
    return redirect(url_for('home'))

if __name__=='__main__':
    app.run(debug=True)