#!/usr/bin/env python
# -*- coding: utf-8 -*-
#=========================================================================
# MONITOR PRIME - APP INDICATOR v0.3.3
# Copyleft: quantum-phy (Néstor), 29/12/2019
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
# - Drivers Open-Source (Mesa) para GPUs Intel, AMD & Nvidia
# - Driver Privativos (Nvidia-Prime) para GPUs Nvidia
#=========================================================================

import os.path
import signal
import subprocess

from gi.repository import Gtk as gtk
from gi.repository import AppIndicator3 as appindicator
from gi.repository import Notify as notify

__VERSION__ = '0.3.3'

APPINDICATOR_ID = 'MONITOR PRIME - APP INDICATOR'
archivo_prime_select = '/usr/bin/prime-select' #<=============== Para Nvidia Prime
archivo_mesa_prime = '/sys/kernel/debug/vgaswitcheroo/switch' #<=============== Para PRIME (Mesa)

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
    #if (os.path.exists(archivo_mesa_prime)): #<=============== Para PRIME (Mesa)
    driver = 'mesa_prime'
    #else:
    if (os.path.exists(archivo_prime_select)): #<=============== Para Nvidia Prime
        driver = 'nvidia_prime'
    indicator.set_menu(build_menu(driver))
    notify.init(APPINDICATOR_ID)
    gtk.main()

def build_menu(driver):
    menu = gtk.Menu()
    if (driver == 'mesa_prime'):
        item_state = gtk.MenuItem('Estado de GPU')
        item_state.connect('activate', notificacion_estado)
        menu.append(item_state)
        
        item_apps_dGPU = gtk.MenuItem('Aplicaciones en dGPU')
        item_apps_dGPU.connect('activate', notificacion_apps_dGPU)
        menu.append(item_apps_dGPU)
        
        #->>>>>>>>>>>
        submenu = gtk.Menu()
        menu_prime_select = gtk.MenuItem('NVIDIA Prime')
        menu_prime_select.set_sensitive(False)
        menu.append(menu_prime_select)
        menu_prime_select.set_submenu(submenu)
        
        item_igpu = gtk.MenuItem('')
        item_igpu.set_sensitive(False)
        submenu.append(item_igpu)
        #->>>>>>>>>>>
        
        item_info_full_GPU = gtk.MenuItem('Información de GPUs')
        item_info_full_GPU.connect('activate', info_full_GPU)
        menu.append(item_info_full_GPU)
    else:
        if (driver == 'nvidia_prime'):
            output_nvidia_select = Estado_Nvidia_Prime_Select()
            capacidad_on_demand = prime_select_capacidad_on_demand()
            
            item_state = gtk.MenuItem('Estado de GPU')
            item_state.connect('activate', Notificacion_estado_Nvidia_Prime)
            if (capacidad_on_demand == 'yes'):
                if (output_nvidia_select=='on-demand\n'):
                    item_state.set_sensitive(False)
            menu.append(item_state)
            
            item_apps_dGPU = gtk.MenuItem('Aplicaciones en dGPU')
            item_apps_dGPU.connect('activate', notificacion_apps_dGPU_Nvidia_optimus)
            if (capacidad_on_demand == 'no' or output_nvidia_select=='intel\n' or output_nvidia_select=='nvidia\n' or output_nvidia_select=='amd\n'):
                item_apps_dGPU.set_sensitive(False)
            menu.append(item_apps_dGPU)
            
            submenu = gtk.Menu()
            menu_prime_select = gtk.MenuItem('NVIDIA Prime')
            menu.append(menu_prime_select)
            menu_prime_select.set_submenu(submenu)
            
            ###############################NUEVO
            
            item_igpu = gtk.MenuItem('Intel (Modo Ahorro de energía)')
            item_igpu.connect('activate', prime_select_intel)
            if (output_nvidia_select=='intel\n'):
                item_igpu.set_sensitive(False)
            submenu.append(item_igpu)
            
            #if (output_nvidia_select=='amd\n'):
            #    item_igpu = gtk.MenuItem('AMD (Modo Ahorro de energia)')
            #    item_igpu.set_sensitive(False)
            #    item_igpu.connect('activate', prime_select_intel)
            #    submenu.append(item_igpu)
            
            item_nvidia = gtk.MenuItem('NVIDIA (Modo Rendimiento)')
            item_nvidia.connect('activate', prime_select_nvidia)
            if (output_nvidia_select=='nvidia\n'):
                item_nvidia.set_sensitive(False)
            submenu.append(item_nvidia)
            
            item_optimus = gtk.MenuItem('NVIDIA Optimus (Demandado)')
            item_optimus.connect('activate', prime_select_optimus)
            if (capacidad_on_demand == 'no'):
                item_optimus.set_sensitive(False)
            else:
                if (capacidad_on_demand == 'yes'):
                    if (output_nvidia_select=='on-demand\n'):
                        item_optimus.set_sensitive(False)
            submenu.append(item_optimus)
            
            ###############################NUEVO
            
            separador = gtk.SeparatorMenuItem()
            submenu.append(separador)
            
            item_nvidia_settings = gtk.MenuItem('NVIDIA X Server Settings')
            item_nvidia_settings.connect('activate', Nvidia_Prime_settings)
            #item_igpu = gtk.CheckMenuItem('Intel (Modo Ahorro de energia)')
            #item_igpu.set_active(True)
            submenu.append(item_nvidia_settings)
            
            item_nvidia_smi = gtk.MenuItem('NVIDIA SMI')
            item_nvidia_smi.connect('activate', Nvidia_Prime_smi)
            if (output_nvidia_select=='intel\n'):
                item_nvidia_smi.set_sensitive(False)
            #item_nvidia = gtk.CheckMenuItem('NVIDIA (Modo Rendimiento)')
            #item_nvidia.set_active(False)
            submenu.append(item_nvidia_smi)
            
            item_info_full_GPU = gtk.MenuItem('Información de GPUs')
            item_info_full_GPU.connect('activate', info_full_GPU_Nvidia_Prime)
            menu.append(item_info_full_GPU)
    
    separador = gtk.SeparatorMenuItem()
    menu.append(separador)
    
    item_acerca = gtk.MenuItem('Acerca')
    item_acerca.connect('activate', acerca)
    menu.append(item_acerca)
    
    item_quit = gtk.MenuItem('Salir')
    item_quit.connect('activate', quit)
    menu.append(item_quit)
    menu.show_all()
    return menu

