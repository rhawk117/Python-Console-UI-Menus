import os
import keyboard
from colorify import ConsoleStencil
import time 
import msvcrt
import sys 

class MenuError(Exception):
    '''base class for all menu errors'''
    

class EmptyMenuError(MenuError):
    """Raised when trying to create a menu with no options."""
    pass

class InvalidPageSizeError(MenuError):
    """Raised when an invalid page size is provided."""
    pass

class MenuStyle:
    VALID_STYLES: dict[str, set[str]]= {
        'ansi': {'bold', 'underline', 'italic', 'normal'},
        'style': {'bright', 'dim', 'normal', 'reset_all'},
        'fg_color': {'red', 'green', 'blue', 'yellow', 'magenta', 'cyan', 'white', 'black'},
        'bg_color': {'red', 'green', 'blue', 'yellow', 'magenta', 'cyan', 'white', 'black'}
    }
    DEFAULT_SELECTED: dict[str, str] = {'fg_color': 'black', 'bg_color': 'white','ansi': 'bold',
    'style': 'bright'}

    DEFAULT_UNSELECTED: dict[str, str] = {'ansi': 'italic', 'style': 'dim'}

    DEFAULT_PROMPT: dict[str, str] = {'ansi': 'bold', 'style': 'bright'}

    
    @staticmethod
    def create_default():
        return MenuStyle(MenuStyle.DEFAULT_SELECTED, MenuStyle.DEFAULT_UNSELECTED, MenuStyle.DEFAULT_PROMPT)

    @staticmethod
    def validate_style(style: dict[str, str]) -> dict[str, str]:
        '''
            Validates the style dictionary to ensure that the key word arguments
            are valid and can be applied to the ConsoleStencil.multi_style() method.
        '''
        if not style:
            return {}
        
        valid_style = {}
        for key, value in style.items():
            value = value.lower()
            if key in MenuStyle.VALID_STYLES and value in MenuStyle.VALID_STYLES[key]:
                valid_style[key] = value
            else:
                print(f"[ ! ] WARNING: Invalid style { key }: '{ value }'. This style will be ignored.")
        return valid_style
    
    def __init__(self, selected: dict[str, str], unselected: dict[str, str], prompt: dict[str, str]) -> None:
        '''
            With the use of the ConsoleStencil Class you can create your own custom
            style for each of the selected and unselected options in the menu using
            dictionaries that contain the keyword arguments for the ConsoleStencil.multi_style()
            method which has the following kwargs.
            
            ansi (str, optional): The text style such as 'bold', 'underline', italicize
            style (str, optional): The colorama style such as 'bright', 'dim', 'normal'.
            
            fg_color (str, optional): The foreground color.
            bg_color (str, optional): The background color.
            
            ^- Accepted Colors: 'red', 'green', 'blue', 'yellow', 'magenta', 'cyan',
            'white', 'black'.
            
            
            NOTE: The values must be one of the ones listed above to be applied.
        '''
        self.selected_style: dict = MenuStyle.validate_style(selected)
        self.unselected_style: dict = MenuStyle.validate_style(unselected)
        self.prompt_style: dict = MenuStyle.validate_style(prompt)
        self.__apply_default()
    
    def __apply_default(self) -> None:
        '''
            If while validating the style dictionaries, the user did not provide any values
            or all values were invalid resulting in an empty dictionary, the default style
            will be applied to the respective invalid styles.
        '''
        if not self.selected_style:
            self.selected_style = MenuStyle.DEFAULT_SELECTED

        if not self.unselected_style:
            self.unselected_style = MenuStyle.DEFAULT_UNSELECTED

        if not self.prompt_style:
            self.prompt_style = MenuStyle.DEFAULT_PROMPT
    
    def apply_option_style(self, option: str, is_selected: bool) -> str:
        option = f'[ { option } ]'
        if is_selected:
            option = f'⇒ { option } ⇐'
            stylized = self.selected_style
        else:
            stylized = self.unselected_style
            
        return ConsoleStencil.multi_style(option, **stylized)
    
    def prompt_stylize(self, prompt: str) -> str:
        prompt = f'[ < ? > { prompt } < ? > ]'
        return ConsoleStencil.multi_style(prompt, **self.prompt_style)

class HorizontalSizeError(MenuError):
    '''Raised when the number of options exceeds the screen width.'''
    pass


