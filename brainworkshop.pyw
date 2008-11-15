#!/usr/bin/env python
#------------------------------------------------------------------------------
# Brain Workshop: a Dual N-Back game in Python
#
# Tutorial, installation instructions & links to the dual n-back community
# are available at the Brain Workshop web site:
#
#       http://brainworkshop.sourceforge.net/
#
# Also see Readme.txt.
#
# Copyright (C) 2008: Paul Hoskinson (plhosk@gmail.com)
#
# License: GPL (http://www.gnu.org/copyleft/gpl.html)
#------------------------------------------------------------------------------

VERSION = '4.23'

import random, os, sys, imp, socket, urllib2, webbrowser, time, math, ConfigParser
from decimal import Decimal
from time import strftime
from datetime import date

# Internal static options not available in config file.
NOVBO = True
FOLDER_RES = 'res'
FOLDER_DATA = 'data'
CONFIGFILE = 'config.ini'
CHARTFILE = ['chart-02-dnb.txt', 'chart-03-tnb.txt', 'chart-04-dlnb.txt', 'chart-05-tlnb.txt',
             'chart-06-qlnb.txt','chart-07-anb.txt', 'chart-08-danb.txt', 'chart-09-tanb.txt',
             'chart-10-ponb.txt', 'chart-11-aunb.txt',]
             #'chart12-dvnb.txt', 'chart13-mnb.txt', 'chart14-dmnb.txt', 'chart15-tmnb.txt', 'chart16-qmnb.txt']
ARITHMETIC_ACCEPTABLE_DECIMALS = ['0.1', '0.2', '0.3', '0.4', '0.5', '0.6', '0.7', '0.8', '0.9',
                       '0.125', '0.25', '0.375', '0.625', '0.75', '0.875',
                       '0.15', '0.35', '0.45', '0.55', '0.65', '0.85', '0.95',]
ATTEMPT_TO_SAVE_STATS = True
STATS_SEPARATOR = ','
WEB_SITE = 'http://brainworkshop.sourceforge.net/'
WEB_TUTORIAL = 'http://brainworkshop.sourceforge.net/#tutorial'
WEB_VERSION_CHECK = 'http://brainworkshop.sourceforge.net/version.txt'
WEB_PYGLET_DOWNLOAD = 'http://pyglet.org/download.html'
WEB_FORUM = 'http://groups.google.com/group/brain-training'
WEB_MORSE = 'http://en.wikipedia.org/wiki/Morse_code'
TIMEOUT_SILENT = 3
TICKS_MIN = 4
TICKS_MAX = 20
TICK_DURATION = 0.25
                                           
# some functions to assist in path determination
def main_is_frozen():
    return (hasattr(sys, "frozen") or # new py2exe
        hasattr(sys, "importers") # old py2exe
        or imp.is_frozen("__main__")) # tools/freeze
def get_main_dir():
    if main_is_frozen():
        return os.path.dirname(sys.executable)
    return sys.path[0]    

CONFIGFILE_DEFAULT_CONTENTS = """
######################################################################
# Brain Workshop configuration file
# 
# To change configuration options:
#   1. Edit this file as desired,
#   2. Save the file,
#   3. Launch Brain Workshop to see the changes.
#
# Every line beginning with # is ignored by the program.
#
# Please see the Brain Workshop web site for more information:
#       http://brainworkshop.sourceforge.net
#
# The configuration options begin below.
######################################################################
[DEFAULT]

# Novice mode?
# This mode emulates the original study protocol.
# It counts non-matches with no inputs as correct (instead of ignoring them).
# It also forces 6 visual and 6 position matches, significantly reducing
# the difficulty & complexity of the n-back task.
# Different thresholds are used to reflect the modified scoring system.
# Only Dual N-Back is available in Novice Mode - the others are disabled.
# Default: False
NOVICE_MODE = False

# This selects which sounds to use for audio n-back tasks.
# Select any combination of letters, numbers, the NATO Phonetic Alphabet
# (Alpha, Bravo, Charlie, etc), the C scale on piano, and morse code.
USE_LETTERS = True
USE_NUMBERS = False
USE_NATO = False
USE_PIANO = False
USE_MORSE = False

# Background color: True = black, False = white.
# Default: False
BLACK_BACKGROUND = False

# Begin in full screen mode?
# Setting this to False will begin in windowed mode.
# Default: False
WINDOW_FULLSCREEN = False

# Window size in windowed mode.
# Minimum values: width = 800, height = 600
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600

# Display feedback of correct/incorrect input?
# Default: True
SHOW_FEEDBACK = True

# Hide text during game? (this can be toggled in-game by pressing F8)
# Default: False
HIDE_TEXT = False

# Set the color of the square in Dual N-Back mode.
# This also affects Dual Combination N-Back and Arithmetic N-Back.
# 1 = red, 2 = white/black, 3 = blue, 4 = yellow,
# 5 = magenta, 6 = cyan, 7 = green, 8 = grey
# Default: 3
VISUAL_COLOR = 3

# Animate squares in Dual/Triple N-Back mode?
ANIMATE_SQUARES = True

# Use the flat, single-color squares like in versions prior to 4.1?
OLD_STYLE_SQUARES = False

# Start in Manual mode?
# If this is False, the game will start in standard mode.
# Default: False
MANUAL = False
USE_MUSIC_MANUAL = False

# Starting game mode.
# Possible values:
# 2: Dual N-back (position & audio)
# 3: Triple N-back (position, color & audio)
# 4: Dual Combination N-Back (visual letter, audio)
# 5: Triple Combination N-Back (position, visual letter, audio)
# 6: Quadruple Combination N-Back (position, color, visual letter, audio)
# 7: Arithmetic N-Back
# 8: Dual Arithmetic N-Back
# 9: Triple Arithmetic N-Back
# 10: Position N-Back
# 11: Audio N-Back
# Note: if NOVICE_MODE is True, only Dual N-Back will be available.
# Default: 2
GAME_MODE = 2

# Default starting n-back levels.
# must be greater than or equal to 1.
# Look above to find the corresponding mode number.
BACK_2 = 2
BACK_3 = 2
BACK_4 = 1
BACK_5 = 1
BACK_6 = 1
BACK_7 = 1
BACK_8 = 1
BACK_9 = 1
BACK_10 = 2
BACK_11 = 2

# Use Variable N-Back by default?
# 0 = static n-back (default)
# 1 = variable n-back
VARIABLE_NBACK = 0

# Number of quarter-seconds per trial.
# Must be greater than or equal to 4 (ie, 1 second)
# Look above to find the corresponding mode number.
# Default: 12 (18 for the Arithmetic modes)
TICKS_2 = 12
TICKS_3 = 12
TICKS_4 = 12
TICKS_5 = 12
TICKS_6 = 12
TICKS_7 = 18
TICKS_8 = 18
TICKS_9 = 18
TICKS_10 = 12
TICKS_11 = 12

# Default number of trials per session.
# Must be greater than or equal to 1.
# Default: 20
NUM_TRIALS = 20

# Thresholds for n-back level advancing & fallback.
# Values are 0-100.
# Set THRESHOLD_ADVANCE to 101 to disable automatic level advance.
# Set THRESHOLD_FALLBACK to 0 to disable fallback.
# FALLBACK_SESSIONS controls the number of sessions below
#    the fallback threshold that will trigger a level decrease.
# Note: in Novice mode, only NOVICE_ADVANCE and NOVICE_FALLBACK
#    are used.
# Defaults: 80, 50, 3, 90, 75
THRESHOLD_ADVANCE = 80
THRESHOLD_FALLBACK = 50
THRESHOLD_FALLBACK_SESSIONS = 3
NOVICE_ADVANCE = 90
NOVICE_FALLBACK = 75

# Music/SFX options.
# Volumes are from 0.0 (silent) to 1.0 (full)
# Defaults: True, True, False, 1.0, 1.0
USE_MUSIC = True
USE_APPLAUSE = True
MUSIC_VOLUME = 1.0
SFX_VOLUME = 1.0

# Specify an alternate stats file.
# Default: stats.txt
STATSFILE = stats.txt

# Version check on startup (http protocol)?
# Default: True
VERSION_CHECK_ON_STARTUP = True

# The chance that a match will be generated by force, in addition to the
# inherent 1/8 chance. Setting this to 1 will guarantee at least one match
# each trial (and will cause some repetitive sequences to be generated).
# The value must be a decimal from 0 to 1
# Increasing this value will make the n-back task significantly easier.
# Note: this option has no effect in Novice mode.
# Default: 0.25
CHANCE_OF_GUARANTEED_MATCH = 0.25

# Arithmetic mode settings.
ARITHMETIC_MAX_NUMBER = 12
ARITHMETIC_USE_NEGATIVES = False
ARITHMETIC_USE_ADDITION = True
ARITHMETIC_USE_SUBTRACTION = True
ARITHMETIC_USE_MULTIPLICATION = True
ARITHMETIC_USE_DIVISION = True

# Colors for the color n-back task
# format: (red, green, blue, 255)
# Note: Changing these colors will have no effect in Dual or
#   Triple N-Back unless OLD_STYLE_SQUARES is set to True. 
# the _BLK colors are used when BLACK_BACKGROUND is set to True.
COLOR_1 = (255, 0, 0, 255)
COLOR_2 = (48, 48, 48, 255)
COLOR_2_BLK = (255, 255, 255, 255)
COLOR_3 = (0, 0, 255, 255)
COLOR_4 = (255, 255, 0, 255)
COLOR_5 = (255, 0, 255, 255)
COLOR_6 = (0, 255, 255, 255)
COLOR_7 = (0, 255, 0, 255)
COLOR_8 = (208, 208, 208, 255)
COLOR_8_BLK = (64, 64, 64, 255)

# text color
COLOR_TEXT = (0, 0, 0, 255)
COLOR_TEXT_BLK = (240, 240, 240, 255)

# input label color
COLOR_LABEL_CORRECT = (64, 255, 64, 255)
COLOR_LABEL_OOPS = (64, 64, 255, 255)
COLOR_LABEL_INCORRECT = (255, 64, 64, 255)

######################################################################
# Keyboard definitions.
# The following keys cannot be used: ESC, X, P, F8, F10.
# Look up the key codes here:
# http://pyglet.org/doc/api/pyglet.window.key-module.html
######################################################################

# These are used in Dual N-Back, the default game mode.
# Position match. Default: 97 (A)
KEY_POSITION = 97
# Audio match. Default: 108 (L)
KEY_AUDIO = 108

# This is used in Triple N-Back.
# Color match. Default: 102 (F)
KEY_COLOR = 102

# These are used in the Combination N-Back modes.
# Visual & n-visual match. Default: 115 (S)
KEY_VISVIS = 115
# Visual & n-audio match. Default: 100 (D)
KEY_VISAUDIO = 100
# Audio & n-visual match. Default: 106 (J)
KEY_AUDIOVIS = 106

######################################################################
# This is the end of the configuration file.
######################################################################
"""

def dump_pyglet_info():
    from pyglet import info
    sys.stdout = open(os.path.join(get_main_dir(), FOLDER_DATA, 'dump.txt'), 'w')
    info.dump()
    sys.stdout.close()
    window.on_close()

# parse config file & command line options
try:
    sys.argv[sys.argv.index('--dump')]
    dump_pyglet_info()
except:
    pass
try: CONFIGFILE = sys.argv[sys.argv.index('--configfile') + 1]
except:
    pass

if not os.path.isfile(os.path.join(get_main_dir(), FOLDER_DATA, CONFIGFILE)):
    newconfigfile = open(os.path.join(os.path.join(get_main_dir(), FOLDER_DATA, CONFIGFILE)), 'w')
    newconfigfile.write(CONFIGFILE_DEFAULT_CONTENTS)
    newconfigfile.close()
    
try:
    config = ConfigParser.ConfigParser()
    config.read(os.path.join(get_main_dir(), FOLDER_DATA, CONFIGFILE))
except:
    if CONFIGFILE != 'config.ini':
        str_list = []
        str_list.append('\nUnable to load config file:\n')
        str_list.append(os.path.join(get_main_dir(), FOLDER_DATA, CONFIGFILE))
        str_list.append('\nFull text of error:\n')
        str_list.append(str(sys.exc_info()))
        print >> sys.stderr, ''.join(str_list)
        sys.exit(1)

try: NOVICE_MODE = config.getboolean('DEFAULT', 'NOVICE_MODE')
except: NOVICE_MODE = False
try: USE_LETTERS = config.getboolean('DEFAULT', 'USE_LETTERS')
except: USE_LETTERS = True
try: USE_NUMBERS = config.getboolean('DEFAULT', 'USE_NUMBERS')
except: USE_NUMBERS = False
try: USE_NATO = config.getboolean('DEFAULT', 'USE_NATO')
except: USE_NATO = False
try: USE_PIANO = config.getboolean('DEFAULT', 'USE_PIANO')
except: USE_PIANO = False
try: USE_MORSE = config.getboolean('DEFAULT', 'USE_MORSE')
except: USE_MORSE = False
try: BLACK_BACKGROUND = config.getboolean('DEFAULT', 'BLACK_BACKGROUND')
except: BLACK_BACKGROUND = False
try: WINDOW_FULLSCREEN = config.getboolean('DEFAULT', 'WINDOW_FULLSCREEN')
except: WINDOW_FULLSCREEN = False
try: WINDOW_WIDTH = config.getint('DEFAULT', 'WINDOW_WIDTH')
except: WINDOW_WIDTH = 800
try: WINDOW_HEIGHT = config.getint('DEFAULT', 'WINDOW_HEIGHT')
except: WINDOW_HEIGHT = 600
try: SHOW_FEEDBACK = config.getboolean('DEFAULT', 'SHOW_FEEDBACK')
except: SHOW_FEEDBACK = True
try: HIDE_TEXT = config.getboolean('DEFAULT', 'HIDE_TEXT')
except: HIDE_TEXT = False
try: VISUAL_COLOR = config.getint('DEFAULT', 'VISUAL_COLOR')
except: VISUAL_COLOR = 3
try: ANIMATE_SQUARES = config.getboolean('DEFAULT', 'ANIMATE_SQUARES')
except: ANIMATE_SQUARES = True
try: OLD_STYLE_SQUARES = config.getboolean('DEFAULT', 'OLD_STYLE_SQUARES')
except: OLD_STYLE_SQUARES = False
try: MANUAL = config.getboolean('DEFAULT', 'MANUAL')
except: MANUAL = False
try: USE_MUSIC_MANUAL = config.getboolean('DEFAULT', 'USE_MUSIC_MANUAL')
except: USE_MUSIC_MANUAL = False
try: GAME_MODE = config.getint('DEFAULT', 'GAME_MODE')
except: GAME_MODE = 2

try: BACK_2 = config.getint('DEFAULT', 'BACK_2')
except: BACK_2 = 2
try: BACK_3 = config.getint('DEFAULT', 'BACK_3')
except: BACK_3 = 2
try: BACK_4 = config.getint('DEFAULT', 'BACK_4')
except: BACK_4 = 1
try: BACK_5 = config.getint('DEFAULT', 'BACK_5')
except: BACK_5 = 1
try: BACK_6 = config.getint('DEFAULT', 'BACK_6')
except: BACK_6 = 1
try: BACK_7 = config.getint('DEFAULT', 'BACK_7')
except: BACK_7 = 1
try: BACK_8 = config.getint('DEFAULT', 'BACK_8')
except: BACK_8 = 1
try: BACK_9 = config.getint('DEFAULT', 'BACK_9')
except: BACK_9 = 1
try: BACK_10 = config.getint('DEFAULT', 'BACK_10')
except: BACK_10 = 2
try: BACK_11 = config.getint('DEFAULT', 'BACK_11')
except: BACK_11 = 2

try: VARIABLE_NBACK = config.getint('DEFAULT', 'VARIABLE_NBACK')
except: VARIABLE_NBACK = 0

try: TICKS_2 = config.getint('DEFAULT', 'TICKS_2')
except: TICKS_2 = 12
try: TICKS_3 = config.getint('DEFAULT', 'TICKS_3')
except: TICKS_3 = 12
try: TICKS_4 = config.getint('DEFAULT', 'TICKS_4')
except: TICKS_4 = 12
try: TICKS_5 = config.getint('DEFAULT', 'TICKS_5')
except: TICKS_5 = 12
try: TICKS_6 = config.getint('DEFAULT', 'TICKS_6')
except: TICKS_6 = 12
try: TICKS_7 = config.getint('DEFAULT', 'TICKS_7')
except: TICKS_7 = 18
try: TICKS_8 = config.getint('DEFAULT', 'TICKS_8')
except: TICKS_8 = 18
try: TICKS_9 = config.getint('DEFAULT', 'TICKS_9')
except: TICKS_9 = 18
try: TICKS_10 = config.getint('DEFAULT', 'TICKS_10')
except: TICKS_10 = 12
try: TICKS_11 = config.getint('DEFAULT', 'TICKS_11')
except: TICKS_11 = 12

try: NUM_TRIALS = config.getint('DEFAULT', 'NUM_TRIALS')
except: NUM_TRIALS = 20
try: THRESHOLD_ADVANCE = config.getint('DEFAULT', 'THRESHOLD_ADVANCE')
except: THRESHOLD_ADVANCE = 80
try: THRESHOLD_FALLBACK = config.getint('DEFAULT', 'THRESHOLD_FALLBACK')
except: THRESHOLD_FALLBACK = 50
try: THRESHOLD_FALLBACK_SESSIONS = config.getint('DEFAULT', 'THRESHOLD_FALLBACK_SESSIONS')
except: THRESHOLD_FALLBACK_SESSIONS = 3
try: NOVICE_ADVANCE = config.getint('DEFAULT', 'NOVICE_ADVANCE')
except: NOVICE_ADVANCE = 90
try: NOVICE_FALLBACK = config.getint('DEFAULT', 'NOVICE_FALLBACK')
except: NOVICE_FALLBACK = 75
try: USE_MUSIC = config.getboolean('DEFAULT', 'USE_MUSIC')
except: USE_MUSIC = True
try: USE_APPLAUSE = config.getboolean('DEFAULT', 'USE_APPLAUSE')
except: USE_APPLAUSE = True
try: MUSIC_VOLUME = config.getfloat('DEFAULT', 'MUSIC_VOLUME')
except: MUSIC_VOLUME = 1.0
try: SFX_VOLUME = config.getfloat('DEFAULT', 'SFX_VOLUME')
except: SFX_VOLUME = 1.0
try: STATSFILE = config.get('DEFAULT', 'STATSFILE')
except: STATSFILE = 'stats.txt'
try: STATSFILE = sys.argv[sys.argv.index('--statsfile') + 1]
except: pass
try: VERSION_CHECK_ON_STARTUP = config.getboolean('DEFAULT', 'VERSION_CHECK_ON_STARTUP')
except: VERSION_CHECK_ON_STARTUP = True
try: CHANCE_OF_GUARANTEED_MATCH = config.getfloat('DEFAULT', 'CHANCE_OF_GUARANTEED_MATCH')
except: CHANCE_OF_GUARANTEED_MATCH = 0.25

try: ARITHMETIC_MAX_NUMBER = config.getint('DEFAULT', 'ARITHMETIC_MAX_NUMBER')
except: ARITHMETIC_MAX_NUMBER = 12
try: ARITHMETIC_USE_NEGATIVES = config.getboolean('DEFAULT', 'ARITHMETIC_USE_NEGATIVES')
except: ARITHMETIC_USE_NEGATIVES = False
try: ARITHMETIC_USE_ADDITION = config.getboolean('DEFAULT', 'ARITHMETIC_USE_ADDITION')
except: ARITHMETIC_USE_ADDITION = True
try: ARITHMETIC_USE_SUBTRACTION = config.getboolean('DEFAULT', 'ARITHMETIC_USE_SUBTRACTION')
except: ARITHMETIC_USE_SUBTRACTION = True
try: ARITHMETIC_USE_MULTIPLICATION = config.getboolean('DEFAULT', 'ARITHMETIC_USE_MULTIPLICATION')
except: ARITHMETIC_USE_MULTIPLICATION = True
try: ARITHMETIC_USE_DIVISION = config.getboolean('DEFAULT', 'ARITHMETIC_USE_DIVISION')
except: ARITHMETIC_USE_DIVISION = True

try: COLOR_1 = eval(config.get('DEFAULT', 'COLOR_1'))
except: COLOR_1 = (255, 0, 0, 255)
try: COLOR_2 = eval(config.get('DEFAULT', 'COLOR_2'))
except: COLOR_2 = (48, 48, 48, 255)
try: COLOR_2_BLK = eval(config.get('DEFAULT', 'COLOR_2_BLK'))
except: COLOR_2_BLK = (255, 255, 255, 255)
try: COLOR_3 = eval(config.get('DEFAULT', 'COLOR_3'))
except: COLOR_3 = (0, 0, 255, 255)
try: COLOR_4 = eval(config.get('DEFAULT', 'COLOR_4'))
except: COLOR_4 = (255, 255, 0, 255)
try: COLOR_5 = eval(config.get('DEFAULT', 'COLOR_5'))
except: COLOR_5 = (255, 0, 255, 255)
try: COLOR_6 = eval(config.get('DEFAULT', 'COLOR_6'))
except: COLOR_6 = (0, 255, 255, 255)
try: COLOR_7 = eval(config.get('DEFAULT', 'COLOR_7'))
except: COLOR_7 = (0, 255, 0, 255)
try: COLOR_8 = eval(config.get('DEFAULT', 'COLOR_8'))
except: COLOR_8 = (208, 208, 208, 255)
try: COLOR_8_BLK = eval(config.get('DEFAULT', 'COLOR_8_BLK'))
except: COLOR_8_BLK = (64, 64, 64, 255)
try: COLOR_TEXT = eval(config.get('DEFAULT', 'COLOR_TEXT'))
except: COLOR_TEXT = (0, 0, 0, 255)
try: COLOR_TEXT_BLK = eval(config.get('DEFAULT', 'COLOR_TEXT_BLK'))
except: COLOR_TEXT_BLK = (240, 240, 240, 255)

