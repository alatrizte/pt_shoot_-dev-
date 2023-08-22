import { useState } from "react"

export function Signin ({ visibilidad, toggle }) {
   
    const [alert, setAlert] = useState('')
    const [mailAlert, setMailAlert] = useState('')
    const [passAlert, setPassAlert] = useState('')
    const [passConfirmAlert, setPassConfirmAlert] = useState('')

    const handleSubmit = (e) => {
        console.log("envio de datos");
        e.preventDefault()
        const user_name = document.getElementById("user_name")
        const user_mail = document.getElementById("user_mail")
        const password = document.getElementById("password")
        const pass_confirm = document.getElementById("pass_confirm")

        const regExPass = /^(?=.*[A-Z])(?=.*\d).+/g
        const regExMail = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}/g
        console.log(regExPass.test(password));
        if (regExPass.test(password) == false) {
            setPassAlert("La contraseña ha de contener una mayúscula y un número.")
        } else if (regExMail.test(user_mail) == false) {
            setMailAlert ("El e-mail ha de tener un formato válido.")
        } else if (password !== pass_confirm) {
            setPassConfirmAlert ("La confirmación del password no es coincidente.")
        } else {
            const df = new FormData()
            df.append('user_name', user_name);
            df.append('user_mail', user_mail);
            df.append('password', password);
            df.append('pass_confirm', pass_confirm)

            fetch('http://localhost:5000/signup', {
                method: 'POST',
                body: df
            })
            .then (respuesta => respuesta.json())
            .then (data => {
                console.log(data);
            })
        }
    }

    const handleClick = () => {
        toggle()
    }

    return (
        <div style={{ display: visibilidad ? 'block' : 'none' }}>
            <h3>Registro de usuario</h3>
            <div>Introduce tus datos para registrarte</div>
            <form action="" onSubmit={ handleSubmit }>
                <div>nombre de usuario<br/><input type="text" name="user_name" id="user_name"/></div>
                <div>mail de usuario<br/><input type="text" name="user_mail"id="user_mail"/></div>
                <p className="alert">{ mailAlert }</p>
                <div>contraseña<br/><input type="password" name="pass" id="password"/></div>
                <p className="alert">{ passAlert }</p>
                <div>repite la contraseña<br/><input type="password" name="pass_confirm" id="pass_confirm"/></div>
                <p className="alert">{ passConfirmAlert }</p>
                <button type="submit">Sign In</button>
            </form>
            <p className="enlace" onClick={ handleClick }>Si ya estás registrado accede con tu contraseña.</p>
            <p className="alert">{ alert }</p>
        </div>
    )
}