# -*- coding: utf-8 -*-
# title : linespacing plugin for gedit 3.12 and upper
# begin : 2014-04-30 14:26:55 
# modif : 2016-02-03 17:08:19 

from gi.repository import GObject, Gio, Gtk, Gedit
import gettext
##from gpdefs import *
from time import *

#  from gedit 3.12, keyboard shortcut setting way like as follows (it seems ... ) :

class LineSpacingAppActivatable(GObject.Object, Gedit.AppActivatable):

    app = GObject.property(type=Gedit.App)

    def __init__(self):
        GObject.Object.__init__(self)

    #  <Primary> means Control key. also usable <Alt>, <Shift> modifier keys.
    #  Logical/Phisical line-spacing toggle and reset line-spacing by Ctrl+Alt+3 key 
    #  Time stamp by Alt+e key for GNOME desktop

    def do_activate(self):
        self.app.set_accels_for_action("win.spacing-larger",  ["<Primary>1", "<Primary>KP_7"])
        self.app.set_accels_for_action("win.spacing-smaller", ["<Primary>2", "<Primary>KP_8"])
        self.app.set_accels_for_action("win.spacing-reset",   ["<Primary>3", "<Primary>KP_9"])
        self.app.set_accels_for_action("win.spacing-toggle",  ["<Primary><Alt>3", "<Primary><Alt>KP_9"])
        self.app.set_accels_for_action("win.str-stamp",       ["<Alt>e"])

        #  item adding for menu. from bottom, items are registered.
        self.menu_ext = self.extend_menu("view-section-2")
        item = Gio.MenuItem.new(_("Stamp Date/Time string (M-e)"), "win.str-stamp")
        self.menu_ext.prepend_menu_item(item)
        item = Gio.MenuItem.new(_("Toggle fold mode (C-M-3)"),     "win.spacing-toggle")
        self.menu_ext.prepend_menu_item(item)
        item = Gio.MenuItem.new(_("Reset spacing (C-3)"),          "win.spacing-reset")
        self.menu_ext.prepend_menu_item(item)
        item = Gio.MenuItem.new(_("Smaller spacing (C-2)"),        "win.spacing-smaller")
        self.menu_ext.prepend_menu_item(item)
        item = Gio.MenuItem.new(_("Larger spacing (C-1)"),         "win.spacing-larger")
        self.menu_ext.prepend_menu_item(item)

    def do_deactivate(self):
        self.app.set_accels_for_action("win.spacing-larger",  [])
        self.app.set_accels_for_action("win.spacing-smaller", [])
        self.app.set_accels_for_action("win.spacing-reset",   [])
        self.app.set_accels_for_action("win.spacing-toggle",  [])
        self.app.set_accels_for_action("win.str-stamp",       [])
        self.menu_ext = None

#  main part

class LineSpacing(GObject.Object, Gedit.WindowActivatable):
    __gtype_name__ = "LineSpacing"
    window = GObject.property(type=Gedit.Window)
   
    def __init__(self):
        GObject.Object.__init__(self)
        #  line fold flag added on 2016/01/31
        #  0 for phisical, 1 for logical
        self.fold = 0
        #  line spacing holdre added on 2016-08-01
        #  set this to initialize line feed size
        self.feed = 5
        
    def do_activate(self):
        action = Gio.SimpleAction(name="spacing-larger")
        action.connect('activate', self.on_linespacing_activate1)
        self.window.add_action(action)

        action = Gio.SimpleAction(name="spacing-smaller")
        action.connect('activate', self.on_linespacing_activate2)
        self.window.add_action(action)

        action = Gio.SimpleAction(name="spacing-reset")
        action.connect('activate', self.on_linespacing_activate3)
        self.window.add_action(action)

        action = Gio.SimpleAction(name="spacing-toggle")
        action.connect('activate', self.on_linespacing_activate4)
        self.window.add_action(action)

        action = Gio.SimpleAction(name="str-stamp")
        action.connect('activate', self.on_linespacing_activate5)
        self.window.add_action(action)


    def do_deactivate(self):
        self.window.remove_action("spacing-larger")
        self.window.remove_action("spacing-smaller")
        self.window.remove_action("spacing-reset")
        self.window.remove_action("spacing-toggle")
        self.window.remove_action("str-stamp")

    # this hook is eval for every widget mapped/updated (It seems).
    def do_update_state(self):
        # initial linespacing setting part.
        view = self.window.get_active_view()
        view.set_pixels_below_lines(self.feed)
        if self.fold == 0:
            view.set_pixels_inside_wrap(self.feed)
#        pass

    #  increase line-spacing
    def on_linespacing_activate1(self, action, data=None):
        view = self.window.get_active_view()
        if view:
            view.set_pixels_below_lines(view.get_pixels_below_lines() + 1)
            if self.fold == 0:
                view.set_pixels_inside_wrap(view.get_pixels_inside_wrap() + 1)

    #  decrease line-spacing
    def on_linespacing_activate2(self, action, data=None):
        view = self.window.get_active_view()
        if view:
            if view.get_pixels_below_lines() > 0:
                view.set_pixels_below_lines(view.get_pixels_below_lines() - 1)
            if view.get_pixels_inside_wrap() > 0 and self.fold == 0:
                view.set_pixels_inside_wrap(view.get_pixels_inside_wrap() - 1)

    #  reset line-spacing
    def on_linespacing_activate3(self, action, data=None):
        view = self.window.get_active_view()
        if view:
            view.set_pixels_below_lines(self.feed)
            view.set_pixels_inside_wrap(self.feed)

    #  toggle Logical/Phisical mode and reset line-spacing
    def on_linespacing_activate4(self, action, data=None):
        view = self.window.get_active_view()
        if view:
            view.set_pixels_below_lines(0)
            view.set_pixels_inside_wrap(0)
            self.fold = 1-self.fold

    #  time stamp in fixed format like "2016-04-21 09:00:00 "
    def on_linespacing_activate5(self, action, data=None):
        doc  = self.window.get_active_document()
        tm = localtime()
        doc.insert_at_cursor(str(tm.tm_year)+'-'+('0'+str(tm.tm_mon))[-2:]+'-'+('0'+str(tm.tm_mday))[-2:]+' '+('0'+str(tm.tm_hour))[-2:]+':'+('0'+str(tm.tm_min))[-2:]+':'+('0'+str(tm.tm_sec))[-2:]+' ')


    def _remove_ui(self):
        manager = self.window.get_ui_manager()
        manager.remove_ui(self._ui_merge_id)
        manager.remove_action_group(self._actions)
        manager.ensure_update()

