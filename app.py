
from flask import Flask, jsonify, request, render_template
# del modulo flask importar la clase Flask y los métodos jsonify,request
from flask_cors import CORS       # del modulo flask_cors importar CORS
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow


app = Flask(__name__,template_folder='/home/otorres/mysite/templates/', static_folder='/home/otorres/mysite/static/')

# @app.route('/productos')
# def productos():
#     return render_template('productos.html')

CORS(app) #modulo cors es para que me permita acceder desde el frontend al backend

# configuro la base de datos, con el nombre el usuario y la clave
app.config['SQLALCHEMY_DATABASE_URI']='mysql+pymysql://otorres:bibianac@otorres.mysql.pythonanywhere-services.com/otorres$default'
# URI de la BBDD                          driver de la BD  user:clave@URLBBDD/nombreBBDD
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False #none
db= SQLAlchemy(app)   #crea el objeto db de la clase SQLAlquemy
ma=Marshmallow(app)   #crea el objeto ma de de la clase Marshmallow


class Producto(db.Model):  # Producto hereda de db.Model
    """
    Definición de la tabla Producto en la base de datos.
    La clase Producto hereda de db.Model.
    Esta clase representa la tabla "Producto" en la base de datos.
    """
    id = db.Column(db.Integer, primary_key=True)
    imagen = db.Column(db.String(400))
    nombre = db.Column(db.String(100))
    tipo = db.Column(db.String(20))
    tipo2 = db.Column(db.String(20))
    nivel = db.Column(db.Integer)
    evo = db.Column(db.Integer)
    evonum = db.Column(db.Integer)


    def __init__(self, imagen, nombre, tipo, tipo2, nivel, evo, evonum):
        """
        Constructor de la clase Producto.

        Args:
            nombre (str): Nombre del producto.
            precio (int): Precio del producto.
            stock (int): Cantidad en stock del producto.
            imagen (str): URL o ruta de la imagen del producto.
        """
        self.imagen = imagen
        self.nombre = nombre
        self.tipo = tipo
        self.tipo2 = tipo2
        self.nivel = nivel
        self.evo = evo
        self.evonum = evonum


    # Se pueden agregar más clases para definir otras tablas en la base de datos

with app.app_context():
    db.create_all()  # Crea todas las tablas en la base de datos

# Definición del esquema para la clase Producto
class ProductoSchema(ma.Schema):
    """
    Esquema de la clase Producto.

    Este esquema define los campos que serán serializados/deserializados
    para la clase Producto.
    """
    class Meta:
        fields = ("id", "imagen", "nombre", "tipo", "tipo2", "nivel", "evo", "evonum" )

producto_schema = ProductoSchema()  # Objeto para serializar/deserializar un producto
productos_schema = ProductoSchema(many=True)  # Objeto para serializar/deserializar múltiples productos

'''
Este código define un endpoint que permite obtener todos los productos de la base de datos y los devuelve como un JSON en respuesta a una solicitud GET a la ruta /productos.
@app.route("/productos", methods=["GET"]): Este decorador establece la ruta /productos para este endpoint y especifica que solo acepta solicitudes GET.
def get_Productos(): Esta es la función asociada al endpoint. Se ejecuta cuando se realiza una solicitud GET a la ruta /productos.
all_productos = Producto.query.all(): Se obtienen todos los registros de la tabla de productos mediante la consulta Producto.query.all(). Esto se realiza utilizando el modelo Producto que representa la tabla en la base de datos. El método query.all() heredado de db.Model se utiliza para obtener todos los registros de la tabla.
result = productos_schema.dump(all_productos): Los registros obtenidos se serializan en formato JSON utilizando el método dump() del objeto productos_schema. El método dump() heredado de ma.Schema se utiliza para convertir los objetos Python en representaciones JSON.
return jsonify(result): El resultado serializado en formato JSON se devuelve como respuesta al cliente utilizando la función jsonify() de Flask. Esta función envuelve el resultado en una respuesta HTTP con el encabezado Content-Type establecido como application/json.

'''
@app.route("/productos", methods=["GET"])
def get_Productos():
    """
    Endpoint para obtener todos los productos de la base de datos.

    Retorna un JSON con todos los registros de la tabla de productos.
    """
    all_productos = Producto.query.all()  # Obtiene todos los registros de la tabla de productos
    result = productos_schema.dump(all_productos)  # Serializa los registros en formato JSON
    return jsonify(result)  # Retorna el JSON de todos los registros de la tabla

