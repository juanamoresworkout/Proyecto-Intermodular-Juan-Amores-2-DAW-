// Carga los estilos globales antes de montar la aplicación.
import './assets/base.css'

import { createApp } from 'vue'
import App from './App.vue'
import router from './router'

// App.vue es el componente raíz de toda la aplicación.
const app = createApp(App)

// Registra Vue Router para poder navegar entre las vistas.
app.use(router)

// Monta Vue dentro del elemento <div id="app"> de index.html.
app.mount('#app')
