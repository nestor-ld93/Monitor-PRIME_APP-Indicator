#!/usr/bin/env python2
# -*- coding: utf-8 -*-
#==================================================================================
#   +==========================================================================+  #
#   |                    MONITOR PRIME - APP INDICATOR v0.4.5b                 |  #
#   +==========================================================================+  #
#   | -Ultima actualizacion: 26/11/2020                                        |  #
#   +--------------------------------------------------------------------------+  #
#   | -Copyright (C) 2020 NestorBase11 (quantum-phy)                           |  #
#   +--------------------------------------------------------------------------+  #
#==================================================================================

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
# - python-dbus (sudo apt install python-dbus)
# - python-gi (sudo apt install python-gi)
# - mesa-utils (sudo apt install mesa-utils)
#=========================================================================
#=========================================================================
# REQUISITOS MINIMOS:
# - Linux Ubuntu 14.04 (Kernel 3.13) 64-bit [Se recomienda Kubuntu 20.04]
# - Drivers Open-Source (Mesa) para GPUs Intel, AMD & Nvidia
# - Driver Privativos (Nvidia-Prime) para GPUs Nvidia
#=========================================================================

import os.path
import signal
import subprocess

from gi.repository import Gtk as gtk
from gi.repository import AppIndicator3 as appindicator
from gi.repository import Notify as notify
from gi.repository import GdkPixbuf

__VERSION__ = '0.4.5b'

APPINDICATOR_ID = 'MONITOR PRIME - APP INDICATOR'
archivo_prime_select = '/usr/bin/prime-select' #<=============== Para Nvidia Prime
archivo_mesa_prime = '/sys/kernel/debug/vgaswitcheroo/switch' #<=============== Para PRIME (Mesa)

IMG_video_card = 'imgs/video_card.svg'
IMG_intel_logo = 'imgs/Notificaciones/Intel_logo.svg'
IMG_amd_radeon_logo = 'imgs/Notificaciones/AMD_Radeon_graphics_logo_2016.svg'
IMG_nvidia_geforce_logo = 'imgs/Notificaciones/Nvidia_Geforce_logo.svg'

IMG_menu_acerca = 'imgs/Menus/Menu_acerca.svg'
IMG_menu_aplicaciones = 'imgs/Menus/Menu_aplicaciones.svg'
IMG_menu_cerrar = 'imgs/Menus/Menu_cerrar.svg'
IMG_menu_estado = 'imgs/Menus/Menu_estado.svg'
IMG_menu_info = 'imgs/Menus/Menu_info.svg'
IMG_menu_nvidia_prime = 'imgs/Menus/Menu_nvidia-prime.svg'
IMG_menu_nvidia_settings = 'imgs/Menus/Menu_nvidia-settings.svg'
IMG_menu_nvidia_smi = 'imgs/Menus/Menu_nvidia-smi.svg'
IMG_menu_select_intel = 'imgs/Menus/Menu_select-intel.svg'
IMG_menu_select_nvidia = 'imgs/Menus/Menu_select-nvidia.svg'
IMG_menu_select_on_demand = 'imgs/Menus/Menu_select-nvidia-on-demand.svg'

archivo_info_gpus = 'txts/info_gpus.txt'
archivo_param_gpus = 'txts/param_gpus.txt'
archivo_PID = 'txts/PID_process.txt'

name_intel_select = 'intel'
name_radeon_select = 'amd'
name_nvidia_select = 'nvidia'
name_demandado_select = 'on-demand'

def main():
    indicator = appindicator.Indicator.new(APPINDICATOR_ID, os.path.abspath(IMG_video_card), appindicator.IndicatorCategory.SYSTEM_SERVICES)
    indicator.set_status(appindicator.IndicatorStatus.ACTIVE)
    
    if (os.path.exists(archivo_info_gpus)==True): # Eliminar archivo de salida principal.
        os.remove(archivo_info_gpus)
    if (os.path.exists(archivo_param_gpus)==True): # Eliminar archivo de salida principal.
        os.remove(archivo_param_gpus)
    if (os.path.exists(archivo_PID)==True): # Eliminar archivo de salida principal.
        os.remove(archivo_PID)
    
    #if (os.path.exists(archivo_mesa_prime)==True): #<=============== Para PRIME (Mesa)
    driver = 'mesa_prime'
    #else:
    if (os.path.exists(archivo_prime_select)==True): #<=============== Para Nvidia Prime
        driver = 'nvidia_prime'
    indicator.set_menu(build_menu(driver))
    notify.init(APPINDICATOR_ID)
    gtk.main()

