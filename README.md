# Práctica 1 — Sistemas de Control con Python y ESP32

## Descripción

En esta práctica desarrollo un sistema de control utilizando Python y posteriormente un ESP32.

Primero realizo una simulación en Python para representar el comportamiento de un proceso donde puedo medir temperatura y presión, controlar una bomba de enfriamiento y abrir o cerrar una válvula de alivio.

Después llevo una idea similar a un sistema físico utilizando un ESP32. En esta segunda parte desarrollo un pequeño **micro-invernadero inteligente**, donde controlo un ventilador y una iluminación dependiendo de las condiciones que detectan los sensores.

Mi objetivo es entender de una manera práctica cómo funciona un sistema de control, desde la lectura de sensores hasta la toma de decisiones y el accionamiento de diferentes elementos.


# 1. Estructura del proyecto

Mi proyecto está organizado de la siguiente manera:

```text
practica-01/
├── .gitignore
├── AUTHORS.md
├── README.md
│
├── docs/
│   ├── diagramas/
│   └── evidencias/
│
├── src/
│   ├── python/
│   │   ├── actuators.py
│   │   ├── controller.py
│   │   ├── main.py
│   │   ├── reactor.py
│   │   └── sensors.py
│   │
│   └── esp32/
│
└── tests/
    ├── python/
    │   └── test_reactor.py
    │
    └── esp32/
```

Separé el proyecto de esta manera para tener por un lado el programa que estoy desarrollando y por otro las pruebas y evidencias.



# 2. Primera parte — Simulación en Python

## ¿Qué estoy simulando?

En la primera parte hice un programa que representa un proceso parecido al funcionamiento de un reactor.

Dentro de la simulación tengo dos valores principales:

* Temperatura.
* Presión.

También tengo dos elementos que puedo controlar:

* Una bomba de enfriamiento.
* Una válvula de alivio.

El programa me permite observar cómo cambian los valores del proceso dependiendo de lo que haga con estos elementos.



# 3. Sensores

Para la simulación utilicé dos sensores.

### Sensor de temperatura

La temperatura puede tener valores entre:

```text
0 °C y 150 °C
```

### Sensor de presión

La presión puede tener valores entre:

```text
0 bar y 15 bar
```

Estos sensores son simulados mediante Python, por lo que no estoy utilizando sensores físicos en esta primera etapa.



# 4. Actuadores

Para modificar el comportamiento del proceso utilicé dos elementos.

### Bomba de enfriamiento

La bomba puede trabajar entre:

```text
0 % y 100 %
```

Mientras más porcentaje de trabajo tenga la bomba, mayor será el enfriamiento.

### Válvula de alivio

La válvula solamente puede tener dos estados:

```text
0 = Cerrada
1 = Abierta
```

La utilizo principalmente para ayudar a disminuir la presión cuando esta aumenta demasiado.



# 5. Comportamiento de la temperatura

Para representar el comportamiento del proceso utilicé la siguiente fórmula:

```text
ΔT = +1.5 °C − (0.05 °C × bomba[%])
```

Esto significa que, si la bomba está apagada, la temperatura aumenta:

```text
+1.5 °C
```

por cada ciclo.

Si la bomba trabaja al 100 %, el cambio de temperatura es:

```text
1.5 − (0.05 × 100) = -3.5 °C
```

Por lo tanto, la temperatura disminuye.

También encontré que con la bomba al 30 %:

```text
1.5 − (0.05 × 30) = 0 °C
```

la temperatura permanece estable.



# 6. Formas de trabajar

Mi programa tiene tres formas principales de operación.

## Manual

En este modo yo puedo controlar directamente la bomba y la válvula.

Por ejemplo:

```text
bomba 50
```

coloca la bomba al 50 %.

También puedo utilizar:

```text
valvula abrir
valvula cerrar
```

para controlar la válvula.



## Automático

En este modo el programa toma las decisiones por mí.

El sistema revisa constantemente la temperatura y modifica la bomba para intentar mantener una temperatura cercana a:

```text
60 °C
```

