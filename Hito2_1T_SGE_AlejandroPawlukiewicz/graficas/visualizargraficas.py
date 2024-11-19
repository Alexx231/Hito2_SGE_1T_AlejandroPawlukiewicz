# graficas/visualizargraficas.py
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from tkinter import messagebox

class VisualizadorGraficas:
    def __init__(self):
        plt.style.use('seaborn-v0_8-darkgrid')
        sns.set_theme()
        plt.rcParams['figure.figsize'] = [10, 6]
        plt.rcParams['figure.dpi'] = 100

    def crear_grafica_consumo_edad(self, datos):
        if datos is None or datos.empty:
            return None
            
        fig, ax = plt.subplots()
        sns.barplot(
            data=datos,
            x='edad',
            y='promedio_semanal',
            hue='Sexo',
            ax=ax
        )
        ax.set_title('Consumo por Edad')
        ax.set_xlabel('Edad')
        ax.set_ylabel('Bebidas por Semana')
        plt.tight_layout()
        return fig

    def crear_grafica_tendencia_temporal(self, datos):
        if datos is None or datos.empty:
            return None
            
        try:
            # Usar las columnas correctas que vienen de la base de datos
            fig = plt.figure(figsize=(10, 6))
            plt.plot(datos.index, datos['BebidasSemana'], marker='o', label='Bebidas por Semana')
            plt.plot(datos.index, datos['BebidasFinSemana'], marker='s', label='Bebidas Fin de Semana')
            
            plt.title('Tendencia de Consumo de Alcohol')
            plt.xlabel('Número de Encuesta')
            plt.ylabel('Consumo (unidades)')
            plt.legend()
            plt.grid(True)
            plt.tight_layout()
            return fig
        except Exception as e:
            print(f"Error al crear gráfica de tendencia: {str(e)}")
            return None

    def crear_grafica_problemas_salud(self, datos):
        if datos is None or datos.empty:
            return None
            
        # Transformar los datos para la visualización
        datos_melt = datos.melt(
            id_vars=['Sexo'],
            value_vars=[
                'problemas_digestivos',
                'tension_alta',
                'dolor_cabeza_frecuente'
            ],
            var_name='Problema',
            value_name='Cantidad'
        )
        
        fig, ax = plt.subplots()
        sns.barplot(
            data=datos_melt,
            x='Problema',
            y='Cantidad',
            hue='Sexo',
            ax=ax
        )
        
        # Personalizar la gráfica
        ax.set_title('Problemas de Salud por Género')
        ax.set_xlabel('Tipo de Problema')
        ax.set_ylabel('Cantidad de Casos')
        
        # Mejorar las etiquetas
        etiquetas = {
            'problemas_digestivos': 'Digestivos',
            'tension_alta': 'Tensión Alta',
            'dolor_cabeza_frecuente': 'Dolor Cabeza'
        }
        ax.set_xticklabels([etiquetas[x.get_text()] for x in ax.get_xticklabels()])
        
        plt.xticks(rotation=45)
        plt.tight_layout()
        return fig

    def crear_grafica_tendencia(self, datos):
        if datos is None or datos.empty:
            return None
            
        fig, ax = plt.subplots()
        sns.lineplot(
            data=datos,
            x='idEncuesta',
            y='BebidasSemana',
            ax=ax
        )
        ax.set_title('Tendencia de Consumo')
        ax.set_xlabel('ID Encuesta')
        ax.set_ylabel('Bebidas por Semana')
        plt.tight_layout()
        return fig