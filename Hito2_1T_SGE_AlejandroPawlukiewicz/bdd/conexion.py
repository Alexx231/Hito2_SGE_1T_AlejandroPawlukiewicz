# bdd/conexion.py
import mysql.connector
from mysql.connector import Error
from tkinter import messagebox

class ConexionBD:
    def __init__(self):
        try:
            print("Intentando conectar a MySQL...")
            self.conexion = mysql.connector.connect(
                host='localhost',
                user='root',
                password='Tcachuk93',
                port=3306,
                auth_plugin='mysql_native_password'  
            )
            
            if self.conexion.is_connected():
                db_info = self.conexion.get_server_info()
                print(f"Conexión exitosa a MySQL. Versión del servidor: {db_info}")
                cursor = self.conexion.cursor()
                
                # Crear y seleccionar la base de datos
                cursor.execute("CREATE DATABASE IF NOT EXISTS encuestas")
                cursor.execute("USE encuestas")
                
                print("Base de datos 'encuestas' seleccionada")
                cursor.close()
            else:
                raise Error("No se pudo establecer la conexión")
        except Error as e:
            print(f"Error de conexión: {str(e)}")
            messagebox.showerror("Error de Conexión","Verifica tus credenciales de MySQL y que el servidor esté activo")
            raise
        
    def cerrar_conexion(self):
        if self.conexion.is_connected():
            self.conexion.close()
            print("Conexión a MySQL cerrada")