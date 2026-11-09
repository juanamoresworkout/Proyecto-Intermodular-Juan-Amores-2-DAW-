<script setup>
import { ref } from 'vue'
import { getHello } from '@/services/helloService'
import HelloResult from '@/components/HelloResult.vue'

// Estado reactivo: Vue actualiza la interfaz cuando cambia uno de estos valores.
const name = ref('')
const message = ref('')
const error = ref('')
const loading = ref(false)

async function saludar() {
  // Prepara la interfaz para una nueva petición.
  loading.value = true
  message.value = ''
  error.value = ''

  try {
    // Llama al servicio y guarda el mensaje devuelto por Laravel.
    message.value = await getHello(name.value)
  } catch (exception) {
    // Ofrece un mensaje comprensible si la petición falla.
    error.value =
      'No se ha podido contactar con el backend. Inténtalo de nuevo.'

    console.error(exception)
  } finally {
    // Se ejecuta tanto si la petición funciona como si falla.
    loading.value = false
  }
}
</script>

<template>
  <!-- Esta vista controla el formulario y delega el resultado al componente. -->
  <section class="hello">
    <div class="hello__heading">
      <p class="hello__eyebrow">Barbería</p>
      <h1>Hello World</h1>
      <p class="hello__description">
        Escribe tu nombre y te saludaré.
      </p>
    </div>

    <!-- .prevent evita que el navegador recargue la página al enviar. -->
    <form class="hello__form" @submit.prevent="saludar">
      <label for="name">Tu nombre (opcional)</label>

      <input
        id="name"
        v-model="name"
        type="text"
        placeholder="Por ejemplo, Ana"
        autocomplete="name"
      />

      <button type="submit" :disabled="loading">
        {{ loading ? 'Cargando…' : 'Saludar' }}
      </button>
    </form>

    <!-- Envía el estado actual al componente de presentación. -->
    <HelloResult
      :message="message"
      :error="error"
    />
  </section>
</template>

<style scoped>
/* Centra el contenido y aplica la anchura máxima definida en los tokens. */
.hello {
  width: min(100%, var(--content-max-width));
  margin: 0 auto;
}

.hello__heading {
  margin-bottom: var(--space-xl);
}

.hello__eyebrow {
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

.hello__description {
  margin: var(--space-m) 0 0;
  color: var(--color-secondary-text);
}

.hello__form {
  /* Distribuye verticalmente la etiqueta, el campo y el botón. */
  display: flex;
  flex-direction: column;
  gap: var(--space-m);

  max-width: 420px;
  padding: var(--space-l);

  background: var(--color-glass);
  border: 1px solid var(--color-glass-border);
  border-radius: var(--radius-m);
  box-shadow: var(--glass-shadow);

  /* Recrea el material Liquid Glass de la guía elegida. */
  backdrop-filter:
    blur(var(--glass-blur))
    saturate(var(--glass-saturation));
}

label {
  font-weight: 600;
}

input {
  min-height: var(--control-min-height);
  padding: var(--space-s) var(--space-m);

  color: var(--color-on-surface);
  background: rgb(255 255 255 / 55%);
  border: 1px solid var(--color-glass-border);
  border-radius: var(--radius-pill);
}

input::placeholder {
  color: var(--color-secondary-text);
}

button {
  min-height: var(--control-min-height);
  padding: var(--space-s) var(--space-l);

  color: var(--color-on-primary);
  font-weight: 600;

  background: var(--color-primary);
  border: 1px solid var(--color-glass-border);
  border-radius: var(--radius-pill);
  box-shadow: var(--glass-shadow);

  cursor: pointer;
  transition:
    filter 160ms ease,
    transform 160ms ease;
}

button:hover:not(:disabled) {
  filter: brightness(1.12);
  transform: translateY(-1px);
}

button:disabled {
  /* Informa visualmente de que la petición está en curso. */
  opacity: 0.6;
  cursor: wait;
}

@supports not (backdrop-filter: blur(1px)) {
  .hello__form {
    background: rgb(255 255 255 / 92%);
  }
}

@media (max-width: 600px) {
  h1 {
    font-size: 2.25rem;
  }

  .hello__form {
    padding: var(--space-m);
  }
}
</style>
