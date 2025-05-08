from flask import Flask,request,current_app,jsonify, Response
from flask_pymongo import PyMongo
from flask_restx import Api,Namespace,Resource,fields
from bson.objectid import ObjectId
from bson import json_util
from datetime import datetime, timezone


app = Flask(__name__)
app.config['MONGO_URI'] = 'mongodb://192.168.1.10:27017/agenciaViajes'
#app.config['MONGO_URI'] = 'mongodb://127.0.0.1:27017/agenciaViajes'
mongo = PyMongo(app) 
api = Api(app, version='1.0', title='Agencia de Viajes API', doc='/swagger')

empleados_ns = api.namespace('empleados', description='Operaciones con empleados')
destinos_ns = api.namespace('destinos', description='Operaciones con destinos')
clientes_ns = api.namespace('clientes', description='Operaciones con clientes')
pagos_ns = api.namespace('pagos', description='Operaciones con pagos')
reservas_ns = api.namespace('reservas', description='Operaciones con reservas')
resenias_ns = api.namespace('resenias', description='Operaciones con resenias')
sucursales_ns = api.namespace('sucursales', description='Operaciones con sucursales')
promociones_ns = api.namespace('promociones', description='Operaciones con promociones')
paquetes_ns = api.namespace('paquetes', description='Operaciones con paquetes')
logs_ns = api.namespace('logs', description='Operaciones con logs')

empleado_model = empleados_ns.model('Empleado', {
    'nombre': fields.String(required=True, description='Nombre del empleado'),
    'correo': fields.String(required=True, description='Correo del empleado'),
    'telefono': fields.String(required=True, description='Teléfono del empleado'),
    'activo': fields.Boolean(required=True, description='Estado del empleado'),
    'cargo': fields.String(required=True, description='Nombre del cargo'),
    'fecha_ingreso': fields.Date(required=True, description='Fecha de ingreso del empleado a la empresa'),
    'sucursal_id': fields.Integer(required=True, description='Sucursal a la que pertenece')
})

destino_model = destinos_ns.model('Destino', {
    'nombre': fields.String(required=True, description='Nombre del destino'),
    'pais': fields.String(required=True, description='Pais del destino'),
    'descripcion': fields.String(required=True, description='Descripcion del destino'),
    'precioBase': fields.Float(required=True, description='Precio del destino'),
    'temporadaAlta': fields.String(required=True, description='Temporada alta del destino'),
    'cupoMaximo': fields.Integer(required=True, description='Cupo Maximo del destino'),
    'promocion_id': fields.String(required=True, description='Promocion a la que pertenece'),
    'sucursal_id': fields.Integer(required=True, description='Sucursal a la que pertenece')
})

cliente_model = clientes_ns.model('Cliente', {
    'nombre': fields.String(required=True, description='Nombre del cliente'),
    'correo': fields.String(required=True, description='Correo del cliente'),
    'telefono': fields.String(required=True, description='Teléfono del cliente'),
    'direccion': fields.String(required=True, description='Direccion del cliente'),
    'fecha_nacimiento': fields.Date(required=True, description='Fecha de nacimiento del cliente'),
    'sucursal_id': fields.Integer(required=True, description='Sucursal a la que pertenece')
})

pago_model = pagos_ns.model('Pago', {
    'fecha_pago': fields.Date(required=True, description='Fecha en la que se realizo el pago'),
    'metodo_pago': fields.String(required=True, description='Metodo con el que se realizo el pago'),
    'estado': fields.String(required=True, description='Estado actual del pago'),
    'reserva_id': fields.String(required=True, description='Reservacion correspondiente al pago'),
    'sucursal_id': fields.Integer(required=True, description='Sucursal a la que pertenece') 
})

reserva_model = reservas_ns.model('Reserva', {
    'fecha_salida': fields.Date(required=True, description='Fecha de salida'),
    'fecha_regreso': fields.Date(required=True, description='Fecha de regreso'),
    'estado': fields.String(required=True, description='Estado actual de la reserva'),
    'detalles': fields.String(required=True, description='Detalles de la reserva'),
    'codigo_descuento': fields.String(required=True, description='Codigo de descuento del destino'),
    'cliente_id': fields.String(required=True, description='Cliente a la que pertenece'),
    'destino_id': fields.String(required=True, description='Destino a la que pertenece'),
    'sucursal_id': fields.Integer(required=True, description='Sucursal a la que pertenece') 
})

resenia_model = resenias_ns.model('Resenia', {
    'comentario': fields.String(required=True, description='Comentario de la resenia'),
    'calificacion': fields.Float(required=True, description='Calificacion de la resenia'),
    'fecha': fields.Date(required=True, description='Fecha de la resenia'),
    'reserva_id': fields.String(required=True, description='Reserva a la que pertenece'),
    'sucursal_id': fields.Integer(required=True, description='Sucursal a la que pertenece') 
})

sucursal_model = sucursales_ns.model('Sucursal', {
    'sucursal_id': fields.Integer(required=True, description='ID de la sucursal'),
    'nombre': fields.String(required=True, description='Nombre de la sucursal'),
    'direccion': fields.String(required=True, description='Direccion de la sucursal'),
    'telefono': fields.String(required=True, description='Telefono de la sucursal')
})

promocion_model = promociones_ns.model('Promocion', {
    'descripcion': fields.String(required=True, description='Descripcion de la promocion'),
    'codigo': fields.String(required=True, description='Codigo de la promocion'),
    'descuento': fields.Integer(required=True, description='Descuento de la promocion'),
    'fecha_inicio': fields.Date(required=True, description='Fecha de inicio de la promocion'),
    'fecha_fin': fields.Date(required=True, description='Fecha de fin de la promocion'),
    'sucursal_id': fields.Integer(required=True, description='ID de la sucursal a la que pertenece')
})

paquete_model = paquetes_ns.model('Paquete', {
    'nombre': fields.String(required=True, description='Nombre del paquete'),
    'precio': fields.Float(required=True, description='Precio del paquete'),
    'servicios': fields.List(fields.String, required=True, description='Servicios que incluye el paquete'),
    'duracion': fields.Integer(required=True, description='Duracion en dias del paquete'),
    'destinos': fields.List(fields.String, required=True, description='Destinos del paquete'),
    'sucursal_id': fields.Integer(required=True, description='ID de la sucursal a la que pertenece')
})

def create_indexes():
    if 'sucursal_id_1' not in mongo.db.empleado.index_information():
        mongo.db.empleado.create_index([('sucursal_id', 1)])
    elif 'sucursal_id_1' not in mongo.db.destino.index_information():
        mongo.db.destino.create_index([('sucursal_id', 1)])
    elif 'sucursal_id_1' not in mongo.db.sucursal.index_information():
        mongo.db.sucursal.create_index([('sucursal_id', 1)])
    elif 'sucursal_id_1' not in mongo.db.cliente.index_information():
        mongo.db.cliente.create_index([('sucursal_id', 1)])
    elif 'sucursal_id_1' not in mongo.db.pago.index_information():
        mongo.db.pago.create_index([('sucursal_id', 1)])
    elif 'sucursal_id_1' not in mongo.db.reserva.index_information():
        mongo.db.reserva.create_index([('sucursal_id', 1)])
    elif 'sucursal_id_1' not in mongo.db.resenia.index_information():
        mongo.db.resenia.create_index([('sucursal_id', 1)])
    elif 'sucursal_id_1' not in mongo.db.promocion.index_information():
        mongo.db.promocion.create_index([('sucursal_id', 1)])
    elif 'sucursal_id_1' not in mongo.db.paquete.index_information():
        mongo.db.paquete.create_index([('sucursal_id', 1)])
    elif 'sucursal_id_1' not in mongo.db.logTransaccion.index_information():
        mongo.db.logTransaccion.create_index([('sucursal_id', 1)])
create_indexes()


