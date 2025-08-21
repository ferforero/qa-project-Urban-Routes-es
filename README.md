# QA Project: Urban.Routes Automatizacion de pruebas de la aplicacion WeB (ES)
Mi nombre es Fernanda Forero (cohort 32) Sprint 8 Bootcamp Tripleten QA Engineer.
Este proyecto automatiza un flujo de prueba desde inicio a fin en la web Urban Driver
Suite de pruebas E2E con **Python + Selenium + Pytest** aplicando **Page Object Model (POM)**.

---

## 🧰 Tecnologías
- Python 3.11+  
- Selenium WebDriver 4+  
- Pytest  
- Google Chrome (y su driver compatible)
---

## 📁 Estructura del proyecto

.
├─ data.py # Datos: URL, direcciones, teléfono, tarjeta, mensaje, etc.
├─ helpers.py # Utilidades (p.ej. retrieve_phone_code para leer el SMS desde logs)
├─ pages.py # Page Objects (UrbanRoutesPage): localizadores + métodos
├─ main.py # Tests (pytest) que usan la page
└─ README.md

---

## ⚙️ Preparación del entorno

1. (Opcional) Crear y activar un entorno virtual:
   ```bash
   python -m venv .venv
   # macOS/Linux
   source .venv/bin/activate
   # Windows
   .venv\Scripts\activate
Instalar dependencias:

pip install -U selenium pytest

El proyecto ya configura los performance logs en main.py (goog:loggingPrefs) para que retrieve_phone_code pueda leer el código SMS desde helpers.py después de solicitarlo en la UI.

▶️ Cómo ejecutar
Desde la raíz del proyecto:

pytest -q main.py


🧪 Pruebas incluidas
Setear ruta (origen/destino).

Seleccionar tarifa Comfort.

Registrar teléfono con verificación por SMS.

Agregar tarjeta como método de pago.

Agregar comentario para el conductor.

Activar “Manta y pañuelos” (switch).

Agregar 2 helados (counter).

Pedir taxi y verificar el modal “Buscar automóvil”.

🧩 Notas y buenas prácticas
Prioriza selectores CSS; usa XPath cuando aporte más robustez.

Evita XPaths absolutos salvo que no haya alternativa (son frágiles).

Usa esperas explícitas (WebDriverWait + expected_conditions) antes de interactuar.

retrieve_phone_code(driver) solo funcionará después de solicitar el código en la app.

✅ Estado
El proyecto ejecuta 8 pruebas E2E organizadas con POM y separadas en:

helpers.py (utilidades),

pages.py (interacciones/UI),

main.py (tests),

data.py (datos de prueba).
