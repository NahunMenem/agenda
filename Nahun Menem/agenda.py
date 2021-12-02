from PyQt5.QtWidgets import QMainWindow, QApplication, QTableWidgetItem, QMessageBox
from PyQt5 import uic
import sqlite3


class MiVentana(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("agenda.ui", self)
        
        self.conexion = sqlite3.connect('agenda.db')
        self.cursor = self.conexion.cursor()
        self.operacion=''
        
        self.nuevo_b.clicked.connect(self.on_agregar)
        self.eliminar_b.clicked.connect(self.on_eliminar)
        self.editar_b.clicked.connect(self.on_editar)
        self.cancelar_b.clicked.connect(self.on_cancelar)
        self.aceptar_b.clicked.connect(self.on_aceptar)
        self.lista_w.itemClicked.connect(self.on_click)
        self.salir_b.clicked.connect(self.on_salir)
        
        self.cursor.execute('select * from contactos')
        
      
  # Se agregan los elementos al QListWidget
        for i in self.cursor:
            self.id = str(i[0]) 
            self.nombre = str(i[1])
            self.apellido = str(i[2])
           
            
            #self.lista_w.addItem(self.nombre + " - " + self.apellido + " - " + self.email+ " - " + self.telefono+ " - " + self.altura)
            self.lista_w.addItem(self.id + " - " +self.nombre + " - " + self.apellido )     
        
        
    def on_agregar(self):
        self.operacion='Agreg'
        self.editar_b.setEnabled(False)
        self.eliminar_b.setEnabled(False)
        self.cancelar_b.setEnabled(True)
        self.nuevo_b.setEnabled(False)
        self.nombre_e.setEnabled(True)
        self.apellido_e.setEnabled(True)
        self.email_e.setEnabled(True)
        self.telefono_e.setEnabled(True)
        self.direccion_e.setEnabled(True)
        self.fecha_n_e.setEnabled(True)
        self.altura_e.setEnabled(True) 
        self.peso_e.setEnabled(True)
        self.aceptar_b.setEnabled(True) 
        self.nombre_e.setText('')
        self.apellido_e.setText('')
        self.email_e.setText('')
        self.telefono_e.setText('')
        self.direccion_e.setText('')
        self.fecha_n_e.setText('')
        self.altura_e.setText('')
        self.peso_e.setText('')
        
        
        
        
    
        
    def on_click(self):
        self.editar_b.setEnabled(True)
        self.cancelar_b.setEnabled(True)
        self.nuevo_b.setEnabled(True)
        self.aceptar_b.setEnabled(False)
        self.eliminar_b.setEnabled(True)
        self.conexion = sqlite3.connect('agenda.db')
        self.cursor = self.conexion.cursor()
        ind= self.lista_w.currentItem().text()
        
        separador = ("-")
        contacto = ind.split(separador, 1)
        self.id_contacto=contacto[0]
        self.n_contacto=contacto[1]
        self.cursor.execute("select * from contactos  WHERE id = " + self.id_contacto)
        for i in self.cursor:
            
            self.nombre_e.setText(str(i[1]))
            self.apellido_e.setText(str(i[2]))
            self.email_e.setText(str(i[3]))
            self.telefono_e.setText(str(i[4]))
            self.direccion_e.setText(str(i[5]))
            self.fecha_n_e.setText(str(i[6])) 
            self.altura_e.setText(str(i[7])) 
            self.peso_e.setText(str(i[8])) 
            
           
    def on_editar(self):
        self.operacion='Modif'
        self.nuevo_b.setEnabled(False)
        self.editar_b.setEnabled(False)
        self.eliminar_b.setEnabled(False)
        self.aceptar_b.setEnabled(True) 
        self.nombre_e.setEnabled(True)
        self.apellido_e.setEnabled(True)
        self.email_e.setEnabled(True)
        self.telefono_e.setEnabled(True)
        self.direccion_e.setEnabled(True)
        self.fecha_n_e.setEnabled(True)
        self.altura_e.setEnabled(True) 
        self.peso_e.setEnabled(True)
        
    def on_eliminar(self):
        self.conexion = sqlite3.connect('agenda.db')
        self.cursor = self.conexion.cursor()
        ret = QMessageBox.question (self, 'Eliminar Contacto' , "Desea Eliminar el contacto '"+self.n_contacto+"'  Para Confirmar click en un botón Ok" , QMessageBox.Ok | QMessageBox.No | QMessageBox.Cancel, QMessageBox.Cancel)
        if ret == QMessageBox.Ok: 
                self.cursor.execute("DELETE FROM contactos  WHERE id = " + self.id_contacto)
                self.conexion.commit()
                self.lista_w.clear()
                self.cursor = self.conexion.cursor()
                self.cursor.execute('select * from contactos')
            # Se agregan los elementos al QListWidget
                for i in self.cursor:
                    self.id = str(i[0]) 
                    self.nombre = str(i[1])
                    self.apellido = str(i[2])
                    self.lista_w.addItem(self.id + " - " +self.nombre + " - " + self.apellido ) 
        self.habilitar_desabilitar()
        
        
        
    
    def on_aceptar(self):  
        self.nombre = self.nombre_e.text()
        self.apellido = self.apellido_e.text()
        self.email = self.email_e.text()
        self.telefono = self.telefono_e.text()
        self.direccion = self.direccion_e.text()
        self.fecha_nac = self.fecha_n_e.text()
        self.altura = self.altura_e.text()
        self.peso = self.peso_e.text()
        
        if self.nombre=='' or self.apellido=='' :
            QMessageBox.information(self, 'Informacion', "Los Datos Apellido y Nombre son obligatorios ",QMessageBox.Ok)
        
        else:
            try:
                float(self.altura)
                self.it_is = True
            except ValueError:
                self.it_is = False
            try:
                float(self.peso)
                self.it_is_p = True
            except ValueError:
                self.it_is_p = False    
                
                
            if self.it_is==False or self.it_is_p == False:
                if self.it_is==False:
                    QMessageBox.information(self, 'Informacion', "El dato ingresado en Altura no es un numero real ",QMessageBox.Ok)    
                if self.it_is_p==False:
                    QMessageBox.information(self, 'Informacion', "El dato ingresado en  Peso no es un numero real ",QMessageBox.Ok)    
            
            else:  
                self.conexion = sqlite3.connect('agenda.db')
                self.cursor = self.conexion.cursor()
                    
            
                if self.operacion=='Agreg':
                    ret = QMessageBox.question (self, 'Nuevo Contacto' , "¿Esta seguro que desea agregar este item?" , QMessageBox.Ok | QMessageBox.No | QMessageBox.Cancel, QMessageBox.Cancel)
                    if ret == QMessageBox.Ok: 
                    
                        self.cursor.execute("INSERT INTO contactos(nombre,apellido,email,telefono,direccion,fecha_nac,altura,peso) VALUES ('"+self.nombre+"','"+self.apellido+"','"+self.email+"', '"+self.telefono+"','"+self.direccion+"','"+self.fecha_nac+"','"+self.altura+"','"+self.peso+"')")
                        
                        self.conexion.commit() 
                    
                
                if self.operacion=='Modif':
                    ret = QMessageBox.question (self, 'Editar Contacto' , "¿Esta seguro que desea modificar este Item?" , QMessageBox.Ok | QMessageBox.No | QMessageBox.Cancel, QMessageBox.Cancel)
                    if ret == QMessageBox.Ok: 
                    
                        
                        self.cursor.execute("UPDATE contactos SET nombre='"+self.nombre+"', apellido='"+self.apellido+"', email='"+self.email+"', telefono='"+self.telefono+"',direccion='"+self.direccion+"',fecha_nac='"+self.fecha_nac+"',altura='"+self.altura+"',peso='"+self.peso+"' WHERE id = " + self.id_contacto)
                        self.conexion.commit()
                        
            
                
                
                    
                if ret == QMessageBox.Ok:  
                    self.lista_w.clear()
                    self.cursor = self.conexion.cursor()
                    self.cursor.execute('select * from contactos')
                    # Se agregan los elementos al QListWidget
                    for i in self.cursor:
                            self.id = str(i[0]) 
                            self.nombre = str(i[1])
                            self.apellido = str(i[2])
                            self.lista_w.addItem(self.id + " - " +self.nombre + " - " + self.apellido ) 
                self.habilitar_desabilitar()
            
    def habilitar_desabilitar(self):            
        # botones
        self.nuevo_b.setEnabled(True)   
        self.editar_b.setEnabled(False)
        self.cancelar_b.setEnabled(False)
        self.eliminar_b.setEnabled(False)
        self.aceptar_b.setEnabled(False)
        
        self.nombre_e.setEnabled(False)
        self.apellido_e.setEnabled(False)
        self.email_e.setEnabled(False)
        self.telefono_e.setEnabled(False)
        self.direccion_e.setEnabled(False)
        self.fecha_n_e.setEnabled(False)
        self.altura_e.setEnabled(False) 
        self.peso_e.setEnabled(False)
        
        self.nombre_e.setText('')
        self.apellido_e.setText('')
        self.email_e.setText('')
        self.telefono_e.setText('')
        self.direccion_e.setText('')
        self.fecha_n_e.setText('')
        self.altura_e.setText('')
        self.peso_e.setText('')
         
             
    def on_cancelar(self):
        self.habilitar_desabilitar()
    
    def on_salir(self):
        exit()    
        
        



app = QApplication([])

win = MiVentana()
win.show()

app.exec_()



