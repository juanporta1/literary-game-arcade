INFORMACION DE LA CONSTRUCCION DE NIVELES EN TILED:

1:Para hacer pozos invisibles se deben crear capas por cada pozo llamadas FalseFloor sumados a un indice.Por ejemplo: FalseFloor1, FalseFloor2. Este indice no debe saltarse, es decir, no puede existir un FalseFloor1 y un FalseFloor3 y no existir un FalseFloor2.

2:Para crear puentes deben hacer lo mismo que los FalseFloor pero poniendo Bridge en su lugar.