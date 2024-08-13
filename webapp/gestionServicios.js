let indFlag = 0;
async function loadServicios() {
    try {
        const response = await fetch('http://127.0.0.1:5000/getServicios');
        const servicios = await response.json();

        const tableBody = document.getElementById('serviciosTableBody');
        tableBody.innerHTML = '';

        servicios.forEach(servicio => {
            const row = `<tr>
                <td>${servicio.identificacion}</td>
                <td>${servicio.servicio}</td>
                <td>${servicio.fechaInicio}</td>
                <td>${servicio.ultimaFacturacion}</td>
                <td>${servicio.ultimoPago}</td>
                <td>
                    <button title="Editar" class="btn btn-warning btn-sm" onclick="editServicio('${servicio.identificacion}', '${servicio.servicio}')"><i class="fas fa-pencil"></i></button>
                    <button title="Eliminar" class="btn btn-danger btn-sm ml-2" onclick="deleteServicio('${servicio.identificacion}', '${servicio.servicio}')"><i class="fas fa-trash"></i></button>
                </td>
            </tr>`;
            tableBody.innerHTML += row;
        });
    } catch (error) {
        console.error('Error al cargar los servicios:', error);
    }
}

async function editServicio(identificacion, servicio) {
    
    try {
        let decodedServicio = decodeURIComponent(servicio);
        const response = await fetch(`http://127.0.0.1:5000/getServicio/${identificacion}/'${decodedServicio}'`);
        const servicioData = await response.json();

        const dateInicio = new Date(servicioData[0].fechaInicio);
        const ultimaFacturacion = new Date(servicioData[0].ultimaFacturacion);
        
        const fechaInicio = `${dateInicio.getFullYear()}-${String(dateInicio.getMonth() + 1).padStart(2, '0')}-${String(dateInicio.getDate()).padStart(2, '0')}`;
        const ultimaFacturacionFecha = `${ultimaFacturacion.getFullYear()}-${String(ultimaFacturacion.getMonth() + 1).padStart(2, '0')}-${String(ultimaFacturacion.getDate()).padStart(2, '0')}`;
        
        document.getElementById('updateIdentificacion').value = servicioData[0].identificacion;
        document.getElementById('updateServicio').value = servicioData[0].servicio;
        document.getElementById('updateFechaInicio').value = fechaInicio;
        document.getElementById('updateUltimaFacturacion').value = ultimaFacturacionFecha;
        document.getElementById('updateUltimoPago').value = servicioData[0].ultimoPago;

        document.getElementById('identificacion').style.display = 'none'; // Ocultar el campo 'identificacion' para edición
        document.getElementById('formTitle').textContent = 'Actualizar Servicio';
        document.getElementById('submitButton').textContent = 'Actualizar';
        document.getElementById('updateFormContainer').classList.remove('hidden');
        indFlag = 1;
    } catch (error) {
        console.error('Error al cargar el servicio para editar:', error);
    }
}

function showCreateForm() {
    document.getElementById('identificacion').style.display = 'block'; // Mostrar el campo 'identificacion' para creación
    document.getElementById('formTitle').textContent = 'Crear Servicio';
    document.getElementById('submitButton').textContent = 'Guardar';
    document.getElementById('updateFormContainer').classList.remove('hidden');
    indFlag = 1;
}

async function deleteServicio(identificacion, servicio) {
    const confirmDelete = confirm(`¿Estás seguro de que deseas eliminar el servicio ${servicio}?`);
    if (confirmDelete) {
        try {
            const response = await fetch('http://127.0.0.1:5000/deleteServicio', {
                method: 'DELETE',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ identificacion, servicio })
            });

            if (response.ok) {
                alert('Servicio eliminado con éxito');
                loadServicios();
            } else {
                alert('Error al eliminar el servicio');
            }
        } catch (error) {
            console.error('Error al eliminar el servicio:', error);
        }
    }
}

document.getElementById('cancelButton').addEventListener('click', function() {
    document.getElementById('updateForm').reset();
    document.getElementById('updateFormContainer').classList.add('hidden');
    showCreateForm();
});

document.getElementById('updateForm').addEventListener('submit', async function(event) {
    event.preventDefault();

    const formData = new FormData(this);
    const servicio = {
        identificacion: formData.get('identificacion'),
        servicio: formData.get('servicio'),
        fechaInicio: formData.get('fechaInicio'),
        ultimaFacturacion: formData.get('ultimaFacturacion'),
        ultimoPago: formData.get('ultimoPago')
    };

    try {
        const url = indFlag == 0 ? 'http://127.0.0.1:5000/insertServicio': 'http://127.0.0.1:5000/updateServicio' ;
        const method = indFlag == 0 ? 'POST':'PUT' ;

        const response = await fetch(url, {
            method: method,
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(servicio)
        });

        if (response.ok) {
            alert(indFlag == 0 ? 'Servicio creado con éxito': 'Servicio actualizado con éxito');
            loadServicios();
            document.getElementById('updateFormContainer').classList.add('hidden');
            document.getElementById('formTitle').textContent = 'Crear Servicio';
            document.getElementById('submitButton').textContent = 'Guardar';
        } else {
            alert('Error al guardar el servicio');
        }
    } catch (error) {
        console.error('Error al guardar el servicio:', error);
    }
});

document.addEventListener('DOMContentLoaded', loadServicios);
document.addEventListener('DOMContentLoaded', showCreateForm);
