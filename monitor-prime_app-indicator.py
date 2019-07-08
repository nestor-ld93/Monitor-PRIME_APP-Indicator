#!/usr/bin/env python
#=========================================================================
# MONITOR PRIME - APP INDICATOR v0.2.6
# Copyleft: quantum-phy (Nestor), 06/07/2019
#=========================================================================

#This program is free software: you can redistribute it and/or modify
#it under the terms of the GNU General Public License as published by
#the Free Software Foundation, either version 3 of the License, or
#(at your option) any later version.

#This program is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU General Public License for more details.

#You should have received a copy of the GNU General Public License
#along with this program.  If not, see <https://www.gnu.org/licenses/>.

#=========================================================================
# DEPENDENCIAS:
# - gir1.2-appindicator3-0.1 (sudo apt install gir1.2-appindicator3-0.1)
# - mesa-utils (sudo apt install mesa-utils)
# - kate (sudo apt install kate)
#=========================================================================
#=========================================================================
# REQUISITOS MINIMOS:
# - Linux Ubuntu 14.04 (Kernel 3.13) 64-bit [Se recomienda Kubuntu 18.04]
# - Drivers Open-Source (Mesa)
#=========================================================================

import os.path
import signal
import subprocess

from gi.repository import Gtk as gtk
from gi.repository import AppIndicator3 as appindicator
from gi.repository import Notify as notify

APPINDICATOR_ID = 'MONITOR PRIME - APP INDICATOR'
IMG_video_card = 'imgs/video-card.svg'
IMG_intel_logo = 'imgs/Intel-logo.svg'
IMG_amd_radeon_logo = 'imgs/AMD_Radeon_graphics_logo_2016.svg'
IMG_nvidia_geforce_logo = 'imgs/Nvidia-Geforce-GTX.svg'
archivo_info_gpus = 'txts/info_gpus.txt'
archivo_info_gpus_full = 'txts/info_gpus_full.txt'
archivo_PID = 'txts/PID_process.txt'
editor_texto = "kate"

def main():
    indicator = appindicator.Indicator.new(APPINDICATOR_ID, os.path.abspath(IMG_video_card), appindicator.IndicatorCategory.SYSTEM_SERVICES)
    indicator.set_status(appindicator.IndicatorStatus.ACTIVE)
    indicator.set_menu(build_menu())
    notify.init(APPINDICATOR_ID)
    gtk.main()

def build_menu():
    menu = gtk.Menu()
    item_state = gtk.MenuItem('Estado de GPU')
    item_state.connect('activate', notificacion_estado)
    menu.append(item_state)
    
### NUEVO!!!!!!!!!!!! (06/07/2019)
    item_apps_dGPU = gtk.MenuItem('Aplicaciones en dGPU')
    item_apps_dGPU.connect('activate', notificacion_apps_dGPU)
    menu.append(item_apps_dGPU)
    
    item_info_full_GPU = gtk.MenuItem('Informacion de GPUs')
    item_info_full_GPU.connect('activate', info_full_GPU)
    menu.append(item_info_full_GPU)
### NUEVO!!!!!!!!!!!! (06/07/2019)
    
    item_quit = gtk.MenuItem('Salir')
    item_quit.connect('activate', quit)
    menu.append(item_quit)
    menu.show_all()
    return menu

### NUEVO!!!!!!!!!!!! (06/07/2019)

