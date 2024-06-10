import os
import keyboard
from colorify import ConsoleStencil
from colorama import Fore, Back

# WORK IN PROGRESS
init(autoreset=True)

class Option:
    def __init__(self, title, action) -> None:
        self.title = title
        self.action = action
        
class ConsoleTextViewer:
    def __init__(self, text, menu_options) -> None:
        self.text_lines = text.split('\n')
        self.menu_options = menu_options
        self._setup_menu()
    
    def _setup_menu(self) -> None:
        self.text_index = 0
        self.menu_index = 0
        self.running = True
        self.term_height = os.get_terminal_size().lines
        self.term_width = os.get_terminal_size().columns

    def clear(self) -> None:
        os.system('cls' if os.name == 'nt' else 'clear')

    def show_text(self) -> None:
        max_lines = self.term_height - 3  
        start_line = max(0, self.text_index - (max_lines // 2))
        end_line = min(len(self.text_lines), start_line + max_lines)

        for idx in range(start_line, end_line):
            line = self.text_lines[idx]
            if idx == self.text_index:
                print(f"{Back.WHITE}{Fore.BLACK}>{line}{Style.RESET_ALL}")
            else:
                print(line)

        
        for _ in range(end_line, start_line + max_lines):
            print()

    def show_menu(self) -> None:
        print("\n" + "=" * self.term_width)  # Separator line
        for idx, option in enumerate(self.menu_options):
            if idx == self.menu_index:
                print(f"{ Back.WHITE }{ Fore.BLACK } { option.title } { Style.RESET_ALL }", end="    ")
            else:
                print(f" { option.title } ", end="    ")
        print()

    def run(self):
        self.clear()
        while self.running:
            self.show_text()
            self.show_menu()

            event = keyboard.read_event()
            if event.event_type != keyboard.KEY_DOWN:
                continue
            
            self._handle_keys(event)
            self.clear()

    def _handle_keys(self, key) -> None:
        if key.name == 'up':
            self.text_index = (self.text_index - 1) % len(self.text_lines)

        elif key.name == 'down':
            self.text_index = (self.text_index + 1) % len(self.text_lines)
                    
        elif key.name == 'left':
            self.menu_index = (self.menu_index - 1) % len(self.menu_options)
                    
        elif key.name == 'right':
            self.menu_index = (self.menu_index + 1) % len(self.menu_options)
                    
        elif key.name == 'enter':
            self.menu_options[self.menu_index].action(self)

    def exit(self):
        self.running = False

# test usage
if __name__ == "__main__":
    sample_text = """[ LONG DEMO ]
Lorem ipsum dolor sit amet, consectetur adipiscing elit.
Pellentesque imperdiet libero eu neque facilisis.
Curabitur ac libero non leo pretium dictum.
Praesent vel tortor facilisis, dapibus dui non, lacinia dui.
Sed fringilla, libero at pulvinar dapibus, justo nisl ultricies magna, id tincidunt justo ligula nec velit.
Etiam at urna malesuada, ultricies nisi quis, ullamcorper risus.
Phasellus lacinia magna non ex tincidunt, vel laoreet odio consectetur.
Donec dapibus enim vitae felis suscipit, at bibendum nulla sagittis.
Mauris posuere sem sed urna dignissim, sed scelerisque magna egestas.
Aliquam erat volutpat.
Nunc ullamcorper ipsum a lacus venenatis, nec suscipit ex suscipit.
Sed sit amet felis tincidunt, tincidunt erat et, pretium ligula.
Nam ac eros eget ligula elementum congue non sit amet elit.
In vehicula lorem vel augue fermentum, ac dignissim orci suscipit.
Nulla facilisi.
Vivamus scelerisque, urna eget luctus dignissim, lorem lorem auctor est, sit amet fermentum elit lectus id justo.
Fusce id magna ut sapien condimentum tristique.
Aliquam venenatis magna ut velit efficitur, sed feugiat nunc tempus.
Aenean tincidunt sem sed quam ullamcorper, in maximus magna pulvinar.
Mauris at felis in elit accumsan dignissim.
Suspendisse potenti.
Proin non nulla at lacus ultrices gravida.
Morbi luctus dolor sit amet leo ullamcorper, nec tincidunt sapien pretium.
Praesent auctor ligula eget nulla scelerisque, non posuere risus pulvinar.
Ut eu est nec augue interdum aliquet.
Pellentesque in arcu a nunc pulvinar accumsan vel quis dui.
Aenean quis velit eget elit facilisis feugiat.
Sed sollicitudin erat non erat faucibus, sed ullamcorper erat dignissim.
Etiam ac nunc ut eros fermentum vestibulum.
Morbi dictum, libero et cursus vehicula, velit justo pretium purus, eget malesuada lorem velit eget orci.
Mauris convallis libero et nisl tristique, non scelerisque sapien vehicula.
Duis sollicitudin erat at felis venenatis, sit amet scelerisque lorem gravida.
Donec faucibus sapien at sapien ultrices, nec feugiat nulla pellentesque.
Fusce auctor sapien nec justo facilisis, eget auctor felis fermentum.
Vivamus feugiat leo sed nisi efficitur, non suscipit justo luctus.
Nam a felis eu felis vestibulum venenatis.
Phasellus quis nunc a odio aliquam egestas.
Aenean non elit eget turpis gravida luctus.
Suspendisse finibus purus ut diam tempus, nec volutpat nulla vestibulum.
Vivamus ac arcu ac ligula efficitur ultricies in sed nunc.
Morbi euismod nunc a enim lacinia, non scelerisque dui cursus.
Integer eget quam ac ipsum ultricies vehicula.
Maecenas sagittis augue ac odio scelerisque, in facilisis mauris ultricies.
Praesent fermentum felis et dui ultricies, at feugiat sapien tristique.
Sed ut dolor nec elit varius bibendum.
Nulla vestibulum libero nec turpis accumsan, vel pellentesque magna condimentum.
Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia curae;
Fusce vel mauris pharetra, hendrerit mauris ut, fermentum mi.
Proin vulputate felis in ipsum gravida, a ullamcorper purus cursus.
Donec gravida odio a magna varius, ac porttitor mi pretium.
Suspendisse tempor magna ac nisl laoreet, ut luctus dolor malesuada.
Sed mollis nulla et nisl feugiat, in varius felis lacinia.
Morbi et est a mi tristique pretium.
Nulla eu turpis in felis bibendum viverra et sed erat.
Vestibulum scelerisque arcu nec leo condimentum, sit amet blandit mi pretium.
Fusce tristique massa ac lectus tincidunt, et aliquet massa suscipit.
Curabitur non velit in eros gravida auctor.
Vestibulum at augue in nisl venenatis blandit.
Etiam vulputate erat non eros posuere laoreet.
Sed volutpat metus in nibh interdum varius.
Etiam ultricies magna eget purus varius, vel malesuada magna tempor.
Nulla facilisi.
Praesent nec velit dapibus, posuere velit in, commodo tortor.
Mauris at libero nec quam consectetur fringilla a non dolor.
Nam tincidunt eros eu lacus facilisis, nec placerat ex gravida.
Curabitur sed magna nec nisl egestas ultrices.
Ut condimentum urna non erat iaculis, nec placerat quam tristique.
In hac habitasse platea dictumst.
Curabitur ut mauris nec elit venenatis dapibus non ac arcu.
Praesent tristique magna vel nisi consectetur, ut laoreet quam vehicula.
Nulla facilisi.
Fusce tempus lorem non nibh sagittis, vel faucibus est scelerisque.
Integer quis nulla vel turpis posuere gravida.
Sed a nunc ac purus dapibus faucibus.
In aliquet velit et metus ultricies, sed egestas arcu feugiat.
Integer nec est suscipit, consequat nulla vel, scelerisque odio.
Donec convallis quam eu nulla fringilla, id varius nisi egestas.
Maecenas viverra odio id ex convallis sollicitudin.
In tincidunt libero non tellus elementum, sit amet scelerisque justo hendrerit.
Sed ullamcorper eros sit amet quam posuere aliquet.
Donec ut nisl nec magna bibendum pharetra.
Suspendisse potenti.
Praesent euismod odio id nibh vehicula, vitae facilisis lectus hendrerit.
Nunc vestibulum magna id orci bibendum ultricies.
Nullam venenatis sapien nec ligula condimentum, id ultricies lectus vestibulum.
Morbi feugiat ligula a turpis fermentum, eu fringilla arcu ultrices.
Nam gravida libero nec mi scelerisque viverra.
Suspendisse feugiat ligula sit amet arcu feugiat, nec viverra nulla vehicula.
Aenean tincidunt erat non orci aliquam, sit amet pretium dui vehicula.
Praesent efficitur eros sit amet justo gravida, id tincidunt est aliquet.
Suspendisse suscipit lectus et sapien consectetur, at gravida est vehicula.
Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia curae;
Ut malesuada metus in nisl fermentum fringilla.
Fusce ultricies purus vel ligula dictum tincidunt.
Ut vel elit ut nisi ultricies sodales in id tortor.
Nullam ut lorem at nulla convallis vehicula non vitae tortor.
Integer vel felis sit amet ligula feugiat gravida vel id sem.
Nam eget nisi non tortor tincidunt porttitor.
Donec sagittis eros sit amet lectus dictum, eget maximus justo vestibulum.
Integer convallis elit ac urna tincidunt, et dictum leo facilisis.
Proin tincidunt magna et mi bibendum maximus.
Curabitur tempor ex ac nisl facilisis, a tincidunt lacus vehicula.
Fusce tincidunt nulla eget libero consectetur, ac posuere tortor bibendum.
Praesent laoreet nisi et tortor tristique, non interdum orci gravida.
Phasellus eu justo nec nisi pulvinar auctor sit amet nec elit.
Suspendisse potenti.
Etiam ac nisi in leo congue dictum a in purus.
Nam condimentum risus eget turpis vehicula, sit amet dictum nisi consequat.
Proin sit amet libero consectetur, elementum eros ut, gravida odio.
Vestibulum sagittis lorem in ipsum bibendum, ac iaculis dolor efficitur.
Donec vitae dolor ac sapien aliquam fermentum in ut augue.
Morbi ac erat eget risus tincidunt laoreet nec eget eros.
Nam et quam eu velit vehicula ultricies non non nisi.
Phasellus sit amet quam gravida, sodales erat id, vehicula justo.
In scelerisque purus ut tortor gravida, sed consectetur urna efficitur.
Etiam eget erat at dui aliquam feugiat.
Phasellus at nunc vitae est ultricies pretium.
Suspendisse potenti.
Phasellus et quam vel velit vehicula dapibus.
Aenean nec turpis non ipsum auctor vehicula.
Suspendisse non turpis ut tortor pretium auctor.
Suspendisse faucibus sapien vel orci pharetra fermentum.
Vivamus non nisi ac nulla fermentum dapibus.
Ut aliquam quam eu risus vehicula, a euismod sapien consequat.
Donec euismod dolor at ipsum feugiat tincidunt.
Mauris vel velit in turpis luctus condimentum.
Sed ac nisi nec ipsum luctus egestas at eget mauris.
Aenean faucibus neque vel urna iaculis, sed gravida risus ultrices.
Phasellus in libero id dolor aliquet interdum.
Vivamus scelerisque urna ut orci blandit maximus.
Pellentesque sed neque ut purus blandit finibus.
Nam lacinia tortor ut purus tristique gravida.
Ut sollicitudin eros at nulla iaculis viverra.
Morbi suscipit nunc et sem consequat, et fringilla orci placerat.
Integer condimentum leo vel risus iaculis, a euismod lacus fermentum.
Aliquam suscipit metus non eros sagittis, quis scelerisque metus eleifend.
Etiam vitae magna rutrum, condimentum leo quis, sollicitudin nisi.
Maecenas vestibulum odio vel purus tincidunt laoreet.
Etiam vel libero id urna facilisis bibendum.
Phasellus eget justo facilisis, dapibus justo a, varius metus.
Mauris accumsan eros vel libero elementum, eu condimentum nunc lacinia.
Phasellus sagittis ligula sit amet erat ultricies pharetra.
Etiam eget ex non eros efficitur volutpat.
Mauris eu risus posuere, tempus justo ut, dictum lacus.
Aenean at sem ut libero sagittis egestas.
Nam eget risus et libero dictum luctus a vel elit.
Suspendisse potenti.
Morbi pharetra mauris eu nisl elementum, nec vestibulum quam gravida.
Phasellus id lorem interdum, rhoncus eros vel, blandit mi.
Fusce pellentesque risus eget erat consequat, in dignissim erat feugiat.
Nullam fringilla ligula a magna fringilla, a vestibulum odio ultricies.
Morbi varius risus in ligula vehicula, sit amet tincidunt lacus fermentum.
Pellentesque in mi at magna varius feugiat nec at velit.
Suspendisse vel elit ut nunc scelerisque ullamcorper in eget justo."""

    def copy_action(viewer):
        current_line = viewer.text_lines[viewer.text_index]
        input(f"\nCopied: {current_line}")
        input("Press Enter to continue...")  # Pause to show copied message

    def dummy_action(viewer):
        print("\nDummy action executed.")
        input("Press Enter to continue...")  # Pause to show dummy message

    horizontal_options = [
        Option("Copy", copy_action),
        Option("Option 2", dummy_action),
        Option("Option 3", dummy_action),
        Option("Exit", lambda viewer: viewer.exit())
    ]

    viewer = ConsoleTextViewer(sample_text, horizontal_options)
    viewer.run()
