#include <Arduino.h>

const int PIN_TEMPERATURA = 34;
const int PIN_LDR = 32;
const int PIN_VENTILADOR = 18;
const int PIN_LED = 19;

const int CANAL_VENTILADOR = 0;
const int CANAL_LED = 1;

const int FRECUENCIA_PWM = 5000;
const int RESOLUCION_PWM = 8;



int velocidadVentilador = 0;
int intensidadLed = 0;

bool ventiladorManual = false;
bool ledManual = false;



void setup() {
    Serial.begin(115200);

    analogReadResolution(12);

    // Configuración PWM del ventilador
    ledcSetup(
        CANAL_VENTILADOR,
        FRECUENCIA_PWM,
        RESOLUCION_PWM
    );

    ledcAttachPin(
        PIN_VENTILADOR,
        CANAL_VENTILADOR
    );

    // Configuración PWM del LED
    ledcSetup(
        CANAL_LED,
        FRECUENCIA_PWM,
        RESOLUCION_PWM
    );

    ledcAttachPin(
        PIN_LED,
        CANAL_LED
    );

    // Iniciar apagados
    ledcWrite(CANAL_VENTILADOR, 0);
    ledcWrite(CANAL_LED, 0);

    Serial.println();
    Serial.println("=================================");
    Serial.println(" PRACTICA_01");
    Serial.println("=================================");
    Serial.println("Sistema iniciado.");
    Serial.println();
    Serial.println("Comandos disponibles:");
    Serial.println("  encender");
    Serial.println("  apagar");
    Serial.println("  ajustar <0-100>");
    Serial.println("  leer");
    Serial.println();
}



float leerTemperatura() {
    int lectura = analogRead(PIN_TEMPERATURA);

    // Conversión inicial para LM35.
    // ADC de 12 bits: 0 - 4095
    float voltaje = (lectura / 4095.0) * 3.3;

    // LM35 = 10 mV por grado Celsius
    float temperatura = voltaje * 100.0;

    return temperatura;
}



int leerLDR() {
    return analogRead(PIN_LDR);
}



void controlarTemperatura(float temperatura) {

    if (ventiladorManual) {
        return;
    }

    if (temperatura > 30.0) {
        velocidadVentilador = 100;

        int pwm = map(
            velocidadVentilador,
            0,
            100,
            0,
            255
        );

        ledcWrite(
            CANAL_VENTILADOR,
            pwm
        );
    } else {
        velocidadVentilador = 0;

        ledcWrite(
            CANAL_VENTILADOR,
            0
        );
    }
}



void controlarIluminacion(int ldr) {

    if (ledManual) {
        return;
    }

    // Menos luz detectada por el LDR
    // = mayor intensidad del LED.

    intensidadLed = map(
        ldr,
        0,
        4095,
        255,
        0
    );

    intensidadLed = constrain(
        intensidadLed,
        0,
        255
    );

    ledcWrite(
        CANAL_LED,
        intensidadLed
    );
}



void mostrarLecturas() {

    float temperatura = leerTemperatura();
    int ldr = leerLDR();

    Serial.println();
    Serial.println("--------- TELEMETRIA ---------");

    Serial.print("Temperatura: ");
    Serial.print(temperatura);
    Serial.println(" °C");

    Serial.print("LDR: ");
    Serial.println(ldr);

    Serial.print("Ventilador: ");
    Serial.print(velocidadVentilador);
    Serial.println(" %");

    Serial.print("LED PWM: ");
    Serial.println(intensidadLed);

    Serial.println("------------------------------");
    Serial.println();
}



void procesarComando(String comando) {

    comando.trim();
    comando.toLowerCase();

    if (comando == "encender") {

        ventiladorManual = true;
        velocidadVentilador = 100;

        ledcWrite(
            CANAL_VENTILADOR,
            255
        );

        Serial.println("Ventilador encendido al 100%.");
    }

    else if (comando == "apagar") {

        ventiladorManual = true;
        velocidadVentilador = 0;

        ledcWrite(
            CANAL_VENTILADOR,
            0
        );

        Serial.println("Ventilador apagado.");
    }

    else if (comando.startsWith("ajustar")) {

        int espacio = comando.indexOf(' ');

        if (espacio > 0) {

            int valor = comando.substring(
                espacio + 1
            ).toInt();

            valor = constrain(
                valor,
                0,
                100
            );

            ventiladorManual = true;
            velocidadVentilador = valor;

            int pwm = map(
                valor,
                0,
                100,
                0,
                255
            );

            ledcWrite(
                CANAL_VENTILADOR,
                pwm
            );

            Serial.print(
                "Ventilador ajustado a "
            );

            Serial.print(valor);
            Serial.println("%.");
        }
    }

    else if (comando == "leer") {

        mostrarLecturas();
    }

    else if (comando == "automatico") {

        ventiladorManual = false;
        ledManual = false;

        Serial.println(
            "Control automatico activado."
        );
    }

    else {

        Serial.println(
            "Comando no reconocido."
        );
    }
}



void loop() {

    float temperatura = leerTemperatura();
    int ldr = leerLDR();

    controlarTemperatura(
        temperatura
    );

    controlarIluminacion(
        ldr
    );

    if (Serial.available() > 0) {

        String comando =
            Serial.readStringUntil('\n');

        procesarComando(comando);
    }

    delay(500);
}