def info_full_GPU(_):
    comando_info1 = "glxinfo -B"
    comando_info2 = "DRI_PRIME=1 glxinfo -B"
    comando_del = "rm "
    comando_del += archivo_info_gpus_full
    separador = "echo '============================================================'"
    cabecero1 = "echo 'INFO. iGPU'"
    cabecero2 = "echo 'INFO. dGPU'"
    
    if (os.path.exists(archivo_info_gpus_full)):
        process = subprocess.Popen(comando_del, stdout=subprocess.PIPE, stderr=None, shell=True)
        
        escribir_info_archivo(separador,archivo_info_gpus_full)
        escribir_info_archivo(cabecero1,archivo_info_gpus_full)
        escribir_info_archivo(separador,archivo_info_gpus_full)
        escribir_info_archivo(comando_info1,archivo_info_gpus_full)
        escribir_info_archivo(separador,archivo_info_gpus_full)
        escribir_info_archivo(separador,archivo_info_gpus_full)
        escribir_info_archivo(cabecero2,archivo_info_gpus_full)
        escribir_info_archivo(separador,archivo_info_gpus_full)
        escribir_info_archivo(comando_info2,archivo_info_gpus_full)
        escribir_info_archivo(separador,archivo_info_gpus_full)
        process = subprocess.Popen(editor_texto+" "+archivo_info_gpus_full, stdout=subprocess.PIPE, stderr=None, shell=True)
        
    else:
        escribir_info_archivo(separador,archivo_info_gpus_full)
        escribir_info_archivo(cabecero1,archivo_info_gpus_full)
        escribir_info_archivo(separador,archivo_info_gpus_full)
        escribir_info_archivo(comando_info1,archivo_info_gpus_full)
        escribir_info_archivo(separador,archivo_info_gpus_full)
        escribir_info_archivo(separador,archivo_info_gpus_full)
        escribir_info_archivo(cabecero2,archivo_info_gpus_full)
        escribir_info_archivo(separador,archivo_info_gpus_full)
        escribir_info_archivo(comando_info2,archivo_info_gpus_full)
        escribir_info_archivo(separador,archivo_info_gpus_full)
        process = subprocess.Popen(editor_texto+" "+archivo_info_gpus_full, stdout=subprocess.PIPE, stderr=None, shell=True)
    return

def notificacion_apps_dGPU(_):
    comando1 = "ps -eo pid"
    comando_del = "rm "
    comando_del += archivo_PID
    
    if (os.path.exists(archivo_PID)):
        process = subprocess.Popen(comando_del, stdout=subprocess.PIPE, stderr=None, shell=True)
        escribir_info_archivo(comando1,archivo_PID)
    else:
        escribir_info_archivo(comando1,archivo_PID)
    
    [output2, PID_and_name] = buscar_PRIME_archivo(archivo_PID)
    mostrar_PRIME_dGPU(output2,PID_and_name)
    return

def buscar_PRIME_archivo(archivo_info_gpus):
    archivo = open(archivo_info_gpus,'r')
    linea = archivo.readlines()
    n = len(linea)
    archivo.close()
    
    i = 122
    output2 = -1
    PID_and_name=""
    while i<n:
        PID1 = int(linea[i])
        comando2 = "sudo grep -i DRI_PRIME=1 /proc/"
        comando2 += str(PID1)
        comando2 += "/environ"
        
        if (os.path.exists("/proc/"+str(PID1)+"/environ")):
            process = subprocess.Popen(comando2, stdout=subprocess.PIPE, stderr=None, shell=True)
            linea_salida = str(process.communicate())
            output1 = linea_salida.find("Coincidencia")
                
            if (output1>=0):
                output2 = output1
                PID2 = PID1
                
                comando3 = "ps -p "
                comando3 += str(PID2)
                comando3 += " -o comm="
                
                process = subprocess.Popen(comando3, stdout=subprocess.PIPE, stderr=None, shell=True)
                process_name = process.communicate()[0]
                PID_and_name = PID_and_name+str(PID2)+" - "+process_name
            else:
                if (output2<=0):
                    output2 = output1
        i = i + 1
    return output2, PID_and_name

def mostrar_PRIME_dGPU(output2,PID_and_name):
    if(output2>=0):
        notify.Notification.new('Aplicaciones renderizadas en el dGPU:', "|PID - NOMBRE DEL PROCESO|\n"+PID_and_name, os.path.abspath(mostrar_info_GPU(archivo_info_gpus)[3])).show()
    else:
        notify.Notification.new('Aplicaciones renderizadas en el dGPU:', 'Ninguna\n', os.path.abspath(mostrar_info_GPU(archivo_info_gpus)[3])).show()
    return
