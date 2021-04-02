# Copyright 2021 Dale Price
# 
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

bl_info = {
    "name": "Auto Dark Mode",
    "description": "Automatically follow the system light/dark mode.",
    "author": "Dale Price",
    "version": (1, 0, 0),
    "blender": (2, 90, 0),
    "category": "User Interface"
}

# TODO: see what happens if a theme set in ADM is removed and ADM tries to set it anyway

import bpy
from bpy.app.handlers import persistent
from .vendor import darkdetect

default_light_theme = bpy.utils.preset_paths('interface_theme')[0] + "/blender_light.xml"
default_dark_theme = bpy.utils.preset_paths('interface_theme')[0] + "/blender_dark.xml"

class ADMAutoDarkMode(bpy.types.AddonPreferences):
    """Preferences for Auto Dark Mode"""
    bl_idname = __name__
    
    light_theme: bpy.props.StringProperty(
        name="Light Mode Theme",
        description="Theme to use when the system is in Light Mode",
        subtype="FILE_PATH",
        default=default_light_theme
    )
    dark_theme: bpy.props.StringProperty(
        name="Dark Mode Theme",
        description="Theme to use when the system is in Dark Mode",
        subtype="FILE_PATH",
        default=default_dark_theme
    )
    
    def draw(self, context):
        layout = self.layout
        col = layout.column()
        col.prop(self, "light_theme")
        col.menu("ADM_MT_light_theme_preset", text=ADM_MT_light_theme_preset.bl_label)
        
        col = layout.column()
        col.prop(self, "dark_theme")
        col.menu("ADM_MT_dark_theme_preset", text=ADM_MT_dark_theme_preset.bl_label)

class ADM_update_theme(bpy.types.Operator):
    """Update the Auto Dark Mode theme to match the OS"""
    bl_idname="adm.update_theme"
    bl_label = "Match Current System Theme"
    bl_options = {'INTERNAL'}
    
    def execute(self, context):
        preferences = context.preferences
        addon_prefs = preferences.addons[__name__].preferences
        
        light_theme = default_light_theme if not addon_prefs.light_theme else addon_prefs.light_theme
        dark_theme = default_dark_theme if not addon_prefs.dark_theme else addon_prefs.dark_theme
        
        # print("Previously, dark theme was", bpy.types.WindowManager.ADM_dark_mode_active)
        
        if darkdetect.isDark():
            # print("OS theme is dark")
            if bpy.types.WindowManager.ADM_dark_mode_active is None or bpy.types.WindowManager.ADM_dark_mode_active == False:
                # print("OS theme differed from blender theme, setting to dark")
                bpy.ops.script.execute_preset(filepath=dark_theme, menu_idname="USERPREF_MT_interface_theme_presets")
                bpy.types.WindowManager.ADM_dark_mode_active = True
        else:
            # print("OS theme is light")
            if bpy.types.WindowManager.ADM_dark_mode_active is None or bpy.types.WindowManager.ADM_dark_mode_active == True:
                # print("OS theme differed from blender theme, setting to light")
                bpy.ops.script.execute_preset(filepath=light_theme, menu_idname="USERPREF_MT_interface_theme_presets")
                bpy.types.WindowManager.ADM_dark_mode_active = False
        
        return {'FINISHED'}

class ADM_set_light_theme(bpy.types.Operator):
    """Set light theme for Auto Dark Mode"""
    bl_idname = "adm.set_light_theme"
    bl_label = "Set a theme for Auto Light Mode"
    bl_options = {'INTERNAL'}
    
    filepath: bpy.props.StringProperty(
        subtype='FILE_PATH',
        options={'HIDDEN', 'SKIP_SAVE'},
    )
    
    menu_idname: bpy.props.StringProperty(
        name="Menu ID Name",
        description="ID name of the menu this was called from",
        options={'HIDDEN', 'SKIP_SAVE'},
    )
    
    def execute(self, context):
        from os.path import basename
        filepath = self.filepath
        
        preferences = context.preferences
        addon_prefs = preferences.addons[__name__].preferences
        
        addon_prefs.light_theme = filepath
        
        bpy.ops.adm.update_theme()
        
        return {'FINISHED'}

