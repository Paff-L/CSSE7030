import sys
import tkinter as tk
from tkinter import messagebox
from typing import Union, Callable
from PIL import ImageTk, Image

from a3_support import AbstractGrid
from a2_solution import *
from constants import *


# Write your classes here
# Task 1
# 3.2.1 LevelView
class LevelView(AbstractGrid):
    """ displays the maze (tiles) along with the entities."""

    def __init__(
            self,
            master: Union[tk.Tk, tk.Frame],
            dimensions: tuple[int, int],
            size: tuple[int, int],
            **kwargs
    ) -> None:
        """ Constructor for LevelView.

        Parameters:
            master: The master frame of this Canvas
            dimensions: the dimension of current level
            size: the width and height of level frame
        """
        super().__init__(master, dimensions, size, **kwargs)
        self._dimensions = dimensions

    def draw(
            self,
            tiles: list[list[Tile]],
            items: dict[tuple[int, int], Item],
            player_pos: tuple[int, int]
    ) -> None:
        """ Draw current level in the LevelView using rectangles and ovals.

        Parameters:
            tiles: The tiles of the maze
            items: The items on the maze
            player_pos: The position of the player
        """
        rows, columns = self._dimensions

        # redraw the level
        # draw tiles of current level
        for row in range(rows):
            for column in range(columns):
                tile_name = tiles[row][column].get_id()
                color = TILE_COLOURS[tile_name]
                self.create_rectangle(self.get_bbox((row, column)), fill=color)

        # draw items on the maze
        for position, item in items.items():
            item_id = item.get_id()
            color = ENTITY_COLOURS[item_id]
            self.create_oval(self.get_bbox(position), fill=color)
            self.create_text(self.get_midpoint(position), text=item_id, font=TEXT_FONT)

        # draw player
        color = ENTITY_COLOURS[PLAYER]
        self.create_oval(self.get_bbox(player_pos), fill=color)
        self.create_text(self.get_midpoint(player_pos), text='P', font=TEXT_FONT)


# 3.2.2 StatsView
class StatsView(AbstractGrid):
    """ Displays the player’s stats (HP, health, thirst), along with the number of coins collected. """

    def __init__(
            self,
            master: Union[tk.Tk, tk.Frame],
            width: int,
            **kwargs
    ) -> None:
        """ Constructor for StatsView.

        Parameter:
            master: The master frame of this Canvas.
            width: The width in pixels of StatsView.
        """
        super().__init__(master, (2, 4), (width, STATS_HEIGHT), **kwargs)
        self.config(bg=THEME_COLOUR)

    def draw_stats(self, player_stats: tuple[int, int, int]) -> None:
        """ Draw player stats: HP, hunger, thirst.

        Parameter:
            player_stats: The (HP, hunger, thirst) of player.
        """
        self.annotate_position((0, 0), 'HP')
        self.annotate_position((0, 1), 'Hunger')
        self.annotate_position((0, 2), 'Thirst')
        self.annotate_position((1, 0), str(player_stats[0]))
        self.annotate_position((1, 1), str(player_stats[1]))
        self.annotate_position((1, 2), str(player_stats[2]))

    def draw_coins(self, num_coins: int) -> None:
        """ Draw the number of coins in player inventory.

        Parameter:
            num_coins: The number of coins in inventory.
        """
        self.annotate_position((0, 3), 'Coins')
        self.annotate_position((1, 3), str(num_coins))


