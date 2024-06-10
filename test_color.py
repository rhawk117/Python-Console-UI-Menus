from colorify import ConsoleStencil
import unittest
from colorama import Fore, Back, Style, init
init(autoreset=True)


# -color_phrase
# -italicize
# -underline
# -bold
# -highlight_phrase
# -multi_style
# -rainbow
# -stylize
# -bg_colorize
# -colorize
# -ansify


def test_color_phrase():
    print(ConsoleStencil.color_phrase('The word blood is red here because red is blood', 'gay', 'red'))
    print(ConsoleStencil.color_phrase('The word cum is white here because cum is white', 'cum', 'white', is_background=True))

def ansi_methods():
    print(ConsoleStencil.ansify('Hello, World! (bold)', 'bold'))
    print(ConsoleStencil.ansify('Hello, World! (underline)', 'underline'))
    print(ConsoleStencil.ansify('Hello, World! (italic)', 'italic'))
    print(ConsoleStencil.ansify('Hello, World! (normal)', 'normal'))

def color_methods():
    print(ConsoleStencil.colorize('Hello, World! (red)', 'red'))
    print(ConsoleStencil.colorize('Hello, World! (green)', 'green'))
    print(ConsoleStencil.colorize('Hello, World! (blue)', 'blue'))
    print(ConsoleStencil.colorize('Hello, World! (yellow)', 'yellow'))
    print(ConsoleStencil.colorize('Hello, World! (magenta)', 'magenta'))
    print(ConsoleStencil.colorize('Hello, World! (cyan)', 'cyan'),)
    print(ConsoleStencil.colorize('Hello, World! (white)', 'white'))
    print(ConsoleStencil.colorize('Hello, World! (black)', 'black'))
    print(ConsoleStencil.rainbow('Hello, World! (rainbow)'))
    print(ConsoleStencil.bg_colorize('Hello, World! (red bg)', 'red'))

def font_vars():
    print(ConsoleStencil.font_variant('Hello, World! (bright)', 'bright'))
    print(ConsoleStencil.font_variant('Hello, World! (dim)', 'dim'))

def multi_style():
    print(ConsoleStencil.multi_style("Hello, World! (info: fg_color='red', bg_color='blue', ans='bold)', fg_color='red'", bg_color='blue', ansi='bold'))
    print(ConsoleStencil.multi_style("Hello, World! (info: fg_color='green', bg_color='yellow', ansi='unerline)'", fg_color='green', bg_color='yellow', ansi='underline'))
    print(ConsoleStencil.multi_style("Hello, World! (info: fg_color='magenta', bg_color='cyan', ansi=italic)'", fg_color='magenta', bg_color='cyan', ansi='italic'))
    print(ConsoleStencil.multi_style("Hello, World! (info: fg_color='white', bg_color='black', style=bright)'", fg_color='white', bg_color='black', style='bright'))
    
    
def run_test(test_name, method_calls):
    print('Running Test for ' + test_name)
    method_calls()
    input('Press Enter to Continue')
    
    

    
    
if __name__ == '__main__':
    pass
    # run_test('Color Phrase', test_color_phrase)
    # run_test('ANSI Methods', ansi_methods)
    # run_test('Color Methods', color_methods)
    # run_test('Font Variants', font_vars)
    # run_test('Multi Style', multi_style)
    # input()