### NUEVO!!!!!!!!!!!! (06/07/2019)

def buscar_estado():
    command = 'sudo cat /sys/kernel/debug/vgaswitcheroo/switch'
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=None, shell=True)
    output = process.communicate()
    
    output1 = output[0].find("DynOff")
    output2 = output[0].find("DynPwr")
    return output1, output2

def notificacion_estado(_):
    output = buscar_estado()
    comando1 = 'glxinfo | grep "Vendor"'
    comando2 = 'glxinfo | grep "Device"'
    comando3 = 'lspci -v -s 00:02.0 | grep "Subsystem"'
    comando4 = 'DRI_PRIME=1 glxinfo | grep "Vendor"'
    comando5 = 'DRI_PRIME=1 glxinfo | grep "Device"'
    comando6 = 'lspci -v -s 01:00.0 | grep "Subsystem"'

    if (os.path.exists(archivo_info_gpus)):
        mostrar_info_GPU(archivo_info_gpus)
    else:
        escribir_info_archivo(comando1,archivo_info_gpus)
        escribir_info_archivo(comando2,archivo_info_gpus)
        escribir_info_archivo(comando3,archivo_info_gpus)
        escribir_info_archivo('echo',archivo_info_gpus)
        escribir_info_archivo(comando4,archivo_info_gpus)
        escribir_info_archivo(comando5,archivo_info_gpus)
        escribir_info_archivo(comando6,archivo_info_gpus)
        mostrar_info_GPU(archivo_info_gpus)
    
    if(output[0]>=0):
        notify.Notification.new('GPU renderizador: iGPU', mostrar_info_GPU(archivo_info_gpus)[0], os.path.abspath(mostrar_info_GPU(archivo_info_gpus)[2])).show()
    else:
        if(output[1]>=0):
            notify.Notification.new('GPU renderizador: dGPU', mostrar_info_GPU(archivo_info_gpus)[1], os.path.abspath(mostrar_info_GPU(archivo_info_gpus)[3])).show()

def mostrar_info_GPU(archivo_info_gpus):
    output0 = buscar_info_archivo(0,archivo_info_gpus)
    if(output0[0]>=0):
        texto0 = output0[5]
        logo0 = IMG_intel_logo
    else:
        if(output0[1]>=0 or output0[2]>=0):
            texto0 = output0[5]
            logo0 = IMG_amd_radeon_logo
            
    output1 = buscar_info_archivo(4,archivo_info_gpus)
    if(output1[1]>=0 or output1[2]>=0):
        texto1 = output0[6]
        logo1 = IMG_amd_radeon_logo
    else:
        if(output1[3]>=0 or output1[4]>=0):
            texto1 = output0[6]
            logo1 = IMG_nvidia_geforce_logo
    return texto0, texto1, logo0, logo1

def escribir_info_archivo(comando,archivo_info_gpus):
    process = subprocess.Popen(comando, stdout=subprocess.PIPE, stderr=None, shell=True)
    output = process.communicate()
    
    archivo = open(archivo_info_gpus,'a')
    archivo.write(output[0])
    archivo.close()
    return

def buscar_info_archivo(i,archivo_info_gpus):
    archivo = open(archivo_info_gpus,'r')
    linea = archivo.readlines()
    archivo.close()
    
    nombre_gpu0 = linea[2]
    nombre_gpu1 = linea[6]
    
    nombre_gpu0 = nombre_gpu0[12:]
    nombre_gpu1 = nombre_gpu1[12:]
    
    output1 = linea[i].find("8086") #Intel
    output2 = linea[i].find("1002") #AMD
    output3 = linea[i].find("1022") #AMD
    output4 = linea[i].find("10DE") #Nvidia
    output5 = linea[i].find("10de") #Nvidia
    return output1, output2, output3, output4, output5, nombre_gpu0, nombre_gpu1

def quit(_):
    notify.uninit()
    gtk.main_quit()

if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    main()