#Empleados
@empleados_ns.route("/agregar")
class AgregarEmpleado(Resource):
    @empleados_ns.expect(empleado_model)
    def post(self):
        data = request.json
            
        if not all(k in data for k in ("nombre", "correo", "telefono", "activo", "cargo", "fecha_ingreso", "sucursal_id")):
            return {"error": "Faltan campos obligatorios"}, 400

        nombre = data["nombre"]
        correo = data["correo"]
        telefono = data["telefono"]
        activo = data["activo"]
        cargo = data["cargo"]
        fecha_ingreso_str = data["fecha_ingreso"]
        fecha_ingreso = datetime.strptime(fecha_ingreso_str, "%Y-%m-%d")
        sucursal_id = data["sucursal_id"]
            
        sucursal = mongo.db.sucursal.find_one({"sucursal_id": sucursal_id})
        if not sucursal:
            return {'error': "No existe esa sucursal"}, 401

        result = mongo.db.empleado.insert_one({
            'nombre': nombre,
            'correo': correo,
            'telefono': telefono,
            'activo': activo,
            'cargo': cargo,
            'fecha_ingreso': fecha_ingreso,
            'sucursal_id': sucursal_id
        })

        object_id = str(result.inserted_id)
            
        mongo.db.logTransaccion.insert_one({
            'tipo': 'Agregar empleado',
            'detalle': 'Agregar empleado a la Base de Datos',
            'fecha': datetime.now(timezone.utc),
            'usuarioResponsable': 'Administrador',
            'sucursal_id': sucursal_id
        })

        response = {
            'id': object_id,
            'nombre': nombre,
            'correo': correo,
            'telefono': telefono,
            'activo': activo,
            'cargo': cargo,
            'fecha_ingreso': fecha_ingreso_str,
            'sucursal_id': sucursal_id
        }
        
        return response  

    
@empleados_ns.route("/<string:id>")
@empleados_ns.param('id', 'ObjectId del empleado')
class EditarEliminarEmpleado(Resource):
    def delete(self, id):
        empleado = mongo.db.empleado.find_one({"_id": ObjectId(id)})
        if not empleado:
            return {"error": "Empleado no encontrado"}, 404
        sucursal_id = empleado.get("sucursal_id")
        mongo.db.empleado.delete_one({ "_id": ObjectId(id)})

        mongo.db.logTransaccion.insert_one({
            'tipo': 'Eliminar empleado',
            'detalle': 'Eliminar empleado de la Base de Datos',
            'fecha': datetime.now(timezone.utc),
            'usuarioResponsable': 'Administrador',
            'sucursal_id': sucursal_id
        })

        return {'message': f'Empleado con id {id} eliminado exitosamente'}
    
    def get(self, id):
        empleado = mongo.db.empleado.find_one({"_id": ObjectId(id)})
        if not empleado:
            return {"error": "Empleado no encontrado"}, 404
        response = json_util.dumps(empleado)
        return Response(response, mimetype='application/json')
    
    @empleados_ns.expect(empleado_model)
    def patch(self, id):
        empleado = mongo.db.empleado.find_one({"_id": ObjectId(id)})
        if not empleado:
            return {"error": "Empleado no encontrado"}, 404
        data = request.json
        if 'nombre' in data:
            mongo.db.empleado.update_one({'_id': ObjectId(id)}, {'$set': {'nombre': data['nombre']}})
        if 'correo' in data:
            mongo.db.empleado.update_one({'_id': ObjectId(id)}, {'$set': {'correo': data['correo']}})
        if 'telefono' in data:
            mongo.db.empleado.update_one({'_id': ObjectId(id)}, {'$set': {'telefono': data['telefono']}})
        if 'activo' in data:
            mongo.db.empleado.update_one({'_id': ObjectId(id)}, {'$set': {'activo': data['activo']}})
        if 'cargo' in data:
            mongo.db.empleado.update_one({'_id': ObjectId(id)}, {'$set': {'cargo': data['cargo']}})
        if 'fecha_ingreso' in data:
            fecha_ingreso_str = data["fecha_ingreso"]
            fecha_ingreso = datetime.strptime(fecha_ingreso_str, "%Y-%m-%d")
            mongo.db.empleado.update_one({'_id': ObjectId(id)}, {'$set': {'fecha_ingreso': fecha_ingreso}})   
        if 'sucursal_id' in data:
            sucursal = mongo.db.sucursal.find_one({"sucursal_id": data['sucursal_id']})
            if not sucursal:
                return {'error': "No existe esa sucursal"},401
            mongo.db.empleado.update_one({'_id': ObjectId(id)}, {'$set': {'sucursal_id': data['sucursal_id']}}) 

        mongo.db.logTransaccion.insert_one({
            'tipo': 'Editar empleado',
            'detalle': 'Editar empleado de la Base de Datos',
            'fecha': datetime.now(timezone.utc),
            'usuarioResponsable': 'Administrador',
            'sucursal_id': empleado.get("sucursal_id")
        })

        return {"mensaje": f"Empleado con id {id} actualizado"}, 200


@empleados_ns.route("/allEmpleados")
class ListarEmpleados(Resource):
    def get(self):
        empleados = mongo.db.empleado.find({})
        if not empleados:
            return {"error": "Ningun empleado encontrado"}, 404
        response = json_util.dumps(empleados)
        return Response(response, mimetype='application/json')
    

@empleados_ns.route("/getEmployeesBySucursalId/<int:sucursal_id>")
@empleados_ns.param('sucursal_id', 'ID de la sucursal')
class ListarEmpleadosPorSucursal(Resource):
    def get(self, sucursal_id):
        sucursal = mongo.db.sucursal.find_one({ "sucursal_id": sucursal_id})
        if not sucursal:
            return {"error": f"Sucursal con id {sucursal_id} no encontrada"}, 404
        empleados = mongo.db.empleado.find({ "sucursal_id": sucursal_id})
        if not empleados:
            return {"error": "Ningun empleado encontrado"}, 404
        response = json_util.dumps(empleados)
        return Response(response, mimetype='application/json')


#Destinos
@destinos_ns.route("/agregar")
class AgregarDestino(Resource):
    @destinos_ns.expect(destino_model)
    def post(self):
        data = request.json

        if not all(k in data for k in ("nombre", "pais", "descripcion", "precioBase", "temporadaAlta", "cupoMaximo", "sucursal_id")):
            return {"error": "Faltan campos obligatorios"}, 400

        nombre = data["nombre"]
        pais = data["pais"]
        descripcion = data["descripcion"]
        precioBase = data["precioBase"]
        temporadaAlta = data["temporadaAlta"]
        cupoMaximo = data["cupoMaximo"]
        sucursal_id = data["sucursal_id"]
        
        sucursal = mongo.db.sucursal.find_one({"sucursal_id": sucursal_id})
        if not sucursal:
            return {'error': "No existe esa sucursal"},401
        
        destino_data = {
            'nombre': nombre,
            'pais': pais,
            'descripcion': descripcion,
            'precioBase': precioBase,
            'temporadaAlta': temporadaAlta,
            'cupoMaximo': cupoMaximo,
            'sucursal_id': sucursal_id
        }
        
        promocion_id = data.get("promocion_id")
        if promocion_id:
            try:
                promocion = mongo.db.promocion.find_one({"_id": ObjectId(promocion_id)})
                if not promocion:
                    return {'error': "No existe esa promoción"}, 402
            except Exception as e:
                return {'error': str(e)}, 400
            fecha_inicio_promocion = promocion.get('fecha_inicio')
            fecha_fin_promocion = promocion.get('fecha_fin')
            if fecha_inicio_promocion.replace(tzinfo=timezone.utc) > datetime.now(timezone.utc):
                return {'error': "La promocion aun no empieza"}, 403
            elif fecha_fin_promocion.replace(tzinfo=timezone.utc) < datetime.now(timezone.utc):
                return {'error': "La promocion ya caduco"}, 404
            destino_data["promocion_id"] = ObjectId(promocion_id)

        result = mongo.db.destino.insert_one((destino_data))

        object_id = str(result.inserted_id)
        
        mongo.db.logTransaccion.insert_one({
            'tipo': 'Agregar destino',
            'detalle': 'Agregar destino a la Base de Datos',
            'fecha': datetime.now(timezone.utc),
            'usuarioResponsable': 'Administrador',
            'sucursal_id': sucursal_id
        })

        response = {
            'id': object_id,
            'nombre': nombre,
            'pais': pais,
            'descripcion': descripcion,
            'precioBase': precioBase,
            'temporadaAlta': temporadaAlta,
            'cupoMaximo': cupoMaximo,
            'sucursal_id': sucursal_id
        }

        if promocion_id:
            response['promocion_id'] = promocion_id
       
        return response


