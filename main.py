#!/usr/bin/env python
# -*- coding: utf-8 -*-
#File name: main.py

# Cosas a Mejorar
# - Iconos y colocacion
# - Importar Alumnos del mes pasado
# - Resolver problema de cambio de mes en ANDROID

import os
os.environ["KIVY_DPI"]="518"
os.environ["KIVY_METRICS_DENSITY"] = "0.9"
# Para Android:
# os.environ["KIVY_METRICS_DENSITY"] = "3.5"
#linea 200
#linea 240

#kv file
#linea 528
#linea 555

from kivy.config import Config,ConfigParser
Config.set('graphics', 'width', '400')
Config.set('graphics', 'height', '600')
# Config.set('graphics', 'fullscreen', 0)
Config.set('postproc','retain_time','0')
Config.set('widgets','scroll_moves','1500')
Config.set('widgets','scroll_distance','200')
Config.write()

from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.tabbedpanel import TabbedPanel,TabbedPanelHeader,TabbedPanelItem
from kivy.uix.button import Button
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.carousel import Carousel
from kivy.uix.accordion import Accordion
from kivy.uix.bubble import Bubble
from kivy.uix.textinput import TextInput
from kivy.uix.checkbox import CheckBox
from kivy.uix.spinner import Spinner
from kivy.uix.widget import Widget
from kivy.uix.screenmanager import ScreenManager, Screen, WipeTransition,SwapTransition
from kivy.properties import StringProperty,ObjectProperty,NumericProperty
from kivy.properties import ListProperty,DictProperty,BooleanProperty
from kivy.lang import Builder
from kivy.metrics import dp, sp
from kivy.metrics import*
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.graphics import *

Window.clearcolor=(0,0,0,0)

from os.path import join, exists
import json
import twisted
from time import*

import Academia_DataBase
# import Excel_Converter
import calendar
import sys

# Archivos Auxiliares
from Builder_aux_tab import*
from Builder_aux_pupil import*
from Builder_aux_PopUp import*
from Builder_aux_PopUp_Confirmacion import*

#Config.set('kivy', 'keyboard_mode', 'systemandmulti')
# configuracion='config_JCP.ini'
# sett=ConfigParser()
# sett.read(configuracion)

Builder.load_string(PopUp_str)
Builder.load_string(PopUp_Confirmacion)
Builder.load_string(pupil_box_str_new)

################################################
######### Ventanas emergentes Auxiliares
##PopUp
class ContenidoPopup_Confirmacion(BoxLayout):
	ok_conf = ObjectProperty(None)
	cancel_conf = ObjectProperty(None)

class ContenidoPopup(BoxLayout):
	ok=ObjectProperty(None)
	cancel=ObjectProperty(None)
	input_nombre=StringProperty(None)
	Old_nombre = StringProperty(None)
	FocusTexto = BooleanProperty(True)

class Desplegable(Bubble):
	Posi=ListProperty(None)
	Nombre_pupil=StringProperty(None)

class SelectHoras(Carousel):
	Horas=StringProperty(None)
	Hora_Inical = StringProperty(None)

class BtnHoras(Button):
	# Mod_Horas=ObjectProperty(None)
	NombreAlumno=StringProperty(None)


################################################


print('###################\n')
print('###################\n')

### Declare all screens

class MainWindow(Screen):
	fecha_ahora = StringProperty()
	posTocada = ListProperty(None)

	def __init__(self,**kwargs):
		super(MainWindow, self).__init__(**kwargs)
		#Actualizamos el valor de la fecha y la pestaña de la asignatura actual
		Clock.schedule_interval(self.fecha, 1.0)

	def info_tabs(self,*args):

		print'###################\n'
		print'###################\n'

		self.Asignatura_actual()

		# print self.tabObject.current_tab.text
		#self.tabObject.remove_widget(self.get_current_tab)
		#print(dir(self.tabObject.tab_list.index))
		# print '---------**--------START'
		# self.tam_lista_tabs=range(len(self.tabObject.tab_list))
		# print 'Hay ' +str(len(self.tam_lista_tabs))+ ' tabs actualmente:'
		# for tabs in self.tam_lista_tabs:
		# 	print self.tabObject.tab_list[tabs].text

		#print ('current tab: ' +self.tabObject.current_tab.text)

	def fecha(self,*args):
		self.dia_mes_year='[b]'+strftime("%A")+'  '+ strftime("%d")+'/'+ strftime("%b")+'/'+strftime("%Y")+'[/b]'
		self.hora_now=strftime("%X")
		self.fecha_ahora=self.dia_mes_year +'\n'+self.hora_now

	# No funciona!!! retocar!
	# def on_touch_down(self, touch):
	# 	if self.collide_point(*touch.pos):
	# 		touch.grab(self)
	# 		# if len(self.children)>1:
	# 		# 	self.remove_widget(self.children[0])
	# 	return super(MainWindow, self).on_touch_down(touch)

	# def on_touch_down(self,touch):
	# 	print touch.pos
	# 	if 'button' in touch.profile:
	# 		print touch.profile[1]
	# 	return super(MainWindow, self).on_touch_down(touch)

	# def tocar(self,touch):
	# 	posTocada = touch.pos

	# def on_touch_down(self,touch):
	# 	# print touch.pos
	# 	self.posTocada = touch.pos
	# 	# if 'button' in touch.profile:
	# 	# 	print touch.profile[1]
	# 	return super(MainWindow, self).on_touch_down(touch)

