import os
import json
import Academia_DataBase
from time import*
import calendar
from xlsxwriter import Workbook


class Excel_Export():

	def __init__(self):

		self.DB = Academia_DataBase.DB()
		self.ruta = 'Main_DB_json_GLOBAL.json'
		self.ruta_current = 'Main_DB_json_CURRENT.json'

		self.mesName = strftime('%B')
		self.hoy = strftime("%d")
		self.mesNum = gmtime()[1]
		self.cal = calendar.Calendar()
		self.currentYear = strftime('%Y')
		self.calendario = self.cal.monthdays2calendar(int(self.currentYear), self.mesNum)
		self.DiaHor = {0:'Lun',1:'Mar',2:'Mie',3:'Jue',4:'Vie',5:'Sab',6:'Dom'}
		# for i in self.calendario:
		# 	print i

		self.DiaHor_rev={}
		for x,y in self.DiaHor.items(): self.DiaHor_rev[y]=x

		self.dias_del_mes={}
		for semanas in self.calendario:
			for dia in semanas:
				if dia[0]!= 0: self.dias_del_mes[dia[0]] = dia[1]

		self.profesor = "Julio"

		self.Check_file_JSON()


	def Check_file_JSON(self):
		if os.path.exists(self.ruta_current):
			self.Main_DB = json.load(open(self.ruta_current, 'r'), parse_int=None, parse_float=None)
		else:
			txt = open('ERROR_json.txt', 'w')
			txt.write('ERROR!!!!   NO HAY ARCHIVO JSON!!!')
			txt.write('DEJA UN ARCHIVO JSON AL LADO DEL EXE!!!!')
			txt.close()


	def Horas_Mes_Asignatura(self,asignatura,alumno):
		# Se obtienen los dias de asistencia y se acortan a 3 letras (ordenados)
		self.D_suelto = self.DB.get_dias_sueltos(asignatura,alumno)

		if self.D_suelto!='---' and self.DB.get_Pagado(asignatura,alumno)!='Mes Completo':
			self.dias=[self.DB.get_dias_sueltos(asignatura,alumno)]
		else:
			self.dias = self.DB.Horarios[asignatura]['dias'][:]

		for dia in range(len(self.dias)):
			self.dias[dia]= self.DiaHor_rev[self.dias[dia][:3]]

		self.dias = self.dias[::-1]
		self.countdias=0
		for day in self.dias:
			for semana in self.calendario:
				for diasem in semana:
					if diasem[1]== day and diasem[0]!=0:
						self.countdias+=1

		return self.countdias


	def Exportar_Excel(self):
		self.Nombre_Archivo = str(self.DB.mes) + str(self.DB.year) + '.xlsx'
		self.wb = Workbook(self.Nombre_Archivo)
		self.ws1 = self.wb.add_worksheet(self.Nombre_Archivo)
		# print self.wb.worksheets()[0].get_name()

		# FORMATOS
		self.color='#FFFFFF'
		self.trasl = 5 #Traslacion que queremos aplicar para que empiezen los dias (desde col. Total Horas)
		self.ID=9 #COLUMNA DONDE INICIAN LOS DIAS
		self.ws1.set_column(3,3,20); self.ws1.set_column(4,4,12); self.ws1.set_column(self.ID,self.ID+len(self.dias_del_mes),5)
		self.formato_encabezado = self.wb.add_format({'border':1,'align':'center','bold':'True','bg_color':'#B8CCE4'})
		self.formato_subject = self.wb.add_format({'border':1,'align':'center','bold':'True','italic':'True','bg_color':'#00CCFF'})
		self.formato_pupil = self.wb.add_format({'border':1,'align':'center','bg_color':self.color})

		# Creamos el encabezado
		self.fila = 7;	self.columna = 3
		self.ws1.write(self.fila,self.columna,'MES:',self.formato_encabezado)
		self.ws1.write(self.fila,self.columna+1,self.DB.mes,self.formato_encabezado)
		self.ws1.write(self.fila+1,self.columna,'PROFESOR:',self.formato_encabezado)
		self.ws1.write(self.fila+1,self.columna+1,self.profesor,self.formato_encabezado)

		self.fila+=3
		self.ws1.write(self.fila,self.columna,'Nombre Alumno',self.formato_encabezado)
		self.ws1.write(self.fila,self.columna+1,'Total Horas',self.formato_encabezado)
		self.ws1.write(self.fila, self.columna + 2, 'Pagado', self.formato_encabezado)
		self.ws1.write(self.fila, self.columna + 3, 'Asistidas', self.formato_encabezado)
		self.ws1.write(self.fila, self.columna + 4, 'Faltas', self.formato_encabezado)
		# Se colocan los dias
		# for col in range(1,32):	self.ws1.write(self.fila,self.columna+2+col,col,self.formato_encabezado)


		for col in self.dias_del_mes.keys():
			self.ws1.write(self.fila,self.columna+self.trasl+col,col,self.formato_encabezado)
			self.ws1.write(self.fila+1, self.columna + self.trasl + col, self.DiaHor[self.dias_del_mes[col]], self.formato_encabezado)

		self.fila+=2
		self.contador = 0
		self.num_alumnos = 0
		for subject in self.DB.get_Asignaturas():
			self.ws1.write(self.fila,self.columna,subject,self.formato_subject)
			# self.HorasTotalMes = self.Horas_Mes_Asignatura(subject)
			self.fila+=1
			for alumno in self.DB.get_Alumnos(subject):
				self.HorasTotalMes = self.Horas_Mes_Asignatura(subject,alumno)
				if self.contador%2==0:	self.color='#D9D9D9'
				else: self.color='#FFFFFF'
				self.formato_pupil = self.wb.add_format({'border': 1, 'align': 'center', 'bg_color': self.color})
				if '_' in alumno: alumno=alumno.replace('_',' ')
				self.ws1.write(self.fila, self.columna, alumno, self.formato_pupil)
				self.Num_Ficha = str(self.DB.get_Numero_FICHA(subject,alumno))
				self.Pagado = self.DB.get_Pagado(subject,alumno)
				self.ws1.write(self.fila, self.columna-1, self.Num_Ficha, self.formato_pupil)

				self.col_mes_pag = self.columna+2 #Columna del PAGO DEL MES
				self.ws1.write(self.fila, self.col_mes_pag, self.Pagado, self.formato_pupil)
				self.ws1.set_column(self.col_mes_pag, self.col_mes_pag, 14)

				self.num_alumnos+=1

				self.horasAsistidas=0.0
				# self.horasFaltas=0.0
				for dia in self.dias_del_mes.keys():
					if str(dia) in self.DB.get_Asistencia(subject, alumno).keys():
						self.tiempo = self.DB.get_horas_dia_alumno(subject, alumno, str(dia))
						if self.tiempo!='X':
							self.ws1.write(self.fila, self.columna+dia+self.trasl, self.tiempo, self.formato_pupil)
							self.horasAsistidas+=float(self.tiempo[:-1])
						else:
							self.ws1.write(self.fila, self.columna + dia + self.trasl, self.tiempo, self.formato_pupil)
							# self.horasFaltas += float(self.tiempo[:-1])
					else:
						self.ws1.write(self.fila,self.columna+dia+self.trasl,'-',self.formato_pupil)


				self.horasbysem=self.DB.get_Pagado(subject,alumno)
				self.D_suelto = self.DB.get_dias_sueltos(subject, alumno)

				if self.horasbysem == 'Mes Completo':
					self.HorasPagadas = float(self.HorasTotalMes)*1.5
				elif self.D_suelto != '---':
					self.horasbysem = float(self.horasbysem.split('h')[0])
					self.HorasPagadas = round((float(self.HorasTotalMes) * self.horasbysem), 2)
				else:
					self.horasbysem = float(self.horasbysem.split('h')[0])
					self.HorasPagadas = round((float(self.HorasTotalMes)*1.5*self.horasbysem)/3.0,2)


				self.ws1.write(self.fila, self.columna + 1, self.HorasPagadas, self.formato_pupil)
				self.ws1.write(self.fila, self.columna + 3, self.horasAsistidas, self.formato_pupil)
				self.ws1.write(self.fila, self.columna + 4, self.HorasPagadas-self.horasAsistidas, self.formato_pupil)

				self.contador+=1
				self.fila+=1


			self.fila+=1

		self.ws1.write(11,3 , 'Total Alumnos: '+str(self.num_alumnos), self.formato_encabezado)
		self.wb.close()


Excel_Export().Exportar_Excel()