# 3.2.3 InventoryView
class InventoryView(tk.Frame):
    """ Displays the items in player inventory. """

    def __init__(self, master: Union[tk.Tk, tk.Frame], **kwargs) -> None:
        """ Creates a new InventoryView within master.

        Parameter:
            master: The master frame of this frame.
        """
        self.master = master
        super().__init__(self.master, **kwargs)

    def set_click_callback(self, callback: Callable[[str], None]) -> None:
        """ Sets the function to be called when an item is clicked.

        Parameter:
            callback: The function to be called.
        """
        # self.bind('<Button>', callback)
        self._callback = callback

    def clear(self):
        """ Clears all child widgets from this InventoryView. """
        for widget in self.winfo_children():
            widget.destroy()

    def _draw_item(self, name: str, num: int, colour: str) -> None:
        """ Creates and binds a single tk.Label in the InventoryView frame.

        parameter:
            name: the name of the item
            num: the number of item in inventory
            colour: the background colour of item label.
        """
        self.label = label = tk.Label(self, text=f"{name}: {num}", bg=colour, font=TEXT_FONT)
        label.pack(fill=tk.X)

        # binds if a callback exists
        if self._callback:
            label.bind("<Button>", lambda e: self._callback(name))

    def draw_inventory(self, inventory: Inventory) -> None:
        """ Draws any 'non-coin' inventory items with their quantities
        and binds the callback for each, if a click callback has been set.

        Parameter:
            inventory: the player inventory
        """
        inventory_title = tk.Label(self, text="Inventory", font=HEADING_FONT)
        inventory_title.pack(fill=tk.X)
        items = inventory.get_items()
        for key in items:
            if key != 'Coin':
                colour = ENTITY_COLOURS[items[key][0].get_id()]
                self._draw_item(key, len(items[key]), colour)


# 3.2.4 GraphicalInterface
class GraphicalInterface(UserInterface):
    def __init__(self, master: tk.Tk):
        """ Creates a new GraphicalInterface.

        Parameter:
            master: the master frame of this canvas.
        """
        self.master = master
        title = tk.Label(master, text='MazeRunner', font=BANNER_FONT, background=THEME_COLOUR)
        title.pack(fill=tk.X)

    def _step(self):
        """ Draw timer per second. """
        self.timer += 1
        self.control_view.draw_timer(self.timer)
        self.master.after(1000, self._step)

    def create_interface(self, dimensions: tuple[int, int]) -> None:
        """ Creates the components (level, inventory, stats view) in the master frame for this interface. """
        # frame for level & inventory
        frame = tk.Frame(self.master)
        frame.pack(fill=tk.BOTH)

        # Level View:
        # TASK = 1, class LevelView work
        # TASK = 2, class ImageLevelView work
        size = (MAZE_WIDTH, MAZE_HEIGHT)
        if TASK == 1:
            self.level_view = LevelView(frame, dimensions, size)
        else:
            self.level_view = ImageLevelView(frame, dimensions, size)
        self.level_view.pack(side=tk.LEFT)

        # Inventory View
        self.inventory_view = InventoryView(frame)
        self.inventory_view.pack(side=tk.LEFT, expand=tk.TRUE, fill=tk.BOTH)
        # stats_view
        self.stats_view = StatsView(self.master, MAZE_WIDTH + INVENTORY_WIDTH)
        self.stats_view.pack()

    def create_file_manu(self, restart, save_game, load_games):
        """ Create file menu with different function.

        Parameter:
            restart: the callback when click on Restart Game.
            save_game: the callback when click on Save Game.
            load_game: the callback when click on Load Game.
        """
        FileMenu(self.master, restart, save_game, load_games)

    def create_control_frame(self, restart, new_game, buy_item):
        """ Create control frame.

        Parameter:
            restart: the callback when click on Restart Game.
            new_game: the callback when click on New game.
            buy_item: the callback when buying an item in the shop.
        """
        self.timer = 0
        self.control_view = ControlsFrame(self.master, restart, new_game, buy_item, self.timer)
        self.control_view.pack(fill=tk.X, expand=tk.TRUE)
        self.master.after(1000, self._step)

    def clear_all(self) -> None:
        """  Clears each of the three major components
        (do not delete the component instances, just clear them). """
        self.level_view.clear()
        self.inventory_view.clear()
        self.stats_view.clear()

    def set_maze_dimensions(self, dimensions: tuple[int, int]) -> None:
        """ Updates the dimensions of the maze in the level to dimensions.

        Parameter:
            dimensions: new dimensions (#rows, #columns)
        """
        self.level_view.set_dimensions(dimensions)

    def bind_keypress(self, command: Callable[[tk.Event], None]) -> None:
        """ Binds the given command to the general keypress event.

        Parameter:
            command: a function which takes in the keypress event
        """
        self.master.bind('<Key>', command)

    def set_inventory_callback(self, callback: Callable[[str], None]) -> None:
        """ Sets the function to be called when an item is clicked in the inventory view to be callback.

        Parameter:
            callback: the function to be called.
        """
        self.inventory_view.set_click_callback(callback)

    def draw_inventory(self, inventory: Inventory) -> None:
        """ Draws any non-coin inventory items with their quantities and binds the callback for each,
            if a click callback has been set.

        Parameter:
            inventory: the player inventory
        """
        self.inventory_view.draw_inventory(inventory)

    def draw(
            self,
            maze: Maze,
            items: dict[tuple[int, int], Item],
            player_position: tuple[int, int],
            inventory: Inventory,
            player_stats: tuple[int, int, int]
    ) -> None:
        """ Clear the three major components and redraw them with the new state.

        Parameter:
            maze: maze of current level
            items: items on the maze
            player_position: (#row, #column)
            inventory: the player inventory
            player_stats: player (HP, hunger, thirst)
        """
        self.clear_all()
        self._draw_level(maze, items, player_position)
        self._draw_player_stats(player_stats)
        self._draw_inventory(inventory)

    def _draw_inventory(self, inventory: Inventory) -> None:
        """ Draw both the non-coin items on the inventory view and the coins on the stats view.

        Parameter:
            inventory: the player inventory
        """
        # draw non-coin items on inventory view
        self.draw_inventory(inventory)
        # draw coins on stats view
        self.coin_num = len(inventory.get_items().get('Coin', ''))
        self.stats_view.draw_coins(self.coin_num)

    def _draw_level(
            self,
            maze: Maze,
            items: dict[tuple[int, int], Item],
            player_position: tuple[int, int]
    ) -> None:
        """ Draw current level with given information.

        Parameter:
            maze: maze of current level
            items: items on the maze
            player_position: (#row, #column)
        """
        self.level_view.draw(maze.get_tiles(), items, player_position)

    def _draw_player_stats(self, player_stats: tuple[int, int, int]) -> None:
        """ Draw player stats with given information.

        Parameter:
            player_stats: the (HP, hunger, thirst) of the player
        """
        self.stats_view.draw_stats(player_stats)


