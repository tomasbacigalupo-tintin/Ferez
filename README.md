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