try: COLOR_LABEL_CORRECT = eval(config.get('DEFAULT', 'COLOR_LABEL_CORRECT'))
except: COLOR_LABEL_CORRECT = (64, 255, 64, 255)
try: COLOR_LABEL_OOPS = eval(config.get('DEFAULT', 'COLOR_LABEL_OOPS'))
except: COLOR_LABEL_OOPS = (64, 64, 255, 255)
try: COLOR_LABEL_INCORRECT = eval(config.get('DEFAULT', 'COLOR_LABEL_INCORRECT'))
except: COLOR_LABEL_INCORRECT = (255, 64, 64, 255)

try: KEY_POSITION = config.getint('DEFAULT', 'KEY_POSITION')
except: KEY_POSITION = 97
try: KEY_AUDIO = config.getint('DEFAULT', 'KEY_AUDIO')
except: KEY_AUDIO = 108
try: KEY_COLOR = config.getint('DEFAULT', 'KEY_COLOR')
except: KEY_COLOR = 102
try: KEY_VISVIS = config.getint('DEFAULT', 'KEY_VISVIS')
except: KEY_VISVIS = 115
try: KEY_VISAUDIO = config.getint('DEFAULT', 'KEY_VISAUDIO')
except: KEY_VISAUDIO = 100
try: KEY_AUDIOVIS = config.getint('DEFAULT', 'KEY_AUDIOVIS')
except: KEY_AUDIOVIS = 106

if BLACK_BACKGROUND:
    COLOR_TEXT = COLOR_TEXT_BLK

if NOVICE_MODE:
    GAME_MODE = 2
    USE_LETTERS = True
    USE_NUMBERS = False
    USE_NATO = False
    USE_PIANO = False
    USE_MORSE = False
    VARIABLE_NBACK = 0

def get_threshold_advance():
    if NOVICE_MODE:
        return NOVICE_ADVANCE
    return THRESHOLD_ADVANCE
def get_threshold_fallback():
    if NOVICE_MODE:
        return NOVICE_FALLBACK
    return THRESHOLD_FALLBACK


# this function checks if a new update for Brain Workshop is available.
update_available = False
update_version = Decimal(0)
def update_check():
    global update_available
    global update_version
    socket.setdefaulttimeout(TIMEOUT_SILENT)
    req = urllib2.Request(WEB_VERSION_CHECK)
    try:
        response = urllib2.urlopen(req)
        version = Decimal(response.readline())
    except:
        return
    if version > Decimal(VERSION):
        update_available = True
        update_version = version

if VERSION_CHECK_ON_STARTUP:
    update_check()

try:
    # workaround for pyglet.gl.ContextException error on certain video cards.
    os.environ["PYGLET_SHADOW_WINDOW"]="0"
    # import pyglet
    import pyglet
    if NOVBO: pyglet.options['graphics_vbo'] = False
    from pyglet.window import key
except:
    str_list = []
    str_list.append('\nError: unable to load pyglet.\n')
    str_list.append('If you already installed pyglet, please ensure ctypes is installed.\n\n')
    str_list.append('Full text of error:\n')
    str_list.append(str(sys.exc_info()))
    str_list.append('\n\nPlease visit ')
    str_list.append(WEB_PYGLET_DOWNLOAD)
    print >> sys.stderr, ''.join(str_list)
    sys.exit(1)

try:
    pyglet.options['audio'] = ('directsound', 'openal', 'alsa', )
    # use in pyglet 1.2: pyglet.options['audio'] = ('directsound', 'pulse', 'openal', )
    import pyglet.media
except:
    str_list = []
    str_list.append('\nNo suitable audio driver could be loaded.\n')
    str_list.append('Full text of error:\n')
    str_list.append(str(sys.exc_info()))
    print >> sys.stderr, ''.join(str_list)
    sys.exit(1)

if USE_MUSIC:
    try:
        from pyglet.media import avbin
    except:
        USE_MUSIC = False
        str_list = []
        str_list.append('\nAVBin not detected. Music disabled.\n')
        str_list.append('Download AVBin from: http://code.google.com/p/avbin/\n\n')
        #str_list.append(str(sys.exc_info()))
        #print >> sys.stderr, ''.join(str_list)
        print ''.join(str_list)
    
# Initialize resources (sounds and images)
#
# --- BEGIN RESOURCE INITIALIZATION SECTION ----------------------------------
#

res_path = os.path.join(get_main_dir(), FOLDER_RES)
if not os.access(res_path, os.F_OK):
    str_list = []
    str_list.append('\nError: the resource folder\n')
    str_list.append(res_path)
    str_list.append('\ndoes not exist or is not readable. Exiting.')
    print >> sys.stderr, ''.join(str_list)
    sys.exit(1)

try:
    pyglet.resource.path = [res_path] # Look only the FOLDER_RES directory
    pyglet.resource.reindex()
except:
    str_list = []
    str_list.append('\nError: pyglet 1.1 or greater is required.\n')
    str_list.append('You probably have an older version of pyglet installed.\n\n')
    str_list.append('Please visit ')
    str_list.append(WEB_PYGLET_DOWNLOAD)
    print >> sys.stderr, ''.join(str_list)
    sys.exit(1)
    
SOUNDS = []
SOUNDS.append('applause.wav') #0 this sound plays when a certain score is achieved
SOUNDS.append('c.wav') #1 sounds 1-8 are the eight non-NATO letter sounds.
SOUNDS.append('h.wav') #2
SOUNDS.append('k.wav') #3
SOUNDS.append('l.wav') #4
SOUNDS.append('q.wav') #5
SOUNDS.append('r.wav') #6
SOUNDS.append('s.wav') #7
SOUNDS.append('t.wav') #8
SOUNDS.append('operation_plus.wav')#9
SOUNDS.append('operation_minus.wav')#10
SOUNDS.append('operation_times.wav')#11
SOUNDS.append('operation_divide.wav')#12
# Make sure DEFAULT_LETTERS corresponds to the letter sounds above, in the
# same order.
DEFAULT_LETTERS = ['C', 'H', 'K', 'L', 'Q', 'R', 'S', 'T']

PIANO_SOUNDS = []
PIANO_SOUNDS.append('piano-1.wav')
PIANO_SOUNDS.append('piano-2.wav')
PIANO_SOUNDS.append('piano-3.wav')
PIANO_SOUNDS.append('piano-4.wav')
PIANO_SOUNDS.append('piano-5.wav')
PIANO_SOUNDS.append('piano-6.wav')
PIANO_SOUNDS.append('piano-7.wav')
PIANO_SOUNDS.append('piano-8.wav')

NUMBER_SOUNDS = []
NUMBER_SOUNDS.append('number-0.wav')
NUMBER_SOUNDS.append('number-1.wav')
NUMBER_SOUNDS.append('number-2.wav')
NUMBER_SOUNDS.append('number-3.wav')
NUMBER_SOUNDS.append('number-4.wav')
NUMBER_SOUNDS.append('number-5.wav')
NUMBER_SOUNDS.append('number-6.wav')
NUMBER_SOUNDS.append('number-7.wav')
NUMBER_SOUNDS.append('number-8.wav')
NUMBER_SOUNDS.append('number-9.wav')
NUMBER_SOUNDS.append('number-10.wav')
NUMBER_SOUNDS.append('number-11.wav')
NUMBER_SOUNDS.append('number-12.wav')
NUMBER_SOUNDS.append('number-13.wav')

NATO_SOUNDS = []
NATO_SOUNDS.append('nato_a.wav')
NATO_SOUNDS.append('nato_b.wav')
NATO_SOUNDS.append('nato_c.wav')
NATO_SOUNDS.append('nato_d.wav')
NATO_SOUNDS.append('nato_e.wav')
NATO_SOUNDS.append('nato_f.wav')
NATO_SOUNDS.append('nato_g.wav')
NATO_SOUNDS.append('nato_h.wav')
NATO_SOUNDS.append('nato_i.wav')
NATO_SOUNDS.append('nato_j.wav')
NATO_SOUNDS.append('nato_k.wav')
NATO_SOUNDS.append('nato_l.wav')
NATO_SOUNDS.append('nato_m.wav')
NATO_SOUNDS.append('nato_n.wav')
NATO_SOUNDS.append('nato_o.wav')
NATO_SOUNDS.append('nato_p.wav')
NATO_SOUNDS.append('nato_q.wav')
NATO_SOUNDS.append('nato_r.wav')
NATO_SOUNDS.append('nato_s.wav')
NATO_SOUNDS.append('nato_t.wav')
NATO_SOUNDS.append('nato_u.wav')
NATO_SOUNDS.append('nato_v.wav')
NATO_SOUNDS.append('nato_w.wav')
NATO_SOUNDS.append('nato_x.wav')
NATO_SOUNDS.append('nato_y.wav')
NATO_SOUNDS.append('nato_z.wav')

MORSE_SOUNDS = []
MORSE_SOUNDS.append('morse_0.wav')
MORSE_SOUNDS.append('morse_1.wav')
MORSE_SOUNDS.append('morse_2.wav')
MORSE_SOUNDS.append('morse_3.wav')
MORSE_SOUNDS.append('morse_4.wav')
MORSE_SOUNDS.append('morse_5.wav')
MORSE_SOUNDS.append('morse_6.wav')
MORSE_SOUNDS.append('morse_7.wav')
MORSE_SOUNDS.append('morse_8.wav')
MORSE_SOUNDS.append('morse_9.wav')
MORSE_SOUNDS.append('morse_a.wav')
MORSE_SOUNDS.append('morse_b.wav')
MORSE_SOUNDS.append('morse_c.wav')
MORSE_SOUNDS.append('morse_d.wav')
MORSE_SOUNDS.append('morse_e.wav')
MORSE_SOUNDS.append('morse_f.wav')
MORSE_SOUNDS.append('morse_g.wav')
MORSE_SOUNDS.append('morse_h.wav')
MORSE_SOUNDS.append('morse_i.wav')
MORSE_SOUNDS.append('morse_j.wav')
MORSE_SOUNDS.append('morse_k.wav')
MORSE_SOUNDS.append('morse_l.wav')
MORSE_SOUNDS.append('morse_m.wav')
MORSE_SOUNDS.append('morse_n.wav')
MORSE_SOUNDS.append('morse_o.wav')
MORSE_SOUNDS.append('morse_p.wav')
MORSE_SOUNDS.append('morse_q.wav')
MORSE_SOUNDS.append('morse_r.wav')
MORSE_SOUNDS.append('morse_s.wav')
MORSE_SOUNDS.append('morse_t.wav')
MORSE_SOUNDS.append('morse_u.wav')
MORSE_SOUNDS.append('morse_v.wav')
MORSE_SOUNDS.append('morse_w.wav')
MORSE_SOUNDS.append('morse_x.wav')
MORSE_SOUNDS.append('morse_y.wav')
MORSE_SOUNDS.append('morse_z.wav')

IMAGES = []
IMAGES.append('brain.png')
IMAGES.append('spr_square_red.png')
IMAGES.append('spr_square_white.png')
IMAGES.append('spr_square_blue.png')
IMAGES.append('spr_square_yellow.png')
IMAGES.append('spr_square_magenta.png')
IMAGES.append('spr_square_cyan.png')
IMAGES.append('spr_square_green.png')
IMAGES.append('spr_square_grey.png')
IMAGES.append('brain_graphic.png')


for resource in (SOUNDS + PIANO_SOUNDS + NUMBER_SOUNDS + NATO_SOUNDS + MORSE_SOUNDS + IMAGES):
    path = os.path.join(res_path, resource)
    if not os.access(path, os.F_OK):
        str_list = []
        str_list.append('\nThe resource ')
        str_list.append(path)
        str_list.append('\ndoes not exist or is not readable. Exiting.')
        print >> sys.stderr, ''.join(str_list)
        sys.exit(1)
        
sound = []
for soundfile in SOUNDS:
    sound.append(pyglet.resource.media(soundfile, streaming=False))
    
numbersound = {}
numbersound['0'] = pyglet.resource.media(NUMBER_SOUNDS[0], streaming=False)
numbersound['1'] = pyglet.resource.media(NUMBER_SOUNDS[1], streaming=False)
numbersound['2'] = pyglet.resource.media(NUMBER_SOUNDS[2], streaming=False)
numbersound['3'] = pyglet.resource.media(NUMBER_SOUNDS[3], streaming=False)
numbersound['4'] = pyglet.resource.media(NUMBER_SOUNDS[4], streaming=False)
numbersound['5'] = pyglet.resource.media(NUMBER_SOUNDS[5], streaming=False)
numbersound['6'] = pyglet.resource.media(NUMBER_SOUNDS[6], streaming=False)
numbersound['7'] = pyglet.resource.media(NUMBER_SOUNDS[7], streaming=False)
numbersound['8'] = pyglet.resource.media(NUMBER_SOUNDS[8], streaming=False)
numbersound['9'] = pyglet.resource.media(NUMBER_SOUNDS[9], streaming=False)
numbersound['10'] = pyglet.resource.media(NUMBER_SOUNDS[10], streaming=False)
numbersound['11'] = pyglet.resource.media(NUMBER_SOUNDS[11], streaming=False)
numbersound['12'] = pyglet.resource.media(NUMBER_SOUNDS[12], streaming=False)
numbersound['13'] = pyglet.resource.media(NUMBER_SOUNDS[13], streaming=False)

pianosound = {}
pianosound['C4'] = pyglet.resource.media(PIANO_SOUNDS[0], streaming=False)
pianosound['D4'] = pyglet.resource.media(PIANO_SOUNDS[1], streaming=False)
pianosound['E4'] = pyglet.resource.media(PIANO_SOUNDS[2], streaming=False)
pianosound['F4'] = pyglet.resource.media(PIANO_SOUNDS[3], streaming=False)
pianosound['G4'] = pyglet.resource.media(PIANO_SOUNDS[4], streaming=False)
pianosound['A4'] = pyglet.resource.media(PIANO_SOUNDS[5], streaming=False)
pianosound['B4'] = pyglet.resource.media(PIANO_SOUNDS[6], streaming=False)
pianosound['C5'] = pyglet.resource.media(PIANO_SOUNDS[7], streaming=False)

natosound = {}
natosound['A'] = pyglet.resource.media(NATO_SOUNDS[0], streaming=False)
natosound['B'] = pyglet.resource.media(NATO_SOUNDS[1], streaming=False)
natosound['C'] = pyglet.resource.media(NATO_SOUNDS[2], streaming=False)
natosound['D'] = pyglet.resource.media(NATO_SOUNDS[3], streaming=False)
natosound['E'] = pyglet.resource.media(NATO_SOUNDS[4], streaming=False)
natosound['F'] = pyglet.resource.media(NATO_SOUNDS[5], streaming=False)
natosound['G'] = pyglet.resource.media(NATO_SOUNDS[6], streaming=False)
natosound['H'] = pyglet.resource.media(NATO_SOUNDS[7], streaming=False)
natosound['I'] = pyglet.resource.media(NATO_SOUNDS[8], streaming=False)
natosound['J'] = pyglet.resource.media(NATO_SOUNDS[9], streaming=False)
natosound['K'] = pyglet.resource.media(NATO_SOUNDS[10], streaming=False)
natosound['L'] = pyglet.resource.media(NATO_SOUNDS[11], streaming=False)
natosound['M'] = pyglet.resource.media(NATO_SOUNDS[12], streaming=False)
natosound['N'] = pyglet.resource.media(NATO_SOUNDS[13], streaming=False)
natosound['O'] = pyglet.resource.media(NATO_SOUNDS[14], streaming=False)
natosound['P'] = pyglet.resource.media(NATO_SOUNDS[15], streaming=False)
natosound['Q'] = pyglet.resource.media(NATO_SOUNDS[16], streaming=False)
natosound['R'] = pyglet.resource.media(NATO_SOUNDS[17], streaming=False)
natosound['S'] = pyglet.resource.media(NATO_SOUNDS[18], streaming=False)
natosound['T'] = pyglet.resource.media(NATO_SOUNDS[19], streaming=False)
natosound['U'] = pyglet.resource.media(NATO_SOUNDS[20], streaming=False)
natosound['V'] = pyglet.resource.media(NATO_SOUNDS[21], streaming=False)
natosound['W'] = pyglet.resource.media(NATO_SOUNDS[22], streaming=False)
natosound['X'] = pyglet.resource.media(NATO_SOUNDS[23], streaming=False)
natosound['Y'] = pyglet.resource.media(NATO_SOUNDS[24], streaming=False)
natosound['Z'] = pyglet.resource.media(NATO_SOUNDS[25], streaming=False)
    
morsesound = {}
morsesound['0'] = pyglet.resource.media(MORSE_SOUNDS[0], streaming=False)
morsesound['1'] = pyglet.resource.media(MORSE_SOUNDS[1], streaming=False)
morsesound['2'] = pyglet.resource.media(MORSE_SOUNDS[2], streaming=False)
morsesound['3'] = pyglet.resource.media(MORSE_SOUNDS[3], streaming=False)
morsesound['4'] = pyglet.resource.media(MORSE_SOUNDS[4], streaming=False)
morsesound['5'] = pyglet.resource.media(MORSE_SOUNDS[5], streaming=False)
morsesound['6'] = pyglet.resource.media(MORSE_SOUNDS[6], streaming=False)
morsesound['7'] = pyglet.resource.media(MORSE_SOUNDS[7], streaming=False)
morsesound['8'] = pyglet.resource.media(MORSE_SOUNDS[8], streaming=False)
morsesound['9'] = pyglet.resource.media(MORSE_SOUNDS[9], streaming=False)
morsesound['A'] = pyglet.resource.media(MORSE_SOUNDS[10], streaming=False)
morsesound['B'] = pyglet.resource.media(MORSE_SOUNDS[11], streaming=False)
morsesound['C'] = pyglet.resource.media(MORSE_SOUNDS[12], streaming=False)
morsesound['D'] = pyglet.resource.media(MORSE_SOUNDS[13], streaming=False)
morsesound['E'] = pyglet.resource.media(MORSE_SOUNDS[14], streaming=False)
morsesound['F'] = pyglet.resource.media(MORSE_SOUNDS[15], streaming=False)
morsesound['G'] = pyglet.resource.media(MORSE_SOUNDS[16], streaming=False)
morsesound['H'] = pyglet.resource.media(MORSE_SOUNDS[17], streaming=False)
morsesound['I'] = pyglet.resource.media(MORSE_SOUNDS[18], streaming=False)
morsesound['J'] = pyglet.resource.media(MORSE_SOUNDS[19], streaming=False)
morsesound['K'] = pyglet.resource.media(MORSE_SOUNDS[20], streaming=False)
morsesound['L'] = pyglet.resource.media(MORSE_SOUNDS[21], streaming=False)
morsesound['M'] = pyglet.resource.media(MORSE_SOUNDS[22], streaming=False)
morsesound['N'] = pyglet.resource.media(MORSE_SOUNDS[23], streaming=False)
morsesound['O'] = pyglet.resource.media(MORSE_SOUNDS[24], streaming=False)
morsesound['P'] = pyglet.resource.media(MORSE_SOUNDS[25], streaming=False)
morsesound['Q'] = pyglet.resource.media(MORSE_SOUNDS[26], streaming=False)
morsesound['R'] = pyglet.resource.media(MORSE_SOUNDS[27], streaming=False)
morsesound['S'] = pyglet.resource.media(MORSE_SOUNDS[28], streaming=False)
morsesound['T'] = pyglet.resource.media(MORSE_SOUNDS[29], streaming=False)
morsesound['U'] = pyglet.resource.media(MORSE_SOUNDS[30], streaming=False)
morsesound['V'] = pyglet.resource.media(MORSE_SOUNDS[31], streaming=False)
morsesound['W'] = pyglet.resource.media(MORSE_SOUNDS[32], streaming=False)
morsesound['X'] = pyglet.resource.media(MORSE_SOUNDS[33], streaming=False)
morsesound['Y'] = pyglet.resource.media(MORSE_SOUNDS[34], streaming=False)
morsesound['Z'] = pyglet.resource.media(MORSE_SOUNDS[35], streaming=False)
    
if USE_MUSIC:
    MUSIC_ADVANCE = []
    MUSIC_ADVANCE.append('areyouawake.ogg')
    MUSIC_ADVANCE.append('glassworks.ogg')
    MUSIC_ADVANCE.append('joyfulnoise.ogg')
    MUSIC_ADVANCE.append('mamaguela.ogg')
    MUSIC_ADVANCE.append('onamistynight.ogg')
    MUSIC_ADVANCE.append('quartetno1.ogg')
    MUSIC_ADVANCE.append('timbacubana.ogg')
    
    MUSIC_GREAT = []
    MUSIC_GREAT.append('biggeorge.ogg')
    MUSIC_GREAT.append('bluerondo.ogg')
    MUSIC_GREAT.append('brandenburg.ogg')
    MUSIC_GREAT.append('caribe.ogg')
    MUSIC_GREAT.append('cornerpocket.ogg')
    MUSIC_GREAT.append('elubechango.ogg')
    MUSIC_GREAT.append('frevorasgado.ogg')
    MUSIC_GREAT.append('linusandlucy.ogg')
    MUSIC_GREAT.append('quieroserpoeta.ogg')
    MUSIC_GREAT.append('streetlife.ogg')
    MUSIC_GREAT.append('suspensionbridge.ogg')
    
    MUSIC_GOOD = []
    MUSIC_GOOD.append('lithia.ogg')
    MUSIC_GOOD.append('autumnleaves.ogg')
    MUSIC_GOOD.append('bbydhyonchord.ogg')
    MUSIC_GOOD.append('blueberryrhyme.ogg')
    MUSIC_GOOD.append('dinah.ogg')
    MUSIC_GOOD.append('harvestbreed.ogg')
    MUSIC_GOOD.append('perisscope.ogg')
    MUSIC_GOOD.append('queenbee.ogg')
    MUSIC_GOOD.append('sarahmencken.ogg')
    MUSIC_GOOD.append('stlouisblues.ogg')
    
    for x in range(len(MUSIC_ADVANCE) - 1, -1, -1):
        path = os.path.join(res_path, MUSIC_ADVANCE[x])
        if not os.access(path, os.F_OK):
            MUSIC_ADVANCE.remove(MUSIC_ADVANCE[x])

    for x in range(len(MUSIC_GREAT) - 1, -1, -1):
        path = os.path.join(res_path, MUSIC_GREAT[x])
        if not os.access(path, os.F_OK):
            MUSIC_GREAT.remove(MUSIC_GREAT[x])

    for x in range(len(MUSIC_GOOD) - 1, -1, -1):
        path = os.path.join(res_path, MUSIC_GOOD[x])
        if not os.access(path, os.F_OK):
            MUSIC_GOOD.remove(MUSIC_GOOD[x])

