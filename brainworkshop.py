#!/usr/bin/env python
# This Python file uses the following encoding: utf-8
#------------------------------------------------------------------------------
# Brain Workshop: a Dual N-Back game in Python
#
# This is a fork of the popular Brain Workshop game. Development on the original
# has not happened for many years. The fork is available at:
# https://github.com/brain-workshop/brainworkshop
#
# Tutorial, installation instructions & links to the dual n-back community
# are available at the original Brain Workshop web site:
#
#       http://brainworkshop.net/
#
# Also see Readme.txt.
#
# Copyright (C) 2009-2011: Paul Hoskinson (plhosk@gmail.com)
# Copyright (C) 2017-2018: Samantha McVey (samantham@posteo.net)
# SPDX-License-Identifier: GPL-2.0-or-later
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not see https://www.gnu.org/licenses/gpl-2.0.html
#------------------------------------------------------------------------------
# Use python3 style division for consistency
from __future__ import division
VERSION = '5.0'
def debug_msg(msg):
    if DEBUG:
        if isinstance(msg, Exception):
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print('debug: %s Line %i' % (str(msg), exc_tb.tb_lineno))
        else:
            print('debug: %s' % str(msg))
def error_msg(msg, e = None):
    if DEBUG and e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print("ERROR: %s\n\t%s Line %i" % (msg, e, exc_tb.tb_lineno))
    else:
        print("ERROR: %s" % msg)
def get_argv(arg):
    if arg in sys.argv:
        index = sys.argv.index(arg)
        if index + 1 < len(sys.argv):
            return sys.argv[index + 1]
        else:
            error_msg("Expected an argument following %s" % arg)
            exit(1)

import random, os, sys, socket, webbrowser, time, math, traceback, datetime, errno
if sys.version_info >= (3,0):
    import urllib.request, configparser as ConfigParser
    from io import StringIO
    import pickle
else:
    import urllib2 as urllib, ConfigParser, StringIO
    import cPickle as pickle

from decimal import Decimal
from time import strftime
from datetime import date
import gettext

if sys.version_info >= (3,0):
    # TODO check if this is right
    gettext.install('messages', localedir='res/i18n')
else:
    gettext.install('messages', localedir='res/i18n', unicode=True)

# Clinical mode?  Clinical mode sets cfg.JAEGGI_MODE = True, enforces a minimal user
# interface, and saves results into a binary file (default 'logfile.dat') which
# should be more difficult to tamper with.
CLINICAL_MODE = False

# Internal static options not available in config file.
CONFIG_OVERWRITE_IF_OLDER_THAN = '4.8'
NOVBO = True
VSYNC = False
DEBUG = False
FOLDER_RES = 'res'
FOLDER_DATA = 'data'
CONFIGFILE = 'config.ini'
STATS_BINARY = 'logfile.dat'
USER = 'default'
#CHARTFILE = {2:'chart-02-dnb.txt', 3:'chart-03-tnb.txt', 4:'chart-04-dlnb.txt', 5:'chart-05-tlnb.txt',
             #6:'chart-06-qlnb.txt',7:'chart-07-anb.txt', 8:'chart-08-danb.txt', 9:'chart-09-tanb.txt',
             #10:'chart-10-ponb.txt', 11:'chart-11-aunb.txt'}
ATTEMPT_TO_SAVE_STATS = True
STATS_SEPARATOR = ','
WEB_SITE     = 'http://brainworkshop.net/'
WEB_TUTORIAL = 'http://brainworkshop.net/tutorial.html'
CLINICAL_TUTORIAL = WEB_TUTORIAL # FIXME: Add tutorial catered to clinical trials
WEB_DONATE          = 'http://brainworkshop.net/donate.html'
WEB_VERSION_CHECK   = 'http://brainworkshop.net/version.txt'
WEB_PYGLET_DOWNLOAD = 'http://pyglet.org'
WEB_FORUM           = 'https://groups.google.com/group/brain-training'
WEB_MORSE           = 'https://en.wikipedia.org/wiki/Morse_code'
TIMEOUT_SILENT =  3
TICKS_MIN      =  3
TICKS_MAX      = 50
TICK_DURATION  =  0.1
DEFAULT_WINDOW_WIDTH  = 912
DEFAULT_WINDOW_HEIGHT = 684
preventMusicSkipping  = True

def from_width_center(offset):
    return int( (window.width/2) + offset * (window.width / DEFAULT_WINDOW_WIDTH) )
def from_height_center(offset):
    return int( (window.height/2) + offset * (window.height / DEFAULT_WINDOW_HEIGHT) )
def width_center():
    return int(window.width/2)
def height_center():
    return int(window.height/2)

def from_top_edge(from_edge):
    return int(window.height - (from_edge * window.height/DEFAULT_WINDOW_HEIGHT))

def from_bottom_edge(from_edge):
    return int(from_edge * (window.height/DEFAULT_WINDOW_HEIGHT))

def from_right_edge(from_edge):
    return int(window.width - (from_edge * window.width/DEFAULT_WINDOW_WIDTH))

def from_left_edge(from_edge):
    return int(from_edge * window.width/DEFAULT_WINDOW_WIDTH)

def scale_to_width(fraction):
    return int(fraction * window.width/DEFAULT_WINDOW_WIDTH)

def scale_to_height(fraction):
    return int(fraction * window.height/DEFAULT_WINDOW_HEIGHT)

def calc_fontsize(size):
    return size * (window.height/DEFAULT_WINDOW_HEIGHT)
def calc_dpi(size = 100):
    return int(size * ((window.width + window.height)/(DEFAULT_WINDOW_WIDTH + DEFAULT_WINDOW_HEIGHT)))

def get_pyglet_media_Player():
    try:
        my_player = pyglet.media.Player()
    except Exception as e:
        debug_msg(e)
        my_player = pyglet.media.ManagedSoundPlayer()
    return my_player

# some functions to assist in path determination
def main_is_frozen():
    return hasattr(sys, "frozen") # py2exe
def get_main_dir():
    if main_is_frozen():
        return os.path.dirname(sys.executable)
    return sys.path[0]

def get_settings_path(name):
    '''Get a directory to save user preferences.
    Copied from pyglet.resource so we don't have to load that module
    (which recursively indexes . on loading -- wtf?).'''
    if sys.platform in ('cygwin', 'win32'):
        if 'APPDATA' in os.environ:
            return os.path.join(os.environ['APPDATA'], name)
        else:
            return os.path.expanduser('~/%s' % name)
    elif sys.platform == 'darwin':
        return os.path.expanduser('~/Library/Application Support/%s' % name)
    else: # on *nix, we want it to be lowercase and without spaces (~/.brainworkshop/data)
        return os.path.expanduser('~/.%s' % (name.lower().replace(' ', '')))

def get_data_dir():
    rtrn = get_argv('--datadir')
    if rtrn:
        return rtrn
    else:
        return os.path.join(get_settings_path('Brain Workshop'), FOLDER_DATA)
def get_res_dir():
    rtrn = get_argv('--resdir')
    if rtrn:
        return rtrn
    else:
        return os.path.join(get_main_dir(), FOLDER_RES)
def edit_config_ini():
    if sys.platform == 'win32':
        cmd = 'notepad'
    elif sys.platform == 'darwin':
        cmd = 'open'
    else:
        cmd = 'xdg-open'
    print(cmd + ' "' + os.path.join(get_data_dir(), CONFIGFILE) + '"')
    window.on_close()
    import subprocess
    subprocess.call((cmd + ' "' + os.path.join(get_data_dir(), CONFIGFILE) + '"'), shell=True)
    sys.exit(0)

def quit_with_error(message='', postmessage='', quit=True, trace=True):
    if message:
        sys.stderr.write(message + '\n')
    if trace:
        sys.stderr.write(_("Full text of error:\n"))
        traceback.print_exc()
    if postmessage:
        sys.stderr.write('\n\n' + postmessage)
    if quit:
        sys.exit(1)

CONFIGFILE_DEFAULT_CONTENTS = """
######################################################################
# Brain Workshop configuration file
# generated by Brain Workshop """ + VERSION + """
#
# To change configuration options:
#   1. Edit this file as desired,
#   2. Save the file,
#   3. Launch Brain Workshop to see the changes.
#
# Every line beginning with # is ignored by the program.
#
# Please see the Brain Workshop web site for more information:
#       http://brainworkshop.net
#
# The configuration options begin below.
######################################################################

[DEFAULT]

# Jaeggi-style interface with default scoring model?
# Choose either this option or JAEGGI_MODE but not both.
# This mode allows access to Manual mode, the extra sound sets, and the
# additional game modes of Brain Workshop while presenting the game in
# the more challenging Jaeggi-style interface featured in the original study.
# With the default BW sequence generation model, the visual and auditory
# sequences are more randomized and unpredictable than they are in Jaeggi
# mode.  The only effect of this option is to set the following options:
#   ANIMATE_SQUARES = False, OLD_STYLE_SQUARES = True,
#   OLD_STYLE_SHARP_CORNERS = True, SHOW_FEEDBACK = False,
#   GRIDLINES = False, CROSSHAIRS = True, BLACK_BACKGROUND = True,
#   WINDOW_FULLSCREEN = True, HIDE_TEXT = True, FIELD_EXPAND = True
# Default: False
JAEGGI_INTERFACE_DEFAULT_SCORING = False

# Jaeggi mode?
# Choose either this option or JAEGGI_INTERFACE_DEFAULT_SCORING but not both.
# This mode emulates the scoring model used in the original study protocol.
# It counts non-matches with no inputs as correct (instead of ignoring them).
# It also forces 4 visual matches, 4 auditory matches, and 2 simultaneous
# matches per session, resulting in less randomized and more predictable
# sequences than in the default BW sequence generation model.
# Different thresholds are used to reflect the modified scoring system
# (see below).  Access to Manual mode, additional game modes and sound sets
# is disabled in Jaeggi mode.
# Default: False
JAEGGI_MODE = False

# The default BW scoring system uses the following formula:
#     score = TP / (TP + FP + FN)
# where TP is a true positive response, FN is a false negative, etc.  All
# stimulus modalities are summed together for this formula.
# The Jaeggi mode scoring system scores uses the following formula:
#     score = (TP + TN) / (TP + TN + FP + FN)
# Each modality is scored separately, and the score for the whole session
# is equal to the lowest score of any modality.
# Default: False
JAEGGI_SCORING = False

# In Jaeggi Mode, adjust the default appearance and sounds of Brain Workshop
# to emulate the original software used in the study?
# If this is enabled, the following options will be set:
#    AUDIO1_SETS = ['letters'],  ANIMATE_SQUARES = False,
#    OLD_STYLE_SQUARES = True, OLD_STYLE_SHARP_CORNERS = True,
#    SHOW_FEEDBACK = False, GRIDLINES = False, CROSSHAIRS = True
# (note: this option only takes effect if JAEGGI_MODE is set to True)
# Default: True
JAEGGI_FORCE_OPTIONS = True

# In Jaeggi Mode, further adjust the appearance to match the original
# software as closely as possible?
# If this is enabled, the following options will be set:
#    BLACK_BACKGROUND = True, WINDOW_FULLSCREEN = True,
#    HIDE_TEXT = True, FIELD_EXPAND = True
# (note: this option only takes effect if JAEGGI_MODE is set to True)
# Default: True
JAEGGI_FORCE_OPTIONS_ADDITIONAL = True

# Allow Mouse to be used for input?
# Only for dual n-back. Automatically disabled in JAEGGI_MODE.
ENABLE_MOUSE = True

# Background color: True = black, False = white.
# Default: False
BLACK_BACKGROUND = False

# Begin in full screen mode?
# Setting this to False will begin in windowed mode.
# Default: False
WINDOW_FULLSCREEN = False

# Window size in windowed mode.
# Minimum recommended values: width = 800, height = 600
WINDOW_WIDTH = 912
WINDOW_HEIGHT = 684

# Skip title screen?
SKIP_TITLE_SCREEN = False

# Display feedback of correct/incorrect input?
# Default: True
SHOW_FEEDBACK = True

# Hide text during game? (this can be toggled in-game by pressing F8)
# Default: False
HIDE_TEXT = False

# Expand the field (squares) to fill the entire height of the screen?
# Note: this should only be used with HIDE_TEXT = True.
FIELD_EXPAND = False

# Show grid lines and crosshairs?
GRIDLINES = True
CROSSHAIRS = True

# Set the color of the square in non-Color N-Back modes.
# This also affects Dual Combination N-Back and Arithmetic N-Back.
# 1 = blue, 2 = cyan, 3 = green, 4 = grey,
# 5 = magenta, 6 = red, 7 = white, 8 = yellow
# Default: [1, 3, 8, 6]
VISUAL_COLORS = [1, 3, 8, 6]

# Specify image sets here. This is a list of subfolders in the res\sprites\
# folder which may be selected in Image mode.
# The first item in the list is the default which is loaded on startup.
IMAGE_SETS = ['polygons-basic', 'national-park-service', 'pentominoes',
              'tetrominoes-fixed', 'cartoon-faces']

# This selects which sounds to use for audio n-back tasks.
# Select any combination of letters, numbers, the NATO Phonetic Alphabet
# (Alpha, Bravo, Charlie, etc), the C scale on piano, and morse code.
# AUDIO1_SETS = ['letters', 'morse', 'nato', 'numbers', 'piano']
AUDIO1_SETS = ['letters']

# Sound configuration for the Dual Audio (A-A) task.
# Possible values for CHANNEL_AUDIO1 and CHANNEL_AUDIO2:
#    'left' 'right' 'center'
AUDIO2_SETS = ['letters']
CHANNEL_AUDIO1 = 'left'
CHANNEL_AUDIO2 = 'right'

# In multiple-stimulus modes, more than one visual stimulus is presented at
# the same time.  Each of the simultaneous visual stimuli has an ID number
# associated with either its color or its image.  Which should we use, by
# default?
# Options: 'color' or 'image'
MULTI_MODE = 'color'

# Animate squares?
ANIMATE_SQUARES = False

# Use the flat, single-color squares like in versions prior to 4.1?
# Also, use sharp corners or rounded corners?
OLD_STYLE_SQUARES = False
OLD_STYLE_SHARP_CORNERS = False

# Start in Manual mode?
# If this is False, the game will start in standard mode.
# Default: False
MANUAL = False
USE_MUSIC_MANUAL = False

# Starting game mode.
# Possible values:
#  2:'Dual',
#  3:'P-C-A',
#  4:'Dual Combination',
#  5:'Tri Combination',
#  6:'Quad Combination',
#  7:'Arithmetic',
#  8:'Dual Arithmetic',
#  9:'Triple Arithmetic',
#  10:'Position',
#  11:'Sound',
#  20:'P-C',
#  21:'P-I',
#  22:'C-A',
#  23:'I-A',
#  24:'C-I',
#  25:'P-C-I',
#  26:'P-I-A',
#  27:'C-I-A',
#  28:'Quad',
#  100:'A-A',
#  101:'P-A-A',
#  102:'C-A-A',
#  103:'I-A-A',
#  104:'P-C-A-A',
#  105:'P-I-A-A',
#  106:'C-I-A-A',
#  107:'P-C-I-A-A' (Pentuple)
#  128+x:  Crab mode
#  256+x:  Double mode (can be combined with crab mode)
#  512+x:  Triple mode
#  768+x:  Quadruple mode

# Note: if JAEGGI_MODE is True, only Dual N-Back will be available.
# Default: 2
GAME_MODE = 2

# Default starting n-back levels.
# must be greater than or equal to 1.
# Look above to find the corresponding mode number.  Add a line for the mode
# if it doesn't already exist.  Modes not specifically listed here will
# use BACK_DEFAULT instead.
#
# Crab and multi-modes will default to the level associated with the modes
# they're based on (if it's listed) or to BACK_DEFAULT (if it's not listed).

BACK_DEFAULT = 2

BACK_4 = 1
BACK_5 = 1
BACK_6 = 1
BACK_7 = 1
BACK_8 = 1
BACK_9 = 1

# N-back level resetting:
# Should we start at the default N-back level for that game mode every
# day, or should we resume at the last day's level?
RESET_LEVEL = False

# Use Variable N-Back by default?
# 0 = static n-back (default)
# 1 = variable n-back
VARIABLE_NBACK = 0

# Number of 0.1 second intervals per trial.
# Must be greater than or equal to 4 (ie, 0.4 seconds)
# Look above to find the corresponding mode number.  Add a line for the mode
# if it doesn't already exist.  Modes not specifically listed here will
# use TICKS_DEFAULT instead.
#
# Crab and multi-modes will default to the ticks associated with the modes
# they're based on, *plus an optional bonus*, unless you add a line here to
# give it a specific value.  Any bonuses will be ignored for specified modes.
TICKS_DEFAULT = 30
TICKS_4 = 35
TICKS_5 = 35
TICKS_6 = 35
TICKS_7 = 40
TICKS_8 = 40
TICKS_9 = 40

# Tick bonuses for crab and multi-modes not listed above.  Can be negative
# if you're a masochist.

BONUS_TICKS_CRAB = 0
BONUS_TICKS_MULTI_2 = 5
BONUS_TICKS_MULTI_3 = 10
BONUS_TICKS_MULTI_4 = 15

# The number of trials per session equals
# NUM_TRIALS + NUM_TRIALS_FACTOR * n ^ NUM_TRIALS_EXPONENT,
# where n is the current n-back level.

# Default base number of trials per session.
# Must be greater than or equal to 1.
# Default: 20
NUM_TRIALS = 20

NUM_TRIALS_FACTOR = 1
NUM_TRIALS_EXPONENT = 2

# Thresholds for n-back level advancing & fallback.
# Values are 0-100.
# Set THRESHOLD_ADVANCE to 101 to disable automatic level advance.
# Set THRESHOLD_FALLBACK to 0 to disable fallback.
# FALLBACK_SESSIONS controls the number of sessions below
#    the fallback threshold that will trigger a level decrease.
# Note: in Jaeggi mode, only JAEGGI_ADVANCE and JAEGGI_FALLBACK
#    are used.
# Defaults: 80, 50, 3, 90, 75
THRESHOLD_ADVANCE = 80
THRESHOLD_FALLBACK = 50
THRESHOLD_FALLBACK_SESSIONS = 3
JAEGGI_ADVANCE = 90
JAEGGI_FALLBACK = 75

# Show feedback regarding session performance.
# If False, forces USE_MUSIC and USE_APPLAUSE to also be False.
USE_SESSION_FEEDBACK = True

# Music/SFX options.
# Volumes are from 0.0 (silent) to 1.0 (full)
# Defaults: True, True, 1.0, 1.0
USE_MUSIC = True
USE_APPLAUSE = True
MUSIC_VOLUME = 1.0
SFX_VOLUME = 1.0

# Specify an alternate stats file.
# Default: stats.txt
STATSFILE = stats.txt

# Specify the hour the stats will roll over to a new day [0-23]
ROLLOVER_HOUR = 4

# Version check on startup (http protocol)?
# Default: False
VERSION_CHECK_ON_STARTUP = False

# The chance that a match will be generated by force, in addition to the
# inherent 1/8 chance. High settings will cause repetitive sequences to be
# generated.  Increasing this value will make the n-back task significantly
# easier if you're using JAGGI_SCORING = False.
# The value must be a decimal from 0 to 1.
# Note: this option has no effect in Jaeggi mode.
# Default: 0.125
CHANCE_OF_GUARANTEED_MATCH = 0.125

# The chance that a near-miss will be generated to help train resolution of
# cognitive interference.  For example, in 5-back, a near-miss might be
# ABCDE-FGDJK--the "D" comes one trial earlier than would be necessary
# for a correct match.  Near-misses can be one trial short of a match,
# one trial late, or N trials late (would have been a match if it was one
# "cycle" ago).  This setting will never accidentally generate a correct match
# in the case of repeating stimuli if it can be avoided.
# Default:  0.125

DEFAULT_CHANCE_OF_INTERFERENCE = 0.125

# How often should Brain Workshop panhandle for a donation?  After every
# PANHANDLE_FREQUENCY sessions, Brain Workshop will annoy you slightly by
# asking for money.  Set this to 0 if you have a clear conscience.
# Default: 100
PANHANDLE_FREQUENCY = 100

# Arithmetic mode settings.
ARITHMETIC_MAX_NUMBER = 12
ARITHMETIC_USE_NEGATIVES = False
ARITHMETIC_USE_ADDITION = True
ARITHMETIC_USE_SUBTRACTION = True
ARITHMETIC_USE_MULTIPLICATION = True
ARITHMETIC_USE_DIVISION = True
ARITHMETIC_ACCEPTABLE_DECIMALS = ['0.1', '0.2', '0.3', '0.4', '0.5', '0.6',
    '0.7', '0.8', '0.9', '0.125', '0.25', '0.375', '0.625', '0.75', '0.875',
    '0.15', '0.35', '0.45', '0.55', '0.65', '0.85', '0.95',]

# Colors for the color n-back task
# format: (red, green, blue, 255)
# Note: Changing these colors will have no effect in Dual or
#   Triple N-Back unless OLD_STYLE_SQUARES is set to True.
# the _BLK colors are used when BLACK_BACKGROUND is set to True.
COLOR_1 = (0, 0, 255, 255)
COLOR_2 = (0, 255, 255, 255)
COLOR_3 = (0, 255, 0, 255)
COLOR_4 = (48, 48, 48, 255)
COLOR_4_BLK = (255, 255, 255, 255)
COLOR_5 = (255, 0, 255, 255)
COLOR_6 = (255, 0, 0, 255)
COLOR_7 = (208, 208, 208, 255)
COLOR_7_BLK = (64, 64, 64, 255)
COLOR_8 = (255, 255, 0, 255)

# text color
COLOR_TEXT = (0, 0, 0, 255)
COLOR_TEXT_BLK = (240, 240, 240, 255)

# input label color
COLOR_LABEL_CORRECT = (64, 255, 64, 255)
COLOR_LABEL_OOPS = (64, 64, 255, 255)
COLOR_LABEL_INCORRECT = (255, 64, 64, 255)


# Saccadic eye movement options.
# Delay = number of seconds to wait before switching the dot
# Repetitions = number of times to switch the dot
SACCADIC_DELAY = 0.5
SACCADIC_REPETITIONS = 60

######################################################################
# Keyboard definitions.
# The following keys cannot be used: ESC, X, P, F8, F10.
# You can find the codes using python "from pyglet.window import key; print(key.A)":
# https://pyglet.readthedocs.io/en/latest/modules/window_key.html#module-pyglet.window.key
######################################################################

# Position match. Default: 97 (A)
KEY_POSITION1 = 97

# Sound match. Default: 108 (L)
KEY_AUDIO = 108

# Sound2 match. Default: 59 (Semicolon ;)
KEY_AUDIO2 = 59

# Color match. Default: 102 (F)
KEY_COLOR = 102
# Image match. Default: 106 (J)
KEY_IMAGE = 106

# Position match, multiple-stimulus mode.
# Defaults:  115 (S), 100 (D), 102 (F)
KEY_POSITION2 = 115
KEY_POSITION3 = 100
KEY_POSITION4 = 102

# Color/image match, multiple-stimulus mode.  KEY_VIS1 will be used instead
# of KEY_COLOR or KEY_IMAGE.
# Defaults: 103 (G), 104 (H), 106 (J), 107 (K)
KEY_VIS1 = 103
KEY_VIS2 = 104
KEY_VIS3 = 106
KEY_VIS4 = 107


# These are used in the Combination N-Back modes.
# Visual & n-visual match. Default: 115 (S)
KEY_VISVIS = 115
# Visual & n-audio match. Default: 100 (D)
KEY_VISAUDIO = 100
# Sound & n-visual match. Default: 106 (J)
KEY_AUDIOVIS = 106

# Advance to the next trial in self-paced mode. Default: 65293 (return/enter).
# You may also like space (32).
KEY_ADVANCE = 65293

######################################################################
# This is the end of the configuration file.
######################################################################
"""