class BaseMenu:
    def __init__(self, options: list[str], prompt: str, menu_style: MenuStyle = None) -> None:
        if len(options) == 0:
            raise EmptyMenuError('ERROR: Menus must have at least one option')

        self.options: list[str] = options
        self.prompt: str = prompt
        self.highlight: int = 0
        self.active: bool = False
        self.menu_style: MenuStyle = menu_style if menu_style else MenuStyle.create_default()        
    
    def clear(self) -> None:
        os.system('cls' if os.name == 'nt' else 'clear')

    def set_menu_style(self, selected: dict[str, str], unselected: dict[str, str], prompt: dict[str, str]) -> None:
        '''
            Allows to set the styling for menu by simply providing the dictionaries of the
            keyword arguments for ConsoleStencil.multi_style() method. The keys must be one of
            the following: 'ansi', 'style', 'fg_color', 'bg_color'.
            
            ansi (str, optional): The text style which are 'bold', 'underline', italicize
            style (str, optional): The colorama style which are 'bright', 'dim', 'normal'.
            
            fg_color (str, optional): The foreground color.
            bg_color (str, optional): The background color.
            
            ^- Accepted Colors: 'red', 'green', 'blue', 'yellow', 'magenta', 'cyan',
            'white', 'black'.
            
            If all arguments for any of the dictionaries passed fail to validate the default
            for the respective style is applied.
        '''
        
        self.menu_style = MenuStyle(selected, unselected, prompt)
        
    def show(self) -> None:
        raise NotImplementedError('ERROR: Called on Base Class, Subclasses must implement this method')

    def run(self) -> str:
        '''
            Menu UI Loop that returns the option selected 
            by the user. 
            
            The menu is controlled by the 'active' attribute which is set to True upon method call
            when the menu is running. The loop will continue to run until the user presses the 'enter'
            
        '''
        self.active = True
        while self.active:
            self.show()
            key = keyboard.read_event()
            if key.event_type != keyboard.KEY_DOWN:
                continue
            if key.name == 'enter':
                    break
            self.handle_keys(key)
            time.sleep(0.01)
        return self.options[self.highlight]

    def handle_keys(self, key) -> None:
        raise NotImplementedError('ERROR: Called on Base Class, Subclasses must implement this method')

    def move_down(self) -> None:
        self.highlight = (self.highlight + 1) % len(self.options)
    
    def move_up(self) -> None:
        self.highlight = (self.highlight - 1) % len(self.options)
    
    def exit_ui(self) -> None:
        self.active = False

class VerticalMenu(BaseMenu):
    def show(self) -> None:
        self.clear()
        prompt = self.menu_style.prompt_stylize(self.prompt)
        print(prompt)
        for idx, item in enumerate(self.options):
            option = self.menu_style.apply_option_style(item, idx == self.highlight)
            print(option)
                
    def handle_keys(self, key: keyboard.KeyboardEvent) -> None:
        if key.name == 'up':
            self.move_up()
        elif key.name == 'down':
            self.move_down()



class HorizontalMenu(BaseMenu):
    def __init__(self, options: list[str], prompt: str, menu_style: MenuStyle = None) -> None:
        super().__init__(options, prompt, menu_style)
        if len(options) > 6:
            raise HorizontalSizeError('ERROR: Horizontal Menus must have 6 or fewer options or they wont fit on the screen')
        self.active = False
        self.highlight = 0
    
    def show(self):
        self.clear()
        prompt = self.menu_style.prompt_stylize(self.prompt)
        print(prompt)
        for idx, item in enumerate(self.options):
            self.menu_style.apply_option_style(item, idx == self.highlight)
        print()
        
    def handle_keys(self, key: keyboard.KeyboardEvent) -> None:
        if key.name == 'left':
            self.move_up()
        elif key.name == 'right':
            self.move_down()

# def __init__(self, options: list[str], prompt: str, menu_style: MenuStyle = None) -> None:


