# MONITOR PRIME APP INDICATOR
APP indicator para usuarios de computadoras portátiles equipados con GPUs híbridos (Intel+AMD, AMD+AMD, Intel+Nvidia). **Su función principal es mostrar el GPU renderizador** cuando se le indique.
Está programado en Python, fue probado en Kubuntu 18.04/20.04 LTS, Linux Mint 20, KDE Neon 18.04/20.04 y MX Linux 19.3, pero nada impide su aplicación para otros entornos y versiones superiores.

Las funciones que realiza **MONITOR PRIME APP INDICATOR** son las siguientes:

- Muestra el "Estado de GPU" (GPU renderizador)
- Muestra las "Aplicaciones en dGPU" (PID y Nombre del proceso)
- Muestra la "Información de GPUs" (VRAM, driver (en uso y compatibles), versión (OpenGL y drivers), etc.)
- Permite la selección del iGPU Intel o dGPU NVIDIA (Driver privativo Nvidia Prime)
- Permite la selección de NVIDIA Optimus (On-Demand) si se encuentra disponible (Driver privativo Nvidia Prime 435.17 o superior y una versión de X.Org X server compatible)

## IMÁGENES PRINCIPALES (en KDE Plasma)

![app menu](https://lh3.googleusercontent.com/-34K7l-gINr0/X77Wg3Ie-BI/AAAAAAAABak/nEIMtBlNSg8U0w4Kw8lF--uskhMA2iUuwCLcBGAsYHQ/h195/Menu_mesa-prime_nvidia_prime_02.png "Menú principal y sus opciones para PRIME y Nvidia Prime")

![app menu](https://lh3.googleusercontent.com/-Zh8pSgTydfs/XgkeZkQVv0I/AAAAAAAAA5Q/1hBx26ZX8jUjc6PFKqb8OodVLn8J0_CcwCLcBGAsYHQ/h291/Apps_Nvidia.png "Aplicaciones renderizadas en el dGPU")

![app menu](https://lh3.googleusercontent.com/-e6td_2jdSiI/XgkeZmaNRII/AAAAAAAAA5Y/2z1bwjYEZHIKNHPN_XImB_WEzSCUfxaYgCLcBGAsYHQ/h177/Estado_Intel-AMD_OpenSource.png "Estado de GPU con drivers Open-Source")

![app menu](https://lh3.googleusercontent.com/-ARgkCEQ5XUc/XgkearIyYJI/AAAAAAAAA5g/DJR4rURDRxQ9CB0yHdD2PA-j5FPbig5TwCLcBGAsYHQ/h159/Estado_Intel_Nvidia_Nvidia-Prime.png "Estado de GPU con drivers Privativos: Nvidia Prime")

![app menu](https://lh3.googleusercontent.com/-Y1huKeDsSLA/X6h74-WH_JI/AAAAAAAABXs/2xziSyzOheYJmLbO5LKFVAg_w0R74Dx6wCLcBGAsYHQ/h412/Info_gpus.png "Información de GPUs: Nvidia Prime")

## DEPENDENCIAS
- gir1.2-appindicator3-0.1 (sudo apt install gir1.2-appindicator3-0.1)
- gir1.2-gtk-3.0 (sudo apt install gir1.2-gtk-3.0)
- gir1.2-notify-0.7 (sudo apt install gir1.2-notify-0.7)
- python-dbus (sudo apt install python-dbus)
- python-gi (sudo apt install python-gi)
- mesa-utils (sudo apt install mesa-utils)

## REQUISITOS MÍNIMOS
- Linux Ubuntu 14.04 (Kernel 3.13) 64-bit [Se recomienda una distribución con KDE Plasma 5.17 o superior]
- Drivers Open-Source (Mesa) para GPUs Intel, AMD & Nvidia
- Driver Privativos (Nvidia-Prime) para GPUs Nvidia

## ¿CÓMO DESCARGAR?
- Para obtener la última versión estable, descargue desde la pestaña [[Releases](https://github.com/nestor-ld93/Monitor-PRIME_APP-Indicator/releases)].
- Para obtener la última versión candidata a estable, descargue desde el botón [Code] o ejecute en un terminal:
`git clone https://github.com/nestor-ld93/Monitor-PRIME_APP-Indicator`

## ¿CÓMO EJECUTAR?
1. Ingresar a la carpeta clonada: `cd Monitor-PRIME_APP-Indicator`
1. Establecer permisos de ejecución: `chmod +x monitor-prime_app-indicator.py`
1. Ejecutar (no ingresar como superusuario): `./monitor-prime_app-indicator.py`
1. Ingresar la contraseña del sistema (en el terminal o en una ventana) cuando se solicite.

## ENLACES DE INTERÉS
- Se muestra un ejemplo de su uso en [NotebookGPU](https://notebookgpu.blogspot.com/2018/10/verificar-el-estado-y-configurar.html)
