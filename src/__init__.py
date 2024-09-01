# Copyright 2021-2024 Dale Price
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


import bpy
from bpy.app.handlers import persistent
from .vendor import darkdetect

themes_paths = bpy.utils.preset_paths('interface_theme')

default_light_theme = "Blender_Light.xml"
default_dark_theme = "Blender_Dark.xml"

class ADMAutoDarkMode(bpy.types.AddonPreferences):
    """Preferences for Auto Dark Mode"""
    bl_idname = __package__
    
    light_theme: bpy.props.StringProperty(
        name="Light Mode Theme",
        description="Theme to use when the system is in Light Mode",
        subtype="FILE_NAME",
        default=default_light_theme
    )
    dark_theme: bpy.props.StringProperty(
        name="Dark Mode Theme",
        description="Theme to use when the system is in Dark Mode",
        subtype="FILE_NAME",
        default=default_dark_theme
    )
    
    def draw(self, context):
        layout = self.layout
        col = layout.column()
        row = col.row(heading="☀️ Light Mode Theme")
        row.menu("ADM_MT_light_theme_preset", text=bpy.path.display_name(context.preferences.addons[__package__].preferences.light_theme))
        
        col = layout.column()
        row = col.row(heading="🌙 Dark Mode Theme")
        row.menu("ADM_MT_dark_theme_preset", text=bpy.path.display_name(context.preferences.addons[__package__].preferences.dark_theme))

class ADM_update_theme(bpy.types.Operator):
    """Update the Auto Dark Mode theme to match the OS"""
    bl_idname="adm.update_theme"
    bl_label = "Match Current System Theme"
    bl_options = {'INTERNAL'}
    
    def execute(self, context):
        # print("Previously, dark theme was", bpy.types.WindowManager.ADM_dark_mode_active)
        
        if darkdetect.isDark():
            # print("OS theme is dark")
            if bpy.types.WindowManager.ADM_dark_mode_active is None or bpy.types.WindowManager.ADM_dark_mode_active == False:
                # print("OS theme differed from blender theme, setting to dark")
                self.set_theme(False, context)
                bpy.types.WindowManager.ADM_dark_mode_active = True
        else:
            # print("OS theme is light")
            if bpy.types.WindowManager.ADM_dark_mode_active is None or bpy.types.WindowManager.ADM_dark_mode_active == True:
                # print("OS theme differed from blender theme, setting to light")
                self.set_theme(True, context)
                bpy.types.WindowManager.ADM_dark_mode_active = False
        
        return {'FINISHED'}
    
    def set_theme(self, light, context):
        preferences = context.preferences
        addon_prefs = preferences.addons[__package__].preferences
        
        light_theme = default_light_theme if not addon_prefs.light_theme else addon_prefs.light_theme
        dark_theme = default_dark_theme if not addon_prefs.dark_theme else addon_prefs.dark_theme
        
        filename = light_theme if light else dark_theme
        
        # look for the theme first in user themes path, then in system themes path
        for path in reversed(themes_paths):
            filepath = path + "/" + filename
            try:
                # Check whether the file exists by trying to open it (if it fails, we continue on to the next themes directory path)
                file = open(filepath)
                file.close()
                
                #if the file exists, set it and exit the loop
                bpy.ops.script.execute_preset(filepath=filepath, menu_idname="USERPREF_MT_interface_theme_presets")
                break
            except:
                continue
        else:
            # use default theme if the one specified isn't found in any of the preset paths
            filename = default_light_theme if light else default_dark_theme
            filepath = themes_paths[0] + "/" + filename
            bpy.ops.script.execute_preset(filepath=filepath, menu_idname="USERPREF_MT_interface_theme_presets")

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
        filename = bpy.path.basename(filepath)
        
        preferences = context.preferences
        addon_prefs = preferences.addons[__package__].preferences
        
        addon_prefs.light_theme = filename
        
        force_theme_update()
        
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
        filename = bpy.path.basename(filepath)
        
        preferences = context.preferences
        addon_prefs = preferences.addons[__package__].preferences
        
        addon_prefs.dark_theme = filename
        
        force_theme_update()
        
        return {'FINISHED'}

class ADM_MT_light_theme_preset(bpy.types.Menu):
    """Choose a theme preset for light mode"""
    bl_label = "Choose from presets…"
    bl_description = "The theme to use when the system is in light mode"
    preset_subdir = "interface_theme"
    preset_operator = "adm.set_light_theme"
    preset_type = 'XML'
    preset_xml_map = (
        ("preferences.themes[0]", "Theme"),
        ("preferences.ui_styles[0]", "ThemeStyle"),
    )
    
    draw = bpy.types.Menu.draw_preset

class ADM_MT_dark_theme_preset(bpy.types.Menu):
    """Choose a theme preset for dark mode"""
    bl_label = "Choose from presets…"
    bl_description = "The theme to use when the system is in dark mode"
    preset_subdir = "interface_theme"
    preset_operator = "adm.set_dark_theme"
    preset_type = 'XML'
    preset_xml_map = (
        ("preferences.themes[0]", "Theme"),
        ("preferences.ui_styles[0]", "ThemeStyle"),
    )
    
    draw = bpy.types.Menu.draw_preset

def force_theme_update():
    """Apply the relevant theme to match the OS regardless of whether it was already active."""
    # set dark_mode_active to None so the theme gets set again to match the preference change regardless of whether light or dark was active before
    bpy.types.WindowManager.ADM_dark_mode_active = None
    bpy.ops.adm.update_theme()

@persistent
def periodic_update():
    """Poll for changes to the system dark mode."""
    bpy.ops.adm.update_theme()
    # print("ran periodic update")
    return 10.0

def start_watching():
    """Start watching for changes, either by starting polling or by listening for changes from the OS"""
    bpy.app.timers.register(periodic_update, persistent=True)
    # print("started periodic update")

def register():
    bpy.types.WindowManager.ADM_dark_mode_active = None
    
    bpy.utils.register_class(ADMAutoDarkMode)
    bpy.utils.register_class(ADM_update_theme)
    bpy.utils.register_class(ADM_MT_light_theme_preset)
    bpy.utils.register_class(ADM_MT_dark_theme_preset)
    bpy.utils.register_class(ADM_set_light_theme)
    bpy.utils.register_class(ADM_set_dark_theme)
    
    start_watching();

def unregister():
    bpy.app.timers.unregister(periodic_update)
    
    bpy.utils.unregister_class(ADMAutoDarkMode)
    bpy.utils.unregister_class(ADM_update_theme)
    bpy.utils.unregister_class(ADM_MT_light_theme_preset)
    bpy.utils.unregister_class(ADM_MT_dark_theme_preset)
    bpy.utils.unregister_class(ADM_set_light_theme)
    bpy.utils.unregister_class(ADM_set_dark_theme)