def Nvidia_Prime_settings(_):
    comando1 = '/usr/bin/nvidia-settings'
    process = subprocess.Popen(comando1, stdout=subprocess.PIPE, stderr=None, shell=True)
    return

def Nvidia_Prime_smi(_):
    comando2 = 'nvidia-smi' 
    process = subprocess.Popen(comando2, shell=True)
    return

def prime_select_intel(_):
    output_nvidia_select = Estado_Nvidia_Prime_Select()
    comando1 = 'pkexec prime-select intel'
    process = subprocess.Popen(comando1, stdout=subprocess.PIPE, stderr=None, shell=True)
    notify.Notification.new('GPU Intel (Ahorro de energía) seleccionado:', "Para aplicar los cambios, se necesitan privilegios de superusuario y cerrar la sesión", os.path.abspath(mostrar_info_GPU_Nvidia_Prime(archivo_info_gpus)[2])).show()
    return

def prime_select_nvidia(_):
    output_nvidia_select = Estado_Nvidia_Prime_Select()
    comando1 = 'pkexec prime-select nvidia'
    process = subprocess.Popen(comando1, stdout=subprocess.PIPE, stderr=None, shell=True)
    notify.Notification.new('GPU NVIDIA (Rendimiento) seleccionado:', "Para aplicar los cambios, se necesitan privilegios de superusuario y cerrar la sesión", os.path.abspath(mostrar_info_GPU_Nvidia_Prime(archivo_info_gpus)[3])).show()
    return

def prime_select_optimus(_):
    output_nvidia_select = Estado_Nvidia_Prime_Select()
    comando1 = 'pkexec prime-select on-demand'
    process = subprocess.Popen(comando1, stdout=subprocess.PIPE, stderr=None, shell=True)
    notify.Notification.new('GPU NVIDIA (Optimus) seleccionado:', "Para aplicar los cambios, se necesitan privilegios de superusuario y cerrar la sesión", os.path.abspath(mostrar_info_GPU_Nvidia_Prime(archivo_info_gpus)[3])).show()
    return

