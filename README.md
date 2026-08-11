# 🌎 Observatorio Sísmico · Sudamérica

<img width="1867" height="810" alt="image" src="https://github.com/user-attachments/assets/7ee1d9c6-7ca6-4587-ac4d-139a319141e3" />

Dashboard interactivo y de código abierto para **analizar, visualizar y pronosticar
sismicidad en Sudamérica** a partir de datos en tiempo real del USGS, con una sección
dedicada a **Colombia** y una capa de **respuesta y ayuda ante emergencias**.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](./LICENSE)
[![Datos: USGS](https://img.shields.io/badge/datos-USGS%20FDSN-blue.svg)](https://earthquake.usgs.gov/fdsnws/event/1/)
[![Sin backend](https://img.shields.io/badge/backend-no%20requerido-brightgreen.svg)](#)

Todo el dashboard es un **UN UNICO ARCHIVO** que corre en el navegador y consulta la
API pública del USGS directamente: no necesita servidor, base de datos ni instalación.

---

## ⚠️ Aviso importante — léelo antes de usar

Este proyecto es una herramienta **educativa y de análisis**. Para que su uso sea
responsable, ten presente que:

- **No predice terremotos.** La ciencia actual no permite predecir sismos individuales
  (lugar, fecha y magnitud exactos). Lo que aquí se llama «pronóstico» es
  **probabilístico**: estima *dónde es más probable* que ocurra actividad y *cómo decae*
  una secuencia de réplicas, con modelos estándar (Gutenberg–Richter, sismicidad
  suavizada + Poisson, ETAS/Omori). No es una alerta ni una garantía.
- **La intensidad describe la sacudida, no el daño observado.** La intensidad de Mercalli
  (MMI) que se muestra al hacer clic en un epicentro proviene de **ShakeMap** (medida por
  instrumentos) o de los reportes ciudadanos de **DYFI**. Cuando el USGS aún no publicó
  ninguna de las dos, se calcula una estimación a partir de magnitud y profundidad, y
  aparece marcada como `est`. El daño real depende de la geología local, el tipo de suelo
  y la construcción.
- **La alerta PAGER es del USGS, no de este proyecto.** Cuando aparece la banda de alerta
  naranja o roja, es el nivel oficial publicado por el USGS. Para decisiones de emergencia,
  consulta siempre al SGC y a la UNGRD.
- **Esto no es alerta sísmica temprana ni un canal oficial de emergencia.** La alerta temprana
  real gana segundos detectando la onda P con redes dedicadas; un navegador que consulta un
  catálogo recibe el sismo minutos después, siempre tarde para la sacudida. El aviso de tsunami
  que muestra la herramienta es un **recordatorio de la regla de autoevacuación**, no una alerta:
  el aviso oficial lo dan DIMAR y el CCCP en Colombia, y el PTWC a nivel internacional.
- **Los canales de ayuda son enlaces a fuentes oficiales**, no direcciones verificadas por
  este proyecto. Los puntos de acopio cambian a diario: **verifica siempre** con las
  entidades oficiales antes de donar o desplazarte, y usa solo canales oficiales para
  donaciones económicas.
- **No está afiliado** al USGS, al Servicio Geológico Colombiano (SGC), a la UNGRD ni a la
  Cruz Roja. Para información oficial de emergencias, consulta directamente esas entidades.
- Se entrega **"AS IS"**, sin garantías (ver [LICENSE](./LICENSE)).

---

## ✨ Características

- **Intensidad real, no estimada**: cada sismo muestra la intensidad de Mercalli medida por
  ShakeMap o reportada por la ciudadanía (DYFI), declarando siempre de dónde sale el dato.
- **Alerta de impacto PAGER**: banda destacada cuando el USGS clasifica un sismo como naranja
  o rojo, con enlace a la ficha oficial, al SGC y a la UNGRD. Los sismos con alerta se
  distinguen en el mapa con un anillo de color.
- **Ficha de impacto**: para esos sismos se consultan los productos oficiales del USGS y se
  traducen a lo que hace falta decidir — cuánta gente sintió cada nivel de intensidad, riesgo
  de **deslizamientos y licuefacción** (que determinan qué vías se cortan y a qué comunidades
  no llega la ayuda), **probabilidad oficial de réplicas** convertida en una recomendación
  concreta, y ciudades afectadas por población. Cada bloque se dibuja solo si su dato llegó.
- **Huella real de la sacudida**: contornos de ShakeMap sobre el mapa, en vez de un radio
  estimado alrededor del epicentro.
- **Sección «Prepárate»**: qué revisar en tu edificio, qué anclar, plan familiar y kit de 72 h,
  qué hacer durante el sismo y en las horas siguientes, y desmentido de los mitos que circulan
  tras cada emergencia. Es la parte que más muertes evita y **no necesita conexión ni API**.
- **Aviso de tsunami** para sismos superficiales de M≥7 frente a la costa: recuerda la única
  regla que llega a tiempo en un tsunami cercano —si el sismo dura más de un minuto, evacúa sin
  esperar aviso— y enlaza a DIMAR y al PTWC.
- **Funciona sin conexión** (PWA instalable): tras la primera visita, la aplicación, la sección
  de preparación y el plan familiar quedan disponibles aunque se caiga la red, con los últimos
  datos conocidos y un aviso claro de que no están actualizados.
- **Plan familiar imprimible**, guardado solo en tu dispositivo.
- **Riesgo para la población**: el pronóstico de amenaza cruzado con dónde vive la gente. Ranking
  de ciudades por exposición esperada a sacudidas con daño (MMI ≥ VI), porque *la celda más
  probable casi nunca es la más peligrosa*: en Sudamérica suele estar mar adentro.
- **Doble fuente**: si el USGS no responde, conmuta automáticamente al espejo del EMSC y lo
  indica en la cabecera, sin duplicar sismos que lleguen por ambas redes.
- **Mapa de calor** de epicentros ponderado por energía, con capas de puntos clicables y
  límites de placas tectónicas.
- **Análisis estadístico**: distribución magnitud–frecuencia de Gutenberg–Richter con
  estimación del valor *b*, histogramas de magnitud y profundidad, serie temporal, y un
  **corte en profundidad** que revela la geometría de subducción de Nazca (zona de
  Wadati–Benioff).
- **Pronóstico espacial** (sismicidad suavizada + Poisson): mapa de probabilidad por
  celdas y ranking de zonas con mayor probabilidad, más curva de periodo de retorno.
- **Pronóstico temporal ETAS / Omori**: ajuste por máxima verosimilitud de la ley de
  Omori–Utsu a una secuencia de réplicas e intensidad condicional λ(t) del catálogo.
- **Tiempo real**: sondeo del USGS cada 60 s con fusión incremental (nuevos eventos y
  revisiones) sin recargar todo; indicador *en vivo* y ticker del último evento.
- **Sección Colombia**: vista dedicada al territorio (filtro por polígono del país), nido
  sísmico de Bucaramanga, contexto tectónico e **intensidad (MMI) por clic**.
- **Respuesta y ayuda**: detección de ubicación aproximada por IP, sismos recientes en
  Sudamérica con distancia al usuario, y canales oficiales de ayuda con **búsquedas en
  vivo** que se mantienen actualizadas.
- **Script Python** complementario para generar mapas de densidad estáticos y cache local.

---

## 🚀 Uso

### Opción A — Consulta directa en GH (recomendado, para el público)

Puedes usar el dashboard directamente o descargarlo para uso personal o comercial siguiendo las normas de licencia. Vicfob desarrollada la herramienta como guia pero puede ser actualizada en cualquier momento

### Opción B — Uso local

No requiere instalación: **abre `index.html`** en un navegador moderno con conexión a
internet (necesita acceso a `earthquake.usgs.gov`, que soporta CORS). Si tu red bloquea la
API, el dashboard ofrece cargar un archivo local (GeoJSON/CSV del USGS o el CSV que genera
el script de Python).

### Opción C — Script de mapas estáticos (Python)

```bash
pip install -r requirements.txt
python scripts/seismic_heatmap.py          # genera output/*.html y output/*.png
python scripts/seismic_heatmap.py --no-cache
```

Los parámetros principales (área, rango de años, magnitud de completitud) están al inicio
del script.

---

## 📁 Estructura del repositorio

```
.
├── index.html              # Dashboard (aplicación completa, sin backend)
├── sw.js                   # Service worker: hace que funcione sin conexión
├── manifest.webmanifest    # Permite instalarla como aplicación
├── icon.svg                # Icono
├── data/
│   └── ciudades.json       # Población de ciudades (GeoNames, CC BY 4.0)
├── scripts/
│   └── seismic_heatmap.py  # Generador de mapas de densidad estáticos (Python)
├── requirements.txt        # Dependencias del script
├── LICENSE                 # Licencia MIT
├── .gitignore
└── README.md
```

> El service worker solo se activa sobre `https://` (o `localhost`). Abriendo `index.html`
> directamente desde el disco la aplicación funciona igual, pero sin caché sin conexión.

---

## 🧪 Metodología (resumen)

| Módulo | Método | Nota |
|---|---|---|
| Valor *b* | Máxima verosimilitud (Aki–Utsu) | Depende de la magnitud de completitud (Mc) |
| Pronóstico espacial | Sismicidad suavizada (kernel gaussiano) + Gutenberg–Richter + Poisson | Línea base tipo CSEP |
| Pronóstico temporal | Ley de Omori–Utsu e intensidad condicional ETAS | La proyección asume que no hay nuevos disparadores |
| Intensidad | ShakeMap del USGS → DYFI → estimación propia | Se indica siempre de cuál de las tres proviene |
| Alerta de impacto | Nivel PAGER del USGS (verde/amarillo/naranja/rojo) | Solo naranja y rojo disparan la banda de alerta |
| Población expuesta | PAGER `exposures.json` | Habitantes por grado de intensidad |
| Terreno | Producto `ground-failure` del USGS | Deslizamientos y licuefacción, con población expuesta |
| Réplicas oficiales | Producto `oaf` (ETAS bayesiano del USGS) | Complementa al ajuste Omori–Utsu propio |

### Modelo de intensidad (IPE)

`MMI = 1,171·M − 0,587·log₁₀(R) − 0,00597·R − 0,555`, con **R** la distancia hipocentral en km.

Ajustado por mínimos cuadrados sobre **1.050 observaciones reales**: los 816 sismos M5.5+ de
Sudamérica con intensidad instrumental publicada (2000–2026), más 234 puntos extraídos de los
contornos de ShakeMap de 26 sismos M6.5+, que aportan intensidad medida entre 22 y 1.191 km
del epicentro.

El término lineal en R es imprescindible. Sin él el modelo no tiene atenuación anelástica y,
extrapolado, seguiría dando MMI VI —daños— a 800 km del epicentro. Con él, un M8.0 superficial
da MMI 7,0 a 100 km, 4,9 a 400 km y 2,3 a 800 km.

| | Acierta dentro de ±1 grado | Sesgo | Error absoluto medio |
|---|---|---|---|
| Fórmula original del proyecto | 31 % | +1,57 (exageraba) | 1,59 |
| Modelo actual | 80 % | 0,00 | 0,63 |

Validación cruzada 5-fold: 0,612 fuera de muestra frente a 0,607 dentro, sin sobreajuste.
Validación ciega contra las intensidades que ShakeMap midió en 11 ciudades del sismo M7.4 del
Chocó (2026): error absoluto **0,53 grados** y **100 % dentro de ±1 grado**.

Se usa solo como respaldo cuando el USGS aún no publicó intensidad (~19 % de los eventos M5.5+),
y entonces lleva un margen conservador de +0,2 grados: quedarse corto puede hacer que alguien no
tome una precaución que necesitaba, mientras que pasarse solo gasta credibilidad. Ese margen baja
la subestimación del 9 % al 5 % sin perder aciertos.

### Riesgo para la población

Para cada ciudad se integra, sobre todas las celdas del pronóstico y sobre la distribución de
magnitudes de Gutenberg–Richter, la probabilidad de sufrir MMI ≥ VI. La intensidad se propaga con
su dispersión medida (σ = 0,776), no como un umbral exacto, y la profundidad representativa de
cada celda entra en la atenuación.

**Es una línea base comparativa, no un estudio de amenaza sísmica.** No incluye vulnerabilidad
constructiva ni efecto de sitio —la microzonificación de Bogotá, Cali, Pereira o Medellín—, y las
tasas provienen del catálogo cargado: unas pocas décadas son un plazo corto para estimar la
frecuencia de los sismos mayores, así que los periodos de retorno largos son los menos fiables.

La magnitud de completitud (Mc) es clave: ajústala hasta que coincida con el pico del
histograma de magnitud para que las estimaciones sean fiables.

---

## 📊 Fuentes de datos y atribución

- **Sismos**: [USGS FDSN Event Web Service](https://earthquake.usgs.gov/fdsnws/event/1/)
  (fuente primaria: es la única que publica intensidad medida y alerta PAGER)
- **Espejo de respaldo**: [EMSC — seismicportal.eu](https://www.seismicportal.eu/) — se usa
  automáticamente si el USGS no responde, para no quedarse sin datos durante una emergencia
- **Mapa base**: [CARTO](https://carto.com/) © OpenStreetMap
- **Límites de placas**: [fraxen/tectonicplates](https://github.com/fraxen/tectonicplates) (PB2002)
- **Librerías**: [Leaflet](https://leafletjs.com/), [Leaflet.heat](https://github.com/Leaflet/Leaflet.heat), [Plotly.js](https://plotly.com/javascript/)
- **Geolocalización por IP**: ipapi.co / ipwho.is (con respaldo)
- **Población de ciudades**: [GeoNames](https://www.geonames.org/) — `cities15000`, licencia
  CC BY 4.0. Se incluye en `data/ciudades.json` un extracto de las 1.288 ciudades de Sudamérica
  con 50.000 habitantes o más.
- **Contexto Colombia**: Servicio Geológico Colombiano (SGC) y UNGRD

Cada fuente conserva su propia licencia y términos de uso.

---

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Abre un *issue* para proponer mejoras o reportar
errores, o envía un *pull request*. Ideas de mejora abiertas: ETAS espacio-temporal con
estimación conjunta de parámetros, integración de catálogos regionales (SGC, IGP, CSN),
y declustering configurable.

---

## 📄 Licencia

Distribuido bajo la licencia **MIT**. Consulta [LICENSE](./LICENSE) para más detalles.

<3 
Dona a este proyecto por medio de Bre-b (sistema de pagos instantaneos colombiano) o por hash moneda virtuales

Con cariño @vicfob

