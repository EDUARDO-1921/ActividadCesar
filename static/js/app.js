function agregarGenero() {
    Swal.fire({
        title: 'Desea Agregar Genero?',
        icon: 'success',
        showCancelButton: true,
        confirmButtonColor: '#3085d6',
        cancelButtonColor: '#d33',
        confirmButtonText: 'Aceptar',
        cancelButtonText: 'Cancelar'
    }).then((result) => {
        if (result.isConfirmed) {
            const genero = { nombre: document.getElementById("txtGenero").value }
            const url = "/generos"
            fetch(url, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(genero)
            })
                .then(respuesta => {
                    Swal.fire(
                        '¡Agregado!',
                        'El género ha sido agregado.',
                        'success'
                   ).then(() => {
                        location.href = "/generosVista"
                    })
                })              
                .catch(error => {
                    console.log(error)
                    alert("Error al agregar el género")
                })
        
        }
} )
}

function agregarPelicula() {
    swal.fire({
        title: 'Desea Agregar Pelicula?',
        icon: 'success',
        showCancelButton: true,
        confirmButtonColor: '#3085d6',
        cancelButtonColor: '#d33',
        confirmButtonText: 'Aceptar',
        cancelButtonText: 'Cancelar'
    }).then((result) => {
        if (result.isConfirmed) {
            const url = "/addPelicula"
            const protagonistasInput = document.getElementById("txtProtagonistas").value;
            const protagonistasArray = protagonistasInput.split(",").map(pro => pro.trim());
            const pelicula = {
                codigo: document.getElementById("txtCodigo").value,
                titulo: document.getElementById("txtTitulo").value,
                duracion: document.getElementById("txtDuracion").value,
                protagonistas: protagonistasArray,
                resumen: document.getElementById("txtResumen").value,
                genero: document.getElementById("cbGenero").value
            }
            fetch(url, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(pelicula)
            })
                .then(respuesta => {
                    Swal.fire(
                        '¡Agregado!',
                        'La película ha sido agregada.',
                        'success'
                    ).then(() => {
                        location.href = "/listarPeliculas"
                    } )
                } )
                .catch(error => {
                    Swal.fire('Error', 'Error de conexión.', 'error');
                });
        }
    });
}

function login() {
    const token = grecaptcha.getResponse();
    const usuario = document.getElementById("txtUser").value.trim()
    const passwordIn = document.getElementById("txtPassword").value.trim()
    // Validar que los campos no estén vacíos
    if (!usuario || !passwordIn) {
        swal.fire("Error", "Por favor, completa todos los campos", "error");
        return;
    }

    const url = "/usuarios/login"
    const loginData = {
        userId: usuario,
        password: passwordIn,
        "g-recaptcha-response": token
    }
    console.log("datos enviados", loginData);

    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(loginData)
    })
        .then(respuesta => respuesta.json())
        .then(resultado => {
            console.log("esta es la data; ", resultado.message)
            if (resultado.message == "Inicio de sesión exitoso") {
                swal.fire("Iniciando Sesion", resultado.message, "success")
                setTimeout(function () {
                    location.href = "/dash"
                }, 2000)
            } else {
                if (resultado.message == "Contraseña incorrecta") {
                    swal.fire("Error", resultado.message, "error")
                    alert("Contraseña incorrecta")
                } else if (resultado.message == "Usuario no encontrado") {
                    swal.fire("Error", resultado.message, "error")
                    alert("Usuario no encontrado")
                }
                swal.fire("Error", resultado.message, "error")
                // alert("Error al iniciar sesión", resultado.message)
            }
        })
        .catch(error => {
            console.log("el error es: ", error)
            alert("Error al iniciar sesión del catch")
        })
}

function salir() {
    const url = "/usuarios/logout"
    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        }
    })
        .then(respuesta => respuesta.json())
        .then(resultado => {
            console.log("esta es la data; ", resultado)
            if (resultado.message == "Sesión cerrada") {
                location.href = "/loginVista"
                alert("Sesion cerrada")
            } else {
                swal.fire("Error", resultado.message, "error")
                alert("Error al cerrar la sesion")
            }
        })
        .catch(error => {
            console.log(error)
            alert("Error al cerrar la sesion")
        })
}

function editarPelicula(id) {
    const url = "/peliculas/" + id
    const protagonistasInput = document.getElementById("txtProtagonistas").value;
    const protagonistasArray = protagonistasInput.split(",").map(pro => pro.trim());
    const pelicula = {
        codigo: document.getElementById("txtCodigo").value,
        titulo: document.getElementById("txtTitulo").value,
        duracion: document.getElementById("txtDuracion").value,
        protagonistas: protagonistasArray,
        resumen: document.getElementById("txtResumen").value,
        genero: document.getElementById("cbGenero").value
    }
    console.log("datos enviados", pelicula);
    fetch(url, {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(pelicula)
    })
        .then(respuesta => respuesta.json())

        .then(resultado => {
            console.log("esta es la data; ", resultado)
            if (resultado.message == "Pelicula actualizada") {
                location.href = "/listarPeliculas"
            } else {
                swal.fire("Error", resultado.message, "error")
                alert("Error al editar la pelicula")
            }
        })
        .catch(error => {
            console.log(error)
            alert("Error al editar la pelicula del catch")
        })
}

function actualizarGenero(codigo) {
    const url = "/generos/" + codigo
    const genero = {
        nombre: document.getElementById("txtGenero").value
    }
    fetch(url, {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(genero)
    })
        .then(respuesta => respuesta.json())
        .then(data => {
            if (data.message == "Genero actualizado") {
                location.href = "/generosVista"
            } else {
                swal.fire("Error", data.message, "error")
                alert("Error al actualizar el genero")
            }
        })
        .catch(error => {
            console.log(error)
            alert("Error al actualizar el genero")
        })
}