class Calendario(Screen):

	# propiedades al archivo kivy
	week=ObjectProperty()
	days=ObjectProperty()
	editar=ObjectProperty()
	crear=ObjectProperty()
	mesName=StringProperty()

	# propiedades de importacion de datos de la pantalla ppal
	Nm_alumno=StringProperty()
	Nm_Asignatura= StringProperty()
	Asist_alumno=DictProperty()
	Horario_Subject = ListProperty()

	def __init__(self, **kwargs):
		super(Calendario, self).__init__(**kwargs)
		# creamos calendario y nombre del mes
		self.mesName=strftime('%B')
		self.hoy = strftime("%d")
		self.mesNum = gmtime()[1]
		self.cal=calendar.Calendar()
		self.currentYear = strftime('%Y')
		self.calendario = self.cal.monthdays2calendar(int(self.currentYear),self.mesNum)
		self.days.rows=len(self.calendario)
		self.DiaHorario={'Lunes':0,'Martes':1,'Miercoles':2,'Jueves':3,'Viernes':4,'Sabado':5,'Domingo':6}
		#####################
		# self.orientation='vertical'
		self.DiasSemana=['Lunes','Martes','Miercoles','Jueves','Viernes','Sabado','Domingo']
		self.Dias_clase_num=[]
		if '---' not in self.Horario_Subject:
			for dia in self.Horario_Subject[::-1]:	self.Dias_clase_num.append(self.DiaHorario[dia])
		self.get_calendar()

	def get_calendar(self):

		for diaSemana in self.DiasSemana:
			# self.week.add_widget(Label(text=diaSemana,font_size=45))
			self.week.add_widget(Label(text=diaSemana))

		for semanas in self.calendario:
			for dias in semanas:
				if dias[0] == 0: self.days.add_widget(Label())
				else:
					# Se crean los widgets
					self.BoxDia=BoxLayout(orientation='vertical',spacing=3)

					if str(dias[0]) in self.Asist_alumno.keys():
						self.cajaAsistencia = CheckBox()
						self.cajaAsistencia._toggle_active()
						self.cajaAsistencia.background_checkbox_disabled_down = self.cajaAsistencia.background_checkbox_down
						self.cajaAsistencia.disabled = True

						#horas
						self.texthoras=str(self.Asist_alumno[str(dias[0])])
						self.valorsHoras=('1h','1.5h','2h','2.5h','3h','X')
						self.TiempoDeClase= Spinner(text=self.texthoras,
													font_size=26,
													values=self.valorsHoras)
						self.TiempoDeClase.disabled = True
						self.TiempoDeClase.background_disabled_normal = self.TiempoDeClase.background_normal
						# self.TiempoDeClase = Label(text=str(self.Asist_alumno[str(dias[0])]))
					else:
						self.cajaAsistencia = CheckBox()
						self.cajaAsistencia.disabled = True
						# self.TiempoDeClase = Label(text='')



					if dias[1] in self.Dias_clase_num:
						self.BotonDia = BoxLayout(orientation='vertical')
						if str(int(self.hoy)) == str(dias[0]):
							self.BotonDia.add_widget(Button(text=str(dias[0]), background_color=[255, 100, 0, 0.4]))
						else:
							self.BotonDia.add_widget(Button(text=str(dias[0])))

						self.BotonDia.add_widget(Button(text='Dia de clase',font_size=33, background_color=[0, 1, 0, 1]))
						# self.BotonDia.add_widget(Button(text='Dia de clase', background_color=[0, 1, 0, 1]))
					else:
						if str(int(self.hoy)) == str(dias[0]):
							self.BotonDia = Button(text=str(dias[0]), background_color=[255, 100, 0, 0.4])
						else:
							self.BotonDia = Button(text=str(dias[0]))


					self.BoxInferior = BoxLayout(orientation='horizontal')
					self.BoxInferior = BoxLayout(orientation='horizontal')
					# Se genera y se distribuye la configurarcion de los widget
					self.BoxInferior.add_widget(self.cajaAsistencia)
					try:
						self.BoxInferior.add_widget(self.TiempoDeClase)
					except:
						pass
					self.BoxDia.add_widget(self.BotonDia)
					self.BoxDia.add_widget(self.BoxInferior)
					# Se une el BoxLayout ppal al calendario
					self.days.add_widget(self.BoxDia)

class Datos_Alumno(Screen):
	Nombre_Alumno = StringProperty()
	Numero_FICHA =StringProperty()
	Pagado = StringProperty()
	Dia_suelto = StringProperty()

class Horarios(Screen):
	Lista_Asignaturas = ListProperty()



##################### Clase Principal #########################
class LayoutsApp(App):

	### Funcion Principal
	def build(self):

		self.title = 'AtoS'
		###### Instanciamos la ventanas que va a haber en la aplicacion
		## Ventana ppal
		self.ppal_window = MainWindow(name='Main_Window')
		# self.ppal_window.size=dp(2560),dp(1440)


		########
		self.sm=ScreenManager()#transition=WipeTransition())
		self.sm.add_widget(self.ppal_window)
		self.sm.current='Main_Window'


		######## Importamos la DB principal que contiene todas las funciones
		######## para interactuar con la estructura de datos.
		######## importamos los datos guardadsos (si existen)
		self.DB = Academia_DataBase.DB()
		# Se importan los datos
		if os.path.exists(self.DB.ruta_current):
			# print self.DB.Main_DB
			self.Cargar_Datos()

		# Comprobaciones Iniciales
		# self.Condiciones_Iniciales()

		### A correr!
		return self.sm