applauseplayer = pyglet.media.ManagedSoundPlayer()
musicplayer = pyglet.media.ManagedSoundPlayer()

def sound_stop():
    global applauseplayer
    global musicplayer
    musicplayer.volume = 0
    applauseplayer.volume = 0

def fade_out(dt):
    global applauseplayer
    global musicplayer

    if musicplayer.volume > 0:
        if musicplayer.volume <= 0.1:
            musicplayer.volume -= 0.02
        else: musicplayer.volume -= 0.1
        if musicplayer.volume <= 0.02:
            musicplayer.volume = 0
    if applauseplayer.volume > 0:
        if applauseplayer.volume <= 0.1:
            applauseplayer.volume -= 0.02
        else: applauseplayer.volume -= 0.1
        if applauseplayer.volume <= 0.02:
            applauseplayer.volume = 0

    if (applauseplayer.volume == 0 and musicplayer.volume == 0) or mode.trial_number == 3:
        pyglet.clock.unschedule(fade_out)
        
        
#
# --- END RESOURCE INITIALIZATION SECTION ----------------------------------
#
    
    
# The colors of the squares in Triple N-Back mode are defined here.
# Color 1 is used in Dual N-Back mode.
def get_color(color):
    if color == 1:
        return COLOR_1   # red
    elif color == 2:
        if BLACK_BACKGROUND:
            return COLOR_2_BLK # white
        else:
            return COLOR_2    # black
    elif color == 3:
        return COLOR_3  # blue
    elif color == 4:
        return COLOR_4  # yellow
    elif color == 5:
        return COLOR_5  # magenta
    elif color == 6:
        return COLOR_6  # cyan
    elif color == 7:
        return COLOR_7   # green
    elif color == 8:
        if BLACK_BACKGROUND:
            return COLOR_8_BLK # dark gray
        else:
            return COLOR_8 # light gray

# set the input text label size
def input_label_size():
    m = mode.mode
    if m == 2 or m == 3 or m == 7 or m == 8 or m == 9 or m == 10 or m == 11: # or m == 12 or m == 13:
        return 16
    if mode.mode == 4: # or m == 14:
        return 14
    if mode.mode == 5: # or m == 15:
        return 13
    if mode.mode == 6: # or m == 16:
        return 11
    sys.exit(1)

def default_nback_mode(mode):
    if mode == 2:
        return BACK_2
    if mode == 3:
        return BACK_3
    if mode == 4:
        return BACK_4
    if mode == 5:
        return BACK_5
    if mode == 6:
        return BACK_6
    if mode == 7:
        return BACK_7
    if mode == 8:
        return BACK_8
    if mode == 9:
        return BACK_9
    if mode == 10:
        return BACK_10
    if mode == 11:
        return BACK_11
    #if mode == 12:
        #return BACK_12
    #if mode == 13:
        #return BACK_13
    #if mode == 14:
        #return BACK_14
    #if mode == 15:
        #return BACK_15
    #if mode == 16:
        #return BACK_16

def default_ticks(mode):
    if mode == 2:
        return TICKS_2
    if mode == 3:
        return TICKS_3
    if mode == 4:
        return TICKS_4
    if mode == 5:
        return TICKS_5
    if mode == 6:
        return TICKS_6
    if mode == 7:
        return TICKS_7
    if mode == 8:
        return TICKS_8
    if mode == 9:
        return TICKS_9
    if mode == 10:
        return TICKS_10
    if mode == 11:
        return TICKS_11
    #if mode == 12:
        #return TICKS_12
    #if mode == 13:
        #return TICKS_13
    #if mode == 14:
        #return TICKS_14
    #if mode == 15:
        #return TICKS_15
    #if mode == 16:
        #return TICKS_16

#Create the game window
caption = []
caption.append('Brain Workshop ')
caption.append(VERSION)
if STATSFILE != 'stats.txt':
    caption.append(' - ')
    caption.append(STATSFILE)
if WINDOW_FULLSCREEN:
    style = pyglet.window.Window.WINDOW_STYLE_BORDERLESS
else:
    style = pyglet.window.Window.WINDOW_STYLE_DEFAULT
    
class MyWindow(pyglet.window.Window):
    def on_key_press(self, symbol, modifiers):
        pass
    def on_key_release(self, symbol, modifiers):
        pass
    
window = MyWindow(WINDOW_WIDTH, WINDOW_HEIGHT, caption=''.join(caption), style=style)

# set the background color of the window
if BLACK_BACKGROUND:
    pyglet.gl.glClearColor(0, 0, 0, 1)
else:
    pyglet.gl.glClearColor(1, 1, 1, 1)
if WINDOW_FULLSCREEN:
    window.maximize()

# All changeable game state variables are located in an instance of the Mode class
class Mode:
    def __init__(self):
        self.mode = GAME_MODE
        self.back = default_nback_mode(self.mode)
        self.ticks_per_trial = default_ticks(self.mode)
        self.num_trials = NUM_TRIALS

        self.variable_list = []
        
        self.manual = MANUAL
        if not self.manual:
            self.enforce_standard_mode()
                    
        self.position_input = False
        self.color_input = False
        self.visvis_input = False
        self.visaudio_input = False
        self.audiovis_input = False
        self.audio_input = False
        
        self.hide_text = HIDE_TEXT
        
        self.current_position = 0
        self.current_color = 0
        self.current_vis = 0
        self.current_audio = 0
        self.current_number = 0
        self.current_operation = 'none'
        
        self.started = False
        self.paused = False
        self.show_missed = False
        self.game_select = False
        self.sound_select = False
        self.draw_graph = False
        self.title_screen = True
        
        self.session_number = 0
        self.trial_number = 0
        self.tick = 0
        self.progress = 0
        
        self.sound_mode = 'none'
        self.soundlist = []
        
        self.bt_sequence = []
        
    def enforce_standard_mode(self):
        self.back = default_nback_mode(self.mode)
        self.ticks_per_trial = default_ticks(self.mode)
        self.num_trials = NUM_TRIALS
        self.session_number = 0

        
# What follows are the classes which control all the text and graphics.
#
# --- BEGIN GRAPHICS SECTION ----------------------------------------------
#

