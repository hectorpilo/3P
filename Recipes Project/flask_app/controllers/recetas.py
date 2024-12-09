from flask import render_template, redirect, session, url_for, flash, request
from flask_app import app
from flask_app.models.receta import Receta
from flask_app.models.ingrediente import Ingrediente

# Agregar la ruta para ver una receta individual
@app.route('/receta/<int:receta_id>')
def ver_receta(receta_id):
    # Verificar si el usuario está logueado
    if 'usuario_id' not in session:
        return redirect('/login')
    
    receta = Receta.get_by_id(receta_id)
    if not receta:
        flash("Receta no encontrada", "error")
        return redirect('/')
    
    # Convertir el usuario_id de la sesión a entero
    usuario_actual = int(session['usuario_id'])
    
    return render_template('ver_receta.html', 
                         receta=receta,
                         usuario_actual=usuario_actual)

@app.route('/receta/editar/<int:id>')
def editar_receta(id):
    if 'usuario_id' not in session:
        return redirect('/login')
    
    receta = Receta.get_by_id(id)
    if not receta:
        flash("Receta no encontrada", "error")
        return redirect('/')
        
    # Verificar que el usuario sea el dueño de la receta
    if int(session['usuario_id']) != receta.usuario_id:
        flash("No tienes permiso para editar esta receta", "error")
        return redirect('/')
        
    return render_template('editar_receta.html', receta=receta) 

@app.route('/receta/<int:receta_id>/ingrediente', methods=['POST'])
def agregar_ingrediente(receta_id):
    if 'usuario_id' not in session:
        return redirect('/login')
    
    receta = Receta.get_by_id(receta_id)
    if not receta or receta.usuario_id != int(session['usuario_id']):
        flash("No tienes permiso para modificar esta receta", "error")
        return redirect('/')
    
    # Crear nuevo ingrediente
    data = {
        'receta_id': receta_id,
        'nombre': request.form['nombre'],
        'cantidad': float(request.form['cantidad']),
        'unidad_medida': request.form['unidad_medida']
    }
    
    Ingrediente.save(data)
    return redirect(url_for('ver_receta', receta_id=receta_id))

@app.route('/receta/<int:receta_id>/ingrediente/<int:ingrediente_id>/eliminar', methods=['POST'])
def eliminar_ingrediente(receta_id, ingrediente_id):
    if 'usuario_id' not in session:
        return redirect('/login')
    
    receta = Receta.get_by_id(receta_id)
    if not receta or receta.usuario_id != int(session['usuario_id']):
        flash("No tienes permiso para modificar esta receta", "error")
        return redirect('/')
    
    Ingrediente.delete(ingrediente_id)
    return redirect(url_for('ver_receta', receta_id=receta_id)) 