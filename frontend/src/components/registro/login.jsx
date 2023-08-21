import { useState } from "react"

export function Login ({ visibilidad, toggle }) {

    const handleClick = () => {
        toggle()
    }

    return (
        <div style={{ display: visibilidad ? 'block' : 'none' }}>
            <h3>Acceso de usuario</h3>
            <div>Introduce tus datos para acceder</div>
            <div>mail de usuario<br/><input type="text" name="user_mail"/></div>
            <div>contraseña<br/><input type="password" name="pass"/></div>
            <button>Log In</button>
            <p className="enlace" onClick={ handleClick }>Regístrate aquí si aún no tienes cuenta.</p>
        </div>
    )
}