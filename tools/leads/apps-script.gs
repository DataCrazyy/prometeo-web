/**
 * Prometeo · Guardar contactos de la web en Google Sheets
 * ------------------------------------------------------
 * Cada formulario del sitio (contacto, reunión, inscripción a cursos, lista de Talks)
 * llega aquí y se guarda como una fila en la hoja "Contactos".
 * Además envía un correo de aviso a NOTIFY_EMAIL.
 *
 * Instalación: ver tools/leads/README.md
 */
const SHEET_NAME = 'Contactos';
const NOTIFY_EMAIL = 'techprometeo@gmail.com';

// Columnas en orden. Si llega un campo nuevo, se agrega al final automáticamente.
const BASE_HEADERS = [
  'fecha', 'origen', 'tema', 'tema_nombre', 'nombre', 'cargo', 'empresa', 'email', 'whatsapp',
  'reunion', 'fecha_reunion', 'horario', 'modalidad',
  'curso', 'nivel', 'personas', 'pago', 'total',
  'mensaje', 'fuente', 'pagina',
];

function doPost(e) {
  const lock = LockService.getScriptLock();
  lock.waitLock(10000);
  try {
    const p = (e && e.parameter) || {};
    const ss = SpreadsheetApp.getActiveSpreadsheet();
    const sh = ss.getSheetByName(SHEET_NAME) || ss.insertSheet(SHEET_NAME);

    // Encabezados
    let headers = sh.getLastRow() ? sh.getRange(1, 1, 1, sh.getLastColumn()).getValues()[0] : [];
    if (!headers.length) {
      headers = BASE_HEADERS.slice();
      sh.getRange(1, 1, 1, headers.length).setValues([headers]).setFontWeight('bold');
      sh.setFrozenRows(1);
    }
    Object.keys(p).forEach((k) => {
      if (headers.indexOf(k) === -1) {
        headers.push(k);
        sh.getRange(1, headers.length).setValue(k).setFontWeight('bold');
      }
    });

    const row = headers.map((h) => (h === 'fecha' ? new Date() : (p[h] || '')));
    sh.appendRow(row);

    // Aviso por correo
    const lines = headers.filter((h) => h !== 'fecha' && p[h]).map((h) => h + ': ' + p[h]);
    MailApp.sendEmail(NOTIFY_EMAIL, 'Nuevo contacto web · ' + (p.origen || 'Prometeo'), lines.join('\n'));

    return ContentService.createTextOutput(JSON.stringify({ ok: true })).setMimeType(ContentService.MimeType.JSON);
  } catch (err) {
    return ContentService.createTextOutput(JSON.stringify({ ok: false, error: String(err) })).setMimeType(ContentService.MimeType.JSON);
  } finally {
    lock.releaseLock();
  }
}

// Para probar desde el navegador que el script está publicado
function doGet() {
  return ContentService.createTextOutput('Prometeo · receptor de formularios activo');
}