def prime_select_capacidad_on_demand():
    comando = 'prime-select'
    process = subprocess.Popen(comando, stdout=subprocess.PIPE, stderr=None, shell=True)
    linea_salida = str(process.communicate())
    
    #output1 = linea_salida.find("nvidia")
    #output2 = linea_salida.find("intel")
    #output2 = linea_salida.find("amd")
    output3 = linea_salida.find("on-demand")
    #output4 = linea_salida.find("query")
    
    if (output3 >= 0):
        capacidad_on_demand = 'si'
    else:
        capacidad_on_demand = 'no'
    
    return capacidad_on_demand

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

def info_full_GPU_Nvidia_Prime(_): #<=============== Para Nvidia Prime
    output_nvidia_select = Estado_Nvidia_Prime_Select()
    comando_info1 = "glxinfo -B"
    comando_del = "rm "
    comando_del += archivo_info_gpus_full
    separador = "echo '============================================================'"
    
    if(output_nvidia_select=='intel\n' or output_nvidia_select=='amd\n'):
        cabecero = "echo 'INFO. iGPU'"
    else:
        if(output_nvidia_select=='nvidia\n'):
            cabecero = "echo 'INFO. dGPU'"
    
    if (os.path.exists(archivo_info_gpus_full)):
        process = subprocess.Popen(comando_del, stdout=subprocess.PIPE, stderr=None, shell=True)
        
        escribir_info_archivo(separador,archivo_info_gpus_full)
        escribir_info_archivo(cabecero,archivo_info_gpus_full)
        escribir_info_archivo(separador,archivo_info_gpus_full)
        escribir_info_archivo(comando_info1,archivo_info_gpus_full)
        escribir_info_archivo(separador,archivo_info_gpus_full)
        process = subprocess.Popen(editor_texto+" "+archivo_info_gpus_full, stdout=subprocess.PIPE, stderr=None, shell=True)
        
    else:
        escribir_info_archivo(separador,archivo_info_gpus_full)
        escribir_info_archivo(cabecero,archivo_info_gpus_full)
        escribir_info_archivo(separador,archivo_info_gpus_full)
        escribir_info_archivo(comando_info1,archivo_info_gpus_full)
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

def buscar_PRIME_archivo(archivo_PID):
    archivo = open(archivo_PID,'r')
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
            output1 = linea_salida.find("/proc/"+str(PID1)+"/environ")
            
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
###------------->>>>>>>>>
def notificacion_apps_dGPU_Nvidia_optimus(_): #<=============== Para Nvidia Prime
    comando1 = "ps -eo pid"
    comando_del = "rm "
    comando_del += archivo_PID
    
    if (os.path.exists(archivo_PID)):
        process = subprocess.Popen(comando_del, stdout=subprocess.PIPE, stderr=None, shell=True)
        escribir_info_archivo(comando1,archivo_PID)
    else:
        escribir_info_archivo(comando1,archivo_PID)
    
    [output2, PID_and_name] = buscar_Nvidia_optimus_archivo(archivo_PID)
    mostrar_Nvidia_optimus_dGPU(output2,PID_and_name)
    return

def buscar_Nvidia_optimus_archivo(archivo_PID):
    archivo = open(archivo_PID,'r')
    linea = archivo.readlines()
    n = len(linea)
    archivo.close()
    
    i = 122
    output2 = -1
    PID_and_name=""
    while i<n:
        PID1 = int(linea[i])
        comando2 = "sudo grep -i __NV_PRIME_RENDER_OFFLOAD=1 /proc/"
        comando2 += str(PID1)
        comando2 += "/environ"
        
        if (os.path.exists("/proc/"+str(PID1)+"/environ")):
            process = subprocess.Popen(comando2, stdout=subprocess.PIPE, stderr=None, shell=True)
            linea_salida = str(process.communicate())
            output1 = linea_salida.find("/proc/"+str(PID1)+"/environ")
            
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

def mostrar_Nvidia_optimus_dGPU(output2,PID_and_name):
    if(output2>=0):
        notify.Notification.new('Aplicaciones renderizadas en el dGPU:', "|PID - NOMBRE DEL PROCESO|\n"+PID_and_name, os.path.abspath(mostrar_info_GPU_Nvidia_Prime(archivo_info_gpus)[3])).show()
    else:
        notify.Notification.new('Aplicaciones renderizadas en el dGPU:', 'Ninguna\n', os.path.abspath(mostrar_info_GPU_Nvidia_Prime(archivo_info_gpus)[3])).show()
    return
###------------->>>>>>>>>

