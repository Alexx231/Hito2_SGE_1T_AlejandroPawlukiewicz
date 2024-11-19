# interfazusuario.py
import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from datetime import datetime

class InterfazSaludAlcohol:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Monitoreo de Salud")
        
        # Inicializar campos de entrada
        self.entrada_fecha = None
        self.entrada_sexo = None
        self.entrada_edad = None
        self.entrada_alcohol = None
        self.entrada_presion = None
        self.entrada_problemas = None
        self.entrada_bebidas_semana = None
        self.entrada_cervezas = None
        self.entrada_finde = None
        self.entrada_destiladas = None
        self.entrada_vinos = None
        self.entrada_perdidas_control = None
        self.entrada_diversion_alcohol = None
        self.entrada_problemas_digestivos = None
        self.entrada_tension_alta = None
        self.entrada_dolor_cabeza = None
        
        # Campos para actualización
        self.entrada_id_busqueda = None
        self.entrada_fecha_act = None 
        self.entrada_edad_act = None
        self.entrada_sexo_act = None
        self.entrada_bebidas_semana_act = None
        self.entrada_cervezas_act = None
        self.entrada_finde_act = None
        self.entrada_destiladas_act = None
        self.entrada_vinos_act = None
        self.entrada_perdidas_control_act = None
        self.entrada_diversion_alcohol_act = None  
        self.entrada_problemas_digestivos_act = None
        self.entrada_tension_alta_act = None
        self.entrada_dolor_cabeza_act = None
        
        # Inicializar callbacks
        self._registrar_callback = None
        self._visualizar_callback = None
        self._estadisticas_callback = None
        self._exportar_callback = None
        self._buscar_callback = None
        self._actualizar_callback = None
        self._eliminar_callback = None
        
        # Crear componentes principales
        self.crear_notebook()
        self.crear_menu()
        self.crear_panel_registro()
        self.crear_panel_visualizacion()
        self.crear_panel_estadisticas()
        self.crear_panel_actualizar()
        self.crear_panel_listado()
        
        # Inicializar canvas
        self.canvas = None

    def crear_notebook(self):
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill='both', expand=True)
        
        self.tab_registro = ttk.Frame(self.notebook)
        self.tab_visualizacion = ttk.Frame(self.notebook)
        self.tab_estadisticas = ttk.Frame(self.notebook)
        self.tab_listado = ttk.Frame(self.notebook)  # Nueva pestaña
        
        self.notebook.add(self.tab_registro, text='Registro')
        self.notebook.add(self.tab_listado, text='Listado Pacientes')
        self.tab_actualizar = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_actualizar, text='Actualizar Paciente')
        self.notebook.add(self.tab_visualizacion, text='Visualización')
        self.notebook.add(self.tab_estadisticas, text='Estadísticas')

    def crear_menu(self):
        menu_bar = tk.Menu(self.root)
        self.root.config(menu=menu_bar)
        
        # Menú Archivo
        file_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="Archivo", menu=file_menu)
        file_menu.add_command(label="Exportar a Excel", 
                            command=lambda: self._exportar_callback("excel") if self._exportar_callback else None)
        file_menu.add_separator()
        file_menu.add_command(label="Salir", command=self.root.quit)
        
        # Menú Consultas
        query_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="Consultas", menu=query_menu)
        query_menu.add_command(label="Ver Estadísticas", 
                            command=lambda: self.notebook.select(self.tab_estadisticas))
        query_menu.add_command(label="Actualizar Paciente", 
                            command=lambda: self.notebook.select(self.tab_actualizar))

    def _crear_seccion_campos(self, titulo, campos, frame_principal):
        """
        Crea una sección de campos en el formulario
        Args:
            titulo (str): Título de la sección
            campos (list): Lista de tuplas con la información de los campos
            frame_principal (ttk.Frame): Frame contenedor
        """
        frame = ttk.LabelFrame(frame_principal, text=titulo, style="Custom.TLabelframe")
        frame.pack(fill='x', padx=20, pady=10)

        frame_grid = ttk.Frame(frame)
        frame_grid.pack(padx=15, pady=15)

        for i, campo in enumerate(campos):
            if len(campo) == 4:  # Campo con etiqueta, nombre, ancho y hint
                label, attr, width, hint = campo
                ttk.Label(frame_grid, text=label).grid(row=i, column=0, padx=10, pady=8, sticky='e')
                setattr(self, attr, ttk.Entry(frame_grid, width=width))
                getattr(self, attr).grid(row=i, column=1, padx=10, pady=8, sticky='w')
                if hint:
                    ttk.Label(frame_grid, text=hint, foreground="gray").grid(row=i, column=2, padx=5, pady=8, sticky='w')
            
            elif len(campo) == 3:  # Campo con etiqueta, nombre y opciones
                label, attr, opciones = campo
                ttk.Label(frame_grid, text=label).grid(row=i, column=0, padx=10, pady=8, sticky='e')
                setattr(self, attr, ttk.Combobox(frame_grid, values=opciones, state='readonly'))
                getattr(self, attr).grid(row=i, column=1, padx=10, pady=8, sticky='w')
                getattr(self, attr).set(opciones[0])

    def crear_panel_registro(self):
        """Crea un panel de registro mejorado y más intuitivo"""
        frame_principal = ttk.Frame(self.tab_registro, style="Custom.TLabelframe")
        frame_principal.pack(padx=30, pady=20, fill='both', expand=True)
        
        # Título principal
        titulo = ttk.Label(frame_principal, 
                        text="REGISTRO DE PACIENTE",
                        style="Title.TLabel")
        titulo.pack(pady=(0, 20))
    
        # Sección de datos personales
        frame_datos = ttk.LabelFrame(frame_principal, text="Datos Personales")
        frame_datos.pack(fill='x', padx=20, pady=10)
        
        frame_grid = ttk.Frame(frame_datos)
        frame_grid.pack(padx=15, pady=15)
        
        # Datos Personales
        ttk.Label(frame_grid, text="Fecha:").grid(row=0, column=0, padx=10, pady=8, sticky='e')
        self.entrada_fecha = ttk.Entry(frame_grid, width=15)
        self.entrada_fecha.grid(row=0, column=1, padx=10, pady=8, sticky='w')
        ttk.Label(frame_grid, text="(YYYY-MM-DD)", foreground="gray").grid(row=0, column=2, pady=8, sticky='w')
        
        ttk.Label(frame_grid, text="Edad:").grid(row=1, column=0, padx=10, pady=8, sticky='e')
        self.entrada_edad = ttk.Entry(frame_grid, width=5)
        self.entrada_edad.grid(row=1, column=1, padx=10, pady=8, sticky='w')
        ttk.Label(frame_grid, text="años", foreground="gray").grid(row=1, column=2, pady=8, sticky='w')
        
        ttk.Label(frame_grid, text="Sexo:").grid(row=2, column=0, padx=10, pady=8, sticky='e')
        self.entrada_sexo = ttk.Combobox(frame_grid, values=["Hombre", "Mujer"], state='readonly')
        self.entrada_sexo.grid(row=2, column=1, padx=10, pady=8, sticky='w')
        self.entrada_sexo.set("Hombre")
    
        # Sección de Consumo de Alcohol
        frame_consumo = ttk.LabelFrame(frame_principal, text="Consumo de Alcohol")
        frame_consumo.pack(fill='x', padx=20, pady=10)
        frame_grid_consumo = ttk.Frame(frame_consumo)
        frame_grid_consumo.pack(padx=15, pady=15)
    
        # Campos de Consumo
        campos_consumo = [
            ("Bebidas por Semana:", "bebidas_semana", 5),
            ("Cervezas por Semana:", "cervezas", 5),
            ("Bebidas Fin de Semana:", "finde", 5),
            ("Bebidas Destiladas:", "destiladas", 5),
            ("Vinos por Semana:", "vinos", 5)
        ]
    
        for i, (label, nombre, width) in enumerate(campos_consumo):
            ttk.Label(frame_grid_consumo, text=label).grid(row=i, column=0, padx=10, pady=8, sticky='e')
            setattr(self, f'entrada_{nombre}', ttk.Entry(frame_grid_consumo, width=width))
            getattr(self, f'entrada_{nombre}').grid(row=i, column=1, padx=10, pady=8, sticky='w')
            ttk.Label(frame_grid_consumo, text="unidades", foreground="gray").grid(row=i, column=2, pady=8, sticky='w')
    
        # Sección de Salud
        frame_salud = ttk.LabelFrame(frame_principal, text="Datos de Salud")
        frame_salud.pack(fill='x', padx=20, pady=10)
        frame_grid_salud = ttk.Frame(frame_salud)
        frame_grid_salud.pack(padx=15, pady=15)
    
        # Campos de Salud
        campos_salud = [
            ("Pérdidas de Control:", "perdidas_control", ["Sí", "No"]),
            ("Diversión Depende del Alcohol:", "diversion_alcohol", ["Sí", "No"]),
            ("Problemas Digestivos:", "problemas_digestivos", ["Sí", "No"]),
            ("Tensión Alta:", "tension_alta", ["Sí", "No"]),
            ("Frecuencia Dolor de Cabeza:", "dolor_cabeza", 
             ["Nunca", "Raramente", "A menudo", "Muy a menudo"])
        ]
    
        for i, (label, nombre, opciones) in enumerate(campos_salud):
            ttk.Label(frame_grid_salud, text=label).grid(row=i, column=0, padx=10, pady=8, sticky='e')
            setattr(self, f'entrada_{nombre}', ttk.Combobox(frame_grid_salud, values=opciones, state='readonly'))
            getattr(self, f'entrada_{nombre}').grid(row=i, column=1, padx=10, pady=8, sticky='w')
            getattr(self, f'entrada_{nombre}').set(opciones[0])
    
        # Frame para botones
        frame_botones = ttk.Frame(frame_principal)
        frame_botones.pack(pady=25)
        
        # Botones mejorados
        ttk.Button(frame_botones,
                text="Limpiar Formulario",
                style="Secondary.TButton",
                command=self.limpiar_formulario).pack(side='left', padx=15)
        ttk.Button(frame_botones,
                text="Registrar Paciente",
                style="Primary.TButton",
                command=self._on_registrar).pack(side='left', padx=15)
    
        # Configurar validación después de crear todos los widgets
        self._configurar_validacion()
        
    def crear_panel_listado(self):
        frame = ttk.LabelFrame(self.tab_listado, text="Listado de Pacientes")
        frame.pack(padx=10, pady=10, fill='both', expand=True)
        
        # Crear Treeview para el listado
        columns = ('ID', 'Fecha', 'Sexo', 'Edad', 'Bebidas/Sem', 'Fin Sem', 'Cervezas', 'Destiladas', 'Vinos')
        self.tree_pacientes = ttk.Treeview(frame, columns=columns, show='headings', height=15)
        
        # Configurar columnas
        for col in columns:
            self.tree_pacientes.heading(col, text=col)
            self.tree_pacientes.column(col, width=80)
        
        # Scrollbars
        scrolly = ttk.Scrollbar(frame, orient='vertical', command=self.tree_pacientes.yview)
        scrollx = ttk.Scrollbar(frame, orient='horizontal', command=self.tree_pacientes.xview)
        self.tree_pacientes.configure(yscrollcommand=scrolly.set, xscrollcommand=scrollx.set)
        
        # Evento de doble clic para eliminar
        self.tree_pacientes.bind('<Double-1>', self._on_doble_click_paciente)
        
        # Empaquetar componentes
        self.tree_pacientes.pack(side='left', fill='both', expand=True)
        scrolly.pack(side='right', fill='y')
        scrollx.pack(side='bottom', fill='x')
    
    def crear_panel_actualizar(self):
        frame = ttk.LabelFrame(self.tab_actualizar, text="Actualizar Paciente")
        frame.pack(padx=10, pady=10, fill='both', expand=True)
        
        # Frame búsqueda
        frame_busqueda = ttk.Frame(frame)
        frame_busqueda.pack(fill='x', padx=5, pady=5)
        
        ttk.Label(frame_busqueda, text="ID Paciente:").pack(side='left', padx=5)
        self.entrada_id_busqueda = ttk.Entry(frame_busqueda, width=10)
        self.entrada_id_busqueda.pack(side='left', padx=5)
        
        ttk.Button(frame_busqueda, 
                text="Buscar",
                command=self._buscar_paciente).pack(side='left', padx=5)

        # Frame principal para los datos
        self.frame_actualizar = ttk.Frame(frame)
        self.frame_actualizar.pack(fill='both', expand=True, padx=5, pady=5)
        
        # Desactivar frame de actualización hasta que se busque un paciente
        for child in self.frame_actualizar.winfo_children():
            child.configure(state='disabled')
    
        # Frame principal para los datos
        frame_principal = ttk.Frame(frame)
        frame_principal.pack(fill='both', expand=True, padx=5, pady=5)
    
        # Sección de datos personales
        frame_datos = ttk.LabelFrame(frame_principal, text="Datos Personales")
        frame_datos.pack(fill='x', padx=20, pady=10)
        
        frame_grid = ttk.Frame(frame_datos)
        frame_grid.pack(padx=15, pady=15)
        
        # Datos Personales
        ttk.Label(frame_grid, text="Fecha:").grid(row=0, column=0, padx=10, pady=8, sticky='e')
        self.entrada_fecha_act = ttk.Entry(frame_grid, width=15)
        self.entrada_fecha_act.grid(row=0, column=1, padx=10, pady=8, sticky='w')
        ttk.Label(frame_grid, text="(YYYY-MM-DD)", foreground="gray").grid(row=0, column=2, pady=8, sticky='w')
        
        ttk.Label(frame_grid, text="Edad:").grid(row=1, column=0, padx=10, pady=8, sticky='e')
        self.entrada_edad_act = ttk.Entry(frame_grid, width=5)
        self.entrada_edad_act.grid(row=1, column=1, padx=10, pady=8, sticky='w')
        ttk.Label(frame_grid, text="años", foreground="gray").grid(row=1, column=2, pady=8, sticky='w')
        
        ttk.Label(frame_grid, text="Sexo:").grid(row=2, column=0, padx=10, pady=8, sticky='e')
        self.entrada_sexo_act = ttk.Combobox(frame_grid, values=["Hombre", "Mujer"], state='readonly')
        self.entrada_sexo_act.grid(row=2, column=1, padx=10, pady=8, sticky='w')
        
        # Sección de Consumo de Alcohol
        frame_consumo = ttk.LabelFrame(frame_principal, text="Consumo de Alcohol")
        frame_consumo.pack(fill='x', padx=20, pady=10)
        frame_grid_consumo = ttk.Frame(frame_consumo)
        frame_grid_consumo.pack(padx=15, pady=15)
    
        # Campos de Consumo
        campos_consumo = [
            ("Bebidas por Semana:", "bebidas_semana_act", 5),
            ("Cervezas por Semana:", "cervezas_act", 5),
            ("Bebidas Fin de Semana:", "finde_act", 5),
            ("Bebidas Destiladas:", "destiladas_act", 5),
            ("Vinos por Semana:", "vinos_act", 5)
        ]
    
        for i, (label, nombre, width) in enumerate(campos_consumo):
            ttk.Label(frame_grid_consumo, text=label).grid(row=i, column=0, padx=10, pady=8, sticky='e')
            setattr(self, f'entrada_{nombre}', ttk.Entry(frame_grid_consumo, width=width))
            getattr(self, f'entrada_{nombre}').grid(row=i, column=1, padx=10, pady=8, sticky='w')
            ttk.Label(frame_grid_consumo, text="unidades", foreground="gray").grid(row=i, column=2, pady=8, sticky='w')
    
        # Sección de Salud
        frame_salud = ttk.LabelFrame(frame_principal, text="Datos de Salud")
        frame_salud.pack(fill='x', padx=20, pady=10)
        frame_grid_salud = ttk.Frame(frame_salud)
        frame_grid_salud.pack(padx=15, pady=15)
    
        # Campos de Salud
        campos_salud = [
            ("Pérdidas de Control:", "perdidas_control_act", ["Sí", "No"]),
            ("Diversión Depende del Alcohol:", "diversion_alcohol_act", ["Sí", "No"]),
            ("Problemas Digestivos:", "problemas_digestivos_act", ["Sí", "No"]),
            ("Tensión Alta:", "tension_alta_act", ["Sí", "No"]),
            ("Frecuencia Dolor de Cabeza:", "dolor_cabeza_act", 
             ["Nunca", "Raramente", "A menudo", "Muy a menudo"])
        ]
    
        for i, (label, nombre, opciones) in enumerate(campos_salud):
            ttk.Label(frame_grid_salud, text=label).grid(row=i, column=0, padx=10, pady=8, sticky='e')
            setattr(self, f'entrada_{nombre}', ttk.Combobox(frame_grid_salud, values=opciones, state='readonly'))
            getattr(self, f'entrada_{nombre}').grid(row=i, column=1, padx=10, pady=8, sticky='w')
            getattr(self, f'entrada_{nombre}').set(opciones[0])
    
        # Frame para botones
        frame_botones = ttk.Frame(self.frame_actualizar)
        frame_botones.pack(pady=25)
        
        # Botón para guardar cambios
        self.boton_guardar = ttk.Button(frame_botones,
                                    text="Guardar Cambios",
                                    style="Primary.TButton",
                                    command=self._guardar_actualizacion,
                                    state='disabled')
        self.boton_guardar.pack(side='left', padx=15)
        
    def registrar_buscar_callback(self, callback):
        """Registra el callback para búsqueda de pacientes"""
        if callable(callback):
            self._buscar_callback = callback

    def registrar_actualizar_callback(self, callback):
        """Registra el callback para actualización de pacientes"""
        if callable(callback):
            self._actualizar_callback = callback

    def _buscar_paciente(self):
        if hasattr(self, '_buscar_callback') and callable(self._buscar_callback):
            id_paciente = self.entrada_id_busqueda.get().strip()
            if id_paciente:
                self._buscar_callback(id_paciente)

    def _guardar_actualizacion(self):
        if hasattr(self, '_actualizar_callback') and callable(self._actualizar_callback):
            datos = self.obtener_datos_formulario_actualizacion()
            if datos:
                self._actualizar_callback(datos)

    def mostrar_datos_paciente(self, datos):
        if datos is not None:
            try:
                # Habilitar campos para edición
                for widget in self.frame_actualizar.winfo_children():
                    try:
                        widget.configure(state='normal')
                    except:
                        pass
    
                # Rellenar campos con los datos existentes
                self.entrada_edad_act.delete(0, tk.END)
                self.entrada_edad_act.insert(0, str(datos['edad']))
                
                self.entrada_sexo_act.set(datos['Sexo'])
                
                self.entrada_bebidas_semana_act.delete(0, tk.END)
                self.entrada_bebidas_semana_act.insert(0, str(datos['BebidasSemana']))
                
                self.entrada_cervezas_act.delete(0, tk.END)
                self.entrada_cervezas_act.insert(0, str(datos['CervezasSemana']))
                
                self.entrada_finde_act.delete(0, tk.END)
                self.entrada_finde_act.insert(0, str(datos['BebidasFinSemana']))
                
                self.entrada_destiladas_act.delete(0, tk.END)
                self.entrada_destiladas_act.insert(0, str(datos['BebidasDestiladasSemana']))
                
                self.entrada_vinos_act.delete(0, tk.END)
                self.entrada_vinos_act.insert(0, str(datos['VinosSemana']))
    
                # Habilitar botón de guardar
                self.boton_guardar.configure(state='normal')
                
            except Exception as e:
                messagebox.showerror("Error", f"Error al mostrar datos del paciente: {str(e)}")
        
    def obtener_datos_formulario_actualizacion(self):
        """
        Obtiene los datos del formulario de actualización
        Returns:
            dict: Diccionario con los datos o None si hay error
        """
        try:
            datos = {
                'id': self.entrada_id_busqueda.get().strip(),
                'fecha': self.entrada_fecha_act.get().strip(),
                'edad': self.entrada_edad_act.get().strip(),
                'sexo': self.entrada_sexo_act.get(),
                'bebidas_semana': self.entrada_bebidas_semana_act.get().strip(),
                'cervezas': self.entrada_cervezas_act.get().strip(),
                'finde': self.entrada_finde_act.get().strip(),
                'destiladas': self.entrada_destiladas_act.get().strip(),
                'vinos': self.entrada_vinos_act.get().strip(),
                'perdidas_control': self.entrada_perdidas_control_act.get() == 'Sí',
                'diversion_alcohol': self.entrada_diversion_alcohol_act.get() == 'Sí',
                'problemas_digestivos': self.entrada_problemas_digestivos_act.get() == 'Sí',
                'tension_alta': self.entrada_tension_alta_act.get() == 'Sí',
                'dolor_cabeza': self.entrada_dolor_cabeza_act.get()
            }
            
            # Validar datos
            if not all(str(v).strip() for v in datos.values() if not isinstance(v, bool)):
                raise ValueError("Todos los campos son obligatorios")
                
            return datos
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al obtener datos: {str(e)}")
            return None
            
    def _guardar_actualizacion(self):
        if messagebox.askyesno("Confirmar actualización", 
                            "¿Está seguro de que desea actualizar los datos del paciente?"):
            if hasattr(self, '_actualizar_callback'):
                datos = self.obtener_datos_formulario_actualizacion()
                if datos:
                    self._actualizar_callback(datos)
                    # Deshabilitar campos después de actualizar
                    for child in self.frame_actualizar.winfo_children():
                        child.configure(state='disabled')
                    self.boton_guardar.configure(state='disabled')
        
    def _configurar_validacion(self):
        """Configura la validación de campos con feedback mejorado"""
        try:
            # Configurar estilos de validación
            style = ttk.Style()
            style.configure('Error.TEntry',
                        fieldbackground='#ffd1d1',
                        bordercolor='#ff0000')
            style.configure('Warning.TEntry',
                        fieldbackground='#fff3cd',
                        bordercolor='#ffeeba')
            style.configure('Valid.TEntry',
                        fieldbackground='#d4edda',
                        bordercolor='#c3e6cb')
    
            # Función genérica para validar campos numéricos
            def validar_numerico(widget, min_val=0, max_val=None, mensaje=""):
                def _validar(event):
                    try:
                        valor = widget.get().strip()
                        if not valor:
                            widget.configure(style='Warning.TEntry')
                            self._mostrar_tooltip(widget, "Campo requerido")
                            return False
                            
                        valor = float(valor)
                        if valor < min_val or (max_val and valor > max_val):
                            raise ValueError(f"Valor fuera de rango ({min_val}-{max_val if max_val else 'inf'})")
                            
                        widget.configure(style='Valid.TEntry')
                        self._ocultar_tooltip(widget)
                        return True
                        
                    except ValueError:
                        widget.configure(style='Error.TEntry')
                        self._mostrar_tooltip(widget, mensaje)
                        return False
                return _validar
    
            # Función para validar fecha
            def validar_fecha(event):
                try:
                    fecha = self.entrada_fecha.get().strip()
                    if not fecha:
                        self.entrada_fecha.configure(style='Warning.TEntry')
                        self._mostrar_tooltip(self.entrada_fecha, "La fecha es obligatoria")
                        return
                        
                    datetime.strptime(fecha, '%Y-%m-%d')
                    self.entrada_fecha.configure(style='Valid.TEntry')
                    self._ocultar_tooltip(self.entrada_fecha)
                    
                except ValueError:
                    self.entrada_fecha.configure(style='Error.TEntry')
                    self._mostrar_tooltip(self.entrada_fecha, "Formato inválido (YYYY-MM-DD)")
    
            # Configurar validaciones solo si los widgets existen
            widgets_validacion = {
                'entrada_fecha': (validar_fecha, None),
                'entrada_edad': (validar_numerico, {'min_val': 0, 'max_val': 120, 'mensaje': "Edad inválida (0-120)"}),
                'entrada_alcohol': (validar_numerico, {'min_val': 0, 'mensaje': "Cantidad inválida"})
            }
    
            # Campos de consumo
            campos_consumo = [
                'bebidas_semana', 'cervezas', 'finde', 'destiladas', 'vinos'
            ]
    
            # Agregar campos de consumo a la validación
            for campo in campos_consumo:
                widgets_validacion[f'entrada_{campo}'] = (
                    validar_numerico, 
                    {'min_val': 0, 'mensaje': "Cantidad inválida"}
                )
    
            # Aplicar validaciones
            for widget_name, (validator, params) in widgets_validacion.items():
                if hasattr(self, widget_name) and getattr(self, widget_name) is not None:
                    widget = getattr(self, widget_name)
                    if params is None:
                        widget.bind('<FocusOut>', validator)
                    else:
                        widget.bind('<FocusOut>', validator(widget, **params))
    
        except Exception as e:
            print(f"Error al configurar validación: {str(e)}")
    
    def _mostrar_tooltip(self, widget, mensaje):
        """Muestra un tooltip con el mensaje de error"""
        try:
            x, y, _, _ = widget.bbox("insert")
            x += widget.winfo_rootx() + 25
            y += widget.winfo_rooty() + 20
    
            self.tooltip = tk.Toplevel(widget)
            self.tooltip.wm_overrideredirect(True)
            self.tooltip.wm_geometry(f"+{x}+{y}")
    
            label = ttk.Label(self.tooltip, text=mensaje,
                             justify='left',
                             background="#ffeeee",
                             relief='solid',
                             borderwidth=1,
                             font=("Segoe UI", 9))
            label.pack()
            
        except Exception as e:
            print(f"Error al mostrar tooltip: {e}")
    
    def _ocultar_tooltip(self, widget):
        """Oculta el tooltip si existe"""
        if hasattr(self, 'tooltip'):
            self.tooltip.destroy()

    
    def crear_panel_visualizacion(self):
        """Crea el panel de visualización de gráficas"""
        self.frame_grafico = ttk.LabelFrame(self.tab_visualizacion, text="Gráficos")
        self.frame_grafico.pack(padx=10, pady=10, fill='both', expand=True)
        
        # Panel de controles
        frame_controles = ttk.Frame(self.frame_grafico)
        frame_controles.pack(fill='x', padx=5, pady=5)
        
        # Selector de tipo de gráfica
        ttk.Label(frame_controles, text="Tipo de Gráfica:").pack(side='left', padx=5)
        self.tipo_grafica = ttk.Combobox(
            frame_controles,
            values=[
                'Consumo por Edad',
                'Problemas de Salud',
                'Tendencia Temporal'
            ],
            state='readonly',
            width=30
        )
        self.tipo_grafica.pack(side='left', padx=5)
        self.tipo_grafica.set('Consumo por Edad')
        
        # Frame para contener el gráfico
        self.frame_figura = ttk.Frame(self.frame_grafico)
        self.frame_figura.pack(fill='both', expand=True, padx=5, pady=5)
        
        # Botón actualizar
        ttk.Button(
            frame_controles,
            text="Mostrar Gráfica",
            command=self._on_visualizar
        ).pack(side='right', padx=5)

    def crear_panel_estadisticas(self):
        self.frame_estadisticas = ttk.LabelFrame(self.tab_estadisticas, text="Estadísticas")
        self.frame_estadisticas.pack(padx=10, pady=10, fill='both', expand=True)
        
        ttk.Button(self.frame_estadisticas, text="Actualizar Estadísticas",
                command=self._on_estadisticas).pack(pady=5)
    

    def registrar_callback(self, callback):
        self._registrar_callback = callback

    def visualizar_callback(self, callback):
        self._visualizar_callback = callback

    def estadisticas_callback(self, callback):
        self._estadisticas_callback = callback

    def exportar_callback(self, callback):
        self._exportar_callback = callback

    def eliminar_callback(self, callback):
        """
        Registra el callback para eliminar pacientes
        Args:
            callback: Función a llamar cuando se quiera eliminar un paciente
        """
        self._eliminar_callback = callback

    def _on_registrar(self):
        """Maneja el evento de registro de paciente"""
        if self._registrar_callback:
            datos = self.obtener_datos_formulario()
            if datos:  # Verifica que se obtuvieron datos válidos
                if self._registrar_callback(datos):  # Llama al callback con los datos
                    # Si el registro fue exitoso, limpiar el formulario
                    self.limpiar_formulario()
    

    def _on_visualizar(self):
        if self._visualizar_callback:
            self._visualizar_callback()

    def _on_estadisticas(self):
        if self._estadisticas_callback:
            self._estadisticas_callback()
            
    def obtener_datos_formulario(self):
        """
        Obtiene y valida los datos del formulario.
        Returns:
            dict: Diccionario con los datos validados o None si hay error
        """
        try:
            # Verificar que los widgets existan
            widgets_requeridos = [
                'entrada_fecha', 
                'entrada_edad', 
                'entrada_sexo',
                'entrada_bebidas_semana',
                'entrada_cervezas',
                'entrada_finde',
                'entrada_destiladas',
                'entrada_vinos',
                'entrada_perdidas_control',
                'entrada_diversion_alcohol',
                'entrada_problemas_digestivos',
                'entrada_tension_alta',
                'entrada_dolor_cabeza'
            ]
    
            # Verificar existencia de widgets
            for widget in widgets_requeridos:
                if not hasattr(self, widget) or getattr(self, widget) is None:
                    raise ValueError(f"Campo {widget} no inicializado")
    
            # Obtener y validar datos
            datos = {}
            
            # Campos de texto con strip()
            campos_texto = {
                'fecha': self.entrada_fecha,
                'edad': self.entrada_edad,
                'sexo': self.entrada_sexo,
                'bebidas_semana': self.entrada_bebidas_semana,
                'cervezas': self.entrada_cervezas,
                'finde': self.entrada_finde,
                'destiladas': self.entrada_destiladas,
                'vinos': self.entrada_vinos
            }
            
            # Campos booleanos/selección
            campos_seleccion = {
                'perdidas_control': self.entrada_perdidas_control,
                'diversion_alcohol': self.entrada_diversion_alcohol,
                'problemas_digestivos': self.entrada_problemas_digestivos,
                'tension_alta': self.entrada_tension_alta,
                'dolor_cabeza': self.entrada_dolor_cabeza
            }
    
            # Procesar campos de texto
            for campo, widget in campos_texto.items():
                valor = widget.get().strip()
                if not valor:
                    self._mostrar_error_campo(campo)
                    raise ValueError(f"El campo {campo} es obligatorio")
                datos[campo] = valor
    
            # Procesar campos de selección
            for campo, widget in campos_seleccion.items():
                valor = widget.get()
                if not valor:
                    self._mostrar_error_campo(campo)
                    raise ValueError(f"El campo {campo} es obligatorio")
                datos[campo] = valor
    
            # Validaciones específicas
            self._validar_fecha(datos['fecha'])
            self._validar_edad(datos['edad'])
            self._validar_campos_numericos(datos)
    
            return datos
    
        except ValueError as e:
            messagebox.showerror("Error de Validación", str(e))
            return None
        except Exception as e:
            messagebox.showerror("Error", f"Error al procesar el formulario: {str(e)}")
            return None
    
    def _validar_fecha(self, fecha):
        """Valida el formato de la fecha"""
        try:
            datetime.strptime(fecha, '%Y-%m-%d')
        except ValueError:
            self._mostrar_error_campo('fecha')
            raise ValueError("Formato de fecha inválido (YYYY-MM-DD)")
    
    def _validar_edad(self, edad):
        """Valida que la edad esté en el rango correcto"""
        try:
            edad = int(edad)
            if not (0 <= edad <= 120):
                raise ValueError
        except ValueError:
            self._mostrar_error_campo('edad')
            raise ValueError("Edad inválida (0-120 años)")
    
    def _validar_campos_numericos(self, datos):
        """Valida los campos numéricos del formulario"""
        campos_numericos = ['bebidas_semana', 'cervezas', 'finde', 'destiladas', 'vinos']
        for campo in campos_numericos:
            try:
                valor = float(datos[campo])
                if valor < 0:
                    raise ValueError
            except ValueError:
                self._mostrar_error_campo(campo)
                raise ValueError(f"Valor inválido en {campo}")
    
    def _mostrar_error_campo(self, campo):
        """Resalta visualmente el campo con error"""
        if hasattr(self, f'entrada_{campo}'):
            widget = getattr(self, f'entrada_{campo}')
            widget.configure(style='Error.TEntry')
            widget.focus()

    def validar_datos(self, datos):
        if not all(datos.values()):
            messagebox.showwarning("Error", "Todos los campos son requeridos")
            return False
        try:
            datetime.strptime(datos['fecha'], '%Y-%m-%d')
            float(datos['alcohol'])
            int(datos['edad'])
            if not '/' in datos['presion']:
                raise ValueError("Formato de presión inválido")
            return True
        except ValueError as e:
            messagebox.showerror("Error", f"Error de validación: {str(e)}")
            return False

    def limpiar_formulario(self):
        """Limpia todos los campos del formulario"""
        campos_a_limpiar = [
            'entrada_fecha', 
            'entrada_edad',
            'entrada_bebidas_semana',
            'entrada_cervezas',
            'entrada_finde',
            'entrada_destiladas',
            'entrada_vinos'
        ]
        
        # Limpiar campos de entrada de texto
        for campo in campos_a_limpiar:
            if hasattr(self, campo):
                widget = getattr(self, campo)
                if widget:
                    widget.delete(0, tk.END)
        
        # Resetear comboboxes
        campos_combo = [
            'entrada_sexo',
            'entrada_perdidas_control',
            'entrada_diversion_alcohol',
            'entrada_problemas_digestivos',
            'entrada_tension_alta',
            'entrada_dolor_cabeza'
        ]
        
        for campo in campos_combo:
            if hasattr(self, campo):
                widget = getattr(self, campo)
                if widget:
                    widget.set(widget.cget('values')[0])
            
    def actualizar_grafico(self, figura):
        """Actualiza el gráfico en la interfaz"""
        try:
            # Limpiar el frame de la figura
            for widget in self.frame_figura.winfo_children():
                widget.destroy()
            
            if figura is None:
                messagebox.showinfo("Info", "No hay datos para mostrar")
                return
                
            # Crear canvas para la figura
            canvas = FigureCanvasTkAgg(figura, self.frame_figura)
            canvas.draw()
            widget = canvas.get_tk_widget()
            widget.pack(fill='both', expand=True)
            
        except Exception as e:
            print(f"Error al actualizar gráfico: {str(e)}")
            messagebox.showerror("Error", f"Error al actualizar gráfico: {str(e)}")
            
    def actualizar_registros_recientes(self, registros):
        """
        Actualiza los registros recientes en el Treeview
        :param registros: DataFrame con los registros recientes
        """
        try:
            # Limpiar registros existentes
            for item in self.tree_registros_recientes.get_children():
                self.tree_registros_recientes.delete(item)
            
            # Insertar nuevos registros
            for _, registro in registros.iterrows():
                valores = (
                    registro['idEncuesta'],
                    registro['Sexo'],
                    registro['edad'],
                    f"{registro['BebidasSemana']:.1f}",
                    f"{registro['BebidasFinSemana']:.1f}",
                    f"{registro['BebidasDestiladasSemana']:.1f}",
                    f"{registro['VinosSemana']:.1f}",
                    f"{registro['CervezasSemana']:.1f}"
                )
                self.tree_registros_recientes.insert('', 'end', values=valores)
        except Exception as e:
            print(f"Error al actualizar registros recientes: {e}")

    def actualizar_estadisticas(self, stats, alto_consumo):
        try:
            # Limpiar widgets anteriores
            for widget in self.frame_estadisticas.winfo_children():
                widget.destroy()
            
            # Panel principal con pestañas
            notebook = ttk.Notebook(self.frame_estadisticas)
            notebook.pack(fill='both', expand=True, padx=10, pady=5)
            
            # Solo mantenemos las dos pestañas principales
            tab_resumen = ttk.Frame(notebook)
            tab_alto_riesgo = ttk.Frame(notebook)
            
            notebook.add(tab_resumen, text='Resumen General')
            notebook.add(tab_alto_riesgo, text='Alto Riesgo')
            
            # Crear contenido de las pestañas
            self._crear_resumen_general(tab_resumen, stats)
            self._crear_panel_alto_riesgo(tab_alto_riesgo, alto_consumo)
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al actualizar estadísticas: {str(e)}")
            
    def eliminar_paciente(self, id_paciente):
        """
        Elimina un paciente utilizando el callback registrado
        Args:
            id_paciente: ID del paciente a eliminar
        """
        try:
            if self._eliminar_callback:
                if self._eliminar_callback(id_paciente):
                    messagebox.showinfo("Éxito", "Paciente eliminado correctamente")
                else:
                    messagebox.showerror("Error", "No se pudo eliminar el paciente")
        except Exception as e:
            messagebox.showerror("Error", f"Error al eliminar paciente: {str(e)}")

    def actualizar_listado_pacientes(self, pacientes):
        try:
            # Limpiar listado existente
            for item in self.tree_pacientes.get_children():
                self.tree_pacientes.delete(item)
            
            # Insertar nuevos datos
            for _, paciente in pacientes.iterrows():
                self.tree_pacientes.insert('', 'end', values=(
                    paciente['idEncuesta'],
                    paciente['Fecha'].strftime('%Y-%m-%d') if 'Fecha' in paciente else '',
                    paciente['Sexo'],
                    paciente['edad'],
                    f"{paciente['BebidasSemana']:.1f}",
                    f"{paciente['BebidasFinSemana']:.1f}",
                    f"{paciente['CervezasSemana']:.1f}",
                    f"{paciente['BebidasDestiladasSemana']:.1f}",
                    f"{paciente['VinosSemana']:.1f}"
                ))
        except Exception as e:
            messagebox.showerror("Error", f"Error al actualizar listado: {str(e)}")

    def _crear_resumen_general(self, tab, stats):
        # Frame principal con grid layout
        main_frame = ttk.Frame(tab)
        main_frame.pack(fill='both', expand=True, padx=10, pady=5)
        
        # Frame izquierdo para estadísticas existentes
        frame_stats = ttk.LabelFrame(main_frame, text="Estadísticas Generales")
        frame_stats.pack(side='left', padx=5, pady=5, fill='both', expand=True)
        
        # Frame derecho para registros recientes
        frame_recientes = ttk.LabelFrame(main_frame, text="Registros Recientes")
        frame_recientes.pack(side='right', padx=5, pady=5, fill='both', expand=True)
        
        # Estadísticas por género
        for sexo in ['Hombre', 'Mujer']:
            datos_sexo = stats[stats['Sexo'] == sexo]
            frame_genero = ttk.LabelFrame(frame_stats, text=f"Estadísticas {sexo}")
            frame_genero.pack(padx=5, pady=5, fill='x')
            
            estadisticas = {
                'Promedio Bebidas/Semana': datos_sexo['BebidasSemana'].mean(),
                'Promedio Cervezas': datos_sexo['CervezasSemana'].mean(),
                'Promedio Fin de Semana': datos_sexo['BebidasFinSemana'].mean(),
                'Promedio Destiladas': datos_sexo['BebidasDestiladasSemana'].mean(),
                'Promedio Vinos': datos_sexo['VinosSemana'].mean(),
                'Total Personas': len(datos_sexo)
            }
            
            for i, (label, value) in enumerate(estadisticas.items()):
                ttk.Label(frame_genero, text=f"{label}:", style="Bold.TLabel").grid(
                    row=i, column=0, padx=5, pady=2, sticky='e')
                ttk.Label(frame_genero, text=f"{value:.2f}").grid(
                    row=i, column=1, padx=5, pady=2, sticky='w')
        
        # Crear Treeview para registros recientes
        columns = ('ID', 'Sexo', 'Edad', 'Bebidas', 'Fin Sem', 'Dest', 'Vinos', 'Cerv')
        self.tree_registros_recientes = ttk.Treeview(frame_recientes, columns=columns, show='headings', height=8)
        
        # Configurar columnas
        for col in columns:
            self.tree_registros_recientes.heading(col, text=col)
            self.tree_registros_recientes.column(col, width=60)
        
        # Añadir scrollbar
        scrollbar = ttk.Scrollbar(frame_recientes, orient='vertical', command=self.tree_registros_recientes.yview)
        self.tree_registros_recientes.configure(yscrollcommand=scrollbar.set)
        
        # Empaquetar Treeview y scrollbar
        self.tree_registros_recientes.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
    def _crear_panel_alto_riesgo(self, tab, alto_consumo):
        frame = ttk.LabelFrame(tab, text="Casos de Alto Consumo")
        frame.pack(padx=10, pady=5, fill='both', expand=True)

        # Crear Treeview con más detalles
        columns = ('ID', 'Edad', 'Sexo', 'Bebidas', 'Cerveza', 'Finde', 'Destiladas', 'Vinos')
        tree = ttk.Treeview(frame, columns=columns, show='headings', height=10)
        
        # Configurar columnas
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=80, anchor='center')

        # Insertar datos
        for _, row in alto_consumo.iterrows():
            tree.insert('', 'end', values=(
                row['idEncuesta'],
                row['edad'],
                row['Sexo'],
                f"{row['BebidasSemana']:.1f}",
                f"{row['CervezasSemana']:.1f}",
                f"{row['BebidasFinSemana']:.1f}",
                f"{row['BebidasDestiladasSemana']:.1f}",
                f"{row['VinosSemana']:.1f}"
            ))

        # Agregar scrollbars
        scrolly = ttk.Scrollbar(frame, orient='vertical', command=tree.yview)
        scrollx = ttk.Scrollbar(frame, orient='horizontal', command=tree.xview)
        tree.configure(yscrollcommand=scrolly.set, xscrollcommand=scrollx.set)

        # Eventos del árbol
        tree.bind('<<TreeviewSelect>>', lambda e: self._on_select_paciente(e, tree))

        # Empaquetar componentes
        tree.pack(side='left', fill='both', expand=True)
        scrolly.pack(side='right', fill='y')
        scrollx.pack(side='bottom', fill='x')
        
    def _on_select_paciente(self, event, tree):
        """Maneja la selección de un paciente en el TreeView"""
        try:
            if tree.selection():
                item = tree.selection()[0]
                valores = tree.item(item)['values']
                print(f"Paciente seleccionado: ID={valores[0]}")
        except Exception as e:
            print(f"Error al seleccionar paciente: {e}")
                
    
    def _on_doble_click_paciente(self, event):
        """
        Maneja el evento de doble clic para eliminar un paciente
        """
        try:
            if self.tree_pacientes.selection():
                item = self.tree_pacientes.selection()[0]
                paciente_id = self.tree_pacientes.item(item)['values'][0]
                
                if messagebox.askyesno("Confirmar eliminación", 
                                    "¿Está seguro de que desea eliminar este paciente?"):
                    if self._eliminar_callback:
                        self._eliminar_callback(paciente_id)
        except Exception as e:
            messagebox.showerror("Error", f"Error al intentar eliminar: {str(e)}")

    def mostrar_mensaje(self, titulo, mensaje):
        messagebox.showinfo(titulo, mensaje)