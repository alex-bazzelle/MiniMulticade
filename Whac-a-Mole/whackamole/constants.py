""" Search for '# !!' to find the most common constant to change """


class GameConstants:
    GAMEWIDTH = 1024
    GAMEHEIGHT = 600
    GAMEMAXFPS = 60


class LevelConstants:
    LEVELGAP = 10  # score
    LEVELMOLESPEED = 5  # % faster
    LEVELMOLECHANCE = 10  # % less


class HoleConstants:
    HOLEWIDTH = 100
    HOLEHEIGHT = int(HOLEWIDTH * (3 / 8))
    HOLEROWS = 5  # !!
    HOLECOLUMNS = 5  # !!

    # Checks
    if HOLEHEIGHT * HOLEROWS > GameConstants.GAMEHEIGHT:
        raise ValueError("HOLEROWS or HOLEHEIGHT too high (or GAMEHEIGHT too small)")
    if HOLEWIDTH * HOLECOLUMNS > GameConstants.GAMEWIDTH:
        raise ValueError("HOLECOLUMNS or HOLEWIDTH too high (or GAMEWIDTH too small)")


class MoleConstants:

    MOLEWIDTH = int(HoleConstants.HOLEWIDTH * (2 / 3))
    MOLEHEIGHT = int(MOLEWIDTH)
    MOLEDEPTH = 15  # % of height
    MOLECOOLDOWN = 1000  # ms

    MOLESTUNNED = 1000  # ms
    MOLEHITHUD = 500  # ms
    MOLEMISSHUD = 250  # ms

    MOLECHANCE = 1 / 30
    MOLECOUNT = 12  # !!
    MOLEUPMIN = 0.3  # s
    MOLEUPMAX = 2  # s

    # Checks
    if MOLECOUNT > HoleConstants.HOLEROWS * HoleConstants.HOLECOLUMNS:
        raise ValueError("MOLECOUNT too high")


class TextConstants:
    TEXTTITLE = "Whack a Mole"
    TEXTFONTSIZE = 15
    TEXTFONTFILE = "assets/font.ttf"


class ImageConstants:
    IMAGEBASE = "assets/"
    IMAGEBACKGROUND = IMAGEBASE + "background.png"
    IMAGEMOLENORMAL = IMAGEBASE + "mole.png"
    IMAGEMOLEHIT = IMAGEBASE + "mole_hit.png"
    IMAGEHOLE = IMAGEBASE + "hole.png"
    IMAGEMALLET = IMAGEBASE + "mallet.png"


class MalletConstants:
    MALLETWIDTH = int(HoleConstants.HOLEWIDTH)
    MALLETHEIGHT = int(MALLETWIDTH)
    MALLETROTNORM = 15
    MALLETROTHIT = 30


class Constants(GameConstants, LevelConstants, HoleConstants, MoleConstants, TextConstants, ImageConstants,
                MalletConstants):
    DEBUGMODE = False
    LEFTMOUSEBUTTON = 1
