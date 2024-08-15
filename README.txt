INFORMACION DE LA CONSTRUCCION DE NIVELES EN TILED:

Pozos invisibles:Para hacer pozos invisibles se deben crear capas por cada pozo llamadas FalseFloor sumados a un indice.Por ejemplo: FalseFloor1, FalseFloor2. Este indice no debe saltarse, es decir, no puede existir un FalseFloor1 y un FalseFloor3 y no existir un FalseFloor2.

Puentes convencionales:Para crear puentes deben hacer lo mismo que los FalseFloor pero poniendo Bridge en su lugar.

Pozos convencionales: Se debe poner Hole.

Puentes Activables: Son puentes que requieren si o si de la capa que viene a continuacion. Son puentes que pueden ser activados por una llave, para que sean creibles deben ponerse sobre un pozo convencional o un pozo invisible, si estan sobre un pozo invisible lo haran visible. Para poder usar esta capa debe ponerse, al igual que los anteriores con su indice, ManualBridge

Llave de los Puentes Activables: Activaran al puente que tenga su mismo indice, debajo de esta capa debe haber algo que la remplaze, ya que al activarse se hara invisible, es decir, si se pone como llave un cofre, debera ponerse un cofre abierto en la capa inferior para que de la ilusion de que se activo. El nombre de la capa debe ser ManualBridgeKey, con su respectivo indice.

