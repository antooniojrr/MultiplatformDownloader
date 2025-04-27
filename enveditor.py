import tkinter as tk
from tkinter import ttk, messagebox
import os
from dotenv import load_dotenv

class EnvEditor:
    def __init__(self, root):
        self.root = root
        self.root.title("Editor de Variables de Entorno")
        
        # Cargar variables existentes
        self.env_file = ".env"
        self.variables = {}
        self.cargar_variables()
        
        # Crear interfaz
        self.crear_interfaz()
    
    def cargar_variables(self):
        """Carga las variables existentes del archivo .env"""
        if os.path.exists(self.env_file):
            load_dotenv(self.env_file)
            with open(self.env_file, 'r') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#'):
                        if '=' in line:
                            key, value = line.split('=', 1)
                            self.variables[key.strip()] = value.strip()
    
    def crear_interfaz(self):
        """Crea los elementos de la interfaz gráfica"""
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Lista de variables
        self.tree = ttk.Treeview(main_frame, columns=('value'), show='headings')
        self.tree.heading('#0', text='Variable')
        self.tree.heading('value', text='Valor')
        self.tree.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # Actualizar Treeview
        self.actualizar_lista()
        
        # Controles
        control_frame = ttk.Frame(main_frame)
        control_frame.pack(fill=tk.X, pady=5)
        
        ttk.Button(control_frame, text="Agregar", command=self.agregar_variable).pack(side=tk.LEFT, padx=5)
        ttk.Button(control_frame, text="Editar", command=self.editar_variable).pack(side=tk.LEFT, padx=5)
        ttk.Button(control_frame, text="Eliminar", command=self.eliminar_variable).pack(side=tk.LEFT, padx=5)
        ttk.Button(control_frame, text="Guardar", command=self.guardar_variables).pack(side=tk.RIGHT, padx=5)
    
    def actualizar_lista(self):
        """Actualiza la lista de variables en el Treeview"""
        self.tree.delete(*self.tree.get_children())
        for key, value in self.variables.items():
            self.tree.insert('', tk.END, text=key, values=(value,))
    
    def agregar_variable(self):
        """Abre diálogo para agregar nueva variable"""
        self.dialogo_variable("Agregar Variable", self.guardar_nueva_variable)
    
    def editar_variable(self):
        """Abre diálogo para editar variable seleccionada"""
        seleccion = self.tree.selection()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Selecciona una variable para editar")
            return
        
        item = self.tree.item(seleccion[0])
        key = item['text']
        value = item['values'][0]
        
        self.dialogo_variable("Editar Variable", self.guardar_edicion_variable, key, value)
    
    def dialogo_variable(self, title, callback, key=None, value=None):
        """Crea diálogo para agregar/editar variables"""
        dialog = tk.Toplevel(self.root)
        dialog.title(title)
        dialog.transient(self.root)
        dialog.grab_set()
        
        ttk.Label(dialog, text="Nombre de la variable:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        nombre_var = tk.StringVar(value=key if key else "")
        ttk.Entry(dialog, textvariable=nombre_var).grid(row=0, column=1, padx=5, pady=5, sticky=tk.EW)
        
        ttk.Label(dialog, text="Valor:").grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        valor_var = tk.StringVar(value=value if value else "")
        ttk.Entry(dialog, textvariable=valor_var).grid(row=1, column=1, padx=5, pady=5, sticky=tk.EW)
        
        def guardar():
            callback(nombre_var.get(), valor_var.get())
            dialog.destroy()
        
        ttk.Button(dialog, text="Guardar", command=guardar).grid(row=2, column=1, sticky=tk.E, padx=5, pady=5)
        
        # Hacer que la ventana sea modal
        dialog.wait_window(dialog)
    
    def guardar_nueva_variable(self, key, value):
        """Guarda una nueva variable"""
        if not key:
            messagebox.showerror("Error", "El nombre de la variable no puede estar vacío")
            return
        
        self.variables[key] = value
        self.actualizar_lista()
    
    def guardar_edicion_variable(self, key, value):
        """Guarda los cambios de una variable existente"""
        seleccion = self.tree.selection()[0]
        old_key = self.tree.item(seleccion)['text']
        
        if key != old_key:
            del self.variables[old_key]
        
        self.variables[key] = value
        self.actualizar_lista()
    
    def eliminar_variable(self):
        """Elimina la variable seleccionada"""
        seleccion = self.tree.selection()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Selecciona una variable para eliminar")
            return
        
        key = self.tree.item(seleccion[0])['text']
        del self.variables[key]
        self.actualizar_lista()
    
    def guardar_variables(self):
        """Guarda todas las variables en el archivo .env"""
        try:
            with open(self.env_file, 'w') as f:
                for key, value in self.variables.items():
                    f.write(f"{key}={value}\n")
            messagebox.showinfo("Éxito", "Variables guardadas correctamente")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo guardar el archivo:\n{str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = EnvEditor(root)
    root.mainloop()