# 3.3 controller class
# 3.3.1 GraphicalMazeRunner
class GraphicalMazeRunner(MazeRunner):
    """ Graphical controller of the game. """

    def __init__(self, game_file: str, root: tk.Tk) -> None:
        """ Creates a new GraphicalMazeRunner game,
        with the view inside the given root widget.

        Parameter:
            game_file: Path to the file from which the game levels are loaded
            root: the root of the GUI
        """
        self.root = root
        self._game_file = game_file
        self.model = Model(game_file)
        self.graphical_interface = GraphicalInterface(root)

    def _handle_keypress(self, e: tk.Event) -> None:
        """ Handles a keypress.

        Parameter:
            e: keypress event ('a', 's', 'd', 'w')
        """
        # move if not win the game
        if not self.model.has_won():
            if e.char in (UP, DOWN, LEFT, RIGHT):
                self.model.move_player(MOVE_DELTAS.get(e.char))

                if self.model.did_level_up():
                    new_dimensions = self.model.get_level().get_dimensions()
                    self.graphical_interface.set_maze_dimensions(new_dimensions)

        # determine win or lose game
        if self.model.has_won():
            messagebox.showinfo(message=WIN_MESSAGE)
        elif self.model.has_lost():
            messagebox.showinfo(message=LOSS_MESSAGE)
        else:
            self._draw()

    def _draw(self) -> None:
        """ Redraw the graphical interface with updated information. """
        level = self.model.get_level()
        player = self.model.get_player()

        self.graphical_interface.draw(
            level.get_maze(),
            level.get_items(),
            player.get_position(),
            player.get_inventory(),
            self.model.get_player_stats())

    def _apply_item(self, item_name: str) -> None:
        """ Attempts to apply an item with the given name to the player.

        Parameter:
            item_name: the name of item that will be applied.
        """
        item = self.model.get_player().get_inventory().remove_item(item_name)
        item.apply(self.model.get_player())
        self._draw()

    def _restart_game(self) -> None:
        """ Reset the model with current game_file. """
        self.model = Model(self._game_file)
        dimensions = self.model.get_current_maze().get_dimensions()
        self.graphical_interface.set_maze_dimensions(dimensions)
        self.graphical_interface.timer = 0
        self.graphical_interface.control_view.draw_timer(self.graphical_interface.timer)
        self._draw()

    def _new_game(self) -> None:
        """ Start a new game with game file that user input. """
        self.view = view = tk.Toplevel()
        self.entry = tk.Entry(view)
        self.entry.pack()
        submit = tk.Button(view, text="submit", command=self._start_new_game)
        submit.pack()

    def _start_new_game(self) -> None:
        """ Start new game.

        Raises:
            FileNotFoundError: An error occurs if input file name is invalid"""
        # start a new game if input file name is valid
        try:
            self._game_file = self.entry.get()
            self.model = Model(self._game_file)
            self.view.destroy()
            dimensions = self.model.get_current_maze().get_dimensions()
            self.graphical_interface.set_maze_dimensions(dimensions)
            self.graphical_interface.timer = 0
            self._draw()

        # show messagebox if input is invalid
        except FileNotFoundError:
            messagebox.showinfo(
                title=None,
                message="Invalid File Name!")

    def _save_game(self) -> None:
        """ Prompt the user for the location to save their file. """
        level = self.model.get_level()
        player = self.model.get_player()

        # save game with necessary information
        with open('save.txt', 'w') as file:
            file.write(f"\ngame_file: {self._game_file}")
            file.write(f"\ntimer: {self.graphical_interface.timer}")
            file.write(f"\ndimensions: {level.get_dimensions()}")
            file.write(f"\nlevel_num: {self.model._level_num}")
            file.write(f"\nitems: {level.get_items()}")
            file.write(f"\nplayer_stats: {self.model.get_player_stats()}")
            file.write(f"\ninventory: {player.get_inventory().get_items()}")
            file.write(f"\nplayer_position: {player.get_position()}")

    def _load_game(self) -> None:
        """ Prompt the user for the location of the file to load a game from
        and load the game described in that file. """
        # open file, read information, and reset the game
        with open('save.txt', 'r') as file:
            for line in file:
                line = line.strip()
                if line.startswith('game_file'):
                    self._game_file = game_file = line.partition(": ")[2]
                    self.model = Model(game_file)
                if line.startswith('dimensions'):
                    dimensions = tuple(eval(line.partition(': ')[2]))
                if line.startswith('level_num'):
                    self.model._level_num = int(line.partition(': ')[2])
                if line.startswith('timer'):
                    timer = line.partition(': ')[2]
                    self.graphical_interface.timer = int(timer)
                if line.startswith('items'):
                    items = eval(line.partition(": ")[2])
                    self.model.get_level()._items = items
                if line.startswith('player_pos'):
                    player_pos = eval(line.partition(": ")[2])
                    self.model.get_player()._position = player_pos
                if line.startswith('inventory'):
                    player_inventory = eval(line.partition(": ")[2])
                    self.model.get_player_inventory()._items = player_inventory
                if line.startswith('player_stats'):
                    player_stats = eval(line.partition(": ")[2])
                    self.model.get_player()._health, \
                    self.model.get_player()._hunger, \
                    self.model.get_player()._thirst = player_stats

        self.graphical_interface.set_maze_dimensions(dimensions)
        self.model.get_level().attempt_unlock_door()
        self._draw()

    def _buy_item(self, item_name) -> None:
        """ Buy items in the shop.

        Parameter:
            item_name: name of item that the user attempt to buy
        """
        shop_items = {
            POTION: Potion((0, 0)),
            APPLE: Apple((0, 0)),
            HONEY: Honey((0, 0)),
            WATER: Water((0, 0)),
            CANDY: Candy((0, 0))
        }

        # add item to inventory if player has enough coins
        # remove coins from inventory according to the price
        if item_name in (APPLE, WATER):
            if self.graphical_interface.coin_num >= 1:
                self.model.get_player_inventory().add_item(shop_items[item_name])
                self.model.get_player_inventory().remove_item("Coin")

        elif item_name in (HONEY, POTION):
            if self.graphical_interface.coin_num >= 2:
                self.model.get_player_inventory().add_item(shop_items[item_name])
                for i in range(2):
                    self.model.get_player_inventory().remove_item('Coin')

        elif item_name == CANDY:
            if self.graphical_interface.coin_num >= 3:
                self.model.get_player_inventory().add_item(shop_items[item_name])
                for i in range(3):
                    self.model.get_player_inventory().remove_item('Coin')

        self._draw()

    def play(self) -> None:
        """ Executes the entire game until a win or loss occurs. """
        dimensions = self.model.get_level().get_dimensions()
        self.graphical_interface.create_interface(dimensions)
        self._draw()
        # create file menu and control frame
        self.graphical_interface.create_file_manu(self._restart_game, self._save_game, self._load_game)
        self.graphical_interface.create_control_frame(self._restart_game, self._new_game, self._buy_item)

        # set keypress and bind inventory callback
        self.graphical_interface.bind_keypress(self._handle_keypress)
        self.graphical_interface.set_inventory_callback(self._apply_item)


