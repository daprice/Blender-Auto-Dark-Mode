# 🌗 Blender Auto Dark Mode
This add-on for [Blender](https://www.blender.org) lets you choose separate UI theme presets for light and dark mode and automatically matches the light/dark mode of your operating system. If you have your computer automatically switch between light and dark mode throughout the day, this add-on will keep Blender in sync as it changes.

<figure>
  <img src="screenshot.png" alt="Side-by-side screenshots of Blender on macOS 11, showcasing the &ldquo;White&rdquo; Blender theme to match light mode and the &ldquo;Blender Dark&rdquo; theme to match dark mode." width="800" />
  <figcaption>Showing off the "White" and "Blender Dark" themes (included with Blender), matching light and dark mode on macOS 11 with the help of Auto Dark Mode</figcaption>
</figure>

Auto Dark Mode will match the system light/dark mode on macOS 10.14 or newer, Windows 10, or Linux with GTK.

## Installation

<a href="https://github.com/daprice/Blender-Auto-Dark-Mode/releases/latest/download/Auto_Dark_Mode.zip" download>Download the .zip package of the latest release</a> (you may need to right click and choose "Download Linked File" to avoid automatically unzipping the package). Add it to Blender using `Edit > Preferences > Add-ons > Install…`, then click the checkbox next to the add-on to activate it.

## Usage

Once activated, the add-on works automatically. You can change the theme presets used for light and dark mode under `Edit > Preferences > Add-ons > User Interface: Auto Dark Mode` (by default, it uses the “Blender Light” and “Blender Dark” themes).

***
Want more themes to pick from? Look in [the Themes forum thread](https://devtalk.blender.org/t/call-for-content-themes) or [Blend Swap](https://www.blendswap.com/blends/category/22).
***

## ⚠️ Warnings

When Auto Dark Mode is installed, always change your preferred light and dark theme under `Preferences > Add-ons > User Interface: Auto Dark Mode`. Theme selections from `Preferences > Themes` will only last until the next light/dark mode switch occurs.

If you have made customizations to individual elements of the Blender user interface in `Preferences > Themes`, save your customizations as a preset before installing Auto Dark Mode. Otherwise, Auto Dark Mode will overwrite your changes. After installation, choose your saved preset in `Preferences > Add-ons > User Interface: Auto Dark Mode`.

While customizing a theme, disable Auto Dark Mode to avoid having your changes overwritten.

If you install this on a system that does not support dark mode, only the Light Mode preset within this add-on will be used.

## License

The Auto Dark Mode add-on is available under the GNU GPL v3 license. See the LICENSE file for more info.

This add-on includes the [darkdetect](https://pypi.org/project/darkdetect/) Python package, which is copyright © Alberto Sottile and distributed under the 3-clause BSD License.
