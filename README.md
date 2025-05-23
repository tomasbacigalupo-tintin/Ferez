# WiFi Fixer Tool

Esta aplicación de escritorio está pensada para diagnosticar y resolver problemas comunes de conectividad WiFi en cualquier sistema operativo.

## Requisitos
- Python 3 instalado.
- Algunos comandos pueden requerir permisos de administrador/superusuario.

## Uso

Ejecuta el script directamente:

```bash
python wifi_fix_tool.py
```

Se abrirá una ventana con botones para:
- Verificar la conexión a Internet.
- Reiniciar el adaptador de red.
- Renovar la IP.
- Limpiar la caché DNS.
- Cambiar a DNS públicos (Google).
- Ejecutar todas las acciones automáticamente con **Arreglar todo**.
- Abrir el archivo de reporte generado.

Cada acción genera un reporte en un archivo `wifi_fix_report.txt` ubicado en el directorio personal del usuario.
