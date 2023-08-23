import { useState } from "react"
import { sha3_256 } from 'js-sha3'
import { Key } from "./key"

export function Login ({ visibilidad, toggle }) {

    const [alert, setAlert] = useState ('')
    const [keyConfirm, setKeyConfirm] = useState(false)

    // Envio de los datos de registro al servidor y esperamos respuesta.
    const handleSubmit = (e) => {
        e.preventDefault()

        // Hasea la contraseña con el algoritmo 'sha3-256'.
        let password = document.getElementById("password");
        const hashedPassword = sha3_256(password.value);

        let email = document.getElementById("email");

        // Comprueba que los campos no estén vacios.
        if (password.value == "" || email.value == "") {
            setAlert ("Todos los campos son obligatorios")
        } else {
            // Envia los datos del formulario.
            const df = new FormData();
            df.append('password', hashedPassword)
            df.append('email', email.value)
            fetch('http://localhost:5000/login', {
                method: 'POST',
                body: df
            })
            .then(respuesta => respuesta.json())
            .then(data => {
                // En caso de error
                if (data['success'] == false) {
                    if (data['message'] == "Sin clave de confirmación"){
                        setKeyConfirm(true)
                    } else {
                        password.value = ''; // borra el campo de password para evitar el mismo envío.
                        setAlert(data['message']) // Imprime el mesaje de respuesta del servidor.
                    }
                } else {
                    // Caso de respuesta de éxito.
                    // Almacena en la sesion la clave de token. 
                    sessionStorage.setItem('token', data['token'])
                    console.log(data);
                    password.value = '';
                    email.value = '';
                    setAlert('')
                }
            })
        }
    }

    const handleClick = () => {
        toggle()
    }

    return (
        <>
        <div style={{ display: visibilidad ? 'block' : 'none' }}>
            <h3>Acceso de usuario</h3>
            <div>Introduce tus datos para acceder</div>
            <form id="login_form" onSubmit={handleSubmit}>
                <div>e-mail del usuario<br/><input type="text" name="email" id="email"/></div>
                <div>contraseña<br/><input type="password" name="password" id="password"/></div>
                <button type="submit">Log In</button>
            </form>
            <p className="enlace" onClick={ handleClick }>Regístrate aquí si aún no tienes cuenta.</p>
            <p className="alert">{ alert }</p>
        </div>
        <Key visibilidad={ keyConfirm }></Key>
        </>
    )
}