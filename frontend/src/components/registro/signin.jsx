import { useState } from "react"

export function Signin ({ visibilidad, toggle }) {
   
    const handleClick = () => {
        toggle()
    }

    return (
        <div style={{ display: visibilidad ? 'block' : 'none' }}>
            <h3>Registro de usuario</h3>
            <div>Introduce tus datos para registrarte</div>
            <div>nombre de usuario<br/><input type="text" name="user_name"/></div>
            <div>mail de usuario<br/><input type="text" name="user_mail"/></div>
            <div>contraseña<br/><input type="password" name="pass"/></div>
            <div>repite la contraseña<br/><input type="password" name="pass_confirm"/></div>
            <button>Sign In</button>
            <p className="enlace" onClick={ handleClick }>Si ya estás registrado accede con tu contraseña.</p>
        </div>
    )
}