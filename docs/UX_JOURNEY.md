# Diseño de flujos de usuario (UX Journey)

Este documento resume la experiencia de usuario propuesta para **WiFi Fixer Tool**.

## 1. Inicio inmediato

- Doble clic sobre el ejecutable y la aplicación se abre en menos de dos segundos.
- Aparece una pantalla de bienvenida sencilla con tres botones principales:
  - **Diagnóstico rápido**
  - **Reparación automática**
  - **Ver reporte**

## 2. Diagnóstico avanzado

- Vista que muestra el progreso de cada etapa en tiempo real:
  1. Ping a un servidor conocido.
  2. Verificación de gateway predeterminado.
  3. Comprobación de DHCP e IP asignada.
  4. Resolución DNS básica.
  5. Test de puertos comunes.
  6. Estado de los adaptadores de red.
  7. Detección de VPN o proxys activos.
  8. Procesos colgados que puedan afectar la red.
- Cada paso indica **éxito**, **advertencia** o **error**.

## 3. Reparación automática

- Un único botón ejecuta las acciones recomendadas:
  - Reinicio del adaptador de red.
  - Renovación de la dirección IP.
  - Limpieza de la caché DNS.
  - Ajustes básicos de firewall.
  - Otros pasos necesarios.
- Al finalizar se ofrece abrir el reporte detallado generado por la aplicación.

## 4. Modo manual

- Para usuarios avanzados se mantiene un panel con herramientas individuales (similar a la versión actual).
- Cada acción puede ejecutarse de forma aislada y se registra en el reporte.

## 5. Historial y soporte

- Acceso a registros y reportes previos desde la misma aplicación.
- Opción de exportar y enviar el log a un equipo de soporte para análisis.