####### Funciones de sistema ############
	def on_pause(self):
		return True

	def on_resume(self):
		pass

	def Cargar_Datos(self,*args):
		### Se cargan las asignaturas y alumnos de cada una
		self.hoy = strftime("%d")
		self.num_alumnos=0
		self.contador_Asistencias=0
		for subject in self.DB.Asignaturas.keys():
			self.Nm_load = str(subject)
			self.tab_load = Builder.load_string(tab_str % (self.Nm_load, self.Nm_load, self.Nm_load))
			self.ppal_window.tabObject.add_widget(self.tab_load)
			self.ppal_window.tabObject.switch_to(self.ppal_window.tabObject.tab_list[0])

			for pupil in self.DB.Asignaturas[subject].keys():
				if '_' in pupil: self.NmNice = pupil.replace('_',' ')
				else:	self.NmNice=pupil
				self.load_alumno = Builder.load_string(pupil_box_str_new % (pupil,pupil,pupil,pupil,self.NmNice,pupil,pupil,pupil))
				self.ppal_window.tabObject.current_tab.content.children[0].children[0].add_widget(self.load_alumno)
				self.num_alumnos+=1
			 	for fecha in self.DB.get_Asistencia(subject,pupil).keys():
					if int(fecha)==int(self.hoy):
						self.p0 = self.ppal_window.tabObject.current_tab.content.children[0].children[0].children
						if self.DB.get_horas_dia_alumno(subject, pupil, fecha) != 'X':
							self.p0[0].children[-1].text = self.DB.get_horas_dia_alumno(subject, pupil, fecha)
							self.p0[0].children[-1].background_disabled_normal='./Images/Attendanced_ref.png'
							self.contador_Asistencias+=1

		self.ppal_window.contador_asistencia.text = 'Contador Alumnos hoy:  ' + str(self.contador_Asistencias)
		self.ppal_window.alumnos_totales.text = 'Alumnos totales: ' + str(self.num_alumnos)

		# self.ppal_window.tabObject.activate
		# self.ppal_window.tabObject.current_tab=self.ppal_window.tabObject.tab_list[0]
		self.ppal_window.tabObject.switch_to(self.ppal_window.tabObject.tab_list[-1])

		### Se cargan los Horarios de las Asignaturas
		self.Cargar_horarios()

	def Exportar_txt_for_Excel(self):
		self.DB.Exportar_txt_for_Excel()

		self.Mensaje='SE HAN EXPORTADO LAS ASISTENCIAS DEL MES!!\n(Importalo en el excel)'
		self.txtcreado=Popup(title='Exportado Correctamente!',
							 auto_dismiss=True,
							 size_hint=(0.9,0.3),
							 pos_hint={'center_x':0.5,'center_y':0.75},
							 content=Label(text=self.Mensaje))
		self.txtcreado.open()

	def Subject_Right(self,*args):
		self.index=self.ppal_window.tabObject.tab_list.index(self.ppal_window.tabObject.current_tab)
		self.ppal_window.tabObject.switch_to(self.ppal_window.tabObject.tab_list[self.index-1])
		self.ppal_window.current_subject.text = self.ppal_window.tabObject.current_tab.text

	def Subject_Left(self, *args):
		self.lista=self.ppal_window.tabObject.tab_list
		self.index=self.lista.index(self.ppal_window.tabObject.current_tab)
		if self.index+1 == len(self.lista):	self.index=-1
		self.ppal_window.tabObject.switch_to(self.lista[self.index+1])
		self.ppal_window.current_subject.text = self.ppal_window.tabObject.current_tab.text

	def check_tab(self,*args):
		self.tabName = self.ppal_window.tabObject.current_tab.text
		if self.tabName == '[color=#000000][b]INICIO[/color][/b]':
			return False

	def PopUp_Warning(self,*args):

		self.texto = 'Este apartado NO tiene alumnos!!!\n Anda... Situate en una Asignatura!!!'
		self.contenido = Label(text= self.texto)
		self.popup_tab = Popup(title='Cuidado!!',
							   auto_dismiss = True,
							   size_hint=(0.8, 0.5),
							   pos_hint = {'center_x': 0.5, 'center_y': 0.75},
							   content=self.contenido)
		self.popup_tab.open()

	def PopUp_Warning_General(self,texto,*args):

		self.texto = texto
		self.contenido = Label(text= self.texto)
		self.popup_tab = Popup(title='Cuidado!!',
							   auto_dismiss = True,
							   size_hint=(0.8, 0.5),
							   pos_hint = {'center_x': 0.5, 'center_y': 0.75},
							   content=self.contenido)
		self.popup_tab.open()

	#funcion para encontrar la posicion del ultimo click
	def Posicion(self):

		self.p0 = self.ppal_window.tabObject.current_tab.content.children[0].children[0].children
		for alumno in self.p0:
			if alumno.children[1].state=='down':
				self.Old_nombre = alumno.children[1].text
				# print alumno.children[1].last_touch.spos
				self.posicion_y = alumno.children[1].last_touch.spos[1]
				self.posicion_x = alumno.children[1].last_touch.spos[0]
				# print dir(alumno.children[1])
		return [self.posicion_x,self.posicion_y,self.Old_nombre]

	# def on_touch_down(self,touch):
	# 	print 'tocado'
	# 	if 'button' in touch.profile:
	# 		print touch.profile
	# 	return super(LayoutsApp, self).on_touch_down(touch)


#########################################
	### Incluir o borrar TAB (Asignatura)
	def PopUp_Add_tab(self):
		# se define el interior del Popup ##
		self.contenido=ContenidoPopup(ok=self.Create_New_TAB,
									  cancel=self.PopUp_close)

		# instanciamos y creamos el Popup
		self.popup_tab=Popup(title='Introduce el nombre de la TAB',
							 auto_dismiss=False,
							 size_hint=(0.8,0.5),
							 pos_hint={'center_x':0.5,'center_y':0.75},
							 content=self.contenido)
		self.popup_tab.open()

	def PopUp_close(self):
		self.popup_tab.dismiss()

	def PopUp_remove_subject_conf(self):
		# se define el interior del Popup ##
		self.contenido_conf = ContenidoPopup_Confirmacion(ok_conf=self.Delete_tab,
														  cancel_conf=self.Popup_close_subject_conf)
		self.popup_conf = Popup(title='Confirmacion',
								auto_dismiss=False,
								size_hint=(0.8, 0.5),
								pos_hint={'center_x': 0.5, 'center_y': 0.75},
								content=self.contenido_conf)
		self.popup_conf.open()

	def Popup_close_subject_conf(self):

		self.popup_conf.dismiss()

	def Create_New_TAB(self,*args):

	 	self.name_tab=self.contenido.input_nombre

		if self.name_tab in self.DB.get_Asignaturas():
			self.texto = 'ESTA ASIGNATURA YA EXISTE!!\nDIFERENCIALA DE OTRA MANERA!'
			self.PopUp_close()
			self.PopUp_Warning_General(self.texto)

		else:
			# print('****')
			# print(self.contenido.input_nombre)
			self.popup_tab.dismiss()

			## SE CONSTRUYE UNA NUEVA TAB
			# self.Nm = str(self.name_tab)
			self.Nm = str(self.name_tab)
			self.tab = Builder.load_string(tab_str %(self.Nm,self.Nm,self.Nm))
			self.ppal_window.tabObject.add_widget(self.tab)
			self.ppal_window.tabObject.switch_to(self.ppal_window.tabObject.tab_list[0])

			## Se incluye la asignatura a la base de datos ppal DB
			self.DB.Crear_Asignatura(self.Nm)


	def Delete_tab(self, *args):
		###
		self.popup_conf.dismiss()
		###
		if self.check_tab() == False:
			self.PopUp_Warning()
			self.ppal_window.checkin.state='normal'
			return False

		if len(self.ppal_window.tabObject.tab_list)>1:
			self.ppal_window.tabObject.children[0].children[0].clear_widgets()
			self.borra=self.ppal_window.tabObject.current_tab.text
			self.ppal_window.tabObject.remove_widget(self.ppal_window.tabObject.current_tab)
			## Borramos la asignatura de la base de datos
			self.DB.Borrar_Asignatura(self.borra)
			self.ppal_window.tabObject.switch_to(self.ppal_window.tabObject.tab_list[-1])

		else:
			print 'No hay asignaturas para borrar...'
			self.ppal_window.tabObject.switch_to(self.ppal_window.tabObject.tab_list[-1])

