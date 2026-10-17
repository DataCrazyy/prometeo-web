// Construye enlaces internos respetando el BASE_PATH (útil en GitHub Pages sin dominio propio).
export const url = (path = '') => {
  const base = import.meta.env.BASE_URL.endsWith('/') ? import.meta.env.BASE_URL : import.meta.env.BASE_URL + '/';
  return base + path.replace(/^\//, '');
};
