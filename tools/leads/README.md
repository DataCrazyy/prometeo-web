# Guardar los contactos de la web en Google Sheets

Así cada persona que llena un formulario (contacto, reunión, inscripción a un curso o lista de Talks)
queda guardada como una fila en una hoja de cálculo, y además les llega un correo de aviso.
Es gratis y toma unos 10 minutos.

1. Con la cuenta **techprometeo@gmail.com**, crea una hoja nueva en Google Sheets llamada **"Prometeo · Contactos web"**.
2. En la hoja: **Extensiones → Apps Script**.
3. Borra lo que aparece y pega todo el contenido de `apps-script.gs`. Guarda.
4. Arriba a la derecha: **Implementar → Nueva implementación**.
   - Tipo: **Aplicación web**
   - Ejecutar como: **Yo**
   - Quién tiene acceso: **Cualquier usuario**
5. Acepta los permisos (Google avisará que la app no está verificada: *Configuración avanzada → Ir a…*). Es tu propio script.
6. Copia la **URL de la aplicación web** (termina en `/exec`).
7. Pégala en `src/data/site.ts`, en `formEndpoint: '...'`.
8. Publica el sitio de nuevo.

Para probar: abre la URL `/exec` en el navegador; debe decir "Prometeo · receptor de formularios activo".
Luego llena el formulario de contacto del sitio y revisa que aparezca la fila en la pestaña **Contactos**.

Columnas que se guardan: fecha, origen (qué formulario), tema, nombre, cargo, empresa, correo, WhatsApp,
datos de la reunión (día, horario, modalidad), datos de inscripción (curso, nivel, personas, pago, total),
mensaje, cómo nos conoció y la página desde donde escribió.
