from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import DATABASE
from flask_app.models.ingrediente import Ingrediente

class Receta:
    def __init__(self, data):
        self.id = data['id']
        self.titulo = data['titulo']
        self.tiempo_prep = data['tiempo_prep']
        self.porciones = data['porciones']
        self.instrucciones = data['instrucciones']
        self.usuario_id = data['usuario_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.ingredientes = []

    @classmethod
    def get_by_id(cls, id):
        query = """
            SELECT r.*, u.username as usuario_nombre
            FROM recetas r
            LEFT JOIN usuarios u ON r.usuario_id = u.id
            WHERE r.id = %(id)s;
        """
        results = connectToMySQL(DATABASE).query_db(query, {'id': id})
        if not results:
            return None
            
        receta = cls(results[0])
        receta.usuario_nombre = results[0]['usuario_nombre']
        
        # Obtener los ingredientes de la receta
        query_ingredientes = """
            SELECT * FROM ingredientes 
            WHERE receta_id = %(receta_id)s;
        """
        ingredientes = connectToMySQL(DATABASE).query_db(query_ingredientes, {'receta_id': id})
        
        if ingredientes:
            for ing in ingredientes:
                receta.ingredientes.append(Ingrediente(ing))
                
        return receta 