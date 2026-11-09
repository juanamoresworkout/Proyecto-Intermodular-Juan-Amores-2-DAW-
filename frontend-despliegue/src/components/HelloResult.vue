<script setup>
// Datos que este componente recibe desde HelloView.
defineProps({
  message: {
    type: String,
    default: '',
  },
  error: {
    type: String,
    default: '',
  },
})
</script>

<template>
  <!-- Los errores tienen prioridad y se anuncian inmediatamente. -->
  <p
    v-if="error"
    class="result result--error"
    role="alert"
  >
    <span aria-hidden="true">⚠</span>
    {{ error }}
  </p>

  <!-- Si no hay error, muestra y anuncia el saludo recibido. -->
  <p
    v-else-if="message"
    class="result"
    aria-live="polite"
  >
    {{ message }}
  </p>
</template>

<style scoped>
/* scoped limita estas reglas a este componente. */
.result {
  margin-top: var(--space-l);
  padding: var(--space-l);

  color: var(--color-on-surface);
  font-size: var(--font-size-title);
  font-weight: 700;
  text-align: center;

  background: var(--color-glass);
  border: 1px solid var(--color-glass-border);
  border-radius: var(--radius-m);
  box-shadow: var(--glass-shadow);

  backdrop-filter:
    blur(var(--glass-blur))
    saturate(var(--glass-saturation));
}

.result--error {
  color: var(--color-error);
  font-size: var(--font-size-body);
  font-weight: 600;
}

/* Alternativa más opaca cuando el navegador no admite el desenfoque. */
@supports not (backdrop-filter: blur(1px)) {
  .result {
    background: rgb(255 255 255 / 90%);
  }
}

@media (max-width: 600px) {
  /* Reduce el tamaño del saludo en pantallas pequeñas. */
  .result {
    font-size: 2.25rem;
  }

  .result--error {
    font-size: var(--font-size-body);
  }
}
</style>
