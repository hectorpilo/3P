from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import DATABASE

class Ingrediente:
    def __init__(self, data):
        self.id = data['id']
        self.receta_id = data['receta_id']
        self.nombre = data['nombre']
        self.cantidad = data['cantidad']
        self.unidad_medida = data['unidad_medida']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
    
    @classmethod
    def save(cls, data):
        query = """
            INSERT INTO ingredientes (receta_id, nombre, cantidad, unidad_medida)
            VALUES (%(receta_id)s, %(nombre)s, %(cantidad)s, %(unidad_medida)s)
        """
        return connectToMySQL(DATABASE).query_db(query, data)
    
    @classmethod
    def delete(cls, ingrediente_id):
        query = "DELETE FROM ingredientes WHERE id = %(id)s"
        return connectToMySQL(DATABASE).query_db(query, {'id': ingrediente_id}) 