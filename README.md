# PruebaPostgreSQLPython

## POLIDEPORTIVO
• Crea un proyecto nuevo en Python llamado Polideportivo.  
• Escribe un programa en Python para la gestión de un Polideportivo cuyos clientes pueden 
matricularse en varios deportes. La aplicación creada se conectará con una base de datos 
Postgres para guardar y consultar los datos.  
• El programa mostrará un menú con las siguientes opciones:
1. Dar de alta un cliente con sus datos personales
2. Dar de baja un cliente
3. Mostrar los datos personales de un cliente o de todos
4. Matricular a un cliente en un deporte
5. Desmatricular a un cliente en un deporte
6. Mostrar los deportes de un cliente
7. Salir  

• Crea una clase llamada Clientes con los siguientes atributos para guardar los datos personales 
de los clientes: nombre completo, dni, fecha de nacimiento y teléfono.  
• Los deportes que ofrece el polideportivo son: tenis, natación, atletismo, baloncesto y futbol.  
• Los datos que deben guardarse de los deportes son nombre del deporte y precio/hora.  
• La clase Clientes tendrá un método llamado __datos__ que permita mostrar los datos 
personales de un cliente.  
• La clase Clientes tendrá un método llamado __deportes__ que permita mostrar el nombre de 
los deportes con su precio en los que está matriculado un cliente.  
• Al matricular a un cliente en un deporte se guardará el nombre del deporte y el horario
elegido.  
• El programa realizará todas las operaciones tanto de creación de la base de datos como de la 
gestión del polideportivo.  
• Toda la información relativa a los clientes se guardará en la base de datos Postgres.  
