bl_info = {
    "name": "Auto Dark Mode",
    "description": "Automatically follow the system light/dark mode.",
    "author": "Dale Price",
    "version": (1, 0, 0),
    "blender": (2, 90, 0),
    "category": "User Interface",
    "warning": "Blender may take up to 60 seconds to react to theme changes. Manually changing the theme in the Themes panel may cause unexpected results."
}

# TODO: see what happens if a theme set in ADM is removed and ADM tries to set it anyway

import bpy
from .vendor import darkdetect

default_light_theme = bpy.utils.preset_paths('interface_theme')[0] + "/blender_light.xml"
default_dark_theme = bpy.utils.preset_paths('interface_theme')[0] + "/blender_dark.xml"

class ADMAutoDarkMode(bpy.types.AddonPreferences):
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
        col.label(text = "Light Mode Theme")
        col.menu("ADM_MT_light_theme_preset", text=ADM_MT_light_theme_preset.bl_label)
        
        col = layout.column()
        col.label(text = "Dark Mode Theme")
        col.menu("ADM_MT_dark_theme_preset", text=ADM_MT_dark_theme_preset.bl_label)

class ADM_update_theme(bpy.types.Operator):
    """Update Auto Dark Mode Theme"""
    bl_idname="adm.update_theme"
    bl_label = "Match current system theme"
    
    dark_theme_active: bpy.props.BoolProperty(
        options={'SKIP_SAVE'},
    )
    
    def execute(self, context):
        preferences = context.preferences
        addon_prefs = preferences.addons[__name__].preferences
        
        light_theme = default_light_theme if not addon_prefs.light_theme else addon_prefs.light_theme
        dark_theme = default_dark_theme if not addon_prefs.dark_theme else addon_prefs.dark_theme
        
        dark_theme_active = None if not self.dark_theme_active else self.dark_theme_active
        
        if darkdetect.isDark():
            if dark_theme_active is None or dark_theme_active == False:
                bpy.ops.script.execute_preset(filepath=dark_theme, menu_idname="USERPREF_MT_interface_theme_presets")
                self.dark_theme_active = True
        else:
            
            if dark_theme_active is None or dark_theme_active == True:
                bpy.ops.script.execute_preset(filepath=light_theme, menu_idname="USERPREF_MT_interface_theme_presets")
                self.dark_theme_active = False
        
        return {'FINISHED'}

class ADM_set_light_theme(bpy.types.Operator):
    """Set Auto Light Mode Theme"""
    bl_idname = "adm.set_light_theme"
    bl_label = "Set a theme for Auto Light Mode"
    bl_options = {'INTERNAL'}
    
    filepath: bpy.props.StringProperty(
        subtype='FILE_PATH',
        options={'SKIP_SAVE'},
    )
    
    menu_idname: bpy.props.StringProperty(
        name="Menu ID Name",
        description="ID name of the menu this was called from",
        options={'SKIP_SAVE'},
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
    """Set Auto Dark Mode Theme"""
    bl_idname = "adm.set_dark_theme"
    bl_label = "Set a theme for Auto Dark Mode"
    bl_options = {'INTERNAL'}
    
    filepath: bpy.props.StringProperty(
        subtype='FILE_PATH',
        options={'SKIP_SAVE'},
    )
    
    menu_idname: bpy.props.StringProperty(
        name="Menu ID Name",
        description="ID name of the menu this was called from",
        options={'SKIP_SAVE'},
    )
    
    def execute(self, context):
        from os.path import basename
        filepath = self.filepath
        
        preferences = context.preferences
        addon_prefs = preferences.addons[__name__].preferences
        
        addon_prefs.dark_theme = filepath
        
        bpy.ops.adm.update_theme()
        
        return {'FINISHED'}

class ADM_MT_light_theme_preset(bpy.types.Menu):
    bl_label = "Change Light Mode preset…"
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
    bl_label = "Change Dark Mode preset…"
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

def initial_update():
    bpy.app.timers.register(periodic_update)

def periodic_update():
    bpy.ops.adm.update_theme()
    return 30.0

def register():
    bpy.utils.register_class(ADMAutoDarkMode)
    bpy.utils.register_class(ADM_update_theme)
    bpy.utils.register_class(ADM_MT_light_theme_preset)
    bpy.utils.register_class(ADM_MT_dark_theme_preset)
    bpy.utils.register_class(ADM_set_light_theme)
    bpy.utils.register_class(ADM_set_dark_theme)
    
    bpy.app.timers.register(initial_update, first_interval = 1)

def unregister():
    bpy.utils.unregister_class(ADMAutoDarkMode)
    bpy.utils.unregister_class(ADM_update_theme)
    bpy.utils.unregister_class(ADM_MT_light_theme_preset)
    bpy.utils.unregister_class(ADM_MT_dark_theme_preset)
    bpy.utils.unregister_class(ADM_set_light_theme)
    bpy.utils.unregister_class(ADM_set_dark_theme)
    
    bpy.app.timers.unregister(periodic_update)