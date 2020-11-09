# keychain
Python framework for intuitive animation scripting in Maya.

# API #
## Timeline ##

```python
from keyframe.api import timeline
tl = timeline.Timeline()
```

Get / set frame information

```python
current_frame = tl.current_frame
tl.current_frame = 10
```

# Tools #
Tools in keychain follow a plug-in style pattern.

## Toolbar ##
They Toolbar is dynamically populated using the main package config
and will recursively search the paths listed in the `KC_TOOLS`
environment variable for tools under same name.   

```json
"UI":{
    "tools":[
        "archer",
        "tracer"
    ]
}
```
![Toolbar example](docs\images\toolbar_settings.gif)

## Writing Tools ##
Tools can be written/added from any directory listed under the `KC_TOOLS`
environment variable.

### File Convention ###
Every tool expects a `main.py` with a `launch()` method like the following:
```python
# main.py

# UI entry point to launch the tool
def launch():
    print ("Tool Active")
```
The launch method will be called when the tool's button in the toolbar is pressed.

A more complex example using a controller class:
```python
class Controller(object):
  def __init__(self):
    # Setup Logic
    pass
  def run(self):
    # Main method
    pass

def launch():
    # UI entry point to launch the tool  
    controller = Controller()
    return controller.run()
```


### Settings ###
Settings serve two main functions in keychain:
  1. To have a clean, maintainable way of changing preferences without the need
  to touch core api.
  2. To standardized and automate the process of writing UI code by automatically
  creating a settings menu from the config.

```json
{
    "icon":"tracer",
    "settings":{
        "blend":{
            "name":"Blend",
            "type":"double",
            "default":1,
            "minimum":0,
            "maximum":1
        },
        "steps":{
            "name":"Steps",
            "type":"int",
            "default":3,
            "minimum":1
        },
}
```