@destinos_ns.route("/<string:id>")
@destinos_ns.param('id', 'ObjectId del destino')
class EditarEliminarDestino(Resource):
    def delete(self, id):
        destino = mongo.db.destino.find_one({"_id": ObjectId(id)})
        if not destino:
            return {"error": "Destino no encontrado"}, 404
        sucursal_id = destino.get("sucursal_id")

        mongo.db.paquete.delete_many({ "destino_id": ObjectId(id)})
        mongo.db.reserva.delete_many({ "destino_id": ObjectId(id)})
        mongo.db.destino.delete_one({ "_id": ObjectId(id)})

        mongo.db.logTransaccion.insert_one({
            'tipo': 'Eliminar destino',
            'detalle': 'Eliminar destino y paquetes y reservas relacionadas con ese destino de la Base de Datos',
            'fecha': datetime.now(timezone.utc),
            'usuarioResponsable': 'Administrador',
            'sucursal_id': sucursal_id
        })

        return {'message': f'Destino con id {id} eliminado exitosamente'}
    
    def get(self, id):
        db = mongo.db
        destino = db.destino.find_one({"_id": ObjectId(id)})
        if not destino:
            return {"error": "Destino no encontrado"}, 404
        response = json_util.dumps(destino)
        return Response(response, mimetype='application/json')
    
    @destinos_ns.expect(destino_model)
    def patch(self, id):
        destino = mongo.db.destino.find_one({"_id": ObjectId(id)})
        if not destino:
            return {"error": "Destino no encontrado"}, 404
        data = request.json
        if 'nombre' in data:
            mongo.db.destino.update_one({'_id': ObjectId(id)}, {'$set': {'nombre': data['nombre']}})
        if 'pais' in data:
            mongo.db.destino.update_one({'_id': ObjectId(id)}, {'$set': {'pais': data['pais']}})
        if 'descripcion' in data:
            mongo.db.destino.update_one({'_id': ObjectId(id)}, {'$set': {'descripcion': data['descripcion']}})
        if 'precioBase' in data:
            mongo.db.destino.update_one({'_id': ObjectId(id)}, {'$set': {'precioBase': data['precioBase']}})  
        if 'temporadaAlta' in data:
            mongo.db.destino.update_one({'_id': ObjectId(id)}, {'$set': {'temporadaAlta': data['temporadaAlta']}}) 
        if 'cupoMaximo' in data:
            mongo.db.destino.update_one({'_id': ObjectId(id)}, {'$set': {'cupoMaximo': data['cupoMaximo']}}) 
        if 'promocion_id' in data:
            try:
                promocion = mongo.db.promocion.find_one({"_id": data['promocion_id']})
                if not promocion:
                    return {'error': "No existe esa promocion"},402
            except Exception as e:
                return {'error': str(e)}, 400
            mongo.db.destino.update_one({'_id': ObjectId(id)}, {'$set': {'promocion_id': ObjectId(data['promocion_id'])}})
        if 'sucursal_id' in data:
            sucursal = mongo.db.sucursal.find_one({"sucursal_id": data['sucursal_id']})
            if not sucursal:
                return {'error': "No existe esa sucursal"},401
            mongo.db.destino.update_one({'_id': ObjectId(id)}, {'$set': {'sucursal_id': data['sucursal_id']}})

        mongo.db.logTransaccion.insert_one({
            'tipo': 'Editar destino',
            'detalle': 'Editar destino de la Base de Datos',
            'fecha': datetime.now(timezone.utc),
            'usuarioResponsable': 'Administrador',
            'sucursal_id': destino.get("sucursal_id")
        }) 

        return {"mensaje": f"Destino con id {id} actualizado"}, 200


@destinos_ns.route("/allDestinos")
class ListarDestinos(Resource):
    def get(self):
        destinos = mongo.db.destino.find({})
        if not destinos:
            return {"error": "Ningun destino encontrado"}, 404
        response = json_util.dumps(destinos)
        return Response(response, mimetype='application/json')
    

@destinos_ns.route("/getDestinationsBySucursalId/<int:sucursal_id>")
@destinos_ns.param('sucursal_id', 'ID de la sucursal')
class ListarDestinosPorSucursal(Resource):
    def get(self, sucursal_id):
        sucursal = mongo.db.sucursal.find_one({ "sucursal_id": sucursal_id})
        if not sucursal:
            return {"error": f"Sucursal con id {sucursal_id} no encontrada"}, 404
        destinos = mongo.db.destino.find({ "sucursal_id": sucursal_id})
        if not destinos:
            return {"error": "Ningun destino encontrado"}, 404
        response = json_util.dumps(destinos)
        return Response(response, mimetype='application/json')


#Clientes
@clientes_ns.route("/agregar")
class AgregarCliente(Resource):
    @clientes_ns.expect(cliente_model)
    def post(self):
        data = request.json

        if not all(k in data for k in ("nombre", "correo", "telefono", "direccion", "fecha_nacimiento", "sucursal_id")):
            return {"error": "Faltan campos obligatorios"}, 400

        nombre = data["nombre"]
        correo = data["correo"]
        telefono = data["telefono"]
        direccion = data["direccion"]
        fecha_nacimiento_str = data["fecha_nacimiento"]
        fecha_nacimiento = datetime.strptime(fecha_nacimiento_str, "%Y-%m-%d")
        sucursal_id = data["sucursal_id"]
        
        sucursal = mongo.db.sucursal.find_one({"sucursal_id": sucursal_id})
        if not sucursal:
            return {'error': "No existe esa sucursal"},401

        result = mongo.db.cliente.insert_one({
            'nombre': nombre,
            'correo': correo,
            'telefono': telefono,
            'direccion': direccion,
            'fecha_nacimiento': fecha_nacimiento,
            'sucursal_id': sucursal_id
        })

        object_id = str(result.inserted_id)
        
        mongo.db.logTransaccion.insert_one({
            'tipo': 'Agregar cliente',
            'detalle': 'Agregar cliente a la Base de Datos',
            'fecha': datetime.now(timezone.utc),
            'usuarioResponsable': 'Administrador',
            'sucursal_id': sucursal_id
        })

        response = {
            'id': object_id,
            'nombre': nombre,
            'correo': correo,
            'telefono': telefono,
            'direccion': direccion,
            'fecha_nacimiento': fecha_nacimiento_str,
            'sucursal_id': sucursal_id
        }
       
        return response


@clientes_ns.route("/<string:id>")
@clientes_ns.param('id', 'ObjectId del cliente')
class EditarEliminarCliente(Resource):
    def delete(self, id):
        cliente = mongo.db.cliente.find_one({"_id": ObjectId(id)})
        if not cliente:
            return {"error": "Cliente no encontrado"}, 404
        sucursal_id = cliente.get("sucursal_id")
        

        mongo.db.resenia.delete_many({"cliente_id": ObjectId(id)})
        mongo.db.reserva.delete_many({"cliente_id": ObjectId(id)})
        mongo.db.cliente.delete_one({ "_id": ObjectId(id)})

        mongo.db.logTransaccion.insert_one({
            'tipo': 'Eliminar cliente',
            'detalle': 'Eliminar cliente y resenias y reservas relacionadas con ese cliente de la Base de Datos',
            'fecha': datetime.now(timezone.utc),
            'usuarioResponsable': 'Administrador',
            'sucursal_id': sucursal_id
        })

        return {'message': f'Cliente con id {id} eliminado exitosamente'}
    
    def get(self, id):
        cliente = mongo.db.cliente.find_one({"_id": ObjectId(id)})
        if not cliente:
            return {"error": "Cliente no encontrado"}, 404
        response = json_util.dumps(cliente)
        return Response(response, mimetype='application/json')
    
    @clientes_ns.expect(cliente_model)
    def patch(self, id):
        cliente = mongo.db.cliente.find_one({"_id": ObjectId(id)})
        if not cliente:
            return {"error": "Cliente no encontrado"}, 404
        data = request.json
        if 'nombre' in data:
            mongo.db.cliente.update_one({'_id': ObjectId(id)}, {'$set': {'nombre': data['nombre']}})
        if 'correo' in data:
            mongo.db.cliente.update_one({'_id': ObjectId(id)}, {'$set': {'correo': data['correo']}})
        if 'telefono' in data:
            mongo.db.cliente.update_one({'_id': ObjectId(id)}, {'$set': {'telefono': data['telefono']}})
        if 'direccion' in data:
            mongo.db.cliente.update_one({'_id': ObjectId(id)}, {'$set': {'direccion': data['direccion']}})
        if 'fecha_nacimiento' in data:
            fecha_nacimiento_str = data["fecha_nacimiento"]
            fecha_nacimiento = datetime.strptime(fecha_nacimiento_str, "%Y-%m-%d")
            mongo.db.cliente.update_one({'_id': ObjectId(id)}, {'$set': {'fecha_nacimiento': fecha_nacimiento}})   
        if 'sucursal_id' in data:
            sucursal = mongo.db.sucursal.find_one({"sucursal_id": data['sucursal_id']})
            if not sucursal:
                return {'error': "No existe esa sucursal"},401
            mongo.db.cliente.update_one({'_id': ObjectId(id)}, {'$set': {'sucursal_id': data['sucursal_id']}}) 

        mongo.db.logTransaccion.insert_one({
            'tipo': 'Editar cliente',
            'detalle': 'Editar cliente de la Base de Datos',
            'fecha': datetime.now(timezone.utc),
            'usuarioResponsable': 'Administrador',
            'sucursal_id': cliente.get("sucursal_id")
        })

        return {"mensaje": f"Cliente con id {id} actualizado"}, 200


