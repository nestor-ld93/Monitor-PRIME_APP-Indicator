# MONITOR PRIME APP INDICATOR
Este es un APP indicator para usuarios de computadoras portátiles equipados con GPUs híbridos (Intel+AMD, AMD+AMD, Intel+Nvidia). **Su función principal es mostrar el GPU renderizador** cuando se le indique.
Está programado en Python, fue probado en Kubuntu 18.04 LTS y KDE Neon 5.16, pero nada impide su aplicación para otros entornos y versiones superiores a Ubuntu 14.04 LTS.

Las funciones que realiza **MONITOR PRIME APP INDICATOR** son las siguientes:

- Muestra el "Estado de GPU" (GPU renderizador)
- Muestra las "Aplicaciones en dGPU" (PID y Nombre del proceso)
- Muestra la "Información de GPUs" (Vendor, Device, VRAM, etc.)
- Permite la selección del iGPU Intel o dGPU NVIDIA (Driver privativo Nvidia Prime)
- Permite la selección de NVIDIA Optimus (On-Demand) si está disponible (Driver privativo Nvidia Prime 435.17 o superior y una versión de X.Org X server compatible)

## IMÁGENES PRINCIPALES (en KDE Neon 5.17)

![app menu](https://lh3.googleusercontent.com/-tAxNuxCPQvQ/XgkeayBPnTI/AAAAAAAAA5k/Pl5qB52-IycZwZDirIT_yMSNLcpESnv-QCLcBGAsYHQ/h195/Menu_mesa-prime_nvidia_prime.png "Menú principal y sus opciones para PRIME y Nvidia Prime")

![app menu](https://lh3.googleusercontent.com/-Zh8pSgTydfs/XgkeZkQVv0I/AAAAAAAAA5Q/1hBx26ZX8jUjc6PFKqb8OodVLn8J0_CcwCLcBGAsYHQ/h291/Apps_Nvidia.png "Aplicaciones renderizadas en el dGPU")

![app menu](https://lh3.googleusercontent.com/-e6td_2jdSiI/XgkeZmaNRII/AAAAAAAAA5Y/2z1bwjYEZHIKNHPN_XImB_WEzSCUfxaYgCLcBGAsYHQ/h177/Estado_Intel-AMD_OpenSource.png "Estado de GPU con drivers Open-Source")

![app menu](https://lh3.googleusercontent.com/-ARgkCEQ5XUc/XgkearIyYJI/AAAAAAAAA5g/DJR4rURDRxQ9CB0yHdD2PA-j5FPbig5TwCLcBGAsYHQ/h159/Estado_Intel_Nvidia_Nvidia-Prime.png "Estado de GPU con drivers Privativos: Nvidia Prime")

## DEPENDENCIAS
- gir1.2-appindicator3-0.1 (sudo apt install gir1.2-appindicator3-0.1)
- mesa-utils (sudo apt install mesa-utils)
- kate (sudo apt install kate)

## REQUISITOS MÍNIMOS
- Linux Ubuntu 14.04 (Kernel 3.13) 64-bit [Se recomienda Kubuntu 18.04 o superior]
- Drivers Open-Source (Mesa) para GPUs Intel, AMD & Nvidia
- Driver Privativos (Nvidia-Prime) para GPUs Nvidia

## ¿CÓMO DESCARGAR?
- Para obtener la última versión estable, descargue desde la pestaña "releases".
- Para obtener la última versión candidata a estable, descargue desde el botón "Clone or download" o ejecute en un terminal:
`git clone https://github.com/quantum-phy/Monitor-PRIME_APP-Indicator`

## ¿CÓMO EJECUTAR?
1. Establecer permisos de ejecución: `chmod +x monitor-prime_app-indicator.py`
1. Ejecutar en un terminal: `./monitor-prime_app-indicator.py`
1. Ingresar la contraseña del sistema (en el terminal o en una ventana) cuando se solicite.

## LISTA DE CAMBIOS
- (v0.2.3) [21/09/2018] Lanzamiento inicial.
- (v0.2.6) [06/07/2019] Se cambió el nombre del menú "Estado" a "Estado de GPU".
- (v0.2.6) [06/07/2019] Se añadió el menú "Aplicaciones en dGPU". Ahora se obtiene una notificación con el PID y el nombre del proceso en el dGPU.
- (v0.2.6) [06/07/2019] Se añadió el menú "Informacion de GPUs". Ahora se obtiene un archivo de texto con la información de ambos GPUs, el archivo se abre automáticamente con kate.
- (v0.2.6) [06/07/2019] Se creó la carpeta "imgs" para almacenar las imágenes utilizadas.
- (v0.2.6) [06/07/2019] Se creó la carpeta "txts" para almacenar los archivos de salida.
- (v0.2.6) [06/07/2019] Se realizaron muchas optimizaciones al código.
- (v0.2.8) [24/12/2019] Se añadió soporte para Nvidia Prime.
- (v0.2.8) [24/12/2019] El menú "Aplicaciones en dGPU" es reemplazado por "NVIDIA SMI" para Nvidia Prime.
- (v0.2.8) [24/12/2019] Se realizaron muchas optimizaciones al código.
- (v0.3.1) [25/12/2019] El menú "Aplicaciones en dGPU" se encuentra de regreso pero desactivado para Nvidia Prime.
- (v0.3.1) [25/12/2019] Se agregaron las 03 opciones disponibles de prime-select dentro del menú "Nvidia Prime".
- (v0.3.1) [25/12/2019] Al seleccionar Intel, NVIDIA o NVIDIA Optimus; aparecerá una ventana solicitando permisos de superusuario.
- (v0.3.1) [25/12/2019] La opción "NVIDIA Optimus (Demandado)" se encontrará habilitada únicamente en los equipos que lo soporten. Revisar: [Chapter 35. PRIME Render Offload](https://download.nvidia.com/XFree86/Linux-x86_64/435.21/README/primerenderoffload.html).
- (v0.3.1) [25/12/2019] Se anadió el menú "Acerca".
- (v0.3.1) [25/12/2019] Se realizaron muchas optimizaciones al código.
- (v0.3.2) [26/12/2019] Se añadió codificación UTF-8.
- (v0.3.2) [26/12/2019] El menú "NVIDIA Prime" se muestra con los drivers Mesa pero el primero se encuentra desactivado.
- (v0.3.2) [26/12/2019] Se corrigió un bug que no permitía la visualización de las aplicaciones en el dGPU (PRIME) si la instalación de GNU/Linux se encontraba en un idioma distinto al español.
- (v0.3.2) [26/12/2019] Cambios menores en la ventana "Acerca".
- (v0.3.3) [29/12/2019] Se añadió la característica "Aplicaciones en dGPU" para Nvidia Prime On-Demand (Nvidia Optimus).
- (v0.3.3) [29/12/2019] Correcciones menores.

## ENLACES DE INTERÉS
- Se muestra un ejemplo de su uso en [NotebookGPU](https://notebookgpu.blogspot.com/2018/10/verificar-el-estado-y-configurar.html)
