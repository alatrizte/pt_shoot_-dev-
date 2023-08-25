import { useEffect, useState } from "react"

export function AdminPanel({ auth, proyectos }) {
    const user_id = sessionStorage.getItem('user_id')
    const token = sessionStorage.getItem('token')

    console.log(proyectos)
   
    return(
        <>
            <h1>Panel administrativo {user_id}</h1>
            { proyectos[0][3] }
        </>
    )
}