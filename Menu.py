import psycopg2.extras
import sys
import Datos

conex = None

try:
    conex = psycopg2.connect(
        dbname="postgres",
        user="postgres",
        password="pruebaspy",
        port="5432"
    )
    # Se crea el cursor:
    cursor = conex.cursor()
    print("Conexión establecida.")

    cursor.execute("DROP TABLE IF EXISTS MATRICULAS")
    print("Tabla matriculas eliminada.")
    cursor.execute("DROP TABLE IF EXISTS CLIENTES")
    print("Tabla clientes eliminada.")
    cursor.execute("DROP TABLE IF EXISTS DEPORTES")
    print("Tabla deportes eliminada.")

    cursor.execute("CREATE TABLE CLIENTES (id serial PRIMARY KEY, "
                   "NOMBRE VARCHAR, APELLIDOS VARCHAR, DNI VARCHAR, "
                   "FECHA_NAC VARCHAR, TELEFONO VARCHAR)")
    print("Tabla clientes creada.")

    cursor.execute("CREATE TABLE DEPORTES (id serial PRIMARY KEY, "
                   "NOMBRE VARCHAR, PRECIO INTEGER)")
    print("Tabla deportes creada.")

    cursor.execute("CREATE TABLE MATRICULAS (ID_CLIENTE INTEGER, ID_DEPORTE INTEGER, HORARIO VARCHAR,"
                   "CONSTRAINT FK_CLI FOREIGN KEY(ID_CLIENTE) REFERENCES CLIENTES(id) ON DELETE CASCADE,"
                   "CONSTRAINT FK_DEPO FOREIGN KEY(ID_DEPORTE) REFERENCES DEPORTES(id),"
                   "CONSTRAINT PK_MAT PRIMARY KEY(ID_CLIENTE, ID_DEPORTE))")
    print("Tabla matriculas creada.")

    # Se insertan los datos:
    cursor.execute("INSERT INTO DEPORTES (NOMBRE, PRECIO) VALUES (%s, %s)",
                   ("futbol", 60))
    cursor.execute("INSERT INTO DEPORTES (NOMBRE, PRECIO) VALUES (%s, %s)",
                   ("baloncesto", 55))
    cursor.execute("INSERT INTO DEPORTES (NOMBRE, PRECIO) VALUES (%s, %s)",
                   ("tenis", 80))
    cursor.execute("INSERT INTO DEPORTES (NOMBRE, PRECIO) VALUES (%s, %s)",
                   ("atletismo", 25))
    cursor.execute("INSERT INTO DEPORTES (NOMBRE, PRECIO) VALUES (%s, %s)",
                   ("natacion", 35))

    conex.commit()
    cursor.close()

except (Exception, psycopg2.DatabaseError) as error:
    print('Error de excepción: ', error)
    sys.exit(1)


def dar_alta():
    try:
        nombre = input("Introduce el nombre del cliente: ")
        apellidos = input("Introduce los apellidos del cliente: ")
        dni = input("Introduce el DNI del cliente: ")
        cursor = conex.cursor()
        print("Conexión establecida.")
        cursor.execute("SELECT * FROM CLIENTES WHERE DNI = %s", (dni,))
        conex.commit()
        cliente = cursor.fetchone()
        if cliente is not None:
            print("Ya existe un cliente con ese DNI.")
        else:
            fecha_nac = input("Introduce la fecha de nacimiento del cliente: ")
            telefono = input("Introduce el teléfono del cliente: ")
            cursor.execute("INSERT INTO CLIENTES (NOMBRE, APELLIDOS, DNI, FECHA_NAC, TELEFONO) "
                           "VALUES (%s, %s, %s, %s, %s)", (nombre, apellidos, dni, fecha_nac, telefono))
            # Se confirma la consulta:
            conex.commit()
            print("Cliente dado de alta.")
        cursor.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print('Error de excepción: ', error)


def dar_baja_cliente():
    dni = input("Introduce el DNI del cliente del que dar la baja: ")
    cursor = conex.cursor()
    print("Conexión establecida.")
    cursor.execute("DELETE FROM CLIENTES WHERE DNI = %s", (dni,))
    conex.commit()
    cursor.close()
    print("Cliente dado de baja.")


def mostrar_clientes(op):
    if op == "uno":
        try:
            dni = input("Introduce el DNI del cliente del que mostrar los datos: ")
            cursor = conex.cursor()
            print("Conexión establecida.")
            cursor.execute("SELECT * FROM CLIENTES WHERE DNI = %s", (dni,))
            conex.commit()
            cliente = cursor.fetchone()
            if cliente is None:
                print("No existe ningún cliente con ese DNI.")
            else:
                cliente = Datos.Cliente(cliente[1], cliente[2], cliente[3], cliente[4], cliente[5])
                print(cliente.__datos__())
            cursor.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print('Error de excepción: ', error)
    elif op == "todos":
        try:
            cursor = conex.cursor()
            print("Conexión establecida.")
            cursor.execute("SELECT * FROM CLIENTES")
            conex.commit()
            clientes = cursor.fetchall()
            if not clientes:
                print("No existen clientes.")
            else:
                for cliente in clientes:
                    cliente = Datos.Cliente(cliente[1], cliente[2], cliente[3], cliente[4], cliente[5])
                    print(cliente.__datos__())
                cursor.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print('Error de excepción: ', error)


