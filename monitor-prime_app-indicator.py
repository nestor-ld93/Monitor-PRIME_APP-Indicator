#!/usr/bin/env python
# MONITOR_PRIME_v0.2.3
# Copyleft: quantum-phy (Nestor), 21/09/2018

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

# Requisito:
# sudo apt install gir1.2-appindicator3-0.1
# sudo apt install mesa-utils

import os.path
import signal
import subprocess

from gi.repository import Gtk as gtk
from gi.repository import AppIndicator3 as appindicator
from gi.repository import Notify as notify


APPINDICATOR_ID = 'MONITOR_PRIME'

def main():
    indicator = appindicator.Indicator.new(APPINDICATOR_ID, os.path.abspath('video-card.svg'), appindicator.IndicatorCategory.SYSTEM_SERVICES)
    indicator.set_status(appindicator.IndicatorStatus.ACTIVE)
    indicator.set_menu(build_menu())
    notify.init(APPINDICATOR_ID)
    gtk.main()

def build_menu():
    menu = gtk.Menu()
    item_state = gtk.MenuItem('Estado')
    item_state.connect('activate', notificacion_estado)
    menu.append(item_state)
    item_quit = gtk.MenuItem('Salir')
    item_quit.connect('activate', quit)
    menu.append(item_quit)
    menu.show_all()
    return menu

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
    archivo  = 'info_gpus.txt'

    if (os.path.exists(archivo)):
        mostrar_info_GPU(archivo)
    else:
        escribir_info_archivo(comando1,archivo)
        escribir_info_archivo(comando2,archivo)
        escribir_info_archivo(comando3,archivo)
        escribir_info_archivo('echo',archivo)
        escribir_info_archivo(comando4,archivo)
        escribir_info_archivo(comando5,archivo)
        escribir_info_archivo(comando6,archivo)
        mostrar_info_GPU(archivo)
    
    if(output[0]>=0):
        notify.Notification.new('GPU renderizador: iGPU', mostrar_info_GPU(archivo)[0], os.path.abspath(mostrar_info_GPU(archivo)[2])).show()
    else:
        if(output[1]>=0):
            notify.Notification.new('GPU renderizador: dGPU', mostrar_info_GPU(archivo)[1], os.path.abspath(mostrar_info_GPU(archivo)[3])).show()

def mostrar_info_GPU(archivo):
    output0 = buscar_info_archivo(0,archivo)
    if(output0[0]>=0):
        texto0 = output0[5]
        logo0 = 'Intel-logo.svg'
    else:
        if(output0[1]>=0 or output0[2]>=0):
            texto0 = output0[5]
            logo0 = 'AMD_Radeon_graphics_logo_2016.svg'
            
    output1 = buscar_info_archivo(4,archivo)
    if(output1[1]>=0 or output1[2]>=0):
        texto1 = output0[6]
        logo1 = 'AMD_Radeon_graphics_logo_2016.svg'
    else:
        if(output1[3]>=0 or output1[4]>=0):
            texto1 = output0[6]
            logo1 = 'Nvidia-Geforce-GTX.svg'
    return texto0, texto1, logo0, logo1

def escribir_info_archivo(comando,archivo):
    process = subprocess.Popen(comando, stdout=subprocess.PIPE, stderr=None, shell=True)
    output = process.communicate()
    
    archivo = open(archivo,'a')
    archivo.write(output[0])
    archivo.close()
    return

def buscar_info_archivo(i,archivo):
    archivo = open(archivo,'r')
    linea = archivo.readlines()
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