# 4.1 ImageLevelView: work when TASK = 2
class ImageLevelView(AbstractGrid):
    """ This is an extension of existing LevelView and images will be used to display the tiles and entities. """

    def __init__(
            self,
            master: Union[tk.Tk, tk.Frame],
            dimensions: tuple[int, int],
            size: tuple[int, int],
            **kwargs
    ) -> None:
        """ Constructor for ImageLevelView.

        Parameters:
            master: The master frame for this Canvas.
            dimensions: (#rows, #columns)
            size: The width and height in pixels of the LevelView.
        """
        super().__init__(master, dimensions, size, **kwargs)
        self.master = master
        self._tiles_images, self._entities_images = {}, {}
        self._size = size

    def draw(
            self,
            tiles: list[list[Tile]],
            items: dict[tuple[int, int], Item],
            player_pos: tuple[int, int]
    ) -> None:
        """ Draw current level using images.

        Parameters:
            tiles: The tiles of current level.
            items: The items on current maze.
            player_pos: Current position of player.
        """
        rows, columns = self._dimensions
        # draw tiles of current level
        for row in range(rows):
            for column in range(columns):
                tile_id = tiles[row][column].get_id()
                # draw with images
                self._load_image(TILE_IMAGES, tile_id, (row, column))

        # draw items on the maze
        for position, item in items.items():
            item_id = item.get_id()
            self._load_image(ENTITY_IMAGES, item_id, position)

        # draw player
        self._load_image(ENTITY_IMAGES, PLAYER, player_pos)

    def _load_image(
            self,
            img_dict: dict,
            image_name: str,
            position: tuple
    ) -> None:
        """ Load images of tiles and entities.

        Parameter:
            img_dict: The image file name of tiles or entities.
            image_name: The name of tile or entity that will be loaded.
            position: The position of loaded tile or entity.
        """
        img_open = Image.open("images/" + img_dict[image_name])
        img_open = img_open.resize(self.get_cell_size())
        img_png = ImageTk.PhotoImage(img_open)
        if img_dict == TILE_IMAGES:
            self._tiles_images[position] = img_png
        else:
            self._entities_images[position] = img_png

        self.create_image(self.get_midpoint(position), image=img_png)


