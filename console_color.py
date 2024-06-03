from colorama import Fore, Back, Style, init

init(autoreset=True)


class TextStyler:
    VALID_COLORS = ['red', 'green', 'blue', 'yellow',
                    'magenta', 'cyan', 'white', 'black'
                   ]
    VALID_STYLES = ['bright', 'dim', 'normal', 'reset_all']
    VALID_ANSI_STYLES = ['bold', 'underline', 'italic', 'normal']

    @staticmethod
    def _log_error(message: str):
        """Logs error messages without raising exceptions."""
        print(f"WARNING: {message}")

    @staticmethod
    def get_fg_color(color: str):
        """
        Provides a string of a color and returns the corresponding Foreground colorama attribute.
        If the color is invalid, it returns the default color (white) and logs a warning.
        
        Valid Colors:'red', 'green', 'blue', 'yellow',
                     'magenta', 'cyan', 'white', 'black'
        """
        if color.lower() in TextStyler.VALID_COLORS:
            return getattr(Fore, color.upper())
        TextStyler._log_error(f"Invalid foreground color: '{color}'. Using default (white). Valid colors are: {', '.join(TextStyler.VALID_COLORS)}")
        return Fore.WHITE

    @staticmethod
    def get_bg_color(color: str):
        """
        Provides a string of a color and returns the corresponding Background attribute.
        If the color is invalid, it returns the default color (black) and logs a warning.
        """
        if color.lower() in TextStyler.VALID_COLORS:
            return getattr(Back, color.upper())
        TextStyler._log_error(f"Invalid background color: '{
                              color}'. Using default (black). Valid colors are: {', '.join(TextStyler.VALID_COLORS)}")
        return Back.BLACK

    @staticmethod
    def get_style(style: str):
        """
        Provides a string of a style and returns colorama attribute.
        If the style is invalid, it returns the default style (normal) and logs a warning.
        
        Valid Styles: 'bright', 'dim', 'normal', 'reset_all'
        """
        if style.lower() in TextStyler.VALID_STYLES:
            return getattr(Style, style.upper())
        TextStyler._log_error(f"Invalid style: '{style}'. Using default (normal). Valid styles are: {', '.join(TextStyler.VALID_STYLES)}")
        return Style.NORMAL

    @staticmethod
    def get_ansi_style(style: str) -> str:
        """
        Applies ANSI escape codes to text for styling.
        If the style is invalid, it returns an empty string and logs a warning.
        """
        ansi_codes = {
            'bold': '\033[1m',
            'underline': '\033[4m',
            'italic': '\033[3m',
            'normal': '\033[0m'
        }
        style = style.lower()
        if style not in TextStyler.VALID_ANSI_STYLES:
            TextStyler._log_error(f"Invalid ANSI style: '{style}'. No style applied. Valid styles are: {', '.join(TextStyler.VALID_ANSI_STYLES)}")
        return ansi_codes.get(style, '')

    @staticmethod
    def multi_style_text(text: str, **kwargs) -> str:
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
            if key == 'fg_color':
                styled_text = f"{TextStyler.get_fg_color(value)}{styled_text}"
                
            elif key == 'bg_color':
                styled_text = f"{TextStyler.get_bg_color(value)}{styled_text}"
                
            elif key == 'ansi':
                styled_text = TextStyler.get_ansi_style(value) + styled_text
                
            elif key == 'style':
                styled_text = f"{TextStyler.get_style(value)}{styled_text}"
                
        return styled_text + Style.RESET_ALL
    

    @staticmethod
    def highlight_phrase(text, phrase, style):
        """
        Highlight all occurrences of 'phrase' in 'text' with the specified ANSI style.

        Args:
            text (str): The full text in which to highlight the phrase.
            phrase (str): The phrase within the text to highlight.
            style (str): The ANSI style to apply ('bold', 'underline', 'italic').

        Returns:
            str: The text with the phrase highlighted.
        """
        ansi_style = TextStyler.get_ansi_style(style)
        reset_style = '\033[0m'
        highlighted_text = text.replace(phrase, f"{ansi_style}{phrase}{reset_style}")
        return highlighted_text
    
    @staticmethod
    def bold_text(text: str) -> str:
        return TextStyler.multi_style_text(text, style='bold')
    
    
    
    

    @staticmethod
    def color_phrase(text: str, phrase: str, color: str, is_back=False) -> str:
        '''
        Colors either the foreground or background of a specific phrase within the string. 
        Args:
            text (str): The full text that features the phrase.
            phrase (str): The phrase within the text to colorize.
            color (str): The color to apply to the phrase.
            is_back (bool): If True, the background color will be applied.
        Returns:
            str: The text with the phrase colorized.
        '''
        if phrase not in text:
            return text
        color_method = TextStyler.get_fg_color if not is_back else TextStyler.get_bg_color
        color_code = color_method(color)
        return text.replace(phrase, f'{color_code}{phrase}{Style.RESET_ALL}')
    
    

    
