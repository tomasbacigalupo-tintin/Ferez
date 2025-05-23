# WiFi Fixer Tool

Esta aplicación de escritorio diagnostica y soluciona problemas de conectividad WiFi y de red en Windows, macOS y Linux. Incluye comprobaciones de gateway, detección de conflictos de IP, verificación de DHCP y test de puertos.

## Estructura del proyecto

El código se organiza como un paquete Python llamado `wifi_fix` que contiene:

- **core.py**: lógica de diagnóstico y reparación.
- **system.py**: abstracción de comandos específicos por plataforma.
- **logger.py**: generación de reportes en `wifi_fix_report.txt`.
- **gui_tkinter.py**: interfaz gráfica simple para escritorio.
- **server.py**: servicio opcional FastAPI para exponer la lógica a otras interfaces (por ejemplo Tauri/Electron).

El script `wifi_fix_tool.py` ejecuta la interfaz Tkinter por defecto.

## Requisitos para desarrolladores

- Python 3.11 o superior.
- Algunas acciones pueden requerir permisos de administrador/superusuario.

## Uso

Durante el desarrollo puedes iniciar la GUI directamente:

```bash
python wifi_fix_tool.py
```

Para ejecutar la API REST (útil para integrarse con una interfaz Tauri o Electron):

```bash
uvicorn wifi_fix.server:app --reload
```

Cada acción genera un reporte en `wifi_fix_report.txt` dentro de tu directorio personal.
Además se genera un archivo `wifi_fix_report.jsonl` con el mismo contenido en formato JSON.

## Distribución sin dependencias

Se recomienda usar **PyInstaller** para crear un ejecutable autónomo:

```bash
pyinstaller --onefile wifi_fix_tool.py
```

El archivo resultante en `dist` funcionará con doble clic en el sistema donde se genere. Los usuarios finales no necesitan instalar Python ni otras dependencias.

También puedes utilizar `make_executable.py` para simplificar la generación del binario:

```bash
python make_executable.py
```

## Actualizaciones automáticas

La carpeta `updater/` contiene funciones para comprobar si existen nuevas
versiones de la aplicación y aplicar paquetes de actualización descargados en
formato ZIP. Estas rutinas están pensadas para integrarse en futuras versiones
del programa.


## Frontend multiplataforma con Tauri

Se incluye un ejemplo mínimo de interfaz creada con **Tauri** en la carpeta `ui/tauri`.
Esta UI consume la API REST de `wifi_fix.server` y permite ejecutar las acciones
principales desde una ventana nativa.

Tauri permite usar tecnologías web modernas y genera binarios ligeros y seguros.
Si se requiere un ecosistema de librerías web más amplio se podría usar
**Electron**, aunque el tamaño final sería mayor.

Para probar la interfaz Tauri primero inicia el servidor FastAPI:

```bash
uvicorn wifi_fix.server:app --reload
```

Luego, dentro de `ui/tauri/src-tauri`, compila y ejecuta la aplicación
(requiere Rust y las herramientas de Tauri instaladas):

```bash
cargo tauri dev
```

La UI se inspira en apps como Notion o Linear: tipografía limpia, colores
neutros con toques de acento, espaciado generoso y soporte de modo oscuro.

## Frontend web con React y Vite

Se incluye una interfaz web desarrollada con **React** y **Vite** en la carpeta `ui/react-vite`. Esta interfaz utiliza el mismo estilo sobrio que la versión Tauri (inspirado en Notion/Linear/Raycast) y consume la API REST proporcionada por `wifi_fix.server`.

Para probarla es necesario instalar las dependencias de Node y luego ejecutar Vite:

```bash
cd ui/react-vite
npm install
npm run dev
```

Por defecto la aplicación se sirve en `http://localhost:5173` y espera que la API de FastAPI esté disponible en `http://localhost:8000`.

## Diseño de flujos de usuario

La carpeta `docs/UX_JOURNEY.md` contiene un esquema detallado de la experiencia de usuario propuesta para la herramienta. Allí se describen los pasos desde la apertura de la aplicación hasta el acceso al historial de reportes.

