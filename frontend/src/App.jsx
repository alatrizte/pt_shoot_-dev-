import { useState } from 'react'
import { Registro } from "./pages/registro";

function App() {
  const [count, setCount] = useState(0)

  return (
    <>
      <Registro />
    </>
  )
}

export default App
