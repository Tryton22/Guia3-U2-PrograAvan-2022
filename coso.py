# Guia 3 Unidad 2 Programacion Avanzada 2022, Matias Fonseca, Claudio La Rosa.
import gi
import json
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
from gi.repository import Gio

def abrir_archivo():
    """Se abre el archivo JSON creado para este proyecto"""
    try:
        with open("libreria.json", 'r') as archivo:
            datos = json.load(archivo)
    except IOError:
        datos = []
    return datos

def guardar_archivo(datos):
    """Guarda los datos ingresados en el archivo JSON"""
    with open("libreria.json", 'w') as archivo:
        json.dump(datos, archivo, indent=2)

# Ventana principal del programa. 
class Ventana_principal(Gtk.Window):
    def __init__(self):
        super().__init__()

        # Se configura el espacio de los bordes.
        self.set_border_width(10)

        # Creacion de la HeaderBar
        self.barra = Gtk.HeaderBar()
        self.barra.set_title("Bibliotecas CDMR")
        self.barra.set_show_close_button(True)
        self.set_titlebar(self.barra)                                  

        # Boton para abrir el AboutDialog
        self.boton_sobre = Gtk.Button()
        icono = Gio.ThemedIcon(name = "help-about")
        imagen = Gtk.Image.new_from_gicon(icono, Gtk.IconSize.BUTTON)
        self.boton_sobre.add(imagen)
        self.boton_sobre.connect("clicked", self.click_sobre)
        self.barra.add(self.boton_sobre)

        # Box de la ventana principal.
        self.caja = Gtk.Box(spacing = 8)
        self.caja.set_orientation(Gtk.Orientation.VERTICAL)
        self.add(self.caja)

        self.texto = Gtk.Label(label= "Bienvenido a la Base de Datos de Bibliotecas CDMR.")
        self.caja.add(self.texto)

        self.texto1 = Gtk.Label(label= "Pulse el boton con la accion que desea realizar.")
        self.caja.add(self.texto1)

        # Boton que abre el dialogo principal.
        self.boton_abrir = Gtk.Button()
        self.boton_abrir.set_label("Ingresar a Base de Datos")
        self.boton_abrir.connect("clicked", self.abrir)
        self.caja.add(self.boton_abrir)

        # Boton para salir.
        self.boton_salir = Gtk.Button()
        self.boton_salir.set_label("Salir")
        self.boton_salir.connect("clicked", self.cerrar)
        self.caja.add(self.boton_salir)
    
    # Funcion que abre el dialogo About de este programa.
    def click_sobre(self, btn=None):
        dialogo_sobre = DialogoSobre()
        dialogo_sobre.run()
        dialogo_sobre.destroy()


    # Funcion que abre el dialogo donde se agregan o eliminan los libros.
    def abrir(self, btn=None):
        dialogo_ingresar = DialogoIngresar(self)
        dialogo_ingresar.run()
        dialogo_ingresar.destroy()

    
    # Funcion que cierra el programa con un MessageDialog como intermediario.
    def cerrar(self, btn=None):
        dialogo_cerrar = Gtk.MessageDialog(
            transient_for =self,
            flags = 0,
            message_type = Gtk.MessageType.QUESTION,
            buttons = Gtk.ButtonsType.YES_NO,
            text = " Esta Seguro/a de querer salir?" 
        )
        respuesta = dialogo_cerrar.run()

        if respuesta == Gtk.ResponseType.YES:
            Gtk.main_quit()
        if respuesta == Gtk.ResponseType.NO:
            dialogo_cerrar.destroy()
        
        dialogo_cerrar.destroy()

# Dialogo About de este programa.
class DialogoSobre(Gtk.AboutDialog):
    def __init__(self):
        super().__init__()
        # Se define la caracteristica del porte del dialogo About.
        self.resize(300,300)

        # Se definen los textos que va a contener el dialogo About
        self.resize(300,300)
        self.set_authors(["Claudio La Rosa", "Matias Fonseca"])
        self.set_license("Licencia publica creada por Bibliotecas CDMR v2.0")
        self.set_program_name("Base de Datos, Bibliotecas CDMR")
        self.set_version("Version 2.5")
        self.set_comments("Profesor: Fabio Duran Verdugo")
        self.set_copyright("Ingenieria Civil en Bioinformatica - Programacion avanzada - 2022")
        self.show_all()

