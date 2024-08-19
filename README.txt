1. Pozos Invisibles:

    Capa: FalseFloorX (donde X es el índice del pozo, por ejemplo, FalseFloor1, FalseFloor2, etc.).
    Reglas:
        Cada pozo invisible debe estar en su propia capa.
        Los índices deben ser consecutivos (no puede existir un FalseFloor1 y un FalseFloor3 sin un FalseFloor2).

2. Puentes Convencionales:

    Capa: BridgeX (donde X es el índice del puente, por ejemplo, Bridge1, Bridge2, etc.).
    Reglas:
        Similar a los pozos invisibles, cada puente debe estar en su propia capa con índices consecutivos.

3. Pozos Convencionales:

    Capa: HoleX (donde X es el índice del pozo, por ejemplo, Hole1, Hole2, etc.).
    Reglas:
        Cada pozo debe tener su capa y respetar el orden de los índices, sin saltos.

4. Puentes Activables:

    Capa: ManualBridgeX (donde X es el índice del puente activable, por ejemplo, ManualBridge1, ManualBridge2, etc.).
    Reglas:
        Estos puentes requieren una llave para ser activados.
        Deben colocarse sobre un pozo convencional (HoleX) o un pozo invisible (FalseFloorX).
        Si están sobre un pozo invisible, al activarse, el puente lo hará visible.

5. Llave de Puentes Activables:

    Capa: ManualBridgeKeyX (donde X es el índice que debe coincidir con el del puente correspondiente, por ejemplo, ManualBridgeKey1 para ManualBridge1).
    Reglas:
        Cuando se activa, la capa de la llave se vuelve invisible, por lo que se debe colocar un reemplazo visual (por ejemplo, un cofre abierto) en la capa inferior para dar la ilusión de activación.

6. Puertas con Código:

    Capas:
        CodeDoorXA y CodeDoorXB: Representan los lados de la puerta que el jugador puede interactuar para ingresar el código. La disposición de A y B es indiferente.
        CodeDoorX: Decoración de la puerta cerrada. Debajo, en la capa de decoraciones, se debe colocar la puerta abierta.
        CodeX: Objeto interactivo que muestra el código al jugador (por ejemplo, una biblioteca o un baúl). Debe tener colisión y estar sobre el suelo, no sobre un muro.

7. Sombra:

    Capas:
        ShadowX: Representa la sección inaccesible hasta que se active un dispositivo.
        UnShadowX: Dispositivo que, al activarse, permite el acceso a la sección ShadowX.
    Reglas:
        ShadowX bloquea el acceso al jugador hasta que UnShadowX se active.
        UnShadowX debe tener colisión y estar sobre el suelo.
        Al activarse, UnShadowX se vuelve invisible, por lo que se debe colocar un elemento decorativo en la capa inferior para reflejar el cambio.