#########################################

#########################################

	### Funciones de Alumno

	def PopUp_Nombre_Pupil(self):

		# Comprobacion de Asignatura actual
		if self.check_tab() == False:
			self.PopUp_Warning()
			return False

		# se define el interior del Popup ##
		self.contenido_create_pupil=ContenidoPopup(ok=self.Add_Subwidget_pupil,
									   cancel=self.PopUp_close_create_pupil)

		self.popup_create_pupil=Popup(title='Alumno Nuevo',
								auto_dismiss=False,
								size_hint=(0.8, 0.5),
								pos_hint={'center_x': 0.5, 'center_y': 0.75},
								content=self.contenido_create_pupil)
		self.popup_create_pupil.open()

	def Popup_Remove_pupil_Conf(self):
		# se define el interior del Popup ##
		self.contenido_conf = ContenidoPopup_Confirmacion(ok_conf=self.Remove_subwidget_pupil,
														  cancel_conf=self.Popup_close_pupil_conf)
		self.popup_conf = Popup(title='Confirmacion',
								auto_dismiss=False,
								size_hint=(0.8, 0.5),
								pos_hint={'center_x': 0.5, 'center_y': 0.75},
								content=self.contenido_conf)
		self.popup_conf.open()

	def PopUp_close_create_pupil(self):
		self.popup_create_pupil.dismiss()

	def PopUp_close_editar_pupil(self):
		self.popup_editar_pupil.dismiss()

	def Popup_close_pupil_conf(self):

		self.p0 = self.ppal_window.tabObject.current_tab.content.children[0].children[0].children
		for alumno_cancel in self.p0: alumno_cancel.children[2].state ='normal'
		self.popup_conf.dismiss()

	def Add_Subwidget_pupil(self,*args):
		###
		self.popup_create_pupil.dismiss()
		###
		self.Nm = self.contenido_create_pupil.input_nombre
		self.NmNice =self.Nm
		if ' ' in self.Nm:	self.Nm=self.Nm.replace(' ','_')
		self.asignatura=self.ppal_window.tabObject.current_tab.text
		self.alumno = Builder.load_string(pupil_box_str_new %(self.Nm,self.Nm,self.Nm,self.Nm,self.NmNice,self.Nm,self.Nm,self.Nm))
		self.ppal_window.tabObject.current_tab.content.children[0].children[0].add_widget(self.alumno)
		self.DB.Crear_Alumno(self.asignatura,self.Nm)
		self.num_alumnos = int(self.ppal_window.alumnos_totales.text.split(':')[-1]) + 1
		self.ppal_window.alumnos_totales.text = 'Alumnos Totales: ' + str(self.num_alumnos)

	def Remove_subwidget_pupil(self, *args):
		####
		self.popup_conf.dismiss()
		####

		self.p0 = self.ppal_window.tabObject.current_tab.content.children[0].children[0].children
		for alumno in self.p0:
			if alumno.children[2].state =='down':
				self.ppal_window.tabObject.current_tab.content.children[0].children[0].remove_widget(alumno)
				self.NmAlumno=alumno.children[1].text
				if ' ' in self.NmAlumno:    self.NmAlumno = self.NmAlumno.replace(' ', '_')
				self.DB.Borrar_Alumno(self.ppal_window.tabObject.current_tab.text,self.NmAlumno)
		self.popup_conf.dismiss()
		self.num_alumnos = int(self.ppal_window.alumnos_totales.text.split(':')[-1]) - 1
		self.ppal_window.alumnos_totales.text = 'Alumnos Totales: ' + str(self.num_alumnos)

	def Desplegable_pupil_options(self,Nombre_Alumno,*args):
		self.Pos = self.Posicion()
		self.desplegar = Desplegable(name='Desplegable_Nombre', Posi=self.Pos, Nombre_pupil=Nombre_Alumno)
		if len(self.ppal_window.children)<2:
			self.ppal_window.add_widget(self.desplegar)
			Clock.schedule_once(self.Quitar_Desplegable, 2)

	def Quitar_Desplegable(self,*args):

		self.ppal_window.remove_widget(self.ppal_window.children[0])

	def PopUp_Editar_Alumno(self,old_pupil,*args):
		# se define el interior del Popup ##
		self.contenido_editar_pupil = ContenidoPopup(ok=self.Editar_Nombre_Alumno,
													 cancel=self.PopUp_close_editar_pupil,
													 Old_nombre = old_pupil,
													 FocusTexto = True)
		self.popup_editar_pupil = Popup(title='Introduce el NUEVO Nombre del alumno...',
										auto_dismiss=False,
										size_hint=(0.8, 0.5),
										pos_hint={'center_x': 0.5, 'center_y': 0.75},
										content=self.contenido_editar_pupil)
		self.popup_editar_pupil.focus = True
		self.popup_editar_pupil.open()

	def Editar_Nombre_Alumno(self,*args):
		###
		self.popup_editar_pupil.dismiss()
		###
		self.asignatura = self.ppal_window.tabObject.current_tab.text
		self.Nuevo_Nombre_Alumno=self.contenido_editar_pupil.input_nombre
		self.Old_Nombre_Alumno=self.contenido_editar_pupil.Old_nombre
		self.DB.Editar_Alumno(self.asignatura,self.Old_Nombre_Alumno,self.Nuevo_Nombre_Alumno)

		self.p0 = self.ppal_window.tabObject.current_tab.content.children[0].children[0].children
		self.subject=self.ppal_window.tabObject.current_tab.text
		for btalumno in self.p0:
			if btalumno.children[1].text == self.Old_Nombre_Alumno:
				btalumno.children[1].text = self.Nuevo_Nombre_Alumno

