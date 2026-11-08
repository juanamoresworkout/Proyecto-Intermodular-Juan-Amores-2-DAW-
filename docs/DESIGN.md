# DESIGN.md - Guia de estilo de mi frontend

> Estado: concepto 1 aprobado para seguir trabajando.
>
> Este documento sigue Apple Human Interface Guidelines como referencia
> principal. La tematica de barberia y sus valores CSS son decisiones propias
> del proyecto. En una pagina web, Liquid Glass se recrea con CSS; no es el
> material nativo de los sistemas operativos de Apple.

## Guia elegida

- Nombre: Apple Human Interface Guidelines (HIG), con lenguaje visual Liquid Glass.
- Enlace oficial: https://developer.apple.com/design/human-interface-guidelines/
- Materiales: https://developer.apple.com/design/human-interface-guidelines/materials
- Por que la he elegido: porque permite separar los controles del contenido
  mediante profundidad, transparencia y desenfoque. Me interesa su aspecto
  limpio y quiero adaptarlo a una barberia clasica sin perder legibilidad.
- Adaptacion propia: reflejos casi imperceptibles en azul, blanco y rojo,
  inspirados en las franjas de un poste de barberia.

## Colores (design tokens)

| Token | Valor | Uso |
|---|---|---|
| `color-primary` | `#123B5D` | Boton principal, enlaces activos y detalles destacados |
| `color-on-primary` | `#FFFFFF` | Texto e iconos sobre el color principal |
| `color-surface` | `#F6FAFE` | Fondo base de la pagina |
| `color-on-surface` | `#17212B` | Texto principal |
| `color-secondary-text` | `#4D5B69` | Textos explicativos y etiquetas secundarias |
| `color-barber-red` | `#A62B2B` | Reflejos decorativos y detalles de barberia |
| `color-error` | `#A62B2B` | Mensajes e iconos de error, acompanado siempre de texto |
| `color-glass` | `rgb(255 255 255 / 30%)` | Base translucida de los controles Liquid Glass |
| `color-glass-border` | `rgb(255 255 255 / 68%)` | Borde luminoso de los controles de cristal |

### Reglas de color

- El azul es el color de las acciones principales.
- El rojo se usa con moderacion. No se emplea como fondo general.
- Las franjas azul, blanca y roja son decorativas y nunca se colocan con
  intensidad alta detras de un texto.
- El texto normal es opaco; la transparencia se aplica a las superficies.
- El texto blanco sobre `color-primary` tiene contraste superior a 4.5:1.
- El texto oscuro `color-on-surface` sobre el fondo claro tambien supera 4.5:1.

## Tipografia

- Familia: `-apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif`.
- Tamano de titulo principal: `48px` en escritorio y `36px` en movil.
- Tamano de texto normal: `17px`.
- Tamano de etiquetas y botones: `16px`.
- Pesos utilizados: `400` para texto, `600` para botones y `700` para titulos.
- Decision del proyecto: se usa la fuente disponible en el sistema para que
  la interfaz sea rapida, legible y cercana al lenguaje visual de Apple.

## Espaciado y forma

- Unidad base de espaciado: `8px`.
- Espaciados: `s = 8px`, `m = 16px`, `l = 24px`, `xl = 32px`.
- Radio de tarjetas: `24px`.
- Radio de campos, botones y navegacion: `999px`, para obtener forma de capsula.
- Anchura maxima del contenido: `880px`.
- Los controles deben tener una altura minima de `48px`.
- Se deja espacio libre alrededor de cada grupo para mantener una jerarquia clara.

## Estilo Liquid Glass

- Liquid Glass se reserva para navegacion, campos, botones y controles.
- Las tarjetas de contenido usan un material translucido mas tranquilo para no
  competir con los controles.
- Desenfoque de referencia: `blur(18px)`.
- Saturacion de referencia: `saturate(125%)`.
- La superficie de cristal tiene un borde blanco fino y una sombra suave.
- Los reflejos azul y rojo aparecen solo en una parte del borde y con opacidad baja.
- Debe existir una alternativa mas opaca cuando el navegador no admita
  `backdrop-filter` o la persona prefiera reducir la transparencia.

Patron decorativo de referencia:

```css
--barber-reflection: repeating-linear-gradient(
  135deg,
  rgb(18 59 93 / 10%) 0 18px,
  rgb(255 255 255 / 16%) 18px 36px,
  rgb(166 43 43 / 10%) 36px 54px
);
```

El patron se combina con el cristal, pero debe ser casi imperceptible. No se usa
como sustituto del color de fondo ni como unica forma de comunicar informacion.

## Componentes

- Boton principal: capsula Liquid Glass con base azul `color-primary`, texto
  blanco, peso `600` y altura minima de `48px`. Al pasar el raton aumenta
  ligeramente el brillo; deshabilitado reduce el contraste visual pero mantiene
  el texto legible y no responde al puntero.
- Campo de texto: capsula Liquid Glass clara, etiqueta o placeholder visible,
  borde blanco fino y reflejos de barberia muy tenues. Al recibir foco muestra
  un contorno azul claramente visible.
- Zona de resultado o mensaje: tarjeta de material translucido estandar, no
  Liquid Glass intenso. Muestra `Hello World` o `Hello World Ana` con texto opaco.
- Mensaje de error: tarjeta translucida con tono rojo suave, icono, titulo y
  texto `No se ha podido contactar con el backend`. El color no es la unica pista.
- Navegacion: barra flotante de cristal con `Inicio` y `Hello`. La opcion activa
  se diferencia mediante forma, contraste y texto, no solo por el color.
- Franja de barberia: capsula decorativa muy fina bajo la navegacion, con los
  tres colores a baja opacidad y sin texto encima.

## Estados de la pagina Hello

1. Inicial: campo vacio y zona de resultado sin saludo.
2. Cargando: boton temporalmente deshabilitado e indicador con texto `Cargando...`.
3. Correcto: zona de resultado con `Hello World` o `Hello World Ana`.
4. Error: aviso con `No se ha podido contactar con el backend` y opcion de reintentar.

## Accesibilidad

- Contraste minimo del texto normal: `4.5:1` (WCAG AA).
- Foco visible: contorno de `3px` en azul, separado `3px` del componente.
- Todos los campos tienen una etiqueta visible asociada.
- Los mensajes no dependen solamente del color: incluyen texto e icono.
- Los controles se pueden utilizar con teclado.
- Las animaciones respetan `prefers-reduced-motion`.
- La interfaz ofrece fondos mas opacos mediante `prefers-reduced-transparency`
  cuando este disponible, y una alternativa CSS sin desenfoque.
- La legibilidad tiene prioridad sobre el efecto de cristal.

## Tono de los textos

- Cercano, claro y breve.
- Se habla de tu a la persona usuaria.
- Se evitan tecnicismos en los mensajes visibles de la interfaz.
- Los errores explican que ha ocurrido y que puede hacer la persona.
- Ejemplo de bienvenida: `Escribe tu nombre y te saludare`.
- Ejemplo de error: `No se ha podido contactar con el backend. Intentalo de nuevo.`

## Fuentes consultadas

- Apple Human Interface Guidelines: https://developer.apple.com/design/human-interface-guidelines/
- Apple HIG - Materials: https://developer.apple.com/design/human-interface-guidelines/materials
- Apple - Adopting Liquid Glass: https://developer.apple.com/documentation/TechnologyOverviews/adopting-liquid-glass
- WebAIM Contrast Checker: https://webaim.org/resources/contrastchecker/
