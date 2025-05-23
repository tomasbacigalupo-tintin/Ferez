# WiFi Fixer Tool

Esta aplicación de escritorio está pensada para diagnosticar y resolver problemas de conectividad WiFi y de red en cualquier sistema operativo. Incluye pruebas de gateway, detección de conflictos de IP, verificación de DHCP y chequeo de puertos.

## Requisitos para desarrolladores
- Python 3 y `pip` para generar el ejecutable.
- Algunos comandos pueden requerir permisos de administrador/superusuario.

## Uso

Durante el desarrollo puedes ejecutar el script directamente:

```bash
python wifi_fix_tool.py
```

Se abrirá una ventana con botones para:
- Verificar la conexión a Internet.
- Reiniciar el adaptador de red.
- Renovar la IP.
- Limpiar la caché DNS.
- Cambiar a DNS públicos (Google).
- Ejecutar un **Diagnóstico avanzado** para detectar conflictos de IP, problemas de DHCP y bloqueo de puertos.
- Ejecutar todas las acciones automáticamente con **Arreglar todo**.
- Abrir el archivo de reporte generado.

Cada acción genera un reporte en un archivo `wifi_fix_report.txt` ubicado en el directorio personal del usuario.

## Distribución sin dependencias

Para generar un ejecutable que no requiera tener Python instalado se puede utilizar **PyInstaller**. Una vez instalado, ejecuta:

```bash
pyinstaller --onefile wifi_fix_tool.py
```

El archivo resultante en la carpeta `dist` funcionará con doble clic en Windows, macOS o Linux, dependiendo del sistema donde se genere.
Los usuarios finales solo necesitan descargar este archivo y ejecutarlo; no es necesario instalar Python, Git ni otras dependencias.
