function eliminarPelicula(codigo) {
    Swal.fire({
        title: '¿Estás seguro?',
        icon: 'warning',
        showCancelButton: true,
        confirmButtonColor: '#d33', // rojo
        cancelButtonColor: '#6c757d', // gris bootstrap
        confirmButtonText: 'Sí, eliminar',
        cancelButtonText: 'Cancelar'
    }).then((result) => {
        if (result.isConfirmed) {
            const url = "/peliculas/" + codigo
            fetch(url, {
                method: 'DELETE',
                headers: {
                    'Content-Type': 'application/json'
                }
            })
            .then(respuesta =>{
                Swal.fire(
                    '¡Eliminado!',
                    'La película ha sido eliminada.',
                    'success'
                ).then(() => {
                    location.href = "/listarPeliculas"
                })
            } )
            .catch(error => {
                Swal.fire('Error', 'Error de conexión.', 'error');
                console.log(error)
            });
        }
    });
}

function eliminarGenero(codigo) {
    Swal.fire({
        title: '¿Estás seguro?',
        icon: 'warning',
        showCancelButton: true,
        confirmButtonColor: '#d33', // rojo
        cancelButtonColor: '#6c757d', // gris bootstrap
        confirmButtonText: 'Sí, eliminar',
        cancelButtonText: 'Cancelar'
    }).then((result) => {
        if (result.isConfirmed) {
            const url = "/generos/" + codigo
            fetch(url, {
                method: 'DELETE',
                headers: {
                    'Content-Type': 'application/json'
                }
            })
            .then(respuesta =>{
                Swal.fire(
                    '¡Eliminado!',
                    'El género ha sido eliminado.',
                    'success'
                ).then(() => {
                    location.href = "/generosVista"
                })
            } )
            .catch(error => {
                Swal.fire('Error', 'Error de conexión.', 'error');
                console.log(error)
            });
        }
    });
}