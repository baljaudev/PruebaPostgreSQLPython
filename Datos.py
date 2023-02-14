class Cliente:
    def __init__(self, nombre, apellidos, dni, fecha_nac, telefono):
        self.nombre = nombre
        self.apellidos = apellidos
        self.dni = dni
        self.fecha_nac = fecha_nac
        self.telefono = telefono

    def __datos__(self):
        return "Nombre: " + self.nombre + " Apellidos: " + self.apellidos + " DNI: "\
            + self.dni + " Fecha de nacimiento: " + self.fecha_nac + " Teléfono: " + self.telefono


class Matricula:
    def __init__(self, cliente, deporte, precio):
        self.cliente = cliente
        self.deporte = deporte
        self.precio = precio

    def __deportes__(self, nombre_deporte):
        return "ID Cliente: " + str(self.cliente) + " ID Deporte: " + str(self.deporte) \
            + " Precio: " + str(self.precio) + " Nombre del deporte: " + nombre_deporte