También revisa la presión y puede abrir la válvula cuando es necesario.

De esta manera estoy simulando un sistema donde los sensores proporcionan información, el programa toma una decisión y los actuadores realizan la acción.



## Pruebas

También agregué un modo de pruebas para poder provocar situaciones fuera de lo normal y comprobar que el sistema responda correctamente.

Puedo provocar una temperatura de:

```text
90 °C
```

con:

```text
fallo temperatura
```

También puedo provocar una presión de:

```text
13 bar
```

con:

```text
fallo presion
```

Esto me permite comprobar el sistema de seguridad sin tener que esperar a que una condición peligrosa ocurra por sí sola.


# 7. Sistema de seguridad

Una de las partes más importantes que agregué fue un sistema que revisa constantemente si la temperatura o la presión llegan a valores peligrosos.

El sistema se activa cuando:

```text
Temperatura > 85 °C
```

o:

```text
Presión > 12 bar
```

Cuando ocurre alguna de estas situaciones, el programa toma el control y realiza automáticamente dos acciones:

```text
Bomba = 100 %
Válvula = ABIERTA
```

Esto tiene prioridad sobre las instrucciones normales.

Por ejemplo, aunque el operador haya dejado la bomba en 20 %, si la temperatura supera los 85 °C, el programa cambia la bomba automáticamente al 100 %.



# 8. Pantalla del programa

También hice una pequeña pantalla en la consola para poder observar lo que está pasando.

En ella puedo ver:

```text
==========================================================
           SISTEMA DE CONTROL - REACTOR
==========================================================
 Modo:                 MANUAL

 Temperatura:            25.00 °C
 Presion:                 1.00 bar

 Bomba:                   0.00 %
 Valvula de alivio:    CERRADA

 Estado:               OPERACION NORMAL
==========================================================
```

La pantalla se limpia y se vuelve a mostrar para que la información sea más fácil de observar.



# 9. Comandos

Para conocer los comandos disponibles puedo escribir:

```text
ayuda
```

Los principales comandos son:

### Cambiar de modo

```text
modo manual
modo automatico
modo pruebas
```

### Controlar la bomba

```text
bomba <0-100>
```

### Controlar la válvula

```text
valvula abrir
valvula cerrar
```

### Consultar información

```text
leer caudal
leer manometro
```

### Realizar pruebas

```text
fallo temperatura
fallo presion
```

### Reiniciar

```text
reset
```

Para cerrar el programa:

```text
salir
```



# 10. Cómo ejecutar el programa

Para iniciar el programa desde la carpeta principal del proyecto utilizo:

```powershell
python -m src.python.main
```

Después aparece la pantalla principal y puedo comenzar a utilizar los comandos.



# 11. Pruebas

Para comprobar que las diferentes partes del programa funcionen correctamente, realicé varias pruebas automáticas.

Las pruebas se encuentran en:

```text
tests/python/test_reactor.py
```

Para ejecutarlas utilizo:

```powershell
python -m pytest -v
```

Entre las cosas que compruebo están:

* El estado inicial del sistema.
* El comportamiento de la temperatura.
* El funcionamiento de la bomba.
* La estabilidad de la temperatura.
* Los límites de la bomba.
* El funcionamiento de la válvula.
* La protección por temperatura.
* La protección por presión.
* El funcionamiento del modo automático.

Actualmente las pruebas realizadas son:

```text
9 passed
```



# 12. Organización del programa

Para que el programa no quedara todo dentro de un solo archivo, lo separé en varias partes.

### `sensors.py`

Aquí tengo todo lo relacionado con los sensores de temperatura y presión.

### `actuators.py`

Aquí manejo la bomba y la válvula.

### `reactor.py`

Aquí tengo la parte que representa el comportamiento del proceso.

### `controller.py`

Aquí se encuentran las decisiones que toma el sistema, como el modo automático y las condiciones de seguridad.

### `main.py`

Aquí se encuentra la pantalla que utilizo para interactuar con el programa.

---

# 13. Segunda parte — ESP32

