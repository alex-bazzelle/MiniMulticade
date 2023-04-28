from pygame import *

from .constants import TextConstants


class Text:
    @staticmethod
    def font(size):
        # f = font.SysFont("monospace", int(size))
        f = font.Font(TextConstants.TEXTFONTFILE, int(size))
        # Generate test char
        test = f.render("a", 1, (0, 0, 0))
        # Calc line sizes
        line_width = test.get_width()
        return f, line_width

    @staticmethod
    def wrap(unsafe, length, break_char):
        safe_lines = []

        # While text needs wrapping
        while len(unsafe) > length:

            # Find closest (to left) break_char from index length
            slash_index = unsafe.rfind(break_char, 0, length)

            # If not found, give up, unbreakable
            if slash_index == -1:
                break

            # Save warped text and continue looping
            safe_lines.append(unsafe[0:slash_index].strip())
            unsafe = unsafe[slash_index + 1:].strip()

        safe_lines.append(unsafe)
        return safe_lines

    def get_lines(self, string, break_char, width, scale, color):
        # Font Size
        font_size = TextConstants.TEXTFONTSIZE * scale
        font, line_width = self.font(font_size)

        # Get wrapped text
        if width:
            lines = self.wrap(string, width // line_width, break_char)
        else:
            lines = [string]

        # Render font
        labels = []
        for line in lines:
            render = font.render(line, 1, color)
            labels.append(render)

        return labels

    def get_label(self, string, break_char="", *, width=None, height=None, scale=1, color=(255, 255, 0),
                  background=None):

        # Scaling
        if width:
            width = int(width * (scale ** -1))
        if height:
            height = int(height * (scale ** -1))

        # Get labels
        labels = self.get_lines(string, break_char, width, scale, color)

        # Generate blank surface
        if not width:
            width = max([f.get_width() for f in labels])
        if not height:
            height = sum([f.get_height() + 2 for f in labels])
        surface = Surface((width, height), SRCALPHA, 32)
        surface = surface.convert_alpha()
        if background:
            surface.fill(background)

        # Add lines
        y = 0
        for label in labels:
            surface.blit(label, (0, y))
            y += label.get_height() + 2

        return surface