@clientes_ns.route("/allClientes")
class ListarClientes(Resource):
    def get(self):
        clientes = mongo.db.cliente.find({})
        if not clientes:
            return {"error": "Ningun cliente encontrado"}, 404
        response = json_util.dumps(clientes)
        return Response(response, mimetype='application/json')
    

@clientes_ns.route("/getCustomersBySucursalId/<int:sucursal_id>")
@clientes_ns.param('sucursal_id', 'ID de la sucursal')
class ListarClientesPorSucursal(Resource):
    def get(self, sucursal_id):
        sucursal = mongo.db.sucursal.find_one({ "sucursal_id": sucursal_id})
        if not sucursal:
            return {"error": f"Sucursal con id {sucursal_id} no encontrada"}, 404
        clientes = mongo.db.empleado.find({ "sucursal_id": sucursal_id})
        if not clientes:
            return {"error": "Ningun cliente encontrado"}, 404
        response = json_util.dumps(clientes)
        return Response(response, mimetype='application/json')
    

#Pagos
@pagos_ns.route("/agregar")
class AgregarPago(Resource):
    @pagos_ns.expect(pago_model)
    def post(self):
        data = request.json

        if not all(k in data for k in ("fecha_pago", "metodo_pago", "estado", "reserva_id", "sucursal_id")):
            return jsonify({"error": "Faltan campos obligatorios"}), 400

        fecha_pago_str = data["fecha_pago"]
        fecha_pago = datetime.strptime(fecha_pago_str, "%Y-%m-%d")
        metodo_pago = data["metodo_pago"]
        estado = data["estado"]
        reserva_id = data["reserva_id"]
        sucursal_id = data["sucursal_id"]
        
        sucursal = mongo.db.sucursal.find_one({"sucursal_id": sucursal_id})
        if not sucursal:
            return jsonify({'error': "No existe esa sucursal"}),401
        
        try:
            reserva = mongo.db.reserva.find_one({"_id": ObjectId(reserva_id)})
            if not reserva:
                return jsonify({'error': "No existe esa reserva"}),402
        except Exception as e:
            return {'error': str(e)}, 400
        
        monto = reserva.get('precio_total')

        result = mongo.db.pago.insert_one({
            'monto': monto,
            'fecha_pago': fecha_pago,
            'metodo_pago': metodo_pago,
            'estado': estado,
            'reserva_id': ObjectId(reserva_id),
            'sucursal_id': sucursal_id
        })

        object_id = str(result.inserted_id)
        
        mongo.db.logTransaccion.insert_one({
            'tipo': 'Agregar pago',
            'detalle': 'Agregar pago a la Base de Datos',
            'fecha': datetime.now(timezone.utc),
            'usuarioResponsable': 'Administrador',
            'sucursal_id': sucursal_id
        })

        response = {
            'id': object_id,
            'monto': monto,
            'fecha_pago': fecha_pago_str,
            'metodo_pago': metodo_pago,
            'estado': estado,
            'reserva_id': reserva_id,
            'sucursal_id': sucursal_id
        }
       
        return response


@pagos_ns.route("/<string:id>")
@pagos_ns.param('id', 'ObjectId del pago')
class EditarEliminarPago(Resource):
    def delete(self, id):
        try:
            pago = mongo.db.pago.find_one({"_id": ObjectId(id)})
            if not pago:
                return {"error": "Pago no encontrado"}, 404
        except Exception as e:
            return {'error': str(e)}, 400

        sucursal_id = pago.get("sucursal_id")
        mongo.db.pago.delete_one({ "_id": ObjectId(id)})

        mongo.db.logTransaccion.insert_one({
            'tipo': 'Eliminar pago',
            'detalle': 'Eliminar pago de la Base de Datos',
            'fecha': datetime.now(timezone.utc),
            'usuarioResponsable': 'Administrador',
            'sucursal_id': sucursal_id
        })

        return {'message': f'Pago con id {id} eliminado exitosamente'}
    
    def get(self, id):
        try:
            pago = mongo.db.pago.find_one({"_id": ObjectId(id)})
            if not pago:
                return {"error": "Pago no encontrado"}, 404
        except Exception as e:
            return {'error': str(e)}, 400
        response = json_util.dumps(pago)
        return Response(response, mimetype='application/json')
    
    @pagos_ns.expect(pago_model)
    def patch(self, id):
        try:
            pago = mongo.db.pago.find_one({"_id": ObjectId(id)})
            if not pago:
                return {"error": "Pago no encontrado"}, 404
        except Exception as e:
            return {'error': str(e)}, 400
        data = request.json
        if 'monto' in data:
            mongo.db.pago.update_one({'_id': ObjectId(id)}, {'$set': {'monto': data['monto']}})
        if 'fecha_pago' in data:
            fecha_pago_str = data["fecha_pago"]
            fecha_pago = datetime.strptime(fecha_pago_str, "%Y-%m-%d")
            mongo.db.pago.update_one({'_id': ObjectId(id)}, {'$set': {'fecha_pago': fecha_pago}})  
        if 'metodo_pago' in data:
            mongo.db.pago.update_one({'_id': ObjectId(id)}, {'$set': {'metodo_pago': data['metodo_pago']}}) 
        if 'estado' in data:
            mongo.db.pago.update_one({'_id': ObjectId(id)}, {'$set': {'estado': data['estado']}}) 
        if 'reserva_id' in data:
            try:
                reserva = mongo.db.reserva.find_one({"_id": data['reserva_id']})
                if not reserva:
                    return {'error': "No existe esa reserva"},402
            except Exception as e:
                return {'error': str(e)}, 400
            mongo.db.pago.update_one({'_id': ObjectId(id)}, {'$set': {'reserva_id': data['reserva_id']}})
        if 'sucursal_id' in data:
            sucursal = mongo.db.sucursal.find_one({"sucursal_id": data['sucursal_id']})
            if not sucursal:
                return {'error': "No existe esa sucursal"},401
            mongo.db.pago.update_one({'_id': ObjectId(id)}, {'$set': {'sucursal_id': data['sucursal_id']}}) 

        mongo.db.logTransaccion.insert_one({
            'tipo': 'Editar pago',
            'detalle': 'Editar pago de la Base de Datos',
            'fecha': datetime.now(timezone.utc),
            'usuarioResponsable': 'Administrador',
            'sucursal_id': pago.get("sucursal_id")
        })

        return {"mensaje": f"Pago con id {id} actualizado"}, 200


@pagos_ns.route("/allPagos")
class ListarPagos(Resource):
    def get(self):
        pagos = mongo.db.pago.find({})
        if not pagos:
            return {"error": "Ningun pago encontrado"}, 404
        response = json_util.dumps(pagos)
        return Response(response, mimetype='application/json')
    

@pagos_ns.route("/getPaysBySucursalId/<int:sucursal_id>")
@pagos_ns.param('sucursal_id', 'ID de la sucursal')
class ListarPagosPorSucursal(Resource):
    def get(self, sucursal_id):
        sucursal = mongo.db.reserva.find_one({ "sucursal_id": sucursal_id})
        if not sucursal:
            return {"error": f"Sucursal con id {sucursal_id} no encontrada"}, 404
        pagos = mongo.db.pago.find({ "sucursal_id": sucursal_id})
        response = json_util.dumps(pagos)
        return Response(response, mimetype='application/json')


