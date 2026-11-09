import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '@/views/HomeView.vue'

// Relaciona cada URL del frontend con la vista que debe mostrarse.
const router = createRouter({
  // Usa URLs normales, como /hello, sin el símbolo #.
  history: createWebHistory(import.meta.env.BASE_URL),

  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView,
    },
    {
      path: '/hello',
      name: 'hello',
      // Carga HelloView solo cuando se visita esta ruta (lazy loading).
      component: () => import('@/views/HelloView.vue'),
    },
  ],
})

export default router
