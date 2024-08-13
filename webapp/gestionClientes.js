let indFlag = 0;
async function loadClientes() {
    try {
        const response = await fetch('http://127.0.0.1:5000/getClientes');
        const clientes = await response.json();

        const tableBody = document.getElementById('clientesTableBody');
        tableBody.innerHTML = '';
        

        clientes.forEach(cliente => {

            let date = new Date(cliente.fechaNacimiento);
            let year = date.getUTCFullYear();
            let month = String(date.getUTCMonth() + 1).padStart(2, '0');
            let day = String(date.getUTCDate()).padStart(2, '0');
            let fecha = `${year}-${month}-${day}`;

            const row = `<tr>
                <td>${cliente.identificacion}</td>
                <td>${cliente.nombres}</td>
                <td>${cliente.apellidos}</td>
                <td>${cliente.tipoIdentificacion}</td>
                <td>${fecha}</td>
                <td>${cliente.numeroCelular}</td>
                <td>${cliente.correoElectronico}</td>
                <td>
                    <button title="Editar" class="btn btn-warning btn-sm" onclick="editCliente('${cliente.identificacion}')"><i class="fas fa-pencil"></i></button>
                    <button title="Eliminar" class="btn btn-danger btn-sm ml-2" onclick="deleteCliente('${cliente.identificacion}', '${cliente.nombres}')"><i class="fas fa-trash"></i></button>
                </td>
            </tr>`;
            tableBody.innerHTML += row;
        });
    } catch (error) {
        console.error('Error al cargar los clientes:', error);
    }
}

async function editCliente(identificacion) {
    try {
        const response = await fetch(`http://127.0.0.1:5000/getCliente/${identificacion}`);
        const cliente = await response.json();

        const date = new Date(cliente[0].fechaNacimiento);
        const year = date.getUTCFullYear();
        const month = String(date.getUTCMonth() + 1).padStart(2, '0');
        const day = String(date.getUTCDate()).padStart(2, '0');
        let fecha = `${year}-${month}-${day}`;

        document.getElementById('updateId').value = cliente[0].identificacion;
        document.getElementById('updateNombres').value = cliente[0].nombres;
        document.getElementById('updateApellidos').value = cliente[0].apellidos;
        document.getElementById('updateTipoIdentificacion').value = cliente[0].tipoIdentificacion;
        document.getElementById('updateFechaNacimiento').value = fecha;
        document.getElementById('updateNumeroCelular').value = cliente[0].numeroCelular;
        document.getElementById('updateCorreoElectronico').value = cliente[0].correoElectronico;

        // Mostrar el campo 'identificacion' solo cuando se está editando un cliente
        document.getElementById('identificacion').style.display = 'none';
        document.getElementById('formTitle').textContent = 'Actualizar Cliente';
        document.getElementById('submitButton').textContent = 'Actualizar';
        document.getElementById('updateFormContainer').classList.remove('hidden');
        indFlag = 1;
    } catch (error) {
        console.error('Error al cargar el cliente para editar:', error);
    }
}

function showCreateForm() {
    document.getElementById('identificacion').style.display = 'block';
    document.getElementById('formTitle').textContent = 'Crear Cliente';
    document.getElementById('submitButton').textContent = 'Guardar';
    document.getElementById('updateFormContainer').classList.remove('hidden');
    indFlag = 0;
}

async function deleteCliente(identificacion, nombre) {
    const confirmDelete = confirm(`¿Estás seguro de que deseas eliminar al cliente ${nombre}?`);
    if (confirmDelete) {
        try {
            const response = await fetch('http://127.0.0.1:5000/deleteCliente', {
                method: 'DELETE',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ identificacion })
            });
            
            if (response.ok) {
                alert('Cliente eliminado con éxito');
                loadClientes();
            } else {
                alert('Error al eliminar el cliente');
            }
        } catch (error) {
            console.error('Error al eliminar el cliente:', error);
        }
    }
}

document.getElementById('cancelButton').addEventListener('click', function() {
    // Limpia los campos del formulario
    document.getElementById('updateForm').reset();
    
    // Oculta el formulario de actualización
    document.getElementById('updateFormContainer').classList.add('hidden');
    
    // Muestra el formulario para crear un nuevo cliente
    showCreateForm();
});

document.getElementById('updateForm').addEventListener('submit', async function(event) {
    event.preventDefault();

    const formData = new FormData(this);
    const cliente = {
        identificacion: formData.get('identificacion'),
        nombres: formData.get('nombres'),
        apellidos: formData.get('apellidos'),
        tipoIdentificacion: formData.get('tipoIdentificacion'),
        fechaNacimiento: formData.get('fechaNacimiento'),
        numeroCelular: formData.get('numeroCelular'),
        correoElectronico: formData.get('correoElectronico')
    };

    try {
        console.log('cliente.identificacion => ', cliente.identificacion)
        const url = indFlag == 0 ? 'http://127.0.0.1:5000/insertCliente' : 'http://127.0.0.1:5000/updateCliente';
        const method = indFlag == 0 ?'POST' :  'PUT' ;

        const response = await fetch(url, {
            method: method,
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(cliente)
        });
        console.log("response => ",response.code)
        if (response.ok) {
            alert(indFlag == 0 ? 'Cliente creado con éxito' : 'Cliente actualizado con éxito' );
            loadClientes();
            document.getElementById('updateFormContainer').classList.add('hidden');
            document.getElementById('formTitle').textContent = 'Crear Cliente';
            document.getElementById('submitButton').textContent = 'Guardar';
        } else {
            alert('Error al guardar el cliente');
        }
    } catch (error) {
        console.error('Error al guardar el cliente:', error);
    }
});

document.addEventListener('DOMContentLoaded', loadClientes);
document.addEventListener('DOMContentLoaded', showCreateForm);