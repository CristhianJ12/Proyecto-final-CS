Integrantes:
- Reymundo Rodriguez Cristhian Jhon
- Chuquirachi Martinez Dante
- Fernandez Durán Rafael
- Iturrizaga Campean Geraldine
- Acevedo Ura Jordan Smith
- Mejia Poma Liand Anthuane

Proyecto Final Construccion de Software 

# "Gestor de tiempo"

Introducción
Este documento describe el diseño y la implementación de una aplicación de gestión de tiempo multipropósito que combina un temporizador, una alarma y un temporizador Pomodoro. La aplicación está desarrollada utilizando el lenguaje de programación Python y una base de datos SQLite para almacenar la configuración de los temporizadores y los registros de uso.

Motivación
La gestión eficaz del tiempo es un aspecto crucial para la productividad y el éxito en diversas áreas de la vida. Esta aplicación pretende abordar la necesidad de una herramienta versátil que permita a los usuarios administrar su tiempo de manera eficiente y organizada.

- Temporizador: Permite configurar y utilizar un temporizador estándar para contar hacia atrás desde un tiempo especificado.
- Alarma: Permite configurar y utilizar una alarma para recibir notificaciones auditivas en momentos específicos del día.
- Temporizador Pomodoro: Permite configurar y utilizar un temporizador Pomodoro, que alterna entre períodos de trabajo y descanso de acuerdo a la técnica Pomodoro.
    * Botones de Control: Proporciona botones para iniciar, pausar, reiniciar y salir de cada temporizador.
    * Ring de 3 Segundos: Al finalizar cada temporizador, se activa un ring de 3 segundos para notificar al usuario.
    * Configuración del Tiempo: Permite a los usuarios configurar la duración de cada temporizador (temporizador estándar, alarma y temporizador Pomodoro).

Tecnologías Empleadas:

- Lenguaje de Programación: Python
- Base de Datos: SQLite
- Control de Versiones: Git y GitHub

# [![Sin-t-tulo.png](https://i.postimg.cc/ryf5jtSZ/Sin-t-tulo.png)](https://postimg.cc/9zq4F0gy)

Primer Test: 
El test de validación de datos de la alarma implementa varias pruebas unitarias para la función set_alarm. Verifica que la función maneje correctamente diferentes escenarios de entrada: datos válidos, datos faltantes, tipos de datos incorrectos y formatos de tiempo inválidos. Cada prueba específica revisa que la función set_alarm valide los datos de entrada según los requisitos establecidos (como la presencia de todas las claves necesarias y la correcta validación de tipos y formatos de datos). Si los datos son válidos, la función debería ejecutar sin problemas, y si no lo son, debería lanzar las excepciones adecuadas (ValueError o TypeError), asegurando así la robustez y fiabilidad de la función.

Segundo Test:
Este test de unidad utiliza el módulo unittest junto con unittest.mock.patch para verificar que la clase MainWindow del archivo Principal.PrincCode llama correctamente a QProcess.startDetached cuando se abren diferentes funcionalidades (temporizador, alarma y pomodoro) a través de sus respectivos botones. Cada prueba crea una instancia de MainWindow, simula un clic en el botón correspondiente (temporizador, alarma o pomodoro) y luego comprueba que QProcess.startDetached fue llamado con los argumentos esperados, que son la ruta del ejecutable de Python y la ruta del script correspondiente (TempoCode.py, AlarmCode.py o PomodoroCode.py). Esto asegura que al presionar cada botón, la aplicación lanza el script adecuado correctamente.
