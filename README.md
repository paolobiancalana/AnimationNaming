# Animation Naming Tool

## Description

The Animation Naming Tool is a package that helps create a standardized naming convention for game animations. The package includes a Python class `AnimationNaming` that takes various parameters to form an animation name, and a PySide2 GUI that allows users to enter these parameters and get the resulting name.

## Structure

The package includes the following Python modules:

- `animation_naming.py`: This module contains the `AnimationNaming` class, which is responsible for creating the animation name.

- `gui_module.py`: This module contains a `Dialog` class, which is a PySide2 QDialog that allows users to enter the parameters for the `AnimationNaming` class.

## Usage

### AnimationNaming Class

The `AnimationNaming` class takes the following parameters:

- `action` (required): The primary action of the animation (e.g., "walk", "jump", "attack").

- `direction` (optional): The direction of the animation (e.g., "forward", "left", "right", "backward").

- `secondary_action` (optional): Any secondary action in the animation.

- `variant` (optional): If there are multiple animations with the same actions and direction, this variant number distinguishes them.

- `meters` (optional): The distance covered in the animation. For a jump, this could be a dictionary with 'x' and 'y' keys.

### PySide2 GUI

To use the GUI, launch `gui_module.py`. This will open a dialog box with fields for each of the parameters for the `AnimationNaming` class. Enter your desired parameters and click "Submit" to print the resulting animation name.

### Launching in Maya

If you're using this package within Maya, you can launch the PySide2 dialog from the Maya environment using the following code:

```python
import maya.OpenMayaUI as omui
from PySide2 import QtWidgets
from shiboken2 import wrapInstance
from gui_module import Dialog

def maya_main_window():
    main_window_ptr = omui.MQtUtil.mainWindow()
    return wrapInstance(int(main_window_ptr), QtWidgets.QWidget)

dialog = Dialog(parent=maya_main_window())
dialog.show()
```

## Note

When you import `AnimationNaming` and `Dialog` in your own code, be sure to adjust the import statements according to your package structure.
