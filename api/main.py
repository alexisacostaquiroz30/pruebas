from flask import Flask, request, jsonify
from controllers.controllerClientes import get_clientes,get_cliente, insert_cliente, update_cliente, delete_cliente
from controllers.controllerServicios import get_servicios,get_servicio, insert_servicio, update_servicio, delete_servicio
from flask_cors import CORS

app = Flask(__name__)
# Configura CORS para permitir solicitudes de cualquier origen
CORS(app)

# Endpoints para clientes
@app.route('/getClientes', methods=['GET'])
def get_clientes_route():
    clientes = get_clientes()
    return jsonify(clientes)

@app.route('/getCliente/<identificacion>', methods=['GET'])
def get_cliente_route(identificacion):
    cliente = get_cliente(identificacion)
    return jsonify(cliente)


@app.route('/insertCliente', methods=['POST'])
def insert_cliente_route():
    data = request.json
    
    required_fields = ['identificacion', 'nombres', 'apellidos', 'tipoIdentificacion', 'fechaNacimiento', 'numeroCelular', 'correoElectronico']
    
    if not all(field in data for field in required_fields):
        return jsonify({'code': 400, 'msg': 'Faltan campos requeridos'}), 400

    try:
        response = insert_cliente(
            data['identificacion'],
            data['nombres'],
            data['apellidos'],
            data['tipoIdentificacion'],
            data['fechaNacimiento'],
            data['numeroCelular'],
            data['correoElectronico']
        )
        return jsonify(response), 200 if response['code'] == 200 else 500
    except Exception as e:
        return jsonify({'code': 500, 'msg': str(e)}), 500

@app.route('/updateCliente', methods=['PUT'])
def update_cliente_route():
    data = request.json
    
    required_fields = ['identificacion', 'nombres', 'apellidos', 'tipoIdentificacion', 'fechaNacimiento', 'numeroCelular', 'correoElectronico']
    
    if not all(field in data for field in required_fields):
        return jsonify({'code': 400, 'msg': 'Faltan campos requeridos'}), 400

    try:
        response = update_cliente(
            data['identificacion'],
            data['nombres'],
            data['apellidos'],
            data['tipoIdentificacion'],
            data['fechaNacimiento'],
            data['numeroCelular'],
            data['correoElectronico']
        )
        return jsonify(response), 200 if response['code'] == 200 else 500
    except Exception as e:
        return jsonify({'code': 500, 'msg': str(e)}), 500

@app.route('/deleteCliente', methods=['DELETE'])
def delete_cliente_route():
    data = request.json
    identificacion = data.get('identificacion')
    
    if not identificacion:
        return jsonify({'code': 400, 'msg': 'Falta el campo "identificacion"'}), 400

    try:
        response = delete_cliente(identificacion)
        return jsonify(response), 200 if response['code'] == 200 else 500
    except Exception as e:
        return jsonify({'code': 500, 'msg': str(e)}), 500

# Endpoints para servicios
@app.route('/getServicios', methods=['GET'])
def get_servicios_route():
    servicios = get_servicios()
    return jsonify(servicios)


@app.route('/getServicio/<identificacion>/<servicio>', methods=['GET'])
def get_servicio_route(identificacion,servicio):
    servicio = get_servicio(identificacion,servicio)
    return jsonify(servicio)


@app.route('/insertServicio', methods=['POST'])
def insert_servicio_route():
    data = request.json
    
    required_fields = ['identificacion', 'servicio', 'fechaInicio', 'ultimaFacturacion', 'ultimoPago']
    
    if not all(field in data for field in required_fields):
        return jsonify({'code': 400, 'msg': 'Faltan campos requeridos'}), 400

    try:
        response = insert_servicio(
            data['identificacion'],
            data['servicio'],
            data['fechaInicio'],
            data['ultimaFacturacion'],
            data['ultimoPago']
        )
        return jsonify(response), 200 if response['code'] == 200 else 500
    except Exception as e:
        return jsonify({'code': 500, 'msg': str(e)}), 500

@app.route('/updateServicio', methods=['PUT'])
def update_servicio_route():
    data = request.json
    
    required_fields = ['identificacion', 'servicio', 'fechaInicio', 'ultimaFacturacion', 'ultimoPago']
    
    if not all(field in data for field in required_fields):
        return jsonify({'code': 400, 'msg': 'Faltan campos requeridos'}), 400

    try:
        response = update_servicio(
            data['identificacion'],
            data['servicio'],
            data['fechaInicio'],
            data['ultimaFacturacion'],
            data['ultimoPago']
        )
        return jsonify(response), 200 if response['code'] == 200 else 500
    except Exception as e:
        return jsonify({'code': 500, 'msg': str(e)}), 500

@app.route('/deleteServicio', methods=['DELETE'])
def delete_servicio_route():
    data = request.json
    identificacion = data.get('identificacion')
    servicio = data.get('servicio')
    
    if not identificacion or not servicio:
        return jsonify({'code': 400, 'msg': 'Faltan campos requeridos'}), 400

    try:
        response = delete_servicio(identificacion, servicio)
        return jsonify(response), 200 if response['code'] == 200 else 500
    except Exception as e:
        return jsonify({'code': 500, 'msg': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
