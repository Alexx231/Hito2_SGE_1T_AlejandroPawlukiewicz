# bdd/consultas.py
import pandas as pd
from mysql.connector import Error

class ConsultasEncuesta:
    def __init__(self, conexion):
        self.conexion = conexion

    def ordenar_por_campo(self, campo):
        """Obtiene todos los registros ordenados por el campo especificado"""
        # Mapeo de nombres de columnas
        campo_map = {
            'fecha': 'idEncuesta',  # Usamos idEncuesta en lugar de fecha
            'alcohol': 'BebidasSemana',
            'presion': None,  # No existe esta columna
            'edad': 'edad',
            'problemas': 'ProblemasDigestivos'
        }
        
        campo_bd = campo_map.get(campo, campo)
        if not campo_bd:
            raise ValueError(f"Campo {campo} no existe en la base de datos")
            
        query = f"""
        SELECT * FROM encuesta 
        ORDER BY {campo_bd}
        """
        try:
            return pd.read_sql(query, self.conexion.conexion)
        except Error as e:
            raise Exception(f"Error al ordenar datos: {str(e)}")

    def insertar_encuesta(self, datos):
        query = """
        INSERT INTO encuesta (
            idEncuesta, edad, Sexo, 
            BebidasSemana, CervezasSemana, BebidasFinSemana, 
            BebidasDestiladasSemana, VinosSemana,
            PerdidasControl, DiversionDependenciaAlcohol,
            ProblemasDigestivos, TensionAlta, DolorCabeza
        ) VALUES (
            %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
        )
        """
        try:
            cursor = self.conexion.conexion.cursor()
            
            # Obtener siguiente ID
            cursor.execute("SELECT MAX(idEncuesta) FROM encuesta")
            max_id = cursor.fetchone()[0] or 0
            nuevo_id = max_id + 1

            # Convertir valores Sí/No a 1/0
            def convertir_si_no(valor):
                return 1 if valor.lower() == 'sí' else 0

            valores = (
                nuevo_id,
                int(datos['edad']),
                datos['sexo'],
                float(datos['bebidas_semana']),
                float(datos['cervezas']),
                float(datos['finde']),
                float(datos['destiladas']),
                float(datos['vinos']),
                convertir_si_no(datos['perdidas_control']),
                convertir_si_no(datos['diversion_alcohol']),
                convertir_si_no(datos['problemas_digestivos']),
                convertir_si_no(datos['tension_alta']),
                datos['dolor_cabeza']
            )
            
            cursor.execute(query, valores)
            self.conexion.conexion.commit()
            return True
            
        except Error as e:
            self.conexion.conexion.rollback()
            raise Exception(f"Error al insertar datos: {str(e)}")
        finally:
            cursor.close()
            
    def obtener_registros_recientes(self, limite=10):
        """
        Obtiene los registros más recientes de la base de datos
        """
        query = """
        SELECT 
            idEncuesta, 
            Sexo, 
            edad, 
            BebidasSemana,
            BebidasFinSemana,
            BebidasDestiladasSemana,
            VinosSemana,
            CervezasSemana
        FROM encuesta 
        ORDER BY idEncuesta DESC 
        LIMIT %s
        """
        try:
            return pd.read_sql(query, self.conexion.conexion, params=(limite,))
        except Exception as e:
            print(f"Error al obtener registros recientes: {e}")
            return pd.DataFrame()

    def obtener_tendencia_temporal(self):
        """Obtiene la tendencia del consumo por edad"""
        query = """
        SELECT 
            edad,
            AVG(BebidasSemana) as consumo_semanal,
            AVG(BebidasFinSemana) as consumo_finde
        FROM encuesta
        GROUP BY edad
        ORDER BY edad
        """
        return pd.read_sql(query, self.conexion.conexion)

    def obtener_estadisticas_consumo(self):
        """Obtiene estadísticas detalladas de consumo"""
        query = """
        SELECT 
            idEncuesta,
            edad,
            Sexo,
            BebidasSemana,
            CervezasSemana,
            BebidasFinSemana,
            BebidasDestiladasSemana,
            VinosSemana,
            AVG(BebidasSemana) as promedio_semanal,
            AVG(CervezasSemana) as promedio_cerveza,
            AVG(BebidasFinSemana) as promedio_finde,
            AVG(BebidasDestiladasSemana) as promedio_destiladas,
            AVG(VinosSemana) as promedio_vinos
        FROM encuesta
        GROUP BY idEncuesta, edad, Sexo, BebidasSemana, CervezasSemana, 
                BebidasFinSemana, BebidasDestiladasSemana, VinosSemana
        """
        try:
            return pd.read_sql(query, self.conexion.conexion)
        except Exception as e:
            print(f"Error en obtener_estadisticas_consumo: {str(e)}")
            return pd.DataFrame()  # Retorna DataFrame vacío en caso de error

    def filtrar_alto_consumo(self, limite=20):
        """Filtra registros con alto consumo de alcohol"""
        query = """
        SELECT 
            idEncuesta,
            edad,
            Sexo,
            BebidasSemana,
            CervezasSemana,
            BebidasFinSemana,
            BebidasDestiladasSemana,
            VinosSemana
        FROM encuesta 
        WHERE BebidasSemana > %s 
           OR BebidasFinSemana > %s
           OR CervezasSemana > %s
           OR BebidasDestiladasSemana > %s
           OR VinosSemana > %s
        ORDER BY BebidasSemana DESC
        LIMIT 100
        """
        params = (limite,) * 5
        return pd.read_sql(query, self.conexion.conexion, params=params)
    
    def filtrar_perdidas_control(self, min_perdidas=3):
        """
        Filtra pacientes que han perdido el control más veces que el mínimo especificado
        Args:
            min_perdidas: Número mínimo de pérdidas de control
        Returns:
            DataFrame con los pacientes filtrados
        """
        query = """
        SELECT 
            idEncuesta,
            Sexo,
            edad,
            PerdidasControl,
            BebidasSemana,
            BebidasFinSemana,
            CervezasSemana,
            BebidasDestiladasSemana,
            VinosSemana
        FROM encuesta 
        WHERE PerdidasControl >= %s
        ORDER BY PerdidasControl DESC
        """
        try:
            return pd.read_sql(query, self.conexion.conexion, params=(min_perdidas,))
        except Exception as e:
            print(f"Error al filtrar pérdidas de control: {e}")
            return pd.DataFrame()

    def filtrar_problemas_salud(self):
        """Analiza problemas de salud relacionados con el consumo"""
        query = """
        SELECT 
            Sexo,
            SUM(CASE WHEN ProblemasDigestivos = 'Sí' THEN 1 ELSE 0 END) as problemas_digestivos,
            SUM(CASE WHEN TensionAlta = 'Sí' THEN 1 ELSE 0 END) as tension_alta,
            SUM(CASE WHEN DolorCabeza IN ('A menudo', 'Muy a menudo') THEN 1 ELSE 0 END) as dolor_cabeza_frecuente,
            AVG(BebidasSemana) as promedio_consumo_semanal,
            COUNT(*) as total_casos
        FROM encuesta
        GROUP BY Sexo
        """
        return pd.read_sql(query, self.conexion.conexion)

    def obtener_correlacion_salud_consumo(self):
        """Analiza la correlación entre consumo y problemas de salud"""
        query = """
        SELECT 
            CASE 
                WHEN BebidasSemana = 0 THEN 'No consume'
                WHEN BebidasSemana <= 5 THEN 'Consumo bajo'
                WHEN BebidasSemana <= 15 THEN 'Consumo moderado'
                ELSE 'Consumo alto'
            END as nivel_consumo,
            COUNT(*) as total_personas,
            SUM(CASE WHEN ProblemasDigestivos = 'Sí' THEN 1 ELSE 0 END) as casos_digestivos,
            SUM(CASE WHEN TensionAlta = 'Sí' THEN 1 ELSE 0 END) as casos_tension,
            SUM(CASE WHEN DolorCabeza IN ('A menudo', 'Muy a menudo') THEN 1 ELSE 0 END) as casos_dolor_cabeza
        FROM encuesta
        GROUP BY 
            CASE 
                WHEN BebidasSemana = 0 THEN 'No consume'
                WHEN BebidasSemana <= 5 THEN 'Consumo bajo'
                WHEN BebidasSemana <= 15 THEN 'Consumo moderado'
                ELSE 'Consumo alto'
            END
        """
        return pd.read_sql(query, self.conexion.conexion)
    
    def actualizar_paciente(self, datos):
        """
        Actualiza los datos de un paciente existente
        Args:
            datos: Diccionario con los datos del paciente
        """
        query = """
        UPDATE encuesta 
        SET Sexo = %s,
            edad = %s,
            BebidasSemana = %s,
            CervezasSemana = %s,
            BebidasFinSemana = %s,
            BebidasDestiladasSemana = %s,
            VinosSemana = %s,
            PerdidasControl = %s,
            DiversionDependenciaAlcohol = %s,
            ProblemasDigestivos = %s,
            TensionAlta = %s,
            DolorCabeza = %s
        WHERE idEncuesta = %s
        """
        try:
            def convertir_si_no(valor):
                return 1 if valor else 0
    
            cursor = self.conexion.conexion.cursor()
            values = (
                datos['sexo'],
                int(datos['edad']),
                float(datos['bebidas_semana']),
                float(datos['cervezas']),
                float(datos['finde']),
                float(datos['destiladas']),
                float(datos['vinos']),
                convertir_si_no(datos['perdidas_control']),
                convertir_si_no(datos['diversion_alcohol']),
                convertir_si_no(datos['problemas_digestivos']),
                convertir_si_no(datos['tension_alta']),
                datos['dolor_cabeza'],
                int(datos['id'])
            )
            
            cursor.execute(query, values)
            self.conexion.conexion.commit()
            return True
        except Exception as e:
            self.conexion.conexion.rollback()
            raise Exception(f"Error al actualizar paciente: {str(e)}")
        finally:
            cursor.close()

    
    def obtener_listado_pacientes(self):
        """
        Obtiene el listado completo de pacientes de la base de datos
        :return: DataFrame con todos los pacientes
        """
        query = """
        SELECT 
            idEncuesta,
            NOW() as Fecha,  # Usamos NOW() como fecha temporal
            Sexo,
            edad,
            BebidasSemana,
            BebidasFinSemana,
            CervezasSemana,
            BebidasDestiladasSemana,
            VinosSemana
        FROM encuesta 
        ORDER BY idEncuesta DESC
        """
        try:
            return pd.read_sql(query, self.conexion.conexion)
        except Exception as e:
            print(f"Error al obtener listado de pacientes: {e}")
            raise Exception(f"Error al obtener listado de pacientes: {str(e)}")
        
    def obtener_paciente_por_id(self, id_paciente):
        """
        Obtiene los datos de un paciente por su ID
        Args:
            id_paciente: ID del paciente a buscar
        Returns:
            dict: Diccionario con los datos del paciente o None si no se encuentra
        """
        query = """
        SELECT 
            idEncuesta,
            Sexo,
            edad,
            BebidasSemana,
            BebidasFinSemana,
            CervezasSemana,
            BebidasDestiladasSemana,
            VinosSemana,
            PerdidasControl,
            DiversionDependenciaAlcohol,
            ProblemasDigestivos,
            TensionAlta,
            DolorCabeza
        FROM encuesta 
        WHERE idEncuesta = %s
        """
        try:
            with self.conexion.conexion.cursor(dictionary=True) as cursor:
                cursor.execute(query, (id_paciente,))
                return cursor.fetchone()
        except Exception as e:
            raise Exception(f"Error al obtener paciente: {str(e)}")

    def eliminar_paciente(self, id_paciente):
        """
        Elimina un paciente de la base de datos
        Args:
            id_paciente: ID del paciente a eliminar
        """
        try:
            cursor = self.conexion.conexion.cursor()
            query = "DELETE FROM encuesta WHERE idEncuesta = %s"
            cursor.execute(query, (id_paciente,))
            self.conexion.conexion.commit()
            cursor.close()
            return True
        except Exception as e:
            self.conexion.conexion.rollback()
            raise Exception(f"No se pudo eliminar el paciente: {str(e)}")

    def exportar_a_excel(self, df, nombre_archivo):
        """Exporta un DataFrame a Excel"""
        try:
            df.to_excel(nombre_archivo, index=False)
            return True
        except Exception as e:
            print(f"Error al exportar: {e}")
            return False