def buscar_estado():
    command  = 'sudo cat '
    command += archivo_mesa_prime
    process  = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=None, shell=True)
    output   = process.communicate()
    
    output1 = output[0].find("DynOff")
    output2 = output[0].find("DynPwr")
    return output1, output2

def Estado_Nvidia_Prime_Select(): #<=============== Para Nvidia Prime
    command = 'prime-select query'
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=None, shell=True)
    output_nvidia_select = process.communicate()[0]
    return output_nvidia_select

def Notificacion_estado_Nvidia_Prime(_): #<=============== Para Nvidia Prime
    output_nvidia_select = Estado_Nvidia_Prime_Select()
    
    comando1 = 'lspci -k | grep -A 2 -i "VGA"'
    
    if (os.path.exists(archivo_info_gpus)):
        if(output_nvidia_select=='intel\n' or output_nvidia_select=='amd\n'):
            notify.Notification.new('GPU renderizador [Mesa]: iGPU', mostrar_info_GPU_Nvidia_Prime(archivo_info_gpus)[0], os.path.abspath(mostrar_info_GPU_Nvidia_Prime(archivo_info_gpus)[2])).show()
        else:
            if(output_nvidia_select=='nvidia\n'):
                notify.Notification.new('GPU renderizador [Nvidia Prime]: dGPU', mostrar_info_GPU_Nvidia_Prime(archivo_info_gpus)[1], os.path.abspath(mostrar_info_GPU_Nvidia_Prime(archivo_info_gpus)[3])).show()
    
    else:
        escribir_info_archivo(comando1,archivo_info_gpus)
        if(output_nvidia_select=='intel\n' or output_nvidia_select=='amd\n'):
            notify.Notification.new('GPU renderizador [Mesa]: iGPU', mostrar_info_GPU_Nvidia_Prime(archivo_info_gpus)[0], os.path.abspath(mostrar_info_GPU_Nvidia_Prime(archivo_info_gpus)[2])).show()
        else:
            if(output_nvidia_select=='nvidia\n'):
                notify.Notification.new('GPU renderizador [Nvidia Prime]: dGPU', mostrar_info_GPU_Nvidia_Prime(archivo_info_gpus)[1], os.path.abspath(mostrar_info_GPU_Nvidia_Prime(archivo_info_gpus)[3])).show()
    
def notificacion_estado(_):
    output = buscar_estado()
    
    comando0 = 'glxinfo | grep "OpenGL renderer string"'
    comando1 = 'glxinfo | grep "Vendor"'
    comando2 = 'glxinfo | grep "Device"'
    comando3 = 'lspci -v -s 00:02.0 | grep "Subsystem"'
    comando4 = 'DRI_PRIME=1 glxinfo | grep "OpenGL renderer string"'
    comando5 = 'DRI_PRIME=1 glxinfo | grep "Vendor"'
    comando6 = 'DRI_PRIME=1 glxinfo | grep "Device"'
    comando7 = 'lspci -v -s 01:00.0 | grep "Subsystem"'
    
    if (os.path.exists(archivo_info_gpus)):
        if(output[0]>=0):
            notify.Notification.new('GPU renderizador [Mesa]: iGPU', mostrar_info_GPU(archivo_info_gpus)[0], os.path.abspath(mostrar_info_GPU(archivo_info_gpus)[2])).show()
        else:
            if(output[1]>=0):
                notify.Notification.new('GPU renderizador [Mesa]: dGPU', mostrar_info_GPU(archivo_info_gpus)[1], os.path.abspath(mostrar_info_GPU(archivo_info_gpus)[3])).show()
    
    else:
        escribir_info_archivo(comando0,archivo_info_gpus)
        escribir_info_archivo(comando1,archivo_info_gpus)
        escribir_info_archivo(comando2,archivo_info_gpus)
        escribir_info_archivo(comando3,archivo_info_gpus)
        escribir_info_archivo('echo',archivo_info_gpus)
        escribir_info_archivo(comando4,archivo_info_gpus)
        escribir_info_archivo(comando5,archivo_info_gpus)
        escribir_info_archivo(comando6,archivo_info_gpus)
        escribir_info_archivo(comando7,archivo_info_gpus)
        mostrar_info_GPU(archivo_info_gpus)
        
        if(output[0]>=0):
            notify.Notification.new('GPU renderizador [Mesa]: iGPU', mostrar_info_GPU(archivo_info_gpus)[0], os.path.abspath(mostrar_info_GPU(archivo_info_gpus)[2])).show()
        else:
            if(output[1]>=0):
                notify.Notification.new('GPU renderizador [Mesa]: dGPU', mostrar_info_GPU(archivo_info_gpus)[1], os.path.abspath(mostrar_info_GPU(archivo_info_gpus)[3])).show()
        
