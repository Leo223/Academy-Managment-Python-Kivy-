#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
from time import*
# from openpyxl import Workbook
import os
import json
import calendar

# python Academia_DataBase.py

class DB():

	def __init__(self):

		self.mesNum = gmtime()[1]
		self.dia = gmtime()[2]
		self.mes=strftime('%B')
		self.year = gmtime()[0]
		self.cal=calendar.Calendar()
		self.constructor_mes=self.cal.monthdays2calendar(self.year,self.mesNum)
		self.InicioMes={'Asignaturas':{},'Horarios':{}}
		# rutas archivos escritura
		self.ruta = 'Main_DB_json_GLOBAL.json'
		self.ruta_current = 'Main_DB_json_CURRENT.json'

		self.ComprobarArchivos()

		#Atajos
		self.Asignaturas = self.Main_DB[self.mes]['Asignaturas']
		self.Horarios = self.Main_DB[self.mes]['Horarios']


	# Funiciones de sistema
	def Guardar(self):
		json.dump(self.Main_DB,open(self.ruta_current,'w'),indent=4)
		open(self.ruta_current,'r').close()

	def Guardar_global(self):
		json.dump(self.Main_DB_global, open(self.ruta, 'w'), indent=4)
		open(self.ruta, 'r').close()


	# Asignaturas
	def Crear_Asignatura(self,N_Asignatura):

		if N_Asignatura not in self.Asignaturas.keys():
			self.Asignaturas[N_Asignatura]={}
			self.Horarios[N_Asignatura]={'dias':['---'],'turno':'---','Horas':['---','---']}
			self.Guardar()
		else:
			return 'Esa Asignatura ya esta en la establecida... Prueba con otra!'

	def Borrar_Asignatura(self,N_Asignatura):

		del self.Asignaturas[N_Asignatura]
		del self.Horarios[N_Asignatura]
		self.Guardar()

	def get_Asignaturas(self):
		return self.Asignaturas.keys()

	#Horarios

	def get_Asignaturas_Horarios(self):
		return self.Horarios.keys()

	def Horario_subject(self,N_Asignatura,dias,turno,horario):
		self.Horarios[N_Asignatura]={'dias':dias,'turno':turno,'Horas':horario}
		self.Guardar()

	# Alumnos
	def Crear_Alumno(self,N_Asignatura,N_Alumno):

		if N_Alumno not in self.Asignaturas[N_Asignatura].keys():

			self.Asignaturas[N_Asignatura][N_Alumno]={'Ficha':{'Pagado': 'Mes Completo'},
													  'Registro de horas':{},
													  'Observaciones':{}}
			self.Guardar()
		else:
			return 'El Alumno ya esta en la lista... Prueba otra vez'

	def Borrar_Alumno(self,N_Asignatura,N_Alumno):
		try:
			del self.Asignaturas[N_Asignatura][N_Alumno]
			self.Guardar()
			
		except KeyError:
			return 'Este alumno no existe, comprueba su nombre...'

	def Editar_Alumno(self,N_Asignatura,N_Alumno,New_N_Alumno):
		if ' ' in N_Alumno:    N_Alumno = N_Alumno.replace(' ', '_')
		if ' ' in New_N_Alumno:    New_N_Alumno = New_N_Alumno.replace(' ', '_')
		self.Asignaturas[N_Asignatura][New_N_Alumno]=self.Asignaturas[N_Asignatura][N_Alumno]
		del self.Asignaturas[N_Asignatura][N_Alumno]
		self.Guardar()

	def Importar_Alumnos_Mes_Anterior(self):
		lista_mes_anterior=[]
		for i in range(9):
			if i==1: lista_mes_anterior.append(gmtime()[1]-1)
			else: lista_mes_anterior.append(0)
		self.mes_anterior=strftime('%B',tuple(lista_mes_anterior))
		Asignaturas_mes_anterior=self.Main_DB[str(self.year)][self.mes_anterior]['Asignaturas']
		self.Main_DB[str(self.year)][self.mes]['Asignaturas']=Asignaturas_mes_anterior
		self.Guardar()

	def get_Alumnos(self,Asignatura):
		# for subject in self.Asignaturas.keys():
		# 	print subject,'-->',self.Asignaturas[subject].keys()
		return self.Asignaturas[Asignatura].keys()


	# Observaciones
	def Observacion_Alumno(self,N_Asignatura,N_Alumno,Observacion):
		if ' ' in N_Alumno:    N_Alumno = N_Alumno.replace(' ', '_')
		self.num_obvs = len(self.Asignaturas[N_Asignatura][N_Alumno]['Observaciones'].keys())
		self.Asignaturas[N_Asignatura][N_Alumno]['Observaciones'][self.num_obvs+1]=Observacion
		self.Guardar()
		
	def Borrar_Observacion(self,N_Asignatura,N_Alumno,No_Observacion):
		if ' ' in N_Alumno:    N_Alumno = N_Alumno.replace(' ', '_')
		del self.Asignaturas[N_Asignatura][N_Alumno]['Observaciones'][No_Observacion]
		self.Guardar()

	# FICHA
	def Numero_FICHA(self,N_Asignatura,N_Alumno,Num_ficha):
		if ' ' in N_Alumno:    N_Alumno = N_Alumno.replace(' ', '_')
		self.Asignaturas[N_Asignatura][N_Alumno]['Ficha']['Numero']= Num_ficha
		self.Guardar()

	def get_Numero_FICHA(self,N_Asignatura,N_Alumno):
		if ' ' in N_Alumno:    N_Alumno = N_Alumno.replace(' ', '_')
		if self.Asignaturas[N_Asignatura][N_Alumno]['Ficha'].has_key('Numero'):
			return self.Asignaturas[N_Asignatura][N_Alumno]['Ficha']['Numero']
		else:
			return '---'

	def Pagado(self,N_Asignatura,N_Alumno,Pago):
		if ' ' in N_Alumno:    N_Alumno = N_Alumno.replace(' ', '_')
		self.Asignaturas[N_Asignatura][N_Alumno]['Ficha']['Pagado']= Pago
		self.Guardar()

	def get_Pagado(self,N_Asignatura,N_Alumno):
		if ' ' in N_Alumno:    N_Alumno = N_Alumno.replace(' ', '_')
		if self.Asignaturas[N_Asignatura][N_Alumno]['Ficha'].has_key('Pagado'):
			return self.Asignaturas[N_Asignatura][N_Alumno]['Ficha']['Pagado']
		else:
			return 'Mes Completo'

	def Set_dias_sueltos(self,N_Asignatura,N_Alumno,Dia_suelto):
		if ' ' in N_Alumno:    N_Alumno = N_Alumno.replace(' ', '_')
		self.Asignaturas[N_Asignatura][N_Alumno]['Ficha']['Dia_Suelto'] = Dia_suelto
		self.Guardar()

	def get_dias_sueltos(self,N_Asignatura,N_Alumno):
		if ' ' in N_Alumno:    N_Alumno = N_Alumno.replace(' ', '_')
		if self.Asignaturas[N_Asignatura][N_Alumno]['Ficha'].has_key('Dia_Suelto'):
			return self.Asignaturas[N_Asignatura][N_Alumno]['Ficha']['Dia_Suelto']
		else:
			return '---'


	# Asistencia
	def Definir_Asistencia(self,N_Asignatura,N_Alumno,horas,dia_input):
		# si la variable dia esta vacia, toma el dia de hoy, en caso contrario
		# define la asistencia del dia que se indique
		if ' ' in N_Alumno:    N_Alumno = N_Alumno.replace(' ', '_')
		if dia_input=='':
			self.Asignaturas[N_Asignatura][N_Alumno]['Registro de horas'][str(self.dia)]=horas
			self.Guardar()
		else:
			self.Asignaturas[N_Asignatura][N_Alumno]['Registro de horas'][str(dia_input)]=horas
			self.Guardar()
		
	def Borrar_Asistencia(self,N_Asignatura,N_Alumno,dia_input):
		if ' ' in N_Alumno:    N_Alumno = N_Alumno.replace(' ', '_')
		if dia_input=='':
			del self.Asignaturas[N_Asignatura][N_Alumno]['Registro de horas'][str(self.dia)]
			self.Guardar()
		else:
			if dia_input in self.Asignaturas[N_Asignatura][N_Alumno]['Registro de horas'].keys():
				del self.Asignaturas[N_Asignatura][N_Alumno]['Registro de horas'][dia_input]
				self.Guardar()
			else:
				print 'No hay ninguna asistencia en el dia que se especifica...'
			
	def Editar_Asistencia(self,N_Asignatura,N_Alumno,horas,dia_input):
		if ' ' in N_Alumno:    N_Alumno = N_Alumno.replace(' ', '_')
		self.Asignaturas[N_Asignatura][N_Alumno]['Registro de horas'][dia_input] = horas
		self.Guardar()

	def get_Asistencia(self,N_Asignatura,N_Alumno):
		if ' ' in N_Alumno:    N_Alumno = N_Alumno.replace(' ', '_')
		return self.Asignaturas[N_Asignatura][N_Alumno]['Registro de horas']

	def get_horas_dia_alumno(self,N_Asignatura,N_Alumno,dia_input):
		if ' ' in N_Alumno:    N_Alumno = N_Alumno.replace(' ', '_')
		return self.Asignaturas[N_Asignatura][N_Alumno]['Registro de horas'][dia_input]

	def Exportar_Excel(self):
		# self.Nombre_Archivo = str(self.mes) + str(self.year) + '.xlsx'
		# self.wb = Workbook()
		# self.wb.worksheets[0].title = self.mes
		# self.ws=self.wb[self.wb.sheetnames[0]]
		# # creamos el encabezado de los numeros del dia del mes
		# self.ws.cell(row=4,column=2,value='Nombre Alumno')
		# for columna in range(1,32):	self.ws.cell(row=4,column=columna+2,value=columna)
		# self.ws.cell(row=4, column=32+2, value='Total Horas')
		# #
		# fila = 5
		# for subject in self.get_Asignaturas():
		# 	self.ws.cell(row=fila,column=2,value=subject)
		# 	fila+=1
		# 	for alumno in self.get_Alumnos(subject):
		# 		self.ws.cell(row=fila, column=2, value=alumno)
		# 		for dia in  self.get_Asistencia(subject,alumno).keys():
		# 			self.tiempo=self.get_horas_dia_alumno(subject,alumno,dia)
		# 			self.ws.cell(row=fila,column=2+int(dia),value=self.tiempo)
		# 		fila+=1
		# # Creamos el Excel y guardamos lo creado
		# self.wb.save(self.Nombre_Archivo)
		pass

	def Exportar_txt_for_Excel(self):

		# Creamos encabezado
		xls=open('HojaAsistencia.txt','w')
		xls.write(self.mes+ '\t:' + 'Julio' +'\n')
		xls.write('NombreAlumno\t')
		for dia in range(1, 32): xls.write(str(dia)+'\t')
		# Exportamos todos los datos de las Asistencias
		xls.write('\n')
		for subject in self.get_Asignaturas():
			xls.write('\n//'+ subject + '\n')
			for alumno in self.get_Alumnos(subject):
				xls.write('+' + alumno + '\t')
				for dia in range(1,32):
					if str(dia) in self.get_Asistencia(subject, alumno).keys():
						self.tiempo = self.get_horas_dia_alumno(subject, alumno, str(dia))
						xls.write(self.tiempo + '\t')
					else:
						xls.write('-' + '\t')
				xls.write('\n')
		xls.close()


	# Calendario
	def GenerarMes_bonito(self):
		print (self.cal)

	def ComprobarArchivos(self):

		if not os.path.exists(self.ruta):
			self.Main_DB_global = {str(self.year): {}}

		if os.path.exists(self.ruta_current):
			self.Main_DB = json.load(open(self.ruta_current, 'r'), parse_int=None, parse_float=None)
			print 'Existe Base de Datos de este MES!! Cargando...'
			self.ComprobarMes()
		else:
			self.Main_DB = {}
			self.Main_DB[self.mes] = self.InicioMes
			print 'NO existe Base de Datos\nNueva Base de Datos Creada!!'

	def ComprobarMes(self):
		self.MesRegistrado = self.Main_DB.keys()[0]
		if self.mes != self.MesRegistrado:
			if os.path.exists(self.ruta):
				self.Main_DB_global = json.load(open(self.ruta, 'r'), parse_int=None, parse_float=None)
				print 'Base de datos GLOBAL encotrada!!'

				if self.MesRegistrado == 'December':
					self.Main_DB_global[str(self.year - 1)][self.MesRegistrado] = self.Main_DB[self.MesRegistrado]
					self.Main_DB_global[str(self.year)] = {}
				else:
					self.Main_DB_global[str(self.year)][self.MesRegistrado] = self.Main_DB[self.MesRegistrado]
			else:
				self.Main_DB_global={}
				if self.MesRegistrado == 'December':
					self.Main_DB_global[str(self.year - 1)] = {self.MesRegistrado: self.Main_DB[self.MesRegistrado]}
					self.Main_DB_global[str(self.year)] = {}
				else:
					self.Main_DB_global[str(self.year)]={self.MesRegistrado: self.Main_DB[self.MesRegistrado]}
				print 'Base de datos GLOBAL creada! '

			self.Guardar_global()

			self.Main_DB_global={}
			self.Main_DB = {}
			self.Main_DB[self.mes] = self.InicioMes

		self.Guardar()



################################################################

#self.Main_DB[gmtime()[0]]['January']={}
#cal=calendar.Calendar()
#calendario = cal.monthdays2calendar(2016,5)

#cd C:\Users\Julio C.P\Desktop\Pruebas_kivy\ACADEMIA
#import Academia_DataBase
#db=Academia_DataBase.DB()

print '***********'
print '***********'

# print 'Empiezan las pruebas...'
print '----------'
# db=DB()
# print db.Main_DB.keys()[0]

# db.Exportar_txt_for_Excel()
# print db.Main_DB
print '----------'
print '----------'


