// Guion de PRUEBA del sistema de diálogo. Texto neutro: no es contenido del guion (doc 02).
VAR decision_prueba = 0

Este es un texto de prueba del sistema de globos. # hablante: Narrador
Primera línea del personaje de prueba A. # hablante: Personaje A
¿Qué opción quieres probar? # hablante: Personaje A

* [Opción uno]
    ~ decision_prueba = 1
    Elegiste la opción uno. # hablante: Personaje B
* [Opción dos]
    ~ decision_prueba = 2
    Elegiste la opción dos. # hablante: Personaje B

- Fin de la prueba. # hablante: Narrador
-> END
