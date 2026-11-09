import { fileURLToPath, URL } from 'node:url'

import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import vueDevTools from 'vite-plugin-vue-devtools'

// https://vite.dev/config/
export default defineConfig({
  // Activa el soporte de componentes .vue y las herramientas de desarrollo.
  plugins: [
    vue(),
    vueDevTools(),
  ],
  resolve: {
    // Permite escribir @/views/... en lugar de rutas relativas largas.
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url)),
    },
  },
  server: {
    // Expone Vite fuera del contenedor de desarrollo.
    host: true,
    // CORS del backend está preparado para este puerto concreto.
    port: 5173,
    // Si 5173 está ocupado, muestra un error en vez de cambiar de puerto.
    strictPort: true,
  },
}) 