# 4.2 Controls Frame
class ControlsFrame(tk.Frame):
    def __init__(
            self,
            master: Union[tk.Tk, tk.Frame],
            restart: Callable,
            new_game: Callable,
            buy_item=None,
            time=0,
            **kwargs
    ) -> None:
        """ Creates a new controls view within master.

        Parameter:
            master: the master frame of the controls frame
            restart: to be called when click on Restart game
            new_game: to be called when click on New game
            buy_item: to be called when the user click on items in the shop
            timer: the seconds that have elapsed since the current game began
        """
        super().__init__(master, **kwargs)
        self.master = master
        self.restart = restart
        self.new_game = new_game
        self.buy_item = buy_item
        self._shop_images = {}
        self.time = time
        self.draw()

    def draw(self) -> None:
        """ Draw buttons and timer. """
        # draw shop button if TASK == 3
        if TASK == 3:
            shop_button = tk.Button(self, text="Shop", command=self.shop_view)
            shop_button.pack(side=tk.LEFT, expand=tk.TRUE)

        restart_button = tk.Button(self, text="Restart game", command=self.restart)
        restart_button.pack(side=tk.LEFT, expand=tk.TRUE)
        new_button = tk.Button(self, text="New game", command=self.new_game)
        new_button.pack(side=tk.LEFT, expand=tk.TRUE)

        # draw timer
        minutes = self.time // 60
        seconds = self.time % 60
        self.time_frame = tk.Frame(self)
        self.time_frame.pack(side=tk.LEFT, expand=tk.TRUE)
        timer_title = tk.Label(self.time_frame, text="Timer")
        timer_title.pack()

        self.time_label = tk.Label(self.time_frame, text=f"{minutes}m {seconds}s")
        self.time_label.pack(side=tk.LEFT, expand=tk.TRUE)

    def shop_view(self) -> None:
        """ Create shop view. """
        view = tk.Toplevel()
        view.title("Shop")
        title = tk.Label(view, text="Shop", bg=THEME_COLOUR, font=HEADING_FONT)
        title.pack(fill=tk.X, expand=tk.TRUE)

        # load images of items in the shop
        for item in (APPLE, WATER, HONEY, POTION, CANDY):
            img_open = Image.open("images/" + ENTITY_IMAGES[item])
            img_open = img_open.resize((200, 200))
            img_png = ImageTk.PhotoImage(img_open)
            self._shop_images[item] = img_png

        frame1 = tk.Frame(view)
        frame1.pack(fill=tk.BOTH, expand=tk.TRUE)
        frame2 = tk.Frame(view)
        frame2.pack(fill=tk.BOTH, expand=tk.TRUE)

        # draw items with their prices
        for item, price in zip((APPLE, WATER, HONEY), ('$1', '$1', '$2')):
            self._draw_item(frame1, item, price, self.buy_item)

        for item, price in zip((POTION, CANDY), ('$2', '$3')):
            self._draw_item(frame2, item, price, self.buy_item)

        done_button = tk.Button(view, text='Done', font=TEXT_FONT, command=view.destroy)
        done_button.pack()

    def _draw_item(self, master: tk.Frame, item: str, price: str, buy_item) -> None:
        """ Draw and bind items in shop.

        Parameter:
            master: the master frame of this item
            item: the name of item to be drawn
            price: the price of the item
            buy_item: the function when click on item image
        """
        item_label = tk.Label(master, text=price, image=self._shop_images[item], compound=tk.TOP)
        item_label.pack(side=tk.LEFT, expand=True)

        # bind item if callback function exists
        if self.buy_item:
            item_label.bind("<Button>", lambda e: buy_item(item))

    def draw_timer(self, time):
        """  display the number of minutes and seconds.

        Parameter:
            time: the seconds that have elapsed since current game began
        """
        self.time_label.destroy()
        self.time_label = tk.Label(self.time_frame, text=f"{time // 60}m {time % 60}s")
        self.time_label.pack(side=tk.LEFT, expand=tk.TRUE)


