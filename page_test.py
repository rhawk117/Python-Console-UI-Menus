import os
import keyboard
import time


def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')


class PagedMenu:
    PREV_PAGE = "[ ← Previous Page ]"
    NEXT_PAGE = "[ Next Page → ]"
    NAV_GUIDE = "[ i ] Move ↑/↓  | Page ←/→ | Select Enter  [ i ]"
    
    def __init__(self, options: list[str], prompt: str, page_size: int = 3):
        if page_size <= 0:
            raise ValueError("Page size must be greater than zero.")
        self.options: list[str] = options
        self.page_size: int = page_size
        self.total_pages: int = (len(options) + page_size - 1) // page_size
        self.current_page: int = 1
        self.highlight_index: int = 0
        self.running: bool = False
        self.prompt: str = prompt

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
        self.highlight_index = 0 

    @property
    def current_page_options(self) -> list[str]:
        '''
            Refreshes the items on each page 
        '''
        start = (self.current_page - 1) * self.page_size
        end = start + self.page_size
        self.options.append(self.PREV_PAGE)
        self.options.append(self.NEXT_PAGE)
        return self.options[start : end]

    def display(self) -> None:
        '''
            Displays the UI in the Console highlighting the currently selected option
        '''
        clear_screen()
        print(self.NAV_GUIDE)
        print(f"\n{ self.prompt } - [ Page { self.current_page } / { self.total_pages } ]")
        for idx, option in enumerate(self.current_page_options):
            prefix = "\033[1;36;44m> " if idx == self.highlight_index else "  "
            suffix = " <\033[0m" if idx == self.highlight_index else ""
            print(f"{prefix}{option}{suffix}")


    def next_page(self) -> None:
        self.current_page += 1  
        self.display()

    def prev_page(self) -> None:
        self.current_page -= 1  
        self.display()

    def select_option(self) -> None:
        if self.current_page_options[self.highlight_index] == self.PREV_PAGE:
            self.prev_page()

        elif self.current_page_options[self.highlight_index] == self.NEXT_PAGE:
            self.next_page()

        else:
            self.exit_ui()
        

    def exit_ui(self):
        self.running = False

    def handle_keys(self, key : keyboard.KeyboardEvent) -> None:
        if key.name == 'up':
            self.highlight_index = (self.highlight_index - 1) % len(self.current_page_options)

        elif key.name == 'down':
            self.highlight_index = (self.highlight_index + 1) % len(self.current_page_options)

        elif key.name == 'left':
            self.prev_page()

        elif key.name == 'right':
            self.next_page()

        elif key.name == 'enter':
            self.select_option()

        
    def run(self) -> str:
        self.running = True
        while self.running:
            self.display()
            key = keyboard.read_event()
            if key.event_type != keyboard.KEY_DOWN:
                continue
            self.handle_keys(key)
            time.sleep(0.01)
        return self.current_page_options[self.highlight_index]


# Example usage:
options = [f"Option {i}" for i in range(1, 12)]
menu = PagedMenu(options, 'Testing', page_size=3)
choice = menu.run()
print(f"Selected: {choice}")