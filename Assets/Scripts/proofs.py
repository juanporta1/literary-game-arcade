import arcade
import arcade.gui

# Constantes
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Menú de Juego"

class MenuView(arcade.View):
    def __init__(self):
        super().__init__()
        self.manager = arcade.gui.UIManager()
        self.manager.enable()
        
        # Crear un contenedor para los botones
        self.v_box = arcade.gui.UIBoxLayout()

        # Botón "Jugar"
        play_button = arcade.gui.UIFlatButton(text="Jugar", width=200)
        self.v_box.add(play_button.with_space_around(bottom=20))
        play_button.on_click = self.on_click_play

        # Botón "Salir"
        quit_button = arcade.gui.UIFlatButton(text="Salir", width=200)
        self.v_box.add(quit_button.with_space_around(bottom=20))
        quit_button.on_click = self.on_click_quit

        # Centrar los botones en la pantalla
        self.manager.add(
            arcade.gui.UIAnchorWidget(
                anchor_x="center_x",
                anchor_y="center_y",
                child=self.v_box
            )
        )

    def on_click_play(self, event):
        game_view = GameView()
        self.window.show_view(game_view)

    def on_click_quit(self, event):
        arcade.close_window()

    def on_show(self):
        arcade.set_background_color(arcade.color.AMAZON)

    def on_draw(self):
        self.clear()
        self.manager.draw()

    def on_hide_view(self):
        self.manager.disable()

class GameView(arcade.View):
    def on_show(self):
        arcade.set_background_color(arcade.color.BLUE)

    def on_draw(self):
        self.clear()
        arcade.draw_text("Juego en Progreso", SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2,
                         arcade.color.WHITE, font_size=50, anchor_x="center")

def main():
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    menu_view = MenuView()
    window.show_view(menu_view)
    arcade.run()

if __name__ == "__main__":
    main()