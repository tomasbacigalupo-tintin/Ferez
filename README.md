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
