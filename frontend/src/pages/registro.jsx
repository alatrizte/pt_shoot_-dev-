import { Login } from "../components/registro/login"
import { Signin } from "../components/registro/signin"
import { useState } from "react"

export function Registro() {
    const [isActive, setIsActive] = useState(true)
    const toggleActive = () => {
        setIsActive(!isActive)
    }
    return(
        <>
            <Login visibilidad={ isActive } toggle={toggleActive}></Login>
            <Signin visibilidad={ !isActive } toggle={toggleActive}></Signin>
        </>
    )
}