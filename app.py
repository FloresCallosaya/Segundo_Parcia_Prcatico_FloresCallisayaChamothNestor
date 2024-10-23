from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'clave_secreta'

# Inicializar la lista de productos en la sesión
@app.before_request
def iniciar_sesion():
    if 'productos' not in session:
        session['productos'] = []

# Página principal (lista de productos)
@app.route('/')
def index():
    return render_template('index.html', productos=session['productos'])

# Ruta para agregar un nuevo producto
@app.route('/agregar', methods=['POST'])
def agregar():
    nuevo_producto = {
        'id': request.form['id'],
        'nombre': request.form['nombre'],
        'cantidad': request.form['cantidad'],
        'precio': request.form['precio'],
        'fecha_vencimiento': request.form['fecha_vencimiento'],
        'categoria': request.form['categoria']
    }
    session['productos'].append(nuevo_producto)
    session.modified = True
    return redirect(url_for('index'))

# Ruta para eliminar un producto
@app.route('/eliminar/<string:id>')
def eliminar(id):
    session['productos'] = [p for p in session['productos'] if p['id'] != id]
    session.modified = True
    return redirect(url_for('index'))

# Ruta para editar un producto
@app.route('/editar/<string:id>', methods=['GET', 'POST'])
def editar(id):
    producto = next((p for p in session['productos'] if p['id'] == id), None)
    
    if request.method == 'POST':
        producto['nombre'] = request.form['nombre']
        producto['cantidad'] = request.form['cantidad']
        producto['precio'] = request.form['precio']
        producto['fecha_vencimiento'] = request.form['fecha_vencimiento']
        producto['categoria'] = request.form['categoria']
        session.modified = True
        return redirect(url_for('index'))
    
    return render_template('editar.html', producto=producto)

if __name__ == '__main__':
    app.run(debug=True)