#Reservas
@reservas_ns.route("/agregar")
class AgregarReserva(Resource):
    @reservas_ns.expect(reserva_model)
    def post(self):
        data = request.json

        if not all(k in data for k in ("fecha_regreso", "fecha_salida", "estado", "detalles", "cliente_id", "destino_id", "sucursal_id")):
            return {"error": "Faltan campos obligatorios"}, 400

        fecha_regreso_str = data["fecha_regreso"]
        fecha_regreso = datetime.strptime(fecha_regreso_str, "%Y-%m-%d")
        fecha_salida_str = data["fecha_salida"]
        fecha_salida = datetime.strptime(fecha_salida_str, "%Y-%m-%d")
        estado = data["estado"]
        detalles = data["detalles"]
        cliente_id = data["cliente_id"]
        destino_id = data["destino_id"]
        sucursal_id = data["sucursal_id"]

        if fecha_salida >= fecha_regreso:
            return {'error': "La fecha de salida no puede ser mayor o igual a la de regreso"},406
        
        sucursal = mongo.db.sucursal.find_one({"sucursal_id": sucursal_id})
        if not sucursal:
            return {'error': "No existe esa sucursal"},401
        
        try:
            cliente = mongo.db.cliente.find_one({"_id": ObjectId(cliente_id)})
            if not cliente:
                return {'error': "No existe ese cliente"},402
        except Exception as e:
            return {'error': str(e)}, 400
        
        try:
            destino = mongo.db.destino.find_one({"_id": ObjectId(destino_id)})
            if not destino:
                return {'error': "No existe ese destino"},403
        except Exception as e:
            return {'error': str(e)}, 400
        
        reserva_data = {
            'fecha_salida': fecha_salida,
            'fecha_regreso': fecha_regreso,
            'estado': estado,
            'detalles': detalles,
            'cliente_id': ObjectId(cliente_id),
            'destino_id': ObjectId(destino_id),
            'sucursal_id': sucursal_id
        }
 
        cupo_maximo_destino = destino.get("cupoMaximo")

        numero_reservas_actuales_salida = mongo.db.reserva.count_documents({"destino_id": ObjectId(destino_id), 
                                                                     "fecha_salida": fecha_salida})

        if cupo_maximo_destino == numero_reservas_actuales_salida:
            return {'error': "Cupo lleno para ese destino en esa fecha de salida"},404
        
        numero_reservas_actuales_regreso = mongo.db.reserva.count_documents({"destino_id": ObjectId(destino_id), 
                                                                     "fecha_regreso": fecha_regreso})
        
        if cupo_maximo_destino == numero_reservas_actuales_regreso:
            return {'error': "Cupo lleno para ese destino en esa fecha de regreso"},405
        
        precio_base_destino = destino.get("precioBase")
        precio_total = precio_base_destino

        codigo_descuento = data.get("codigo_descuento")
        if codigo_descuento:
            print(destino.get("_id"))
            promocion = mongo.db.promocion.find_one({"_id": destino.get("promocion_id")})
            if not promocion:
                return {'error': "Ese destino no tiene promocion"},406
            if codigo_descuento == promocion.get("codigo"):
                descuento_porciento = promocion.get("descuento")
                precio_total = precio_base_destino - ((precio_base_destino * descuento_porciento) / 100)
                reserva_data["codigo_descuento"] = codigo_descuento
            else:
                return {'error': "Codigo de descuento invalido"},407
        
        reserva_data["precio_total"] = precio_total

        result = mongo.db.reserva.insert_one(reserva_data)

        object_id = str(result.inserted_id)
        
        mongo.db.logTransaccion.insert_one({
            'tipo': 'Agregar reserva',
            'detalle': 'Agregar reserva a la Base de Datos',
            'fecha': datetime.now(timezone.utc),
            'usuarioResponsable': 'Cliente',
            'sucursal_id': sucursal_id
        })

        response = {
            'id': object_id,
            'fecha_salida': fecha_salida_str,
            'fecha_regreso': fecha_regreso_str,
            'precio_total': precio_total,
            'estado': estado,
            'detalles': detalles,
            'cliente_id': cliente_id,
            'destino_id': destino_id,
            'sucursal_id': sucursal_id
        }

        if codigo_descuento:
            response['codigo_descuento'] = codigo_descuento
       
        return response


@reservas_ns.route("/<string:id>")
@reservas_ns.param('id', 'ObjectId de la reserva')
class EditarEliminarReserva(Resource):
    def delete(self, id):
        reserva = mongo.db.reserva.find_one({"_id": ObjectId(id)})
        if not reserva:
            return {"error": "Reserva no encontrada"}, 404
        sucursal_id = reserva.get("sucursal_id")
        
        mongo.db.resenia.delete_many({"reserva_id": ObjectId(id)})
        mongo.db.pago.delete_many({"reserva_id": ObjectId(id)})
        mongo.db.reserva.delete_one({ "_id": ObjectId(id)})

        mongo.db.logTransaccion.insert_one({
            'tipo': 'Eliminar reserva',
            'detalle': 'Eliminar reserva y resenias y pagos relacionados con esa reserva de la Base de Datos',
            'fecha': datetime.now(timezone.utc),
            'usuarioResponsable': 'Cliente',
            'sucursal_id': sucursal_id
        })

        return {'message': f'Reserva con id {id} eliminada exitosamente'}
    
    def get(self, id):
        reserva = mongo.db.reserva.find_one({"_id": ObjectId(id)})
        if not reserva:
            return {"error": "Reserva no encontrada"}, 404
        response = json_util.dumps(reserva)
        return Response(response, mimetype='application/json')
    
    @reservas_ns.expect(reserva_model)
    def patch(self, id):
        reserva = mongo.db.reserva.find_one({"_id": ObjectId(id)})
        if not reserva:
            return {"error": "Reserva no encontrada"}, 404
        data = request.json
        if 'fecha_salida' in data:
            fecha_salida_str = data["fecha_salida"]
            fecha_salida = datetime.strptime(fecha_salida_str, "%Y-%m-%d")
            mongo.db.reserva.update_one({'_id': ObjectId(id)}, {'$set': {'fecha_salida': fecha_salida}}) 
        if 'fecha_regreso' in data:
            fecha_regreso_str = data["fecha_regreso"]
            fecha_regreso = datetime.strptime(fecha_regreso_str, "%Y-%m-%d")
            mongo.db.reserva.update_one({'_id': ObjectId(id)}, {'$set': {'fecha_regreso': fecha_regreso}})  
        if 'precio_total' in data:
            mongo.db.reserva.update_one({'_id': ObjectId(id)}, {'$set': {'precio_total': data['precio_total']}}) 
        if 'estado' in data:
            mongo.db.reserva.update_one({'_id': ObjectId(id)}, {'$set': {'estado': data['estado']}}) 
        if 'detalles' in data:
            mongo.db.reserva.update_one({'_id': ObjectId(id)}, {'$set': {'detalles': data['detalles']}})
        if 'cliente_id' in data:
            try:
                cliente = mongo.db.cliente.find_one({"cliente_id": data['cliente_id']})
                if not cliente:
                    return {'error': "No existe ese cliente"},401
            except Exception as e:
                return {'error': str(e)}, 400
            mongo.db.reserva.update_one({'_id': ObjectId(id)}, {'$set': {'cliente_id': data['cliente_id']}}) 
        if 'destino_id' in data:
            try:
                destino = mongo.db.destino.find_one({"destino_id": data['destino_id']})
                if not destino:
                    return {'error': "No existe ese destino"},401
            except Exception as e:
                return {'error': str(e)}, 400
            mongo.db.reserva.update_one({'_id': ObjectId(id)}, {'$set': {'destino_id': data['destino_id']}}) 
        if 'sucursal_id' in data:
            sucursal = mongo.db.sucursal.find_one({"sucursal_id": data['sucursal_id']})
            if not sucursal:
                return {'error': "No existe esa sucursal"},401
            mongo.db.reserva.update_one({'_id': ObjectId(id)}, {'$set': {'sucursal_id': data['sucursal_id']}}) 

        mongo.db.logTransaccion.insert_one({
            'tipo': 'Editar reserva',
            'detalle': 'Editar reserva de la Base de Datos',
            'fecha': datetime.now(timezone.utc),
            'usuarioResponsable': 'Cliente',
            'sucursal_id': reserva.get("sucursal_id")
        })

        return {"mensaje": f"Reserva con id {id} actualizado"}, 200


@reservas_ns.route("/allReservations")
class ListarReservas(Resource):
    def get(self):
        reservaciones = mongo.db.reserva.find({})
        if not reservaciones:
            return {"error": "Ninguna reserva encontrada"}, 404
        response = json_util.dumps(reservaciones)
        return Response(response, mimetype='application/json')
    

@reservas_ns.route("/getReservationsBySucursalId/<int:sucursal_id>")
@reservas_ns.param('sucursal_id', 'ID de la sucursal')
class ListarReservasPorSucursal(Resource):
    def get(self, sucursal_id):
        sucursal = mongo.db.sucursal.find_one({ "sucursal_id": sucursal_id})
        if not sucursal:
            return {"error": f"Sucursal con id {sucursal_id} no encontrada"}, 404
        reservas = mongo.db.reserva.find({ "sucursal_id": sucursal_id})
        if not reservas:
            return {"error": "Ninguna reserva encontrada"}, 404
        response = json_util.dumps(reservas)
        return Response(response, mimetype='application/json')