class dotdict(dict):
    def __getattr__(self, attr):
        return self.get(attr, None)
    __setattr__= dict.__setitem__
    __delattr__= dict.__delitem__

def dump_pyglet_info():
    from pyglet import info
    oldStdout = sys.stdout
    pygletDumpPath = os.path.join(get_data_dir(), 'dump.txt')
    sys.stdout = open(pygletDumpPath, 'w')
    info.dump()
    sys.stdout.close()
    sys.stdout = oldStdout
    print("pyglet info dumped to %s" % pygletDumpPath)
    sys.exit()

# parse config file & command line options
if '--debug' in sys.argv:
    DEBUG = True
if '--vsync' in sys.argv or sys.platform == 'darwin':
    VSYNC = True
if '--dump' in sys.argv:
    dump_pyglet_info()
if get_argv('--configfile'):
    CONFIGFILE = get_argv('--configfile')

messagequeue = [] # add messages generated during loading here
class Message:
    def __init__(self, msg):
        if not 'window' in globals():
            print(msg)               # dump it to console just in case
            messagequeue.append(msg) # but we'll display this later
            return
        self.batch = pyglet.graphics.Batch()
        self.label = pyglet.text.Label(msg,
                            font_name=self.fontlist_serif,
                            color=cfg.COLOR_TEXT,
                            batch=self.batch,
                            multiline=True,
                            width=(4*window.width)/5,
                            font_size=calc_fontsize(14),
                            x=width_center(), y=height_center(),
                            anchor_x='center', anchor_y='center')
        window.push_handlers(self.on_key_press, self.on_draw)
        self.on_draw()

    def on_key_press(self, sym, mod):
        if sym:
            self.close()
        return pyglet.event.EVENT_HANDLED

    def close(self):
        return window.remove_handlers(self.on_key_press, self.on_draw)

    def on_draw(self):
        window.clear()
        self.batch.draw()
        return pyglet.event.EVENT_HANDLED

def load_last_user(lastuserpath):
    path = os.path.join(get_data_dir(), lastuserpath)
    if os.path.isfile(path):
        debug_msg("Trying to load '%s'" % (path))
        try:
            f = open(path, 'rb')
            p = pickle.Unpickler(f)
            options = p.load()
            del p
            f.close()
        except Exception as e:
            print("%s\nDue to error, continuing as user 'default'" % e)
            # Delete the pickle file, since it wasn't able to be loaded.
            os.remove(path)
            return
        if options['USER'] == '':
            print("Last loaded user is an empty string! Setting it to default instead")
            options['USER'] = "default"
        if not options['USER'].lower() == 'default':
            global USER
            global STATS_BINARY
            global CONFIGFILE
            USER         = options['USER']
            CONFIGFILE   = USER + '-config.ini'
            STATS_BINARY = USER + '-logfile.dat'

def save_last_user(lastuserpath):
    try:
        f = open(os.path.join(get_data_dir(), lastuserpath), 'wb')
        p = pickle.Pickler(f)
        p.dump({'USER': USER})
        # also do date of last session?
    except Exception as e:
        error_msg("Could not save last user", e)
        pass

def parse_config(configpath):
    if not (CLINICAL_MODE and configpath == 'config.ini'):
        fullpath = os.path.join(get_data_dir(), configpath)
        if not os.path.isfile(fullpath):
            rewrite_configfile(configpath, overwrite=False)

        # The following is a routine to overwrite older config files with the new one.
        oldconfigfile = open(fullpath, 'r+')
        while oldconfigfile:
            line = oldconfigfile.readline()
            if line == '': # EOF reached. string 'generated by Brain Workshop' not found
                oldconfigfile.close()
                rewrite_configfile(configpath, overwrite=True)
                break
            if line.find('generated by Brain Workshop') > -1:
                splitline = line.split()
                version = splitline[5]
                if version < CONFIG_OVERWRITE_IF_OLDER_THAN:
                    oldconfigfile.close()
                    os.rename(fullpath, fullpath + '.' + version + '.bak')
                    rewrite_configfile(configpath, overwrite=True)
                break
        oldconfigfile.close()

        try:
            config = ConfigParser.ConfigParser()
            config.read(os.path.join(get_data_dir(), configpath))
        except Exception as e:
            debug_msg(e)
            if configpath != 'config.ini':
                quit_with_error(_('Unable to load config file: %s') %
                                 os.path.join(get_data_dir(), configpath))

    defaultconfig = ConfigParser.ConfigParser()
    if sys.version_info >= (3,):
        defaultconfig.read_file(StringIO(CONFIGFILE_DEFAULT_CONTENTS))
    else:
        defaultconfig.readfp(StringIO.StringIO(CONFIGFILE_DEFAULT_CONTENTS))

    def try_eval(text):  # this is a one-use function for config parsing
        try:  return eval(text)
        except: return text

    cfg = dotdict()
    if CLINICAL_MODE and CONFIGFILE == 'config.ini': configs = (defaultconfig,)
    else: configs = (defaultconfig, config)
    for config in configs: # load defaultconfig first, in case of incomplete user's config.ini
        config_items = [(k.upper(), try_eval(v)) for k, v in config.items('DEFAULT')]
        cfg.update(config_items)

    if not 'CHANCE_OF_INTERFERENCE' in cfg:
        cfg.CHANCE_OF_INTERFERENCE = cfg.DEFAULT_CHANCE_OF_INTERFERENCE
    rtrn = get_argv('--statsfile')
    if rtrn:
        cfg.STATSFILE = rtrn
    return cfg

def rewrite_configfile(configfile, overwrite=False):
    global STATS_BINARY
    if USER.lower() == 'default':
        statsfile = 'stats.txt'
        STATS_BINARY = 'logfile.dat' # or cmd-line-opts use non-default files
    else:
        statsfile = USER + '-stats.txt'
    try:
        os.stat(os.path.join(get_data_dir(), configfile))
    except OSError as e:
        debug_msg(e)
        overwrite = True
    if overwrite:
        f = open(os.path.join(get_data_dir(), configfile), 'w')
        newconfigfile_contents = CONFIGFILE_DEFAULT_CONTENTS.replace(
            'stats.txt', statsfile)
        f.write(newconfigfile_contents)
        f.close()
    # let's hope nobody uses '-stats.txt' in their username
    STATS_BINARY = statsfile.replace('-stats.txt', '-logfile.dat')
    try:
        os.stat(os.path.join(get_data_dir(), statsfile))
    except OSError as e:
        debug_msg(e)
        f = open(os.path.join(get_data_dir(), statsfile), 'w')
        f.close()
    try:
        os.stat(os.path.join(get_data_dir(), STATS_BINARY))
    except OSError:
        f = open(os.path.join(get_data_dir(), STATS_BINARY), 'w')
        f.close()

try:
    path = get_data_dir()
    os.makedirs(path)
except OSError as e:
    if e.errno == errno.EEXIST and os.path.isdir(path):
        pass
    else:
        raise

load_last_user('defaults.ini')

cfg = parse_config(CONFIGFILE)

if CLINICAL_MODE:
    cfg.JAEGGI_INTERFACE_DEFAULT_SCORING = False
    cfg.JAEGGI_MODE                      = True
    cfg.JAEGGI_FORCE_OPTIONS             = True
    cfg.JAEGGI_FORCE_OPTIONS_ADDITIONAL  = True
    cfg.SKIP_TITLE_SCREEN                = True
    cfg.USE_MUSIC                        = False
elif cfg.JAEGGI_INTERFACE_DEFAULT_SCORING:
    cfg.ANIMATE_SQUARES         = False
    cfg.OLD_STYLE_SQUARES       = True
    cfg.OLD_STYLE_SHARP_CORNERS = True
    cfg.GRIDLINES               = False
    cfg.CROSSHAIRS              = True
    cfg.SHOW_FEEDBACK           = False
    cfg.BLACK_BACKGROUND        = True
    cfg.WINDOW_FULLSCREEN       = True
    cfg.HIDE_TEXT               = True
    cfg.FIELD_EXPAND            = True

if cfg.JAEGGI_MODE and not cfg.JAEGGI_INTERFACE_DEFAULT_SCORING:
    cfg.GAME_MODE      = 2
    cfg.VARIABLE_NBACK = 0
    cfg.JAEGGI_SCORING = True
    if cfg.JAEGGI_FORCE_OPTIONS:
        cfg.AUDIO1_SETS = ['letters']
        cfg.ANIMATE_SQUARES   = False
        cfg.OLD_STYLE_SQUARES = True
        cfg.OLD_STYLE_SHARP_CORNERS = True
        cfg.GRIDLINES     = False
        cfg.CROSSHAIRS    = True
        cfg.SHOW_FEEDBACK = False
        cfg.THRESHOLD_FALLBACK_SESSIONS = 1
        cfg.NUM_TRIALS_FACTOR   = 1
        cfg.NUM_TRIALS_EXPONENT = 1
    if cfg.JAEGGI_FORCE_OPTIONS_ADDITIONAL:
        cfg.BLACK_BACKGROUND  = True
        cfg.WINDOW_FULLSCREEN = True
        cfg.HIDE_TEXT    = True
        cfg.FIELD_EXPAND = True

if not cfg.USE_SESSION_FEEDBACK:
    cfg.USE_MUSIC    = False
    cfg.USE_APPLAUSE = False

if cfg.BLACK_BACKGROUND:
    cfg.COLOR_TEXT = cfg.COLOR_TEXT_BLK
def get_threshold_advance():
    if cfg.JAEGGI_SCORING:
        return cfg.JAEGGI_ADVANCE
    return cfg.THRESHOLD_ADVANCE
def get_threshold_fallback():
    if cfg.JAEGGI_SCORING:
        return cfg.JAEGGI_FALLBACK
    return cfg.THRESHOLD_FALLBACK

# this function checks if a new update for Brain Workshop is available.
update_available = False
update_version = 0
def update_check():
    global update_available
    global update_version
    socket.setdefaulttimeout(TIMEOUT_SILENT)
    if sys.version_info >= (3,0):
        req = urllib.request.Request(WEB_VERSION_CHECK)
    else:
        req = urllib.Request(WEB_VERSION_CHECK)
    try:
        response = urllib.urlopen(req)
        version = response.readline().strip()
    except Exception as e:
        debug_msg(e)
        return
    if version > VERSION: # simply comparing strings works just fine
        update_available = True
        update_version   = version

if cfg.VERSION_CHECK_ON_STARTUP and not CLINICAL_MODE:
    update_check()
try:
    # workaround for pyglet.gl.ContextException error on certain video cards.
    os.environ["PYGLET_SHADOW_WINDOW"] = "0"
    import pyglet
    if NOVBO: pyglet.options['graphics_vbo'] = False
    from pyglet.window import key

    # shapes submodule is available with pyglet >=1.5.4
    have_shapes = hasattr(pyglet, 'shapes')
except Exception as e:
    debug_msg(e)
    quit_with_error(_('Error: unable to load pyglet.  If you already installed pyglet, please ensure ctypes is installed.  Please visit %s') % WEB_PYGLET_DOWNLOAD)

audio_driver = pyglet.media.get_audio_driver()
debug_msg("Loaded audio driver=" + audio_driver.__class__.__name__)
if audio_driver.__class__.__name__ == "SilentDriver":
    quit_with_error(_('No suitable audio driver could be loaded.'))

# Initialize resources (sounds and images)
#
# --- BEGIN RESOURCE INITIALIZATION SECTION ----------------------------------
#

res_path = get_res_dir()
if not os.access(res_path, os.F_OK):
    quit_with_error(_('Error: the resource folder\n%s') % res_path +
                    _(' does not exist or is not readable.  Exiting'), trace=False)

if pyglet.version < '1.1':
    quit_with_error(_('Error: pyglet 1.1 or greater is required.\n') +
                    _('You probably have an older version of pyglet installed.\n') +
                    _('Please visit %s') % WEB_PYGLET_DOWNLOAD, trace=False)

supportedtypes = {'sounds' :['wav'],
                  'music'  :['wav', 'ogg', 'mp3', 'aac', 'mp2', 'ac3', 'm4a'], # what else?
                  'sprites':['png', 'jpg', 'bmp']}

def test_music():
    try:
        import pyglet
        if pyglet.version >= '1.4':
            from pyglet.media import have_ffmpeg
            pyglet.media.have_avbin = have_ffmpeg()
            if not pyglet.media.have_avbin:
                cfg.USE_MUSIC = False
        else:
            try:
                from pyglet.media import avbin
            except Exception as e:
                debug_msg(e)
                pyglet.lib.load_library('avbin')
            if pyglet.version >= '1.2':  # temporary workaround for defect in pyglet svn 2445
                pyglet.media.have_avbin = True

            # On Windows with Data Execution Protection enabled (on by default on Vista),
            # an exception will be raised when use of avbin is attempted:
            #   WindowsError: exception: access violation writing [ADDRESS]
            # The file doesn't need to be in a avbin-specific format,
            # since pyglet will use avbin over riff whenever it's detected.
            # Let's find an audio file and try to load it to see if avbin works.
            opj = os.path.join
            opj = os.path.join
            def look_for_music(path):
                files = [p for p in os.listdir(path) if not p.startswith('.') and not os.path.isdir(opj(path, p))]
                for f in files:
                    ext = f.lower()[-3:]
                    if ext in ['wav', 'ogg', 'mp3', 'aac', 'mp2', 'ac3', 'm4a'] and not ext in ('wav'):
                        return [opj(path, f)]
                dirs  = [opj(path, p) for p in os.listdir(path) if not p.startswith('.') and os.path.isdir(opj(path, p))]
                results = []
                for d in dirs:
                    results.extend(look_for_music(d))
                    if results: return results
                return results
            music_file = look_for_music(res_path)
            if music_file:
                # The first time we load a file should trigger the exception
                music_file = music_file[0]
                loaded_music = pyglet.media.load(music_file, streaming=False)
                del loaded_music
            else:
                cfg.USE_MUSIC = False

    except ImportError as e:
        debug_msg(e)
        cfg.USE_MUSIC = False
        if pyglet.version >= '1.2':
            pyglet.media.have_avbin = False
        print( _('AVBin not detected. Music disabled.'))
        print( _('Download AVBin from: https://avbin.github.io'))

    except Exception as e: # WindowsError
        debug_msg(e)
        cfg.USE_MUSIC = False
        pyglet.media.have_avbin = False
        if hasattr(pyglet.media, '_source_class'): # pyglet v1.1
            import pyglet.media.riff
            pyglet.media._source_class = pyglet.media.riff.WaveSource
        elif hasattr(pyglet.media, '_source_loader'): # pyglet v1.2 and development branches
            import pyglet.media.riff
            pyglet.media._source_loader = pyglet.media.RIFFSourceLoader()
        Message("""Warning: Could not load AVbin. Music disabled.

This is usually due to Windows Data Execution Prevention (DEP). Due to a bug in
AVbin, a library used for decoding sound files, music is not available when \
DEP is enabled. To enable music, disable DEP for Brain Workshop. To simply get \
rid of this message, set USE_MUSIC = False in your config.ini file.

To disable DEP:

1. Open Control Panel -> System
2. Select Advanced System Settings
3. Click on Performance -> Settings
4. Click on the Data Execution Prevention tab
5. Either select the "Turn on DEP for essential Windows programs and services \
only" option, or add an exception for Brain Workshop.

Press any key to continue without music support.
""")

test_music()
if pyglet.media.have_avbin: supportedtypes['sounds'] = supportedtypes['music']
elif cfg.USE_MUSIC:         supportedtypes['music'] = supportedtypes['sounds']
else:                       del supportedtypes['music']

supportedtypes['misc'] = supportedtypes['sounds'] + supportedtypes['sprites']

resourcepaths = {}
for restype in list(supportedtypes):
    res_sets = {}
    for folder in os.listdir(os.path.join(res_path, restype)):
        contents = []
        if os.path.isdir(os.path.join(res_path, restype, folder)):
            contents = [os.path.join(res_path, restype, folder, obj)
                          for obj in os.listdir(os.path.join(res_path, restype, folder))
                                  if obj[-3:] in supportedtypes[restype]]
            contents.sort()
        if contents: res_sets[folder] = contents
    if res_sets: resourcepaths[restype] = res_sets

sounds = {}
for k in list(resourcepaths['sounds']):
    sounds[k] = {}
    for f in resourcepaths['sounds'][k]:
        sounds[k][os.path.basename(f).split('.')[0]] = pyglet.media.load(f, streaming=False)

sound = sounds['letters'] # is this obsolete yet?

if cfg.USE_APPLAUSE:
    applausesounds = [pyglet.media.load(soundfile, streaming=False)

                     for soundfile in resourcepaths['misc']['applause']]

applauseplayer = get_pyglet_media_Player()
musicplayer    = get_pyglet_media_Player()
def play_applause():
    applauseplayer.queue(random.choice(applausesounds))
    applauseplayer.volume = cfg.SFX_VOLUME
    if DEBUG: print("Playing applause")
    applauseplayer.play()
def play_music(percent):
    if 'music' in resourcepaths:
        if preventMusicSkipping: pyglet.clock.tick(poll=True) # Prevent music skipping 1
        if percent >= get_threshold_advance() and 'advance' in resourcepaths['music']:
            musicplayer.queue(pyglet.media.load(random.choice(resourcepaths['music']['advance']), streaming = True))
        elif percent >= (get_threshold_advance() + get_threshold_fallback()) // 2 and 'great' in resourcepaths['music']:
            musicplayer.queue(pyglet.media.load(random.choice(resourcepaths['music']['great']), streaming = True))
        elif percent >= get_threshold_fallback() and 'good' in resourcepaths['music']:
            musicplayer.queue(pyglet.media.load(random.choice(resourcepaths['music']['good']), streaming = True))
        else:
            return
    else:
        return
    musicplayer.volume = cfg.MUSIC_VOLUME
    if DEBUG: print("Playing music")
    musicplayer.play()
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
    if color in (4, 7) and cfg.BLACK_BACKGROUND:
        return cfg['COLOR_%i_BLK' % color]
    return cfg['COLOR_%i' % color]

def default_nback_mode(mode):
    if ('BACK_%i' % mode) in cfg:
        return cfg['BACK_%i' % mode]
    elif mode > 127:  # try to use the base mode for crab, multi
        return default_nback_mode(mode % 128)
    else:
        return cfg.BACK_DEFAULT


def default_ticks(mode):
    if ('TICKS_%i' % mode) in cfg:
        return cfg['TICKS_%i' % mode]
    elif mode > 127:
        bonus = ((mode & 128)/128) * cfg.BONUS_TICKS_CRAB
        if mode & 768:
            bonus += cfg['BONUS_TICKS_MULTI_%i' % ((mode & 768)/256+1)]
        if DEBUG: print("Adding a bonus of %i ticks for mode %i" % (bonus, mode))
        return bonus + default_ticks(mode % 128)
    else:
        return cfg.TICKS_DEFAULT

#Create the game window
caption = []
if CLINICAL_MODE:
    caption.append('BW-Clinical ')
else:
    caption.append('Brain Workshop ')
caption.append(VERSION)
if USER != 'default':
    caption.append(' - ')
    caption.append(USER)
if cfg.WINDOW_FULLSCREEN:
    style = pyglet.window.Window.WINDOW_STYLE_BORDERLESS
else:
    style = pyglet.window.Window.WINDOW_STYLE_DEFAULT

class MyWindow(pyglet.window.Window):
    def on_key_press(self, symbol, modifiers):
        pass
    def on_key_release(self, symbol, modifiers):
        pass
if cfg.WINDOW_FULLSCREEN:
    screen = pyglet.canvas.get_display().get_default_screen()
    cfg.WINDOW_WIDTH_FULLSCREEN  = screen.width
    cfg.WINDOW_HEIGHT_FULLSCREEN = screen.height
    window = MyWindow(cfg.WINDOW_WIDTH_FULLSCREEN, cfg.WINDOW_HEIGHT_FULLSCREEN, caption=''.join(caption), style=style, vsync=VSYNC, fullscreen=True)
else:
    window = MyWindow(cfg.WINDOW_WIDTH, cfg.WINDOW_HEIGHT, caption=''.join(caption), style=style, vsync=VSYNC)