# Dialogo donde se ingresa a la base de datos.
class DialogoIngresar(Gtk.Dialog):
    def __init__(self, parent):
        super().__init__(title="Biblioteca CDMR", transient_for=parent, flags=0)
        
        self.set_border_width(10)
        self.resize(500, 100)

        # Se configura un TreeView para contener los datos de los libros.
        self.vista = Gtk.TreeView()
        self.modelo = Gtk.ListStore(str, str)
        self.vista.set_model(model=self.modelo)

        nombre_columnas = ("Nombre", "Autor")
        celda = Gtk.CellRendererText()
        for x in range(len(nombre_columnas)):
            columnas = Gtk.TreeViewColumn(nombre_columnas[x],
                                         celda,
                                         text=x)
            self.vista.append_column(columnas)        

        # Se cargan los datos en la interfaz.
        self.cargar_datos_del_json()

        # Se agrega un ComboBoxText para elegir opciones.
        self.opciones_combo = Gtk.ComboBoxText()

        # Lista de opciones para el ComboBoxText.
        self.lista_opcion = Gtk.ListStore(str)
        self.opciones = [
            "AGREGAR LIBRO",
            "ELIMINAR LIBRO",
        ]

        # Se cargan las opciones en el ComboBoxText.
        for x in self.opciones:
            self.opciones_combo.append_text(x)
        
        # Boton que sirve para seleccionar opcion del ComboBoxText.
        self.boton_elegir = Gtk.Button()
        self.boton_elegir.set_label("Seleccionar opcion mostrada")
        self.boton_elegir.connect("clicked", self.eleccion)

        self.boton_regreso = Gtk.Button()
        self.boton_regreso.set_label("Volver a la ventana principal")
        self.boton_regreso.connect("clicked", self.regresar)


        # Box que almacena los widgets de esta ventana.
        contenedor = self.get_content_area()
        contenedor.set_orientation(Gtk.Orientation.VERTICAL)
        contenedor.add(self.vista)
        contenedor.add(self.opciones_combo)
        contenedor.add(self.boton_elegir)
        contenedor.add(self.boton_regreso)
        self.show_all()    

    # Se cargan los datos del JSON para su manipulacion.
    def cargar_datos_del_json(self):
        datos = abrir_archivo()

        for item in datos:
            lineas = [x for x in item.values()]
            #print(line)
            self.modelo.append(lineas)
    
    # Se elimina el contenido del tree para su actualizacion.
    def borrar_todo(self):
        for x in range(len(self.modelo)):
            iterador_ = self.modelo.get_iter(0)
            self.modelo.remove(iterador_)
    
    # Funcion que se encarga de que las opciones del ComboBoxText hagan algo
    def eleccion(self, btn=None):


        if self.opciones_combo.get_active_text() == "AGREGAR LIBRO":
            print("hOLA")
            agregar_libro = DialogoAgregar(self)
            respuesta_1 = agregar_libro.run()
            agregar_libro.destroy()

        # Opcion de eliminar libro.
        elif self.opciones_combo.get_active_text() == "ELIMINAR LIBRO":
            x, y = self.vista.get_selection().get_selected()
            # Por si no se seleccionada nada.
            if x is None or y is None:
                print("Seleccione un libro.")
                return
            
            datos = abrir_archivo()
            for z in datos:
                if z['nombre'] == x.get_value(y, 0):
                    datos.remove(z)
            guardar_archivo(datos)

            self.borrar_todo()
            self.cargar_datos_del_json()

        else:
            print("elige algo")

    def regresar(self, btn=None):
        self.destroy()

class DialogoAgregar(Gtk.Dialog):
    def __init__(self, parent):
        super().__init__(title="Biblioteca CDMR", transient_for=parent, flags=0)
        
        self.set_border_width(10)
        self.resize(300, 100)

        # Box de la ventana donde se agregan los datos de los libros.
        contenedor_1 = self.get_content_area(spacing = 5)
        contenedor_1.set_orientation(Gtk.Orientation.VERTICAL)

        # Se Configura distintos Label y Entry para los datos.        
        etiqueta_nombre = Gtk.Label(label="Nombre")
        contenedor_1.add(etiqueta_nombre)

        self.nombre = Gtk.Entry()
        contenedor_1.add(self.nombre)
        
        etiqueta_autor = Gtk.Label(label="Autor")
        contenedor_1.add(etiqueta_autor)

        self.autor = Gtk.Entry()
        contenedor_1.add(self.autor)

        # Configuracion del boton "OK" de esta ventana.
        boton_OK = Gtk.Button()
        boton_OK.set_label("OK")
        boton_OK.connect("clicked", self.aceptar)
        contenedor_1.add(boton_OK)

        self.show_all()

    def aceptar(self, btn=None):
        nombre = self.nombre.get_text()
        autor = self.autor.get_text()

        datos = abrir_archivo()
        nuevos_datos = {"nombre": nombre,
                    "autor": autor
                    }
        datos.append(nuevos_datos)
        guardar_archivo(datos)

        self.borrar_todo()
        self.cargar_datos_del_json()
    

if __name__ == "__main__":
    # Se llama a la Ventana principal del programa.
    progra = Ventana_principal()
    progra.resize(800,100)
    progra.connect("destroy", Gtk.main_quit)
    progra.show_all()
    Gtk.main()