#Reseñas
@resenias_ns.route("/agregar")
class AgregarResenia(Resource):
    @resenias_ns.expect(resenia_model)
    def post(self):
        data = request.json

        if not all(k in data for k in ("fecha", "comentario", "calificacion", "reserva_id", "sucursal_id")):
            return {"error": "Faltan campos obligatorios"}, 400

        fecha_str = data["fecha"]
        fecha = datetime.strptime(fecha_str, "%Y-%m-%d")
        comentario = data["comentario"]
        calificacion = data["calificacion"]
        reserva_id = data["reserva_id"]
        sucursal_id = data["sucursal_id"]
        
        sucursal = mongo.db.sucursal.find_one({"sucursal_id": sucursal_id})
        if not sucursal:
            return {'error': "No existe esa sucursal"},401
        
        try:
            reserva = mongo.db.reserva.find_one({"_id": ObjectId(reserva_id)})
            if not reserva:
                return {'error': "No existe esa reserva"},402
        except Exception as e:
            return {'error': str(e)}, 400
        
        cliente = mongo.db.cliente.find_one({"_id": ObjectId(reserva.get("cliente_id"))})
        cliente_nombre = cliente.get("nombre")

        result = mongo.db.resenia.insert_one({
            'fecha': fecha,
            'comentario': comentario,
            'calificacion': calificacion,
            'reserva_id': ObjectId(reserva_id),
            'sucursal_id': sucursal_id
        })

        object_id = str(result.inserted_id)
        
        mongo.db.logTransaccion.insert_one({
            'tipo': 'Agregar resenia',
            'detalle': 'Agregar resenia a la Base de Datos',
            'fecha': datetime.now(timezone.utc),
            'usuarioResponsable': 'Cliente',
            'sucursal_id': sucursal_id
        })

        response = {
            'id': object_id,
            'fecha': fecha_str,
            'comentario': comentario,
            'calificacion': calificacion,
            'cliente_nombre': cliente_nombre,
            'reserva_id': reserva_id,
            'sucursal_id': sucursal_id
        }
       
        return response


@resenias_ns.route("/<string:id>")
@resenias_ns.param('id', 'ObjectId de la resenia')
class EditarEliminarResenia(Resource):
    def delete(self, id):
        try:
            resenia = mongo.db.resenia.find_one({"_id": ObjectId(id)})
            if not resenia:
                return {"error": "Resenia no encontrada"}, 404
        except Exception as e:
            return {'error': str(e)}, 400
        
        sucursal_id = resenia.get("sucursal_id")
        mongo.db.resenia.delete_one({ "_id": ObjectId(id)})

        mongo.db.logTransaccion.insert_one({
            'tipo': 'Eliminar resenia',
            'detalle': 'Eliminar resenia de la Base de Datos',
            'fecha': datetime.now(timezone.utc),
            'usuarioResponsable': 'Cliente',
            'sucursal_id': sucursal_id
        })

        return {'message': f'Resenia con id {id} eliminada exitosamente'}
    
    def get(self, id):
        try:
            resenia = mongo.db.resenia.find_one({"_id": ObjectId(id)})
            if not resenia:
                return {"error": "Resenia no encontrada"}, 404
        except Exception as e:
            return {'error': str(e)}, 400
        response = json_util.dumps(resenia)
        return Response(response, mimetype='application/json')
    
    @resenias_ns.expect(resenia_model)
    def patch(self, id):
        try:
            resenia = mongo.db.resenia.find_one({"_id": ObjectId(id)})
            if not resenia:
                return {"error": "Resenia no encontrada"}, 404
        except Exception as e:
            return {'error': str(e)}, 400
        data = request.json
        if 'fecha' in data:
            fecha_str = data["fecha"]
            fecha = datetime.strptime(fecha_str, "%Y-%m-%d")
            mongo.db.resenia.update_one({'_id': ObjectId(id)}, {'$set': {'fecha': fecha}}) 
        if 'calificacion' in data:
            mongo.db.resenia.update_one({'_id': ObjectId(id)}, {'$set': {'califiacion': data['calificacion']}}) 
        if 'comentario' in data:
            mongo.db.resenia.update_one({'_id': ObjectId(id)}, {'$set': {'comentario': data['comentario']}})
        if 'cliente_id' in data:
            try:
                cliente = mongo.db.cliente.find_one({"cliente_id": data['cliente_id']})
                if not cliente:
                    return {'error': "No existe ese cliente"},401
            except Exception as e:
                return {'error': str(e)}, 400
            mongo.db.resenia.update_one({'_id': ObjectId(id)}, {'$set': {'cliente_id': data['cliente_id']}}) 
        if 'reserva_id' in data:
            try:
                reserva = mongo.db.reserva.find_one({"reserva_id": data['reserva_id']})
                if not reserva:
                    return {'error': "No existe esa reserva"},401
            except Exception as e:
                return {'error': str(e)}, 400
            mongo.db.resenia.update_one({'_id': ObjectId(id)}, {'$set': {'reserva_id': data['reserva_id']}}) 
        if 'sucursal_id' in data:
            sucursal = mongo.db.sucursal.find_one({"sucursal_id": data['sucursal_id']})
            if not sucursal:
                return {'error': "No existe esa sucursal"},401
            mongo.db.resenia.update_one({'_id': ObjectId(id)}, {'$set': {'sucursal_id': data['sucursal_id']}}) 

        mongo.db.logTransaccion.insert_one({
            'tipo': 'Editar resenia',
            'detalle': 'Editar resenia de la Base de Datos',
            'fecha': datetime.now(timezone.utc),
            'usuarioResponsable': 'Cliente',
            'sucursal_id': resenia.get("sucursal_id")
        })

        return {"mensaje": f"Resenia con id {id} actualizada"}, 200


@resenias_ns.route("/allReviews")
class ListarResenias(Resource):
    def get(self):
        resenias = mongo.db.resenia.find({})
        if not resenias:
            return {"error": "Ninguna resenia encontrada"}, 404
        response = json_util.dumps(resenias)
        return Response(response, mimetype='application/json')
    

@resenias_ns.route("/getReviewsBySucursalId/<int:sucursal_id>")
@resenias_ns.param('sucursal_id', 'ID de la sucursal')
class ListarReseniasPorSucursal(Resource):
    def get(self, sucursal_id):
        sucursal = mongo.db.sucursal.find_one({ "sucursal_id": sucursal_id})
        if not sucursal:
            return {"error": f"Sucursal con id {sucursal_id} no encontrada"}, 404
        resenias = mongo.db.resenia.find({ "sucursal_id": sucursal_id})
        response = json_util.dumps(resenias)
        return Response(response, mimetype='application/json')
    

#Sucursales
@sucursales_ns.route("/agregar")
class AgregarSucursal(Resource):
    @sucursales_ns.expect(sucursal_model)
    def post(self):
        data = request.json

        if not all(k in data for k in ("sucursal_id", "nombre", "direccion", "telefono")):
            return jsonify({"error": "Faltan campos obligatorios"}), 400

        sucursal_id = data["sucursal_id"]
        nombre = data["nombre"]
        direccion = data["direccion"]
        telefono = data["telefono"]
        
        sucursal = mongo.db.sucursal.find_one({"sucursal_id": sucursal_id})
        if sucursal:
            return jsonify({'error': "Ya existe sucursal con ese id"}),401
        
        id = mongo.db.sucursal.insert_one({
            'sucursal_id': sucursal_id,
            'nombre': nombre,
            'direccion': direccion,
            'telefono': telefono
        })
        
        mongo.db.logTransaccion.insert_one({
            'tipo': 'Agregar sucursal',
            'detalle': 'Agregar sucursal a la Base de Datos',
            'fecha': datetime.now(timezone.utc),
            'usuarioResponsable': 'Administrador',
            'sucursal_id': sucursal_id
        })

        response = {
            'id': str(id),
            'sucursal_id': sucursal_id,
            'nombre': nombre,
            'direccion': direccion,
            'telefono': telefono
        }
       
        return response


