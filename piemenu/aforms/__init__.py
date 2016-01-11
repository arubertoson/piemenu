#!/user/bin/env python2

""" TODO: package string

"""

import os
import platform

from PySide import QtGui, QtCore

from utils import jsonparser
from utils.pathlib import Path
from utils.bunch import Bunch

__version__ = '0.1'

config = None
menus = None
commands = None
icon = None
font = None


class path:
    """ Application paths. """

    root = Path(__file__).parent
    resources = Path(root, 'resources')

    icons = Path(resources, 'icons')
    fonts = Path(resources, 'fonts')
    styles = Path(resources, 'styles')
    config = Path(resources, 'config.json')
    menus = Path(resources, 'menus.json')
    commands = Path(resources, 'commands.json')


class Fonts:
    """ Font manager. """

    _default_font_family = 'Source Code Pro'

    @staticmethod
    def loadFonts():
        """ Load fonts into script. """
        db = QtGui.QFontDatabase()

        if not path.fonts.exists():
            return

        for name in path.fonts.iterdir():
            if name.suffix not in ['.otf', '.ttf']:
                continue
            try:
                db.addApplicationFont(str(path.fonts.joinpath(name)))
            except Exception as err:
                print('Could not load font: {0}: {1}'.format(name, str(err)))

    @staticmethod
    def fontNames():
        """ Returns a list of available monospace fonts on this system. """
        db = QtGui.QFontDatabase()
        QFont, QFontInfo = QtGui.QFont, QtGui.QFontInfo
        return [fn for fn in db.families() if QFontInfo(QFont(fn)).fixedPitch()]

    @classmethod
    def setDefaultFont(cls, name):
        cls._default_font_family = name

    @classmethod
    def defaultFont(cls):
        """ Return the default font as a QFont object. """
        f = QtGui.QFont(cls._default_font_family)
        f.setStyleHint(f.TypeWriter, f.PreferDefault)
        fi = QtGui.QFontInfo(f)
        family = fi.family()

        size = 9
        if platform.system().lower().startswith('darwin'):
            # Account for Qt font size difference
            size = int(size*1.33333+0.4999)
        return QtGui.QFont(family, size)

    @classmethod
    def get(cls, name):
        """ Returns QFont if name is available in the system, if not
        return default.
        """
        try:
            QtGui.QFontDatabase().families().index(name)
        except IndexError:
            name = cls._default_font_family
            print('{0} does not exists on the system, using default.'.format(name))
        return QtGui.QFont(name)


class Icons(dict):
    """ Icon dict, collects icons from application path. """

    def __init__(self):
        self.load_icons()

    def __getitem__(self, key):
        """ Returns QIcon instead of path value. """
        val = dict.__getitem__(self, key)
        return QtGui.QIcon(val)

    def load_icons(self):
        """ Load all icons from the icon dir. """
        for name in path.icons.iterdir():
            if name.suffix not in ['.png']:
                continue
            try:
                self[name.stem] = str(path.resources.joinpath(name))
            except Exception as err:
                self[name.stem] = QtGui.QPixmap(16, 16)
                self[name.stem].fill(QtGui.QColor(0, 0, 0, 0))
                print('Could not load icon {0}: {1}'.format(name, str(err)))


class Styles(object):

    _default_style = 'qdarkstyle'

    def __init__(self):
        self.compile()

    def update(self):
        self.compile()

    def compile(self):
        """ Compiles all given resources to file. """
        styles = path.styles.joinpath('styles.qrc')
        if styles.exists():
            output = path.root.joinpath('styles_rc.py')
            os.system('pyside-rcc -py2 {0!s} -o {1!s}'.format(styles, output))

        try:
            reload(style_rc)
        except UnboundLocalError:
            import style_rc

    def load(self, stylename=None):
        """ Given stylename loads compiled stylsheet. """
        stylename = stylename or self._default_style
        f = QtCore.QFile(':style/{0}.qss'.format(stylename))
        if not f.exists():
            return ""
        else:
            f.open(f.ReadOnly | f.Text)
            stream = QtCore.QTextStream(f)
            stylesheet = stream.readAll()
            if platform.system().lower() == 'darwin' and stylename == 'qdarkstyle':
                mac_fix = '''
                QDockWidget::title
                {
                    background-color: #353434;
                    text-align: center;
                    height: 12px;
                }
                '''
                stylesheet += mac_fix
            return stylesheet


def init():
    """ Load necessary resouces and inits application. """
    global icon, font, config, menus, commands

    from aforms.core.main import MainWindow

    # Check if Qt app is running or create new one and start app in background.
    # If QApp already exists Qt is handled by another application and does not
    # need a new app object.
    if QtGui.qApp is not None:
        app = QtGui.qApp
    else:
        app = QtGui.QApplication([])
        if not QtGui.QSystemTrayIcon.isSystemTrayAvailable():
            QtGui.QMessageBox.critical(
                None, 'Systray', 'Systray not available on this system')

    # QtGui.QApplication.setQuitOnLastWindowClosed(False)

    # Init settings
    config = jsonparser.parse(path.config)
    menus = jsonparser.parse(path.menus)
    commands = jsonparser.parse(path.commands)

    # Init resources
    icon = Icons()
    font = Fonts()
    style = Styles()

    # Set default font from config
    # TODO: Move.
    font.setDefaultFont(config['main']['font_family'])

    # Create app elements and set stylesheet
    frame = MainWindow(None)
    frame.setStyleSheet(style.load())
    app.exec_()
