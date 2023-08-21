import { useState, useEffect } from "react"
import { sha3_256 } from 'js-sha3'

export function Login ({ visibilidad, toggle }) {

    const [alert, setAlert] = useState ('')

    const handleSubmit = (e) => {
        e.preventDefault()
        let password = document.getElementById("password");
        const hashedPassword = sha3_256(password.value);

        let email = document.getElementById("email");

        if (password.value == "" || email.value == "") {
            setAlert ("Todos los campos son obligatorios")
        } else {
            const df = new FormData();
            df.append('password', hashedPassword)
            df.append('email', email.value)
            fetch('http://localhost:5000/login', {
                method: 'POST',
                body: df
            })
            .then(respuesta => respuesta.json())
            .then(data => {
                if (data['success'] == false) {
                    password.value = '';
                    setAlert(data['message'])
                } else {
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
    )
}