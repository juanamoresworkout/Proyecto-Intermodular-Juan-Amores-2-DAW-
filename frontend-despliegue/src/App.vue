<script setup>
// Componentes de Vue Router para crear enlaces y mostrar la vista activa.
import { RouterLink, RouterView } from 'vue-router'
</script>

<template>
  <!-- Estructura común que se mantiene al cambiar de ruta. -->
  <div class="app-shell">
    <header class="app-header">
      <nav aria-label="Navegación principal">
        <RouterLink to="/">
          Inicio
        </RouterLink>

        <RouterLink to="/hello">
          Hello
        </RouterLink>
      </nav>

      <!-- Decoración visual; se oculta a los lectores de pantalla. -->
      <div class="barber-stripe" aria-hidden="true"></div>
    </header>

    <main class="app-main">
      <!-- Aquí se muestra HomeView o HelloView según la URL. -->
      <RouterView />
    </main>
  </div>
</template>

<style scoped>
/* El contenedor ocupa como mínimo toda la altura de la ventana. */
.app-shell {
  min-height: 100vh;
}

.app-header {
  /* Mantiene la navegación visible mientras se desplaza la página. */
  position: sticky;
  z-index: 10;
  top: 0;

  width: min(
    calc(100% - (var(--space-l) * 2)),
    var(--content-max-width)
  );

  margin: var(--space-m) auto 0;
  padding: var(--space-s);

  background: var(--color-glass);
  border: 1px solid var(--color-glass-border);
  border-radius: var(--radius-pill);
  box-shadow: var(--glass-shadow);

  /* Desenfoque y saturación del efecto Liquid Glass. */
  backdrop-filter:
    blur(var(--glass-blur))
    saturate(var(--glass-saturation));
}

nav {
  display: flex;
  gap: var(--space-s);
}

nav a {
  display: inline-flex;
  align-items: center;
  justify-content: center;

  min-height: var(--control-min-height);
  padding: var(--space-s) var(--space-l);

  color: var(--color-on-surface);
  font-weight: 600;
  text-decoration: none;

  border-radius: var(--radius-pill);

  transition:
    color 160ms ease,
    background-color 160ms ease;
}

nav a:hover {
  background: rgb(255 255 255 / 45%);
}

nav a.router-link-exact-active {
  /* Vue Router aplica esta clase al enlace de la ruta actual. */
  color: var(--color-on-primary);
  background: var(--color-primary);
}

.barber-stripe {
  height: 4px;
  margin: var(--space-s) var(--space-m) 0;

  background: var(--barber-reflection);
  border-radius: var(--radius-pill);
}

.app-main {
  padding: var(--space-xl) var(--space-l);
}

@supports not (backdrop-filter: blur(1px)) {
  .app-header {
    background: rgb(255 255 255 / 92%);
  }
}

@media (max-width: 600px) {
  .app-header {
    width: calc(100% - (var(--space-m) * 2));
  }

  nav a {
    flex: 1;
    padding-inline: var(--space-m);
  }

  .app-main {
    padding: var(--space-l) var(--space-m);
  }
}
</style>
