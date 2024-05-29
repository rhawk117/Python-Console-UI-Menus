import os
import keyboard
from colorama import init, Fore, Back, Style

init(autoreset=True)

class BaseMenu:
    def __init__(self, options: list[str], prompt: str) -> None:
        if len(options) == 0:
            raise ValueError('ERROR: Menus must have at least one option')
        self.options: list[str] = options
        self.prompt: str = prompt
        self.highlight: int = 0

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
        return self.options[self.highlight]

    def handle_keys(self, key) -> None:
        if key.name in ['up', 'left']:
            self.highlight = (self.highlight - 1) % len(self.options)
            
        elif key.name in ['down', 'right']:
            self.highlight = (self.highlight + 1) % len(self.options)

    def clear_screen(self) -> None:
        os.system('cls' if os.name == 'nt' else 'clear')


class VerticalMenu(BaseMenu):
    def show_options(self) -> None:
        self.clear_screen()
        print(self.prompt)
        for idx, item in enumerate(self.options):
            if idx == self.highlight:
                print(f"{ Back.WHITE }{ Fore.BLACK }>> [ { item } ]{ Style.RESET_ALL }")
            else:
                print(f"   [ { item } ]")


class HorizontalMenu(BaseMenu):
    def show_options(self):
        self.clear_screen()
        print(self.prompt)
        for idx, item in enumerate(self.options):
            if idx == self.highlight:
                print(f"{Back.WHITE}{Fore.BLACK} [ {item} ] {Style.RESET_ALL}", end="    ")
            else:
                print(f" [ {item} ] ", end="    ")
        print()


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




if __name__ == "__main__":
    vertical_demo()
    # horizontal_demo()
    