#########################################

	### FICHA

	def Editar_Nombre_FICHA(self,nombre,*args):
		self.Old_Nombre_Alumno = self.Ficha.nombre_FICHA.text
		if self.Ficha.editar_nombre_FICHA.state == 'down':
			self.Ficha.remove_widget(self.Ficha.box_nombre.children[-1])
			self.Ficha.box_nombre.add_widget(TextInput(text=self.Old_Nombre_Alumno,multiline=False))
		else:
			self.Nm_input=self.Ficha.box_nombre.children[0]
			if self.Nm_input.text !='' and self.Nm_input.text != self.Old_Nombre_Alumno:
				self.asignatura = self.ppal_window.tabObject.current_tab.text
				self.Nuevo_Nombre = self.Nm_input.text
				self.Ficha.nombre_FICHA.text = self.Nuevo_Nombre
				self.DB.Editar_Alumno(self.asignatura, self.Old_Nombre_Alumno, self.Nuevo_Nombre)
				self.Ficha.box_nombre.remove_widget(self.Nm_input)
			else:
				self.Ficha.box_nombre.remove_widget(self.Nm_input)

	def Numero_FICHA(self,nombre,*args):
		self.Nombre = self.Ficha.nombre_FICHA.text
		self.asignatura = self.ppal_window.tabObject.current_tab.text

		if self.Ficha.set_num_FICHA.state == 'down':
			# self.Ficha.remove_widget(self.Ficha.box_NumeroFicha.children[-1])
			self.Ficha.box_NumeroFicha.add_widget(TextInput(text='', multiline=False))
		else:
			if self.Ficha.box_NumeroFicha.children[0].text != '':
				self.Num_Ficha = self.Ficha.box_NumeroFicha.children[0].text
				self.Ficha.numero_FICHA.text = self.Num_Ficha
				self.DB.Numero_FICHA(self.asignatura,self.Nombre,self.Num_Ficha)
				self.Ficha.box_NumeroFicha.remove_widget(self.Ficha.box_NumeroFicha.children[0])

			else:
				self.Ficha.box_NumeroFicha.remove_widget(self.Ficha.box_NumeroFicha.children[0])

	def Mes_Pagado(self,*args):
		self.asignatura = self.ppal_window.tabObject.current_tab.text
		self.nombre=self.Ficha.nombre_FICHA.text
		if self.Ficha.set_horas_Mes.state == 'down':
			self.Ficha.horas_Mes.disabled=False

		else:
			self.Pagado = self.Ficha.horas_Mes.text
			self.DB.Pagado(self.asignatura,self.nombre,self.Pagado)
			self.Ficha.horas_Mes.disabled = True
			if self.Ficha.horas_Mes.text != 'Mes Completo':
				self.Ficha.box_dias_sueltos.disabled = False

	def Set_dia_suelto(self,*args):
		self.asignatura = self.ppal_window.tabObject.current_tab.text
		self.nombre = self.Ficha.nombre_FICHA.text
		self.diaSuelto=self.Ficha.dias_sueltos.text
		self.DB.Set_dias_sueltos(self.asignatura,self.nombre,self.diaSuelto)
		self.Ficha.set_dia_suelto.state='normal'
		self.Ficha.box_dias_sueltos.disabled=True

	### Horarios
	def Cargar_horarios(self,*args):
		for subject in self.DB.get_Asignaturas_Horarios():
			self.Lista_check=[subject,
							  self.DB.Horarios[subject]['dias'],
							  self.DB.Horarios[subject]['turno'],
							  self.DB.Horarios[subject]['Horas']]
			if self.Lista_check[2]!='---':
				self.wid = BoxLayout(orientation='horizontal', size_hint_y=None, border=(30, 30, 30, 30))
				self.wid.add_widget(Label(text=self.Lista_check[0]))
				self.textoDias = ''

				for dias in self.Lista_check[1][::-1]:    self.textoDias += dias + '\n'
				self.wid.add_widget(Label(text=self.textoDias))
				self.wid.add_widget(Label(text=self.Lista_check[2]))
				self.wid.add_widget(Label(text=self.Lista_check[3][0] + '-' + self.Lista_check[3][1]))

				if self.Lista_check[2] == 'Tardes':
					self.ppal_window.box_Tardes.add_widget(self.wid)
				else:
					self.ppal_window.box_Manana.add_widget(self.wid)

	def Definir_horarios(self, *args):
		self.Lista_check=[]
		## Asignatura
		if self.Horarios.asignatura.text == '-----':
			self.texto = 'Tienes que seleccionar la asignatura'
			self.PopUp_Warning_General(self.texto)
		else:
			self.Lista_check.append(self.Horarios.asignatura.text)

		### Dias de la semana
		self.Lista_dias=[]
		for dia in self.Horarios.diasSemana.children:
			if type(dia) is CheckBox:
				if dia.active == True:
					self.Lista_dias.append(dia.text)
		if len(self.Lista_dias)==0:
			self.texto = 'Tienes que Marcar los dias de clase!!'
			self.PopUp_Warning_General(self.texto)
		else:
			self.Lista_check.append(self.Lista_dias)

		### Horario de la Asignatura
		if self.Horarios.mananas.state =='down':
			self.IM_h = self.Horarios.mananaInicioHora.children[0].children[0].text
			self.IM_m = self.Horarios.mananaInicioMinuto.children[0].children[0].text
			self.FM_h = self.Horarios.mananaFinHora.children[0].children[0].text
			self.FM_m = self.Horarios.mananaFinMinuto.children[0].children[0].text

			self.Inicio_manana = self.IM_h + str(':') + self.IM_m
			self.Fin_manana = self.FM_h + str(':') + self.FM_m

			if int(self.FM_h)<int(self.IM_h):
				self.texto = 'La hora de Fin es MENOR que la hora de Entrada' \
							 '\nNo creo que la clase dure mas de 24h... ;)'
				self.PopUp_Warning_General(self.texto)
			elif int(self.FM_h) == int(self.IM_h):
				self.texto = 'La hora de Fin es la MISMA que la hora de Entrada' \
							 '\n No creo que la clase dure menos de una hora... ;P'
				self.PopUp_Warning_General(self.texto)
			else:
				self.Lista_check.append(str(self.Horarios.mananas.text))
				self.Lista_check.append([self.Inicio_manana,self.Fin_manana])

		elif self.Horarios.tardes.state =='down':
			self.IT_h = self.Horarios.tardeInicioHora.children[0].children[0].text
			self.IT_m = self.Horarios.tardeInicioMinuto.children[0].children[0].text
			self.FT_h = self.Horarios.tardeFinHora.children[0].children[0].text
			self.FT_m = self.Horarios.tardeFinMinuto.children[0].children[0].text

			self.Inicio_tarde = self.IT_h + str(':') + self.IT_m
			self.Fin_tarde = self.FT_h + str(':') + self.FT_m

			if int(self.FT_h) < int(self.IT_h):
				self.texto = 'La hora de Fin es MENOR que la hora de Entrada' \
							 '\nNo creo que la clase dure mas de 24h... ;)'
				self.PopUp_Warning_General(self.texto)
			elif int(self.FT_h) == int(self.IT_h):
				self.texto = 'La hora de Fin es la MISMA que la hora de Entrada' \
							 '\n No creo que la clase dure menos de una hora... ;P'
				self.PopUp_Warning_General(self.texto)
			else:
				self.Lista_check.append(str(self.Horarios.tardes.text))
				self.Lista_check.append([self.Inicio_tarde, self.Fin_tarde])

		else:
			self.texto = 'Tienes que establecer un horario para la asignatura!'
			self.PopUp_Warning_General(self.texto)
		# print self.ppal_window.box_Tardes.children[0]
		if len(self.Lista_check)==4:
			if self.Lista_check[0] in self.DB.get_Asignaturas_Horarios():
				if self.Lista_check[2] == 'Tardes':
					for subject in self.ppal_window.box_Tardes.children:
						if subject.children[-1].text==self.Lista_check[0]:
							self.ppal_window.box_Tardes.remove_widget(subject)
				else:
					for subject in self.ppal_window.box_Manana.children:
						if subject.children[-1].text == self.Lista_check[0]:
							self.ppal_window.box_Manana.remove_widget(subject)

			self.DB.Horario_subject(self.Lista_check[0],self.Lista_check[1],self.Lista_check[2],self.Lista_check[3])
			self.wid = BoxLayout(orientation='horizontal',size_hint_y=None,border= (30, 30,30, 30))
			self.wid.add_widget(Label(text=self.Lista_check[0]))
			self.textoDias=''
			for dias in self.Lista_check[1][::-1]:	self.textoDias+= dias+'\n'
			self.wid.add_widget(Label(text=self.textoDias))
			self.wid.add_widget(Label(text=self.Lista_check[2]))
			self.wid.add_widget(Label(text=self.Lista_check[3][0] +'-'+ self.Lista_check[3][1]))

			if self.Lista_check[2] == 'Tardes':
				self.ppal_window.box_Tardes.add_widget(self.wid)
			else:
				self.ppal_window.box_Manana.add_widget(self.wid)



			self.texto = 'HORARIO DE ASIGNATURA CREADO!!\n'
			self.PopUp_Warning_General(self.texto)



	# def Activar_Horario_HORARIOS(self,instance,value,*args):
    #


	# Horario/ppal
	def Cambiar_franja_HORARIO_mananas(self,*args):
		if self.ppal_window.tardes.state=='down':
			self.ppal_window.mananas.state = 'normal'
			self.ppal_window.franjaHoraria.load_next()
		else:
			self.ppal_window.mananas.state = 'down'
			self.ppal_window.tardes.state = 'normal'
			self.ppal_window.franjaHoraria.load_previous()
	def Cambiar_franja_HORARIO_tardes(self, *args):
		if self.ppal_window.mananas.state=='down':
			self.ppal_window.tardes.state = 'normal'
			self.ppal_window.franjaHoraria.load_previous()
		else:
			self.ppal_window.tardes.state = 'down'
			self.ppal_window.mananas.state = 'normal'
			self.ppal_window.franjaHoraria.load_next()

	def Set_mananas(self,*args):
		if self.Horarios.mananas.state == 'down':
			self.Horarios.box_mananas.children[0].disabled = False
			self.Horarios.box_mananas.children[1].disabled = False
			self.Horarios.tardes.state = 'normal'
			self.Horarios.box_tardes.children[0].disabled = True
			self.Horarios.box_tardes.children[1].disabled = True
		else:
			self.Horarios.box_mananas.children[0].disabled = True
			self.Horarios.box_mananas.children[1].disabled = True
	def Set_tardes(self,*args):
		if self.Horarios.tardes.state == 'down':
			self.Horarios.box_tardes.children[0].disabled = False
			self.Horarios.box_tardes.children[1].disabled = False
			self.Horarios.mananas.state = 'normal'
			self.Horarios.box_mananas.children[0].disabled = True
			self.Horarios.box_mananas.children[1].disabled = True
		else:
			self.Horarios.box_tardes.children[0].disabled = True
			self.Horarios.box_tardes.children[1].disabled = True



	### Control de Asistencia

	def Asistencia_global(self,*args):

		# Comprobacion de Asignatura actual
		if self.check_tab() == False:
			self.PopUp_Warning()
			self.ppal_window.checkin.state='normal'
			return False

		self.p0 = self.ppal_window.tabObject.current_tab.content.children[0].children[0].children
		self.subject=self.ppal_window.tabObject.current_tab.text
		self.contador_asistencia=int(self.ppal_window.contador_asistencia.text.split(':')[-1])

		if self.ppal_window.checkin.state =='down':
			self.ppal_window.checkout.disabled = True
		else:
			self.ppal_window.checkout.disabled = False

		for btalumno in self.p0:
			if btalumno.children[-1].background_disabled_normal != './Images/Attendanced_ref.png':
				btalumno.children[-1].disabled = False
				btalumno.children[-1].background_normal = './Images/cross.png'

		if self.ppal_window.checkin.state =='normal':
			for alumno in self.p0:
				if alumno.children[-1].disabled == False:
					self.NmAlumno = alumno.children[1].text
					if alumno.children[-1].state == 'down':
						self.tiempoDeClase = alumno.children[-2].children[0].current_slide.text
						self.DB.Definir_Asistencia(self.subject,self.NmAlumno,self.tiempoDeClase,'')
						alumno.children[-1].state = 'normal'
						alumno.children[-1].background_disabled_normal = './Images/Attendanced_ref.png'
						alumno.children[-1].text = self.tiempoDeClase
						self.contador_asistencia+=1
					else:
						self.DB.Definir_Asistencia(self.subject, self.NmAlumno, 'X', '')

			for btalumno in self.p0:
				btalumno.children[-1].disabled = True
				btalumno.children[-2].clear_widgets()
				btalumno.children[-2].size_hint_x = 0.01

			self.ppal_window.contador_asistencia.text = 'Contador Alumnos hoy:  '+ str(self.contador_asistencia)

		else:
			for alumno in self.p0:
				self.NmAlumno = alumno.children[1].text
				self.horasbysem = self.DB.get_Pagado(self.subject, self.NmAlumno)
				self.D_suelto = self.DB.get_dias_sueltos(self.subject, self.NmAlumno)

				if self.horasbysem == 'Mes Completo':
					self.Inicial = '1.5h'
				else:
					if self.D_suelto == '---':
						self.hora = str(float(self.horasbysem.split('h')[0])/2.0)
						if self.hora.split('.')[1]=='0':	self.hora = self.hora.split('.')[0]
						self.Inicial= self.hora+'h'
					else:	self.Inicial = self.horasbysem.split('h')[0]+'h'

				self.TiempoDeClase = SelectHoras(nombre='SeleccionHoras',Hora_Inical=self.Inicial)
				self.Nombre = alumno.children[1].text
				alumno.children[-2].size_hint_x = 0.4
				alumno.children[-2].add_widget(self.TiempoDeClase)

				if alumno.children[-1].background_disabled_normal == './Images/Attendanced_ref.png':
					alumno.children[-2].disabled = True
				else:
					alumno.children[-2].disabled = False

	def Borrar_Asistencia_global(self,*args):

		# Comprobacion de Asignatura actual
		if self.check_tab() == False:
			self.PopUp_Warning()
			self.ppal_window.checkout.state='normal'
			return False

		self.p0 = self.ppal_window.tabObject.current_tab.content.children[0].children[0].children
		self.subject = self.ppal_window.tabObject.current_tab.text

		if self.ppal_window.checkout.state=='down':
			self.ppal_window.checkin.disabled = True
		else:
			self.ppal_window.checkin.disabled = False


		# Contador de alumnos en el dia
		self.cont = int(self.ppal_window.contador_asistencia.text.split(':')[-1])

		# Se activan o desactivan los alumnos que estaban con la asistencia verificada
		if self.ppal_window.checkout.state == 'down':
			for btalumno in self.p0:
				if btalumno.children[-1].background_disabled_normal=='./Images/Attendanced_ref.png':
					btalumno.children[-1].disabled = False
					btalumno.children[-1].background_normal='./Images/check.png'
					btalumno.children[-1].background_down='./Images/cross.png'

		# Proceso que borra en el caso de que se haya seleccionado para ello
		# if self.ppal_window.checkout.state == 'normal':
		else:
			for alumno in self.p0:
				if alumno.children[-1].disabled == False:
					if alumno.children[-1].state == 'down':
						self.DB.Borrar_Asistencia(self.subject, alumno.children[1].text, '')
						self.DB.Definir_Asistencia(self.subject, alumno.children[1].text, 'X', '')
						alumno.children[-1].state = 'normal'
						self.imagen_desactivado='atlas://data/images/defaulttheme/button_disabled'
						alumno.children[-1].background_disabled_normal = self.imagen_desactivado
						alumno.children[-1].text = ''

						self.cont-=1
						# alumno.children[-1].text = 'X'
						# self.DB.Definir_Asistencia(self.subject, alumno.children[1].text, 'X', '')
					else:
						alumno.children[-1].state = 'normal'
						alumno.children[-1].background_disabled_normal = './Images/Attendanced_ref.png'

					alumno.children[-1].background_normal='/Images/cross.png'
					alumno.children[-1].background_down='./Images/check.png'


			for btalumno in self.p0:    btalumno.children[-1].disabled = True

			self.ppal_window.contador_asistencia.text = 'Contador Alumnos hoy:  ' + str(self.cont)