def matricular():
    dicc_deportes_horarios = {
        'futbol': ['10:00', '11:00', '12:00', '13:00', '16:00', '17:00', '18:00', '19:00'],
        'baloncesto': ['10:00', '11:00', '12:00', '13:00', '16:00', '17:00', '18:00', '19:00'],
        'tenis': ['10:00', '11:00', '12:00', '13:00', '16:00', '17:00', '18:00', '19:00'],
        'atletismo': ['10:00', '11:00', '12:00', '13:00', '16:00', '17:00', '18:00', '19:00'],
        'natacion': ['10:00', '11:00', '12:00', '13:00', '16:00', '17:00', '18:00', '19:00']
    }
    try:
        dni = input("Introduce el DNI del cliente: ")
        cursor = conex.cursor()
        print("Conexión establecida.")
        cursor.execute("SELECT * FROM CLIENTES WHERE DNI = %s", (dni,))
        conex.commit()
        cliente = cursor.fetchone()
        if cliente is None:
            print("No existe ningún cliente con ese DNI.")
        else:
            deporte = input(str("Introduce el deporte en el que matricular al cliente: "))
            deporte = deporte.lower()
            if deporte not in dicc_deportes_horarios:
                print("No existe ese deporte.")
            else:
                hora = input("Introduce la hora en la que matricular al cliente: ")
                if hora not in dicc_deportes_horarios[deporte]:
                    print("No existe ese horario.")
                else:
                    cursor.execute("SELECT * FROM DEPORTES WHERE NOMBRE = %s", (deporte,))
                    conex.commit()
                    deporte = cursor.fetchone()
                    cursor.execute("INSERT INTO MATRICULAS (ID_CLIENTE, ID_DEPORTE, HORARIO) VALUES (%s, %s, %s)",
                                   (cliente[0], deporte[0], hora))
                    conex.commit()
                    print("Cliente matriculado.")
        cursor.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print('Error de excepción: ', error)


def dar_baja_deporte():
    try:
        dni = input("Introduce el DNI del cliente para desmatricular de un deporte: ")
        cursor = conex.cursor()
        print("Conexión establecida.")
        cursor.execute("SELECT * FROM CLIENTES WHERE DNI = %s", (dni,))
        conex.commit()
        cliente = cursor.fetchone()
        if cliente is None:
            print("No existe ningún cliente con ese DNI.")
        else:
            cursor.execute("SELECT * FROM MATRICULAS WHERE ID_CLIENTE = %s", (cliente[0],))
            conex.commit()
            matriculas = cursor.fetchall()
            if matriculas is None:
                print("No existen matrículas.")
            else:
                print("Deportes en los que estás matriculado:")
                deportes_matriculado = []
                for matricula in matriculas:
                    cursor.execute("SELECT * FROM DEPORTES WHERE ID = %s", (matricula[1],))
                    conex.commit()
                    deporte = cursor.fetchone()
                    print("Deporte: " + deporte[1] + " - Hora: " + matricula[2])
                    deportes_matriculado.append(deporte[1].lower())
                deporte = input(
                    str("Introduce uno de los deportes en los que estás matriculado y deseas desmatricularte:"))
                if deporte.lower() not in deportes_matriculado:
                    print("No estás matriculado en ese deporte.")
                else:
                    cursor.execute("SELECT * FROM DEPORTES WHERE NOMBRE = %s", (deporte,))
                    conex.commit()
                    deporte = cursor.fetchone()
                    cursor.execute("DELETE FROM MATRICULAS WHERE ID_CLIENTE = %s AND ID_DEPORTE = %s",
                                   (cliente[0], deporte[0]))
                    conex.commit()
                    print("Cliente desmatriculado.")
        cursor.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print('Error de excepción: ', error)


def mostrar_deportes():
    try:
        dni = input("Introduce el DNI del cliente para mostrar todos sus deportes: ")
        cursor = conex.cursor()
        print("Conexión establecida.")
        cursor.execute("SELECT * FROM CLIENTES WHERE DNI = %s", (dni,))
        conex.commit()
        cliente = cursor.fetchone()
        if cliente is None:
            print("No existe ningún cliente con ese DNI.")
        else:
            cursor.execute("SELECT * FROM MATRICULAS WHERE ID_CLIENTE = %s", (cliente[0],))
            conex.commit()
            matriculas = cursor.fetchall()
            if not matriculas:
                print("No existen matrículas.")
            else:
                for matricula in matriculas:
                    cursor.execute("SELECT * FROM DEPORTES WHERE ID = %s", (matricula[1],))
                    conex.commit()
                    deporte = cursor.fetchone()
                    print("Deporte: " + deporte[1] + " - Hora: " + matricula[2])
                    matricula = Datos.Matricula(matricula[0], matricula[1], matricula[2])
                    print(matricula.__deportes__(deporte[1]))
        cursor.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print('Error de excepción: ', error)


while True:
    print('''
    1. Dar de alta a un cliente.
    2. Dar de baja a un cliente.
    3. Mostrar todos los clientes o uno en concreto (inserta 'uno', o 'todos').
    4. Matricular a un cliente en un deporte.
    5. Dar de baja a un cliente de un deporte.
    6. Mostrar todos los deportes.
    7. Salir.
    ''')
    opcion_menu = input("Introduce una opción: ")
    if opcion_menu == "1":
        dar_alta()
    elif opcion_menu == "2":
        dar_baja_cliente()
    elif opcion_menu == "uno" or opcion_menu == "todos":
        mostrar_clientes(opcion_menu)
    elif opcion_menu == "4":
        matricular()
    elif opcion_menu == "5":
        dar_baja_deporte()
    elif opcion_menu == "6":
        mostrar_deportes()
    elif opcion_menu == "7":
        if conex is not None:
            conex.close()
            print("Conexión cerrada.")
        print("Saliendo del programa...")
        break
    else:
        print("Opción incorrecta.")
