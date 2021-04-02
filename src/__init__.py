bl_info = {
    "name": "Auto Dark Mode",
    "description": "Automatically follow the system light/dark mode.",
    "author": "Dale Price",
    "version": (1, 0, 0),
    "blender": (2, 90, 0),
    "category": "User Interface",
}

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
        
        return {'FINISHED'}

class ADM_MT_light_theme_preset(bpy.types.Menu):
    bl_label = "Light theme presets"
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
    bl_label = "Dark theme presets"
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

def register():
    bpy.utils.register_class(ADMAutoDarkMode)
    bpy.utils.register_class(ADM_MT_light_theme_preset)
    bpy.utils.register_class(ADM_MT_dark_theme_preset)
    bpy.utils.register_class(ADM_set_light_theme)
    bpy.utils.register_class(ADM_set_dark_theme)

def unregister():
    bpy.utils.unregister_class(ADMAutoDarkMode)
    bpy.utils.unregister_class(ADM_MT_light_theme_preset)
    bpy.utils.unregister_class(ADM_MT_dark_theme_preset)
    bpy.utils.unregister_class(ADM_set_light_theme)
    bpy.utils.unregister_class(ADM_set_dark_theme)