@sucursales_ns.route("/<int:id>")
@sucursales_ns.param('id', 'ID de la sucursal')
class EditarEliminarSucursal(Resource):
    def delete(self, id):
        sucursal = mongo.db.sucursal.find_one({"sucursal_id": id})
        if not sucursal:
            return jsonify({"error": "Sucursal no encontrada"}), 404
        
        mongo.db.empleado.delete_many({ "sucursal_id": id})
        mongo.db.resenia.delete_many({ "sucursal_id": id})
        mongo.db.reserva.delete_many({ "sucursal_id": id})
        mongo.db.cliente.delete_many({ "sucursal_id": id})
        mongo.db.logTransaccion.delete_many({ "sucursal_id": id})
        mongo.db.pago.delete_many({ "sucursal_id": id})
        mongo.db.paquete.delete_many({ "sucursal_id": id})
        mongo.db.promocion.delete_many({ "sucursal_id": id})
        mongo.db.destino.delete_many({ "sucursal_id": id})

        mongo.db.sucursal.delete_one({ "sucursal_id": id})

        mongo.db.logTransaccion.insert_one({
            'tipo': 'Eliminar sucursal',
            'detalle': 'Eliminar sucursal junto con sus empleados, resenias, reservas, clientes, logs, pagos, paquetes, promociones y destinos de la Base de Datos',
            'fecha': datetime.now(timezone.utc),
            'usuarioResponsable': 'Administrador'
        })

        return jsonify({'message': f'Sucursal con id {id} eliminada exitosamente'})
    
    def get(self, id):
        sucursal = mongo.db.sucursal.find_one({"sucursal_id": id})
        if not sucursal:
            return jsonify({"error": "Sucursal no encontrada"}), 404
        response = json_util.dumps(sucursal)
        return Response(response, mimetype='application/json')
    
    @sucursales_ns.expect(sucursal_model)
    def patch(self, id):
        sucursal = mongo.db.sucursal.find_one({"sucursal_id": id})
        if not sucursal:
            return jsonify({"error": "Sucursal no encontrada"}), 404
        data = request.json 
         
        nuevo_sucursal_id = data.get("sucursal_id")
        if nuevo_sucursal_id and nuevo_sucursal_id != id:
            sucursal_existente = mongo.db.sucursal.find_one({"sucursal_id": nuevo_sucursal_id})
            if sucursal_existente:
                return jsonify({"error": "El nuevo sucursal_id ya está en uso"}), 400
            
            colecciones = [
                "empleado", "resenia", "reserva", "cliente", 
                "logTransaccion", "pago", "paquete", "promocion", "destino"
            ]
            for coleccion in colecciones:
                mongo.db[coleccion].update_many(
                    {"sucursal_id": id},
                    {"$set": {"sucursal_id": nuevo_sucursal_id}}
                )

            mongo.db.sucursal.update_one({"sucursal_id": id}, {"$set": {'sucursal_id': nuevo_sucursal_id}})

        if 'nombre' in data:
            mongo.db.sucursal.update_one({'sucursal_id': id}, {'$set': {'nombre': data['nombre']}})
        if 'direccion' in data:
            mongo.db.sucursal.update_one({'sucursal_id': id}, {'$set': {'direccion': data['direccion']}})
        if 'telefono' in data:
            mongo.db.sucursal.update_one({'sucursal_id': id}, {'$set': {'telefono': data['telefono']}})  
        
        mongo.db.logTransaccion.insert_one({
            'tipo': 'Editar sucursal',
            'detalle': 'Editar sucursal de la Base de Datos',
            'fecha': datetime.now(timezone.utc),
            'usuarioResponsable': 'Aministrador',
            'sucursal_id': nuevo_sucursal_id if nuevo_sucursal_id else id
        })

        return jsonify({"mensaje": f"Sucursal con id {id} actualizada"}), 200


@sucursales_ns.route("/allBranches")
class ListarSucursales(Resource):
    def get(self):
        sucursales = mongo.db.sucursal.find({})
        if not sucursales:
            return jsonify({"error": "Ninguna sucursal encontrada"}), 404
        response = json_util.dumps(sucursales)
        return Response(response, mimetype='application/json')
    
    
#Promociones
@promociones_ns.route("/agregar")
class AgregarPromocion(Resource):
    @promociones_ns.expect(promocion_model)
    def post(self):
        data = request.json

        if not all(k in data for k in ("fecha_inicio", "fecha_fin", "descripcion", "codigo", "descuento", "sucursal_id")):
            return {"error": "Faltan campos obligatorios"}, 400

        fecha_inicio_str = data["fecha_inicio"]
        fecha_inicio = datetime.strptime(fecha_inicio_str, "%Y-%m-%d")
        fecha_fin_str = data["fecha_fin"]
        fecha_fin = datetime.strptime(fecha_fin_str, "%Y-%m-%d")
        descripcion = data["descripcion"]
        codigo = data["codigo"]
        descuento = data["descuento"]
        sucursal_id = data["sucursal_id"]
        
        sucursal = mongo.db.sucursal.find_one({"sucursal_id": sucursal_id})
        if not sucursal:
            return {'error': "No existe esa sucursal"},401

        result = mongo.db.promocion.insert_one({
            'descripcion': descripcion,
            'codigo': codigo,
            'descuento': descuento,
            'fecha_inicio': fecha_inicio,
            'fecha_fin': fecha_fin,
            'sucursal_id': sucursal_id
        })

        object_id = str(result.inserted_id)
        
        mongo.db.logTransaccion.insert_one({
            'tipo': 'Agregar promocion',
            'detalle': 'Agregar promocion a la Base de Datos',
            'fecha': datetime.now(timezone.utc),
            'usuarioResponsable': 'Administrador',
            'sucursal_id': sucursal_id
        })

        response = {
            'id': object_id,
            'descripcion': descripcion,
            'codigo': codigo,
            'descuento': descuento,
            'fecha_inicio': fecha_inicio_str,
            'fecha_fin': fecha_fin_str,
            'sucursal_id': sucursal_id
        }
       
        return response


@promociones_ns.route("/<string:id>")
@promociones_ns.param('id', 'ObjectId de la promocion')
class EditarEliminarPromocion(Resource):
    def delete(self, id):
        promocion = mongo.db.promocion.find_one({"_id": ObjectId(id)})
        if not promocion:
            return {"error": "Promocion no encontrada"}, 404
        sucursal_id = promocion.get("sucursal_id")

        mongo.db.destino.delete_many({ "promocion_id": ObjectId(id)})
        mongo.db.promocion.delete_one({ "_id": ObjectId(id)})

        mongo.db.logTransaccion.insert_one({
            'tipo': 'Eliminar promocion',
            'detalle': 'Eliminar promocion de la Base de Datos',
            'fecha': datetime.now(timezone.utc),
            'usuarioResponsable': 'Administrador',
            'sucursal_id': sucursal_id
        })

        return {'message': f'Promocion con id {id} eliminada exitosamente'}
    
    def get(self, id):
        promocion = mongo.db.promocion.find_one({"_id": ObjectId(id)})
        if not promocion:
            return {"error": "Promocion no encontrada"}, 404
        response = json_util.dumps(promocion)
        return Response(response, mimetype='application/json')
    
    @promociones_ns.expect(promocion_model)
    def patch(self, id):
        promocion = mongo.db.promocion.find_one({"_id": ObjectId(id)})
        if not promocion:
            return {"error": "Promocion no encontrada"}, 404
        data = request.json
        if 'fecha_inicio' in data:
            fecha_inicio_str = data["fecha_inicio"]
            fecha_inicio = datetime.strptime(fecha_inicio_str, "%Y-%m-%d")
            mongo.db.promocion.update_one({'_id': ObjectId(id)}, {'$set': {'fecha_inicio': fecha_inicio}}) 
        if 'fecha_fin' in data:
            fecha_fin_str = data["fecha_fin"]
            fecha_fin = datetime.strptime(fecha_fin_str, "%Y-%m-%d")
            mongo.db.promocion.update_one({'_id': ObjectId(id)}, {'$set': {'fecha_fin': fecha_fin}}) 
        if 'descripcion' in data:
            mongo.db.promocion.update_one({'_id': ObjectId(id)}, {'$set': {'descripcion': data['descripcion']}}) 
        if 'codigo' in data:
            mongo.db.promocion.update_one({'_id': ObjectId(id)}, {'$set': {'codigo': data['codigo']}})
        if 'descuento' in data:
            mongo.db.promocion.update_one({'_id': ObjectId(id)}, {'$set': {'descuento': data['descuento']}})
        if 'sucursal_id' in data:
            sucursal = mongo.db.sucursal.find_one({"sucursal_id": data['sucursal_id']})
            if not sucursal:
                return {'error': "No existe esa sucursal"},401
            mongo.db.promocion.update_one({'_id': ObjectId(id)}, {'$set': {'sucursal_id': data['sucursal_id']}}) 

        mongo.db.logTransaccion.insert_one({
            'tipo': 'Editar promocion',
            'detalle': 'Editar promocion de la Base de Datos',
            'fecha': datetime.now(timezone.utc),
            'usuarioResponsable': 'Administrador',
            'sucursal_id': promocion.get("sucursal_id")
        })

        return {"mensaje": f"Promocion con id {id} actualizada"}, 200


@promociones_ns.route("/allPromotions")
class ListarPromociones(Resource):
    def get(self):
        promociones = mongo.db.promocion.find({})
        if not promociones:
            return {"error": "Ninguna promocion encontrada"}, 404
        response = json_util.dumps(promociones)
        return Response(response, mimetype='application/json')
    

