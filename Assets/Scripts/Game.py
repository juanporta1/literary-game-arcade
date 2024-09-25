import arcade
import arcade.color
import arcade.color
import arcade.gui
from Player import Player
from PauseMenu import PauseMenu
import random
from questionsMenu import QuestionMenu
from room import Room
import globalVars
from textView import TextView

class Game(arcade.View):
    global globalVars
    def __init__(self,window,menu):
        super().__init__(window)
       
        self.lastTextTwo = TextView(self.window,'Mientras sostienes el pergamino, un eco del pasado resuena en la sala: "El conocimiento es poder, pero solo en manos de los justos. No olvides las enseñanzas del caballero de la triste figura, el hobbit valiente, el retrato que desafía el tiempo y la varita mágica. Cada historia te ha mostrado que la valentía, el coraje, la autenticidad y el poder del conocimiento son esenciales para iluminar la oscuridad y guiar a otros hacia la verdad. La lectura abre puertas a mundos desconocidos y a una sabiduría profunda." Con el pergamino en mano, sabes que tu misión apenas comienza.',bg="Assets/Backgrounds/book2.jpg")
        
        self.lastTextOne = TextView(self.window,'Has recorrido el castillo, encontrando los libros ocultos y respondiendo cada pregunta con éxito. Al final del último desafío, un haz de luz ilumina la sala y aparece un mensaje: "Eres digno del conocimiento de Alden. Usa esta sabiduría con honor y responsabilidad." El castillo empieza a desvanecerse, revelando un pergamino antiguo que había estado escondido. En él, encuentras el verdadero propósito del desafío: Alden buscaba un guardián digno de su conocimiento, alguien que pudiera preservar y compartir la sabiduría con el mundo.',bg="Assets/Backgrounds/book1.jpg")
        self.fifthLevel = Room(self.window,menu,self,"Assets/Scripts/levelsInformation/level5.json")
        
        self.afterFourth = TextView(self.window,'El cuarto libro habla de un artefacto poderoso escondido en el castillo, uno que puede alterar la realidad misma. Encuentras una sala decorada con símbolos mágicos que evocan el poder de una varita que desafió al mal más oscuro. La atmósfera en la sala te recuerda que el poder, cuando se usa sabiamente, puede transformar el mundo. Sientes que el final está cerca.',bg="Assets/Backgrounds/harrypotter.jpg")
        
        self.fourthLevel = Room(self.window,menu,self,"Assets/Scripts/levelsInformation/level4.json",self.afterFourth)
        
        self.afterThird = TextView(self.window,'El tercer libro contiene un mapa antiguo del castillo. En una biblioteca oculta, descubres una pintura de un hombre cuya imagen permanece inmutable mientras él envejece en secreto. La imagen te sugiere que la verdadera esencia y el conocimiento permanecen ocultos a simple vista. Con esta reflexión, avanzas hacia la siguiente etapa del enigma.',bg="Assets/Backgrounds/doriangray.jpg")
        
        self.thirdLevel = Room(self.window,menu,self,"Assets/Scripts/levelsInformation/level3.json")
        
        self.afterSecond = TextView(self.window,'El segundo libro revela pistas sobre un antiguo hechizo perdido. Mientras avanzas, encuentras una piedra con una inscripción que alude a un hobbit que enfrentó grandes desafíos y halló coraje en su travesía. La mención de este pequeño héroe te recuerda que a veces, el valor más grande proviene de los lugares más inesperados. Continúas con renovada determinación.',bg="Assets/Backgrounds/hobbitrock.png")
        
        self.secondLevel = Room(self.window,menu,self,"Assets/Scripts/levelsInformation/level2.json")
        
        self.afterFirst = TextView(self.window,'Con el primer libro en tus manos, sientes una presencia extraña en el castillo. Mientras exploras, encuentras una inscripción en una pared que menciona a un caballero valiente con una figura triste, perdido en el tiempo y en busca de aventuras imposibles. La leyenda de este caballero parece inspirar la valentía necesaria para seguir adelante. Sigues tu camino, sabiendo que el próximo libro te espera.',None,bg="Assets/Backgrounds/quixote.jpg")
        
        self.firstLevel = Room(self.window,menu,self,"Assets/Scripts/levelsInformation/level1.json")
        
        self.firstTextTwo = TextView(self.window,'Hace poco, encontraste un mapa antiguo en una librería polvorienta, que indicaba la ubicación del castillo perdido. En el rincón de la librería, te llamó la atención un libro con una ilustración de un caballero de triste figura, un símbolo de alguien que parecía haber sido olvidado por el tiempo. Intrigado por la promesa de conocimiento y misterio, te aventuraste a explorar los antiguos salones del castillo. Sabes que superar este desafío no solo te dará acceso a sabiduría prohibida, sino que también resolverá un enigma que ha perdurado durante siglos.',bg="Assets/Backgrounds/bookmap.jpg")
        self.firstTextOne = TextView(self.window,'Te encuentras en el Castillo de Arcanum, un lugar antiguo y lleno de misterio. Hace siglos, el mago Alden escondió en este castillo los libros más valiosos de la literatura. Para preservar su conocimiento, creó un desafío: solo quien pudiera encontrar los libros y responder las preguntas literarias podría acceder a su sabiduría.',bg="Assets/Backgrounds/hallway.jpeg")
        
        self.views = [self.firstTextOne,self.firstTextTwo,self.firstLevel,self.afterFirst,self.secondLevel,self.afterSecond,self.thirdLevel,self.afterThird,self.fourthLevel,self.afterFourth,self.fifthLevel,self.lastTextOne,self.lastTextTwo]
        for i in range(len(self.views)-1):
        
            self.views[i].nextView = self.views[i+1]
            
        self.views[len(self.views)-1].nextView = menu
    def on_update(self, delta_time: float):
        self.window.show_view(self.views[0])
            
        
        
        
    
    
    