class PagedMenu(BaseMenu):
    NAV_GUIDE = "\t< i > Move ↑/↓  | Page ←/→ | Select Enter  < i >"

    def __init__(self, options: list[str], prompt: str, menu_style: MenuStyle = None, 
    page_size: int = 3):
        self.__guard_ctor(page_size, options)
        super().__init__(options, prompt, menu_style)
        self.running: bool = False
        self.__setup_menu(page_size)
        
    def __setup_menu(self, page_size: int) -> None:
        '''
            sets up attributes / properties required
            for the paged menu to function correctly
        '''
        self.page_size: int = page_size
        self.total_pages: int = (len(self.options) + page_size - 1) // page_size
        self.current_page: int = 1
        self.highlight: int = 0
        
    def __guard_ctor(self, page_size: int, options: list) -> None:
        if page_size <= 0:
            raise ValueError("[ ERROR ] Page size must be greater than zero.")
        if page_size > len(options):
            raise InvalidPageSizeError(
                "[ ERROR ] Page size must be less than or equal to the number of options.")

    @property
    def current_page(self) -> int:
        return self._current_page

    @current_page.setter
    def current_page(self, value: int) -> None:
        ''''
            Allows the current page to bounce on first and last 
        '''
        if value < 1:
            self._current_page = self.total_pages

        elif value > self.total_pages:
            self._current_page = 1

        else:
            self._current_page = value

        self.highlight = 0

    @property
    def current_page_options(self) -> list[str]:
        '''
            Refreshes the items on each page 
        '''
        start = (self.current_page - 1) * self.page_size
        end = start + self.page_size
        return self.options[start: end]

    def __title_text(self) -> None:
        bar = '*' * 100
        nav_txt = ConsoleStencil.multi_style(
            f'{ bar }\n{ self.NAV_GUIDE }\n{ bar }\n', ansi='italic', style='dim'
        )
        prompt_txt = self.menu_style.prompt_stylize(self.prompt)
        print(
        f'{ nav_txt }{ prompt_txt } - [ Page { self.current_page } / { self.total_pages } ]\n'
        )
        
    def show(self) -> None:
        '''
            Displays the UI in the Console highlighting
            the currently selected option.
        '''
        self.clear()
        self.__title_text()
        for idx, option in enumerate(self.current_page_options):
            opt = self.menu_style.apply_option_style(option, 
            idx == self.highlight)
            print(opt)
        print('*' * 100)

    def handle_keys(self, key: keyboard.KeyboardEvent) -> None:
        '''
            Handles user keyboard input and manipulates list of
            options; properties handle the 'bouncing' allowing 
            last and first pages to seemlessly transition.
        '''
        if key.name == 'up':
            self.highlight = (self.highlight - 1) % len(self.current_page_options)

        elif key.name == 'down':
            self.highlight = (self.highlight + 1) % len(self.current_page_options)

        elif key.name == 'left':
            self.current_page -= 1

        elif key.name == 'right':
            self.current_page += 1

        elif key.name == 'enter':
            self.running = False
    

    def run(self) -> str:
        self.running = True
        while self.running:
            self.show()
            key = keyboard.read_event()
            if key.event_type != keyboard.KEY_DOWN:
                continue
            self.handle_keys(key)
            time.sleep(0.01)
        return self.current_page_options[self.highlight]

class CharMenuStyle:
    OPTION_DEFAULT = {
        'ansi' : 'italic',
        'style' : 'bright'
    }
    PROMPT_DEFAULT = {
        'ansi' : 'bold',
        'style' : 'bright'
    }
    
    def __init__(self, option_style: dict[str, str] = {}, prompt_style: dict[str, str] = {}) -> None:
        self.option_style = self.__stylize(option_style)
        self.prompt_style = self.__stylize(prompt_style)
    
    def __stylize(self, styling: dict[str,str]) -> None:
        styling = MenuStyle.validate_style(styling)
        return styling if styling else CharMenuStyle.OPTION_DEFAULT
    
    @staticmethod
    def create_default():
        return CharMenuStyle(CharMenuStyle.OPTION_DEFAULT, CharMenuStyle.PROMPT_DEFAULT)
    
    def apply_option(self, option: str) -> str:
        return ConsoleStencil.multi_style(option, **self.option_style)
    
    def apply_prompt(self, prompt: str) -> str:
        return ConsoleStencil.multi_style(prompt, **self.prompt_style)

        
class CharMenu:
    def __init__(self, key_map: dict[str, str], prompt: str, option_style: CharMenuStyle = None) -> None:
        '''
            Args:
                key_map (dict[str, str]): A dictionary mapping keys to options
                (e.g {'a': 'Option 1', 'b': 'Option 2'})
                
                prompt (str): The prompt to show at the top of the menu
        '''
        if len(key_map) == 0:
            raise ValueError('ERROR: Menus must have at least one option')
        self.key_map: dict[str, str] = key_map
        self.prompt: str = prompt
        self.style: CharMenuStyle = option_style if option_style else CharMenuStyle.create_default()
        
    def __read_key(self) -> str:
        '''
            Reads a single key without the need for the user to press enter
            built for both Unix and Windows 
        '''
        if os.name == 'nt':
            return msvcrt.getch().decode('utf-8')
        else:
            return self.__unix_read_key()
    
    def __unix_read_key(self) -> str:
        import termios
        import tty
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch.encode('utf-8')

    def show(self) -> None:
        os.system('cls' if os.name == 'nt' else 'clear')
        print(self.style.apply_prompt(f'[ < ? > {self.prompt} < ? > ]'))
        for key, value in self.key_map.items():
            print(self.style.apply_option(f'[ {key} ] - {value}'))
            
    def run(self) -> str:
        key = None
        while not key in self.key_map.keys():
            self.show()
            key = self.__read_key()
        return self.key_map[key]
    