@promociones_ns.route("/getPromotionsBySucursalId/<int:sucursal_id>")
@promociones_ns.param('sucursal_id', 'ID de la sucursal')
class ListarPromocionesPorSucursal(Resource):
    def get(self, sucursal_id):
        sucursal = mongo.db.sucursal.find_one({ "sucursal_id": sucursal_id})
        if not sucursal:
            return {"error": f"Sucursal con id {sucursal_id} no encontrada"}, 404
        promociones = mongo.db.promocion.find({ "sucursal_id": sucursal_id})
        if not promociones:
            return {"error": "Ninguna promocion encontrada"}, 404
        response = json_util.dumps(promociones)
        return Response(response, mimetype='application/json')


#Paquetes
@paquetes_ns.route("/agregar")
class AgregarPaquete(Resource):
    @paquetes_ns.expect(paquete_model)
    def post(self):
        data = request.json

        if not all(k in data for k in ("nombre", "duracion", "precio", "servicios", "destinos", "sucursal_id")):
            return {"error": "Faltan campos obligatorios"}, 400

        nombre = data["nombre"]
        duracion = data["duracion"]
        precio = data["precio"]
        servicios = data["servicios"]
        destinos = data["destinos"]
        sucursal_id = data["sucursal_id"]
        
        sucursal = mongo.db.sucursal.find_one({"sucursal_id": sucursal_id})
        if not sucursal:
            return {'error': "No existe esa sucursal"},401
        
        destinos_objectids = []
        for destino_id in destinos:
            try:
                destino = mongo.db.destino.find_one({"_id": ObjectId(destino_id)})
                if not destino:
                    return {'error': f"No existe ese destino con id {destino_id}"},402
            except Exception as e:
                return {'error': str(e)}, 400
            destinos_objectids.append(ObjectId(destino_id))

        result = mongo.db.paquete.insert_one({
            'nombre': nombre,
            'duracion': duracion,
            'precio': precio,
            'servicios': servicios,
            'destinos': destinos_objectids,
            'sucursal_id': sucursal_id
        })

        object_id = str(result.inserted_id)
        
        mongo.db.logTransaccion.insert_one({
            'tipo': 'Agregar paquete',
            'detalle': 'Agregar paquete a la Base de Datos',
            'fecha': datetime.now(timezone.utc),
            'usuarioResponsable': 'Administrador',
            'sucursal_id': sucursal_id
        })

        response = {
            'id': object_id,
            'nombre': nombre,
            'duracion': duracion,
            'precio': precio,
            'servicios': servicios,
            'destinos': [str(destino_id) for destino_id in destinos_objectids],
            'sucursal_id': sucursal_id
        }
       
        return response


@paquetes_ns.route("/<string:id>")
@paquetes_ns.param('id', 'ObjectId del paquete')
class EditarEliminarPaquete(Resource):
    def delete(self, id):
        try:
            paquete = mongo.db.paquete.find_one({"_id": ObjectId(id)})
            if not paquete:
                return {"error": "Paquete no encontrado"}, 404
        except Exception as e:
            return {'error': str(e)}, 400
        
        sucursal_id = paquete.get("sucursal_id")
        mongo.db.paquete.delete_one({ "_id": ObjectId(id)})

        mongo.db.logTransaccion.insert_one({
            'tipo': 'Eliminar paquete',
            'detalle': 'Eliminar paquete de la Base de Datos',
            'fecha': datetime.now(timezone.utc),
            'usuarioResponsable': 'Administrador',
            'sucursal_id': sucursal_id
        })

        return {'message': f'Paquete con id {id} eliminado exitosamente'}
    
    def get(self, id):
        try:
            paquete = mongo.db.paquete.find_one({"_id": ObjectId(id)})
            if not paquete:
                return {"error": "Paquete no encontrado"}, 404
        except Exception as e:
            return {'error': str(e)}, 400
        response = json_util.dumps(paquete)
        return Response(response, mimetype='application/json')
    
    @paquetes_ns.expect(paquete_model)
    def patch(self, id):
        paquete = mongo.db.paquete.find_one({"_id": ObjectId(id)})
        if not paquete:
            return {"error": "Paquete no encontrado"}, 404
        data = request.json
        if 'nombre' in data:
            mongo.db.paquete.update_one({'_id': ObjectId(id)}, {'$set': {'nombre': data['nombre']}}) 
        if 'precio' in data:
            mongo.db.paquete.update_one({'_id': ObjectId(id)}, {'$set': {'precio': data['precio']}})
        if 'servicios' in data:
            mongo.db.paquete.update_one({'_id': ObjectId(id)}, {'$set': {'servicios': data['servicios']}})
        if 'destinos' in data:
            destinos = data["destinos"]
            destinos_objectids = []
            for destino_id in destinos:
                try:
                    destino = mongo.db.destino.find_one({"_id": ObjectId(destino_id)})
                    if not destino:
                        return {'error': f"No existe ese destino con id {destino_id}"},402
                except Exception as e:
                    return {'error': str(e)}, 400
                destinos_objectids.append(ObjectId(destino_id))
            mongo.db.paquete.update_one({'_id': ObjectId(id)}, {'$set': {'destinos': destinos_objectids}})
        if 'sucursal_id' in data:
            sucursal = mongo.db.sucursal.find_one({"sucursal_id": data['sucursal_id']})
            if not sucursal:
                return {'error': "No existe esa sucursal"},401
            mongo.db.paquete.update_one({'_id': ObjectId(id)}, {'$set': {'sucursal_id': data['sucursal_id']}}) 

        mongo.db.logTransaccion.insert_one({
            'tipo': 'Editar paquete',
            'detalle': 'Editar paquete de la Base de Datos',
            'fecha': datetime.now(timezone.utc),
            'usuarioResponsable': 'Administrador',
            'sucursal_id': paquete.get("sucursal_id")
        })

        return {"mensaje": f"Paquete con id {id} actualizado"}, 200


@paquetes_ns.route("/allPackages")
class ListarPaquetes(Resource):
    def get(self):
        paquetes = mongo.db.paquete.find({})
        if not paquetes:
            return {"error": "Ningun paquete encontrada"}, 404
        response = json_util.dumps(paquetes)
        return Response(response, mimetype='application/json')
    

@paquetes_ns.route("/getPacketsBySucursalId/<int:sucursal_id>")
@paquetes_ns.param('sucursal_id', 'ID de la sucursal')
class ListarPaquetesPorSucursal(Resource):
    def get(self, sucursal_id):
        sucursal = mongo.db.sucursal.find_one({ "sucursal_id": sucursal_id})
        if not sucursal:
            return {"error": f"Sucursal con id {sucursal_id} no encontrada"}, 404
        paquetes = mongo.db.paquete.find({ "sucursal_id": sucursal_id})
        response = json_util.dumps(paquetes)
        return Response(response, mimetype='application/json')


#logs
@logs_ns.route("/<string:id>")
@logs_ns.param('id', 'ObjectId del logTransaccion')
class EditarEliminarLog(Resource):
    def delete(self, id):
        try:
            log = mongo.db.logTransaccion.find_one({"_id": ObjectId(id)})
            if not log:
                return {"error": "Log no encontrado"}, 404
        except Exception as e:
            return {'error': str(e)}, 400
        
        sucursal_id = log.get("sucursal_id")
        mongo.db.logTransaccion.delete_one({ "_id": ObjectId(id)})

        mongo.db.logTransaccion.insert_one({
            'tipo': 'Eliminar log',
            'detalle': 'Eliminar log de la Base de Datos',
            'fecha': datetime.now(timezone.utc),
            'usuarioResponsable': 'Administrador',
            'sucursal_id': sucursal_id
        })

        return {'message': f'Log con id {id} eliminado exitosamente'}
    
    def get(self, id):
        try:
            log = mongo.db.logTransaccion.find_one({"_id": ObjectId(id)})
            if not log:
                return {"error": "Log no encontrado"}, 404
        except Exception as e:
            return {'error': str(e)}, 400
        response = json_util.dumps(log)
        return Response(response, mimetype='application/json')


@logs_ns.route("/allLogs")
class ListarLogs(Resource):
    def get(self):
        logs = mongo.db.logTransaccion.find({})
        if not logs:
            return {"error": "Ningun log encontrado"}, 404
        response = json_util.dumps(logs)
        return Response(response, mimetype='application/json')
    

@logs_ns.route("/getLogsBySucursalId/<int:sucursal_id>")
@logs_ns.param('sucursal_id', 'ID de la sucursal')
class ListarLogsPorSucursal(Resource):
    def get(self, sucursal_id):
        sucursal = mongo.db.sucursal.find_one({ "sucursal_id": sucursal_id})
        if not sucursal:
            return {"error": f"Sucursal con id {sucursal_id} no encontrada"}, 404
        logs = mongo.db.logTransaccion.find({ "sucursal_id": sucursal_id})
        response = json_util.dumps(logs)
        return Response(response, mimetype='application/json')


if __name__ == "__main__":
    app.run(debug=True, host='192.168.1.10')
  