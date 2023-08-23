import { useState } from "react"

export function Signin ({ visibilidad, toggle }) {
   
    const [alert, setAlert] = useState('')
    const [nameAlert, setNameAlert] = useState('')
    const [mailAlert, setMailAlert] = useState('')
    const [passAlert, setPassAlert] = useState('')
    const [passConfirmAlert, setPassConfirmAlert] = useState('')

    const submit_form = () => {
        const reg_form = document.getElementById("reg_form")
        const df = new FormData(reg_form)

        fetch('http://localhost:5000/signup', {
            method: 'POST',
            body: df
        })
        .then (respuesta => respuesta.json())
        .then (data => {
            if (data['success']==true) {
                reg_form.reset();
            } else {
                setAlert(data['message']);
            }
        })
    }

    const handleSubmit = (e) => {  
        e.preventDefault()
        // Bandera de estado, si todo está correcto se envia a la base de datos.
        let flag_ok = true
        const user_name = document.getElementById("reg_user_name")
        const user_mail = document.getElementById("reg_user_mail")
        const password = document.getElementById("reg_password")
        const pass_confirm = document.getElementById("reg_pass_confirm")

        // Valida el campo de nombre de usuario.
        if (user_name.value == '') {
            setNameAlert("Este campo es obligatorio.")
            flag_ok = false
        } else {
            setNameAlert('')
        }

        // el password ha de tener minimo: 
        // 8 caracters, un dígito y una letra mayúscula
        const regExPass = /^(?=.*[A-Z])(?=.*\d).{8,}$/;
        if (password.value == '') {
            setPassAlert("Este campo es obligatorio.")
            flag_ok = false
        } else if (regExPass.test(password.value) == false) {
            setPassAlert("La contraseña debe tener una mayúscula, un número y 8 caracteres.")
            flag_ok = false
        } else {
            setPassAlert('')
        }

        // Valida el campo de e-mail
        const regExMail = /^\w+([.-_+]?\w+)*@\w+([.-]?\w+)*(\.\w{2,10})+$/;
        if (user_mail.value == '') {
            setMailAlert("Este campo es obligatorio.")
            flag_ok = false
        } else if (regExMail.test(user_mail.value) == false) {
            setMailAlert ("El e-mail ha de tener un formato válido.")
            flag_ok = false
        } else {
            setMailAlert('')
        }

        // Valida el campo de confirmación de password
        if (pass_confirm.value == '') {
            setPassConfirmAlert("Este campo es obligatorio.")
            flag_ok = false
        } else if (password.value !== pass_confirm.value) {
            setPassConfirmAlert ("La confirmación del password no es coincidente.")
            flag_ok = false
        }
         else {
            setPassConfirmAlert('')
        }

        if (flag_ok){
            submit_form()
        }
    }

    const handleClick = () => {
        toggle()
    }

    return (
        <div style={{ display: visibilidad ? 'block' : 'none' }}>
            <h3>Registro de usuario</h3>
            <div>Introduce tus datos para registrarte</div>
            <form action="" onSubmit={ handleSubmit } id="reg_form">
                <div>nombre de usuario<br/><input type="text" name="user_name" id="reg_user_name"/></div>
                <p className="alert">{ nameAlert }</p>
                <div>mail de usuario<br/><input type="text" name="user_mail"id="reg_user_mail"/></div>
                <p className="alert">{ mailAlert }</p>
                <div>contraseña<br/><input type="password" name="password" id="reg_password"/></div>
                <p className="alert">{ passAlert }</p>
                <div>repite la contraseña<br/><input type="password" name="pass_confirm" id="reg_pass_confirm"/></div>
                <p className="alert">{ passConfirmAlert }</p>
                <button type="submit">Sign In</button>
            </form>
            <p className="enlace" onClick={ handleClick }>Si ya estás registrado accede con tu contraseña.</p>
            <p className="alert">{ alert }</p>
        </div>
    )
}