def build_menu(driver):
    menu = gtk.Menu()
    
    IMG_menu_acerca_gtk = gtk.Image()
    IMG_menu_acerca_gtk.set_from_file(IMG_menu_acerca)
    
    IMG_menu_aplicaciones_gtk = gtk.Image()
    IMG_menu_aplicaciones_gtk.set_from_file(IMG_menu_aplicaciones)
    
    IMG_menu_cerrar_gtk = gtk.Image()
    IMG_menu_cerrar_gtk.set_from_file(IMG_menu_cerrar)
    
    IMG_menu_estado_gtk = gtk.Image()
    IMG_menu_estado_gtk.set_from_file(IMG_menu_estado)
    
    IMG_menu_info_gtk = gtk.Image()
    IMG_menu_info_gtk.set_from_file(IMG_menu_info)
    
    IMG_menu_nvidia_prime_gtk = gtk.Image()
    IMG_menu_nvidia_prime_gtk.set_from_file(IMG_menu_nvidia_prime)
    
    IMG_menu_nvidia_settings_gtk = gtk.Image()
    IMG_menu_nvidia_settings_gtk.set_from_file(IMG_menu_nvidia_settings)
    
    IMG_menu_nvidia_smi_gtk = gtk.Image()
    IMG_menu_nvidia_smi_gtk.set_from_file(IMG_menu_nvidia_smi)
    
    IMG_menu_select_intel_gtk = gtk.Image()
    IMG_menu_select_intel_gtk.set_from_file(IMG_menu_select_intel)
    
    IMG_menu_select_nvidia_gtk = gtk.Image()
    IMG_menu_select_nvidia_gtk.set_from_file(IMG_menu_select_nvidia)
    
    IMG_menu_select_on_demand_gtk = gtk.Image()
    IMG_menu_select_on_demand_gtk.set_from_file(IMG_menu_select_on_demand)
    
    if (driver == 'mesa_prime'):
        #item_state = gtk.MenuItem('Estado de GPU')
        item_state = gtk.ImageMenuItem('Estado de GPU')
        item_state.set_image(IMG_menu_estado_gtk)
        item_state.connect('activate', notificacion_estado_PRIME)
        menu.append(item_state)
        
        #item_apps_dGPU = gtk.MenuItem('Aplicaciones en dGPU')
        item_apps_dGPU = gtk.ImageMenuItem('Aplicaciones en dGPU')
        item_apps_dGPU.set_image(IMG_menu_aplicaciones_gtk)
        item_apps_dGPU.connect('activate', mostrar_apps_dGPU_PRIME)
        menu.append(item_apps_dGPU)
        
        #->>>>>>>>>>>
        submenu = gtk.Menu()
        #menu_prime_select = gtk.MenuItem('NVIDIA Prime')
        menu_prime_select = gtk.ImageMenuItem('NVIDIA Prime')
        menu_prime_select.set_image(IMG_menu_nvidia_prime_gtk)
        menu_prime_select.set_sensitive(False)
        menu.append(menu_prime_select)
        menu_prime_select.set_submenu(submenu)
        
        item_igpu = gtk.MenuItem('')
        item_igpu.set_sensitive(False)
        submenu.append(item_igpu)
        #->>>>>>>>>>>
        
        #item_info_full_GPU = gtk.MenuItem('Información de GPUs')
        item_info_full_GPU = gtk.ImageMenuItem('Información de GPUs')
        item_info_full_GPU.set_image(IMG_menu_info_gtk)
        item_info_full_GPU.connect('activate', informacion_final_PRIME)
        menu.append(item_info_full_GPU)
    else:
        if (driver == 'nvidia_prime'):
            output_nvidia_select = Estado_Nvidia_Prime_Select()
            capacidad_on_demand = prime_select_capacidad_on_demand()
            
            #item_state = gtk.MenuItem('Estado de GPU')
            item_state = gtk.ImageMenuItem('Estado de GPU')
            item_state.set_image(IMG_menu_estado_gtk)
            item_state.connect('activate', Notificacion_estado_Nvidia_Prime)
            #if (capacidad_on_demand == 'si'):
            #    if (output_nvidia_select==name_demandado_select):
            #        item_state.set_sensitive(False)
            menu.append(item_state)
            
            #item_apps_dGPU = gtk.MenuItem('Aplicaciones en dGPU')
            item_apps_dGPU = gtk.ImageMenuItem('Aplicaciones en dGPU')
            item_apps_dGPU.set_image(IMG_menu_aplicaciones_gtk)
            item_apps_dGPU.connect('activate', mostrar_apps_dGPU_Nvidia_Prime)
            if (capacidad_on_demand == 'si'):
                if (output_nvidia_select == name_demandado_select):
                    item_apps_dGPU.set_sensitive(True)
                else:
                    if (output_nvidia_select== name_intel_select or output_nvidia_select==name_nvidia_select or output_nvidia_select==name_radeon_select):
                        item_apps_dGPU.set_sensitive(False)
            else:
                if (capacidad_on_demand == 'no'):
                    if (output_nvidia_select==name_intel_select or output_nvidia_select==name_nvidia_select or output_nvidia_select==name_radeon_select):
                        item_apps_dGPU.set_sensitive(False)
            menu.append(item_apps_dGPU)
            
            submenu = gtk.Menu()
            #menu_prime_select = gtk.MenuItem('NVIDIA Prime')
            menu_prime_select = gtk.ImageMenuItem('NVIDIA Prime')
            menu_prime_select.set_image(IMG_menu_nvidia_prime_gtk)
            menu.append(menu_prime_select)
            menu_prime_select.set_submenu(submenu)
            
            ###############################NUEVO
            
            #item_igpu = gtk.MenuItem('Intel (Modo Ahorro de energía)')
            item_igpu = gtk.ImageMenuItem('Intel (Modo Ahorro de energía)')
            item_igpu.set_image(IMG_menu_select_intel_gtk)
            item_igpu.connect('activate', prime_select_intel)
            if (output_nvidia_select==name_intel_select):
                item_igpu.set_sensitive(False)
            submenu.append(item_igpu)
            
            #if (output_nvidia_select==name_radeon_select):
            #    item_igpu = gtk.MenuItem('AMD (Modo Ahorro de energia)')
            #    item_igpu.set_sensitive(False)
            #    item_igpu.connect('activate', prime_select_intel)
            #    submenu.append(item_igpu)
            
            #item_nvidia = gtk.MenuItem('NVIDIA (Modo Rendimiento)')
            item_nvidia = gtk.ImageMenuItem('NVIDIA (Modo Rendimiento)')
            item_nvidia.set_image(IMG_menu_select_nvidia_gtk)
            item_nvidia.connect('activate', prime_select_nvidia)
            if (output_nvidia_select==name_nvidia_select):
                item_nvidia.set_sensitive(False)
            submenu.append(item_nvidia)
            
            #item_optimus = gtk.MenuItem('NVIDIA Optimus (Demandado)')
            item_optimus = gtk.ImageMenuItem('NVIDIA Optimus (Demandado)')
            item_optimus.set_image(IMG_menu_select_on_demand_gtk)
            item_optimus.connect('activate', prime_select_optimus)
            if (capacidad_on_demand == 'no'):
                item_optimus.set_sensitive(False)
            else:
                if (capacidad_on_demand == 'si'):
                    if (output_nvidia_select==name_demandado_select):
                        item_optimus.set_sensitive(False)
            submenu.append(item_optimus)
            
            ###############################NUEVO
            
            separador = gtk.SeparatorMenuItem()
            submenu.append(separador)
            
            #item_nvidia_settings = gtk.MenuItem('NVIDIA X Server Settings')
            item_nvidia_settings = gtk.ImageMenuItem('NVIDIA X Server Settings')
            item_nvidia_settings.set_image(IMG_menu_nvidia_settings_gtk)
            item_nvidia_settings.connect('activate', Nvidia_Prime_settings)
            #item_igpu = gtk.CheckMenuItem('Intel (Modo Ahorro de energia)')
            #item_igpu.set_active(True)
            submenu.append(item_nvidia_settings)
            
            #item_nvidia_smi = gtk.MenuItem('NVIDIA SMI')
            item_nvidia_smi = gtk.ImageMenuItem('NVIDIA SMI')
            item_nvidia_smi.set_image(IMG_menu_nvidia_smi_gtk)
            item_nvidia_smi.connect('activate', Nvidia_Prime_smi)
            if (output_nvidia_select==name_intel_select):
                item_nvidia_smi.set_sensitive(False)
            #item_nvidia = gtk.CheckMenuItem('NVIDIA (Modo Rendimiento)')
            #item_nvidia.set_active(False)
            submenu.append(item_nvidia_smi)
            
            #item_info_full_GPU = gtk.MenuItem('Información de GPUs')
            item_info_full_GPU = gtk.ImageMenuItem('Información de GPUs')
            item_info_full_GPU.set_image(IMG_menu_info_gtk)
            item_info_full_GPU.connect('activate', informacion_final_Nvidia_Prime)
            menu.append(item_info_full_GPU)
    
    separador = gtk.SeparatorMenuItem()
    menu.append(separador)
    
    #item_acerca = gtk.MenuItem('Acerca')
    item_acerca = gtk.ImageMenuItem('Acerca')
    item_acerca.set_image(IMG_menu_acerca_gtk)
    item_acerca.connect('activate', acerca)
    menu.append(item_acerca)
    
    #item_quit = gtk.MenuItem('Salir')
    item_quit = gtk.ImageMenuItem('Salir')
    item_quit.set_image(IMG_menu_cerrar_gtk)
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
    #cargar_archivos = texto_archivo_basico('nvidia_prime') # Para cargar el archivo de información.
    
    comando1 = 'pkexec prime-select'+' '+name_intel_select
    process = subprocess.Popen(comando1, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    process.wait()
    
    linea_salida = process.communicate()
    if (linea_salida[1] == ''):
        notify.Notification.new('OPERACIÓN REALIZADA:', "- Prime-select (antes): "+output_nvidia_select+" \n"+"- Prime-select (después): "+name_intel_select, os.path.abspath(IMG_video_card)).show()
        Dialogo_nvidia_prime(output_nvidia_select)
    else:
        notify.Notification.new('OPERACIÓN NO REALIZADA:', "- Prime-select (antes): "+output_nvidia_select+" \n"+"- Prime-select (después): "+output_nvidia_select, os.path.abspath(IMG_video_card)).show()        
    return

def prime_select_nvidia(_):
    output_nvidia_select = Estado_Nvidia_Prime_Select()
    #cargar_archivos = texto_archivo_basico('nvidia_prime') # Para cargar el archivo de información.
    
    comando1 = 'pkexec prime-select'+' '+name_nvidia_select
    process = subprocess.Popen(comando1, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    process.wait()
    
    linea_salida = process.communicate()
    if (linea_salida[1] == ''):
        notify.Notification.new('OPERACIÓN REALIZADA:', "- Prime-select (antes): "+output_nvidia_select+" \n"+"- Prime-select (después): "+name_nvidia_select, os.path.abspath(IMG_video_card)).show()
        Dialogo_nvidia_prime(output_nvidia_select)
    else:
        notify.Notification.new('OPERACIÓN NO REALIZADA:', "- Prime-select (antes): "+output_nvidia_select+" \n"+"- Prime-select (después): "+output_nvidia_select, os.path.abspath(IMG_video_card)).show()        
    return

def prime_select_optimus(_):
    output_nvidia_select = Estado_Nvidia_Prime_Select()
    #cargar_archivos = texto_archivo_basico('nvidia_prime') # Para cargar el archivo de información.
    
    comando1 = 'pkexec prime-select'+' '+name_demandado_select
    process = subprocess.Popen(comando1, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    process.wait()
    
    linea_salida = process.communicate()
    if (linea_salida[1] == ''):
        notify.Notification.new('OPERACIÓN REALIZADA:', "- Prime-select (antes): "+output_nvidia_select+" \n"+"- Prime-select (después): "+name_demandado_select, os.path.abspath(IMG_video_card)).show()
        Dialogo_nvidia_prime(output_nvidia_select)
    else:
        notify.Notification.new('OPERACIÓN NO REALIZADA:', "- Prime-select (antes): "+output_nvidia_select+" \n"+"- Prime-select (después): "+output_nvidia_select, os.path.abspath(IMG_video_card)).show()        
    return

def prime_select_capacidad_on_demand():
    comando = 'prime-select'
    process = subprocess.Popen(comando, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    linea_salida = str(process.communicate())
    
    #output1 = linea_salida.find("nvidia")
    #output2 = linea_salida.find("intel")
    #output2 = linea_salida.find("amd")
    output3 = linea_salida.find(name_demandado_select)
    #output4 = linea_salida.find("query")
    
    if (output3 >= 0):
        capacidad_on_demand = 'si'
    else:
        capacidad_on_demand = 'no'
    
    return capacidad_on_demand

def mostrar_apps_dGPU_PRIME(_):
    driver = 'mesa_prime'
    variable_entorno = 'DRI_PRIME=1'
    
    comando1 = "ps -eo pid"
    comando_del = "rm "
    comando_del += archivo_PID
    
    if (os.path.exists(archivo_PID)==True):
        process = subprocess.Popen(comando_del, stdout=subprocess.PIPE, stderr=None, shell=True)
        escribir_info_archivo(comando1,archivo_PID)
    else:
        escribir_info_archivo(comando1,archivo_PID)
    
    [output2, PID_and_name] = buscar_apps_dGPU_archivo(variable_entorno,archivo_PID)
    notificacion_apps_dGPU(driver,output2,PID_and_name)
    return

def mostrar_apps_dGPU_Nvidia_Prime(_):
    driver = 'nvidia_prime'
    variable_entorno = '__NV_PRIME_RENDER_OFFLOAD=1'
    
    comando1 = "ps -eo pid"
    comando_del = "rm "
    comando_del += archivo_PID
    
    if (os.path.exists(archivo_PID)==True):
        process = subprocess.Popen(comando_del, stdout=subprocess.PIPE, stderr=None, shell=True)
        escribir_info_archivo(comando1,archivo_PID)
    else:
        escribir_info_archivo(comando1,archivo_PID)
    
    [output2, PID_and_name] = buscar_apps_dGPU_archivo(variable_entorno,archivo_PID)
    notificacion_apps_dGPU(driver,output2,PID_and_name)
    return

def buscar_apps_dGPU_archivo(variable_entorno,archivo_PID):
    archivo = open(archivo_PID,'r')
    linea = archivo.readlines()
    n = len(linea)
    archivo.close()
    
    i = 122
    output2 = -1
    PID_and_name=""
    while i<n:
        PID1 = int(linea[i])
        comando2 = "sudo grep -i"+" "+variable_entorno+" "+"/proc/"
        comando2 += str(PID1)
        comando2 += "/environ"
        
        if (os.path.exists("/proc/"+str(PID1)+"/environ")==True):
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

def notificacion_apps_dGPU(driver,output2,PID_and_name):
    if (driver == 'mesa_prime'):
        cargar_archivos = texto_archivo_basico(driver) # Para cargar el archivo de información.
        if(output2>=0):
            notify.Notification.new('Aplicaciones renderizadas en el dGPU:', "|PID - NOMBRE DEL PROCESO|\n"+PID_and_name, os.path.abspath(mostrar_info_GPU(archivo_info_gpus)[3])).show()
        else:
            notify.Notification.new('Aplicaciones renderizadas en el dGPU:', 'Ninguna\n', os.path.abspath(mostrar_info_GPU(archivo_info_gpus)[3])).show()
    else:
        if (driver == 'nvidia_prime'):
            cargar_archivos = texto_archivo_basico(driver) # Para cargar el archivo de información.
            if(output2>=0):
                notify.Notification.new('Aplicaciones renderizadas en el dGPU:', "|PID - NOMBRE DEL PROCESO|\n"+PID_and_name, os.path.abspath(mostrar_info_GPU(archivo_info_gpus)[3])).show()
            else:
                notify.Notification.new('Aplicaciones renderizadas en el dGPU:', 'Ninguna\n', os.path.abspath(mostrar_info_GPU(archivo_info_gpus)[3])).show()
    return

def buscar_estado_PRIME():
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
    output_nvidia_select = output_nvidia_select.replace("\n","")
    return output_nvidia_select

def Notificacion_estado_Nvidia_Prime(_): #<=============== Para Nvidia Prime
    driver = 'nvidia_prime'
    output_nvidia_select = Estado_Nvidia_Prime_Select()
    cargar_archivos = texto_archivo_basico(driver) # Para cargar el archivo de información.
    
    if(output_nvidia_select==name_intel_select or output_nvidia_select==name_radeon_select):
        notify.Notification.new('[GPU renderizador] : iGPU', mostrar_info_GPU(archivo_info_gpus)[0], os.path.abspath(mostrar_info_GPU(archivo_info_gpus)[2])).show()
    else:
        if(output_nvidia_select==name_nvidia_select):
            notify.Notification.new('[GPU renderizador] : dGPU', mostrar_info_GPU(archivo_info_gpus)[1], os.path.abspath(mostrar_info_GPU(archivo_info_gpus)[3])).show()
        else:
            if(output_nvidia_select==name_demandado_select):
                notify.Notification.new('[GPU renderizador] : iGPU + dGPU', "- iGPU: "+mostrar_info_GPU(archivo_info_gpus)[0]+"\n"+"- dGPU: "+mostrar_info_GPU(archivo_info_gpus)[1], os.path.abspath(mostrar_info_GPU(archivo_info_gpus)[3])).show()
    
def notificacion_estado_PRIME(_):
    driver = 'mesa_prime'
    output = buscar_estado_PRIME()
    cargar_archivos = texto_archivo_basico(driver) # Para cargar el archivo de información.
    
    if(output[0]>=0):
        notify.Notification.new('[GPU renderizador] : iGPU', mostrar_info_GPU(archivo_info_gpus)[0], os.path.abspath(mostrar_info_GPU(archivo_info_gpus)[2])).show()
    else:
        if(output[1]>=0):
            notify.Notification.new('[GPU renderizador] : dGPU', mostrar_info_GPU(archivo_info_gpus)[1], os.path.abspath(mostrar_info_GPU(archivo_info_gpus)[3])).show()
    
def mostrar_info_GPU(archivo_info_gpus):
    archivo = open(archivo_info_gpus,'r')
    linea = archivo.readlines()
    archivo.close()
    
    [n_devices, id_igpu, id_dgpu, texto_igpu, texto_dgpu] = buscar_ids()
    
    nombre_gpu0 = linea[0]
    nombre_gpu0 = nombre_gpu0[9:]
    if (texto_igpu == 'intel'):
        logo_gpu0 = IMG_intel_logo
    else:
        if (texto_igpu == 'amd'):
            logo_gpu0 = IMG_amd_radeon_logo
    
    if (n_devices == 2):
        nombre_gpu1 = linea[6]
        nombre_gpu1 = nombre_gpu1[9:]
        if (texto_dgpu == 'amd'):
            logo_gpu1 = IMG_amd_radeon_logo
        else:
            if (texto_dgpu == 'nvidia'):
                logo_gpu1 = IMG_nvidia_geforce_logo
    else: # Este caso es un problema, pero es la programación más óptima que se me ocurrió.
        nombre_gpu1 = 'NaN'
        logo_gpu1 = 'NaN'
        
    return nombre_gpu0, nombre_gpu1, logo_gpu0, logo_gpu1

def escribir_info_archivo(comando,archivo_info_gpus):
    process = subprocess.Popen(comando, stdout=subprocess.PIPE, stderr=None, shell=True)
    output = process.communicate()
    
    archivo = open(archivo_info_gpus,'ab')
    archivo.write(output[0])
    archivo.close()
    return

def escribir_texto_archivo(texto,archivo_info_gpus):
    archivo = open(archivo_info_gpus,'wb')
    archivo.write(texto)
    archivo.close()

def acerca(_):
    autor = ["NestorBase11 (quantum-phy)"]
    mensaje  = "App indicator que muestra el GPU renderizador, PID-Proceso en dGPU, información de GPUs "
    mensaje += "y selección de GPUs (Nvidia Prime) en portátiles con gráficos híbridos. "
    mensaje += "\n[Para Drivers Open-Source (Mesa) y/o Privativos (Nvidia-Prime)]"
    copyright = "2018-2020 - NestorBase11 (quantum-phy)"
    licencia = "Licencia Pública General de GNU, versión 3"
    website = "https://github.com/nestor-ld93/Monitor-PRIME_APP-Indicator"
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
    about.set_logo(GdkPixbuf.Pixbuf.new_from_file_at_size(IMG_video_card,64,64))
    #about.set_logo_icon_name(None)
    about.run()
    about.destroy()
    
    return

def informacion_final_PRIME(_):
    driver = 'mesa_prime'
    titulo = "Información de GPUs [PRIME]"
    titulo_barra = APPINDICATOR_ID
    
    mensaje = texto_archivo_basico(driver)    

    dialog = gtk.MessageDialog(None, gtk.DialogFlags.MODAL, gtk.MessageType.INFO, gtk.ButtonsType.NONE, titulo)
    dialog.format_secondary_text(mensaje)
    dialog.set_deletable(False)
    dialog.set_title(titulo_barra)
    dialog.add_button("Aceptar", gtk.ResponseType.OK)
    response = dialog.run()
    dialog.destroy()
    return response

def informacion_final_Nvidia_Prime(_):
    driver = 'nvidia_prime'
    titulo = "Información de GPUs [Nvidia Prime]"
    titulo_barra = APPINDICATOR_ID
    
    output_nvidia_select = Estado_Nvidia_Prime_Select()
    mensaje = texto_archivo_basico(driver)
    
    dialog = gtk.MessageDialog(None, gtk.DialogFlags.MODAL, gtk.MessageType.INFO, gtk.ButtonsType.NONE, titulo)
    if(output_nvidia_select==name_demandado_select):
        dialog.format_secondary_text(mensaje+"\n\n"+"[Prime-Select]: "+output_nvidia_select+" (Demandado)")
    else:
        if(output_nvidia_select==name_intel_select or output_nvidia_select==name_radeon_select):
            dialog.format_secondary_text(mensaje+"\n\n"+"[Prime-Select]: "+output_nvidia_select+" (Modo Ahorro de energía)")
        else:
            if(output_nvidia_select==name_nvidia_select):
                dialog.format_secondary_text(mensaje+"\n\n"+"[Prime-Select]: "+output_nvidia_select+" (Modo Rendimiento)")
    
    dialog.set_deletable(False)
    dialog.set_title(titulo_barra)
    dialog.add_button("Aceptar", gtk.ResponseType.OK)
    response = dialog.run()
    dialog.destroy()
    return response

def Dialogo_nvidia_prime(output_nvidia_select):
    titulo = "Nvidia Prime-select"
    titulo_barra = APPINDICATOR_ID
    
    mensaje = "Cierre sesión del sistema para aplicar los cambios\n(reinicio recomendado)."
    
    dialog = gtk.MessageDialog(None, gtk.DialogFlags.MODAL, gtk.MessageType.INFO, gtk.ButtonsType.NONE, titulo)
    dialog.format_secondary_text(mensaje)
    dialog.set_deletable(False)
    dialog.set_title(titulo_barra)
    dialog.add_button("Aceptar", gtk.ResponseType.OK)
    response = dialog.run()
    dialog.destroy()
    return response

def texto_archivo_basico(driver):
    if (os.path.exists(archivo_info_gpus)==False):
        [nombre_gpu0, driver_use_gpu0, driver_comp_gpu0, driver_version_gpu0, VRAM_gpu0, nombre_gpu1, driver_use_gpu1, driver_comp_gpu1, driver_version_gpu1, VRAM_gpu1] = extraccion_info_gui(driver)

        mensaje  = "[GPU 0]: "+nombre_gpu0+"\n"
        mensaje += "\tVRAM (compartida): "+VRAM_gpu0+"\n"
        mensaje += "\tDriver (en uso): "+driver_use_gpu0+"\n"
        mensaje += "\tVersión (OpenGL y Driver): "+driver_version_gpu0+"\n"
        mensaje += "\tDriver (compatible): "+driver_comp_gpu0+"\n"
    
        mensaje += "\n"
        mensaje += "[GPU 1]: "+nombre_gpu1+"\n"
        mensaje += "\tVRAM (Dedicada): "+VRAM_gpu1+"\n"
        mensaje += "\tDriver (en uso): "+driver_use_gpu1+"\n"
        mensaje += "\tVersión (OpenGL y Driver): "+driver_version_gpu1+"\n"
        mensaje += "\tDriver (compatible): "+driver_comp_gpu1
        
        escribir_texto_archivo(mensaje,archivo_info_gpus)
    else:
        mensaje = open(archivo_info_gpus, 'r').read()
    
    return mensaje

def extraccion_info_gui(driver):
    [n_devices, id_igpu, id_dgpu, texto_igpu, texto_dgpu] = buscar_ids()
    
    comando_iGPU_01 = 'lspci -v -s'+' '+id_igpu+' '+'| grep "VGA compatible controller"' # Nombre más correcto.
    comando_iGPU_02 = 'lspci -v -s'+' '+id_igpu+' '+'| grep "Kernel driver in use"'
    comando_iGPU_03 = 'lspci -v -s'+' '+id_igpu+' '+'| grep "Kernel modules"'
    
    comando_dGPU_01 = 'lspci -v -s'+' '+id_dgpu+' '+'| grep "VGA compatible controller"' # Nombre más correcto.
    comando_dGPU_02 = 'lspci -v -s'+' '+id_dgpu+' '+'| grep "Kernel driver in use"'
    comando_dGPU_03 = 'lspci -v -s'+' '+id_dgpu+' '+'| grep "Kernel modules"'
    
    if (driver == 'nvidia_prime'):
        output_nvidia_select = Estado_Nvidia_Prime_Select()
        
        if(output_nvidia_select==name_demandado_select):
            ##comando_iGPU_01 = 'glxinfo -B | grep "OpenGL renderer string"'
            comando_iGPU_04 = 'glxinfo -B | grep "OpenGL version string"'
            comando_iGPU_05 = 'glxinfo -B | grep "Video memory"'
        
            variable_entorno = '__NV_PRIME_RENDER_OFFLOAD=1 __GLX_VENDOR_LIBRARY_NAME=nvidia'
            ##comando_dGPU_01 = variable_entorno+' '+'glxinfo -B | grep "OpenGL renderer string"'
            comando_dGPU_04 = variable_entorno+' '+'glxinfo -B | grep "OpenGL version string"'
            comando_dGPU_05 = variable_entorno+' '+'glxinfo -B | grep "Dedicated video memory"'
    
        else:        
            if(output_nvidia_select==name_intel_select or output_nvidia_select==name_radeon_select):
                ##comando_iGPU_01 = 'glxinfo -B | grep "OpenGL renderer string"'
                comando_iGPU_04 = 'glxinfo -B | grep "OpenGL version string"'
                comando_iGPU_05 = 'glxinfo -B | grep "Video memory"'
                
                ##comando_dGPU_01 = ''
                comando_dGPU_04 = ''
                comando_dGPU_05 = ''
                
            else:
                if(output_nvidia_select==name_nvidia_select):
                    ##comando_iGPU_01 = ''
                    comando_iGPU_04 = ''
                    comando_iGPU_05 = ''
                
                    comando_dGPU_04 = 'glxinfo -B | grep "OpenGL version string"'
                    comando_dGPU_05 = 'glxinfo -B | grep "Dedicated video memory"'
    else:
        if (driver == 'mesa_prime'):
            ##comando_iGPU_01 = 'lspci -v -s'+' '+id_igpu+' '+'| grep "DeviceName"' # Nombre más correcto.
            comando_iGPU_04 = 'glxinfo -B | grep "OpenGL version string"'
            comando_iGPU_05 = 'glxinfo -B | grep "Video memory"'
        
            variable_entorno = 'DRI_PRIME=1'
            ##comando_dGPU_01 = 'lspci -v -s'+' '+id_dgpu+' '+'| grep "DeviceName"' # Nombre más correcto.
            comando_dGPU_04 = variable_entorno+' '+'glxinfo -B | grep "OpenGL version string"'
            comando_dGPU_05 = variable_entorno+' '+'glxinfo -B | grep "Dedicated video memory"'
    
    comando_GPU0 = [comando_iGPU_01, comando_iGPU_02, comando_iGPU_03, comando_iGPU_04, comando_iGPU_05]
    salida_GPU0  = ['nombre_gpu0', 'driver_use_gpu0', 'driver_comp_gpu0', 'driver_version_gpu0', 'VRAM_gpu0']
    inicio_texto0 = [35, 23, 17, 23, 18]
    
    comando_GPU1 = [comando_dGPU_01, comando_dGPU_02, comando_dGPU_03, comando_dGPU_04, comando_dGPU_05]
    salida_GPU1  = ['nombre_gpu1', 'driver_use_gpu1', 'driver_comp_gpu1', 'driver_version_gpu1', 'VRAM_gpu1']
    inicio_texto1 = [35, 23, 17, 23, 28]
    
    n_comandos = len(comando_GPU0)
    
    i = 1
    while (i <= n_comandos):
        if (comando_GPU0[i-1] != ''):
            #print(i)
            process  = subprocess.Popen(comando_GPU0[i-1], stdout=subprocess.PIPE, stderr=None, shell=True)
            salida_GPU0[i-1] = process.communicate()[0]
            salida_GPU0[i-1] = salida_GPU0[i-1].replace("\n","")
            if (i == 1):
                ubicacion = salida_GPU0[i-1].find('(rev')    # Para prime-select = nvidia
                salida_GPU0[i-1] = salida_GPU0[i-1][inicio_texto0[i-1]:ubicacion] # Para prime-select = nvidia
                ubicacion = salida_GPU0[i-1].find('(prog')    # Para PRIME
                salida_GPU0[i-1] = salida_GPU0[i-1][:ubicacion] # Para PRIME
                salida_GPU0[i-1] = salida_GPU0[i-1].replace("Corporation ","")
                salida_GPU0[i-1] = salida_GPU0[i-1].replace("Advanced Micro Devices, Inc. ","")
            else:
                salida_GPU0[i-1] = salida_GPU0[i-1][inicio_texto0[i-1]:]
            #print(salida_GPU0[i-1])
            i = i + 1
        else:
            salida_GPU0[i-1] = 'NaN'
            #print(salida_GPU0[i-1])
            i = i + 1
    
    if (n_devices == 2):
        i = 1
        while (i <= n_comandos):
            if (comando_GPU1[i-1] != ''):
                #print(i)
                process  = subprocess.Popen(comando_GPU1[i-1], stdout=subprocess.PIPE, stderr=None, shell=True)
                salida_GPU1[i-1] = process.communicate()[0]
                salida_GPU1[i-1] = salida_GPU1[i-1].replace("\n","")
                if (i == 1):
                    ubicacion = salida_GPU1[i-1].find('(rev')    # Para prime-select = nvidia
                    salida_GPU1[i-1] = salida_GPU1[i-1][inicio_texto0[i-1]:ubicacion] # Para prime-select = nvidia
                    ubicacion = salida_GPU1[i-1].find('(prog')    # Para PRIME
                    salida_GPU1[i-1] = salida_GPU1[i-1][:ubicacion] # Para PRIME
                    salida_GPU1[i-1] = salida_GPU1[i-1].replace("Corporation ","")
                    salida_GPU1[i-1] = salida_GPU1[i-1].replace("Advanced Micro Devices, Inc. ","")
                else:
                    salida_GPU1[i-1] = salida_GPU1[i-1][inicio_texto1[i-1]:]
                #print(salida_GPU1[i-1])
                i = i + 1
            else:
                salida_GPU1[i-1] = 'NaN'
                #print(salida_GPU1[i-1])
                i = i + 1
    else:
        if (n_devices == 1):
            i = 1
            while (i <= n_comandos):
                #print(i)
                salida_GPU1[i-1] = 'NaN'
                #print(salida_GPU1[i-1])
                i = i + 1
    
    nombre_gpu0 = salida_GPU0[0]
    driver_use_gpu0 = salida_GPU0[1]
    driver_comp_gpu0 = salida_GPU0[2]
    driver_version_gpu0 = salida_GPU0[3]
    VRAM_gpu0 = salida_GPU0[4]
    
    nombre_gpu1 = salida_GPU1[0]
    driver_use_gpu1 = salida_GPU1[1]
    driver_comp_gpu1 = salida_GPU1[2]
    driver_version_gpu1 = salida_GPU1[3]
    VRAM_gpu1 = salida_GPU1[4]
    
    return nombre_gpu0, driver_use_gpu0, driver_comp_gpu0, driver_version_gpu0, VRAM_gpu0, nombre_gpu1, driver_use_gpu1, driver_comp_gpu1, driver_version_gpu1, VRAM_gpu1

def buscar_ids():
    if (os.path.exists(archivo_param_gpus)==False):
        comando = 'lspci -v | grep "VGA compatible controller"'
        process  = subprocess.Popen(comando, stdout=subprocess.PIPE, stderr=None, shell=True)
        salida_comando = process.communicate()[0]
        linea_salida = salida_comando.split("\n")
        n = len(linea_salida)
        n_devices = n - 1
    
        textos_igpu = ["Intel", "AMD", "Radeon"]
        textos_dgpu = ["AMD", "Radeon", "Nvidia", "NVIDIA"]
        output1 = -1
        i = 0
        while (output1 <= 0):
            output1 = linea_salida[0].find(textos_igpu[i])
            if (output1 >= 0):
                id_igpu = linea_salida[0][0:7]
                texto_igpu = textos_igpu[i]
            i += 1
    
        if (n_devices == 2):
            output2 = -1
            i = 0
            while (output2 <= 0):
                output2 = linea_salida[1].find(textos_dgpu[i])
                if (output2 >= 0):
                    id_dgpu = linea_salida[1][0:7]
                    texto_dgpu = textos_dgpu[i]
                i += 1
        else:
            id_dgpu = 'NaN'
            texto_dgpu = 'NaN'
    
        if (texto_igpu == "Intel"):
            texto_igpu = "intel"
        else:
            if (texto_igpu == "AMD" or texto_igpu == "Radeon"):
                texto_igpu = "amd"
    
        if (texto_dgpu == "AMD" or texto_dgpu == "Radeon"):
            texto_dgpu = "amd"
        else:
            if (texto_dgpu == "Nvidia" or texto_dgpu == "NVIDIA"):
                texto_dgpu = "nvidia"
        
        contenido_archivo  = 'N_devices = '+str(n_devices)+'\n'
        contenido_archivo += 'GPU0      = '+str(texto_igpu)+'\n'
        contenido_archivo += 'ID_GPU0   = '+str(id_igpu)+'\n'
        contenido_archivo += 'GPU1      = '+str(texto_dgpu)+'\n'
        contenido_archivo += 'ID_GPU1   = '+str(id_dgpu)
        
        escribir_texto_archivo(contenido_archivo,archivo_param_gpus)
    
    else:
        archivo = open(archivo_param_gpus,'r')
        linea = archivo.readlines()
        archivo.close()
        
        n_devices = linea[0]
        n_devices = n_devices[12:]
        n_devices = int(n_devices.replace("\n",""))
        
        texto_igpu = linea[1]
        texto_igpu = texto_igpu[12:]
        texto_igpu = texto_igpu.replace("\n","")
        
        id_igpu = linea[2]
        id_igpu = id_igpu[12:]
        id_igpu = id_igpu.replace("\n","")
        
        texto_dgpu = linea[3]
        texto_dgpu = texto_dgpu[12:]
        texto_dgpu = texto_dgpu.replace("\n","")
        
        id_dgpu = linea[4]
        id_dgpu = id_dgpu[12:]
        id_dgpu = id_dgpu.replace("\n","")
        
    return n_devices, id_igpu, id_dgpu, texto_igpu, texto_dgpu

def quit(_):
    notify.uninit()
    gtk.main_quit()

if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    main()
