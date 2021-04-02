bl_info = {
    "name": "Auto Dark Mode",
    "description": "Automatically follow the system light/dark mode on MacOS, Windows 10, and Linux with GTK.",
    "author": "Dale Price",
    "version": (1, 0, 0),
    "blender": (2, 90, 0),
    "category": "User Interface",
}

import bpy
from .vendor import darkdetect

