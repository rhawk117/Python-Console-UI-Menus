import os
import keyboard
from colorify import ConsoleStencil
import time



class Option:
    def __init__(self, title: str, mapping, icon: str = '') -> None:
        self.title: str = title
        self.icon: str = icon
        self.mapping = mapping
    
    def show(self, is_selected: bool):
        style = f'[ { self.icon } { self.title } ]'
        if is_selected:
            return ConsoleStencil.multi_style(style, fg_color='black', 
                    bg_color='white', ansi='bold', style='bright'
            )
        else:
            return ConsoleStencil.multi_style(style, fg_color='white', 
                    bg_color='black', ansi='italic', style='dim'
            )


def clear() -> None:
    os.system('cls' if os.name == 'nt' else 'clear')

def promptify(prompt: str) -> str:
    return ConsoleStencil.multi_style(f'[ < ? > {prompt} < ? > ]', ansi='bold', style='bright')

def navify(nav: str) -> str:
    return ConsoleStencil.multi_style(f'[ {nav} ]', ansi='italic', style='dim')


class SingleMenu:
    def __init__(self, options: list[Option], prompt: str) -> None:
        self.options: list[Option] = options
        self.prompt: str = promptify(prompt)
        self.highlight: int = 0
        self.active: bool = False


    def render(self) -> None:
        clear()
        print(f'{ self.prompt } - { navify("[ Move ↑ / ↓ ]") }')
        for idx, item in enumerate(self.options):
            print(item.show(idx == self.highlight))

    def handle_keys(self, key: keyboard.KeyboardEvent) -> None:
        if key.name == 'up':
            self.highlight = (self.highlight - 1) % len(self.options)

        elif key.name == 'down':
            self.highlight = (self.highlight + 1) % len(self.options)

    def run(self) -> str:
        self.active = True
        while self.active:
            self.render()
            key = keyboard.read_event()
            if key.event_type != keyboard.KEY_DOWN:
                continue
            if key.name == 'enter':
                break
            self.handle_keys(key)
            time.sleep(0.01)
        return self.options[self.highlight]


class PagedMenu:

    def __init__(self, options: list[Option], prompt: str, page_size: int = 3):
        self.options = options
        self.prompt = promptify(prompt)
        self.running: bool = False
        self.__setup_menu(page_size)

    def __setup_menu(self, page_size: int) -> None:
        self.page_size: int = page_size
        self.total_pages: int = (len(self.options) + page_size - 1) // page_size
        self.current_page: int = 1
        self.highlight: int = 0

    @property
    def current_page_options(self) -> list[str]:
        start = (self.current_page - 1) * self.page_size
        end = start + self.page_size
        return self.options[start : end]

    
    def render(self) -> None:
        clear()
        print(f'{self.prompt} - { navify("[ < i > Move ↑/↓  | Page ←/→ | Select Enter  < i > ]") }')
        for idx, option in enumerate(self.current_page_options):
            print(option.show(idx == self.highlight))


    def handle_keys(self, key: keyboard.KeyboardEvent) -> None:
        if key.name == 'up':
            self.highlight = (self.highlight - 1) % len(self.current_page_options)

        elif key.name == 'down':
            self.highlight = (self.highlight + 1) % len(self.current_page_options)

        elif key.name == 'left':
            self.current_page = (self.current_page - 1) % self.total_pages

        elif key.name == 'right':
            self.current_page = (self.current_page + 1) % self.total_pages

        elif key.name == 'enter':
            self.running = False

    def run(self) -> str:
        self.running = True
        while self.running:
            self.render()
            key = keyboard.read_event()
            if key.event_type != keyboard.KEY_DOWN:
                continue
            self.handle_keys(key)
            time.sleep(0.01)
        return self.current_page_options[self.highlight]

    


def main() -> None:
    menu = PagedMenu([
        Option(f"Option {i}\nFiller text", 10, '>') for i in range(51)
    ], 'Select an option', 10)
    choice = menu.run()
    print(f'You selected: { choice.title }')
    
    
    
if __name__ == "__main__":
    main()
