# MONITOR PRIME APP INDICATOR
Este es un APP indicator para usuarios de computadoras portátiles equipados con GPUs híbridos (Intel+AMD, AMD+AMD, Intel+Nvidia). **Su función principal es mostrar el GPU renderizador** cuando se le indique.
Está programado en Python y fue probado en Kubuntu 18.04 LTS, pero nada impide su aplicación para otros entornos y versiones superiores a Ubuntu 14.04 LTS.

Las funciones que realiza **MONITOR PRIME APP INDICATOR** son las siguientes:

- Muestra el "Estado de GPU" (GPU renderizador)
- Muestra las "Aplicaciones en dGPU" (PID y Nombre del proceso)
- Muestra la "Informacion de GPUs" (Vendor, Device, VRAM, etc.)

## IMÁGENES PRINCIPALES (en Kubuntu 18.04)

![app menu](https://lh3.googleusercontent.com/-qWbqLEj9TL8/XSKfgSM7NeI/AAAAAAAAA08/R0-jKBvcdIsy1lUkGrNYauXaFMtt0x37gCLcBGAs/h153/monitor_prime_app_indicator_04.png "Menú principal y sus opciones")

![app menu](https://lh3.googleusercontent.com/-zOm12GdHN3M/XSKgaWkh31I/AAAAAAAAA1M/3v5WpufGmNkCmfpMq4e6S6HwE9vLJ75wwCLcBGAs/h620/monitor_prime_app_indicator_06.png "Aplicaciones renderizadas en el dGPU")

## DEPENDENCIAS
- gir1.2-appindicator3-0.1 (sudo apt install gir1.2-appindicator3-0.1)
- mesa-utils (sudo apt install mesa-utils)
- kate (sudo apt install kate)

## REQUISITOS MÍNIMOS
- Linux Ubuntu 14.04 (Kernel 3.13) 64-bit [Se recomienda Kubuntu 18.04]
- Drivers Open-Source (Mesa)

## ¿CÓMO EJECUTAR?
1. Establecer permisos de ejecución: `chmod +x monitor-prime_app-indicator.py`
1. Ejecutar en un terminal: `./monitor-prime_app-indicator.py`
1. Ingresar la contraseña del sistema (en el terminal) cuando se solicite.

## LISTA DE CAMBIOS
- (v0.2.3) [21/09/2018] Lanzamiento inicial.
- (v0.2.6) [06/07/2019] Se cambió el nombre del menú "Estado" a "Estado de GPU".
- (v0.2.6) [06/07/2019] Se añadió el menú "Aplicaciones en dGPU". Ahora se obtiene una notificación con el PID y el nombre del proceso en el dGPU.
- (v0.2.6) [06/07/2019] Se añadió el menú "Informacion de GPUs". Ahora se obtiene un archivo de texto con la información de ambos GPUs, el archivo se abre automáticamente con kate.
- (v0.2.6) [06/07/2019] Se creó la carpeta "imgs" para almacenar las imágenes utilizadas.
- (v0.2.6) [06/07/2019] Se creó la carpeta "txts" para almacenar los archivos de salida.
- (v0.2.6) [06/07/2019] Se realizaron muchas optimizaciones al código

## ENLACES DE INTERÉS
- Se muestra un ejemplo de su uso en [NotebookGPU](https://notebookgpu.blogspot.com/2018/10/verificar-el-estado-y-configurar.html)
