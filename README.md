# mylinespacing
my line-spacing plugin for Gedit 3

first appearance : 2017-03-06

##  getting files and installations

1. move gedit plugin directory

    cd ~/.local/share/gedit/plugins

2. download files using git command

    git clone github.com/GaraSharp/mylinespacing

3. modify files fit for your needs

    +  linespacing.plugin

        set author name and copyrights, and others as you need.

    +  linespacing.py

        set parameters in line# 60-66 as follows : 

         \#  line fold flag added on 2016/01/31

        \#  0 for phisical, 1 for logical
            
        self.fold = 0
        
        \#  line spacing holdre added on 2016-08-01

        \#  set this to initialize line feed size

        self.feed = 5

    default, linespacing applies in "Phisical line" and linespacing size is 5.

4. activate linespacing plugins from gedit menu



##  Usage and Dosage

+ Ctrl+1	linespacing widen
+ Ctrl+2	linespacing narrowly
+ Ctrl+3	reset linespacing default
+ Alt+e 	insert date stamp with fixed format (like : 2017-03-06 21:50:43 )

running gedit from terminal, error messages appears like as follows :

        Traceback (most recent call last):
          File "/home/user/.local/share/gedit/plugins/linespacing.py", line 100, in do_update_state
            view.set_pixels_below_lines(self.feed)
        AttributeError: 'NoneType' object has no attribute 'set_pixels_below_lines'
        
        (gedit:1349): Gtk-WARNING **: Allocating size to GtkOverlay 0x12f5130 without calling gtk_widget_get_preferred_width/height(). How does the code know the size to allocate?
        Traceback (most recent call last):
          File "/home/user/.local/share/gedit/plugins/linespacing.py", line 100, in do_update_state
            view.set_pixels_below_lines(self.feed)
        AttributeError: 'NoneType' object has no attribute 'set_pixels_below_lines'
        
        (gedit:1349): Gtk-CRITICAL **: gtk_scrolled_window_set_min_content_height: assertion 'height == -1 || priv->max_content_height == -1 || height <= priv->max_content_height' failed

this plugin runs before allocate text-buffer window, so could not refer text-buffer window structure member , it seems.
currently I have no idea to fix.

these error messages appears only in first time. after allocate text-buffer window, this scripts will work fine (?)


