// Vite obtiene esta dirección de .env.development.
const API_URL = import.meta.env.VITE_API_URL

/**
 * Llama a GET /api/hello y devuelve el mensaje.
 * @param {string} name Nombre opcional
 * @returns {Promise<string>} "Hello World" o "Hello World <nombre>"
 */
export async function getHello(name = '') {
  // Construimos la URL a partir de la dirección base de la API.
  const url = new URL(`${API_URL}/hello`)
  // Evita enviar un nombre compuesto solamente por espacios.
  const cleanName = name.trim()

  if (cleanName !== '') {
    // searchParams codifica de forma segura espacios, tildes y otros caracteres.
    url.searchParams.set('name', cleanName)
  }

  // await pausa esta función hasta que el backend responda.
  const response = await fetch(url, {
    headers: {
      Accept: 'application/json',
    },
  })

  if (!response.ok) {
    // Convierte respuestas 4xx o 5xx en errores que gestionará la vista.
    throw new Error(`Error ${response.status} al llamar a la API`)
  }

  // Convierte el JSON recibido en un objeto JavaScript.
  const data = await response.json()

  // La vista solo necesita el valor de la propiedad message.
  return data.message
}
