<template>
  <!-- Vista inicial con una explicación y acceso a la actividad principal. -->
  <section class="home">
    <div class="home__card">
      <p class="home__eyebrow">Frontend Vue + Laravel</p>

      <h1>Bienvenido</h1>

      <p>
        Esta aplicación consume el endpoint
        <code>/api/hello</code>
        de nuestro backend Laravel.
      </p>

      <!-- RouterLink navega sin recargar por completo la aplicación. -->
      <RouterLink to="/hello" class="home__link">
        Ir al saludo
      </RouterLink>
    </div>
  </section>
</template>

<style scoped>
/* Contenedor centrado y limitado por el token de anchura máxima. */
.home {
  width: min(100%, var(--content-max-width));
  margin: 0 auto;
}

.home__card {
  /* Tarjeta translúcida inspirada en Liquid Glass. */
  padding: var(--space-xl);

  background: var(--color-glass);
  border: 1px solid var(--color-glass-border);
  border-radius: var(--radius-m);
  box-shadow: var(--glass-shadow);

  backdrop-filter:
    blur(var(--glass-blur))
    saturate(var(--glass-saturation));
}

.home__eyebrow {
  margin: 0 0 var(--space-s);
  color: var(--color-barber-red);
  font-size: 0.875rem;
  font-weight: 700;
  letter-spacing: 0.12em;
  text-transform: uppercase;
}

h1 {
  margin: 0;
  font-size: var(--font-size-title);
  line-height: 1.1;
}

p {
  color: var(--color-secondary-text);
  line-height: 1.6;
}

code {
  color: var(--color-primary);
  font-weight: 600;
}

.home__link {
  display: inline-flex;
  align-items: center;
  justify-content: center;

  min-height: var(--control-min-height);
  margin-top: var(--space-m);
  padding: var(--space-s) var(--space-l);

  color: var(--color-on-primary);
  font-weight: 600;
  text-decoration: none;

  background: var(--color-primary);
  border: 1px solid var(--color-glass-border);
  border-radius: var(--radius-pill);
  box-shadow: var(--glass-shadow);

  transition:
    filter 160ms ease,
    transform 160ms ease;
}

.home__link:hover {
  filter: brightness(1.12);
  transform: translateY(-1px);
}

@supports not (backdrop-filter: blur(1px)) {
  .home__card {
    background: rgb(255 255 255 / 92%);
  }
}

@media (max-width: 600px) {
  .home__card {
    padding: var(--space-l);
  }

  h1 {
    font-size: 2.25rem;
  }
}
</style>
