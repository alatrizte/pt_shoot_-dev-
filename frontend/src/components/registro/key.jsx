import { useState } from "react"

export function Key ({visibilidad}) {

    const [alert, setAlert] = useState ('')

    // Envio de los datos de registro al servidor y esperamos respuesta.
    const handleSubmit = (e) => {
        e.preventDefault()
        
    }

    const handleClick = () => {
        toggle()
    }

    return (
        <div style={{ display: visibilidad ? 'block' : 'none' }}>
            <h3>Clave de registro de usuario</h3>
            <div>Introduce tu clave para confirmar tu registro.</div>
            <form id="key_form" onSubmit={handleSubmit}>
                <div>clave de registro<br/><input type="text" name="key" id="key"/></div>
                <button type="submit">Enviar</button>
            </form>
            <p className="alert">{ alert }</p>
        </div>
    )
}