#if DEBUG:
#    window.push_handlers(pyglet.window.event.WindowEventLogger())
if sys.platform == 'darwin' and cfg.WINDOW_FULLSCREEN:
    window.set_exclusive_keyboard()
if sys.platform == 'linux2':
    window.set_icon(pyglet.image.load(resourcepaths['misc']['brain'][0]))

# set the background color of the window
if cfg.BLACK_BACKGROUND:
    pyglet.gl.glClearColor(0, 0, 0, 1)
else:
    pyglet.gl.glClearColor(1, 1, 1, 1)
if cfg.WINDOW_FULLSCREEN:
    window.maximize()
    window.set_fullscreen(cfg.WINDOW_FULLSCREEN)
    window.set_mouse_visible(False)


# All changeable game state variables are located in an instance of the Mode class
class Mode:
    def __init__(self):
        self.mode = cfg.GAME_MODE
        self.back = default_nback_mode(self.mode)
        self.ticks_per_trial = default_ticks(self.mode)
        self.num_trials = cfg.NUM_TRIALS
        self.num_trials_factor = cfg.NUM_TRIALS_FACTOR
        self.num_trials_exponent = cfg.NUM_TRIALS_EXPONENT
        self.num_trials_total = self.num_trials + self.num_trials_factor * \
            self.back ** self.num_trials_exponent

        self.short_mode_names = {2:'D',
                                 3:'PCA',
                                 4:'DC',
                                 5:'TC',
                                 6:'QC',
                                 7:'A',
                                 8:'DA',
                                 9:'TA',
                                 10:'Po',
                                 11:'Au',
                                 12:'TCC',
                                 20:'PC',
                                 21:'PI',
                                 22:'CA',
                                 23:'IA',
                                 24:'CI',
                                 25:'PCI',
                                 26:'PIA',
                                 27:'CIA',
                                 28:'Q',
                                 100:'AA',
                                 101:'PAA',
                                 102:'CAA',
                                 103:'IAA',
                                 104:'PCAA',
                                 105:'PIAA',
                                 106:'CIAA',
                                 107:'P'
                                 }

        self.long_mode_names =  {2:_('Dual'),
                                 3:_('Position, Color, Sound'),
                                 4:_('Dual Combination'),
                                 5:_('Tri Combination'),
                                 6:_('Quad Combination'),
                                 7:_('Arithmetic'),
                                 8:_('Dual Arithmetic'),
                                 9:_('Triple Arithmetic'),
                                 10:_('Position'),
                                 11:_('Sound'),
                                 12:_('Tri Combination (Color)'),
                                 20:_('Position, Color'),
                                 21:_('Position, Image'),
                                 22:_('Color, Sound'),
                                 23:_('Image, Sound'),
                                 24:_('Color, Image'),
                                 25:_('Position, Color, Image'),
                                 26:_('Position, Image, Sound'),
                                 27:_('Color, Image, Sound'),
                                 28:_('Quad'),
                                 100:_('Sound, Sound2'),
                                 101:_('Position, Sound, Sound2'),
                                 102:_('Color, Sound, Sound2'),
                                 103:_('Image, Sound, Sound2'),
                                 104:_('Position, Color, Sound, Sound2'),
                                 105:_('Position, Image, Sound, Sound2'),
                                 106:_('Color, Image, Sound, Sound2'),
                                 107:_('Pentuple')
                                 }

        self.modalities = { 2:['position1', 'audio'],
                            3:['position1', 'color', 'audio'],
                            4:['visvis', 'visaudio', 'audiovis', 'audio'],
                            5:['position1', 'visvis', 'visaudio', 'audiovis', 'audio'],
                            6:['position1', 'visvis', 'visaudio', 'color', 'audiovis', 'audio'],
                            7:['arithmetic'],
                            8:['position1', 'arithmetic'],
                            9:['position1', 'arithmetic', 'color'],
                            10:['position1'],
                            11:['audio'],
                            12:['visvis', 'visaudio', 'color', 'audiovis', 'audio'],
                            20:['position1', 'color'],
                            21:['position1', 'image'],
                            22:['color', 'audio'],
                            23:['image', 'audio'],
                            24:['color', 'image'],
                            25:['position1', 'color', 'image'],
                            26:['position1', 'image', 'audio'],
                            27:['color', 'image', 'audio'],
                            28:['position1', 'color', 'image', 'audio'],
                            100:['audio', 'audio2'],
                            101:['position1', 'audio', 'audio2'],
                            102:['color', 'audio', 'audio2'],
                            103:['image', 'audio', 'audio2'],
                            104:['position1', 'color', 'audio', 'audio2'],
                            105:['position1', 'image', 'audio', 'audio2'],
                            106:['color', 'image', 'audio', 'audio2'],
                            107:['position1', 'color', 'image', 'audio', 'audio2']
                            }

        self.flags = {}

        # generate crab modes
        for m in list(self.short_mode_names):
            nm = m | 128                          # newmode; Crab DNB = 2 | 128 = 130
            self.flags[m]  = {'crab':0, 'multi':1, 'selfpaced':0}# forwards
            self.flags[nm] = {'crab':1, 'multi':1, 'selfpaced':0}# every (self.back) stimuli are reversed for matching
            self.short_mode_names[nm] = 'C' + self.short_mode_names[m]
            self.long_mode_names[nm] = _('Crab ') + self.long_mode_names[m]
            self.modalities[nm] = self.modalities[m][:] # the [:] at the end is
            # so we take a copy of the list, in case we want to change it later

        # generate multi-stim modes
        for m in list(self.short_mode_names):
            for n, s in [(2, _('Double-stim')), (3, _('Triple-stim')), (4, _('Quadruple-stim'))]:
                if set(['color', 'image']).issubset(self.modalities[m]) \
                  or not 'position1' in self.modalities[m] \
                  or set(['visvis', 'arithmetic']).intersection(self.modalities[m]):  # Combination? AAAH! Scary!
                    continue
                nm = m | 256 * (n-1)               # newmode; 3xDNB = 2 | 512 = 514
                self.flags[nm] = dict(self.flags[m]) # take a copy
                self.flags[nm]['multi'] = n
                self.short_mode_names[nm] = repr(n) + 'x' + self.short_mode_names[m]
                self.long_mode_names[nm] = s + ' ' + self.long_mode_names[m]
                self.modalities[nm] = self.modalities[m][:] # take a copy ([:])
                for i in range(2, n+1):
                    self.modalities[nm].insert(i-1, 'position'+repr(i))
                if 'color' in self.modalities[m] or 'image' in self.modalities[m]:
                    for i in range(1, n+1):
                        self.modalities[nm].insert(n+i-1, 'vis'+repr(i))
                for ic in 'image', 'color':
                    if ic in self.modalities[nm]:
                        self.modalities[nm].remove(ic)

        for m in list(self.short_mode_names):
            nm = m | 1024
            self.short_mode_names[nm] = 'SP-' + self.short_mode_names[m]
            self.long_mode_names[nm] = 'Self-paced ' + self.long_mode_names[m]
            self.modalities[nm] = self.modalities[m][:]
            self.flags[nm] = dict(self.flags[m])
            self.flags[nm]['selfpaced'] = 1


        self.variable_list = []

        self.manual = cfg.MANUAL
        if not self.manual:
            self.enforce_standard_mode()

        self.inputs = {'position1': False,
                       'position2': False,
                       'position3': False,
                       'position4': False,
                       'color':     False,
                       'image':     False,
                       'vis1':      False,
                       'vis2':      False,
                       'vis3':      False,
                       'vis4':      False,
                       'visvis':    False,
                       'visaudio':  False,
                       'audiovis':  False,
                       'audio':     False,
                       'audio2':    False}

        self.input_rts = {'position1': 0.,
                          'position2': 0.,
                          'position3': 0.,
                          'position4': 0.,
                          'color':     0.,
                          'image':     0.,
                          'vis1':      0.,
                          'vis2':      0.,
                          'vis3':      0.,
                          'vis4':      0.,
                          'visvis':    0.,
                          'visaudio':  0.,
                          'audiovis':  0.,
                          'audio':     0.,
                          'audio2':    0.}

        self.hide_text = cfg.HIDE_TEXT

        self.current_stim = {'position1': 0,
                             'position2': 0,
                             'position3': 0,
                             'position4': 0,
                             'color':     0,
                             'vis':       0, # image or letter for non-multi mode
                             'vis1':      0, # image or color for multi mode
                             'vis2':      0,
                             'vis3':      0,
                             'vis4':      0,
                             'audio':     0,
                             'audio2':    0,
                             'number':    0}

        self.current_operation = 'none'

        self.started = False
        self.paused = False
        self.show_missed = False
        self.sound_select = False
        self.draw_graph = False
        self.saccadic = False
        if cfg.SKIP_TITLE_SCREEN:
            self.title_screen = False
        else:
            self.title_screen = True
        self.shrink_brain = False

        self.session_number = 0
        self.trial_number = 0
        self.tick = 0
        self.progress = 0

        self.sound_mode = 'none'
        self.sound2_mode = 'none'
        self.soundlist = []
        self.soundlist2 = []

        self.bt_sequence = []

    def enforce_standard_mode(self):
        self.back = default_nback_mode(self.mode)
        self.ticks_per_trial = default_ticks(self.mode)
        self.num_trials = cfg.NUM_TRIALS
        self.num_trials_factor = cfg.NUM_TRIALS_FACTOR
        self.num_trials_exponent = cfg.NUM_TRIALS_EXPONENT
        self.num_trials_total = self.num_trials + self.num_trials_factor * \
            self.back ** self.num_trials_exponent
        self.session_number = 0

    def short_name(self, mode=None, back=None):
        if mode == None: mode = self.mode
        if back == None: back = self.back
        return self.short_mode_names[mode] + str(back) + 'B'

# What follows are the classes which control all the text and graphics.
#
# --- BEGIN GRAPHICS SECTION ----------------------------------------------
#

