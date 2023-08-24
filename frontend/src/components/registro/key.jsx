import { useState } from "react"

export function Key ({visibilidad, handleSubmitKey}) {

    const [alert, setAlert] = useState ('')


    return (
        <div style={{ display: visibilidad ? 'block' : 'none' }}>
            <h3>Clave de registro de usuario</h3>
            <div>Introduce tu clave para confirmar tu registro.</div>
            <form id="key_form" onSubmit={ handleSubmitKey }>
                <div>clave de registro<br/><input type="text" name="key" id="key"/></div>
                <button type="submit">Enviar</button>
            </form>
            <p className="alert">{ alert }</p>
        </div>
    )
}