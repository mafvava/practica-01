# Práctica 01 — Sistemas de Control con Python y ESP32

## Descripción

Implementación de sistemas de control de lazo cerrado mediante simulación en Python y hardware físico con ESP32.

## Versiones

### Versión 1.0.0 — Simulador en Python
Sistema dinámico de control de un reactor químico con sensores de temperatura y presión, actuadores de enfriamiento y alivio, modos manual, automático y pruebas, además de interlocks de seguridad.

### Versión 2.0.0 — Micro-Invernadero con ESP32
Sistema de control térmico y lumínico utilizando sensores, ventilador y LED de potencia mediante PWM.

## Estructura

```text
src/python/    → Simulador del reactor
src/esp32/     → Código para ESP32
tests/python/  → Pruebas del simulador
tests/esp32/   → Pruebas y validaciones del hardware
docs/          → Evidencias y documentación