class Graph:
    def __init__(self):
        self.graph = 2
        self.reset_dictionaries()
        self.reset_percents()
        self.batch = None
        self.styles = ['N+10/3+4/3', 'N', '%', 'N.%', 'N+2*%-1']
        self.style = 0

    def next_style(self):
        self.style = (self.style + 1) % len(self.styles)
        print("style = %s" % self.styles[self.style]) # fixme:  change the labels
        self.parse_stats()

    def reset_dictionaries(self):
        self.dictionaries = dict([(i, {}) for i in mode.modalities])

    def reset_percents(self):
        self.percents = dict([(k, dict([(i, []) for i in v])) for k,v in mode.modalities.items()])

    def next_nonempty_mode(self):
        self.next_mode()
        mode1 = self.graph
        mode2 = None    # to make sure the loop runs the first iteration
        while self.graph != mode2 and not self.dictionaries[self.graph]:
            self.next_mode()
            mode2 = mode1
    def next_mode(self):
        modes = list(mode.modalities)
        modes.sort()
        i = modes.index(self.graph)
        i = (i + 1) % len(modes)
        self.graph = modes[i]
        self.batch = None

    def parse_stats(self):
        self.batch = None
        self.reset_dictionaries()
        self.reset_percents()
        ind = {'date':0, 'modename':1, 'percent':2, 'mode':3, 'n':4, 'ticks':5,
               'trials':6, 'manual':7, 'session':8, 'position1':9, 'audio':10,
               'color':11, 'visvis':12, 'audiovis':13, 'arithmetic':14,
               'image':15, 'visaudio':16, 'audio2':17, 'position2':18,
               'position3':19, 'position4':20, 'vis1':21, 'vis2':22, 'vis3':23,
               'vis4':24}

        if os.path.isfile(os.path.join(get_data_dir(), cfg.STATSFILE)):
            try:
                statsfile_path = os.path.join(get_data_dir(), cfg.STATSFILE)
                statsfile = open(statsfile_path, 'r')
                for line in statsfile:
                    if line == '': continue
                    if line == '\n': continue
                    if line[0] not in '0123456789': continue
                    datestamp = date(int(line[:4]), int(line[5:7]), int(line[8:10]))
                    hour = int(line[11:13])
                    if hour < cfg.ROLLOVER_HOUR:
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
                    newback = int(newline[4])

                    while len(newline) < 24:
                        newline.append('0') # make it work for image mode, missing visaudio and audio2
                    if len(newline) >= 16:
                        for m in mode.modalities[newmode]:
                            self.percents[newmode][m].append(int(newline[ind[m]]))

                    dictionary = self.dictionaries[newmode]
                    if datestamp not in dictionary:
                        dictionary[datestamp] = []
                    dictionary[datestamp].append([newback] + [int(newline[2])] + \
                        [self.percents[newmode][n][-1] for n in mode.modalities[newmode]])

                statsfile.close()
            except:
                quit_with_error(_('Error parsing stats file\n %s') %
                                os.path.join(get_data_dir(), cfg.STATSFILE),
                                _('Please fix, delete or rename the stats file.'))

            def mean(x):
                if len(x):
                    return sum(x)/float(len(x))
                else:
                    return 0.
            def cent(x):
                return map(lambda y: .01*y, x)

            for dictionary in self.dictionaries.values():
                for datestamp in list(dictionary): # this would be so much easier with numpy
                    entries = dictionary[datestamp]
                    if self.styles[self.style] == 'N':
                        scores = [entry[0] for entry in entries]
                    elif self.styles[self.style] == '%':
                        scores = [.01*entry[1] for entry in entries]
                    elif self.styles[self.style] == 'N.%':
                        scores = [entry[0] + .01*entry[1] for entry in entries]
                    elif self.styles[self.style] == 'N+2*%-1':
                        scores = [entry[0] - 1 + 2*.01*entry[1] for entry in entries]
                    elif self.styles[self.style] == 'N+10/3+4/3':
                        adv, flb = get_threshold_advance(), get_threshold_fallback()
                        m = 1./(adv - flb)
                        b = -m*flb
                        scores = [entry[0] + b + m*(entry[1]) for entry in entries]
                    dictionary[datestamp] = (mean(scores), max(scores))

            for game in self.percents:
                for category in self.percents[game]:
                    pcts = self.percents[game][category][-50:]
                    if not pcts:
                        self.percents[game][category].append(0)
                    else:
                        self.percents[game][category].append(sum(pcts)/len(pcts))

    #def export_data(self):
        #dictionary = {}
        #for x in self.dictionaries: # cycle through game modes
            #chartfile_name = CHARTFILE[x]
            #dictionary = self.dictionaries[x]
            #output = ['Date\t%s N-Back Average\n' % mode.long_mode_names[x]]

            #keyslist = list(dictionary)
            #keyslist.sort()
            #if len(keyslist) == 0: continue
            #for datestamp in keyslist:
                #if dictionary[datestamp] == (-1, -1):
                    #continue
                #output.append(str(datestamp))
                #output.append('\t')
                #output.append(str(dictionary[datestamp]))
                #output.append('\n')

            #try:
                #chartfile_path = os.path.join(get_data_dir(), chartfile_name)
                #chartfile = open(chartfile_path, 'w')
                #chartfile.write(''.join(output))
                #chartfile.close()

            #except:
                #quit_with_error('Error writing chart file:\n%s' %
                                #os.path.join(get_data_dir(), chartfile_name))


    def draw(self):
        if not self.batch:
            self.create_batch()
        else:
            self.batch.draw()

    def create_batch(self):
        self.batch = pyglet.graphics.Batch()

        linecolor = (0, 0, 255)
        linecolor2 = (255, 0, 0)
        if cfg.BLACK_BACKGROUND:
            axiscolor = (96, 96, 96)
            minorcolor = (64, 64, 64)
        else:
            axiscolor = (160, 160, 160)
            minorcolor = (224, 224, 224)
        y_marking_interval = 0.25 # This doesn't need scaling
        x_label_width      = 20   # TODO does this need to be scaled too?

        height = int(window.height * 0.625)
        width = int(window.width * 0.625)
        center_x = width_center()
        center_y = from_height_center(20)
        left   = center_x - width  // 2
        right  = center_x + width  // 2
        top    = center_y + height // 2
        bottom = center_y - height // 2
        try:
            dictionary = self.dictionaries[self.graph]
        except:
            print(self.graph)
        graph_title = mode.long_mode_names[self.graph] + _(' N-Back')

        if have_shapes:
            pyglet.shapes.Line(left, top, left, bottom, color=axiscolor, batch=self.batch)
            pyglet.shapes.Line(left, bottom, right, bottom, color=axiscolor, batch=self.batch)
        else:
            self.batch.add(3, pyglet.gl.GL_LINE_STRIP,
                pyglet.graphics.OrderedGroup(order=1), ('v2i', (
                left, top,
                left, bottom,
                right, bottom)), ('c3B', axiscolor * 3))

        pyglet.text.Label(
            _('G: Return to Main Screen\n\nN: Next Game Type'),
            batch=self.batch,
            multiline = True, width = scale_to_width(300),
            font_size=calc_fontsize(9),
            color=cfg.COLOR_TEXT,
            x=from_left_edge(10), y=from_top_edge(10),
            anchor_x='left', anchor_y='top')

        pyglet.text.Label(graph_title,
            batch=self.batch,
            font_size=calc_fontsize(18), bold=True, color=cfg.COLOR_TEXT,
            x = center_x, y = top + scale_to_height(60),
            anchor_x = 'center', anchor_y = 'center')

        pyglet.text.Label(_('Date'),
            batch=self.batch,
            font_size=calc_fontsize(12), bold=True, color=cfg.COLOR_TEXT,
            x = center_x, y = bottom - scale_to_height(80),
            anchor_x = 'center', anchor_y = 'center')

        pyglet.text.Label(_('Maximum'), width=scale_to_width(1),
            batch=self.batch,
            font_size=calc_fontsize(12), bold=True, color=linecolor2+(255,),
            x = left - scale_to_width(60), y = center_y + scale_to_height(50),
            anchor_x = 'right', anchor_y = 'center')

        pyglet.text.Label(_('Average'), width=scale_to_width(1),
            batch=self.batch,
            font_size=calc_fontsize(12), bold=True, color=linecolor+(255,),
            x = left - scale_to_width(60), y = center_y + scale_to_height(25),
            anchor_x = 'right', anchor_y = 'center')

        pyglet.text.Label(_('Score'), width=scale_to_width(1),
            batch=self.batch,
            font_size=calc_fontsize(12), bold=True, color=cfg.COLOR_TEXT,
            x = left - scale_to_width(60), y = center_y,
            anchor_x = 'right', anchor_y = 'center')

        dates = list(dictionary)
        dates.sort()
        if len(dates) < 2:
            pyglet.text.Label(_('Insufficient data: two days needed'),
                batch=self.batch,
                font_size=calc_fontsize(12), bold = True, color = axiscolor + (255,),
                x = center_x, y = center_y,
                anchor_x = 'center', anchor_y = 'center')
            return

        ymin = 100000.0
        ymax = 0.0
        for entry in dates:
            if dictionary[entry] == (-1, -1):
                continue
            if dictionary[entry][0] < ymin:
                ymin = dictionary[entry][0]
            if dictionary[entry][1] > ymax:
                ymax = dictionary[entry][1]
        if ymin == ymax:
            ymin = 0

        if preventMusicSkipping: pyglet.clock.tick(poll=True) # Prevent music skipping 1

        ymin = int(math.floor(ymin * 4))/4.
        ymax = int(math.ceil(ymax * 4))/4.

        # remove these two lines to revert to the old behaviour
        #ymin = 1.0
        #ymax += 0.25

        # add intermediate days
        z = 0
        while z < len(dates) - 1:
            if dates[z+1].toordinal() > dates[z].toordinal() + 1:
                newdate = date.fromordinal(dates[z].toordinal() + 1)
                dates.insert(z+1, newdate)
                dictionary[newdate] = (-1, -1)
            z += 1

        avgpoints = []
        maxpoints = []

        xinterval = width / (float(len(dates) - 1))
        skip_x = int(x_label_width // xinterval)

        for index in range(len(dates)):
            x = int(xinterval * index + left)
            if dictionary[dates[index]][0] != -1:
                avgpoints.extend([x, int((dictionary[dates[index]][0] - ymin)/(ymax - ymin) * height + bottom)])
                maxpoints.extend([x, int((dictionary[dates[index]][1] - ymin)/(ymax - ymin) * height + bottom)])
            datestring = str(dates[index])[2:]
            # If more than 10 dates, don't separate by '-' but by newlines so
            # they appear vertically rather than 01-01-01
            if 10 < len(dates):
                datestring = datestring.replace('-', '\n')
            if not index % (skip_x + 1):
                pyglet.text.Label(datestring, multiline=True, width=scale_to_width(12),
                    batch=self.batch,
                    font_size=calc_fontsize(8), bold=True, color=cfg.COLOR_TEXT,
                    x=x, y=bottom - scale_to_height(15),
                    anchor_x='center', anchor_y='top')
                if have_shapes:
                    pyglet.shapes.Line(x, bottom, x, top, color=minorcolor, batch=self.batch)
                    pyglet.shapes.Line(x, bottom - scale_to_height(10), x, bottom, color=minorcolor, batch=self.batch)
                else:
                    self.batch.add(2, pyglet.gl.GL_LINES,
                        pyglet.graphics.OrderedGroup(order=0), ('v2i', (
                        x, bottom,
                        x, top)), ('c3B', minorcolor * 2))
                    self.batch.add(2, pyglet.gl.GL_LINES,
                        pyglet.graphics.OrderedGroup(order=1), ('v2i', (
                        x, bottom - scale_to_height(10),
                        x, bottom)), ('c3B', axiscolor * 2))

        if preventMusicSkipping: pyglet.clock.tick(poll=True) # Prevent music skipping 2

        y_marking = ymin
        while y_marking <= ymax:
            y = int((y_marking - ymin)/(ymax - ymin) * height + bottom)
            pyglet.text.Label(str(round(y_marking, 2)),
                batch=self.batch,
                font_size=calc_fontsize(10), bold=False, color=cfg.COLOR_TEXT,
                x = left - scale_to_width(30), y = y + scale_to_width(1),
                anchor_x = 'center', anchor_y = 'center')
            if have_shapes:
                pyglet.shapes.Line(left, y, right, y, color=minorcolor, batch=self.batch)
                pyglet.shapes.Line(left - scale_to_width(10), y, left, y, color=minorcolor, batch=self.batch)
            else:
                self.batch.add(2, pyglet.gl.GL_LINES,
                    pyglet.graphics.OrderedGroup(order=0), ('v2i', (
                    left, y,
                    right, y)), ('c3B', minorcolor * 2))
                self.batch.add(2, pyglet.gl.GL_LINES,
                    pyglet.graphics.OrderedGroup(order=1), ('v2i', (
                    left - scale_to_width(10), y,
                    left, y)), ('c3B', axiscolor * 2))
            y_marking += y_marking_interval

        if have_shapes:
            for index in range(len(avgpoints) // 2 - 1):
                pyglet.shapes.Line(avgpoints[index], avgpoints[index + 1], avgpoints[index + 2], avgpoints[index + 3], batch=self.batch)
        else:
            self.batch.add(len(avgpoints) // 2, pyglet.gl.GL_LINE_STRIP,
                pyglet.graphics.OrderedGroup(order=2), ('v2i',
                avgpoints),
                ('c3B', linecolor * (len(avgpoints) // 2)))
            self.batch.add(len(maxpoints) // 2, pyglet.gl.GL_LINE_STRIP,
                pyglet.graphics.OrderedGroup(order=3), ('v2i',
                maxpoints),
                ('c3B', linecolor2 * (len(maxpoints) // 2)))

        if preventMusicSkipping: pyglet.clock.tick(poll=True) # Prevent music skipping 3

        radius = scale_to_height(3)
        o = 4
        for index in range(0, len(avgpoints) // 2):
            x = avgpoints[index * 2]
            avg = avgpoints[index * 2 + 1]
            maxp = maxpoints[index * 2 + 1]
            # draw average
            if have_shapes:
                pyglet.shapes.Polygon((x - radius, avg - radius), (x - radius, avg + radius), (x + radius, avg + radius), (x + radius, avg - radius), color=linecolor, batch=self.batch)
            else:
                self.batch.add(4, pyglet.gl.GL_POLYGON,
                    pyglet.graphics.OrderedGroup(order=o), ('v2i',
                    (x - radius, avg - radius,
                    x - radius, avg + radius,
                    x + radius, avg + radius,
                    x + radius, avg - radius)),
                    ('c3B', linecolor * 4))
            o += 1
            # draw maximum
            if have_shapes:
                pyglet.shapes.Polygon((x - radius, maxp - radius), (x - radius, maxp + radius), (x + radius, maxp + radius), (x + radius, maxp - radius), color=linecolor, batch=self.batch)
            else:
                self.batch.add(4, pyglet.gl.GL_POLYGON,
                    pyglet.graphics.OrderedGroup(order=o), ('v2i',
                    (x - radius, maxp - radius,
                    x - radius, maxp + radius,
                    x + radius, maxp + radius,
                    x + radius, maxp - radius)),
                    ('c3B', linecolor2 * 4))
            o += 1

        if preventMusicSkipping: pyglet.clock.tick(poll=True) # Prevent music skipping 4

        labelstrings = {'position1':_('Position: ')  , 'position2':_('Position 2: '),
                        'position3':_('Position 3: '), 'position4':_('Position 4: '),
                        'vis1':_('Color/Image 1: '), 'vis2':_('Color/Image 2: '),
                        'vis3':_('Color/Image 3: '), 'vis4':_('Color/Image 4: '),
                        'visvis':_('Vis & nvis: '), 'visaudio':_('Vis & n-sound: '),
                        'audiovis':_('Sound & n-vis: '), 'audio':_('Sound: '),
                        'color':_('Color: '), 'image':_('Image: '),
                        'arithmetic':_('Arithmetic: '), 'audio2':_('Sound2: ')}
        str_list = [_('Last 50 rounds:   ')]
        for m in mode.modalities[self.graph]:
            str_list.append(labelstrings[m] + '%i%% ' % self.percents[self.graph][m][-1]
                            + ' ' * (7-len(mode.modalities[self.graph])))

        pyglet.text.Label(''.join(str_list),
            batch=self.batch,
            font_size=calc_fontsize(11), bold = False, color = cfg.COLOR_TEXT,
            x = width_center(), y = scale_to_width(20),
            anchor_x = 'center', anchor_y = 'center')

class TextInputScreen:
    titlesize = calc_fontsize(18)
    textsize  = calc_fontsize(16)
    instance = None

    def __init__(self, title='', text='', callback=None, catch=''):
        self.titletext = title
        self.text = text
        self.starttext = text
        self.bgcolor = (255 * int(not cfg.BLACK_BACKGROUND), )*3
        self.textcolor = (255 * int(cfg.BLACK_BACKGROUND), )*3 + (255, )
        self.batch = pyglet.graphics.Batch()
        self.title = pyglet.text.Label(title, font_size=self.titlesize,
            bold=True, color=self.textcolor, batch=self.batch,
            x=width_center(), y=(window.height*9)/10,
            anchor_x='center', anchor_y='center')
        self.document = pyglet.text.document.UnformattedDocument()
        self.document.set_style(0, len(self.document.text), {'color': self.textcolor})
        self.layout = pyglet.text.layout.IncrementalTextLayout(self.document,
            (from_width_center(-20) - len(title) * calc_fontsize(6)), (window.height*10)/11, batch=self.batch, dpi=calc_dpi())
        self.layout.x = from_width_center(15) + len(title) * calc_fontsize(6)
        if not callback: callback = lambda x: x
        self.callback = callback
        self.caret = pyglet.text.caret.Caret(self.layout)
        window.push_handlers(self.caret)
        window.push_handlers(self.on_key_press, self.on_draw)
        self.document.text = text
        # workaround for a bug:  the keypress that spawns TextInputScreen doesn't
        # get handled until after the caret handler has been pushed, which seems
        # to result in the keypress being interpreted as a text input, so we
        # catch that later
        self.catch = catch
        self.instance = self


    def on_draw(self):
        # the bugfix hack, which currently does not work
        if self.catch and self.document.text == self.catch + self.starttext:
            self.document.text = self.starttext
            self.catch = ''
            self.caret.select_paragraph(600,0)

        window.clear()
        self.batch.draw()
        return pyglet.event.EVENT_HANDLED


    def on_key_press(self, k, mod):
        if k in (key.ESCAPE, key.RETURN, key.ENTER):
            if k is key.ESCAPE:
                self.text = self.starttext
            else:
                self.text = self.document.text
            window.pop_handlers()
            window.pop_handlers()
        self.callback(self.text.strip())
        return pyglet.event.EVENT_HANDLED


class Cycler:
    def __init__(self, values, default=0):
        self.values = values
        if type(default) is not int or default > len(values):
            default = values.index(default)
        self.i = default
    def choose(self, val):
        if val in self.values:
            self.i = self.values.index(val)
    def nxt(self): # not named "next" to prevent using a Cycler as an iterator, which would hang
        self.i = (self.i + 1) % len(self.values)
        return self.value()
    def value(self):
        return self.values[self.i]
    def __str__(self):
        return str(self.value())

class PercentCycler(Cycler):
    def __str__(self):
        v = self.value()
        if type(v) == float and (v < .1 or v > .9) and not v in (0., 1.):
            return "%2.2f%%" % (v*100.)
        else:
            return "%2.1f%%"   % (v*100.)

class Menu:
    """
    Menu.__init__(self, options, values={}, actions={}, names={}, title='',  choose_once=False,
                  default=0):

    A generic menu class.  The argument options is edited in-place.  Instancing
    the Menu displays the menu.  Menu will install its own event handlers for
    on_key_press, on_text, on_text_motion and on_draw, all of which
    do not pass events to later handlers on the stack.  When the user presses
    esc,  Menu pops its handlers off the stack. If the argument actions is used,
    it should be a dict with keys being options with specific actions, and values
    being a python callable which returns the new value for that option.

    """
    titlesize    = calc_fontsize(18)
    choicesize   = calc_fontsize(12)
    footnotesize = calc_fontsize(12)
    fontlist = ['Courier New', # try fixed width fonts first
                'Monospace', 'Terminal', 'fixed', 'Fixed', 'Times New Roman',
                'Helvetica', 'Arial']
    fontlist_serif = ['Times New Roman', 'Serif', 'Helvetica', 'Arial']
    instance = None


    def __init__(self, options, values=None, actions={}, names={}, title='',
                 footnote = _('Esc: cancel     Space: modify option     Enter: apply'),
                 choose_once=False, default=0):
        self.bgcolor = (255 * int(not cfg.BLACK_BACKGROUND), )*3
        self.textcolor = (255 * int(cfg.BLACK_BACKGROUND), )*3 + (255,)
        self.markercolors = (0,0,255,0,255,0,255,0,0)#(255 * int(cfg.BLACK_BACKGROUND), )*3*3
        self.pagesize = min(len(options), (window.height*6/10) / (self.choicesize*3/2))
        if type(options) == dict:
            vals = options
            self.options = list(options)
        else:
            vals = dict([[op, None] for op in options])
            self.options = options
        self.values = values or vals # use values if there's anything in it
        self.actions = actions
        for op in self.options:
            if not op in names.keys():
                names[op] = op
        self.names = names
        self.choose_once = choose_once
        self.disppos = 0 # which item in options is the first on the screen
        self.selpos = default # may be offscreen?
        self.batch = pyglet.graphics.Batch()

        self.title = pyglet.text.Label(title, font_size=self.titlesize,
            bold=True, color=self.textcolor, batch=self.batch,
            x=width_center(), y=(window.height*9)/10,
            anchor_x='center', anchor_y='center')
        self.footnote = pyglet.text.Label(footnote, font_size=self.footnotesize,
            bold=True, color=self.textcolor, batch=self.batch,
            x=width_center(), y=from_bottom_edge(35),
            anchor_x='center', anchor_y='center')

        self.labels = [pyglet.text.Label('', font_size=self.choicesize,
            bold=True, color=self.textcolor, batch=self.batch,
            x=window.width/8, y=(window.height*8)/10 - i*(self.choicesize*3/2),
            anchor_x='left', anchor_y='center', font_name=self.fontlist)
                       for i in range(self.pagesize)]

        if have_shapes:
            self.marker = pyglet.shapes.Polygon((0,0), (0,0), (0,0), color=[1] * 3, batch=self.batch)
        else:
            self.marker = self.batch.add(3, pyglet.gl.GL_POLYGON, None, ('v2i', (0,)*6,),
                ('c3B', self.markercolors))

        self.update_labels()

        window.push_handlers(self.on_key_press, self.on_text,
                             self.on_text_motion, self.on_draw)

        # keep a reference to the current instance as pyglet>=1.4 Window.push_handlers
        # only keep weak references to handlers so Menu subclasses will be deleted
        self.instance = self

    def textify(self, x):
        if type(x) == bool:
            return x and _('Yes') or _('No')
        return str(x)

    def update_labels(self):
        for l in self.labels: l.text = 'Hello, bug!'

        markerpos = self.selpos - self.disppos
        i = 0
        di = self.disppos
        if not di == 0: # displacement of i
            self.labels[i].text = '...'
            i += 1
        ending = int(di + self.pagesize < len(self.options))
        while i < self.pagesize-ending and i+self.disppos < len(self.options):
            k = self.options[i+di]
            if k == 'Blank line':
                self.labels[i].text = ''
            elif k in self.values.keys() and not self.values[k] == None:
                v = self.values[k]
                self.labels[i].text = '%s:%7s' % (self.names[k].ljust(52), self.textify(v))
            else:
                self.labels[i].text = self.names[k]
            i += 1
        if ending:
            self.labels[i].text = '...'
        w, h, cs = window.width, window.height, self.choicesize
        self.marker.vertices = [w//10, int((h*8)/10 - markerpos*(cs*3/2) + cs/2),
                                w//9,  int((h*8)/10 - markerpos*(cs*3/2)),
                                w//10, int((h*8)/10 - markerpos*(cs*3/2) - cs/2)]

    def move_selection(self, steps, relative=True):
        # FIXME:  pageup/pagedown can occasionally cause "Hello bug!" to be displayed
        if relative:
            self.selpos += steps
        else:
            self.selpos = steps
        self.selpos = min(len(self.options)-1, max(0, self.selpos))
        if self.disppos >= self.selpos and not self.disppos == 0:
            self.disppos = max(0, self.selpos-1)
        if self.disppos <= self.selpos - self.pagesize +1\
          and not self.disppos == len(self.options) - self.pagesize:
            self.disppos = max(0, min(len(self.options), self.selpos+1) - self.pagesize + 1)

        if not self.selpos in (0, len(self.options)-1) and self.options[self.selpos] == 'Blank line':
            self.move_selection(int(steps > 0)*2-1)
        self.update_labels()

    def on_key_press(self, sym, mod):
        if sym == key.ESCAPE:
            self.close()
        elif sym in (key.RETURN, key.ENTER):
            self.save()
            self.close()
        elif sym == key.SPACE:
            self.select()
        return pyglet.event.EVENT_HANDLED

    def select(self):
        k = self.options[self.selpos]
        i = self.selpos
        if k == "Blank line":
            pass
        elif k in self.actions.keys():
            self.values[k] = self.actions[k](k)
        elif type(self.values[k]) == bool:
            self.values[k] = not self.values[k]  # todo: other data types
        elif isinstance(self.values[k], Cycler):
            self.values[k].nxt()
        elif self.values[k] == None:
            self.choose(k, i)
            self.close()
        if self.choose_once:
            self.close()
        self.update_labels()

    def choose(self, k, i): # override this method in subclasses
        print("Thank you for beta-testing our software.")

    def close(self):
        return window.remove_handlers(self.on_key_press, self.on_text,
                                      self.on_text_motion, self.on_draw)

    def save(self):
        "Override me in subclasses."
        return

    def on_text_motion(self, evt):
        if evt == key.MOTION_UP:            self.move_selection(steps=-1)
        if evt == key.MOTION_DOWN:          self.move_selection(steps=1)
        if evt == key.MOTION_PREVIOUS_PAGE: self.move_selection(steps=-self.pagesize)
        if evt == key.MOTION_NEXT_PAGE:     self.move_selection(steps=self.pagesize)
        return pyglet.event.EVENT_HANDLED

    def on_text(self, evt):
        return pyglet.event.EVENT_HANDLED # todo: entering values after select()

    def on_draw(self):
        window.clear()
        self.batch.draw()
        return pyglet.event.EVENT_HANDLED

class MainMenu(Menu):
    def __init__(self):
        def NotImplemented():
            raise NotImplementedError
        ops = [('game', _('Choose Game Mode'), GameSelect),
               ('sounds', _('Choose Sounds'), SoundSelect),
               ('images', _('Choose Images'), ImageSelect),
               ('user', _('Choose User'), UserScreen),
               ('graph', _('Daily Progress Graph'), NotImplemented),
               ('help', _('Help / Tutorial'), NotImplemented),
               ('donate', _('Donate'), Notimplemented),
               ('forum', _('Go to Forum / Mailing List'), NotImplemented)]
        options =       [  op[0]         for op in ops]
        names   = dict( [ (op[0], op[1]) for op in ops])
        actions = dict( [ (op[0], op[2]) for op in ops])

class UserScreen(Menu):
    def __init__(self):

        self.users = users = [_("New user"), 'Blank line'] + get_users()
        Menu.__init__(self, options=users,
                      #actions=dict([(user, choose_user) for user in users]),
                      title=_("Please select your user profile"),
                      choose_once=True,
                      default=users.index(USER))

    def save(self):
        self.select() # Enter should choose a user too
        Menu.save(self)

    def choose(self, k, i):
        newuser = self.users[i]
        if newuser == _("New user"):
            # TODO Don't allow the user to create a username that's an empty string
            textInput = TextInputScreen(_("Enter new user name:"), USER, callback=set_user, catch=' ')
        else:
            set_user(newuser)

class LanguageScreen(Menu):
    def __init__(self):
        self.languages = languages = [fn for fn in os.listdir(os.path.join('res', 'i18n')) if fn.lower().endswith('mo')]
        try:
            default = languages.index(cfg.LANGUAGE + '.mo')
        except:
            default = 0
        Menu.__init__(self, options=languages,
                      title=_("Please select your preferred language"),
                      choose_once=True,
                      default=default)
    def save(self):
        self.select()
        Menu.save(self)

    def choose(self, k, i):
        newlang = self.languages[i]
        # set the new language here

class OptionsScreen(Menu):
    def __init__(self):
        """
        Sorta works.  Not yet useful, though.
        """
        options = list(cfg)
        options.sort()
        Menu.__init__(self, options=options, values=cfg, title=_('Configuration'))


class GameSelect(Menu):
    def __init__(self):
        modalities = ['position1', 'color', 'image', 'audio', 'audio2', 'arithmetic']
        options = modalities[:]
        names = dict([(m, _("Use %s") % m) for m in modalities])
        names['position1'] = _("Use position")
        options.extend(["Blank line", 'combination', "Blank line", 'variable',
            'crab', "Blank line", 'multi', 'multimode', 'Blank line',
            'selfpaced', "Blank line", 'interference'])
        names['combination'] = _('Combination N-back mode')
        names['variable'] = _('Use variable N-Back levels')
        names['crab'] = _('Crab-back mode (reverse order of sets of N stimuli)')
        names['multi'] = _('Simultaneous visual stimuli')
        names['multimode'] = _('Simultaneous stimuli differentiated by')
        names['selfpaced'] = _('Self-paced mode')
        names['interference'] = _('Interference (tricky stimulus generation)')
        vals = dict([[op, None] for op in options])
        curmodes = mode.modalities[mode.mode]
        interference_options = [i / 8. for i in range(0, 9)]
        if not cfg.DEFAULT_CHANCE_OF_INTERFERENCE in interference_options:
            interference_options.append(cfg.DEFAULT_CHANCE_OF_INTERFERENCE)
        interference_options.sort()
        if cfg.CHANCE_OF_INTERFERENCE in interference_options:
            interference_default = interference_options.index(cfg.CHANCE_OF_INTERFERENCE)
        else:
            interference_default = 3
        vals['interference'] = PercentCycler(values=interference_options, default=interference_default)
        vals['combination'] = 'visvis' in curmodes
        vals['variable'] = bool(cfg.VARIABLE_NBACK)
        vals['crab'] = bool(mode.flags[mode.mode]['crab'])
        vals['multi'] = Cycler(values=[1,2,3,4], default=mode.flags[mode.mode]['multi']-1)
        vals['multimode'] = Cycler(values=['color', 'image'], default=cfg.MULTI_MODE)
        vals['selfpaced'] = bool(mode.flags[mode.mode]['selfpaced'])
        for m in modalities:
            vals[m] = m in curmodes
        Menu.__init__(self, options, vals, names=names, title=_('Choose your game mode'))
        self.modelabel = pyglet.text.Label('', font_size=self.titlesize,
            bold=False, color=(0,0,0,255), batch=self.batch,
            x=width_center(), y=(window.height*1)/10,
            anchor_x='center', anchor_y='center')
        self.update_labels()
        self.newmode = mode.mode # self.newmode will be False if an invalid mode is chosen

    def update_labels(self):
        self.calc_mode()
        try:
            if self.newmode:
                self.modelabel.text = mode.long_mode_names[self.newmode] + \
                    (self.values['variable'] and ' V.' or '') + ' N-Back'
            else:
                self.modelabel.text = _("An invalid mode has been selected.")
        except AttributeError:
            pass
        Menu.update_labels(self)

    def calc_mode(self):
        modes = [k for (k, v) in self.values.items() if v and not isinstance(v, Cycler)]
        crab = 'crab' in modes
        if 'variable' in modes:  modes.remove('variable')
        if 'combination' in modes:
            modes.remove('combination')
            modes.extend(['visvis', 'visaudio', 'audiovis']) # audio should already be there
        base = 0
        base += 256 * (self.values['multi'].value()-1)
        if 'crab' in modes:
            modes.remove('crab')
            base += 128
        if 'selfpaced' in modes:
            modes.remove('selfpaced')
            base += 1024

        candidates = set([k for k,v in mode.modalities.items() if not
                         [True for m in modes if not m in v] and not
                         [True for m in v if not m in modes]])
        candidates = candidates & set(range(0, 128))
        if len(candidates) == 1:
            candidate = list(candidates)[0] + base
            if candidate in mode.modalities:
                self.newmode = candidate
            else: self.newmode = False
        else:
            if DEBUG: print(candidates, base)
            self.newmode = False

    def close(self):
        Menu.close(self)
        if not mode.manual:
            mode.enforce_standard_mode()
            stats.retrieve_progress()
        update_all_labels()
        circles.update()

    def save(self):
        self.calc_mode()
        cfg.VARIABLE_NBACK = self.values['variable']
        cfg.MULTI_MODE = self.values['multimode'].value()
        cfg.CHANCE_OF_INTERFERENCE = self.values['interference'].value()
        if self.newmode:
            mode.mode = self.newmode


    def select(self):
        choice = self.options[self.selpos]
        if choice == 'combination':
            self.values['arithmetic'] = False
            self.values['image']      = False
            self.values['audio2']     = False
            self.values['audio']      = True
            self.values['multi'].i    = 0 # no multi mode
        elif choice == 'arithmetic':
            self.values['image']       = False
            self.values['audio']       = False
            self.values['audio2']      = False
            self.values['combination'] = False
            self.values['multi'].i     = 0
        elif choice == 'audio':
            self.values['arithmetic'] = False
            if self.values['audio']:
                self.values['combination'] = False
                self.values['audio2']      = False
        elif choice == 'audio2':
            self.values['audio']       = True
            self.values['combination'] = False
            self.values['arithmetic']  = False
        elif choice == 'image':
            self.values['combination'] = False
            self.values['arithmetic'] = False
            if self.values['multi'].value() > 1 and not self.values['image']:
                self.values['color'] = False
                self.values['multimode'].choose('color')
        elif choice == 'color':
            if self.values['multi'].value() > 1 and not self.values['color']:
                self.values['image'] = False
                self.values['multimode'].choose('image')
        elif choice == 'multi':
            self.values['arithmetic'] = False
            self.values['combination'] = False
            self.values[self.values['multimode'].value()] = False
        elif choice == 'multimode' and self.values['multi'].value() > 1:
            mm = self.values['multimode'].value() # what we're changing from
            notmm = (mm == 'image') and 'color' or 'image' # changing to
            self.values[mm] = self.values[notmm]
            self.values[notmm] = False


        Menu.select(self)
        modes = [k for k,v in self.values.items() if v]
        if not [v for k,v in self.values.items()
                  if v and not k in ('crab', 'combination', 'variable')] \
           or len(modes) == 1 and modes[0] in ['image', 'color']:
            self.values['position1'] = True
            self.update_labels()
        self.calc_mode()

class ImageSelect(Menu):
    def __init__(self):
        imagesets = resourcepaths['sprites']
        self.new_sets = {}
        for image in imagesets:
            self.new_sets[image] = image in cfg.IMAGE_SETS
        options = list(self.new_sets)
        options.sort()
        vals = self.new_sets
        Menu.__init__(self, options, vals, title=_('Choose images to use for the Image n-back tasks.'))

    def close(self):
        while cfg.IMAGE_SETS:
            cfg.IMAGE_SETS.remove(cfg.IMAGE_SETS[0])
        for k,v in self.new_sets.items():
            if v: cfg.IMAGE_SETS.append(k)
        Menu.close(self)
        update_all_labels()

    def select(self):
        Menu.select(self)
        if not [val for val in self.values.values() if (val and not isinstance(val, Cycler))]:
            i = 0
            if self.selpos == 0:
                i = random.randint(1, len(self.options)-1)
            self.values[self.options[i]] = True
            self.update_labels()

class SoundSelect(Menu):
    def __init__(self):
        audiosets = resourcepaths['sounds'] # we don't want to delete 'operations' from resourcepaths['sounds']
        self.new_sets = {}
        for audio in audiosets:
            if not audio == 'operations':
                self.new_sets['1'+audio] = audio in cfg.AUDIO1_SETS
                self.new_sets['2'+audio] = audio in cfg.AUDIO2_SETS
        for audio in audiosets:
            if not audio == 'operations':
                self.new_sets['2'+audio] = audio in cfg.AUDIO2_SETS
        options = list(self.new_sets)
        options.sort()
        options.insert(len(self.new_sets)//2, "Blank line") # Menu.update_labels and .select will ignore this
        options.append("Blank line")
        options.extend(['cfg.CHANNEL_AUDIO1', 'cfg.CHANNEL_AUDIO2'])
        lcr = ['left', 'right', 'center']
        vals = self.new_sets
        vals['cfg.CHANNEL_AUDIO1'] = Cycler(lcr, default=lcr.index(cfg.CHANNEL_AUDIO1))
        vals['cfg.CHANNEL_AUDIO2'] = Cycler(lcr, default=lcr.index(cfg.CHANNEL_AUDIO2))
        names = {}
        for op in options:
            if op.startswith('1') or op.startswith('2'):
                names[op] = _("Use sound set '%s' for channel %s") % (op[1:], op[0])
            elif 'CHANNEL_AUDIO' in op:
                names[op] = 'Channel %i is' % (op[-1]=='2' and 2 or 1)
        Menu.__init__(self, options, vals, {}, names, title=_('Choose sound sets to Sound n-back tasks.'))

    def close(self):
        cfg.AUDIO1_SETS = []
        cfg.AUDIO2_SETS = []
        for k,v in self.new_sets.items():
            if   k.startswith('1') and v: cfg.AUDIO1_SETS.append(k[1:])
            elif k.startswith('2') and v: cfg.AUDIO2_SETS.append(k[1:])
        cfg.CHANNEL_AUDIO1  = self.values['cfg.CHANNEL_AUDIO1'].value()
        cfg.CHANNEL_AUDIO2 = self.values['cfg.CHANNEL_AUDIO2'].value()
        Menu.close(self)
        update_all_labels()

    def select(self):
        Menu.select(self)
        for c in ('1', '2'):
            if not [v for k,v in self.values.items() if (k.startswith(c) and v and not isinstance(v, Cycler))]:
                options = list(resourcepaths['sounds'])
                options.remove('operations')
                i = 0
                if self.selpos == 0:
                    i = random.randint(1, len(options)-1)
                elif self.selpos==len(options)+1:
                    i = random.randint(len(options)+2, 2*len(options))
                elif self.selpos > len(options)+1:
                    i = len(options)+1
                self.values[self.options[i]] = True
            self.update_labels()

# this class controls the field.
# the field is the grid on which the squares appear
class Field:
    def __init__(self):
        if cfg.FIELD_EXPAND:
            self.size = int(window.height * 0.85)
        else: self.size = int(window.height * 0.625)
        if cfg.BLACK_BACKGROUND:
            self.color = (64, 64, 64)
        else:
            self.color = (192, 192, 192)
        self.color4 = self.color * 4
        self.color8 = self.color * 8
        self.center_x = width_center()
        if cfg.FIELD_EXPAND:
            self.center_y = height_center()
        else:
            self.center_y = from_height_center(20)
        self.x1 = int(self.center_x - self.size/2)
        self.x2 = int(self.center_x + self.size/2)
        self.x3 = int(self.center_x - self.size/6)
        self.x4 = int(self.center_x + self.size/6)
        self.y1 = int(self.center_y - self.size/2)
        self.y2 = int(self.center_y + self.size/2)
        self.y3 = int(self.center_y - self.size/6)
        self.y4 = int(self.center_y + self.size/6)

        # add the inside lines
        if cfg.GRIDLINES:
            if have_shapes:
                self.v_lines = [pyglet.shapes.Line(self.x1, self.y3, self.x2, self.y3, color=self.color, batch=batch),
                                pyglet.shapes.Line(self.x1, self.y4, self.x2, self.y4, color=self.color, batch=batch),
                                pyglet.shapes.Line(self.x3, self.y1, self.x3, self.y2, color=self.color, batch=batch),
                                pyglet.shapes.Line(self.x4, self.y1, self.x4, self.y2, color=self.color, batch=batch)]
            else:
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
        if not cfg.CROSSHAIRS:
            return
        if (not mode.paused) and 'position1' in mode.modalities[mode.mode] and not cfg.VARIABLE_NBACK:
            if not self.crosshair_visible:
                length_of_crosshair = scale_to_height(8)
                if have_shapes:
                    self.v_crosshair = [pyglet.shapes.Line(self.center_x - length_of_crosshair, self.center_y,
                                                           self.center_x + length_of_crosshair, self.center_y,
                                                           color=self.color, batch=batch),
                                        pyglet.shapes.Line(self.center_x, self.center_y - length_of_crosshair,
                                                           self.center_x, self.center_y + length_of_crosshair,
                                                           color=self.color, batch=batch)]
                else:
                    self.v_crosshair = batch.add(4, pyglet.gl.GL_LINES, None, ('v2i', (
                        self.center_x - length_of_crosshair, self.center_y,
                        self.center_x + length_of_crosshair, self.center_y,
                        self.center_x, self.center_y - length_of_crosshair,
                        self.center_x, self.center_y + length_of_crosshair)), ('c3B', self.color4))
                self.crosshair_visible = True
        else:
            if self.crosshair_visible:
                if have_shapes:
                    for i in range(2):
                        self.v_crosshair[i].delete()
                else:
                    self.v_crosshair.delete()
                self.crosshair_visible = False


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

        self.spr_square = [pyglet.sprite.Sprite(pyglet.image.load(path))
                              for path in resourcepaths['misc']['colored-squares']]
        self.spr_square_size = self.spr_square[0].width

        if cfg.ANIMATE_SQUARES:
            self.size_factor = 0.9375
        elif cfg.OLD_STYLE_SQUARES:
            self.size_factor = 0.9375
        else:
            self.size_factor = 1.0
        self.size = int(field.size / 3 * self.size_factor)

        # load an image set
        self.load_set()

    def load_set(self, index=None):
        if type(index) == int:
            index = cfg.IMAGE_SETS[index]
        if index == None:
            index = random.choice(cfg.IMAGE_SETS)
        if hasattr(self, 'image_set_index') and index == self.image_set_index:
            return
        self.image_set_index = index
        self.image_set = [pyglet.sprite.Sprite(pyglet.image.load(path))
                            for path in resourcepaths['sprites'][index]]
        self.image_set_size = self.image_set[0].width

    def choose_random_images(self, number):
        self.image_indices = random.sample(range(len(self.image_set)), number)
        self.images = random.sample(self.image_set, number)

    def choose_indicated_images(self, indices):
        self.image_indices = indices
        self.images = [self.image_set[i] for i in indices]

    def spawn(self, position=0, color=1, vis=0, number=-1, operation='none', variable = 0):
        self.position = position
        self.color = get_color(color)
        self.vis = vis

        self.center_x = field.center_x + (field.size // 3)*((position+1)%3 - 1) + (field.size // 3 - self.size)//2
        self.center_y = field.center_y + (field.size // 3)*((position//3+1)%3 - 1) + (field.size // 3 - self.size)//2

        if self.vis == 0:
            if cfg.OLD_STYLE_SQUARES:
                lx = self.center_x - self.size // 2 + 2
                rx = self.center_x + self.size // 2 - 2
                by = self.center_y - self.size // 2 + 2
                ty = self.center_y + self.size // 2 - 2
                cr = self.size // 5

                if cfg.OLD_STYLE_SHARP_CORNERS:
                    self.square = batch.add(4, pyglet.gl.GL_POLYGON, None, ('v2i', (
                        lx, by,
                        rx, by,
                        rx, ty,
                        lx, ty,)),
                        ('c4B', self.color * 4))
                else:
                    #rounded corners: bottom-left, bottom-right, top-right, top-left
                    x = ([lx + int(cr*(1-math.cos(math.radians(i)))) for i in range(0, 91, 10)] +
                         [rx - int(cr*(1-math.sin(math.radians(i)))) for i in range(0, 91, 10)] +
                         [rx - int(cr*(1-math.sin(math.radians(i)))) for i in range(90, -1, -10)] +
                         [lx + int(cr*(1-math.cos(math.radians(i)))) for i in range(90, -1, -10)])

                    y = ([by + int(cr*(1-math.sin(math.radians(i)))) for i in range(0, 91, 10) + range(90, -1, -10)] +
                         [ty - int(cr*(1-math.sin(math.radians(i)))) for i in range(0, 91, 10) + range(90, -1, -10)])
                    xy = []
                    for a,b in zip(x,y): xy.extend((a, b))

                    self.square = batch.add(40, pyglet.gl.GL_POLYGON, None,
                                            ('v2i', xy), ('c4B', self.color * 40))

            else:
                # use sprite squares
                self.square = self.spr_square[color-1]
                self.square.opacity = 255
                self.square.x = self.center_x - field.size // 6
                self.square.y = self.center_y - field.size // 6
                self.square.scale = 1.0 * self.size / self.spr_square_size
                self.square_size_scaled = self.square.width
                self.square.batch = batch

                # initiate square animation
                self.age = 0.0
                pyglet.clock.schedule_interval(self.animate_square, 1/60.)

        elif 'arithmetic' in mode.modalities[mode.mode]: # display a number
            self.label.text = str(number)
            self.label.x = self.center_x
            self.label.y = self.center_y + 4
            self.label.color = self.color
        elif 'visvis' in mode.modalities[mode.mode]: # display a letter
            self.label.text = self.letters[vis - 1].upper()
            self.label.x = self.center_x
            self.label.y = self.center_y + 4
            self.label.color = self.color
        elif 'image' in mode.modalities[mode.mode] \
              or 'vis1' in mode.modalities[mode.mode] \
              or (mode.flags[mode.mode]['multi'] > 1 and cfg.MULTI_MODE == 'image'): # display a pictogram
            self.square = self.images[vis-1]
            self.square.opacity = 255
            self.square.color = self.color[:3]
            self.square.x = self.center_x - field.size // 6
            self.square.y = self.center_y - field.size // 6
            self.square.scale = 1.0 * self.size / self.image_set_size
            self.square_size_scaled = self.square.width
            self.square.batch = batch

            # initiate square animation
            self.age = 0.0
            #self.animate_square(0)
            pyglet.clock.schedule_interval(self.animate_square, 1/60.)

        if variable > 0:
            # display variable n-back level
            self.variable_label.text = str(variable)

            if not 'position1' in mode.modalities[mode.mode]:
                self.variable_label.x = field.center_x
                self.variable_label.y = field.center_y - field.size//3 + 4
            else:
                self.variable_label.x = field.center_x
                self.variable_label.y = field.center_y + 4

            self.variable_label.color = self.color

        self.visible = True

    def animate_square(self, dt):
        self.age += dt
        if mode.paused: return
        if not cfg.ANIMATE_SQUARES: return

        # factors which affect animation
        scale_addition = dt / 8
        fade_begin_time = 0.4
        fade_end_time = 0.5
        fade_end_transparency = 1.0  # 1 = fully transparent, 0.5 = half transparent

        self.square.scale += scale_addition
        dx = (self.square.width - self.square_size_scaled) // 2
        self.square.x = self.center_x - field.size // 6 - dx
        self.square.y = self.center_y - field.size // 6 - dx

        if self.age > fade_begin_time:
            factor = (1.0 - fade_end_transparency * (self.age - fade_begin_time) / (fade_end_time - fade_begin_time))
            if factor > 1.0: factor = 1.0
            if factor < 0.0: factor = 0.0
            self.square.opacity = int(255 * factor)

    def hide(self):
        if self.visible:
            self.label.text = ''
            self.variable_label.text = ''
            if 'image' in mode.modalities[mode.mode] \
                  or 'vis1' in mode.modalities[mode.mode] \
                  or (mode.flags[mode.mode]['multi'] > 1 and cfg.MULTI_MODE == 'image'): # hide pictogram
                self.square.batch = None
                pyglet.clock.unschedule(self.animate_square)
            elif self.vis == 0:
                if cfg.OLD_STYLE_SQUARES:
                    self.square.delete()
                else:
                    self.square.batch = None
                    pyglet.clock.unschedule(self.animate_square)
            self.visible = False

# Circles is the 3-strikes indicator in the top left corner of the screen.
class Circles:
    def __init__(self):
        self.y        = from_top_edge(20)
        self.start_x  = from_left_edge(30)
        self.radius   = scale_to_width(8)
        self.distance = scale_to_width(20)
        if cfg.BLACK_BACKGROUND:
            self.not_activated = [64, 64, 64, 255]
        else:
            self.not_activated = [192, 192, 192, 255]
        self.activated = [64, 64, 255, 255]
        if cfg.BLACK_BACKGROUND:
            self.invisible = [0, 0, 0, 0]
        else:
            self.invisible = [255, 255, 255, 0]

        self.circle = []
        for index in range(0, cfg.THRESHOLD_FALLBACK_SESSIONS - 1):
            if have_shapes:
                self.circle.append([pyglet.shapes.Rectangle(self.start_x + self.distance * index - self.radius,
                                                            self.y + self.radius,
                                                            self.start_x + self.distance * index + self.radius,
                                                            self.y + self.radius,
                                                            color=self.not_activated[:3], batch=batch),
                                    pyglet.shapes.Rectangle(self.start_x + self.distance * index + self.radius,
                                                            self.y - self.radius,
                                                            self.start_x + self.distance * index - self.radius,
                                                            self.y - self.radius,
                                                            color=self.not_activated[:3], batch=batch)])
            else:
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
        if mode.manual or mode.started or cfg.JAEGGI_MODE:
            for i in range(0, cfg.THRESHOLD_FALLBACK_SESSIONS - 1):
                if have_shapes:
                    for j in range(2):
                        self.circle[i][j].colors = (self.invisible * 4)
                else:
                    self.circle[i].colors = (self.invisible * 4)
        else:
            for i in range(0, cfg.THRESHOLD_FALLBACK_SESSIONS - 1):
                if have_shapes:
                    for j in range(2):
                        self.circle[i][j].colors = (self.not_activated * 4)
                else:
                    self.circle[i].colors = (self.not_activated * 4)
            for i in range(0, mode.progress):
                if have_shapes:
                    for j in range(2):
                        self.circle[i][j].colors = (self.activated * 4)
                else:
                    self.circle[i].colors = (self.activated * 4)


# this is the update notification
class UpdateLabel:
    def __init__(self):
        # Some versions don't accept the align argument and some don't accept halign.
        # So try with one and if that fails use the other.
        try:
            self.label = pyglet.text.Label(
                '',
                multiline = True, width = field.size//3 - 4, align='middle',
                font_size=calc_fontsize(11), bold=True,
                color=(0, 128, 0, 255),
                x=width_center(), y=field.center_x + field.size // 6,
                anchor_x='center', anchor_y='center', batch=batch)
        except:
            self.label = pyglet.text.Label(
                '',
                multiline = True, width = field.size//3 - 4, halign='middle',
                font_size=calc_fontsize(11), bold=True,
                color=(0, 128, 0, 255),
                x=width_center(), y=field.center_x + field.size // 6,
                anchor_x='center', anchor_y='center', batch=batch)
        self.update()
    def update(self):
        if not mode.started and update_available:
            str_list = []
            str_list.append(_('An update is available ('))
            str_list.append(str(update_version))
            str_list.append(_('). Press W to open web site'))
            self.label.text = ''.join(str_list)
        else: self.label.text = ''

# this is the black text above the field
class GameModeLabel:
    def __init__(self):
        self.label = pyglet.text.Label(
            '',
            font_size=calc_fontsize(16),
            color=cfg.COLOR_TEXT,
            x=width_center(), y=from_top_edge(20),
            anchor_x='center', anchor_y='center', batch=batch)
        self.update()
    def update(self):
        if mode.started and mode.hide_text:
            self.label.text = ''
        else:
            str_list = []
            if cfg.JAEGGI_MODE and not CLINICAL_MODE:
                str_list.append(_('Jaeggi mode: '))
            if mode.manual:
                str_list.append(_('Manual mode: '))
            str_list.append(mode.long_mode_names[mode.mode] + ' ')
            if cfg.VARIABLE_NBACK:
                str_list.append(_('V. '))
            str_list.append(str(mode.back))
            str_list.append(_('-Back'))
            self.label.text = ''.join(str_list)

    def flash(self):
        pyglet.clock.unschedule(gameModeLabel.unflash)
        self.label.color = (255,0 , 255, 255)
        self.update()
        pyglet.clock.schedule_once(gameModeLabel.unflash, 0.5)
    def unflash(self, dt):
        self.label.color = cfg.COLOR_TEXT
        self.update()

class JaeggiWarningLabel:
    def __init__(self):
        self.label = pyglet.text.Label(
            '',
            font_size=calc_fontsize(12), bold = True,
            color=(255, 0, 255, 255),
            x=width_center(), y=field.center_x + field.size // 3 + 8,
            anchor_x='center', anchor_y='center', batch=batch)

    def show(self):
        pyglet.clock.unschedule(jaeggiWarningLabel.hide)
        self.label.text = _('Please disable Jaeggi Mode to access additional modes.')
        pyglet.clock.schedule_once(jaeggiWarningLabel.hide, 3.0)
    def hide(self, dt):
        self.label.text = ''

# this is the keyboard reference list along the left side
class KeysListLabel:
    def __init__(self):
        self.label = pyglet.text.Label(
            '',
            multiline = True, width = scale_to_width(300), bold = False,
            font_size=calc_fontsize(9),
            color=cfg.COLOR_TEXT,
            x = scale_to_width(10), y = from_top_edge(30),
            anchor_x='left', anchor_y='top', batch=batch)
        self.update()
    def update(self):
        str_list = []
        if mode.started:
            self.label.y = from_top_edge(30)
            if not mode.hide_text:
                str_list.append(_('P: Pause / Unpause\n'))
                str_list.append('\n')
                str_list.append(_('F8: Hide / Reveal Text\n'))
                str_list.append('\n')
                str_list.append(_('ESC: Cancel Session\n'))
        elif CLINICAL_MODE:
            self.label.y = from_top_edge(30)
            str_list.append(_('ESC: Exit'))
        else:
            if mode.manual or cfg.JAEGGI_MODE:
                self.label.y = from_top_edge(30)
            else:
                self.label.y = from_top_edge(40)
            if 'morse' in cfg.AUDIO1_SETS or 'morse' in cfg.AUDIO2_SETS:
                str_list.append(_('J: Morse Code Reference\n'))
                str_list.append('\n')
            str_list.append(_('H: Help / Tutorial\n'))
            str_list.append('\n')
            if mode.manual:
                str_list.extend([
                    _('F1: Decrease N-Back\n'),
                    _('F2: Increase N-Back\n'), '\n',
                    _('F3: Decrease Trials\n'),
                    _('F4: Increase Trials\n'), '\n'])
            if mode.manual:
                str_list.extend([
                    _('F5: Decrease Speed\n'),
                    _('F6: Increase Speed\n'), '\n',
                    _('C: Choose Game Type\n'),
                    _('S: Select Sounds\n')])
            str_list.append(_('I: Select Images\n'))
            if mode.manual:
                str_list.append(_('M: Standard Mode\n'))
            else:
                str_list.extend([
                    _('M: Manual Mode\n'),
                    _('D: Donate\n'), '\n',
                    _('G: Daily Progress Graph\n'), '\n',
                    _('W: Brain Workshop Web Site\n')])
            if cfg.WINDOW_FULLSCREEN:
                str_list.append(_('E: Saccadic Eye Exercise\n'))
            str_list.extend(['\n', _('ESC: Exit\n')])

        self.label.text = ''.join(str_list)

class TitleMessageLabel:
    def __init__(self):
        self.label = pyglet.text.Label(
            _('Brain Workshop'),
            #multiline = True, width = window.width // 2,
            font_size=calc_fontsize(32), bold = True, color = cfg.COLOR_TEXT,
            x = width_center(), y = from_top_edge(25),
            anchor_x = 'center', anchor_y = 'center')
        self.label2 = pyglet.text.Label(
            _('Version ') + str(VERSION),
            font_size=calc_fontsize(14), bold = False, color = cfg.COLOR_TEXT,
            x = width_center(), y = from_top_edge(55),
            anchor_x = 'center', anchor_y = 'center')

    def draw(self):
        self.label.draw()
        self.label2.draw()

class TitleKeysLabel:
    def __init__(self):
        str_list = []
        if not (cfg.JAEGGI_MODE or CLINICAL_MODE):
            str_list.append(_('C: Choose Game Mode\n'))
            str_list.append(_('S: Choose Sounds\n'))
            str_list.append(_('I: Choose Images\n'))
        if not CLINICAL_MODE:
            str_list.append(_('U: Choose User\n'))
            str_list.append(_('G: Daily Progress Graph\n'))
        str_list.append(_('H: Help / Tutorial\n'))
        if not CLINICAL_MODE:
            str_list.append(_('D: Donate\n'))
            str_list.append(_('F: Go to Forum / Mailing List\n'))
            str_list.append(_('O: Edit configuration file'))

        self.keys = pyglet.text.Label(
            ''.join(str_list),
            multiline = True, width = scale_to_width(260),
            font_size=calc_fontsize(12), bold = True, color = cfg.COLOR_TEXT,
            x = from_width_center(65), y = from_bottom_edge(230),
            anchor_x = 'center', anchor_y = 'top')

        self.space = pyglet.text.Label(
            _('Press SPACE to enter the Workshop'),
            font_size=calc_fontsize(20), bold = True, color = (32, 32, 255, 255),
            x = width_center(), y = from_bottom_edge(35),
            anchor_x = 'center', anchor_y = 'center')
    def draw(self):
        self.space.draw()
        self.keys.draw()


# this is the word "brain" above the brain logo.
class LogoUpperLabel:
    def __init__(self):
        self.label = pyglet.text.Label(
            'Brain', # I think we shouldn't translate the program name.  Yes?
            font_size=calc_fontsize(11), bold = True,
            color=cfg.COLOR_TEXT,
            x=field.center_x, y=field.center_y + scale_to_height(30),
            anchor_x='center', anchor_y='center')
    def draw(self):
        self.label.draw()

# this is the word "workshop" below the brain logo.
class LogoLowerLabel:
    def __init__(self):
        self.label = pyglet.text.Label(
            'Workshop',
            font_size=calc_fontsize(11), bold = True,
            color=cfg.COLOR_TEXT,
            x=field.center_x, y=field.center_y - scale_to_height(27),
            anchor_x='center', anchor_y='center')
    def draw(self):
        self.label.draw()

# this is the word "Paused" which appears when the game is paused.
class PausedLabel:
    def __init__(self):
        self.label = pyglet.text.Label(
            '',
            font_size=calc_fontsize(14),
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
            font_size=calc_fontsize(14),
            color=(255, 32, 32, 255),
            x=field.center_x, y=from_top_edge(47),
            anchor_x='center', anchor_y='center', batch=batch)
        self.update()
    def update(self, show=False, advance=False, fallback=False, awesome=False, great=False, good=False, perfect = False):
        str_list = []
        if show and not CLINICAL_MODE and cfg.USE_SESSION_FEEDBACK:
            if perfect: str_list.append(_('Perfect score! '))
            elif awesome: str_list.append(_('Awesome score! '))
            elif great: str_list.append(_('Great score! '))
            elif good: str_list.append(_('Not bad! '))
            else: str_list.append(_('Keep trying. You\'re getting there! '))
        if advance:
            str_list.append(_('N-Back increased'))
        elif fallback:
            str_list.append(_('N-Back decreased'))
        self.label.text = ''.join(str_list)

class FeedbackLabel:
    def __init__(self, modality, pos=0, total=1):
        """
        Generic text label for giving user feedback during N-back sessions.  All
        of the feedback labels should be instances of this class.

        pos should be which label number this one is displayed as (order: left-to-right).
        total should be the total number of feedback labels for this mode.
        """
        self.modality = modality
        self.letter = key.symbol_string(cfg['KEY_%s' % modality.upper()])
        if self.letter == 'SEMICOLON':
            self.letter = ';'
        modalityname = modality
        if modalityname.endswith('vis'):
            modalityname = modalityname[:-3] + ' & n-vis'
        elif modalityname.endswith('audio') and not modalityname == 'audio':
            modalityname = modalityname[:-5] + ' & n-audio'
        if mode.flags[mode.mode]['multi'] == 1 and modalityname == 'position1':
            modalityname = 'position'

        if total == 2 and not cfg.JAEGGI_MODE and cfg.ENABLE_MOUSE:
            if pos == 0:
                self.mousetext = "Left-click or"
            if pos == 1:
                self.mousetext = "Right-click or"
        else:
            self.mousetext = ""

        self.text = "%s %s: %s" % (_(self.mousetext), self.letter, _(modalityname)) # FIXME: will this break pyglettext?

        if total < 4:
            self.text += _(' match')
            font_size=calc_fontsize(16)
        elif total < 5: font_size=calc_fontsize(14)
        elif total < 6: font_size=calc_fontsize(13)
        else:           font_size=calc_fontsize(11)

        self.label = pyglet.text.Label(
            text=self.text,
            x=-200, y=from_bottom_edge(30), # we'll fix the x position later, after we see how big the label is
            anchor_x='left', anchor_y='center', batch=batch, font_size=font_size)
        #w = self.label.width  # this doesn't work; how are you supposed to find the width of a label texture?
        w = (len(self.text) * font_size*4)/5
        dis = (window.width-100) / float(total-.99)
        x = 30 + int( pos*dis - w*pos/(total-.5) )

        # draw an icon next to the label for multi-stim mode
        if mode.flags[mode.mode]['multi'] > 1 and self.modality[-1].isdigit():
            self.id = int(modality[-1])
            if cfg.MULTI_MODE == 'color':
                self.icon = pyglet.sprite.Sprite(visuals[self.id-1].spr_square[cfg.VISUAL_COLORS[self.id-1]-1].image)
                self.icon.scale = .125 * visuals[self.id-1].size / visuals[self.id-1].image_set_size
                self.icon.y = from_bottom_edge(22)
                self.icon.x = x - 15
                x += 15

            else: # 'image'
                self.icon = pyglet.sprite.Sprite(visuals[self.id-1].images[self.id-1].image)
                self.icon.color = get_color(1)[:3]
                self.icon.scale = .25 * visuals[self.id-1].size / visuals[self.id-1].image_set_size
                self.icon.y = from_bottom_edge(15)
                self.icon.x = x - 25
                x += 25

            self.icon.opacity = 255
            self.icon.batch = batch

        self.label.x = x

        self.update()

    def draw(self):
        pass # don't draw twice; this was just for debugging
        #self.label.draw()

    def update(self):
        if mode.started and not mode.hide_text and self.modality in mode.modalities[mode.mode]: # still necessary?
            self.label.text = self.text
        else:
            self.label.text = ''
        if cfg.SHOW_FEEDBACK and mode.inputs[self.modality]:
            result = check_match(self.modality)
            #self.label.bold = True
            if result == 'correct':
                self.label.color = cfg.COLOR_LABEL_CORRECT
            elif result == 'unknown':
                self.label.color = cfg.COLOR_LABEL_OOPS
            elif result == 'incorrect':
                self.label.color = cfg.COLOR_LABEL_INCORRECT
        elif cfg.SHOW_FEEDBACK and (not mode.inputs['audiovis']) and mode.show_missed:
            result = check_match(self.modality, check_missed=True)
            if result == 'missed':
                self.label.color = cfg.COLOR_LABEL_OOPS
                #self.label.bold = True
        else:
            self.label.color = cfg.COLOR_TEXT
            self.label.bold = False

    def delete(self):
        self.label.delete()
        if mode.flags[mode.mode]['multi'] > 1 and self.modality[-1].isdigit():
            self.icon.batch = None


def generate_input_labels():
    labels = []
    modalities = mode.modalities[mode.mode]
    pos = 0
    total = len(modalities)
    for m in modalities:
        if m != 'arithmetic':

            labels.append(FeedbackLabel(m, pos, total))
        pos += 1
    return labels

class ArithmeticAnswerLabel:
    def __init__(self):
        self.answer = []
        self.negative = False
        self.decimal = False
        self.label = pyglet.text.Label(
            '',
            x=window.width/2 - 40, y=from_bottom_edge(30),
            anchor_x='left', anchor_y='center', batch=batch)
        self.update()
    def update(self):
        if not 'arithmetic' in mode.modalities[mode.mode] or not mode.started:
            self.label.text = ''
            return
        if mode.started and mode.hide_text:
            self.label.text = ''
            return

        self.label.font_size=calc_fontsize(16)
        str_list = []
        str_list.append(_('Answer: '))
        str_list.append(str(self.parse_answer()))
        self.label.text = ''.join(str_list)

        if cfg.SHOW_FEEDBACK and mode.show_missed:
            result = check_match('arithmetic')
            if result == _('correct'):
                self.label.color = cfg.COLOR_LABEL_CORRECT
                self.label.bold = True
            if result == _('incorrect'):
                self.label.color = cfg.COLOR_LABEL_INCORRECT
                self.label.bold = True
        else:
            self.label.color = cfg.COLOR_TEXT
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
        elif input == '.':
            if not self.decimal:
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


# this is the text that shows the seconds per trial and the number of trials.
class SessionInfoLabel:
    def __init__(self):
        self.label = pyglet.text.Label(
            '',
            multiline = True, width = scale_to_width(128),
            font_size=calc_fontsize(11),
            color=cfg.COLOR_TEXT,
            x=from_left_edge(20), y=from_bottom_edge(145),
            anchor_x='left', anchor_y='top', batch=batch)
        self.update()
    def update(self):
        if mode.started or CLINICAL_MODE:
            self.label.text = ''
        else:
            self.label.text = _('Session:\n%1.2f sec/trial\n%i+%i trials\n%i seconds') % \
                              (mode.ticks_per_trial / 10.0, mode.num_trials, \
                               mode.num_trials_total - mode.num_trials,
                               int((mode.ticks_per_trial / 10.0) * \
                               (mode.num_trials_total)))
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
            multiline = True, width = scale_to_width(128),
            font_size=calc_fontsize(11),
            color=cfg.COLOR_TEXT,
            x=from_right_edge(20), y=from_bottom_edge(145),
            anchor_x='right', anchor_y='top', batch=batch)
        self.update()
    def update(self):
        if mode.started or mode.manual or CLINICAL_MODE:
            self.label.text = ''
        else:
            self.label.text = _(u'Thresholds:\nRaise level: \u2265 %i%%\nLower level: < %i%%') % \
            (get_threshold_advance(), get_threshold_fallback())   # '\u2265' = '>='

# this controls the "press space to begin session #" text.
class SpaceLabel:
    def __init__(self):
        self.label = pyglet.text.Label(
            '',
            font_size=calc_fontsize(16),
            bold=True,
            color=(32, 32, 255, 255),
            x=width_center(), y=from_bottom_edge(62),
            anchor_x='center', anchor_y='center', batch=batch)
        self.update()
    def update(self):
        if mode.started:
            self.label.text = ''
        else:
            str_list = []
            str_list.append(_('Press SPACE to begin session #'))
            str_list.append(str(mode.session_number + 1))
            str_list.append(': ')
            str_list.append(mode.long_mode_names[mode.mode] + ' ')

            if cfg.VARIABLE_NBACK:
                str_list.append(_('V. '))
            str_list.append(str(mode.back))
            str_list.append(_('-Back'))
            self.label.text = ''.join(str_list)

def check_match(input_type, check_missed = False):
    current = 0
    back_data = ''
    operation = 0
    # FIXME:  I'm not going to think about whether crab_back will work with
    # cfg.VARIABLE_NBACK yet, since I don't actually understand how the latter works

    if mode.flags[mode.mode]['crab'] == 1:
        back = 1 + 2*((mode.trial_number-1) % mode.back)
    else:
        back = mode.back

    if cfg.VARIABLE_NBACK:
        nback_trial = mode.trial_number - mode.variable_list[mode.trial_number - back - 1] - 1
    else:
        nback_trial = mode.trial_number - back - 1

    if len(stats.session['position1']) < mode.back:
        return 'unknown'

    if   input_type in ('visvis', 'visaudio', 'image'):
        current = mode.current_stim['vis']
    elif input_type in ('audiovis', ):
        current = mode.current_stim['audio']
    if   input_type in ('visvis', 'audiovis', 'image'):
        back_data = 'vis'
    elif input_type in ('visaudio', ):
        back_data = 'audio'
    elif input_type == 'arithmetic':
        current = mode.current_stim['number']
        back_data = stats.session['numbers'][nback_trial]
        operation = mode.current_operation
    else:
        current = mode.current_stim[input_type]
        back_data = input_type

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
    else:
        # Catch accesses past list end
        try:
            if current == stats.session[back_data][nback_trial]:
                if check_missed:
                    return 'missed'
                else:
                    return 'correct'
        except Exception as e:
            print(e)
            return 'incorrect'
    return 'incorrect'


# this controls the statistics which display upon completion of a session.
class AnalysisLabel:
    def __init__(self):
        self.label = pyglet.text.Label(
            '',
            font_size=calc_fontsize(14),
            color=cfg.COLOR_TEXT,
            x=width_center(), y=from_bottom_edge(92),
            anchor_x='center', anchor_y='center', batch=batch)
        self.update()

    def update(self, skip=False):
        if mode.started or mode.session_number == 0 or skip:
            self.label.text = ''
            return

        poss_mods = ['position1', 'position2', 'position3', 'position4',
                     'vis1', 'vis2', 'vis3', 'vis4',  'color', 'visvis',
                     'visaudio', 'audiovis', 'image', 'audio',
                     'audio2', 'arithmetic'] # arithmetic must be last so it's easy to exclude

        rights = dict([(mod, 0) for mod in poss_mods])
        wrongs = dict([(mod, 0) for mod in poss_mods])
        category_percents = dict([(mod, 0) for mod in poss_mods])

        mods = mode.modalities[mode.mode]
        data = stats.session

        for mod in mods:
            for x in range(mode.back, len(data['position1'])):

                if mode.flags[mode.mode]['crab'] == 1:
                    back = 1 + 2*(x % mode.back)
                else:
                    back = mode.back
                if cfg.VARIABLE_NBACK:
                    back = mode.variable_list[x - back]

                # data is a dictionary of lists.
                if mod in ['position1', 'position2', 'position3', 'position4',
                           'vis1', 'vis2', 'vis3', 'vis4', 'audio', 'audio2', 'color', 'image']:
                    rights[mod] += int((data[mod][x] == data[mod][x-back]) and data[mod+'_input'][x])
                    wrongs[mod] += int((data[mod][x] == data[mod][x-back])  ^  data[mod+'_input'][x]) # ^ is XOR
                    if cfg.JAEGGI_SCORING:
                        rights[mod] += int(data[mod][x] != data[mod][x-back]  and not data[mod+'_input'][x])

                if mod in ['visvis', 'visaudio', 'audiovis']:
                    modnow = mod.startswith('vis') and 'vis' or 'audio' # these are the python<2.5 compatible versions
                    modthn = mod.endswith('vis')   and 'vis' or 'audio' # of 'vis' if mod.startswith('vis') else 'audio'
                    rights[mod] += int((data[modnow][x] == data[modthn][x-back]) and data[mod+'_input'][x])
                    wrongs[mod] += int((data[modnow][x] == data[modthn][x-back])  ^  data[mod+'_input'][x])
                    if cfg.JAEGGI_SCORING:
                        rights[mod] += int(data[modnow][x] != data[modthn][x-back]  and not data[mod+'_input'][x])

                if mod in ['arithmetic']:
                    ops = {'add':'+', 'subtract':'-', 'multiply':'*', 'divide':'/'}
                    answer = eval("Decimal(data['numbers'][x-back]) %s Decimal(data['numbers'][x])" % ops[data['operation'][x]])
                    rights[mod] += int(answer == Decimal(data[mod+'_input'][x])) # data[...][x] is only Decimal if op == /
                    wrongs[mod] += int(answer != Decimal(data[mod+'_input'][x]))

        str_list = []
        if not CLINICAL_MODE:
            str_list += [_('Correct-Errors:   ')]
            sep = '   '
            keys = dict([(mod, cfg['KEY_%s' % mod.upper()]) for mod in poss_mods[:-1]]) # exclude 'arithmetic'

            for mod in poss_mods[:-1]: # exclude 'arithmetic'
                if mod in mods:
                    keytext = key.symbol_string(keys[mod])
                    if keytext == 'SEMICOLON': keytext = ';'
                    str_list += ["%s:%i-%i%s" % (keytext, rights[mod], wrongs[mod], sep)]

            if 'arithmetic' in mods:
                str_list += ["%s:%i-%i%s" % (_("Arithmetic"), rights['arithmetic'], wrongs['arithmetic'], sep)]

        def calc_percent(r, w):
            if r+w: return int(r*100 / float(r+w))
            else:   return 0

        right = sum([rights[mod] for mod in mods])
        wrong = sum([wrongs[mod] for mod in mods])

        for mod in mods:
            category_percents[mod] = calc_percent(rights[mod], wrongs[mod])

        if cfg.JAEGGI_SCORING:
            percent = min([category_percents[m] for m in mode.modalities[mode.mode]])
            #percent = min(category_percents['position1'], category_percents['audio']) # cfg.JAEGGI_MODE forces mode.mode==2
            if not CLINICAL_MODE:
                str_list += [_('Lowest score: %i%%') % percent]
        else:
            percent = calc_percent(right, wrong)
            str_list += [_('Score: %i%%') % percent]

        self.label.text = ''.join(str_list)

        stats.submit_session(percent, category_percents)

# this controls the title of the session history chart.
class ChartTitleLabel:
    def __init__(self):
        self.label = pyglet.text.Label(
            '',
            font_size=calc_fontsize(10),
            bold = True,
            color = cfg.COLOR_TEXT,
            x = from_right_edge(30),
            y = from_top_edge(85),
            anchor_x = 'right',
            anchor_y = 'top',
            batch = batch)
        self.update()
    def update(self):
        if mode.started:
            self.label.text = ''
        else:
            self.label.text = _('Today\'s Last 20:')

# this controls the session history chart.
class ChartLabel:
    def __init__(self):
        self.start_x = from_right_edge(140)
        self.start_y = from_top_edge(105)
        self.line_spacing      = calc_fontsize(15)
        self.column_spacing_12 = calc_fontsize(30)
        self.column_spacing_23 = calc_fontsize(70)
        self.font_size         = calc_fontsize(10)
        self.color_normal   = (128, 128, 128, 255)
        self.color_advance  = (0, 160, 0, 255)
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
        stats.parse_statsfile()
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
            manual = stats.history[x][4]
            color = self.color_normal
            if not manual and stats.history[x][3] >= get_threshold_advance():
                color = self.color_advance
            elif not manual and stats.history[x][3] < get_threshold_fallback():
                color = self.color_fallback
            self.column1[index].color = color
            self.column2[index].color = color
            self.column3[index].color = color
            if manual:
                self.column1[index].text = 'M'
            elif stats.history[x][0] > -1:
                self.column1[index].text = '#%i' % stats.history[x][0]
            self.column2[index].text = mode.short_name(mode=stats.history[x][1], back=stats.history[x][2])
            self.column3[index].text = '%i%%' % stats.history[x][3]
            index += 1

# this controls the title of the session history chart.
class AverageLabel:
    def __init__(self):
        self.label = pyglet.text.Label(
            '',
            font_size=calc_fontsize(10), bold=False,
            color=cfg.COLOR_TEXT,
            x=from_right_edge(30), y=from_top_edge(70),
            anchor_x='right', anchor_y='top', batch=batch)
        self.update()
    def update(self):
        if mode.started or CLINICAL_MODE:
            self.label.text = ''
        else:
            sessions = [sess for sess in stats.history if sess[1] == mode.mode][-20:]
            if sessions:
                average = sum([sess[2] for sess in sessions]) / float(len(sessions))
            else:
                average = 0.
            self.label.text = _("%sNB average: %1.2f") % (mode.short_mode_names[mode.mode], average)


class TodayLabel:
    def __init__(self):
        self.labelTitle = pyglet.text.Label(
            '',
            font_size=calc_fontsize(9),
            color = cfg.COLOR_TEXT,
            x=window.width, y=from_top_edge(5),
            anchor_x='right', anchor_y='top',width=scale_to_width(280), multiline=True, batch=batch)
        self.update()
    def update(self):
        if mode.started:
            self.labelTitle.text = ''
        else:
            total_trials = sum([mode.num_trials + mode.num_trials_factor * \
                his[2] ** mode.num_trials_exponent for his in stats.history])
            total_time = mode.ticks_per_trial * TICK_DURATION * total_trials

            self.labelTitle.text = _(
                ("%i min %i sec done today in %i sessions\n" \
               + "%i min %i sec done in last 24 hours in %i sessions") \
                % (stats.time_today//60, stats.time_today%60, stats.sessions_today, \
                    stats.time_thours//60, stats.time_thours%60, stats.sessions_thours))

class TrialsRemainingLabel:
    def __init__(self):
        self.label = pyglet.text.Label(
            '',
            font_size=calc_fontsize(12), bold = True,
            color=cfg.COLOR_TEXT,
            x=from_right_edge(10), y=from_top_edge(5),
            anchor_x='right', anchor_y='top', batch=batch)
        self.update()
    def update(self):
        if (not mode.started) or mode.hide_text:
            self.label.text = ''
        else:
            self.label.text = _('%i remaining') % (mode.num_trials_total - mode.trial_number)

class Saccadic:
    def __init__(self):
        self.position = 'left'
        self.counter = 0
        self.radius = scale_to_height(10)
        self.color = (0, 0, 255, 255)

    def tick(self, dt):
        self.counter += 1
        if self.counter == cfg.SACCADIC_REPETITIONS:
            self.stop()
        elif self.position == 'left':
            self.position = 'right'
        else: self.position = 'left'

    def start(self):
        self.position = 'left'
        mode.saccadic = True
        self.counter = 0
        pyglet.clock.schedule_interval(saccadic.tick, cfg.SACCADIC_DELAY)

    def stop(self):
        pyglet.clock.unschedule(saccadic.tick)
        mode.saccadic = False

    def draw(self):
        y = height_center()
        if saccadic.position == 'left':
            x = self.radius
        elif saccadic.position == 'right':
            x = window.width - self.radius
        pyglet.graphics.draw(4, pyglet.gl.GL_POLYGON, ('v2i', (
            x - self.radius, y - self.radius,  # lower-left
            x + self.radius, y - self.radius,  # lower-right
            x + self.radius, y + self.radius,  # upper-right
            x - self.radius, y + self.radius,  # upper-left

            )), ('c4B', self.color * 4))

#                    self.square = batch.add(40, pyglet.gl.GL_POLYGON, None,
#                                            ('v2i', xy), ('c4B', self.color * 40))


class Panhandle:
    def __init__(self, n=-1):
        paragraphs = [
_("""
You have completed %i sessions with Brain Workshop.  Your perseverance suggests \
that you are finding some benefit from using the program.  If you have been \
benefiting from Brain Workshop, don't you think Brain Workshop should \
benefit from you?
""") % n,
_("""
Brain Workshop is and always will be 100% free.  Up until now, Brain Workshop \
as a project has succeeded because a very small number of people have each \
donated a huge amount of time to it.  It would be much better if the project \
were supported by small donations from a large number of people.  Do your \
part.  Donate.
"""),
_("""
As of March 2010, Brain Workshop has been downloaded over 75,000 times in 20 \
months.  If each downloader donated an average of $1, we could afford to pay \
decent full- or part-time salaries (as appropriate) to all of our developers, \
and we would be able to buy advertising to help people learn about Brain \
Workshop.  With $2 per downloader, or with more downloaders, we could afford \
to fund controlled experiments and clinical trials on Brain Workshop and \
cognitive training.  Help us make that vision a reality.  Donate.
"""),
_("""
The authors think it important that access to cognitive training \
technologies be available to everyone as freely as possible.  Like other \
forms of education, cognitive training should not be a luxury of the rich, \
since that would tend to exacerbate class disparity and conflict.  Charging \
money for cognitive training does exactly that.  The commercial competitors \
of Brain Workshop have two orders of magnitude more users than does Brain \
Workshop because they have far more resources for research, development, and \
marketing.  Help us bridge that gap and improve social equality of \
opportunity.  Donate.
"""),
_("""
Brain Workshop has many known bugs and missing features.  The developers \
would like to fix these issues, but they also have to work in order to be \
able to pay for rent and food.  If you think the developers' time is better \
spent programming than serving coffee, then do something about it.  Donate.
"""),
_("""
Press SPACE to continue, or press D to donate now.
""")]    # feel free to add more paragraphs or to change the chances for the
        # paragraphs you like and dislike, etc.
        chances = [-1, 10, 10, 10, 10, 0] # if < 0, 100% chance of being included.  Otherwise, relative weight.
                                         # if == 0, appended to end and not counted
                                         # for target_len.
        assert len(chances) == len(paragraphs)
        target_len = 3
        text = []
        options = []
        for i in range(len(chances)):
            if chances[i] < 0:
                text.append(i)
            else:
                options.extend([i]*chances[i])
        while len(text) < target_len and len(options) > 0:
            choice = random.choice(options)
            while choice in options:
                options.remove(choice)
            text.append(choice)
        for i in range(len(chances)):
            if chances[i] == 0:
                text.append(i)
        self.text = ''.join([paragraphs[i] for i in text])

        self.batch = pyglet.graphics.Batch()
        self.label = pyglet.text.Label(self.text,
                            color=cfg.COLOR_TEXT,
                            batch=self.batch,
                            multiline=True,
                            width=(4*window.width)/5,
                            font_size=calc_fontsize(14),
                            x=width_center(), y=height_center(),
                            anchor_x='center', anchor_y='center')
        window.push_handlers(self.on_key_press, self.on_draw)
        self.on_draw()

    def on_key_press(self, sym, mod):
        if sym in (key.ESCAPE, key.SPACE):
            self.close()
        elif sym in (key.RETURN, key.ENTER, key.D):
            self.select()
        return pyglet.event.EVENT_HANDLED

    def select(self):
        webbrowser.open_new_tab(WEB_DONATE)
        self.close()

    def close(self):
        return window.remove_handlers(self.on_key_press, self.on_draw)

    def on_draw(self):
        window.clear()
        self.batch.draw()
        return pyglet.event.EVENT_HANDLED

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
        self.full_history = [] # not just today
        self.sessions_today = 0
        self.time_today = 0
        self.time_thours = 0
        self.sessions_thours = 0

    def parse_statsfile(self):
        self.clear()
        if os.path.isfile(os.path.join(get_data_dir(), cfg.STATSFILE)):
            try:
                #last_session = []
                #last_session_number = 0
                last_mode = 0
                last_back = 0
                statsfile_path = os.path.join(get_data_dir(), cfg.STATSFILE)
                statsfile = open(statsfile_path, 'r')
                is_today = False
                is_thours = False
                today = date.today()
                yesterday = date.fromordinal(today.toordinal() - 1)
                tomorrow = date.fromordinal(today.toordinal() + 1)
                for line in statsfile:
                    if line == '': continue
                    if line == '\n': continue
                    if line[0] not in '0123456789': continue
                    datestamp = date(int(line[:4]), int(line[5:7]), int(line[8:10]))
                    hour = int(line[11:13])
                    mins = int(line[14:16])
                    sec = int(line[17:19])
                    thour = datetime.datetime.today().hour
                    tmin = datetime.datetime.today().minute
                    tsec = datetime.datetime.today().second
                    if int(strftime('%H')) < cfg.ROLLOVER_HOUR:
                        if datestamp == today or (datestamp == yesterday and hour >= cfg.ROLLOVER_HOUR):
                            is_today = True
                    elif datestamp == today and hour >= cfg.ROLLOVER_HOUR:
                        is_today = True
                    if datestamp == today or (datestamp == yesterday and (hour > thour or (hour == thour and (mins > tmin or (mins == tmin and sec > tsec))))):
                        is_thours = True
                    if '\t' in line:
                        separator = '\t'
                    else: separator = ','
                    newline = line.split(separator)
                    newmode = int(newline[3])
                    newback = int(newline[4])
                    newpercent = int(newline[2])
                    newmanual = bool(int(newline[7]))
                    newsession_number = int(newline[8])
                    try:
                        sesstime = int(round(float(newline[25])))
                    except Exception as e:
                        debug_msg(e)
                        # this session wasn't performed with this version of BW, and is therefore
                        # old, and therefore the session time doesn't matter
                        sesstime = 0
                    if newmanual:
                        newsession_number = 0
                    self.full_history.append([newsession_number, newmode, newback, newpercent, newmanual])
                    if is_thours:
                        stats.sessions_thours += 1
                        stats.time_thours += sesstime
                    if is_today:
                        stats.sessions_today += 1
                        self.time_today += sesstime
                        self.history.append([newsession_number, newmode, newback, newpercent, newmanual])
                    #if not newmanual and (is_today or cfg.RESET_LEVEL):
                    #    last_session = self.full_history[-1]
                statsfile.close()
                self.retrieve_progress()

            except Exception as e:
                debug_msg(e)
                quit_with_error(_('Error parsing stats file\n%s') %
                                os.path.join(get_data_dir(), cfg.STATSFILE),
                                _('\nPlease fix, delete or rename the stats file.'),
                                quit=False)

    def retrieve_progress(self):
        if cfg.RESET_LEVEL:
            sessions = [s for s in self.history if s[1] == mode.mode]
        else:
            sessions = [s for s in self.full_history if s[1] == mode.mode]
        mode.enforce_standard_mode()
        if sessions:
            ls = sessions[-1]
            mode.back = ls[2]
            if ls[3] >= get_threshold_advance():
                mode.back += 1
            mode.session_number = ls[0]
            mode.progress = 0
            for s in sessions:
                if s[2] == mode.back and s[3] < get_threshold_fallback():
                    mode.progress += 1
                elif s[2] != mode.back:
                    mode.progress = 0
            if mode.progress >= cfg.THRESHOLD_FALLBACK_SESSIONS:
                mode.progress = 0
                mode.back -= 1
                if mode.back < 1:
                    mode.back = 1
        else: # no sessions today for this user and this mode
            mode.back = default_nback_mode(mode.mode)
        mode.num_trials_total = mode.num_trials + mode.num_trials_factor * mode.back ** mode.num_trials_exponent

    def initialize_session(self):
        self.session = {}
        for name in ('position1', 'position2', 'position3', 'position4',
             'vis1', 'vis2', 'vis3', 'vis4',
            'color', 'image', 'audio', 'audio2'
            ):
            self.session[name] = []
            self.session["%s_input" % name] = []
            self.session["%s_rt"    % name] = [] # reaction times
        for name in ('vis', 'numbers', 'operation', 'visvis_input',
            'visaudio_input', 'audiovis_input', 'arithmetic_input', 'visvis_rt',
            'visaudio_rt', 'audiovis_rt' # , 'arithmetic_rt'
            ):
            self.session[name] = []

    def save_input(self):
        for k, v in mode.current_stim.items():
            if k == 'number':
                self.session['numbers'].append(v)
            else:
                self.session[k].append(v)
            if k == 'vis': # goes to both self.session['vis'] and ['image']
                self.session['image'].append(v)
        for k, v in mode.inputs.items():
            self.session[k + '_input'].append(v)
        for k, v in mode.input_rts.items():
            self.session[k + '_rt'].append(v)

        self.session['operation'].append(mode.current_operation)
        self.session['arithmetic_input'].append(arithmeticAnswerLabel.parse_answer())


    def submit_session(self, percent, category_percents):
        global musicplayer
        global applauseplayer
        self.history.append([mode.session_number, mode.mode, mode.back, percent, mode.manual])

        if ATTEMPT_TO_SAVE_STATS:
            try:
                sep = STATS_SEPARATOR
                statsfile_path = os.path.join(get_data_dir(), cfg.STATSFILE)
                statsfile = open(statsfile_path, 'a')
                outlist = [strftime("%Y-%m-%d %H:%M:%S"),
                           mode.short_name(),
                           str(percent),
                           str(mode.mode),
                           str(mode.back),
                           str(mode.ticks_per_trial),
                           str(mode.num_trials_total),
                           str(int(mode.manual)),
                           str(mode.session_number),
                           str(category_percents['position1']),
                           str(category_percents['audio']),
                           str(category_percents['color']),
                           str(category_percents['visvis']),
                           str(category_percents['audiovis']),
                           str(category_percents['arithmetic']),
                           str(category_percents['image']),
                           str(category_percents['visaudio']),
                           str(category_percents['audio2']),
                           str(category_percents['position2']),
                           str(category_percents['position3']),
                           str(category_percents['position4']),
                           str(category_percents['vis1']),
                           str(category_percents['vis2']),
                           str(category_percents['vis3']),
                           str(category_percents['vis4']),
                           str(mode.ticks_per_trial * TICK_DURATION * mode.num_trials_total),
                           str(0),
                           ]
                statsfile.write(sep.join(outlist)) # adds sep between each element
                statsfile.write('\n')  # but we don't want a sep before '\n'
                statsfile.close()
                if CLINICAL_MODE:
                    picklefile = open(os.path.join(get_data_dir(), STATS_BINARY), 'ab')
                    pickle.dump([strftime("%Y-%m-%d %H:%M:%S"), mode.short_name(),
                                 percent, mode.mode, mode.back, mode.ticks_per_trial,
                                 mode.num_trials_total, int(mode.manual),
                                 mode.session_number, category_percents['position1'],
                                 category_percents['audio'], category_percents['color'],
                                 category_percents['visvis'], category_percents['audiovis'],
                                 category_percents['arithmetic'], category_percents['image'],
                                 category_percents['visaudio'], category_percents['audio2'],
                                 category_percents['position2'], category_percents['position3'],
                                 category_percents['position4'],
                                 category_percents['vis1'], category_percents['vis2'],
                                 category_percents['vis3'], category_percents['vis4']],
                                picklefile, protocol=2)
                    picklefile.close()
                cfg.SAVE_SESSIONS = True # FIXME: put this where it belongs
                cfg.SESSION_STATS = USER + '-sessions.dat' # FIXME: default user; configurability
                if cfg.SAVE_SESSIONS:
                    picklefile = open(os.path.join(get_data_dir(), cfg.SESSION_STATS), 'ab')
                    session = {} # it's not a dotdict because we want to pickle it
                    session['summary'] = outlist # that's what goes into stats.txt
                    session['cfg'] = cfg.__dict__
                    session['timestamp'] = strftime("%Y-%m-%d %H:%M:%S")
                    session['mode']   = mode.mode
                    session['n']      = mode.back
                    session['manual'] = mode.manual
                    session['trial_duration'] = mode.ticks_per_trial * TICK_DURATION
                    session['trials']  = mode.num_trials_total
                    session['session'] = self.session
                    pickle.dump(session, picklefile)
                    picklefile.close()
            except Exception as e:
                debug_msg(e)
                quit_with_error(_('Error writing to stats file\n%s') %
                                os.path.join(get_data_dir(), cfg.STATSFILE),
                                _('\nPlease check file and directory permissions.'))

        perfect = awesome = great = good = advance = fallback = False

        if not mode.manual:
            if percent >= get_threshold_advance():
                mode.back += 1
                mode.num_trials_total = (mode.num_trials +
                    mode.num_trials_factor * mode.back ** mode.num_trials_exponent)
                mode.progress = 0
                circles.update()
                if cfg.USE_APPLAUSE:
                    play_applause()
                advance = True
            elif mode.back > 1 and percent < get_threshold_fallback():
                if cfg.JAEGGI_MODE:
                    mode.back -= 1
                    fallback = True
                else:
                    if mode.progress == cfg.THRESHOLD_FALLBACK_SESSIONS - 1:
                        mode.back -= 1
                        mode.num_trials_total = mode.num_trials + mode.num_trials_factor * mode.back ** mode.num_trials_exponent
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

        if mode.manual and not cfg.USE_MUSIC_MANUAL:
            return

        if cfg.USE_MUSIC:
            play_music(percent)

    def clear(self):
        self.history = []
        self.sessions_today = 0
        self.time_today = 0
        self.sessions_thours = 0
        self.time_thours = 0

def update_all_labels(do_analysis=False):
    updateLabel.update()
    congratsLabel.update()
    if do_analysis:
        analysisLabel.update()
    else:
        analysisLabel.update(skip=True)

    if preventMusicSkipping: pyglet.clock.tick(poll=True) # Prevent music/applause skipping 1

    gameModeLabel.update()
    keysListLabel.update()
    pausedLabel.update()
    sessionInfoLabel.update()
    thresholdLabel.update()
    spaceLabel.update()
    chartTitleLabel.update()
    chartLabel.update()

    if preventMusicSkipping: pyglet.clock.tick(poll=True) # Prevent music/applause skipping 2

    averageLabel.update()
    todayLabel.update()
    trialsRemainingLabel.update()

    update_input_labels()

def update_input_labels():
    arithmeticAnswerLabel.update()
    for label in input_labels:
        label.update()

# this function handles initiation of a new session.
def new_session():
    mode.tick = -9  # give a 1-second delay before displaying first trial
    mode.tick -= 5 * (mode.flags[mode.mode]['multi'] - 1 )
    if cfg.MULTI_MODE == 'image':
        mode.tick -= 5 * (mode.flags[mode.mode]['multi'] - 1 )

    mode.session_number += 1
    mode.trial_number = 0
    mode.started = True
    mode.paused = False
    circles.update()

    mode.sound_mode  = random.choice(cfg.AUDIO1_SETS)
    mode.sound2_mode = random.choice(cfg.AUDIO2_SETS)

    visuals[0].load_set()
    visuals[0].choose_random_images(8)
    visuals[0].letters  = random.sample(list(sounds[mode.sound_mode ].keys()), 8)
    visuals[0].letters2 = random.sample(list(sounds[mode.sound2_mode].keys()), 8)


    for i in range(1, mode.flags[mode.mode]['multi']):
        visuals[i].load_set(visuals[0].image_set_index)
        visuals[i].choose_indicated_images(visuals[0].image_indices)
        visuals[i].letters  = visuals[0].letters  # I don't think these are used for anything, but I'm not sure
        visuals[i].letters2 = visuals[0].letters2

    global input_labels
    input_labels.extend(generate_input_labels()) # have to do this after images are loaded


    mode.soundlist  = [sounds[mode.sound_mode][l]  for l in visuals[0].letters]
    mode.soundlist2 = [sounds[mode.sound2_mode][l] for l in visuals[0].letters2]

    if cfg.JAEGGI_MODE:
        compute_bt_sequence()

    if preventMusicSkipping: pyglet.clock.tick(poll=True) # Prevent music/applause skipping

    if cfg.VARIABLE_NBACK:
        # compute variable n-back sequence using beta distribution
        mode.variable_list = []
        for index in range(0, mode.num_trials_total - mode.back):
            mode.variable_list.append(int(random.betavariate(mode.back / 2.0, 1) * mode.back + 1))
    field.crosshair_update()
    reset_input()
    stats.initialize_session()
    update_all_labels()
    pyglet.clock.schedule_interval(fade_out, 0.05)

# this function handles the finish or cancellation of a session.
def end_session(cancelled=False):
    for label in input_labels:
        label.delete()
    while input_labels:
        input_labels.remove(input_labels[0])
    if cancelled:
        mode.session_number -= 1
    if not cancelled:
        stats.sessions_today += 1
    for visual in visuals: visual.hide()
    mode.started = False
    mode.paused = False
    circles.update()
    field.crosshair_update()
    reset_input()
    if cancelled:
        update_all_labels()
    else:
        update_all_labels(do_analysis = True)
        if cfg.PANHANDLE_FREQUENCY:
            statsfile_path = os.path.join(get_data_dir(), cfg.STATSFILE)
            statsfile = open(statsfile_path, 'r')
            sessions = len(statsfile.readlines()) # let's just hope people
            statsfile.close()       # don't manually edit their statsfiles
            if (sessions % cfg.PANHANDLE_FREQUENCY) == 0 and not CLINICAL_MODE:
                Panhandle(n=sessions)



# this function causes the key labels along the bottom to revert to their
# "non-pressed" state for a new trial or when returning to the main screen.
def reset_input():
    for k in list(mode.inputs):
        mode.inputs[k] = False
        mode.input_rts[k] = 0.
    arithmeticAnswerLabel.reset_input()
    update_input_labels()

# this handles the computation of a round with exactly 6 position and 6 audio matches
# this function is not currently used -- compute_bt_sequence() is used instead
##def new_compute_bt_sequence(matches=6, modalities=['audio', 'vis']):
##    # not ready for visaudio or audiovis, doesn't get
##    seq = {}
##    for m in modalities:
##        seq[m] = [False]*mode.back + \
##                 random.shuffle([True]*matches +
##                                [False]*(mode.num_trials_total - mode.back - matches))
##        for i in range(mode.back):
##            seq[m][i] = random.randint(1,8)
##
##        for i in range(mode.back, len(seq[m])):
##            if seq[m][i] == True:
##                seq[m][i] = seq[m][i-mode.back]
##            elif seq[m][i] == False:  # should be all other cases
##                seq[m][i] = random.randint(1,7)
##                if seq[m][i] >= seq[m][i-mode.back]:
##                    seq[m][i] += 1
##    mode.bt_sequence = seq.values()

def compute_bt_sequence():
    bt_sequence = [[], []]
    for x in range(0, mode.num_trials_total):
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
        for x in range(mode.back, mode.num_trials_total):
            bt_sequence[0][x] = random.randint(1, 8)
            if bt_sequence[0][x] == bt_sequence[0][x - mode.back]:
                position += 1
        if position != 6:
            continue
        while True:
            audio = 0
            for x in range(mode.back, mode.num_trials_total):
                bt_sequence[1][x] = random.randint(1, 8)
                if bt_sequence[1][x] == bt_sequence[1][x - mode.back]:
                    audio += 1
            if audio == 6:
                break
        both = 0
        for x in range(mode.back, mode.num_trials_total):
            if bt_sequence[0][x] == bt_sequence[0][x - mode.back] and bt_sequence[1][x] == bt_sequence[1][x - mode.back]:
                both += 1
        if both == 2:
            break

    mode.bt_sequence = bt_sequence

player = get_pyglet_media_Player()
player2 = get_pyglet_media_Player()
# responsible for the random generation of each new stimulus (audio, color, position)
def generate_stimulus():
    # first, randomly generate all stimuli
    positions = random.sample(range(1,9), 4)   # sample without replacement
    for s, p in zip(range(1, 5), positions):
        mode.current_stim['position' + repr(s)] = p
        mode.current_stim['vis' + repr(s)] = random.randint(1, 8)

    #mode.current_stim['position1'] = random.randint(1, 8)
    mode.current_stim['color']  = random.randint(1, 8)
    mode.current_stim['vis']    = random.randint(1, 8)
    mode.current_stim['audio']  = random.randint(1, 8)
    mode.current_stim['audio2'] = random.randint(1, 8)


    # treat arithmetic specially
    operations = []
    if cfg.ARITHMETIC_USE_ADDITION: operations.append('add')
    if cfg.ARITHMETIC_USE_SUBTRACTION: operations.append('subtract')
    if cfg.ARITHMETIC_USE_MULTIPLICATION: operations.append('multiply')
    if cfg.ARITHMETIC_USE_DIVISION: operations.append('divide')
    mode.current_operation = random.choice(operations)

    if cfg.ARITHMETIC_USE_NEGATIVES:
        min_number = 0 - cfg.ARITHMETIC_MAX_NUMBER
    else:
        min_number = 0
    max_number = cfg.ARITHMETIC_MAX_NUMBER

    if mode.current_operation == 'divide' and 'arithmetic' in mode.modalities[mode.mode]:
        if len(stats.session['position1']) >= mode.back:
            number_nback = stats.session['numbers'][mode.trial_number - mode.back - 1]
            possibilities = []
            for x in range(min_number, max_number + 1):
                if x == 0:
                    continue
                if number_nback % x == 0:
                    possibilities.append(x)
                    continue
                frac = Decimal(abs(number_nback)) / Decimal(abs(x))
                if (frac % 1) in map(Decimal, cfg.ARITHMETIC_ACCEPTABLE_DECIMALS):
                    possibilities.append(x)
            mode.current_stim['number'] = random.choice(possibilities)
        else:
            mode.current_stim['number'] = random.randint(min_number, max_number)
            while mode.current_stim['number'] == 0:
                mode.current_stim['number'] = random.randint(min_number, max_number)
    else:
        mode.current_stim['number'] = random.randint(min_number, max_number)

    multi = mode.flags[mode.mode]['multi']

    real_back = mode.back
    if mode.flags[mode.mode]['crab'] == 1:
        real_back = 1 + 2*((mode.trial_number-1) % mode.back)
    else:
        real_back = mode.back
    if cfg.VARIABLE_NBACK:
        real_back = mode.variable_list[mode.trial_number - real_back - 1]

    if mode.modalities[mode.mode] != ['arithmetic'] and mode.trial_number > mode.back:
        for mod in mode.modalities[mode.mode]:
            if   mod in ('visvis', 'visaudio', 'image'):
                current = 'vis'
            elif mod in ('audiovis', ):
                current = 'audio'
            elif mod == 'arithmetic':
                continue
            else:
                current = mod
            if   mod in ('visvis', 'audiovis', 'image'):
                back_data = 'vis'
            elif mod in ('visaudio', ):
                back_data = 'audio'
            else:
                back_data = mod

            back = None
            r1, r2 = random.random(), random.random()
            if multi > 1:
                r2 = 3./2. * r2 # 33% chance of multi-stim reversal

            if  (r1 < cfg.CHANCE_OF_GUARANTEED_MATCH):
                back = real_back

            elif r2 < cfg.CHANCE_OF_INTERFERENCE and mode.back > 1:
                back = real_back
                interference = [-1, 1, mode.back]
                if back < 3: interference = interference[1:] # for crab mode and 2-back
                random.shuffle(interference)
                for i in interference: # we'll just take the last one that works.
                    if mode.trial_number - (real_back+i) - 1 >= 0 and \
                         stats.session[back_data][mode.trial_number - (real_back+i) - 1] != \
                         stats.session[back_data][mode.trial_number -  real_back    - 1]:
                        back = real_back + i
                if back == real_back: back = None # if none of the above worked
                elif DEBUG:
                    print('Forcing interference for %s' % current)

            if back:
                nback_trial = mode.trial_number - back - 1
                matching_stim = stats.session[back_data][nback_trial]
                # check for collisions in multi-stim mode
                if multi > 1 and mod.startswith('position'):
                    potential_conflicts = set(range(1, multi+1)) - set([int(mod[-1])])
                    conflict_positions = [positions[i-1] for i in potential_conflicts]
                    if matching_stim in conflict_positions: # swap 'em
                        i = positions.index(matching_stim)
                        if DEBUG:
                            print("moving position%i from %i to %i for %s" % (i+1, positions[i], mode.current_stim[current], current))
                        mode.current_stim['position' + repr(i+1)] = mode.current_stim[current]
                        positions[i] = mode.current_stim[current]
                    positions[int(current[-1])-1] = matching_stim
                if DEBUG:
                    print("setting %s to %i" % (current, matching_stim))
                mode.current_stim[current] = matching_stim

        if multi > 1:
            if random.random() < cfg.CHANCE_OF_INTERFERENCE / 3.:
                mod = 'position'
                if 'vis1' in mode.modalities[mode.mode] and random.random() < .5:
                    mod = 'vis'
                offset = random.choice(range(1, multi))
                for i in range(multi):
                    mode.current_stim[mod + repr(i+1)] = stats.session[mod + repr(((i+offset)%multi) + 1)][mode.trial_number - real_back - 1]
                    if mod == 'position':
                        positions[i] = mode.current_stim[mod + repr(i+1)]


    # set static stimuli according to mode.
    # default position is 0 (center)
    # default color is 1 (red) or 2 (black)
    # default vis is 0 (square)
    # audio is never static so it doesn't have a default.
    if not 'color'     in mode.modalities[mode.mode]: mode.current_stim['color'] = cfg.VISUAL_COLORS[0]
    if not 'position1' in mode.modalities[mode.mode]: mode.current_stim['position1'] = 0
    if not set(['visvis', 'arithmetic', 'image']).intersection( mode.modalities[mode.mode] ):
        mode.current_stim['vis'] = 0
    if multi > 1 and not 'vis1' in mode.modalities[mode.mode]:
        for i in range(1, 5):
            if cfg.MULTI_MODE == 'color':
                mode.current_stim['vis'+repr(i)] = 0 # use squares
            elif cfg.MULTI_MODE == 'image':
                mode.current_stim['vis'+repr(i)] = cfg.VISUAL_COLORS[0]

    # in jaeggi mode, set using the predetermined sequence.
    if cfg.JAEGGI_MODE:
        mode.current_stim['position1'] = mode.bt_sequence[0][mode.trial_number - 1]
        mode.current_stim['audio'] = mode.bt_sequence[1][mode.trial_number - 1]

    # initiate the chosen stimuli.
    # mode.current_stim['audio'] is a number from 1 to 8.
    if 'arithmetic' in mode.modalities[mode.mode] and mode.trial_number > mode.back:
        player.queue(sounds['operations'][mode.current_operation])  # maybe we should try... catch... here
        player.play()                                               # and maybe we should recycle sound players...
    elif 'audio' in mode.modalities[mode.mode] and not 'audio2' in mode.modalities[mode.mode]:
        player.queue(mode.soundlist[mode.current_stim['audio']-1])
        player.play()
    elif 'audio2' in mode.modalities[mode.mode]:
        # dual audio modes - two sound players
        player.queue(mode.soundlist[mode.current_stim['audio']-1])
        player.min_distance = 100.0
        if cfg.CHANNEL_AUDIO1 == 'left':
            player.position = (-99.0, 0.0, 0.0)
        elif cfg.CHANNEL_AUDIO1 == 'right':
            player.position = (99.0, 0.0, 0.0)
        elif cfg.CHANNEL_AUDIO1 == 'center':
            #player.position = (0.0, 0.0, 0.0)
            pass
        player.play()
        player2.queue(mode.soundlist2[mode.current_stim['audio2']-1])
        player2.min_distance = 100.0
        if cfg.CHANNEL_AUDIO2 == 'left':
            player2.position = (-99.0, 0.0, 0.0)
        elif cfg.CHANNEL_AUDIO2 == 'right':
            player2.position = (99.0, 0.0, 0.0)
        elif cfg.CHANNEL_AUDIO2 == 'center':
            #player2.position = (0.0, 0.0, 0.0)
            pass
        player2.play()


    if cfg.VARIABLE_NBACK and mode.trial_number > mode.back:
        variable = mode.variable_list[mode.trial_number - 1 - mode.back]
    else:
        variable = 0
    if DEBUG and multi < 2:
        print("trial=%i, \tpos=%i, \taud=%i, \tcol=%i, \tvis=%i, \tnum=%i,\top=%s, \tvar=%i" % \
                (mode.trial_number, mode.current_stim['position1'], mode.current_stim['audio'],
                 mode.current_stim['color'], mode.current_stim['vis'], \
                 mode.current_stim['number'], mode.current_operation, variable))
    if multi == 1:
        visuals[0].spawn(mode.current_stim['position1'], mode.current_stim['color'],
                         mode.current_stim['vis'], mode.current_stim['number'],
                         mode.current_operation, variable)
    else: # multi > 1
        for i in range(1, multi+1):
            if cfg.MULTI_MODE == 'color':
                if DEBUG:
                    print("trial=%i, \tpos=%i, \taud=%i, \tcol=%i, \tvis=%i, \tnum=%i,\top=%s, \tvar=%i" % \
                        (mode.trial_number, mode.current_stim['position' + repr(i)], mode.current_stim['audio'],
                        cfg.VISUAL_COLORS[i-1], mode.current_stim['vis'+repr(i)], \
                        mode.current_stim['number'], mode.current_operation, variable))
                visuals[i-1].spawn(mode.current_stim['position'+repr(i)], cfg.VISUAL_COLORS[i-1],
                                   mode.current_stim['vis'+repr(i)], mode.current_stim['number'],
                                   mode.current_operation, variable)
            else:
                if DEBUG:
                    print("trial=%i, \tpos=%i, \taud=%i, \tcol=%i, \tvis=%i, \tnum=%i,\top=%s, \tvar=%i" % \
                        (mode.trial_number, mode.current_stim['position' + repr(i)], mode.current_stim['audio'],
                        mode.current_stim['vis'+repr(i)], i, \
                        mode.current_stim['number'], mode.current_operation, variable))
                visuals[i-1].spawn(mode.current_stim['position'+repr(i)], mode.current_stim['vis'+repr(i)],
                                   i,                            mode.current_stim['number'],
                                   mode.current_operation, variable)

def toggle_manual_mode():
    if mode.manual:
        mode.manual = False
    else:
        mode.manual = True

    #if not mode.manual:
        #mode.enforce_standard_mode()

    update_all_labels()

def set_user(newuser):
    global cfg
    global USER
    global CONFIGFILE
    USER = newuser
    if USER.lower() == 'default':
        CONFIGFILE = 'config.ini'
    else:
        CONFIGFILE = USER + '-config.ini'
    rewrite_configfile(CONFIGFILE, overwrite=False)
    cfg = parse_config(CONFIGFILE)
    stats.initialize_session()
    stats.parse_statsfile()
    if len(stats.full_history) > 0 and not cfg.JAEGGI_MODE:
        mode.mode = stats.full_history[-1][1]
    stats.retrieve_progress()
    # text labels also need to be remade; until that's done, this remains commented out
    #if cfg.BLACK_BACKGROUND:
    #    glClearColor(0, 0, 0, 1)
    #else:
    #    glClearColor(1, 1, 1, 1)
    window.set_fullscreen(cfg.WINDOW_FULLSCREEN) # window size needs to be changed
    update_all_labels()
    save_last_user('defaults.ini')


def get_users():
    users = ['default'] + [fn.split('-')[0] for fn in os.listdir(get_data_dir()) if '-stats.txt' in fn]
    if 'Readme' in users: users.remove('Readme')
    return users

# there are 4 event loops:
#   on_mouse_press: allows the user to use the mouse (LMB and RMB) instead of keys
#   on_key_press:   listens to the keyboard and acts when certain keys are pressed
#   on_draw:        draws everything to the screen something like 60 times per second
#   update(dt):     the session timer loop which controls the game during the sessions.
#                   Runs once every quarter-second.
#
# --- BEGIN EVENT LOOP SECTION ----------------------------------------------
#

# this is where the keyboard keys are defined.
@window.event
def on_mouse_press(x, y, button, modifiers):
    Flag = True
    if mode.started:
        if len(mode.modalities[mode.mode])==2:
            for k in mode.modalities[mode.mode]:
                if k == 'arithmetic':
                    Flag = False
            if Flag:
                if (button == pyglet.window.mouse.LEFT):
                    mode.inputs[mode.modalities[mode.mode][0]] = True
                elif (button == pyglet.window.mouse.RIGHT):
                    mode.inputs[mode.modalities[mode.mode][1]] = True
                update_input_labels()

@window.event
def on_key_press(symbol, modifiers):
    if symbol == key.D and (modifiers & key.MOD_CTRL):
        dump_pyglet_info()

    elif mode.title_screen and not mode.draw_graph:
        if symbol == key.ESCAPE or symbol == key.X:
            window.on_close()

        elif symbol == key.SPACE:
            mode.title_screen = False
            #mode.shrink_brain = True
            #pyglet.clock.schedule_interval(shrink_brain, 1/60.)

        elif symbol == key.C and not cfg.JAEGGI_MODE:
            GameSelect()

        elif symbol == key.I and not cfg.JAEGGI_MODE:
            ImageSelect()

        elif symbol == key.H:
            webbrowser.open_new_tab(WEB_TUTORIAL)

        elif symbol == key.D and not CLINICAL_MODE:
            webbrowser.open_new_tab(WEB_DONATE)

        elif symbol == key.V and DEBUG:
            OptionsScreen()

        elif symbol == key.G:
#            sound_stop()
            graph.parse_stats()
            graph.graph = mode.mode
            mode.draw_graph = True

        elif symbol == key.U:
            UserScreen()

        elif symbol == key.L:
            LanguageScreen()

        elif symbol == key.S and not cfg.JAEGGI_MODE:
            SoundSelect()

        elif symbol == key.F:
            webbrowser.open_new_tab(WEB_FORUM)

        elif symbol == key.O:
            edit_config_ini()

    elif mode.draw_graph:
        if symbol == key.ESCAPE or symbol == key.G or symbol == key.X:
            mode.draw_graph = False

        #elif symbol == key.E and (modifiers & key.MOD_CTRL):
            #graph.export_data()

        elif symbol == key.N:
            graph.next_nonempty_mode()

        elif symbol == key.M:
            graph.next_style()

    elif mode.saccadic:
        if symbol in (key.ESCAPE, key.E, key.X, key.SPACE):
            saccadic.stop()

    elif not mode.started:

        if symbol == key.ESCAPE or symbol == key.X:
            if cfg.SKIP_TITLE_SCREEN:
                window.on_close()
            else:
                mode.title_screen = True

        elif symbol == key.SPACE:
            new_session()

        elif CLINICAL_MODE:
            pass
            #if symbol == key.H:
                #webbrowser.open_new_tab(CLINICAL_TUTORIAL)
        # No elifs below this line at this indentation will be
        # executed in CLINICAL_MODE

        elif symbol == key.E and cfg.WINDOW_FULLSCREEN:
            saccadic.start()

        elif symbol == key.G:
#            sound_stop()
            graph.parse_stats()
            graph.graph = mode.mode
            mode.draw_graph = True

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
            mode.num_trials_total = mode.num_trials + mode.num_trials_factor * \
                mode.back ** mode.num_trials_exponent
            sessionInfoLabel.flash()

        elif symbol == key.F4 and mode.manual:
            mode.num_trials += 5
            mode.num_trials_total = mode.num_trials + mode.num_trials_factor * \
                mode.back ** mode.num_trials_exponent
            sessionInfoLabel.flash()

        elif symbol == key.F5 and mode.manual:
            if mode.ticks_per_trial < TICKS_MAX:
                mode.ticks_per_trial += 1
                sessionInfoLabel.flash()

        elif symbol == key.F6 and mode.manual:
            if mode.ticks_per_trial > TICKS_MIN:
                mode.ticks_per_trial -= 1
                sessionInfoLabel.flash()

        elif symbol == key.C and (modifiers & key.MOD_CTRL):
            stats.clear()
            chartLabel.update()
            averageLabel.update()
            todayLabel.update()
            mode.progress = 0
            circles.update()

        elif symbol == key.C:
            if cfg.JAEGGI_MODE:
                jaeggiWarningLabel.show()
                return
            GameSelect()

        elif symbol == key.U:
            UserScreen()

        elif symbol == key.I:
            if cfg.JAEGGI_MODE:
                jaeggiWarningLabel.show()
                return
            ImageSelect()

        elif symbol == key.S:
            if cfg.JAEGGI_MODE:
                jaeggiWarningLabel.show()
                return
            SoundSelect()

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

        elif symbol == key.D and not CLINICAL_MODE:
            webbrowser.open_new_tab(WEB_DONATE)

        elif symbol == key.J and 'morse' in cfg.AUDIO1_SETS or 'morse' in cfg.AUDIO2_SETS:
            webbrowser.open_new_tab(WEB_MORSE)


    # these are the keys during a running session.
    elif mode.started:
        if (symbol == key.ESCAPE or symbol == key.X) and not CLINICAL_MODE:
            end_session(cancelled = True)

        elif symbol == key.P and not CLINICAL_MODE:
            mode.paused = not mode.paused
            pausedLabel.update()
            field.crosshair_update()

        elif symbol == key.F8 and not CLINICAL_MODE:
            mode.hide_text = not mode.hide_text
            update_all_labels()

        elif mode.tick != 0 and mode.trial_number > 0:
            if 'arithmetic' in mode.modalities[mode.mode]:
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


            for k in mode.modalities[mode.mode]:
                if not k == 'arithmetic':
                    keycode = cfg['KEY_%s' % k.upper()]
                    if symbol == keycode:
                        mode.inputs[k] = True
                        mode.input_rts[k] = time.time() - mode.trial_starttime
                        update_input_labels()

        if symbol == cfg.KEY_ADVANCE and mode.flags[mode.mode]['selfpaced']:
            mode.tick = mode.ticks_per_trial-2

    return pyglet.event.EVENT_HANDLED
# the loop where everything is drawn on the screen.
@window.event
def on_draw():
    if mode.shrink_brain:
        return
    window.clear()
    if mode.draw_graph:
        graph.draw()
    elif mode.saccadic:
        saccadic.draw()
    elif mode.title_screen:
        brain_graphic.draw()
        titleMessageLabel.draw()
        titleKeysLabel.draw()
    else:
        batch.draw()
        if not mode.started and not CLINICAL_MODE:
            brain_icon.draw()
            logoUpperLabel.draw()
            logoLowerLabel.draw()
    for label in input_labels:
        label.draw()

# the event timer loop. Runs every 1/10 second. This loop controls the session
# game logic.
# During each trial the tick goes from 1 to ticks_per_trial-1 then back to 0.
# tick = 1: Input from the last trial is saved. Input is reset.
#             A new square appears and the sound cue plays.
# tick = 6: the square disappears.
# tick = ticks_per_trial - 1: tick is reset to 0.
# tick = 1: etc.
def update(dt):
    if mode.started and not mode.paused: # only run the timer during a game
        if (not mode.flags[mode.mode]['selfpaced'] or
                mode.tick > mode.ticks_per_trial-6 or
                mode.tick < 5):
            mode.tick += 1
        if mode.tick == 1:
            mode.show_missed = False
            if mode.trial_number > 0:
                stats.save_input()
            mode.trial_number += 1
            mode.trial_starttime = time.time()
            trialsRemainingLabel.update()
            if mode.trial_number > mode.num_trials_total:
                end_session()
            else: generate_stimulus()
            reset_input()
        # Hide square at either the 0.5 second mark or sooner
        positions = len([mod for mod in mode.modalities[mode.mode] if mod.startswith('position')])
        positions = max(0, positions-1)
        if mode.tick == (6+positions) or mode.tick == mode.ticks_per_trial - 1:
            for visual in visuals: visual.hide()
        if mode.tick == mode.ticks_per_trial - 2:  # display feedback for 200 ms
            mode.tick = 0
            mode.show_missed = True
            update_input_labels()
        if mode.tick == mode.ticks_per_trial:
            mode.tick = 0
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
    if have_shapes:
        test_polygon = pyglet.shapes.Rectangle(100, 100, 200, 200, color=[0] * 3, batch=batch)
    else:
        test_polygon = batch.add(4, pyglet.gl.GL_QUADS, None, ('v2i', (
            100, 100,
            100, 200,
            200, 200,
            200, 100)),
                ('c3B', (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)))
    test_polygon.delete()
except Exception as e:
    debug_msg(e)
    quit_with_error('Error creating test polygon. Full text of error:\n')

# Instantiate the classes
mode = Mode()
field = Field()
visuals = [Visual() for i in range(4)]
stats = Stats()
graph = Graph()
circles = Circles()
saccadic = Saccadic()

updateLabel = UpdateLabel()
gameModeLabel = GameModeLabel()
jaeggiWarningLabel = JaeggiWarningLabel()
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
input_labels = []


# load last game mode
stats.initialize_session()
stats.parse_statsfile()
if len(stats.full_history) > 0 and not cfg.JAEGGI_MODE:
    mode.mode = stats.full_history[-1][1]
stats.retrieve_progress()

update_all_labels()

# Initialize brain sprite
brain_icon = pyglet.sprite.Sprite(pyglet.image.load(random.choice(resourcepaths['misc']['brain'])))
pos = (field.center_x - brain_icon.width//2,
       field.center_y - brain_icon.height//2)
pyglet2x = pyglet.version >= "2"
if pyglet2x:
    # add z component
    pos += (0,)
brain_icon.position = pos

if cfg.BLACK_BACKGROUND:
    brain_graphic = pyglet.sprite.Sprite(pyglet.image.load(random.choice(resourcepaths['misc']['splash-black'])))
else:
    brain_graphic = pyglet.sprite.Sprite(pyglet.image.load(random.choice(resourcepaths['misc']['splash'])))
pos = (field.center_x - brain_graphic.width//2,
       field.center_y - brain_graphic.height//2 + 40)
if pyglet2x:
    # add z component
    pos += (0,)
brain_graphic.position = pos
def scale_brain(dt):
    brain_graphic.scale = dt
    brain_graphic.x = field.center_x - brain_graphic.image.width//2  + scale_to_width(2) + (brain_graphic.image.width - brain_graphic.width) // 2
    brain_graphic.y = field.center_y - brain_graphic.image.height//2 + scale_to_height(60) + (brain_graphic.image.height - brain_graphic.height) // 2
    window.clear()
    brain_graphic.draw()
    if brain_graphic.width < 56:
        mode.shrink_brain = False
        pyglet.clock.unschedule(scale_brain)
        brain_graphic.scale = 1
        brain_graphic.position = (field.center_x - brain_graphic.width//2,
                           field.center_y - brain_graphic.height//2 + 40)

scale_brain(scale_to_width(1))
# If we had messages queued during loading (like from moving our data files), display them now
messagequeue.reverse()
for msg in messagequeue:
    Message(msg)

# start the event loops!
if __name__ == '__main__':

    pyglet.app.run()

# nothing below the line "pyglet.app.run()" will be executed until the
# window is closed or ESC is pressed.