#

#########################################

	def Editar_Asistencia(self,*args):
		self.subject = self.ppal_window.tabObject.current_tab.text
		self.BoxDia=self.Mes.days.children
		self.editar_alumno=self.Mes.days
		# print self.Mes.days.children[-8].children[0].children[0].text
		# print self.Mes.days.children[-8].children[0].children[1].active
		# print dir(self.BoxDia[-8].children[0].children[0])
		# print self.BoxDia[-7].children[0].children[0]

		if self.Mes.editar.state=='down':
			for i in self.BoxDia:
				if len(i.children) > 1:
					if len(i.children[0].children) > 1:
						i.children[0].children[1].disabled = False
						i.children[0].children[0].disabled = False

		else:
			for i in self.BoxDia:
				if len(i.children) > 1:
					if len(i.children[0].children) > 1:
						# dia (texto en el boton superior)
						if 'BoxLayout' in i.children[1].__str__():
							self.diaAcambiar = i.children[1].children[1].text
						else:
							self.diaAcambiar = i.children[1].text

						if i.children[0].children[1].active == True:
							# horas en el spinner (horas correspondiente en el spinner)
							self.horas_nuevas = i.children[0].children[0].text
							self.DB.Editar_Asistencia(self.subject,self.Nombre_alumno,self.horas_nuevas,self.diaAcambiar)
						else:
							self.DB.Borrar_Asistencia(self.subject,self.Nombre_alumno,self.diaAcambiar)
							i.children[0].remove_widget(i.children[0].children[0])
							## Let's update the screen
							Clock.schedule_once(lambda dt: 0, 0)
						i.children[0].children[0].disabled = True

			for i in self.BoxDia:
				if len(i.children) > 1:
					if len(i.children[0].children) > 1:
						i.children[0].children[1].disabled = True
						i.children[0].children[0].disabled = True

	def Asistencia_puntual(self,*args):
		self.subject = self.ppal_window.tabObject.current_tab.text
		self.BoxDia=self.Mes.days.children
		self.crear_asistencia=self.Mes.days
		###########

		###########
		if self.Mes.crear.state=='down':
			for i in self.BoxDia:
				if len(i.children)>1:
					if len(i.children[0].children) == 1:
						i.children[0].children[0].disabled = False
						self.valorsHoras = ('1h', '1.5h', '2h', '2.5h', '3h','X')
						self.TiempoDeClase = Spinner(text='---',
													 font_size=26,
													 values=self.valorsHoras)
						i.children[0].add_widget(self.TiempoDeClase)
			## Let's update the screen
			Clock.schedule_once(lambda dt: 0, 0)
		else:
			for i in self.BoxDia:
				if len(i.children) > 1:
					# if len(i.children[0].children) == 1:
					self.spinner = i.children[0].children[0]
					self.check = i.children[0].children[1]
					if self.spinner.text != '---' and self.check.active == True:
						self.horas = self.spinner.text
						if 'BoxLayout' in i.children[1].__str__():
							self.diaInput = i.children[1].children[1].text
						else:
							self.diaInput = i.children[1].text
						self.DB.Definir_Asistencia(self.subject,self.Nombre_alumno,self.horas,self.diaInput)
						self.spinner.background_disabled_normal = self.spinner.background_normal
						self.check.background_checkbox_disabled_down = self.check.background_checkbox_down
						self.spinner.disabled = True
						self.check.disabled = True
					else:
						i.children[0].remove_widget(self.spinner)
						self.check.active == False
						self.check.disabled = True
			# Let's update the screen
			Clock.schedule_once(lambda dt: None, 0)


	### Switch to screen

	def Switch_to_Calendar_screen(self,cal_nombre,*args):

		#Importamos los datos del alumno

		self.current_subject = self.ppal_window.tabObject.current_tab.text
		self.Nombre_alumno = cal_nombre
		self.Lista_Asistencia = self.DB.get_Asistencia(self.current_subject, self.Nombre_alumno)
		self.Mes = Calendario(name='Calendario',
							  Nm_alumno=self.Nombre_alumno,
							  Nm_Asignatura = self.current_subject,
							  Horario_Subject=self.DB.Horarios[self.current_subject]['dias'],
							  Asist_alumno=self.Lista_Asistencia)

		self.sm.add_widget(self.Mes)
		self.sm.transition.direction = 'left'
		self.sm.current = 'Calendario'

	def Switch_to_Ficha_Alumno(self,nombre, *args):
		# self.sm=ScreenManager(transition = WipeTransition())
		self.asignatura = self.ppal_window.tabObject.current_tab.text
		self.Num_Ficha = self.DB.get_Numero_FICHA(self.asignatura,nombre)
		self.Pagado = self.DB.get_Pagado(self.asignatura,nombre)
		self.diaSuelto = self.DB.get_dias_sueltos(self.asignatura,nombre)
		self.Ficha = Datos_Alumno(name='Ficha',
								  Nombre_Alumno = nombre,
								  Numero_FICHA=self.Num_Ficha,
								  Pagado = self.Pagado,
								  Dia_suelto = self.diaSuelto)

		self.sm.add_widget(self.Ficha)
		self.sm.transition.direction = 'down'
		self.sm.current = 'Ficha'

	def Switch_to_Horario(self,*args):

		self.Asignaturas = self.DB.Asignaturas.keys()
		self.Horarios = Horarios(name='Horarios',Lista_Asignaturas = self.Asignaturas)
		self.sm.add_widget(self.Horarios)
		self.sm.transition.direction = 'up'
		self.sm.current = 'Horarios'

	def Switch_to_Main_screen(self, *args):
		# print self.sm.screens
		# self.sm.switch_to('Calendario', direction='right')
		self.sm.transition.direction = 'right'
		self.sm.current = 'Main_Window'
		self.sm.remove_widget(self.sm.screens[-1])


	# Generar Outputs (Excel)

	# def Crear_Excel(self):
	# 	Excel_Converter.Excel_Export().Exportar_Excel()



#########################################

if __name__ == '__main__':
    LayoutsApp().run()





