import os
import keyboard
from colorama import init, Fore, Back, Style
from console_color import TextStyler
import time 
import msvcrt

init(autoreset=True)


class MenuStyle:
    
    @staticmethod
    def print_selected(item: str) -> None:
        txt = TextStyler.multi_style_text(
            f'[ {item} ]', fg_color='black', bg_color='white', ansi='bold')
        print(txt)
        
    @staticmethod
    def print_unselected(item: str) -> None:
        txt = TextStyler.multi_style_text(f'[ { item } ]', ansi='italic', style='dim')
        print(txt)
        
    @staticmethod    
    def print_prompt(prompt) -> None:
        txt = TextStyler.multi_style_text(f'[ < ? > { prompt } < ? > ]', style='bright', ansi='italic')
        print(txt)


class BaseMenu:
    def __init__(self, options: list[str], prompt: str) -> None:
        if len(options) == 0:
            raise ValueError('ERROR: Menus must have at least one option')
        self.options: list[str] = options
        self.prompt: str = prompt
        self.highlight: int = 0
        self.clear_cmd = 'cls' if os.name == 'nt' else 'clear'

    def show_options(self) -> None:
        raise NotImplementedError('ERROR: Called on Base Class, Subclasses must implement this method')

    def run(self) -> str:
        while True:
            self.show_options()
            key = keyboard.read_event()
            if key.event_type == keyboard.KEY_DOWN:
                if key.name == 'enter':
                    break
                self.handle_keys(key)
            time.sleep(0.01)
        return self.options[self.highlight]

    def handle_keys(self, key) -> None:
        raise NotImplementedError('ERROR: Called on Base Class, Subclasses must implement this method')
        # if key.name == ['up', 'left']:
        #     self.highlight = (self.highlight - 1) % len(self.options)
            
        # elif key.name in ['down', 'right']:
        #     self.highlight = (self.highlight + 1) % len(self.options)

    def move_down(self) -> None:
        self.highlight = (self.highlight + 1) % len(self.options)
    
    def move_up(self) -> None:
        self.highlight = (self.highlight - 1) % len(self.options)

    def clear_screen(self) -> None:
        os.system(self.clear_cmd)
    

class VerticalMenu(BaseMenu):
    def show_options(self) -> None:
        self.clear_screen()
        MenuStyle.print_prompt(self.prompt)
        for idx, item in enumerate(self.options):
            if idx == self.highlight:
                MenuStyle.print_selected(item)
            else:
                MenuStyle.print_unselected(item)
                
    def handle_keys(self, key) -> None:
        if key.name == 'up':
            self.move_up()
        elif key.name == 'down':
            self.move_down()

    


class HorizontalMenu(BaseMenu):
    def show_options(self):
        self.clear_screen()
        MenuStyle.print_prompt(self.prompt)
        for idx, item in enumerate(self.options):
            if idx == self.highlight:
                txt = TextStyler.multi_style_text(f" [ {item} ] ", fg_color='black',
                                                  bg_color='white', ansi='bold')
                print(txt, end="    ")
            else:
                txt = TextStyler.multi_style_text(f" [ {item} ] ", ansi='italic', style='dim')
                print(txt, end="    ")
        print()
        
    def handle_keys(self, key) -> None:
        if key.name == 'left':
            self.move_up()
        elif key.name == 'right':
            self.move_down()


class CharMenu:
    def __init__(self, key_map: dict[str, str], prompt: str) -> None:
        if len(key_map) == 0:
            raise ValueError('ERROR: Menus must have at least one option')
        self.key_map: dict[str, str] = key_map
        self.prompt: str = prompt
        
    def read_key(self) -> str:
        return msvcrt.getch().decode('utf-8').lower()

    def show(self) -> None:
        os.system('nt')
        MenuStyle.print_prompt(self.prompt)
        for key, value in self.key_map.items():
            print(
                TextStyler.multi_style_text(f" [ { key } ] { value } ", ansi='bold', style='bright')
            )
    
    def run(self) -> str:
        key = None
        while not key in self.key_map.keys():
            self.show()
            key = self.read_key()
        return self.key_map[key]
    






def vertical_demo():
    options = ["Option 1", "Option 2", "Option 3", "Option 4"]
    menu = VerticalMenu(options, "Select an option:")
    selected_option = menu.run()
    print(f"You selected: {selected_option}")

def horizontal_demo():
    options = ["Option 1", "Option 2", "Option 3", "Option 4"]
    menu = HorizontalMenu(options, "Select an option:")
    selected_option = menu.run()
    print(f"You selected: {selected_option}")

def char_demo():
    key_map = {
        'a': 'Option 1',
        'b': 'Option 2',
        'c': 'Option 3',
    }
    menu = CharMenu(key_map, "Select an option")
    choice = menu.run()
    print(f"You selected: {choice}")
    
    



if __name__ == "__main__":
    vertical_demo()
    horizontal_demo()
    char_demo()
    
