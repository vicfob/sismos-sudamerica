/* Service worker del Observatorio Sísmico.
 *
 * Existe por una razón concreta: después de un sismo mayor se cae la luz y se
 * satura la red móvil justo en el momento en que la gente necesita saber qué
 * hacer. Sin esto, la herramienta es una pantalla en blanco precisamente cuando
 * más falta hace.
 *
 * Estrategias, distintas según lo que cueste equivocarse:
 *  - La aplicación (index.html): red primero, con copia guardada. Así siempre se
 *    ve la versión más reciente si hay conexión, y la última conocida si no.
 *  - Librerías y estilos: copia primero. No cambian y no vale la pena esperarlas.
 *  - Catálogo de sismos (USGS/EMSC): red primero. Si falla, se sirve la última
 *    respuesta guardada, marcada para que la interfaz pueda advertirlo.
 *  - Teselas del mapa: copia primero, con tope de tamaño para no llenar el
 *    almacenamiento del teléfono.
 */
const VERSION    = "v3";
const APP_CACHE  = `sismos-app-${VERSION}`;
const LIB_CACHE  = `sismos-lib-${VERSION}`;
const DATA_CACHE = `sismos-data-${VERSION}`;
const TILE_CACHE = `sismos-tiles-${VERSION}`;
const TILE_MAX   = 350;                       // teselas guardadas como máximo

const APP_SHELL = ["./", "./index.html", "./manifest.webmanifest", "./icon.svg",
                   "./data/ciudades.json"];

const esDatos = u =>
  u.hostname.includes("earthquake.usgs.gov") || u.hostname.includes("seismicportal.eu");
const esTesela = u =>
  u.hostname.includes("basemaps.cartocdn.com") || u.hostname.includes("tile.openstreetmap");
const esLibreria = u =>
  u.hostname === "unpkg.com" || u.hostname === "cdn.plot.ly" ||
  u.hostname === "fonts.googleapis.com" || u.hostname === "fonts.gstatic.com" ||
  u.hostname === "raw.githubusercontent.com";

self.addEventListener("install", ev => {
  ev.waitUntil((async () => {
    const cache = await caches.open(APP_CACHE);
    // addAll falla entero si un recurso falla; se piden de a uno para tolerarlo
    await Promise.all(APP_SHELL.map(u => cache.add(u).catch(() => {})));
    await self.skipWaiting();
  })());
});

self.addEventListener("activate", ev => {
  ev.waitUntil((async () => {
    const vigentes = [APP_CACHE, LIB_CACHE, DATA_CACHE, TILE_CACHE];
    for(const nombre of await caches.keys())
      if(nombre.startsWith("sismos-") && !vigentes.includes(nombre)) await caches.delete(nombre);
    await self.clients.claim();
  })());
});

/* Mantiene acotado el número de teselas guardadas (las más viejas se van). */
async function podar(nombre, max){
  const cache = await caches.open(nombre);
  const claves = await cache.keys();
  for(let i = 0; i < claves.length - max; i++) await cache.delete(claves[i]);
}

async function redPrimero(req, nombreCache, marcarSiEsCopia){
  const cache = await caches.open(nombreCache);
  try{
    const res = await fetch(req);
    if(res && res.ok) cache.put(req, res.clone());
    return res;
  }catch(err){
    const guardada = await cache.match(req);
    if(guardada && marcarSiEsCopia){
      // la interfaz lee esta cabecera para avisar de que son datos guardados
      const cabeceras = new Headers(guardada.headers);
      cabeceras.set("X-Sismos-Cache", "1");
      return new Response(await guardada.blob(), {status:200, headers:cabeceras});
    }
    if(guardada) return guardada;
    throw err;
  }
}

async function copiaPrimero(req, nombreCache, max){
  const cache = await caches.open(nombreCache);
  const guardada = await cache.match(req);
  if(guardada) return guardada;
  const res = await fetch(req);
  if(res && res.ok){
    await cache.put(req, res.clone());
    if(max) podar(nombreCache, max);
  }
  return res;
}

self.addEventListener("fetch", ev => {
  const req = ev.request;
  if(req.method !== "GET") return;
  let url;
  try{ url = new URL(req.url); }catch(e){ return; }
  if(url.protocol !== "http:" && url.protocol !== "https:") return;

  if(req.mode === "navigate"){
    ev.respondWith(redPrimero(req, APP_CACHE, false)
      .catch(() => caches.match("./index.html")));
    return;
  }
  if(esDatos(url)){    ev.respondWith(redPrimero(req, DATA_CACHE, true)); return; }
  if(esTesela(url)){   ev.respondWith(copiaPrimero(req, TILE_CACHE, TILE_MAX)
                          .catch(() => Response.error())); return; }
  if(esLibreria(url)){ ev.respondWith(copiaPrimero(req, LIB_CACHE)
                          .catch(() => caches.match(req))); return; }
  if(url.origin === self.location.origin){
    ev.respondWith(redPrimero(req, APP_CACHE, false).catch(() => caches.match(req)));
  }
});