'''
El código que sigue a continuación termina de resolver la API de gestión de productos, a continuación se destaca los principales detalles de cada endpoint, incluyendo su funcionalidad y el tipo de respuesta que se espera.
Endpoints de la API de gestión de productos:
get_producto(id):
    # Obtiene un producto específico de la base de datos
    # Retorna un JSON con la información del producto correspondiente al ID proporcionado
delete_producto(id):
    # Elimina un producto de la base de datos
    # Retorna un JSON con el registro eliminado del producto correspondiente al ID proporcionado
create_producto():
    # Crea un nuevo producto en la base de datos
    # Lee los datos proporcionados en formato JSON por el cliente y crea un nuevo registro de producto
    # Retorna un JSON con el nuevo producto creado
update_producto(id):
    # Actualiza un producto existente en la base de datos
    # Lee los datos proporcionados en formato JSON por el cliente y actualiza el registro del producto con el ID especificado
    # Retorna un JSON con el producto actualizado

'''
@app.route("/productos/<id>", methods=["GET"])
def get_producto(id):
    """
    Endpoint para obtener un producto específico de la base de datos.

    Retorna un JSON con la información del producto correspondiente al ID proporcionado.
    """
    producto = Producto.query.get(id)  # Obtiene el producto correspondiente al ID recibido
    return producto_schema.jsonify(producto)  # Retorna el JSON del producto

@app.route("/productos/<id>", methods=["DELETE"])
def delete_producto(id):
    """
    Endpoint para eliminar un producto de la base de datos.

    Elimina el producto correspondiente al ID proporcionado y retorna un JSON con el registro eliminado.
    """
    producto = Producto.query.get(id)  # Obtiene el producto correspondiente al ID recibido
    db.session.delete(producto)  # Elimina el producto de la sesión de la base de datos
    db.session.commit()  # Guarda los cambios en la base de datos
    return producto_schema.jsonify(producto)  # Retorna el JSON del producto eliminado

@app.route("/productos", methods=["POST"])  # Endpoint para crear un producto
def create_producto():
    """
    Endpoint para crear un nuevo producto en la base de datos.

    Lee los datos proporcionados en formato JSON por el cliente y crea un nuevo registro de producto en la base de datos.
    Retorna un JSON con el nuevo producto creado.
    """
    imagen = request.json["imagen"]  # Obtiene la imagen del producto del JSON proporcionado
    nombre = request.json["nombre"]  # Obtiene el nombre del producto del JSON proporcionado
    tipo = request.json["tipo"]  # Obtiene el precio del producto del JSON proporcionado
    tipo2 = request.json["tipo2"]  # Obtiene el stock del producto del JSON proporcionado
    nivel = request.json["nivel"]
    evo = request.json["evo"]
    evonum = request.json["evonum"]

    new_producto = Producto(imagen, nombre, tipo, tipo2, nivel, evo, evonum)  # Crea un nuevo objeto Producto con los datos proporcionados
    db.session.add(new_producto)  # Agrega el nuevo producto a la sesión de la base de datos
    db.session.commit()  # Guarda los cambios en la base de datos
    return producto_schema.jsonify(new_producto)  # Retorna el JSON del nuevo producto creado

@app.route("/productos/<id>", methods=["PUT"])  # Endpoint para actualizar un producto
def update_producto(id):
    """
    Endpoint para actualizar un producto existente en la base de datos.

    Lee los datos proporcionados en formato JSON por el cliente y actualiza el registro del producto con el ID especificado.
    Retorna un JSON con el producto actualizado.
    """
    producto = Producto.query.get(id)  # Obtiene el producto existente con el ID especificado

    # Actualiza los atributos del producto con los datos proporcionados en el JSON
    producto.imagen = request.json["imagen"]
    producto.nombre = request.json["nombre"]
    producto.tipo = request.json["tipo"]
    producto.tipo2 = request.json["tipo2"]
    producto.nivel = request.json["nivel"]
    # producto.evo = request.json["evo"]
    # producto.evonum = request.json["evonum"]


    db.session.commit()  # Guarda los cambios en la base de datos
    return producto_schema.jsonify(producto)  # Retorna el JSON del producto actualizado

@app.route('/incrementar-nivel', methods=['POST'])
def incrementar_nivel():

    id = request.json.get('id')
    # Obtener el producto correspondiente desde la base de datos basado en el ID
    producto = Producto.query.get(id)
    print('ID del producto:', producto.nivel)
    if producto is None:
        return 'No se encontró el producto'

    # Incrementar en 1 el valor del campo "nivel"
    producto.nivel += 1

    # Guardar los cambios en la base de datos
    db.session.commit()

    respuesta = 'Campo "nivel" incrementado en 1'

    # print(respuesta)

    return respuesta

'''
Este código es el programa principal de la aplicación Flask. Se verifica si el archivo actual está siendo ejecutado directamente y no importado como módulo. Luego, se inicia el servidor Flask en el puerto 5000 con el modo de depuración habilitado. Esto permite ejecutar la aplicación y realizar pruebas mientras se muestra información adicional de depuración en caso de errores.

'''

# @app.route('/')
# def hello_world():
#     return 'Hello from Flask'

@app.route('/')
def home():
    return render_template('productos.html')

@app.route('/templates/producto_update.html')
def editar():
    return render_template('producto_update.html')

@app.route('/templates/producto_nuevo.html')
def capturar():
    return render_template('producto_nuevo.html')