# 5.2 Candy
class Candy(Food):
    """ Candy decreases the player’s hunger to 0 and health by 2. """
    _id = CANDY

    def apply(self, player: Player) -> None:
        """ Decreases hunger to 0 and health by 2. """
        player.change_hunger(-10)
        player.change_health(-2)


# 4.3 File Menu
class FileMenu(GraphicalMazeRunner):
    def __init__(
        self,
        master: Union[tk.Tk, tk.Frame],
        restart: Callable,
        save_game=None,
        load_games=None
    ) -> None:
        """ Create file menu with options. """
        self.master = master
        menu = tk.Menu(master)
        master.config(menu=menu)
        file_menu = tk.Menu(menu, tearoff=False)
        menu.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Save game", command=save_game)
        file_menu.add_command(label="Load game", command=load_games)
        file_menu.add_command(label="Restart game", command=restart)
        file_menu.add_command(label="Quit", command=self._quit_game)

    def _quit_game(self):
        """ Function of option Quit. """
        # show messagebox to prompt user click an option
        answer = messagebox.askquestion(
            title=None,
            message="Do you want to quit?"
        )
        # quit game if click yes, nothing happen if click no
        if answer == 'yes':
            quit()


# 3.4 play_game function
def play_game(root: tk.Tk):
    """ 1. Construct the controller instance.
        2. Cause gameplay to commence.
        3. Ensure the root window stays opening listening for events.
    """
    # load game
    maze_runner = GraphicalMazeRunner(GAME_FILE, root)
    maze_runner.play()

    root.mainloop()


def main():
    # Write your main function code here
    """ 1. Construct the root tk.Tk instance.
        2. Call the play game function passing in the newly created root tk.Tk instance."""
    root = tk.Tk()
    play_game(root)


if __name__ == '__main__':
    main()