Después de terminar la simulación en Python, voy a llevar el concepto a un circuito físico utilizando un ESP32.

Para esta parte desarrollaré un:

## Micro-Invernadero Inteligente

La idea es controlar algunas condiciones de un pequeño espacio para plantas.

Voy a utilizar sensores para conocer las condiciones del ambiente y elementos de salida para responder a ellas.



# 14. Elementos del ESP32

Los elementos que utilizaré son:

| Elemento                       |   GPIO |
| ------------------------------ | -----: |
| Sensor de temperatura LM35/DHT | GPIO34 |
| LDR                            | GPIO32 |
| Ventilador                     | GPIO18 |
| LED                            | GPIO19 |

El ventilador y el LED serán controlados mediante PWM.

Para el ventilador utilizaré una frecuencia de:

```text
5 kHz
```



# 15. Control de temperatura

El ESP32 revisará constantemente la temperatura.

Cuando la temperatura sea mayor a:

```text
30 °C
```

el ventilador se encenderá al:

```text
100 %
```

De esta manera puedo comprobar físicamente cómo una lectura del sensor provoca una respuesta automática.



# 16. Control de iluminación

También utilizaré una LDR para detectar la cantidad de luz.

La idea es sencilla:

```text
Menos luz
    ↓
Mayor intensidad del LED
```

y:

```text
Más luz
    ↓
Menor intensidad del LED
```

Así puedo simular un sistema que intenta mantener una iluminación adecuada de manera automática.



# 17. Comunicación con el ESP32

También agregaré comunicación mediante el monitor serial.

Los comandos principales serán:

```text
encender
ajustar
leer
```

Esto me permitirá comprobar desde la computadora qué está haciendo el ESP32 y consultar los valores de los sensores.



# 18. Diagramas y evidencias

Guardaré los diagramas del proyecto dentro de:

```text
docs/diagramas/
```

Aquí incluiré los diagramas necesarios para explicar cómo está conectado el sistema.

Las fotografías y demás evidencias estarán en:

```text
docs/evidencias/
```

Entre las evidencias que voy a incluir están:

* Capturas del programa en Python.
* Funcionamiento manual.
* Funcionamiento automático.
* Pruebas de seguridad.
* Pruebas de fallas.
* Fotografía del circuito con ESP32.
* Sensor de temperatura.
* LDR.
* LED.
* Ventilador.
* Diagrama de conexiones.



# 19. Reporte final

Al terminar la práctica prepararé un reporte en formato PDF:

```text
docs/Reporte_Evidencias_P1.pdf
```

En este reporte incluiré el desarrollo de la práctica, las pruebas realizadas, fotografías, diagramas y los resultados obtenidos.

También agregaré los enlaces a los videos donde mostraré el funcionamiento del programa de Python y del circuito con ESP32.



# 20. Control de versiones

Estoy utilizando Git y GitHub para guardar los cambios que voy realizando durante el desarrollo.

Esto me permite llevar un registro de cómo ha ido creciendo el proyecto y regresar a versiones anteriores si fuera necesario.

Algunos de los cambios realizados hasta ahora son:

```text
chore: inicializar estructura del proyecto
feat: implementar simulador de control en Python
```


# 21. Estado actual

| Parte                         | Estado     |
| ----------------------------- | ---------- |
| Estructura del proyecto       | Completada |
| Configuración de Git y GitHub | Completada |
| Simulación en Python          | Completada |
| Sensores simulados            | Completada |
| Actuadores simulados          | Completada |
| Modo manual                   | Completada |
| Modo automático               | Completada |
| Sistema de seguridad          | Completada |
| Modo de pruebas               | Completada |
| Pantalla HMI                  | Completada |
| Pruebas automáticas           | Completada |
| Programa para ESP32           | Pendiente  |
| Circuito físico               | Pendiente  |
| Diagramas                     | Pendiente  |
| Evidencias                    | Pendiente  |
| Reporte PDF                   | Pendiente  |
| Videos                        | Pendiente  |



# 22. Autor

La información del autor se encuentra en el archivo:

```text
AUTHORS.md
```
