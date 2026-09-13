# Guion — Video de sustentación (máx. 10 min)
### Tarea 01: Persistencia, API REST y Autenticación — App de notas

---

## 0:00 – 0:40 · Introducción
"Hola, soy Esneider. Esta es la Tarea 01 de Línea de Énfasis II: una app de gestión de notas con persistencia local, API REST y autenticación.

Todo el proyecto está hecho 100% en Python: el backend con Flask, y la app móvil con Flet, un framework que compila Python directamente sobre el motor de Flutter. Elegí esta combinación para no depender de un segundo lenguaje como Dart, y reforzar Python de punta a punta."

---

## 0:40 – 2:00 · Arquitectura (mostrar el diagrama o explicar en palabras)
"El proyecto tiene dos componentes independientes que hablan por HTTP:

- **notas-api**: el backend en Flask. Expone los endpoints REST, maneja la autenticación con JWT, y guarda las notas en una base de datos del lado del servidor.
- **notas_app**: la app móvil en Flet. Tiene su propia base de datos local en SQLite para el modo offline, y un cliente HTTP que consume la API.

Muestro rápido la estructura de carpetas de cada uno..." *(mostrar el explorador de VS Code de ambos proyectos, 15-20 segundos cada uno)*

---

## 2:00 – 4:00 · Demo del backend (Postman)
"Antes de mostrar la app, pruebo la API directamente para que se vea que funciona de forma independiente."

1. `POST /register` → mostrar `201` con el id creado.
2. `POST /login` → mostrar `200` con el `access_token`.
3. `POST /notas` (con el Bearer Token) → mostrar `201`.
4. `GET /notas` → mostrar el array con la nota.

"Con esto ya se ve: la contraseña nunca viaja ni se guarda en texto plano, el login entrega un token JWT, y ese token es obligatorio para tocar `/notas` — si lo quito, el servidor responde 401."

*(Opcional: mostrar un intento sin el header Authorization para demostrar el 401 en vivo)*

---

## 4:00 – 7:00 · Demo de la app móvil (Flet)
1. Abrir la app → pantalla de login.
2. Registrar un usuario nuevo → iniciar sesión → caer en "Mis notas".
3. Crear una nota → explicar: "esto se guardó primero en SQLite local, y se sincronizó sola con el servidor — se ve marcada como ✅ sincronizada".
4. Editar esa nota (ícono de lápiz) → cambiar el texto → "Actualizar nota" → mostrar que pasó a ⏳ pendiente y luego se sincronizó.
5. **Demostración del modo offline** (la parte más importante):
   - Apagar el servidor Flask (Ctrl+C en su terminal).
   - Crear una nota nueva en la app → debe quedar "⏳ pendiente" y el mensaje debe decir que no hay conexión.
   - Prender el servidor de nuevo.
   - Clic en "Sincronizar ahora" → la nota pasa a "✅ sincronizada".
   - "Esto demuestra que la app nunca pierde información aunque no haya internet en el momento de crear la nota."
6. Eliminar una nota (ícono de basura) → aclarar en voz: "esto elimina localmente; eliminarla también del lado del servidor queda planteado como mejora para una siguiente entrega."

---

## 7:00 – 9:00 · Explicación de las decisiones técnicas
"Para cerrar, explico las tres decisiones clave, que también dejé documentadas en el Word:

- **Persistencia**: SQLite local con un campo `sincronizado` (0/1) que marca si una nota ya llegó al servidor o sigue pendiente. Es el patrón *offline-first*: primero se guarda local, después se sincroniza.
- **API REST**: un cliente HTTP centralizado (`ApiClient`, con `httpx`) que decide entre crear (POST) o actualizar (PUT) según si la nota ya tiene un id del servidor.
- **Autenticación**: JWT con `flask-jwt-extended`. Contraseñas hasheadas con `werkzeug.security`, tokens firmados con una clave generada con `secrets.token_hex`, y cada endpoint de notas filtrado por el id del usuario dentro del token — así nadie puede ver las notas de otro usuario."

---

## 9:00 – 10:00 · Cierre
"El código completo, tanto del backend como de la app, está en mi repositorio de GitHub [decir el link o mostrarlo en pantalla]. Con esto cubro los tres requisitos de la tarea: persistencia, API REST y autenticación. Gracias."

---

### Notas para grabar
- Practica una vez sin cámara para medir el tiempo real — este guion apunta a ~9-10 min hablando con calma.
- Si te pasas de tiempo, el tramo más recortable es el "0:40–2:00" (arquitectura) — puedes resumirlo a una sola frase y apoyarte en lo visual.
- Ten las dos terminales y Postman ya abiertos antes de darle grabar, para no perder tiempo muerto buscando ventanas.
