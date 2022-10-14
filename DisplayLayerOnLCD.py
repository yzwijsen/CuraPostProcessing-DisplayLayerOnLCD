# Cura PostProcessingPlugin
# Author:   Yannick Zwijsen
# Date:     September 13, 2022
# Description:  This plugin shows which layer is being printed on your 3D printer's LCD. (Based on DisplayFilenameAndLayerOnLCD by Amanda de Castilho)

from ..Script import Script
from UM.Application import Application

class DisplayLayerOnLCD(Script):
    def __init__(self):
        super().__init__()

    def getSettingDataString(self):
        return """{
            "name": "Display Layer On LCD",
            "key": "DisplayLayerOnLCD",
            "metadata": {},
            "version": 2,
            "settings":
            {
                "initialLayer":
                {
                    "label": "Initial layer number:",
                    "description": "Choose which number you prefer for the initial layer, 0 or 1",
                    "type": "int",
                    "default_value": 1,
                    "minimum_value": 0,
                    "maximum_value": 1                    
                },
                "showMaxLayer":
                {
                    "label": "Display max layer?:",
                    "description": "Display how many layers are in the entire print on status bar?",
                    "type": "bool",
                    "default_value": true
                }
            }
        }"""

    def execute(self, data):
        max_layer = 0
        lcd_text = "M117 Printing Layer "

        i = self.getSettingValueByKey("initialLayer")
        for layer in data:
            display_text = lcd_text + str(i)
            layer_index = data.index(layer)
            lines = layer.split("\n")
            for line in lines:
                # Get layer count
                if line.startswith(";LAYER_COUNT:"):
                    max_layer = line
                    max_layer = max_layer.split(":")[1]
                    # Decrease max layer by 1 if starting layer is set to 0
                    if self.getSettingValueByKey("initialLayer") == 0:
                        max_layer = str(int(max_layer) - 1)
                if line.startswith(";LAYER:"):
                    # Add max layer to lcd data if this option is selected
                    if self.getSettingValueByKey("showMaxLayer"):
                        display_text = display_text + " of " + max_layer
                    # Insert lcd status line into gcode file    
                    line_index = lines.index(line)
                    lines.insert(line_index + 1, display_text)
                    i += 1
            final_lines = "\n".join(lines)
            data[layer_index] = final_lines
        return data
