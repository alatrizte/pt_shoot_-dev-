
import { useState, useEffect } from "react";
import { Registro } from "./pages/registro";
import { AdminPanel } from "./pages/admin_panel";

function App() {
  const token = sessionStorage.getItem('token')
  
  const [isTokened, setIsTokened] = useState(token)

  const [proyectos, setProyectos] = useState([])
 
  let user_id = sessionStorage.getItem('user_id')
  if (user_id !== null) {
    useEffect(() => {
      fetch(`http://localhost:5000/list-project/${user_id}`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        }
      })
        .then(respuesta => respuesta.json())
        .then(data => {
          if (data['message'] == "No autorizado"){
            setIsTokened(false)
          } else {
            //console.log(data);
            setProyectos(data)
          }
        })
        .catch(e => console.error(e))
    }, [])
  }

  return (
    <>
      { isTokened ? <AdminPanel auth={setIsTokened} proyectos={proyectos}/> : <Registro auth={setIsTokened}/>}
    </>
  )
}

export default App
