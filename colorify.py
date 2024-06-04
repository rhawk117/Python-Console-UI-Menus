from colorama import Fore, Back, Style, init

init(autoreset=True)

class ConsoleStencil:
    VALID_COLORS: set[str] = {
        'red', 'green', 'blue', 'yellow', 'magenta', 'cyan', 'white', 'black'
    }
    VALID_STYLES: set[str] = {'bright', 'dim', 'normal', 'reset_all'}

    VALID_ANSI_STYLES: set[str] = {'bold', 'underline', 'italic', 'normal'}

    COLOR_MAP: dict[str, str] = {
        color: getattr(Fore, color.upper()) for color in VALID_COLORS
    }
    BACKGROUND_MAP: dict[str, str] = {
        color: getattr(Back, color.upper()) for color in VALID_COLORS
    }
    STYLE_MAP: dict[str, str] = {
        style: getattr(Style, style.upper()) for style in VALID_STYLES
    }
    ANSI_STYLE_MAP: dict[str, str] = {
        'bold': '\033[1m',
        'underline': '\033[4m',
        'italic': '\033[3m',
        'normal': '\033[0m'
    }

    @staticmethod
    def _log_error(message: str) -> None:
        print(f"[ ! ] WARNING: { message } [ ! ]")

    @staticmethod
    def ansify(text: str, ansi: str) -> str:
        """
        Apply an ANSI style to the text. 
        Accepts 'bold', 'underline', 'italic', 'normal' as valid styles.
        
        Args:
            text (str): _description_
            ansi (str): _description_

        Returns:
            str: _description_
        """
        ansi = ansi.lower()
        if not ansi.lower() in ConsoleStencil.VALID_ANSI_STYLES:
            return text
        return f"{ ConsoleStencil.ANSI_STYLE_MAP[ansi] } { text } { ConsoleStencil.ANSI_STYLE_MAP['normal'] }"
    
    @staticmethod
    def colorize(text: str, color: str) -> str:
        """
        Applies color to the text itself.
        
        Accepts 'red', 'green', 'blue', 'yellow', 'magenta', 'cyan', 
        'white', 'black' as valid colors.

        Args:
            text (str): text to colorize
            color (str): color to apply

        """
        color = color.lower()
        if not color in ConsoleStencil.VALID_COLORS:
            return text
        return f"{ ConsoleStencil.COLOR_MAP[color] } { text } { Style.RESET_ALL }" 
    
    def bg_colorize(text: str, color: str) -> str:
        """
        Applies color to the background of the text

        Accepts 'red', 'green', 'blue', 'yellow', 'magenta', 'cyan',
        'white', 'black' as valid colors.

        Args:
            text (str): text to colorize
            color (str): color to apply
        """
        color = color.lower()
        if not color in ConsoleStencil.VALID_COLORS:
            return text
        return f"{ ConsoleStencil.BACKGROUND_MAP[color] } { text } { Style.RESET_ALL }"

    @staticmethod
    def font_variant(text: str, style: str) -> str:
        """
        Apply a colorama style to the entire text.
        
        Args:
            text (str): The text to style.
            style (str): The style to apply ('bright', 'dim', 'normal', 'reset_all').
        
        Returns:
            str: The styled text.
        """
        style = style.lower()
        if not style in ConsoleStencil.VALID_STYLES:
            return text

        return f"{ConsoleStencil.STYLE_MAP[style]}{text}{Style.RESET_ALL}"

    @staticmethod
    def rainbow(text: str) -> str:
        """
            Apply a different color to each character in the text, cycling through available colors.

            Args:
                text (str): The text to colorize.

            Returns:
                str: The rainbow-colored text.
        """
        colors = list(ConsoleStencil.VALID_COLORS)
        colored_chars = [ConsoleStencil.colorize(char, colors[i % len(colors)]) for i, char in enumerate(text)]
        return ''.join(colored_chars)

    @staticmethod
    def multi_style(text: str, **kwargs) -> str:
        """
        Apply styles to text using keyword arguments for maximum flexibility.

        Keyword Args:
            text (str): The text to style.
            ansi (str, optional): The text style such as 'bold', 'underline', etc.
            fg_color (str, optional): The foreground color.
            bg_color (str, optional): The background color.
            style (str, optional): The colorama style such as 'bright', 'dim', etc.
        Returns:
            str: The stylized text.
        """
        styled_text = text
        for key, value in kwargs.items():
            value = value.lower()
            if key == 'fg_color' and value in ConsoleStencil.VALID_COLORS:
                styled_text = f"{ ConsoleStencil.COLOR_MAP[value] } { styled_text }"
                
            elif key == 'bg_color' and value in ConsoleStencil.VALID_COLORS:
                styled_text = f"{ ConsoleStencil.BACKGROUND_MAP[value] } { styled_text }"
                
            elif key == 'ansi' and value in ConsoleStencil.VALID_ANSI_STYLES:
                styled_text = f"{ ConsoleStencil.ANSI_STYLE_MAP[value] } { styled_text } { ConsoleStencil.ANSI_STYLE_MAP['normal'] }"
                
            elif key == 'style' and value in ConsoleStencil.VALID_STYLES:
                styled_text = f"{ ConsoleStencil.STYLE_MAP[value] } { styled_text }"
                
            else:
                ConsoleStencil._log_error(f"Invalid { key }: '{ value }'. This style will be ignored.")
                
        return f'{ styled_text } { Style.RESET_ALL }'

    @staticmethod
    def highlight_phrase(text: str, phrase: str, ansi: str) -> str:
        """
        Highlight all occurrences of 'phrase' in 'text' with the specified ANSI style.

        Args:
            text (str): The full text in which to highlight the phrase.
            phrase (str): The phrase within the text to highlight.
            style (str): The ANSI style to apply ('bold', 'underline', 'italic').

        Returns:
            str: The text with the phrase highlighted.
        """
        if not phrase in text:
            return text
        
        if not ansi in ConsoleStencil.VALID_ANSI_STYLES:
            ConsoleStencil._log_error(f"Invalid ANSI style: '{ ansi }'. No style applied.")
            return text
        
        ansi = ansi.lower()
        ansi_style = ConsoleStencil.ANSI_STYLE_MAP[ansi]
        return text.replace(phrase, 
                f"{ ansi_style }{ phrase }{ ConsoleStencil.ANSI_STYLE_MAP['normal'] }"
        )

    @staticmethod
    def bold(text: str) -> str:
        """
        Returns a bolded version of a string passed.
        
        Args:
            text (str): The text to bold.
        """
        return ConsoleStencil.ansify(text, style='bold')

    @staticmethod
    def underline(text: str) -> str:
        """
        Returns an underlined version of string passed.
        
        Args:
            text (str): The text to underline.
        """
        return ConsoleStencil.ansify(text, ansi='underline')

    @staticmethod
    def italicize(text: str) -> str:
        """
        Returns an italicized version of string passed.
        
        Args:
            text (str): The text to italicize.
        """
        return ConsoleStencil.ansify(text, ansi='italic')

    @staticmethod
    def color_phrase(text: str, phrase: str, color: str, is_background: bool = False) -> str:
        """
            Colors either the foreground or background of a specific phrase within the string. 
            Is Case Sensitive.
            
            Args:
                text (str): The full text that features the phrase.
                phrase (str): The phrase within the text to colorize.
                color (str): The color to apply to the phrase.
                is_background (bool): If True, the color is applied to the background.
            
            Returns:
                str: The text with the phrase colorized.
        """
        if not phrase in text or not color in ConsoleStencil.VALID_COLORS:
            return text
    
        color = color.lower()
        color_map = ConsoleStencil.BACKGROUND_MAP if is_background else ConsoleStencil.COLOR_MAP
        color_code = color_map[color]
        return text.replace(phrase, f'{ color_code }{ phrase }{ Style.RESET_ALL }')

        
    
def main():
    pass
    

if __name__ == '__main__':
    main()


