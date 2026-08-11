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
- **El «potencial de daño» es una estimación.** La intensidad de Mercalli (MMI) que se
  muestra al hacer clic en un epicentro se calcula a partir de magnitud y profundidad;
  **no es daño observado**. La intensidad real depende de la geología local, el tipo de
  suelo y la construcción.
- **Los canales de ayuda son enlaces a fuentes oficiales**, no direcciones verificadas por
  este proyecto. Los puntos de acopio cambian a diario: **verifica siempre** con las
  entidades oficiales antes de donar o desplazarte, y usa solo canales oficiales para
  donaciones económicas.
- **No está afiliado** al USGS, al Servicio Geológico Colombiano (SGC), a la UNGRD ni a la
  Cruz Roja. Para información oficial de emergencias, consulta directamente esas entidades.
- Se entrega **"AS IS"**, sin garantías (ver [LICENSE](./LICENSE)).

---

## ✨ Características

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
  sísmico de Bucaramanga, contexto tectónico y **medida de daño estimada (MMI) por clic**.
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
├── scripts/
│   └── seismic_heatmap.py  # Generador de mapas de densidad estáticos (Python)
├── requirements.txt        # Dependencias del script
├── LICENSE                 # Licencia MIT
├── .gitignore
└── README.md
```

---

## 🧪 Metodología (resumen)

| Módulo | Método | Nota |
|---|---|---|
| Valor *b* | Máxima verosimilitud (Aki–Utsu) | Depende de la magnitud de completitud (Mc) |
| Pronóstico espacial | Sismicidad suavizada (kernel gaussiano) + Gutenberg–Richter + Poisson | Línea base tipo CSEP |
| Pronóstico temporal | Ley de Omori–Utsu e intensidad condicional ETAS | La proyección asume que no hay nuevos disparadores |
| Potencial de daño | Intensidad de Mercalli estimada a partir de M y profundidad | Estimación, no daño observado |

La magnitud de completitud (Mc) es clave: ajústala hasta que coincida con el pico del
histograma de magnitud para que las estimaciones sean fiables.

---

## 📊 Fuentes de datos y atribución

- **Sismos**: [USGS FDSN Event Web Service](https://earthquake.usgs.gov/fdsnws/event/1/)
- **Mapa base**: [CARTO](https://carto.com/) © OpenStreetMap
- **Límites de placas**: [fraxen/tectonicplates](https://github.com/fraxen/tectonicplates) (PB2002)
- **Librerías**: [Leaflet](https://leafletjs.com/), [Leaflet.heat](https://github.com/Leaflet/Leaflet.heat), [Plotly.js](https://plotly.com/javascript/)
- **Geolocalización por IP**: ipapi.co / ipwho.is (con respaldo)
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