class Graph:
    def __init__(self):
        self.graph = 2
        self.reset_dictionaries()
        self.reset_percents()

    def reset_dictionaries(self):
        self.dnb = {}
        self.tnb = {}
        self.dlnb = {}
        self.tlnb = {}
        self.qlnb = {}
        self.anb = {}
        self.danb = {}
        self.tanb = {}
        self.ponb = {}
        self.aunb = {}
        #self.dvnb = {}
        #self.mnb = {}
        #self.dmnb = {}
        #self.tmnb = {}
        #self.qmnb = {}
        self.dictionaries = [self.dnb, self.tnb, self.dlnb, self.tlnb, self.qlnb, self.anb,
                             self.danb, self.tanb, self.ponb, self.aunb,]
                             #self.dvnb, self.mnb, self.dmnb, self.tmnb, self.qmnb]
        for dictionary in self.dictionaries:
            dictionary.clear()
        
    def reset_percents(self):
        self.percents = []        
        self.percents.append([]) # dnb
        self.percents.append([]) # tnb
        self.percents.append([]) # dlnb
        self.percents.append([]) # tlnb
        self.percents.append([]) # qlnb
        self.percents.append([]) # anb
        self.percents.append([]) # danb
        self.percents.append([]) # tanb
        self.percents.append([]) # ponb
        self.percents.append([]) # aunb
        
        #self.percents.append([]) # dvnb
        
        #self.percents.append([]) # mnb
        #self.percents.append([]) # dmnb
        #self.percents.append([]) # tmnb
        #self.percents.append([]) # qmnb
        
        self.percents[0].append([])
        self.percents[0].append([])

        self.percents[1].append([])
        self.percents[1].append([])
        self.percents[1].append([])

        self.percents[2].append([])
        self.percents[2].append([])
        self.percents[2].append([])
        self.percents[2].append([])

        self.percents[3].append([])
        self.percents[3].append([])
        self.percents[3].append([])
        self.percents[3].append([])
        self.percents[3].append([])

        self.percents[4].append([])
        self.percents[4].append([])
        self.percents[4].append([])
        self.percents[4].append([])
        self.percents[4].append([])
        self.percents[4].append([])

        self.percents[5].append([])
        
        self.percents[6].append([])
        self.percents[6].append([])

        self.percents[7].append([])
        self.percents[7].append([])
        self.percents[7].append([])
        
        self.percents[8].append([])
        
        self.percents[9].append([])
        
        #self.percents[10].append([])
        #self.percents[10].append([])
        
        #self.percents[11].append([])
        
        #self.percents[12].append([])
        #self.percents[12].append([])
        #self.percents[12].append([])
        #self.percents[12].append([])
        
        #self.percents[13].append([])
        #self.percents[13].append([])
        #self.percents[13].append([])
        #self.percents[13].append([])
        #self.percents[13].append([])

        #self.percents[14].append([])
        #self.percents[14].append([])
        #self.percents[14].append([])
        #self.percents[14].append([])
        #self.percents[14].append([])
        #self.percents[14].append([])
        
    def next_mode(self):
        if self.graph == 11:
            self.graph = 2
        else: self.graph += 1
        
    def parse_stats(self):
        self.reset_dictionaries()
        self.reset_percents()
        
        if os.path.isfile(os.path.join(get_main_dir(), FOLDER_DATA, STATSFILE)):
            try:
                statsfile_path = os.path.join(get_main_dir(), FOLDER_DATA, STATSFILE)
                statsfile = open(statsfile_path, 'r')
                for line in statsfile:
                    if line == '': continue
                    if line == '\n': continue
                    datestamp = date(int(line[:4]), int(line[5:7]), int(line[8:10]))
                    hour = int(line[11:13])
                    if hour <= 3:
                        datestamp = date.fromordinal(datestamp.toordinal() - 1)
                    if line.find('\t') >= 0:
                        separator = '\t'
                    else: separator = ','
                    newline = line.split(separator)
                    try: 
                        if int(newline[7]) != 0: # only consider standard mode
                            continue
                    except:
                        continue
                    newmode = int(newline[3])
                    if newmode > 11:
                        continue
                    newback = int(newline[4])
                    newpercent = int(newline[2])
                    dictionary = self.dictionaries[newmode - 2]
                    if datestamp not in dictionary:
                        dictionary[datestamp] = []
                    contribution = newback
                    dictionary[datestamp].append(contribution)
                    
                    if len(newline) >= 16:
                        if newmode == 2:
                            self.percents[0][0].append(int(newline[9]))
                            self.percents[0][1].append(int(newline[10]))
                        elif newmode == 3:
                            self.percents[1][0].append(int(newline[9]))
                            self.percents[1][1].append(int(newline[11]))
                            self.percents[1][2].append(int(newline[10]))
                        elif newmode == 4:
                            self.percents[2][0].append(int(newline[12]))
                            self.percents[2][1].append(int(newline[13]))
                            self.percents[2][2].append(int(newline[14]))
                            self.percents[2][3].append(int(newline[10]))
                        elif newmode == 5:
                            self.percents[3][0].append(int(newline[9]))
                            self.percents[3][1].append(int(newline[12]))
                            self.percents[3][2].append(int(newline[13]))
                            self.percents[3][3].append(int(newline[14]))
                            self.percents[3][4].append(int(newline[10]))
                        elif newmode == 6:
                            self.percents[4][0].append(int(newline[9]))
                            self.percents[4][1].append(int(newline[12]))
                            self.percents[4][2].append(int(newline[13]))
                            self.percents[4][3].append(int(newline[11]))
                            self.percents[4][4].append(int(newline[14]))
                            self.percents[4][5].append(int(newline[10]))
                        elif newmode == 7:
                            self.percents[5][0].append(int(newline[15]))
                        elif newmode == 8:
                            self.percents[6][0].append(int(newline[9]))
                            self.percents[6][1].append(int(newline[15]))
                        elif newmode == 9:
                            self.percents[7][0].append(int(newline[9]))
                            self.percents[7][1].append(int(newline[15]))
                            self.percents[7][2].append(int(newline[11]))
                        elif newmode == 10:
                            self.percents[8][0].append(int(newline[9]))
                        elif newmode == 11:
                            self.percents[9][0].append(int(newline[10]))
                        #elif newmode == 12:
                            #self.percents[10][0].append(int(newline[9]))
                            #self.percents[10][1].append(int(newline[10]))
                        #elif newmode == 13:
                            #self.percents[11][0].append(int(newline[10]))
                        #elif newmode == 14:
                            #self.percents[12][0].append(int(newline[12]))
                            #self.percents[12][1].append(int(newline[13]))
                            #self.percents[12][2].append(int(newline[14]))
                            #self.percents[12][3].append(int(newline[10]))
                        #elif newmode == 15:
                            #self.percents[13][0].append(int(newline[9]))
                            #self.percents[13][1].append(int(newline[12]))
                            #self.percents[13][2].append(int(newline[13]))
                            #self.percents[13][3].append(int(newline[14]))
                            #self.percents[13][4].append(int(newline[10]))
                        #elif newmode == 16:
                            #self.percents[14][0].append(int(newline[9]))
                            #self.percents[14][1].append(int(newline[12]))
                            #self.percents[14][2].append(int(newline[13]))
                            #self.percents[14][3].append(int(newline[11]))
                            #self.percents[14][4].append(int(newline[14]))
                            #self.percents[14][5].append(int(newline[10]))

                        
                statsfile.close()
            except:
                str_list = []
                str_list.append('\nError parsing stats file\n')
                str_list.append(os.path.join(get_main_dir(), FOLDER_DATA, STATSFILE))
                str_list.append('\n\n')
                str_list.append('Full text of error:\n\n')
                str_list.append(str(sys.exc_info()))
                str_list.append('\n\nPlease fix, delete or rename the stats file.')
                print >> sys.stderr, ''.join(str_list)
                sys.exit(1)

            for dictionary in self.dictionaries:
                for datestamp in dictionary.keys():
                    average = 0.0
                    numentries = 0
                    for entry in dictionary[datestamp]:
                        average += entry
                        numentries += 1
                    dictionary[datestamp] = average / numentries
                    
            for game in range(0, len(self.percents)):
                for category in range(0, len(self.percents[game])):
                    summation = 0
                    count = 0
                    for index in range(0, len(self.percents[game][category])):
                        if index < len(self.percents[game][category]) - 50:
                            continue
                        count += 1
                        summation += self.percents[game][category][index]
                    if count == 0:
                        average = 0
                    else:
                        average = int(summation / count)
                    self.percents[game][category].append(average)
                                    
                        
    def export_data(self):       
        dictionary = {}
        for x in range(len(self.dictionaries)): # cycle through game modes
            chartfile_name = CHARTFILE[x]
            dictionary = self.dictionaries[x]
            
            output = []
            if x == 0: output.append('Date\tDual N-Back Average\n')
            elif x == 1: output.append('Date\tTriple N-Back Average\n')
            elif x == 2: output.append('Date\tDual Combination N-Back Average\n')
            elif x == 3: output.append('Date\tTri Combination N-Back Average\n')
            elif x == 4: output.append('Date\tQuad Combination N-Back Average\n')
            elif x == 5: output.append('Date\tArithmetic N-Back Average\n')
            elif x == 6: output.append('Date\tDual Arithmetic N-Back Average\n')
            elif x == 7: output.append('Date\tTriple Arithmetic N-Back Average\n')
            elif x == 8: output.append('Date\tPosition N-Back Average\n')
            elif x == 9: output.append('Date\tAudio N-Back Average\n')
            #elif x == 10: output.append('Date\tDual Variable N-Back Average\n')
            #elif x == 11: output.append('Date\tMorse Code N-Back Average\n')
            #elif x == 12: output.append('Date\tDual Morse Code N-Back Average\n')
            #elif x == 13: output.append('Date\tTri Morse Code N-Back Average\n')
            #elif x == 14: output.append('Date\tQuad Morse Code N-Back Average\n')
            
            keyslist = dictionary.keys()
            keyslist.sort()
            if len(keyslist) == 0: continue
            for datestamp in keyslist:
                if dictionary[datestamp] == -1:
                    continue
                output.append(str(datestamp))
                output.append('\t')
                output.append(str(dictionary[datestamp]))
                output.append('\n')
        
            try:
                chartfile_path = os.path.join(get_main_dir(), FOLDER_DATA, chartfile_name)
                chartfile = open(chartfile_path, 'w')
                chartfile.write(''.join(output))
                chartfile.close()
                            
            except:
                str_list = []
                str_list.append('\nError writing chart file\n')
                str_list.append(os.path.join(get_main_dir(), FOLDER_DATA, chartfile_name))
                str_list.append('\n\n')
                str_list.append('Full text of error:\n\n')
                str_list.append(str(sys.exc_info()))
                print >> sys.stderr, ''.join(str_list)
                sys.exit(1)
                
    def draw(self):
        if BLACK_BACKGROUND:
            axiscolor = (96, 96, 96)
            linecolor = (0, 0, 255)
            minorcolor = (64, 64, 64)
        else: 
            axiscolor = (160, 160, 160)
            linecolor = (0, 0, 255)
            minorcolor = (224, 224, 224)
        
        x_label_width = 20
        y_marking_interval = 0.25

        height = int(window.height * 0.625)
        width = int(window.width * 0.625)
        center_x = window.width // 2
        center_y = window.height // 2 + 20
        left = center_x - width // 2
        right = center_x + width // 2
        top = center_y + height // 2
        bottom = center_y - height // 2
        
        dictionary = self.dictionaries[self.graph - 2]
        if self.graph == 2: graph_title = 'Dual N-Back'
        elif self.graph == 3: graph_title = 'Triple N-Back'
        elif self.graph == 4: graph_title = 'Dual Combination N-Back'
        elif self.graph == 5: graph_title = 'Tri Combination N-Back'
        elif self.graph == 6: graph_title = 'Quad Combination N-Back'
        elif self.graph == 7: graph_title = 'Arithmetic N-Back'
        elif self.graph == 8: graph_title = 'Dual Arithmetic N-Back'
        elif self.graph == 9: graph_title = 'Triple Arithmetic N-Back'
        elif self.graph == 10: graph_title = 'Position N-Back'
        elif self.graph == 11: graph_title = 'Audio N-Back'
        #elif self.graph == 12: graph_title = 'Dual Variable N-Back'
        #elif self.graph == 13: graph_title = 'Morse Code N-Back'
        #elif self.graph == 14: graph_title = 'Dual Morse Code N-Back'
        #elif self.graph == 15: graph_title = 'Tri Morse Code N-Back'
        #elif self.graph == 16: graph_title = 'Quad Morse Code N-Back'
        
        def drawaxes():
            pyglet.graphics.draw(3, pyglet.gl.GL_LINE_STRIP, ('v2i', (
            left, top,
            left, bottom,
            right, bottom)), ('c3B', axiscolor * 3))
        drawaxes()
        
        str_list = []
        str_list.append('G: Return to Main Screen\n')
        str_list.append('Ctrl-E: Export Data\n')
        str_list.append('\n')
        str_list.append('N: Next Game Type')
        keyslabel = pyglet.text.Label(
            ''.join(str_list),
            multiline = True, width = 300,
            font_size=9,
            color=COLOR_TEXT,
            x=10, y=window.height - 10,
            anchor_x='left', anchor_y='top')
        keyslabel.draw()

        titlelabel = pyglet.text.Label(graph_title,
                                  font_size = 18, bold=True, color=COLOR_TEXT,
                                  x = center_x, y = top + 60,
                                  anchor_x = 'center', anchor_y = 'center')
        titlelabel.draw()
        
        xaxistitle = pyglet.text.Label('Date',
                                  font_size = 12, bold=True, color=COLOR_TEXT,
                                  x = center_x, y = bottom - 80,
                                  anchor_x = 'center', anchor_y = 'center')
        xaxistitle.draw()

        yaxistitle = pyglet.text.Label('Average\nN-Back', multiline=True, width=1,
                                  font_size = 12, bold=True, color=COLOR_TEXT,
                                  x = left - 130, y = center_y,
                                  anchor_x = 'right', anchor_y = 'center')
        yaxistitle.draw()
                
        dates = dictionary.keys()
        dates.sort()
        if len(dates) < 2:
            insufficient_label = pyglet.text.Label(
                'Insufficient data: two days needed',
                font_size = 12, bold = True, color = axiscolor + (255,),
                x = center_x, y = center_y,
                anchor_x = 'center', anchor_y = 'center')
            insufficient_label.draw()
            return
        
        ymin = 100000.0
        ymax = 0.0
        for entry in dates:
            if dictionary[entry] == -1:
                continue
            if dictionary[entry] < ymin:
                ymin = dictionary[entry]
            if dictionary[entry] > ymax:
                ymax = dictionary[entry]
        if ymin == ymax:
            ymin = 0
        
        ymin = int(math.floor(ymin * 4))/4.
        ymax = int(math.ceil(ymax * 4))/4.
        
        # remove these two lines to revert to the old behaviour
        ymin = 1.0
        ymax += 0.25
        
        # add intermediate days
        z = 0
        while z < len(dates) - 1:
            if dates[z+1].toordinal() > dates[z].toordinal() + 1:
                newdate = date.fromordinal(dates[z].toordinal() + 1)
                dates.insert(z+1, newdate)
                dictionary[newdate] = -1
            z += 1
        
        points = []
        xaxislabels = []
        yaxislabels = []
        
        xinterval = width / (float(len(dates) - 1))
        skip_x = int(math.floor(x_label_width / xinterval))
        
        self.last = 0
        def skip():
            if skip_x == 0: return False
            if self.last == 0:
                self.last += 1
                return False
            elif self.last < skip_x:
                self.last += 1
                return True
            elif self.last == skip_x:
                self.last = 0
                return True
            sys.exit(1)
        
        for index in range(len(dates)):
            x = int(xinterval * index + left)
            y = int((dictionary[dates[index]] - ymin)/(ymax - ymin) * height + bottom)
            if dictionary[dates[index]] != -1:
                points.append(x)
                points.append(y)
            datestring = str(dates[index])[2:]
            datestring = datestring.replace('-', '\n')
            if not skip():
                xaxislabels.append(pyglet.text.Label(datestring, multiline=True, width=12,
                                      font_size = 8, bold=False, color=COLOR_TEXT,
                                      x = x, y = bottom - 15,
                                      anchor_x = 'center', anchor_y = 'top'))
                pyglet.graphics.draw(2, pyglet.gl.GL_LINE_STRIP, ('v2i', (
                    x, bottom,
                    x, top)), ('c3B', minorcolor * 2))
                pyglet.graphics.draw(2, pyglet.gl.GL_LINE_STRIP, ('v2i', (
                    x, bottom - 10,
                    x, bottom)), ('c3B', axiscolor * 2))
        
        y_marking = ymin
        while y_marking <= ymax:
            y = int((y_marking - ymin)/(ymax - ymin) * height + bottom)
            yaxislabels.append(pyglet.text.Label(str(round(y_marking, 2)),
                  font_size = 10, bold=False, color=COLOR_TEXT,
                  x = left - 30, y = y + 1,
                  anchor_x = 'center', anchor_y = 'center'))
            pyglet.graphics.draw(2, pyglet.gl.GL_LINE_STRIP, ('v2i', (
                left, y,
                right, y)), ('c3B', minorcolor * 2))
            pyglet.graphics.draw(2, pyglet.gl.GL_LINE_STRIP, ('v2i', (
                left - 10, y,
                left, y)), ('c3B', axiscolor * 2))
            y_marking += y_marking_interval
        
        drawaxes()
            
        for label in xaxislabels:
            label.draw()
        for label in yaxislabels:
            label.draw()
            
        pyglet.graphics.draw(len(points) // 2, pyglet.gl.GL_LINE_STRIP, ('v2i',
            points),
            ('c3B', linecolor * (len(points) // 2)))                                                                        

        radius = 2
        for index in range(0, len(points) // 2):
            pyglet.graphics.draw(4, pyglet.gl.GL_POLYGON, ('v2i',
                (points[index * 2] - radius, points[index * 2 + 1] - radius,
                points[index * 2] - radius, points[index * 2 + 1] + radius,
                points[index * 2] + radius, points[index * 2 + 1] + radius,
                points[index * 2] + radius, points[index * 2 + 1] - radius)),
                ('c3B', linecolor * 4))
            
        str_list = []
        str_list.append('Last 50 rounds:   ')
        if self.graph == 2:
            str_list.append('Position: ')
            str_list.append(str(self.percents[0][0][len(self.percents[0][0])-1]))
            str_list.append('%   ')
            str_list.append('Sound: ')
            str_list.append(str(self.percents[0][1][len(self.percents[0][1])-1]))
            str_list.append('%   ')
        elif self.graph == 3:
            str_list.append('Position: ')
            str_list.append(str(self.percents[1][0][len(self.percents[1][0])-1]))
            str_list.append('%   ')
            str_list.append('Color: ')
            str_list.append(str(self.percents[1][1][len(self.percents[1][1])-1]))
            str_list.append('%   ')
            str_list.append('Sound: ')
            str_list.append(str(self.percents[1][2][len(self.percents[1][2])-1]))
            str_list.append('%   ')
        elif self.graph == 4:
            str_list.append('Vis & n-vis: ')
            str_list.append(str(self.percents[2][0][len(self.percents[2][0])-1]))
            str_list.append('%   ')
            str_list.append('Vis & n-sound: ')
            str_list.append(str(self.percents[2][1][len(self.percents[2][1])-1]))
            str_list.append('%   ')
            str_list.append('Sound & n-vis: ')
            str_list.append(str(self.percents[2][2][len(self.percents[2][2])-1]))
            str_list.append('%   ')
            str_list.append('Sound: ')
            str_list.append(str(self.percents[2][3][len(self.percents[2][3])-1]))
            str_list.append('%   ')
        elif self.graph == 5:
            str_list.append('Position: ')
            str_list.append(str(self.percents[3][0][len(self.percents[3][0])-1]))
            str_list.append('%   ')
            str_list.append('Vis & n-vis: ')
            str_list.append(str(self.percents[3][1][len(self.percents[3][1])-1]))
            str_list.append('%   ')
            str_list.append('Vis & n-sound: ')
            str_list.append(str(self.percents[3][2][len(self.percents[3][2])-1]))
            str_list.append('%   ')
            str_list.append('Sound & n-vis: ')
            str_list.append(str(self.percents[3][3][len(self.percents[3][3])-1]))
            str_list.append('%   ')
            str_list.append('Sound: ')
            str_list.append(str(self.percents[3][4][len(self.percents[3][4])-1]))
            str_list.append('%   ')
        elif self.graph == 6:
            str_list.append('Position: ')
            str_list.append(str(self.percents[4][0][len(self.percents[4][0])-1]))
            str_list.append('%   ')
            str_list.append('Vis & n-vis: ')
            str_list.append(str(self.percents[4][1][len(self.percents[4][1])-1]))
            str_list.append('%   ')
            str_list.append('Vis & n-sound: ')
            str_list.append(str(self.percents[4][2][len(self.percents[4][2])-1]))
            str_list.append('%   ')
            str_list.append('Color: ')
            str_list.append(str(self.percents[4][3][len(self.percents[4][3])-1]))
            str_list.append('%   ')
            str_list.append('Sound & n-vis: ')
            str_list.append(str(self.percents[4][4][len(self.percents[4][4])-1]))
            str_list.append('%   ')
            str_list.append('Sound: ')
            str_list.append(str(self.percents[4][5][len(self.percents[4][5])-1]))
            str_list.append('%   ')
        elif self.graph == 7:
            str_list.append('Arithmetic: ')
            str_list.append(str(self.percents[5][0][len(self.percents[5][0])-1]))
            str_list.append('%   ')
        elif self.graph == 8:
            str_list.append('Position: ')
            str_list.append(str(self.percents[6][0][len(self.percents[6][0])-1]))
            str_list.append('%   ')
            str_list.append('Arithmetic: ')
            str_list.append(str(self.percents[6][1][len(self.percents[6][1])-1]))
            str_list.append('%   ')
        elif self.graph == 9:
            str_list.append('Position: ')
            str_list.append(str(self.percents[7][0][len(self.percents[7][0])-1]))
            str_list.append('%   ')
            str_list.append('Arithmetic: ')
            str_list.append(str(self.percents[7][1][len(self.percents[7][1])-1]))
            str_list.append('%   ')
            str_list.append('Color: ')
            str_list.append(str(self.percents[7][2][len(self.percents[7][2])-1]))
            str_list.append('%   ')
        elif self.graph == 10:
            str_list.append('Position: ')
            str_list.append(str(self.percents[8][0][len(self.percents[8][0])-1]))
            str_list.append('%   ')
        elif self.graph == 11:
            str_list.append('Sound: ')
            str_list.append(str(self.percents[9][0][len(self.percents[9][0])-1]))
            str_list.append('%   ')
        #elif self.graph == 12:
            #str_list.append('Position: ')
            #str_list.append(str(self.percents[10][0][len(self.percents[10][0])-1]))
            #str_list.append('%   ')
            #str_list.append('Sound: ')
            #str_list.append(str(self.percents[10][1][len(self.percents[10][1])-1]))
            #str_list.append('%   ')
        #elif self.graph == 13:
            #str_list.append('Sound: ')
            #str_list.append(str(self.percents[11][0][len(self.percents[11][0])-1]))
            #str_list.append('%   ')
        #elif self.graph == 14:
            #str_list.append('Vis & n-vis: ')
            #str_list.append(str(self.percents[12][0][len(self.percents[12][0])-1]))
            #str_list.append('%   ')
            #str_list.append('Vis & n-sound: ')
            #str_list.append(str(self.percents[12][1][len(self.percents[12][1])-1]))
            #str_list.append('%   ')
            #str_list.append('Sound & n-vis: ')
            #str_list.append(str(self.percents[12][2][len(self.percents[12][2])-1]))
            #str_list.append('%   ')
            #str_list.append('Sound: ')
            #str_list.append(str(self.percents[12][3][len(self.percents[12][3])-1]))
            #str_list.append('%   ')
        #elif self.graph == 15:
            #str_list.append('Position: ')
            #str_list.append(str(self.percents[13][0][len(self.percents[13][0])-1]))
            #str_list.append('%   ')
            #str_list.append('Vis & n-vis: ')
            #str_list.append(str(self.percents[13][1][len(self.percents[13][1])-1]))
            #str_list.append('%   ')
            #str_list.append('Vis & n-sound: ')
            #str_list.append(str(self.percents[13][2][len(self.percents[13][2])-1]))
            #str_list.append('%   ')
            #str_list.append('Sound & n-vis: ')
            #str_list.append(str(self.percents[13][3][len(self.percents[13][3])-1]))
            #str_list.append('%   ')
            #str_list.append('Sound: ')
            #str_list.append(str(self.percents[13][4][len(self.percents[13][4])-1]))
            #str_list.append('%   ')
        #elif self.graph == 16:
            #str_list.append('Position: ')
            #str_list.append(str(self.percents[14][0][len(self.percents[14][0])-1]))
            #str_list.append('%   ')
            #str_list.append('Vis & n-vis: ')
            #str_list.append(str(self.percents[14][1][len(self.percents[14][1])-1]))
            #str_list.append('%   ')
            #str_list.append('Vis & n-sound: ')
            #str_list.append(str(self.percents[14][2][len(self.percents[14][2])-1]))
            #str_list.append('%   ')
            #str_list.append('Color: ')
            #str_list.append(str(self.percents[14][3][len(self.percents[14][3])-1]))
            #str_list.append('%   ')
            #str_list.append('Sound & n-vis: ')
            #str_list.append(str(self.percents[14][4][len(self.percents[14][4])-1]))
            #str_list.append('%   ')
            #str_list.append('Sound: ')
            #str_list.append(str(self.percents[14][5][len(self.percents[14][5])-1]))
            #str_list.append('%   ')
           
        percentagesLabel = pyglet.text.Label(''.join(str_list),
            font_size = 11, bold = False, color = COLOR_TEXT,
            x = window.width // 2, y = 20,
            anchor_x = 'center', anchor_y = 'center')
        
        percentagesLabel.draw()
        

class GameSelect:
    def __init__(self):
        str_list = []
        str_list.append('Type a number or letter choose the game mode.\n')
        str_list.append('\n\n')
        str_list.append('  0: Position N-Back\n')
        str_list.append('  1: Audio N-Back\n')
        str_list.append('\n')
        str_list.append('  2: Dual N-Back (default)\n')
        str_list.append('  3: Triple N-Back\n')
        str_list.append('\n')
        str_list.append('  4: Dual Combination N-Back\n')
        str_list.append('  5: Tri Combination N-Back\n')
        str_list.append('  6: Quad Combination N-Back\n')
        str_list.append('\n')
        str_list.append('  7: Arithmetic N-Back\n')
        str_list.append('  8: Dual Arithmetic N-Back\n')
        str_list.append('  9: Triple Arithmetic N-Back\n')
        #str_list.append('\n')
        #str_list.append('  A: Dual Variable N-Back\n')
        str_list.append('\n\n')
        str_list.append('  ESC: Cancel')
        
        #str_list2 = []
        #str_list2.append('\n\n\n\n')
        #str_list2.append('  S: Morse Code N-Back\n')
        #str_list2.append('  D: Dual Morse Code N-Back\n')
        #str_list2.append('  F: Tri Morse Code N-Back\n')
        #str_list2.append('  G: Quad Morse Code N-Back\n')
        
        self.label = pyglet.text.Label(
            ''.join(str_list), multiline = True, width = 450,
            font_size=14, bold=False, color = COLOR_TEXT,
            x = window.width // 2, y = window.height - 50,
            anchor_x='center', anchor_y='top')
        #self.label2 = pyglet.text.Label(
            #''.join(str_list2), multiline = True, width = 450,
            #font_size=14, bold=False, color = COLOR_TEXT,
            #x = window.width // 3 * 2, y = window.height - 50,
            #anchor_x='center', anchor_y='top')
        
    def draw(self):
        self.label.draw()
        #self.label2.draw()
            
class SoundSelect:
    def __init__(self):
                
        self.label = pyglet.text.Label(
            '', multiline = True, width = 450,
            font_size=14, bold=False, color = COLOR_TEXT,
            x = window.width // 3, y = window.height - 50,
            anchor_x='center', anchor_y='top')
        
    def draw(self):
        str_list = []
        str_list.append('Type a number to choose sounds for the auditory n-back task.\n\n')
        str_list.append('If multiple sounds are selected, one will be randomly chosen each session.\n\n')
        str_list.append('Edit the config file to set permanent defaults.\n')
        str_list.append('\n\n')
        if USE_LETTERS:
            str_list.append('Yes')
        else: str_list.append('No  ')
        str_list.append('  1:  Letters\n')
        if USE_NUMBERS:
            str_list.append('Yes')
        else: str_list.append('No  ')
        str_list.append('  2:  Numbers\n')
        if USE_NATO:
            str_list.append('Yes')
        else: str_list.append('No  ')
        str_list.append('  3:  NATO Phonetic Alphabet\n')
        if USE_PIANO:
            str_list.append('Yes')
        else: str_list.append('No  ')
        str_list.append('  4:  Piano Notes\n')
        if USE_MORSE:
            str_list.append('Yes')
        else: str_list.append('No  ')
        str_list.append('  5:  Morse Code\n')
        str_list.append('\n\n')
        str_list.append('SPACE: Continue')
        
        self.label.text = ''.join(str_list)
        
        self.label.draw()            

# this class controls the field.
# the field is the grid on which the squares appear
class Field:
    def __init__(self):
        self.size = int(window.height * 0.625)
        if BLACK_BACKGROUND:
            self.color = (64, 64, 64)
        else: 
            self.color = (192, 192, 192)
        self.color4 = self.color * 4
        self.color8 = self.color * 8
        self.center_x = window.width // 2
        self.center_y = window.height // 2 + 20
        self.x1 = self.center_x - self.size/2
        self.x2 = self.center_x + self.size/2
        self.x3 = self.center_x - self.size/6
        self.x4 = self.center_x + self.size/6
        self.y1 = self.center_y - self.size/2
        self.y2 = self.center_y + self.size/2
        self.y3 = self.center_y - self.size/6
        self.y4 = self.center_y + self.size/6
        
        # add the inside lines
        self.v_lines = batch.add(8, pyglet.gl.GL_LINES, None, ('v2i', (
            self.x1, self.y3,
            self.x2, self.y3,
            self.x1, self.y4,
            self.x2, self.y4,
            self.x3, self.y1,
            self.x3, self.y2,
            self.x4, self.y1,
            self.x4, self.y2)),
                  ('c3B', self.color8))
                
        self.crosshair_visible = False
        # initialize crosshair
        self.crosshair_update()
                
    # draw the target cross in the center
    def crosshair_update(self):
        if (not mode.paused) and mode.mode != 4 and mode.mode != 7 and mode.mode != 11 and VARIABLE_NBACK == 0: # and mode.mode != 12 and mode.mode != 13 and mode.mode != 14:
            if self.crosshair_visible: return
            else:
                self.v_crosshair = batch.add(4, pyglet.gl.GL_LINES, None, ('v2i', (
                    self.center_x - 8, self.center_y,
                    self.center_x + 8, self.center_y,
                    self.center_x, self.center_y - 8,
                    self.center_x, self.center_y + 8)), ('c3B', self.color4))
                self.crosshair_visible = True
        else:
            if self.crosshair_visible:
                self.v_crosshair.delete()
                self.crosshair_visible = False
            else: return


# this class controls the visual cues (colored squares).
class Visual:
    def __init__(self):
        self.visible = False
        self.label = pyglet.text.Label(
            '',
            font_size=field.size//6, bold=True,
            anchor_x='center', anchor_y='center', batch=batch)
        self.variable_label = pyglet.text.Label(
            '',
            font_size=field.size//6, bold=True,
            anchor_x='center', anchor_y='center', batch=batch)
        self.spr_square = []
        for index in range(1, 9):
            self.spr_square.append(pyglet.sprite.Sprite(pyglet.resource.image(IMAGES[index])))
        self.spr_square_size = self.spr_square[0].width

    def spawn(self, position=0, color=1, vis=0, number=-1, operation='none', variable = 0):
        if OLD_STYLE_SQUARES:
            self.size = int(field.size / 3.2)
        else:
            self.size = int(field.size / 3)
        self.position = position
        self.color = get_color(color)
        self.vis = vis
        if self.position == 0:
            self.center_x = field.center_x
            self.center_y = field.center_y
        elif self.position == 1:
            self.center_x = field.center_x - field.size//3
            self.center_y = field.center_y - field.size//3
        elif self.position == 2:
            self.center_x = field.center_x
            self.center_y = field.center_y - field.size//3
        elif self.position == 3:
            self.center_x = field.center_x + field.size//3
            self.center_y = field.center_y - field.size//3
        elif self.position == 4:
            self.center_x = field.center_x - field.size//3
            self.center_y = field.center_y
        elif self.position == 5:
            self.center_x = field.center_x + field.size//3
            self.center_y = field.center_y
        elif self.position == 6:
            self.center_x = field.center_x - field.size//3
            self.center_y = field.center_y + field.size//3
        elif self.position == 7:
            self.center_x = field.center_x
            self.center_y = field.center_y + field.size//3
        elif self.position == 8:
            self.center_x = field.center_x + field.size//3
            self.center_y = field.center_y + field.size//3
        
        if self.vis == 0:
            if OLD_STYLE_SQUARES:
                lx = self.center_x - self.size // 2 + 2
                rx = self.center_x + self.size // 2 - 2
                by = self.center_y - self.size // 2 + 2
                ty = self.center_y + self.size // 2 - 2
                cr = self.size // 5
                
                # decreases fast
                df1 = 1-math.sin(math.radians(10))
                df2 = 1-math.sin(math.radians(20))
                df3 = 1-math.sin(math.radians(30))
                df4 = 1-math.sin(math.radians(40))
                df5 = 1-math.sin(math.radians(50))
                df6 = 1-math.sin(math.radians(60))
                df7 = 1-math.sin(math.radians(70))
                df8 = 1-math.sin(math.radians(80))
                # decreases slowly
                ds1 = 1-math.cos(math.radians(10))
                ds2 = 1-math.cos(math.radians(20))
                ds3 = 1-math.cos(math.radians(30))
                ds4 = 1-math.cos(math.radians(40))
                ds5 = 1-math.cos(math.radians(50))
                ds6 = 1-math.cos(math.radians(60))
                ds7 = 1-math.cos(math.radians(70))
                ds8 = 1-math.cos(math.radians(80))
                
                x01=lx+cr
                y01=by
                x02=rx-cr
                y02=by
                x03=int(rx-cr*df1)
                y03=int(by+cr*df8)
                x04=int(rx-cr*df2)
                y04=int(by+cr*df7)
                x05=int(rx-cr*df3)
                y05=int(by+cr*df6)
                x06=int(rx-cr*df4)
                y06=int(by+cr*df5)
                x07=int(rx-cr*df5)
                y07=int(by+cr*df4)
                x08=int(rx-cr*df6)
                y08=int(by+cr*df3)
                x09=int(rx-cr*df7)
                y09=int(by+cr*df2)
                x10=int(rx-cr*df8)
                y10=int(by+cr*df1)
                x11=rx
                y11=by+cr
                x12=rx
                y12=ty-cr
                x13=int(rx-cr*df8)
                y13=int(ty-cr*df1)
                x14=int(rx-cr*df7)
                y14=int(ty-cr*df2)
                x15=int(rx-cr*df6)
                y15=int(ty-cr*df3)
                x16=int(rx-cr*df5)
                y16=int(ty-cr*df4)
                x17=int(rx-cr*df4)
                y17=int(ty-cr*df5)
                x18=int(rx-cr*df3)
                y18=int(ty-cr*df6)
                x19=int(rx-cr*df2)
                y19=int(ty-cr*df7)
                x20=int(rx-cr*df1)
                y20=int(ty-cr*df8)
                x21=rx-cr
                y21=ty
                x22=lx+cr
                y22=ty
                x23=int(lx+cr*ds8)
                y23=int(ty-cr*ds1)
                x24=int(lx+cr*ds7)
                y24=int(ty-cr*ds2)
                x25=int(lx+cr*ds6)
                y25=int(ty-cr*ds3)
                x26=int(lx+cr*ds5)
                y26=int(ty-cr*ds4)
                x27=int(lx+cr*ds4)
                y27=int(ty-cr*ds5)
                x28=int(lx+cr*ds3)
                y28=int(ty-cr*ds6)
                x29=int(lx+cr*ds2)
                y29=int(ty-cr*ds7)
                x30=int(lx+cr*ds1)
                y30=int(ty-cr*ds8)
                x31=lx
                y31=ty-cr
                x32=lx
                y32=by+cr
                x33=int(lx+cr*ds1)
                y33=int(by+cr*df1)
                x34=int(lx+cr*ds2)
                y34=int(by+cr*df2)
                x35=int(lx+cr*ds3)
                y35=int(by+cr*df3)
                x36=int(lx+cr*ds4)
                y36=int(by+cr*df4)
                x37=int(lx+cr*ds5)
                y37=int(by+cr*df5)
                x38=int(lx+cr*ds6)
                y38=int(by+cr*df6)
                x39=int(lx+cr*ds7)
                y39=int(by+cr*df7)
                x40=int(lx+cr*ds8)
                y40=int(by+cr*df8)
    
                self.square = batch.add(40, pyglet.gl.GL_POLYGON, None, ('v2i', (
                    x01, y01,
                    x02, y02,
                    x03, y03,
                    x04, y04,
                    x05, y05,
                    x06, y06,
                    x07, y07,
                    x08, y08,
                    x09, y09,
                    x10, y10,
                    x11, y11,
                    x12, y12,
                    x13, y13,
                    x14, y14,
                    x15, y15,
                    x16, y16,
                    x17, y17,
                    x18, y18,
                    x19, y19,
                    x20, y20,
                    x21, y21,
                    x22, y22,
                    x23, y23,
                    x24, y24,
                    x25, y25,
                    x26, y26,
                    x27, y27,
                    x28, y28,
                    x29, y29,
                    x30, y30,
                    x31, y31,
                    x32, y32,
                    x33, y33,
                    x34, y34,
                    x35, y35,
                    x36, y36,
                    x37, y37,
                    x38, y38,
                    x39, y39,
                    x40, y40)),
                    ('c4B', self.color * 40))
                
            else:
                # use sprite squares   
                self.square = self.spr_square[color-1]
                self.square.opacity = 255
                self.square.x = self.center_x - field.size // 6
                self.square.y = self.center_y - field.size // 6
                self.square.scale = 1.0 * self.size / self.spr_square_size
                self.spr_square_size_scaled = self.square.width
                self.square.batch = batch
                
                # initiate square animation
                pyglet.clock.schedule_interval(visual.animate_square, 1/60.)
        
        else: # display a letter
            if mode.mode == 7 or mode.mode == 8 or mode.mode == 9:
                self.label.text = str(number)
            else:
                self.label.text = self.letters[vis - 1]
            self.label.x = self.center_x
            self.label.y = self.center_y + 4
            self.label.color = self.color
            
        if variable > 0:
            # display variable n-back level
            self.variable_label.text = str(variable)

            if mode.mode == 4 or mode.mode == 7 or mode.mode == 11:
                self.variable_label.x = field.center_x
                self.variable_label.y = field.center_y - field.size//3 + 4
            else:
                self.variable_label.x = field.center_x
                self.variable_label.y = field.center_y + 4

            self.variable_label.color = self.color
        
        self.visible = True
        
    def animate_square(self, dt):
        if mode.paused: return
        if not ANIMATE_SQUARES: return
        
        # factors which affect animation
        scale_addition = dt / 4
        opacity_begin = 0.095
        opacity_end = 0.12
    
        self.square.scale += scale_addition
        dx = (self.square.width - self.spr_square_size_scaled) // 2
        self.square.x = self.center_x - field.size // 6 - dx
        self.square.y = self.center_y - field.size // 6 - dx
        
        size_ratio = float(dx) / self.spr_square_size_scaled
        if size_ratio >= opacity_begin:
            opacity_factor = 1.0 - (size_ratio - opacity_begin) / (opacity_end - opacity_begin)
            if opacity_factor < 0: opacity_factor = 0
            self.square.opacity = int(255 * opacity_factor)

    def set_letters(self, letters):
        self.letters = letters
    
    def hide(self):
        if self.visible:
            self.label.text = ''
            self.variable_label.text = ''
            #self.operationlabel.text = ''
            if self.vis == 0:
                if OLD_STYLE_SQUARES:
                    self.square.delete()
                else:
                    self.square.batch = None
                    pyglet.clock.unschedule(visual.animate_square)
            self.visible = False
            
class Circles:
    def __init__(self):
        self.y = window.height - 20
        self.start_x = 30
        self.radius = 8
        self.distance = 20
        if BLACK_BACKGROUND:
            self.not_activated = [64, 64, 64, 255]
        else:
            self.not_activated = [192, 192, 192, 255]
        self.activated = [64, 64, 255, 255]
        if BLACK_BACKGROUND:
            self.invisible = [0, 0, 0, 0]
        else:
            self.invisible = [255, 255, 255, 0]
        
        self.circle = []
        for index in range(0, THRESHOLD_FALLBACK_SESSIONS - 1):
            self.circle.append(batch.add(4, pyglet.gl.GL_QUADS, None, ('v2i', (
                self.start_x + self.distance * index - self.radius,
                self.y + self.radius,
                self.start_x + self.distance * index + self.radius,
                self.y + self.radius,
                self.start_x + self.distance * index + self.radius,
                self.y - self.radius,
                self.start_x + self.distance * index - self.radius,
                self.y - self.radius)),
                ('c4B', self.not_activated * 4)))
            
        self.update()
            
    def update(self):
        if mode.manual or mode.started or NOVICE_MODE:
            for i in range(0, THRESHOLD_FALLBACK_SESSIONS - 1):
                self.circle[i].colors = (self.invisible * 4)
        else:
            for i in range(0, THRESHOLD_FALLBACK_SESSIONS - 1):
                self.circle[i].colors = (self.not_activated * 4)
            for i in range(0, mode.progress):
                self.circle[i].colors = (self.activated * 4)
            
        
# this is the update notification
class UpdateLabel:
    def __init__(self):
        self.label = pyglet.text.Label(
            '',
            multiline = True, width = field.size//3 - 4, halign='middle',
            font_size=11, bold=True,
            color=(0, 128, 0, 255),
            x=window.width//2, y=field.center_x + field.size // 6,
            anchor_x='center', anchor_y='center', batch=batch)
        self.update()
    def update(self):
        if not mode.started and update_available:
            str_list = []
            str_list.append('An update is available (')
            str_list.append(str(update_version))
            str_list.append('). Press W to open web site')
            self.label.text = ''.join(str_list)
        else: self.label.text = ''
        
# this is the black text above the field
class GameModeLabel:
    def __init__(self):
        self.label = pyglet.text.Label(
            '',
            font_size=16,
            color=COLOR_TEXT,
            x=window.width//2, y=window.height - 20,
            anchor_x='center', anchor_y='center', batch=batch)
        self.update()
    def update(self):
        if mode.started and mode.hide_text:
            self.label.text = ''
        else:
            str_list = []
            if NOVICE_MODE:
                str_list.append('Novice mode: ')
            if mode.manual:
                str_list.append('Manual mode: ')
            if mode.mode == 10:
                str_list.append('Position ')
            elif mode.mode == 11:
                str_list.append('Audio ')
            elif mode.mode == 2:
                str_list.append('Dual ')
            elif mode.mode == 3:
                str_list.append('Triple ')
            elif mode.mode == 4:
                str_list.append('Dual Combination ')
            elif mode.mode == 5:
                str_list.append('Tri Combination ')
            elif mode.mode == 6:
                str_list.append('Quad Combination ')
            elif mode.mode == 7:
                str_list.append('Arithmetic ')
            elif mode.mode == 8:
                str_list.append('Dual Arithmetic ')
            elif mode.mode == 9:
                str_list.append('Triple Arithmetic ')
            #elif mode.mode == 12:
                #str_list.append('Dual Variable ')
            #elif mode.mode == 13:
                #str_list.append('Morse Code ')
            #elif mode.mode == 14:
                #str_list.append('Dual Morse Code ')
            #elif mode.mode == 15:
                #str_list.append('Tri Morse Code ')
            #elif mode.mode == 16:
                #str_list.append('Quad Morse Code ')
            if VARIABLE_NBACK == 1:
                str_list.append('V. ')
            str_list.append(str(mode.back))
            str_list.append('-Back')
            self.label.text = ''.join(str_list)

    def flash(self):
        pyglet.clock.unschedule(gameModeLabel.unflash)
        self.label.color = (255,0 , 255, 255)
        self.update()
        pyglet.clock.schedule_once(gameModeLabel.unflash, 0.5)
    def unflash(self, dt):
        self.label.color = COLOR_TEXT
        self.update()

class NoviceWarningLabel:
    def __init__(self):
        self.label = pyglet.text.Label(
            '',
            font_size=12, bold = True,
            color=(255, 0, 255, 255),
            x=window.width//2, y=field.center_x + field.size // 3 + 8,
            anchor_x='center', anchor_y='center', batch=batch)

    def show(self):
        pyglet.clock.unschedule(noviceWarningLabel.hide)
        self.label.text = 'Please disable Novice Mode to access additional modes.'
        pyglet.clock.schedule_once(noviceWarningLabel.hide, 3.0)
    def hide(self, dt):
        self.label.text = ''

# this is the keyboard reference list along the left side
class KeysListLabel:
    def __init__(self):
        self.label = pyglet.text.Label(
            '',
            multiline = True, width = 300, bold = False,
            font_size=9,
            color=COLOR_TEXT,
            x = 10,
            anchor_x='left', anchor_y='top', batch=batch)
        self.update()
    def update(self):
        str_list = []
        if mode.started:
            self.label.y = window.height - 10
            if not mode.hide_text:
                str_list.append('P: Pause / Unpause\n')
                str_list.append('\n')
                str_list.append('F8: Hide / Reveal Text\n')
                str_list.append('\n')                
                str_list.append('ESC: Cancel Session\n')
        else:
            if mode.manual or NOVICE_MODE:
                self.label.y = window.height - 10
            else:
                self.label.y = window.height - 40
            if USE_MORSE:
                str_list.append('J: Morse Code Reference\n')
                str_list.append('\n')
            str_list.append('H: Help / Tutorial\n')
            str_list.append('\n')
            if mode.manual:
                str_list.append('F1: Decrease N-Back\n')
                str_list.append('F2: Increase N-Back\n')
                str_list.append('\n')
                str_list.append('F3: Decrease Trials\n')
                str_list.append('F4: Increase Trials\n')
                str_list.append('\n')
            if mode.manual:
                str_list.append('F5: Decrease Speed\n')
                str_list.append('F6: Increase Speed\n')
                str_list.append('\n')
            str_list.append('C: Choose Game Type\n')
            str_list.append('S: Select Sounds\n')
            if not NOVICE_MODE:
                str_list.append('V: Variable n-back toggle\n')
            if mode.manual:
                str_list.append('M: Standard Mode\n')
            else:
                str_list.append('M: Manual Mode\n')
            str_list.append('\n')
            str_list.append('G: Daily Progress Graph\n')
            str_list.append('\n')
            str_list.append('W: Brain Workshop Web Site\n')
            str_list.append('\n')
            str_list.append('ESC: Exit\n')
            
        self.label.text = ''.join(str_list)

class TitleMessageLabel:
    def __init__(self):
        self.label = pyglet.text.Label(
            'Brain Workshop',
            #multiline = True, width = window.width // 2,
            font_size = 32, bold = True, color = COLOR_TEXT,
            x = window.width // 2, y = window.height - 35,
            anchor_x = 'center', anchor_y = 'center')
    def draw(self):
        self.label.draw()

class TitleKeysLabel:
    def __init__(self):
        str_list = []
        if not NOVICE_MODE:
            str_list.append('C: Choose Game Mode\n')
            str_list.append('S: Choose Sounds\n\n')
        str_list.append('G: Daily Progress Graph\n')
        str_list.append('H: Help / Tutorial\n')
        str_list.append('F: Go to Forum / Mailing List')
        
        self.keys = pyglet.text.Label(
            ''.join(str_list),
            multiline = True, width = 260,
            font_size = 12, bold = True, color = COLOR_TEXT,
            x = window.width // 2, y = 180,
            anchor_x = 'center', anchor_y = 'top')
        
        self.space = pyglet.text.Label(
            'Press SPACE to enter the Workshop',
            font_size = 20, bold = True, color = (32, 32, 255, 255),
            x = window.width // 2, y = 35,
            anchor_x = 'center', anchor_y = 'center')
    def draw(self):
        self.space.draw()
        self.keys.draw()

        
# this is the word "brain" above the brain logo.
class LogoUpperLabel:
    def __init__(self):
        self.label = pyglet.text.Label(
            'Brain',
            font_size=11, bold = True,
            color=COLOR_TEXT,
            x=field.center_x, y=field.center_y + 30,
            anchor_x='center', anchor_y='center')
    def draw(self):
        self.label.draw()

# this is the word "workshop" below the brain logo.
class LogoLowerLabel:
    def __init__(self):
        self.label = pyglet.text.Label(
            'Workshop',
            font_size=11, bold = True,
            color=COLOR_TEXT,
            x=field.center_x, y=field.center_y - 27,
            anchor_x='center', anchor_y='center')
    def draw(self):
        self.label.draw()

# this is the word "Paused" which appears when the game is paused.
class PausedLabel:
    def __init__(self):
        self.label = pyglet.text.Label(
            '',
            font_size=14,
            color=(64, 64, 255, 255),
            x=field.center_x, y=field.center_y,
            anchor_x='center', anchor_y='center', batch=batch)
        self.update()
    def update(self):
        if mode.paused:
            self.label.text = 'Paused'
        else:
            self.label.text = ''

# this is the congratulations message which appears when advancing N-back levels.
class CongratsLabel:
    def __init__(self):
        self.label = pyglet.text.Label(
            '',
            font_size=14,
            color=(255, 32, 32, 255),
            x=field.center_x, y=window.height - 47,
            anchor_x='center', anchor_y='center', batch=batch)
        self.update()
    def update(self, show=False, advance=False, fallback=False, awesome=False, great=False, good=False, perfect = False):
        str_list = []
        if show:
            if perfect: str_list.append('Perfect score! ')
            elif awesome: str_list.append('Awesome score! ')
            elif great: str_list.append('Great score! ')
            elif good: str_list.append('Not bad! ')
            else: str_list.append('Keep trying. You\'re getting there! ')
        if advance:
            str_list.append('N-Back increased')
        elif fallback:
            str_list.append('N-Back decreased')
        self.label.text = ''.join(str_list)
        
class ArithmeticAnswerLabel:
    def __init__(self):
        self.answer = []
        self.negative = False
        self.decimal = False
        self.label = pyglet.text.Label(
            '',
            x=window.width // 5 * 2, y=30,
            anchor_x='left', anchor_y='center', batch=batch)
        self.update()
    def update(self):
        if mode.mode != 7 and mode.mode != 8 and mode.mode != 9:
            self.label.text = ''
            return
        if mode.started and mode.hide_text:
            self.label.text = ''
            return
        
        self.label.font_size = input_label_size()
        str_list = []
        str_list.append('Answer: ')
        str_list.append(str(self.parse_answer()))
        self.label.text = ''.join(str_list)
        
        if SHOW_FEEDBACK and mode.show_missed:
            result = check_match('arithmetic')
            if result == 'correct':
                self.label.color = COLOR_LABEL_CORRECT
                self.label.bold = True
            if result == 'incorrect':
                self.label.color = COLOR_LABEL_INCORRECT
                self.label.bold = True
        else:
            self.label.color = COLOR_TEXT
            self.label.bold = False
        
    def parse_answer(self):
        chars = ''.join(self.answer)
        if chars == '' or chars == '.':
            result = Decimal('0')
        else:
            result = Decimal(chars)
        if self.negative:
            result = Decimal('0') - result
        return result
            
    def input(self, input):
        if input == '-':
            if self.negative:
                self.negative = False
            else: self.negative = True
        elif input == '.' and not self.decimal:
            self.decimal = True
            self.answer.append(input)
        else:
            self.answer.append(input)
        self.update()
    
    def reset_input(self):
        self.answer = []
        self.negative = False
        self.decimal = False
        self.update()
                

# this controls the "A: position match" below the field.
class PositionLabel:
    def __init__(self):
        self.label = pyglet.text.Label(
            '',
            x=20, y=30,
            anchor_x='left', anchor_y='center', batch=batch)
        self.update()
    def update(self):
        self.label.font_size = input_label_size()
        if mode.started and mode.hide_text:
            self.label.text = ''
        elif mode.mode == 10 or mode.mode == 2 or mode.mode == 3 or mode.mode == 8 or mode.mode == 9: # or mode.mode == 12:
            str_list = []
            str_list.append(key.symbol_string(KEY_POSITION))
            str_list.append(': position match')
            self.label.text = ''.join(str_list)
        elif mode.mode == 4:
            self.label.text = ''
        elif mode.mode == 5 or mode.mode == 6: # or mode.mode == 15 or mode.mode == 16:
            str_list = []
            str_list.append(key.symbol_string(KEY_POSITION))
            str_list.append(': position')
            self.label.text = ''.join(str_list)
        else:
            self.label.text = ''
        if SHOW_FEEDBACK and mode.position_input:
            result = check_match('position')
            if result == 'correct':
                self.label.color = COLOR_LABEL_CORRECT
                self.label.bold = True
            elif result == 'unknown':
                self.label.color = COLOR_LABEL_OOPS
                self.label.bold = True
            elif result == 'incorrect':
                self.label.color = COLOR_LABEL_INCORRECT
                self.label.bold = True
        elif SHOW_FEEDBACK and (not mode.audiovis_input) and mode.show_missed:
            result = check_match('position', check_missed = True)
            if result == 'missed':
                self.label.color = COLOR_LABEL_OOPS
                self.label.bold = True
        else:
            self.label.color = COLOR_TEXT
            self.label.bold = False
            
# this controls the "S: visual & n-visual" below the field.
class VisvisLabel:
    def __init__(self):
        self.label = pyglet.text.Label(
            '',
            y=30,
            anchor_y='center', batch=batch)
        self.update()
    def update(self):
        self.label.font_size = input_label_size()
        if mode.started and mode.hide_text:
            self.label.text = ''
        elif mode.mode == 4 or mode.mode == 5 or mode.mode == 6: # or mode.mode == 14 or mode.mode == 15 or mode.mode == 16:
            if mode.mode == 4 or mode.mode == 14: self.label.anchor_x = 'left'
            else: self.label.anchor_x = 'center'
            str_list = []
            str_list.append(key.symbol_string(KEY_VISVIS))
            str_list.append(': vis & n-vis')
            self.label.text = ''.join(str_list)
            if mode.mode == 4: # or mode.mode == 14:
                self.label.x = 20
            elif mode.mode == 5: # or mode.mode == 15:
                self.label.x = window.width // 4
            elif mode.mode == 6: # or mode.mode == 16:
                self.label.x = window.width // 5
        else:
            self.label.text = ''
        if SHOW_FEEDBACK and mode.visvis_input:
            result = check_match('visvis')
            if result == 'correct':
                self.label.color = COLOR_LABEL_CORRECT
                self.label.bold = True
            elif result == 'unknown':
                self.label.color = COLOR_LABEL_OOPS
                self.label.bold = True
            elif result == 'incorrect':
                self.label.color = COLOR_LABEL_INCORRECT
                self.label.bold = True
        elif SHOW_FEEDBACK and (not mode.audiovis_input) and mode.show_missed:
            result = check_match('visvis', check_missed = True)
            if result == 'missed':
                self.label.color = COLOR_LABEL_OOPS
                self.label.bold = True
        else:
            self.label.color = COLOR_TEXT
            self.label.bold = False
        
# this controls the "D: visual & n-audio" below the field.
class VisaudioLabel:
    def __init__(self):
        self.label = pyglet.text.Label(
            '',
            y=30,
            anchor_x = 'center', anchor_y='center', batch=batch)
        self.update()
    def update(self):
        self.label.font_size = input_label_size()
        if mode.started and mode.hide_text:
            self.label.text = ''
        elif mode.mode == 4 or mode.mode == 5 or mode.mode == 6: # or mode.mode == 14 or mode.mode == 15 or mode.mode == 16:
            str_list = []
            str_list.append(key.symbol_string(KEY_VISAUDIO))
            str_list.append(': vis & n-sound')
            self.label.text = ''.join(str_list)
            if mode.mode == 4: # or mode.mode == 14:
                self.label.x = window.width // 3
            elif mode.mode == 5: # or mode.mode == 15:
                self.label.x = window.width // 2
            elif mode.mode == 6: # or mode.mode == 16:
                self.label.x = window.width // 5 * 2
        else:
            self.label.text = ''
        if SHOW_FEEDBACK and mode.visaudio_input:
            result = check_match('visaudio')
            if result == 'correct':
                self.label.color = COLOR_LABEL_CORRECT
                self.label.bold = True
            elif result == 'unknown':
                self.label.color = COLOR_LABEL_OOPS
                self.label.bold = True
            elif result == 'incorrect':
                self.label.color = COLOR_LABEL_INCORRECT
                self.label.bold = True
        elif SHOW_FEEDBACK and (not mode.audiovis_input) and mode.show_missed:
            result = check_match('visaudio', check_missed = True)
            if result == 'missed':
                self.label.color = COLOR_LABEL_OOPS
                self.label.bold = True
        else:
            self.label.color = COLOR_TEXT
            self.label.bold = False

# this controls the "F: color match" below the field.
class ColorLabel:
    def __init__(self):
        self.label = pyglet.text.Label(
            '',
            y=30,
            anchor_y='center', batch=batch)
        self.update()
    def update(self):
        self.label.font_size = input_label_size()
        if mode.started and mode.hide_text:
            self.label.text = ''
        elif mode.mode == 3:
            str_list = []
            str_list.append(key.symbol_string(KEY_COLOR))
            str_list.append(': color match')
            self.label.text = ''.join(str_list)
            self.label.anchor_x = 'center'
            self.label.x = window.width // 2
        elif mode.mode == 6: # or mode.mode == 16:
            str_list = []
            str_list.append(key.symbol_string(KEY_COLOR))
            str_list.append(': color')
            self.label.text = ''.join(str_list)
            self.label.anchor_x = 'center'
            self.label.x = window.width // 5 * 3
        elif mode.mode == 9:
            str_list = []
            str_list.append(key.symbol_string(KEY_COLOR))
            str_list.append(': color match')
            self.label.text = ''.join(str_list)
            self.label.anchor_x = 'right'
            self.label.x = window.width - 20
        else:
            self.label.text = ''
        if SHOW_FEEDBACK and mode.color_input:
            result = check_match('color')
            if result == 'correct':
                self.label.color = COLOR_LABEL_CORRECT
                self.label.bold = True
            elif result == 'unknown':
                self.label.color = COLOR_LABEL_OOPS
                self.label.bold = True
            elif result == 'incorrect':
                self.label.color = COLOR_LABEL_INCORRECT
                self.label.bold = True
        elif SHOW_FEEDBACK and (not mode.audiovis_input) and mode.show_missed:
            result = check_match('color', check_missed = True)
            if result == 'missed':
                self.label.color = COLOR_LABEL_OOPS
                self.label.bold = True
        else:
            self.label.color = COLOR_TEXT
            self.label.bold = False

# this controls the "J: audio & n-visual" below the field.
class AudiovisLabel:
    def __init__(self):
        self.label = pyglet.text.Label(
            '',
            x=window.width - window.width//5, y=30,
            anchor_x='center', anchor_y='center', batch=batch)
        self.update()
    def update(self):
        self.label.font_size = input_label_size()
        if mode.started and mode.hide_text:
            self.label.text = ''
        elif mode.mode == 4 or mode.mode == 5 or mode.mode == 6 or mode.mode == 14 or mode.mode == 15 or mode.mode == 16:
            str_list = []
            str_list.append(key.symbol_string(KEY_AUDIOVIS))
            str_list.append(': sound & n-vis')
            self.label.text = ''.join(str_list)
            if mode.mode == 4: # or mode.mode == 14:
                self.label.x = window.width // 3 * 2
            elif mode.mode == 5: # or mode.mode == 15:
                self.label.x = window.width // 4 * 3
            elif mode.mode == 6: # or mode.mode == 16:
                self.label.x = window.width // 5 * 4
        else:
            self.label.text = ''
        if SHOW_FEEDBACK and mode.audiovis_input:
            result = check_match('audiovis')
            if result == 'correct':
                self.label.color = COLOR_LABEL_CORRECT
                self.label.bold = True
            elif result == 'unknown':
                self.label.color = COLOR_LABEL_OOPS
                self.label.bold = True
            elif result == 'incorrect':
                self.label.color = COLOR_LABEL_INCORRECT
                self.label.bold = True
        elif SHOW_FEEDBACK and (not mode.audiovis_input) and mode.show_missed:
            result = check_match('audiovis', check_missed = True)
            if result == 'missed':
                self.label.color = COLOR_LABEL_OOPS
                self.label.bold = True
        else:
            self.label.color = COLOR_TEXT
            self.label.bold = False

# this controls the "L: letter match" below the field.
class AudioLabel:
    def __init__(self):
        self.label = pyglet.text.Label(
            '',
            x=window.width-20, y=30,
            anchor_x='right', anchor_y='center', batch=batch)
        self.update()
    def update(self):
        self.label.font_size = input_label_size()
        if mode.started and mode.hide_text:
            self.label.text = ''
        elif mode.mode == 11 or mode.mode == 2 or mode.mode == 3: # or mode.mode == 12 or mode.mode == 13:
            str_list = []
            str_list.append(key.symbol_string(KEY_AUDIO))
            str_list.append(': sound match')
            self.label.text = ''.join(str_list)
        elif mode.mode == 4 or mode.mode == 5 or mode.mode == 6: # or mode.mode == 14 or mode.mode == 15 or mode.mode == 16:
            str_list = []
            str_list.append(key.symbol_string(KEY_AUDIO))
            str_list.append(': sound')
            self.label.text = ''.join(str_list)
        else:
            self.label.text = ''
        if SHOW_FEEDBACK and mode.audio_input:
            result = check_match('audio')
            if result == 'correct':
                self.label.color = COLOR_LABEL_CORRECT
                self.label.bold = True
            elif result == 'unknown':
                self.label.color = COLOR_LABEL_OOPS
                self.label.bold = True
            elif result == 'incorrect':
                self.label.color = COLOR_LABEL_INCORRECT
                self.label.bold = True
        elif SHOW_FEEDBACK and (not mode.audiovis_input) and mode.show_missed:
            result = check_match('audio', check_missed = True)
            if result == 'missed':
                self.label.color = COLOR_LABEL_OOPS
                self.label.bold = True
        else:
            self.label.color = COLOR_TEXT
            self.label.bold = False


# this is the text that shows the seconds per trial and the number of trials.
class SessionInfoLabel:
    def __init__(self):
        self.label = pyglet.text.Label(
            '',
            multiline = True, width = 128,
            font_size=11,
            color=COLOR_TEXT,
            x=20, y=field.center_y - 145,
            anchor_x='left', anchor_y='top', batch=batch)
        self.update()
    def update(self):
        if mode.started:
            self.label.text = ''
        else:
            str_list = []
            str_list.append('Session:\n')
            str_list.append(str(mode.ticks_per_trial / 4.0))
            str_list.append(' sec/trial\n')
            str_list.append(str(mode.num_trials))
            str_list.append('+')
            str_list.append(str(mode.back))
            str_list.append(' trials\n')
            str_list.append(str(int((mode.ticks_per_trial / 4.0) * (mode.num_trials + mode.back))))
            str_list.append(' seconds')
            self.label.text = ''.join(str_list)            
    def flash(self):
        pyglet.clock.unschedule(sessionInfoLabel.unflash)
        self.label.bold = True
        self.update()
        pyglet.clock.schedule_once(sessionInfoLabel.unflash, 1.0)
    def unflash(self, dt):
        self.label.bold = False
        self.update()
# this is the text that shows the seconds per trial and the number of trials.

class ThresholdLabel:
    def __init__(self):
        self.label = pyglet.text.Label(
            '',
            multiline = True, width = 155,
            font_size=11,
            color=COLOR_TEXT,
            x=window.width - 20, y=field.center_y - 145,
            anchor_x='right', anchor_y='top', batch=batch)
        self.update()
    def update(self):
        if mode.started or mode.manual:
            self.label.text = ''
        else:
            str_list = []
            str_list.append('Thresholds:\n')
            str_list.append('Raise level: >= ')
            str_list.append(str(get_threshold_advance()))
            str_list.append('%\n')
            str_list.append('Lower level: < ')
            str_list.append(str(get_threshold_fallback()))
            str_list.append('%')
            self.label.text = ''.join(str_list)            
        
# this controls the "press space to begin session #" text.
class SpaceLabel:
    def __init__(self):
        self.label = pyglet.text.Label(
            '',
            font_size=16,
            bold=True,
            color=(32, 32, 255, 255),
            x=window.width//2, y=62,
            anchor_x='center', anchor_y='center', batch=batch)
        self.update()
    def update(self):
        if mode.started:
            self.label.text = ''
        else: 
            str_list = []
            str_list.append('Press SPACE to begin session #')
            str_list.append(str(mode.session_number + 1))
            str_list.append(': ')
            if mode.mode == 10:
                str_list.append('Position ')
            elif mode.mode == 11:
                str_list.append('Audio ')
            elif mode.mode == 2:
                str_list.append('Dual ')
            elif mode.mode == 3:
                str_list.append('Triple ')
            elif mode.mode == 4:
                str_list.append('Dual Combination ')
            elif mode.mode == 5:
                str_list.append('Tri Combination ')
            elif mode.mode == 6:
                str_list.append('Quad Combination ')
            elif mode.mode == 7:
                str_list.append('Arithmetic ')
            elif mode.mode == 8:
                str_list.append('Dual Arithmetic ')
            elif mode.mode == 9:
                str_list.append('Triple Arithmetic ')
            #elif mode.mode == 12:
                #str_list.append('Dual Variable ')
            #elif mode.mode == 13:
                #str_list.append('Morse Code ')
            #elif mode.mode == 14:
                #str_list.append('Dual Morse Code ')
            #elif mode.mode == 15:
                #str_list.append('Tri Morse Code ')
            #elif mode.mode == 16:
                #str_list.append('Quad Morse Code ')
                
            if VARIABLE_NBACK == 1:
                str_list.append('V. ')
            str_list.append(str(mode.back))
            str_list.append('-Back')
            self.label.text = ''.join(str_list)
        
def check_match(input_type, check_missed = False):
    current = 0
    back_data = ''
    operation = 0
    if VARIABLE_NBACK == 1:
        nback_trial = mode.trial_number - mode.variable_list[mode.trial_number - mode.back - 1] - 1
    else:
        nback_trial = mode.trial_number - mode.back - 1
        
    if len(stats.session['position']) < mode.back:
        return 'unknown'
    if input_type == 'position':
        current = mode.current_position
        back_data = 'position'
    elif input_type == 'color':
        current = mode.current_color
        back_data = 'color'
    elif input_type == 'visvis':
        current = mode.current_vis
        back_data = 'vis'
    elif input_type == 'visaudio':
        current = mode.current_vis
        back_data = 'audio'
    elif input_type == 'audiovis':
        current = mode.current_audio
        back_data = 'vis'
    elif input_type == 'audio':
        current = mode.current_audio
        back_data = 'audio'
    elif input_type == 'arithmetic':
        current = mode.current_number
        back_data = stats.session['number'][nback_trial]
        operation = mode.current_operation
        
    if input_type == 'arithmetic':
        if operation == 'add':
            correct_answer = back_data + current
        elif operation == 'subtract':
            correct_answer = back_data - current
        elif operation == 'multiply':
            correct_answer = back_data * current
        elif operation == 'divide':
            correct_answer = Decimal(back_data) / Decimal(current)
        if correct_answer == arithmeticAnswerLabel.parse_answer():
            return 'correct'
        
    elif current == stats.session[back_data][nback_trial]:
        if check_missed:
            return 'missed'
        else:
            return 'correct'
    return 'incorrect'

                
# this controls the statistics which display upon completion of a session.
class AnalysisLabel:
    def __init__(self):
        self.label = pyglet.text.Label(
            '',
            font_size=14,
            color=COLOR_TEXT,
            x=window.width//2, y=92,
            anchor_x='center', anchor_y='center', batch=batch)
        self.update()
    def update(self, skip = False):
        if mode.started or mode.session_number == 0 or skip:
            self.label.text = ''
            return
        
        position_right = 0
        position_wrong = 0
        color_right = 0
        color_wrong = 0
        visvis_right = 0
        visvis_wrong = 0
        visaudio_right = 0
        visaudio_wrong = 0
        audiovis_right = 0
        audiovis_wrong = 0
        audio_right = 0
        audio_wrong = 0
        arithmetic_right = 0
        arithmetic_wrong = 0
                    
        for x in range(len(stats.session['position'])):
            if x < mode.back: continue
            
            data = stats.session
            if mode.mode != 12:
                back = mode.back
            else:
                back = mode.variable_list[x - mode.back]
                            
            # data is a dictionary of lists.

            if data['position'][x] == data['position'][x-back] and data['position_input'][x]:
                position_right += 1
            elif data['position'][x] != data['position'][x-back] and data['position_input'][x]:
                position_wrong += 1
            elif data['position'][x] == data['position'][x-back] and not data['position_input'][x]:
                position_wrong += 1
            elif NOVICE_MODE and data['position'][x] != data['position'][x-back] and not data['position_input'][x]:
                    position_right += 1

            if data['color'][x] == data['color'][x-back] and data['color_input'][x]:
                color_right += 1
            elif data['color'][x] != data['color'][x-back] and data['color_input'][x]:
                color_wrong += 1
            elif data['color'][x] == data['color'][x-back] and not data['color_input'][x]:
                color_wrong += 1
            elif NOVICE_MODE and data['color'][x] != data['color'][x-back] and not data['color_input'][x]:
                color_right += 1

            if data['vis'][x] == data['vis'][x-back] and data['visvis_input'][x]:
                visvis_right += 1
            elif data['vis'][x] != data['vis'][x-back] and data['visvis_input'][x]:
                visvis_wrong += 1
            elif data['vis'][x] == data['vis'][x-back] and not data['visvis_input'][x]:
                visvis_wrong += 1
            elif NOVICE_MODE and data['vis'][x] != data['vis'][x-back] and not data['visvis_input'][x]:
                visvis_right += 1

            if data['vis'][x] == data['audio'][x-back] and data['visaudio_input'][x]:
                visaudio_right += 1
            elif data['vis'][x] != data['audio'][x-back] and data['visaudio_input'][x]:
                visaudio_wrong += 1
            elif data['vis'][x] == data['audio'][x-back] and not data['visaudio_input'][x]:
                visaudio_wrong += 1
            elif NOVICE_MODE and data['vis'][x] != data['audio'][x-back] and not data['visaudio_input'][x]:
                visaudio_right += 1

            if data['audio'][x] == data['vis'][x-back] and data['audiovis_input'][x]:
                audiovis_right += 1
            elif data['audio'][x] != data['vis'][x-back] and data['audiovis_input'][x]:
                audiovis_wrong += 1
            elif data['audio'][x] == data['vis'][x-back] and not data['audiovis_input'][x]:
                audiovis_wrong += 1
            elif NOVICE_MODE and data['audio'][x] != data['vis'][x-back] and not data['audiovis_input'][x]:
                audiovis_right += 1

            if data['audio'][x] == data['audio'][x-back] and data['audio_input'][x]:
                audio_right += 1
            elif data['audio'][x] != data['audio'][x-back] and data['audio_input'][x]:
                audio_wrong += 1
            elif data['audio'][x] == data['audio'][x-back] and not data['audio_input'][x]:
                audio_wrong += 1
            elif NOVICE_MODE and data['audio'][x] != data['audio'][x-back] and not data['audio_input'][x]:
                audio_right += 1

            if mode.mode == 7 or mode.mode == 8 or mode.mode == 9:
                if data['operation'][x] == 'add':
                    if data['number'][x-back] + data['number'][x] == data['arithmetic_input'][x]:
                        arithmetic_right += 1
                    else:
                        arithmetic_wrong += 1
                elif data['operation'][x] == 'subtract':
                    if data['number'][x-back] - data['number'][x] == data['arithmetic_input'][x]:
                        arithmetic_right += 1
                    else:
                        arithmetic_wrong += 1
                elif data['operation'][x] == 'multiply':
                    if data['number'][x-back] * data['number'][x] == data['arithmetic_input'][x]:
                        arithmetic_right += 1
                    else:
                        arithmetic_wrong += 1
                elif data['operation'][x] == 'divide':
                    if Decimal(data['number'][x-back]) / Decimal(data['number'][x]) == data['arithmetic_input'][x]:
                        arithmetic_right += 1
                    else:
                        arithmetic_wrong += 1
                
        str_list = []
        separator = '   '
        str_list.append('Correct-Errors:   ')
        
        if mode.mode == 10 or mode.mode == 2 or mode.mode == 3 or mode.mode == 5 or mode.mode == 6 or mode.mode == 8 or mode.mode == 9: # or mode.mode == 12:
            str_list.append(key.symbol_string(KEY_POSITION))
            str_list.append(':')
            str_list.append(str(position_right))
            str_list.append('-')
            str_list.append(str(position_wrong))
            str_list.append(separator)
            
        if mode.mode == 4 or mode.mode == 5 or mode.mode == 6: # or mode.mode == 14 or mode.mode == 15 or mode.mode == 16:
            str_list.append(key.symbol_string(KEY_VISVIS))
            str_list.append(':')
            str_list.append(str(visvis_right))
            str_list.append('-')
            str_list.append(str(visvis_wrong))
            str_list.append(separator)

            str_list.append(key.symbol_string(KEY_VISAUDIO))
            str_list.append(':')
            str_list.append(str(visaudio_right))
            str_list.append('-')
            str_list.append(str(visaudio_wrong))
            str_list.append(separator)

        if mode.mode == 3 or mode.mode == 6 or mode.mode == 9: # or mode.mode == 16:
            str_list.append(key.symbol_string(KEY_COLOR))
            str_list.append(':')
            str_list.append(str(color_right))
            str_list.append('-')
            str_list.append(str(color_wrong))
            str_list.append(separator)
            
        if mode.mode == 4 or mode.mode == 5 or mode.mode == 6: # or mode.mode == 14 or mode.mode == 15 or mode.mode == 16:
            str_list.append(key.symbol_string(KEY_AUDIOVIS))
            str_list.append(':')
            str_list.append(str(audiovis_right))
            str_list.append('-')
            str_list.append(str(audiovis_wrong))
            str_list.append(separator)
            
        if mode.mode == 11 or mode.mode == 2 or mode.mode == 3 or mode.mode == 4 or mode.mode == 5 or mode.mode == 6: # or mode.mode == 12: # or mode.mode == 13 or mode.mode == 14 or mode.mode == 15 or mode.mode == 16:
            str_list.append(key.symbol_string(KEY_AUDIO))
            str_list.append(':')
            str_list.append(str(audio_right))
            str_list.append('-')
            str_list.append(str(audio_wrong))
            str_list.append(separator)
        
        if mode.mode == 7 or mode.mode == 8 or mode.mode == 9:
            str_list.append('Arithmetic:')
            str_list.append(str(arithmetic_right))
            str_list.append('-')
            str_list.append(str(arithmetic_wrong))
            str_list.append(separator)

        right = 0
        wrong = 0
        if mode.mode == 10:
            right += position_right
            wrong += position_wrong
        elif mode.mode == 11:
            right += audio_right
            wrong += audio_wrong
        elif mode.mode == 2:
            right += position_right
            wrong += position_wrong
            right += audio_right
            wrong += audio_wrong
        elif mode.mode == 3:
            right += position_right
            wrong += position_wrong
            right += color_right
            wrong += color_wrong
            right += audio_right
            wrong += audio_wrong
        elif mode.mode == 4:
            right += visvis_right
            wrong += visvis_wrong
            right += visaudio_right
            wrong += visaudio_wrong
            right += audiovis_right
            wrong += audiovis_wrong
            right += audio_right
            wrong += audio_wrong
        elif mode.mode == 5:
            right += position_right
            wrong += position_wrong
            right += visvis_right
            wrong += visvis_wrong
            right += visaudio_right
            wrong += visaudio_wrong
            right += audiovis_right
            wrong += audiovis_wrong
            right += audio_right
            wrong += audio_wrong
        elif mode.mode == 6:
            right += position_right
            wrong += position_wrong
            right += visvis_right
            wrong += visvis_wrong
            right += visaudio_right
            wrong += visaudio_wrong
            right += color_right
            wrong += color_wrong
            right += audiovis_right
            wrong += audiovis_wrong
            right += audio_right
            wrong += audio_wrong
        elif mode.mode == 7:
            right += arithmetic_right
            wrong += arithmetic_wrong
        elif mode.mode == 8:
            right += position_right
            wrong += position_wrong
            right += arithmetic_right
            wrong += arithmetic_wrong
        elif mode.mode == 9:
            right += position_right
            wrong += position_wrong
            right += color_right
            wrong += color_wrong
            right += arithmetic_right
            wrong += arithmetic_wrong
        #elif mode.mode == 12:
            #right += position_right
            #wrong += position_wrong
            #right += audio_right
            #wrong += audio_wrong
        #elif mode.mode == 13:
            #right += audio_right
            #wrong += audio_wrong
        #elif mode.mode == 14:
            #right += visvis_right
            #wrong += visvis_wrong
            #right += visaudio_right
            #wrong += visaudio_wrong
            #right += audiovis_right
            #wrong += audiovis_wrong
            #right += audio_right
            #wrong += audio_wrong
        #elif mode.mode == 15:
            #right += position_right
            #wrong += position_wrong
            #right += visvis_right
            #wrong += visvis_wrong
            #right += visaudio_right
            #wrong += visaudio_wrong
            #right += audiovis_right
            #wrong += audiovis_wrong
            #right += audio_right
            #wrong += audio_wrong
        #elif mode.mode == 16:
            #right += position_right
            #wrong += position_wrong
            #right += visvis_right
            #wrong += visvis_wrong
            #right += visaudio_right
            #wrong += visaudio_wrong
            #right += color_right
            #wrong += color_wrong
            #right += audiovis_right
            #wrong += audiovis_wrong
            #right += audio_right
            #wrong += audio_wrong
            
        total = right + wrong
        if total == 0:
            percent = 0
        else:
            percent = int(right * 100 / float(right + wrong))
        
        category_percents = {}
        if mode.mode == 10 or mode.mode == 2 or mode.mode == 3 or mode.mode == 5 or mode.mode == 6 or mode.mode == 8 or mode.mode == 9: # or mode.mode == 12:
            if position_right + position_wrong == 0:
                category_percents['position'] = 0
            else:
                category_percents['position'] = int(position_right * 100 / float(position_right + position_wrong))
        else: category_percents['position'] = 0
        
        if mode.mode == 4 or mode.mode == 5 or mode.mode == 6: # or mode.mode == 14 or mode.mode == 15 or mode.mode == 16:
            if visvis_right + visvis_wrong == 0:
                category_percents['visvis'] = 0
            else:
                category_percents['visvis'] = int(visvis_right * 100 / float(visvis_right + visvis_wrong))
        else: category_percents['visvis'] = 0
        
        if mode.mode == 4 or mode.mode == 5 or mode.mode == 6: # or mode.mode == 14 or mode.mode == 15 or mode.mode == 16:
            if visaudio_right + visaudio_wrong == 0:
                category_percents['visaudio'] = 0
            else:
                category_percents['visaudio'] = int(visaudio_right * 100 / float(visaudio_right + visaudio_wrong))
        else: category_percents['visaudio'] = 0
        
        if mode.mode == 3 or mode.mode == 6 or mode.mode == 9: # or mode.mode == 16:
            if color_right + color_wrong == 0:
                category_percents['color'] = 0
            else:
                category_percents['color'] = int(color_right * 100 / float(color_right + color_wrong))
        else: category_percents['color'] = 0
        if mode.mode == 4 or mode.mode == 5 or mode.mode == 6: # or mode.mode == 14 or mode.mode == 15 or mode.mode == 16:
            if audiovis_right + audiovis_wrong == 0:
                category_percents['audiovis'] = 0
            else:
                category_percents['audiovis'] = int(audiovis_right * 100 / float(audiovis_right + audiovis_wrong))
        else: category_percents['audiovis'] = 0
        
        if mode.mode == 11 or mode.mode == 2 or mode.mode == 3 or mode.mode == 4 or mode.mode == 5 or mode.mode == 6: # or mode.mode == 12: # or mode.mode == 13 or mode.mode == 14 or mode.mode == 15 or mode.mode == 16:
            if audio_right + audio_wrong == 0:
                category_percents['audio'] = 0
            else:
                category_percents['audio'] = int(audio_right * 100 / float(audio_right + audio_wrong))
        else: category_percents['audio'] = 0
        
        if mode.mode == 7 or mode.mode == 8 or mode.mode == 9:
            if arithmetic_right + arithmetic_wrong == 0:
                category_percents['arithmetic'] = 0
            else:
                category_percents['arithmetic'] = int(arithmetic_right * 100 / float(arithmetic_right + arithmetic_wrong))
        else: category_percents['arithmetic'] = 0
        
        if NOVICE_MODE:
            percent = min(category_percents['position'], category_percents['audio'])
        
        if NOVICE_MODE:
            str_list.append('Lowest score: ')
        else:
            str_list.append('Score: ')
        str_list.append(str(percent))
        str_list.append('%')
        
        self.label.text = ''.join(str_list)
        stats.submit_session(percent, category_percents)
                    
# this controls the title of the session history chart.
class ChartTitleLabel:
    def __init__(self):
        self.label = pyglet.text.Label(
            '',
            font_size=11, bold=True,
            color=COLOR_TEXT,
            x=window.width - 10, y=window.height-25,
            anchor_x='right', anchor_y='top', batch=batch)
        self.update()
    def update(self):
        if mode.started:
            self.label.text = ''
        else:
            self.label.text = 'Today\'s Last 20:'

# this controls the session history chart.
class ChartLabel:
    def __init__(self):
        self.start_x = window.width - 140
        self.start_y = window.height - 65
        self.line_spacing = 15
        self.column_spacing_12 = 40
        self.column_spacing_23 = 45
        self.font_size = 10
        self.color_normal = (128, 128, 128, 255)
        self.color_advance = (0, 160, 0, 255)
        self.color_fallback = (160, 0, 0, 255)
        self.column1 = []
        self.column2 = []
        self.column3 = []
        for zap in range(0, 20):
            self.column1.append(pyglet.text.Label(
                '', font_size = self.font_size,
                x = self.start_x, y = self.start_y - zap * self.line_spacing,
                anchor_x = 'left', anchor_y = 'top', batch=batch))
            self.column2.append(pyglet.text.Label(
                '', font_size = self.font_size,
                x = self.start_x + self.column_spacing_12, y = self.start_y - zap * self.line_spacing,
                anchor_x = 'left', anchor_y = 'top', batch=batch))
            self.column3.append(pyglet.text.Label(
                '', font_size = self.font_size,
                x = self.start_x + self.column_spacing_12 + self.column_spacing_23, y = self.start_y - zap * self.line_spacing,
                anchor_x = 'left', anchor_y = 'top', batch=batch))
                        
        if os.path.isfile(os.path.join(get_main_dir(), FOLDER_DATA, STATSFILE)):
            try:
                last_session_number = 0
                last_mode = 0
                last_back = 0
                use_last_session = False
                statsfile_path = os.path.join(get_main_dir(), FOLDER_DATA, STATSFILE)
                statsfile = open(statsfile_path, 'r')
                today = date.today()
                if int(strftime('%H')) <= 3:
                    today = date.fromordinal(today.toordinal() - 1)
                for line in statsfile:
                    if line == '': continue
                    if line == '\n': continue
                    datestamp = date(int(line[:4]), int(line[5:7]), int(line[8:10]))
                    if datestamp != today:
                        continue
                    if line.find('\t') >= 0:
                        separator = '\t'
                    else: separator = ','
                    stats.sessions_today += 1
                    newline = line.split(separator)
                    newmode = int(newline[3])
                    if newmode > 11:
                        continue
                    newback = int(newline[4])
                    newpercent = int(newline[2])
                    newmanual = 0
                    try:
                        newmanual = bool(int(newline[7]))
                    except:
                        newmanual = False
                    newsession_number = -1
                    if newmanual:
                        use_last_session = False
                    else:
                        try:
                            newsession_number = int(newline[8])
                        except:
                            pass
                        use_last_session = True
                        last_session_number = newsession_number
                        last_mode = newmode
                        if newpercent >= get_threshold_advance():
                            last_back = newback + 1
                        else:
                            last_back = newback

                    stats.history.append([newsession_number, newmode, newback, newpercent, newmanual])
                
                statsfile.close()
                    
                if use_last_session:
                    mode.mode = last_mode
                    if NOVICE_MODE:
                        mode.mode = 2
                    mode.enforce_standard_mode()
                    mode.back = last_back
                    mode.session_number = last_session_number
    
            except:
                str_list = []
                str_list.append('\nError parsing stats file\n')
                str_list.append(os.path.join(get_main_dir(), FOLDER_DATA, STATSFILE))
                str_list.append('\n\n')
                str_list.append('Full text of error:\n\n')
                str_list.append(str(sys.exc_info()))
                str_list.append('\n\nPlease fix, delete or rename the stats file.')
                #print >> sys.stderr, ''.join(str_list)
                print ''.join(str_list)
        
        self.update()
    def update(self):
        for x in range(0, 20):
            self.column1[x].text = ''
            self.column2[x].text = ''
            self.column3[x].text = ''
        if mode.started: return
        index = 0
        for x in range(len(stats.history) - 20, len(stats.history)):
            if x < 0: continue
            self.column1[index].color = self.color_normal
            self.column2[index].color = self.color_normal
            self.column3[index].color = self.color_normal
            manual = False
            try:
                if stats.history[x][4]:
                    manual = True
            except:
                pass
            if not manual and stats.history[x][3] >= get_threshold_advance():
                self.column1[index].color = self.color_advance
                self.column2[index].color = self.color_advance
                self.column3[index].color = self.color_advance
            elif not manual and stats.history[x][3] < get_threshold_fallback():
                self.column1[index].color = self.color_fallback
                self.column2[index].color = self.color_fallback
                self.column3[index].color = self.color_fallback
            str_list = []
            if manual:
                str_list.append('M')
            elif stats.history[x][0] > -1:
                str_list.append('#')
                str_list.append(str(stats.history[x][0]))
            self.column1[index].text = ''.join(str_list)
            str_list = []
            if stats.history[x][1] == 10: str_list.append('Po')
            elif stats.history[x][1] == 11: str_list.append('Au')
            elif stats.history[x][1] == 2: str_list.append('D')
            elif stats.history[x][1] == 3: str_list.append('T')
            elif stats.history[x][1] == 4: str_list.append('DC')
            elif stats.history[x][1] == 5: str_list.append('TC')
            elif stats.history[x][1] == 6: str_list.append('QC')
            elif stats.history[x][1] == 7: str_list.append('A')
            elif stats.history[x][1] == 8: str_list.append('DA')
            elif stats.history[x][1] == 9: str_list.append('TA')
            #elif stats.history[x][1] == 12: str_list.append('DV')
            #elif stats.history[x][1] == 13: str_list.append('M')
            #elif stats.history[x][1] == 14: str_list.append('DM')
            #elif stats.history[x][1] == 15: str_list.append('TM')
            #elif stats.history[x][1] == 16: str_list.append('QM')
            str_list.append(str(stats.history[x][2]))
            str_list.append('B')
            self.column2[index].text = ''.join(str_list)
            str_list = []
            str_list.append(str(stats.history[x][3]))
            str_list.append('%')
            self.column3[index].text = ''.join(str_list)
            index += 1
            
# this controls the title of the session history chart.
class AverageLabel:
    def __init__(self):
        self.label = pyglet.text.Label(
            '',
            font_size=9, bold=True,
            color=COLOR_TEXT,
            x=window.width - 10, y=window.height-45,
            anchor_x='right', anchor_y='top', batch=batch)
        self.update()
    def update(self):
        if mode.started:
            self.label.text = ''
        else:
            average = 0.
            total_sessions = 0
            for x in range(len(stats.history) - 20, len(stats.history)):
                if x < 0: continue
                total_sessions += 1
                average += stats.history[x][2]
            if len(stats.history) > 0:
                average /= total_sessions
            str_list = []
            str_list.append('n-back average: ')
            str_list.append(str(round(average, 2)))
            self.label.text = ''.join(str_list)

class TodayLabel:
    def __init__(self):
        self.label = pyglet.text.Label(
            '',
            font_size=10, bold = True,
            color=COLOR_TEXT,
            x=window.width - 10, y=window.height-5,
            anchor_x='right', anchor_y='top', batch=batch)
        self.update()
    def update(self):
        if mode.started:
            self.label.text = ''
        else:
            str_list = []
            str_list.append('Sessions today: ')
            str_list.append(str(stats.sessions_today))
            self.label.text = ''.join(str_list)

class TrialsRemainingLabel:
    def __init__(self):
        self.label = pyglet.text.Label(
            '',
            font_size=12, bold = True,
            color=COLOR_TEXT,
            x=window.width - 10, y=window.height-5,
            anchor_x='right', anchor_y='top', batch=batch)
        self.update()
    def update(self):
        if (not mode.started) or mode.hide_text:
            self.label.text = ''
        else:
            str_list = []
            str_list.append(str(mode.num_trials + mode.back - mode.trial_number))
            str_list.append(' remaining')
            self.label.text = ''.join(str_list)
           
#
# --- END GRAPHICS SECTION ----------------------------------------------
#

# this class stores the raw statistics and history information.
# the information is analyzed by the AnalysisLabel class.
class Stats:
    def __init__(self):
        # set up data variables
        self.initialize_session()
        self.history = []
        self.sessions_today = 0
        
    def initialize_session(self):
        self.session = {}
        self.session['position'] = []
        self.session['color'] = []
        self.session['audio'] = []
        self.session['vis'] = []
        self.session['number'] = []
        self.session['operation'] = []
        
        self.session['position_input'] = []
        self.session['visvis_input'] = []
        self.session['visaudio_input'] = []
        self.session['color_input'] = []
        self.session['audiovis_input'] = []
        self.session['audio_input'] = []
        self.session['arithmetic_input'] = []

    def save_input(self):
        self.session['position'].append(mode.current_position)
        self.session['color'].append(mode.current_color)
        self.session['audio'].append(mode.current_audio)
        self.session['vis'].append(mode.current_vis)
        self.session['number'].append(mode.current_number)
        self.session['operation'].append(mode.current_operation)

        self.session['position_input'].append(mode.position_input)
        self.session['visvis_input'].append(mode.visvis_input)
        self.session['visaudio_input'].append(mode.visaudio_input)
        self.session['color_input'].append(mode.color_input)
        self.session['audiovis_input'].append(mode.audiovis_input)
        self.session['audio_input'].append(mode.audio_input)
        self.session['arithmetic_input'].append(arithmeticAnswerLabel.parse_answer())

    def submit_session(self, percent, category_percents):
        global musicplayer
        global applauseplayer
        self.history.append([mode.session_number, mode.mode, mode.back, percent, mode.manual])
        
        if ATTEMPT_TO_SAVE_STATS:
            try:
                separator = STATS_SEPARATOR
                statsfile_path = os.path.join(get_main_dir(), FOLDER_DATA, STATSFILE)
                statsfile = open(statsfile_path, 'a')
                str_list = []
                str_list.append(strftime("%Y-%m-%d %H:%M:%S"))
                str_list.append(separator)
                if mode.mode == 10: str_list.append('Po')
                elif mode.mode == 11: str_list.append('Au')
                elif mode.mode == 2: str_list.append('D')
                elif mode.mode == 3: str_list.append('T')
                elif mode.mode == 4: str_list.append('DC')
                elif mode.mode == 5: str_list.append('TC')
                elif mode.mode == 6: str_list.append('QC')
                elif mode.mode == 7: str_list.append('A')
                elif mode.mode == 8: str_list.append('DA')
                elif mode.mode == 9: str_list.append('TA')
                #elif mode.mode == 12: str_blist.append('DV')
                #elif mode.mode == 13: str_list.append('M')
                #elif mode.mode == 14: str_list.append('DM')
                #elif mode.mode == 15: str_list.append('TM')
                #elif mode.mode == 16: str_list.append('QM')
                str_list.append(str(mode.back))
                str_list.append('B')
                str_list.append(separator)
                str_list.append(str(percent))
                str_list.append(separator)
                str_list.append(str(mode.mode))
                str_list.append(separator)
                str_list.append(str(mode.back))
                str_list.append(separator)
                str_list.append(str(mode.ticks_per_trial))
                str_list.append(separator)
                str_list.append(str(mode.num_trials + mode.back))
                str_list.append(separator)
                if mode.manual:
                    str_list.append('1')
                else: str_list.append('0')
                str_list.append(separator)
                str_list.append(str(mode.session_number))
                str_list.append(separator)
                str_list.append(str(category_percents['position']))
                str_list.append(separator)
                str_list.append(str(category_percents['audio']))
                str_list.append(separator)
                str_list.append(str(category_percents['color']))
                str_list.append(separator)
                str_list.append(str(category_percents['visvis']))
                str_list.append(separator)
                str_list.append(str(category_percents['visaudio']))
                str_list.append(separator)
                str_list.append(str(category_percents['audiovis']))
                str_list.append(separator)
                str_list.append(str(category_percents['arithmetic']))
                str_list.append('\n')
                statsfile.write(''.join(str_list))
                statsfile.close()
            except:
                str_list = []
                str_list.append('\nError writing to stats file\n')
                str_list.append(os.path.join(get_main_dir(), FOLDER_DATA, STATSFILE))
                str_list.append('\n\n')
                str_list.append('Full text of error:\n\n')
                str_list.append(str(sys.exc_info()))
                str_list.append('\n\nPlease check file and directory permissions.\n')
                print >> sys.stderr, ''.join(str_list)
                sys.exit(1)

        perfect = False        
        awesome = False
        great = False
        good = False
        advance = False
        fallback = False
        
        if not mode.manual:
            if percent >= get_threshold_advance():
                mode.back += 1
                mode.progress = 0
                circles.update()
                if USE_APPLAUSE:
                    applauseplayer = sound[0].play()
                    applauseplayer.volume = SFX_VOLUME
                advance = True
            elif mode.back > 1 and percent < get_threshold_fallback():
                if NOVICE_MODE:
                    mode.back -= 1
                    fallback = True
                else:
                    if mode.progress == THRESHOLD_FALLBACK_SESSIONS - 1:
                        mode.back -= 1
                        fallback = True
                        mode.progress = 0
                        circles.update()
                    else:
                        mode.progress += 1
                        circles.update()
    
            if percent == 100: perfect = True
            elif percent >= get_threshold_advance(): awesome = True
            elif percent >= (get_threshold_advance() + get_threshold_fallback()) // 2: great = True
            elif percent >= get_threshold_fallback(): good = True
            congratsLabel.update(True, advance, fallback, awesome, great, good, perfect)
        
        if mode.manual and not USE_MUSIC_MANUAL:
            return
        
        if USE_MUSIC:
            if percent >= get_threshold_advance() and len(MUSIC_ADVANCE) > 0:
                musicplayer = pyglet.resource.media(random.choice(MUSIC_ADVANCE), streaming = True).play()
                musicplayer.volume = MUSIC_VOLUME
            elif percent >= (get_threshold_advance() + get_threshold_fallback()) // 2 and len(MUSIC_GREAT) > 0:
                musicplayer = pyglet.resource.media(random.choice(MUSIC_GREAT), streaming = True).play()
                musicplayer.volume = MUSIC_VOLUME
            elif percent >= get_threshold_fallback() and len(MUSIC_GOOD) > 0:
                musicplayer = pyglet.resource.media(random.choice(MUSIC_GOOD), streaming = True).play()
                musicplayer.volume = MUSIC_VOLUME
        
    def clear(self):
        self.history = []
        self.sessions_today = 0
        
def test_sounds():
    global applauseplayer
    global musicplayer
    
    musicplayer = pyglet.resource.media(random.choice(MUSIC_GOOD), streaming = True).play()
    musicplayer.volume = MUSIC_VOLUME
    applauseplayer = sound[0].play()
    applauseplayer.volume = SFX_VOLUME
        
def update_all_labels(do_analysis = False):
    updateLabel.update()
    congratsLabel.update()
    if do_analysis:
        analysisLabel.update()
    else:
        analysisLabel.update(skip = True)
    gameModeLabel.update()
    keysListLabel.update()
    pausedLabel.update()
    sessionInfoLabel.update()
    thresholdLabel.update()
    spaceLabel.update()
    chartTitleLabel.update()
    chartLabel.update()
    averageLabel.update()
    todayLabel.update()
    trialsRemainingLabel.update()
   
    update_input_labels()
    
def update_input_labels():
    positionLabel.update()
    colorLabel.update()
    audioLabel.update()
    visvisLabel.update()
    visaudioLabel.update()
    audiovisLabel.update()
    arithmeticAnswerLabel.update()

# this function handles initiation of a new session.
def new_session():
    mode.tick = -3  # give a 1-second delay before displaying first trial
    mode.session_number += 1
    mode.trial_number = 0
    mode.started = True
    mode.paused = False
    circles.update()
    
    # initialize sounds
    choices = []
    #if mode.mode == 13 or mode.mode == 14 or mode.mode == 15 or mode.mode == 16:
        #choices.append('morse')
    #else:
    if USE_LETTERS:
        choices.append('letters')
    if USE_NUMBERS:
        choices.append('numbers')
    if USE_NATO:
        choices.append('nato')
    if USE_PIANO:
        choices.append('piano')
    if USE_MORSE:
        choices.append('morse')
    if len(choices) == 0:
        choices.append('letters')
    mode.sound_mode = random.choice(choices)
    if mode.sound_mode == 'letters':
        visual.set_letters(DEFAULT_LETTERS)
    elif mode.sound_mode == 'numbers':
        numbers = random.sample(numbersound.keys(), 8)
        visual.set_letters(numbers)
        mode.soundlist = []
        for number in numbers:
            mode.soundlist.append(numbersound[number])
    elif mode.sound_mode == 'piano':
        pianos = random.sample(pianosound.keys(), 8)
        visual.set_letters(pianos)
        mode.soundlist = []
        for piano in pianos:
            mode.soundlist.append(pianosound[piano])
    elif mode.sound_mode == 'nato':
        letters = random.sample(natosound.keys(), 8)
        visual.set_letters(letters)
        mode.soundlist = []
        for letter in letters:
            mode.soundlist.append(natosound[letter])
    elif mode.sound_mode == 'morse':
        morses = random.sample(morsesound.keys(), 8)
        visual.set_letters(morses)
        mode.soundlist = []
        for morse in morses:
            mode.soundlist.append(morsesound[morse])
            
    if NOVICE_MODE:
        compute_bt_sequence()
        
    if VARIABLE_NBACK == 1:
        # compute variable n-back sequence using beta distribution
        mode.variable_list = []
        for index in range(0, mode.num_trials):
            mode.variable_list.append(int(random.betavariate(mode.back / 2.0, 1) * mode.back + 1))
    field.crosshair_update()
    reset_input()
    stats.initialize_session()
    update_all_labels()
    pyglet.clock.schedule_interval(fade_out, 0.05)

# this function handles the finish or cancellation of a session.
def end_session(cancelled = False):
    if cancelled:
        mode.session_number -= 1
    if not cancelled:
        stats.sessions_today += 1
    visual.hide()
    mode.started = False
    mode.paused = False
    circles.update()
    field.crosshair_update()
    reset_input()
    if cancelled:
        update_all_labels()
    else:
        update_all_labels(do_analysis = True)
            
# this function causes the key labels along the bottom to revert to their
# "non-pressed" state for a new trial or when returning to the main screen.
def reset_input():
    mode.position_input = False
    mode.color_input = False
    mode.visvis_input = False
    mode.visaudio_input = False
    mode.audiovis_input = False
    mode.audio_input = False
    arithmeticAnswerLabel.reset_input()
    update_input_labels()

# this handles the computation of a round with exactly 6 position and 6 audio matches
def compute_bt_sequence():
    bt_sequence = []
    bt_sequence.append([])
    bt_sequence.append([])    
    for x in range(0, mode.num_trials + mode.back):
        bt_sequence[0].append(0)
        bt_sequence[1].append(0)
    
    for x in range(0, mode.back):
        bt_sequence[0][x] = random.randint(1, 8)
        bt_sequence[1][x] = random.randint(1, 8)
        
    position = 0
    audio = 0
    both = 0
    
    # brute force it
    while True:
        position = 0
        for x in range(mode.back, mode.num_trials + mode.back):
            bt_sequence[0][x] = random.randint(1, 8)
            if bt_sequence[0][x] == bt_sequence[0][x - mode.back]:
                position += 1
        if position != 6:
            continue
        while True:
            audio = 0
            for x in range(mode.back, mode.num_trials + mode.back):
                bt_sequence[1][x] = random.randint(1, 8)
                if bt_sequence[1][x] == bt_sequence[1][x - mode.back]:
                    audio += 1
            if audio == 6:
                break
        both = 0
        for x in range(mode.back, mode.num_trials + mode.back):
            if bt_sequence[0][x] == bt_sequence[0][x - mode.back] and bt_sequence[1][x] == bt_sequence[1][x - mode.back]:
                both += 1
        if both == 2:
            break
    
    mode.bt_sequence = bt_sequence
    
# responsible for the random generation of each new stimulus (audio, color, position)
def generate_stimulus():
    # first, randomly generate all stimuli
    mode.current_position = random.randint(1, 8)
    mode.current_color = random.randint(1, 8)
    mode.current_vis = random.randint(1, 8)
    mode.current_audio = random.randint(1, 8)
    
    # treat arithmetic specially
    operations = []
    if ARITHMETIC_USE_ADDITION: operations.append('add')
    if ARITHMETIC_USE_SUBTRACTION: operations.append('subtract')
    if ARITHMETIC_USE_MULTIPLICATION: operations.append('multiply')
    if ARITHMETIC_USE_DIVISION: operations.append('divide')
    mode.current_operation = random.choice(operations)
    
    if ARITHMETIC_USE_NEGATIVES:
        min_number = 0 - ARITHMETIC_MAX_NUMBER
    else:
        min_number = 0
    max_number = ARITHMETIC_MAX_NUMBER
    
    if mode.current_operation == 'divide' and (mode.mode == 7 or mode.mode == 8 or mode.mode == 9):
        if len(stats.session['position']) >= mode.back:
            number_nback = stats.session['number'][mode.trial_number - mode.back - 1]
            possibilities = []
            for x in range(min_number, max_number + 1):
                if x == 0:
                    continue
                if number_nback % x == 0:
                    possibilities.append(x)
                    continue
                frac = Decimal(abs(number_nback)) / Decimal(abs(x))
                frac -= frac.quantize(0)
                for number in ARITHMETIC_ACCEPTABLE_DECIMALS:
                    if frac == Decimal(number):
                        possibilities.append(x)
            mode.current_number = random.choice(possibilities)
        else:
            mode.current_number = random.randint(min_number, max_number)
            while mode.current_number == 0:
                mode.current_number = random.randint(min_number, max_number)
    else:
        mode.current_number = random.randint(min_number, max_number)
    
    # force a match?
    if mode.mode != 7 and mode.trial_number > mode.back and random.random() < CHANCE_OF_GUARANTEED_MATCH:
        # A match of a randomly chosen input type is guaranteed this trial.
        # input type list:
        
        input_types = []
        if mode.mode == 10:
            input_types.append('position')
        elif mode.mode == 11: # or mode.mode == 13:
            input_types.append('audio')
        elif mode.mode == 2:
            input_types.append('position')
            input_types.append('audio')
        elif mode.mode == 3:
            input_types.append('position')
            input_types.append('color')
            input_types.append('audio')
        elif mode.mode == 4: # or mode.mode == 14:
            input_types.append('visvis')
            input_types.append('visaudio')
            input_types.append('audiovis')
            input_types.append('audio')
        elif mode.mode == 5: # or mode.mode == 15:
            input_types.append('position')
            input_types.append('visvis')
            input_types.append('visaudio')
            input_types.append('audiovis')
            input_types.append('audio')
        elif mode.mode == 6: # or mode.mode == 16:
            input_types.append('position')
            input_types.append('color')
            input_types.append('visvis')
            input_types.append('visaudio')
            input_types.append('audiovis')
            input_types.append('audio')
        elif mode.mode == 8:
            input_types.append('position')
        elif mode.mode == 9:
            input_types.append('position')
            input_types.append('color')
        #elif mode.mode == 12:
            #input_types.append('position')
            #input_types.append('audio')

        choice = random.choice(input_types)
        if VARIABLE_NBACK == 1:
            nback_trial = mode.trial_number - mode.variable_list[mode.trial_number - mode.back - 1] - 1
        else:
            nback_trial = mode.trial_number - mode.back - 1

        if choice == 'position':
            mode.current_position = stats.session['position'][nback_trial]
        elif choice == 'color':
            mode.current_color = stats.session['color'][nback_trial]
        elif choice == 'visvis':
            mode.current_vis = stats.session['vis'][nback_trial]
        elif choice == 'visaudio':
            mode.current_vis = stats.session['audio'][nback_trial]
        elif choice == 'audiovis':
            mode.current_audio = stats.session['vis'][nback_trial]
        elif choice == 'audio':
            mode.current_audio = stats.session['audio'][nback_trial]

    # set static stimuli according to mode.
    # default position is 0 (center)
    # default color is 1 (red) or 2 (black)
    # default vis is 0 (square)
    # audio is never static so it doesn't have a default.
    if mode.mode == 10:
        mode.current_color = VISUAL_COLOR
        mode.current_vis = 0
    elif mode.mode == 11: # or mode.mode == 13:
        mode.current_color = VISUAL_COLOR
        mode.current_vis = 0
        mode.current_position = 0
    elif mode.mode == 2:
        mode.current_color = VISUAL_COLOR
        mode.current_vis = 0
    elif mode.mode == 3:
        mode.current_vis = 0
    elif mode.mode == 4: # or mode.mode == 14:
        mode.current_position = 0
        mode.current_color = VISUAL_COLOR
    elif mode.mode == 5: # or mode.mode == 15:
        mode.current_color = VISUAL_COLOR
    elif mode.mode == 6: # or mode.mode == 16:
        pass
    elif mode.mode == 7:
        mode.current_position = 0
        mode.current_color = VISUAL_COLOR
    elif mode.mode == 8:
        mode.current_color = VISUAL_COLOR
    elif mode.mode == 9:
        pass
    #elif mode.mode == 12:
        #mode.current_color = VISUAL_COLOR
        #mode.current_vis = 0

    # in novice mode, set using the predetermined sequence.
    if NOVICE_MODE:
        mode.current_position = mode.bt_sequence[0][mode.trial_number - 1]
        mode.current_audio = mode.bt_sequence[1][mode.trial_number - 1]
    
    # initiate the chosen stimuli.
    # mode.current_audio is a number from 1 to 8.
    if (mode.mode == 7 or mode.mode == 8 or mode.mode == 9) and mode.trial_number > mode.back:
        if mode.current_operation == 'add':
            sound[9].play()
        elif mode.current_operation == 'subtract':
            sound[10].play()
        elif mode.current_operation == 'multiply':
            sound[11].play()
        elif mode.current_operation == 'divide':
            sound[12].play()
    elif (mode.mode >= 2 and mode.mode <= 6) or (mode.mode >= 11 and mode.mode <= 11):
        if mode.sound_mode == 'letters':
            sound[mode.current_audio].play()
        elif mode.sound_mode == 'numbers' or mode.sound_mode == 'nato' or mode.sound_mode == 'piano' or mode.sound_mode == 'morse':
            mode.soundlist[mode.current_audio - 1].play()
            
    if VARIABLE_NBACK == 1 and mode.trial_number > mode.back:
        variable = mode.variable_list[mode.trial_number - 1 - mode.back]
    else:
        variable = 0
    visual.spawn(mode.current_position, mode.current_color, mode.current_vis, mode.current_number, mode.current_operation, variable)

def toggle_manual_mode():
    if mode.manual:
        mode.manual = False
    else:
        mode.manual = True
    
    if not mode.manual:
        mode.enforce_standard_mode()
        
    update_all_labels()


# there are 3 event loops:
#   on_key_press: listens to the keyboard and acts when certain keys are pressed
#   on_draw:      draws everything to the screen something like 60 times per second
#   update(dt):   the session timer loop which controls the game during the sessions.
#                 Runs once every quarter-second.
#
# --- BEGIN EVENT LOOP SECTION ----------------------------------------------
#

# this is where the keyboard keys are defined.
@window.event
def on_key_press(symbol, modifiers):
    global USE_LETTERS
    global USE_NUMBERS
    global USE_NATO
    global USE_PIANO
    global USE_MORSE
    global VARIABLE_NBACK
    
    if symbol == key.D and (modifiers & key.MOD_CTRL):
        dump_pyglet_info()
        
    elif mode.title_screen and not mode.draw_graph and not mode.game_select and not mode.sound_select:
        if symbol == key.ESCAPE or symbol == key.X:
            window.on_close()
            
        elif symbol == key.SPACE:
            mode.title_screen = False
            
        elif symbol == key.C and not NOVICE_MODE:
            mode.game_select = True
                                    
        elif symbol == key.H:
            webbrowser.open_new_tab(WEB_TUTORIAL)
                
        elif symbol == key.G:
            sound_stop()
            graph.parse_stats()
            graph.graph = mode.mode
            mode.draw_graph = True
            
        elif symbol == key.S and not NOVICE_MODE:
            mode.sound_select = True
    
        elif symbol == key.F:
            webbrowser.open_new_tab(WEB_FORUM)

    elif mode.draw_graph:
        if symbol == key.ESCAPE or symbol == key.G or symbol == key.X:
            mode.draw_graph = False
            
        elif symbol == key.E and (modifiers & key.MOD_CTRL):
            graph.export_data()

        elif symbol == key.N:
            graph.next_mode()
            
    elif mode.game_select:
        def execute_mode_change():
            if not mode.manual:
                mode.enforce_standard_mode()
            update_all_labels()
            mode.progress = 0
            circles.update()
            mode.game_select = False
            mode.title_screen = False
        
        if symbol == key.ESCAPE or symbol == key.C or symbol == key.X:
            mode.game_select = False
        elif symbol == key._0 or symbol == key.NUM_0:
            mode.mode = 10
            execute_mode_change()
        elif symbol == key._1 or symbol == key.NUM_1:
            mode.mode = 11
            execute_mode_change()
        elif symbol == key._2 or symbol == key.NUM_2:
            mode.mode = 2
            execute_mode_change()
        elif symbol == key._3 or symbol == key.NUM_3:
            mode.mode = 3
            execute_mode_change()
        elif symbol == key._4 or symbol == key.NUM_4:
            mode.mode = 4
            execute_mode_change()
        elif symbol == key._5 or symbol == key.NUM_5:
            mode.mode = 5
            execute_mode_change()
        elif symbol == key._6 or symbol == key.NUM_6:
            mode.mode = 6
            execute_mode_change()
        elif symbol == key._7 or symbol == key.NUM_7:
            mode.mode = 7
            execute_mode_change()
        elif symbol == key._8 or symbol == key.NUM_8:
            mode.mode = 8
            execute_mode_change()
        elif symbol == key._9 or symbol == key.NUM_9:
            mode.mode = 9
            execute_mode_change()
        #elif symbol == key.A:
            #mode.mode = 12
            #execute_mode_change()
        #elif symbol == key.S:
            #mode.mode = 13
            #execute_mode_change()
        #elif symbol == key.D:
            #mode.mode = 14
            #execute_mode_change()
        #elif symbol == key.F:
            #mode.mode = 15
            #execute_mode_change()
        #elif symbol == key.G:
            #mode.mode = 16
            #execute_mode_change()
            
    elif mode.sound_select:
        if symbol == key.ESCAPE or symbol == key.S or symbol == key.X or symbol == key.SPACE:
            mode.sound_select = False
            
        elif symbol == key._1 or symbol == key.NUM_1:
            if USE_LETTERS:
                USE_LETTERS = False
            else: USE_LETTERS = True
        elif symbol == key._2 or symbol == key.NUM_2:
            if USE_NUMBERS:
                USE_NUMBERS = False
            else: USE_NUMBERS = True
        elif symbol == key._3 or symbol == key.NUM_3:
            if USE_NATO:
                USE_NATO = False
            else: USE_NATO = True
        elif symbol == key._4 or symbol == key.NUM_4:
            if USE_PIANO:
                USE_PIANO = False
            else: USE_PIANO = True
        elif symbol == key._5 or symbol == key.NUM_5:
            if USE_MORSE:
                USE_MORSE = False
            else: USE_MORSE = True
            keysListLabel.update()
    
    elif not mode.started:
        
        if symbol == key.ESCAPE or symbol == key.X:
            mode.title_screen = True
        
        elif symbol == key.SPACE:
            new_session()
                        
        elif symbol == key.F1 and mode.manual:
            if mode.back > 1:
                mode.back -= 1
                gameModeLabel.flash()
                spaceLabel.update()
                sessionInfoLabel.update()
                
        elif symbol == key.F2 and mode.manual:
            mode.back += 1
            gameModeLabel.flash()
            spaceLabel.update()
            sessionInfoLabel.update()

        elif symbol == key.F3 and mode.num_trials > 5 and mode.manual:
            mode.num_trials -= 5
            sessionInfoLabel.flash()

        elif symbol == key.F4 and mode.manual:
            mode.num_trials += 5
            sessionInfoLabel.flash()            
            
            
        elif symbol == key.F5 and mode.manual:
            if mode.ticks_per_trial < TICKS_MAX:
                mode.ticks_per_trial += 1
                sessionInfoLabel.flash()
                        
        elif symbol == key.F6 and mode.manual:
            if mode.ticks_per_trial > TICKS_MIN:
                mode.ticks_per_trial -= 1
                sessionInfoLabel.flash()

        elif symbol == key.C:
            if NOVICE_MODE:
                noviceWarningLabel.show()
                return
            mode.game_select = True
        elif symbol == key.S:
            if NOVICE_MODE:
                noviceWarningLabel.show()
                return
            mode.sound_select = True
            
        elif symbol == key.V and not NOVICE_MODE:
            if VARIABLE_NBACK == 1:
                VARIABLE_NBACK = 0
            else: VARIABLE_NBACK = 1
            gameModeLabel.flash()
            spaceLabel.update()

        elif symbol == key.W:
            webbrowser.open_new_tab(WEB_SITE)
            if update_available:
                window.on_close()
            
        elif symbol == key.M:
            toggle_manual_mode()
            update_all_labels()
            mode.progress = 0
            circles.update()

        elif symbol == key.H:
            webbrowser.open_new_tab(WEB_TUTORIAL)
            
        elif symbol == key.J and USE_MORSE:
            webbrowser.open_new_tab(WEB_MORSE)
                
        elif symbol == key.C and (modifiers & key.MOD_CTRL):
            stats.clear()
            chartLabel.update()
            averageLabel.update()
            todayLabel.update()
            mode.progress = 0
            circles.update()
            
        elif symbol == key.G:
            sound_stop()
            graph.parse_stats()
            graph.graph = mode.mode
            mode.draw_graph = True
                        
    # these are the keys during a running session.
    elif mode.started:            
        if symbol == key.ESCAPE or symbol == key.X:
            end_session(cancelled = True)
            
        elif symbol == key.P:
            if mode.paused: 
                mode.paused = False
                pausedLabel.update()
                field.crosshair_update()
            else:
                mode.paused = True
                pausedLabel.update()
                field.crosshair_update()
                
        elif symbol == key.F8:
            if mode.hide_text:
                mode.hide_text = False
            else: mode.hide_text = True
            update_all_labels()
                
        elif mode.tick != 0 and mode.trial_number > 0:
            if mode.mode == 7 or mode.mode == 8 or mode.mode == 9:
                if symbol == key.BACKSPACE or symbol == key.DELETE:
                    arithmeticAnswerLabel.reset_input()
                elif symbol == key.MINUS or symbol == key.NUM_SUBTRACT:
                    arithmeticAnswerLabel.input('-')
                elif symbol == key.PERIOD or symbol == key.NUM_DECIMAL:
                    arithmeticAnswerLabel.input('.')
                elif symbol == key._0 or symbol == key.NUM_0:
                    arithmeticAnswerLabel.input('0')
                elif symbol == key._1 or symbol == key.NUM_1:
                    arithmeticAnswerLabel.input('1')
                elif symbol == key._2 or symbol == key.NUM_2:
                    arithmeticAnswerLabel.input('2')
                elif symbol == key._3 or symbol == key.NUM_3:
                    arithmeticAnswerLabel.input('3')
                elif symbol == key._4 or symbol == key.NUM_4:
                    arithmeticAnswerLabel.input('4')
                elif symbol == key._5 or symbol == key.NUM_5:
                    arithmeticAnswerLabel.input('5')
                elif symbol == key._6 or symbol == key.NUM_6:
                    arithmeticAnswerLabel.input('6')
                elif symbol == key._7 or symbol == key.NUM_7:
                    arithmeticAnswerLabel.input('7')
                elif symbol == key._8 or symbol == key.NUM_8:
                    arithmeticAnswerLabel.input('8')
                elif symbol == key._9 or symbol == key.NUM_9:
                    arithmeticAnswerLabel.input('9')
                    
            if symbol == KEY_POSITION:
                mode.position_input = True
                positionLabel.update()
                
            elif symbol == KEY_VISVIS:
                mode.visvis_input = True
                visvisLabel.update()
                
            elif symbol == KEY_VISAUDIO:
                mode.visaudio_input = True
                visaudioLabel.update()
                
            elif symbol == KEY_COLOR:
                mode.color_input = True
                colorLabel.update()
                
            elif symbol == KEY_AUDIOVIS:
                mode.audiovis_input = True
                audiovisLabel.update()
                
            elif symbol == KEY_AUDIO:
                mode.audio_input = True
                audioLabel.update()
            
# the loop where everything is drawn on the screen.
@window.event
def on_draw():
    window.clear()
    if mode.draw_graph:
        graph.draw()
    elif mode.game_select:
        gameSelect.draw()
    elif mode.sound_select:
        soundSelect.draw()
    elif mode.title_screen:
        brain_graphic.draw()
        titleMessageLabel.draw()
        titleKeysLabel.draw()
    else:
        batch.draw()
        if not mode.started:
            brain_icon.draw()
            logoUpperLabel.draw()
            logoLowerLabel.draw()

# the event timer loop. Runs every 1/4 second. This loop controls the session
# game logic.
# During each trial the tick goes from 1 to ticks_per_trial-1 then back to 0.
# tick = 1: Input from the last trial is saved. Input is reset.
#             A new square appears and the sound cue plays. 
# tick = 3: the square disappears.
# tick = ticks_per_trial - 1: tick is reset to 0.
# tick = 1: etc.
def update(dt):
    if mode.started and not mode.paused: # only run the timer during a game
        mode.tick += 1
        if mode.tick == 1:
            mode.show_missed = False
            if mode.trial_number > 0:
                stats.save_input()
            mode.trial_number += 1
            trialsRemainingLabel.update()
            if mode.trial_number > mode.num_trials + mode.back:
                end_session()
            else: generate_stimulus()
            reset_input()
        if mode.tick == mode.ticks_per_trial:
            mode.tick = 0
            mode.show_missed = True
            update_input_labels()
        if mode.tick == 3:
            visual.hide()
pyglet.clock.schedule_interval(update, TICK_DURATION)

angle = 0
def pulsate(dt):
    global angle
    if mode.started: return
    if not window.visible: return
    angle += 15
    if angle == 360:
        angle = 0
    r = 0
    g = 0
    b = 191 + min(64, int(80 * math.cos(math.radians(angle))))
    spaceLabel.label.color = (r, g, b, 255)
#pyglet.clock.schedule_interval(pulsate, 1/20.)
        
#
# --- END EVENT LOOP SECTION ----------------------------------------------
#


batch = pyglet.graphics.Batch()

try: 
    test_polygon = batch.add(4, pyglet.gl.GL_QUADS, None, ('v2i', (
        100, 100,
        100, 200,
        200, 200,
        200, 100)),
              ('c3B', (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)))
    test_polygon.delete()
except:
    str_list = []
    str_list.append('\nError creating test polygon. Full text of error:\n')
    str_list.append(str(sys.exc_info()))
    print >> sys.stderr, ''.join(str_list)
    sys.exit(1)

# Instantiate the classes
mode = Mode()
field = Field()
visual = Visual()
stats = Stats()
graph = Graph()
circles = Circles()

gameSelect = GameSelect()
soundSelect = SoundSelect()
updateLabel = UpdateLabel()
gameModeLabel = GameModeLabel()
noviceWarningLabel = NoviceWarningLabel()
keysListLabel = KeysListLabel()
logoUpperLabel = LogoUpperLabel()
logoLowerLabel = LogoLowerLabel()
titleMessageLabel = TitleMessageLabel()
titleKeysLabel = TitleKeysLabel()
pausedLabel = PausedLabel()
congratsLabel = CongratsLabel()
sessionInfoLabel = SessionInfoLabel()
thresholdLabel = ThresholdLabel()
spaceLabel = SpaceLabel()
analysisLabel = AnalysisLabel()
chartTitleLabel = ChartTitleLabel()
chartLabel = ChartLabel()
averageLabel = AverageLabel()
todayLabel = TodayLabel()
trialsRemainingLabel = TrialsRemainingLabel()

arithmeticAnswerLabel = ArithmeticAnswerLabel()
positionLabel = PositionLabel()
colorLabel = ColorLabel()
audioLabel = AudioLabel()
visvisLabel = VisvisLabel()
visaudioLabel = VisaudioLabel()
audiovisLabel = AudiovisLabel()

update_all_labels()

# Initialize brain sprite
brain_icon = pyglet.sprite.Sprite(pyglet.resource.image(IMAGES[0]))
brain_icon.set_position(field.center_x - brain_icon.width//2,
                           field.center_y - brain_icon.height//2)
brain_graphic = pyglet.sprite.Sprite(pyglet.resource.image(IMAGES[9]))
brain_graphic.set_position(field.center_x - brain_graphic.width//2,
                           field.center_y - brain_graphic.height//2 + 40)

# start the event loops!
if __name__ == '__main__':
    pyglet.app.run()

# nothing below the line "pyglet.app.run()" will be executed until the
# window is closed or ESC is pressed.