def mostrar_info_GPU(archivo_info_gpus):
    output0 = buscar_info_archivo(1,archivo_info_gpus)
    if(output0[0]>=0):
        texto0 = output0[5]
        logo0 = IMG_intel_logo
    else:
        if(output0[1]>=0 or output0[2]>=0):
            texto0 = output0[5]
            logo0 = IMG_amd_radeon_logo
    
    output1 = buscar_info_archivo(6,archivo_info_gpus)
    if(output1[1]>=0 or output1[2]>=0):
        texto1 = output0[6]
        logo1 = IMG_amd_radeon_logo
    else:
        if(output1[3]>=0 or output1[4]>=0):
            texto1 = output0[6]
            logo1 = IMG_nvidia_geforce_logo
    return texto0, texto1, logo0, logo1

def mostrar_info_GPU_Nvidia_Prime(archivo_info_gpus): #<=============== Para Nvidia Prime
    output0 = buscar_info_archivo_Nvidia_Prime(0,archivo_info_gpus)
    if(output0[0]>=0):
        texto0 = output0[5]
        logo0 = IMG_intel_logo
    else:
        if(output0[1]>=0 or output0[2]>=0):
            texto0 = output0[5]
            logo0 = IMG_amd_radeon_logo
    
    output1 = buscar_info_archivo_Nvidia_Prime(4,archivo_info_gpus)
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
    
    nombre_gpu0 = linea[0]
    nombre_gpu1 = linea[8]
    
    nombre_gpu0 = nombre_gpu0[29:]
    nombre_gpu1 = nombre_gpu1[12:]
    
    output1 = linea[i].find("8086") #Intel
    output2 = linea[i].find("1002") #AMD
    output3 = linea[i].find("1022") #AMD
    output4 = linea[i].find("10DE") #Nvidia
    output5 = linea[i].find("10de") #Nvidia
    return output1, output2, output3, output4, output5, nombre_gpu0, nombre_gpu1

def buscar_info_archivo_Nvidia_Prime(i,archivo_info_gpus): #<=============== Para Nvidia Prime
    archivo = open(archivo_info_gpus,'r')
    linea = archivo.readlines()
    archivo.close()
    
    nombre_gpu0 = linea[0]
    nombre_gpu1 = linea[5]
    
    nombre_gpu0 = nombre_gpu0[35:]
    nombre_gpu1 = nombre_gpu1[12:]
    
    output1 = linea[i].find("Intel") #Intel
    output2 = linea[i].find("AMD") #AMD
    output3 = linea[i].find("Radeon") #AMD
    output4 = linea[i].find("Nvidia") #Nvidia
    output5 = linea[i].find("NVIDIA") #Nvidia
    return output1, output2, output3, output4, output5, nombre_gpu0, nombre_gpu1

def acerca(_):
    autor = ["quantum-phy (Néstor)"]
    mensaje  = "App indicator que muestra el GPU renderizador, PID-Proceso en dGPU, información de GPUs "
    mensaje += "y selección de GPUs (Nvidia Prime) en portátiles con gráficos híbridos. "
    mensaje += "\n[Para Drivers Open-Source (Mesa) y/o Privativos (Nvidia-Prime)]"
    copyright = "2018-2019 - quantum-phy (Néstor)"
    licencia = "Licencia Pública General de GNU, versión 3"
    website = "https://github.com/quantum-phy/Monitor-PRIME_APP-Indicator"
    website_label = "Sitio web GitHub"
    
    about = gtk.AboutDialog()
    about.set_program_name(APPINDICATOR_ID)
    about.set_version("v."+__VERSION__)
    about.set_copyright(copyright)
    about.set_comments(mensaje)
    about.set_license(licencia)
    about.set_authors(autor)
    about.set_website(website)
    about.set_website_label(website_label)
    about.set_logo_icon_name(None)
    about.run()
    about.destroy()
    
    return

def quit(_):
    notify.uninit()
    gtk.main_quit()

if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    main()