class ADM_set_dark_theme(bpy.types.Operator):
    """Set dark theme for Auto Dark Mode"""
    bl_idname = "adm.set_dark_theme"
    bl_label = "Set a theme for Auto Dark Mode"
    bl_options = {'INTERNAL'}
    
    filepath: bpy.props.StringProperty(
        subtype='FILE_PATH',
        options={'HIDDEN', 'SKIP_SAVE'},
    )
    
    menu_idname: bpy.props.StringProperty(
        name="Menu ID Name",
        description="ID name of the menu this was called from",
        options={'HIDDEN', 'SKIP_SAVE'},
    )
    
    def execute(self, context):
        from os.path import basename
        filepath = self.filepath
        
        preferences = context.preferences
        addon_prefs = preferences.addons[__name__].preferences
        
        addon_prefs.dark_theme = filepath
        
        # set dark_mode_active to None so the theme gets set again to match the preference change regardless of whether light or dark was active before
        bpy.types.WindowManager.ADM_dark_mode_active = None
        bpy.ops.adm.update_theme()
        
        return {'FINISHED'}

class ADM_MT_light_theme_preset(bpy.types.Menu):
    """Menu for choosing a theme preset for light mode."""
    bl_label = "Choose from presets…"
    preset_subdir = "interface_theme"
    preset_operator = "adm.set_light_theme"
    preset_type = 'XML'
    preset_xml_map = (
        ("preferences.themes[0]", "Theme"),
        ("preferences.ui_styles[0]", "ThemeStyle"),
    )
    
    draw = bpy.types.Menu.draw_preset
    
    @staticmethod
    def reset_cb(context):
        bpy.ops.preferences.reset_default_theme()

class ADM_MT_dark_theme_preset(bpy.types.Menu):
    """Menu for choosing a theme preset for dark mode."""
    bl_label = "Choose from presets…"
    preset_subdir = "interface_theme"
    preset_operator = "adm.set_dark_theme"
    preset_type = 'XML'
    preset_xml_map = (
        ("preferences.themes[0]", "Theme"),
        ("preferences.ui_styles[0]", "ThemeStyle"),
    )
    
    draw = bpy.types.Menu.draw_preset
    
    @staticmethod
    def reset_cb(context):
        bpy.ops.preferences.reset_default_theme()

def periodic_update():
    """Poll for changes to the system dark mode."""
    bpy.ops.adm.update_theme()
    # print("ran periodic update")
    return 10.0

@persistent
def reinstate_timers(dummy = None, dummy2 = None):
    """Just setting a timer in bpy.app.timers isn't enough because apparently all timers get cleared whenever a new blend file is loaded, with no way to opt out of that behavior. This needs to get called whenever a new blend file is loaded to start the timer again."""
    bpy.app.timers.register(periodic_update)
    # print("reinstated periodic update")

def register():
    bpy.types.WindowManager.ADM_dark_mode_active = None
    
    bpy.utils.register_class(ADMAutoDarkMode)
    bpy.utils.register_class(ADM_update_theme)
    bpy.utils.register_class(ADM_MT_light_theme_preset)
    bpy.utils.register_class(ADM_MT_dark_theme_preset)
    bpy.utils.register_class(ADM_set_light_theme)
    bpy.utils.register_class(ADM_set_dark_theme)
    
    # every time a blend file is loaded, the dark mode polling timer needs to be set up again
    bpy.app.handlers.load_post.append(reinstate_timers)
    reinstate_timers();

def unregister():
    bpy.app.handlers.load_post.remove(reinstate_timers)
    bpy.app.timers.unregister(periodic_update)
    
    bpy.utils.unregister_class(ADMAutoDarkMode)
    bpy.utils.unregister_class(ADM_update_theme)
    bpy.utils.unregister_class(ADM_MT_light_theme_preset)
    bpy.utils.unregister_class(ADM_MT_dark_theme_preset)
    bpy.utils.unregister_class(ADM_set_light_theme)
    bpy.utils.unregister_class(ADM_set_dark_theme)