def test_vertical_menu():
    print("Testing VerticalMenu...")

    input()
    options = ["New Game", "Load Game", "Settings", "Exit"]
    menu = VerticalMenu(options, "Main Menu")
    selected = menu.run()
    print(f"You selected: {selected}\n")

    # Custom Styling
    custom_style = MenuStyle(
        selected={'fg_color': 'green', 'bg_color': 'black',
                  'ansi': 'bold', 'style': 'bright'},
        unselected={'fg_color': 'cyan', 'ansi': 'italic'},
        prompt={'fg_color': 'yellow', 'ansi': 'underline'}
    )
    menu = VerticalMenu(options, "Main Menu (Custom Style)", custom_style)
    selected = menu.run()
    print(f"You selected: {selected}\n")

    # Error Handling - Invalid Style
    invalid_style = MenuStyle(
        selected={'fg_color': 'purple', 'bg_style': 'glow'},
        unselected={'fg_color': 'orange', 'style': 'blink'},
        prompt={'fg_color': 'rainbow', 'ansi': 'shadow'}
    )
    menu = VerticalMenu(options, "Main Menu (Invalid Style)", invalid_style)
    selected = menu.run()
    print(f"You selected: {selected}\n")

    # Error Handling - Empty Options List
    try:
        menu = VerticalMenu([], "Empty Menu")
    except ValueError as e:
        print(f"Caught error: {e}\n")


def test_horizontal_menu():
    print("Testing HorizontalMenu...")
    input()
    # Basic Usage
    options = ["Home", "Shop", "About", "Contact"]
    menu = HorizontalMenu(options, "Navigation")
    selected = menu.run()
    print(f"You selected: {selected}\n")

    # Custom Styling
    custom_style = MenuStyle(
        selected={'fg_color': 'blue', 'bg_color': 'white',
                  'ansi': 'bold', 'style': 'bright'},
        unselected={'fg_color': 'white', 'bg_color': 'blue', 'ansi': 'italic'},
        prompt={'fg_color': 'magenta', 'ansi': 'underline', 'style': 'bright'}
    )
    menu = HorizontalMenu(options, "Navigation (Custom Style)", custom_style)
    selected = menu.run()
    print(f"You selected: {selected}\n")

    # Error Handling - Too Many Options
    try:
        many_options = ["Home", "Shop", "About",
                        "Contact", "Blog", "FAQ", "Careers"]
        menu = HorizontalMenu(many_options, "Too Many Options")
    except ValueError as e:
        print(f"Caught error: {e}\n")

    # Error Handling - Empty Options List
    try:
        menu = HorizontalMenu([], "Empty Menu")
    except ValueError as e:
        print(f"Caught error: {e}\n")
        

def test_char_menu():
    print("Testing CharMenu...")
    input()
    # Basic Usage
    key_map = {
        'a': 'Attack',
        'd': 'Defend',
        'r': 'Run',
        'i': 'Item'
    }
    menu = CharMenu(key_map, "Battle Options")
    selected = menu.run()
    print(f"You selected: {selected}\n")

    # Custom Styling - Options
    option_style = CharMenuStyle(
        option_style={'fg_color': 'yellow', 'ansi': 'bold', 'style': 'bright'},
        prompt_style={'fg_color': 'green',
                      'ansi': 'underline', 'style': 'bright'}
    )
    menu = CharMenu(key_map, "Battle Options (Custom Style)", option_style)
    selected = menu.run()
    print(f"You selected: {selected}\n")

    # Custom Styling - Prompt Only
    prompt_style = CharMenuStyle(
        prompt_style={'fg_color': 'red', 'ansi': 'bold', 'style': 'bright'}
    )
    menu = CharMenu(key_map, "Battle Options (Custom Prompt)", prompt_style)
    selected = menu.run()
    print(f"You selected: {selected}\n")

    # Error Handling - Invalid Style
    invalid_style = CharMenuStyle(
        option_style={'fg_color': 'purple', 'bg_style': 'glow'},
        prompt_style={'fg_color': 'rainbow', 'ansi': 'shadow'}
    )
    menu = CharMenu(key_map, "Battle Options (Invalid Style)", invalid_style)
    selected = menu.run()
    print(f"You selected: {selected}\n")

    # Error Handling - Empty Key Map
    try:
        menu = CharMenu({}, "Empty Options")
    except ValueError as e:
        print(f"Caught error: {e}\n")


def test_paged():
    options = [f"Option {i} " for i in range(51)]
    menu = PagedMenu(options, "Testing (shrexd)", page_size=10)
    choice = menu.run()
    
    print(f'You selected { choice }')
    
    
    





def main() -> None:
    # test_vertical_menu()
    # test_horizontal_menu()
    # test_char_menu()
    test_paged()



if __name__ == "__main__":
    main()
