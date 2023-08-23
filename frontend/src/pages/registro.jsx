import { Login } from "../components/registro/login"
import { Signin } from "../components/registro/signin"
import { Key } from "../components/registro/key"
import { useState } from "react"
import './registro.css'

export function Registro() {
    const [isActive, setIsActive] = useState(true)
    const toggleActive = () => {
        setIsActive(!isActive)
    }
    return(
        <>
            <Login visibilidad={ isActive } toggle={toggleActive}></Login>
            <Signin visibilidad={ !isActive } toggle={toggleActive}></Signin>
            <Key visibilidad={ !isActive } toggle={toggleActive}></Key>
        </>
    )
}