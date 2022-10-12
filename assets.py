# import base64
# import struct
# from time import sleep
# from PIL import Image
# import numpy as np
from typing import Optional
import xml.etree.ElementTree as ET

class Interactive:

    def __init__(self, node:ET.Element):
        self.node = node
        self.pages:list[Page] = []
        self.width = int(self.node.find('Video').attrib['Width'])
        self.height = int(self.node.find('Video').attrib['Height'])
        self.getPages()
        
    @property
    def caption(self):
        return self.node.find('Caption').text
    @caption.setter
    def caption(self, x:str):
        self.node.find('Caption').text = x

    def getPages(self):
        for pageNode in self.node.find('InterData/Pages'):
            self.pages.append(Page(pageNode, self))


class Page:

    def __init__(self, node:ET.Element, parent:Interactive):
        self.node = node
        self.parent = parent
        self.id = int(node.attrib['Page_id'])
        self.bogs:list[BOG] = []
        self.getBOGs()

    @property
    def caption(self):
        return self.node.find('Caption').text
    @caption.setter
    def caption(self, x:str):
        self.node.find('Caption').text = x

    def getBOGs(self):
        for bogNode in self.node.find('BOGs'):
            self.bogs.append(BOG(bogNode, self))


class BOG:

    def __init__(self, node:ET.Element, parent:Page):
        self.node = node
        self.parent = parent
        self.buttons:list[Button] = []
        self.getButtons()

    @property
    def caption(self):
        return self.node.find('Caption').text
    @caption.setter
    def caption(self, x:str):
        self.node.find('Caption').text = x

    def getButtons(self):
        for buttonNode in self.node.find('Buttons'):
            self.buttons.append(Button(buttonNode, self))

class Button:

    def __init__(self, node:ET.Element, parent:BOG):
        self.node = node
        self.parent = parent
        self.id = int(node.find('Button_id').text)

    @property
    def caption(self):
        return self.node.find('Caption').text
    @caption.setter
    def caption(self, x:str):
        self.node.find('Caption').text = x

    @property
    def up(self):
        return int(self.node.find('Upper_button_id_ref').text)
    @up.setter
    def up(self, value:int):
        self.node.find('Upper_button_id_ref').text = str(value)

    @property
    def down(self):
        return int(self.node.find('Lower_button_id_ref').text)
    @down.setter
    def down(self, value:int):
        self.node.find('Lower_button_id_ref').text = str(value)

    @property
    def left(self):
        return int(self.node.find('Left_button_id_ref').text)
    @left.setter
    def left(self, value:int):
        self.node.find('Left_button_id_ref').text = str(value)

    @property
    def right(self):
        return int(self.node.find('Right_button_id_ref').text)
    @right.setter
    def right(self, value:int):
        self.node.find('Right_button_id_ref').text = str(value)

    @property
    def x(self):
        return int(self.node.find('Button_horisontal_position').text)
    @x.setter
    def x(self, value:int):
        self.node.find('Button_horisontal_position').text = str(value)

    @property
    def y(self):
        return int(self.node.find('Button_vertical_position').text)
    @y.setter
    def y(self, value:int):
        self.node.find('Button_vertical_position').text = str(value)

    @property
    def n(self):
        return int(self.node.find('Normal_start_object_id_ref').text)
    @n.setter
    def n(self, value:Optional[int]):
        if not value:
            value = 65535
        self.node.find('Normal_start_object_id_ref').text = str(value)
        self.node.find('Normal_end_object_id_ref').text = str(value)

    @property
    def s(self):
        return int(self.node.find('Selected_start_object_id_ref').text)
    @s.setter
    def s(self, value:Optional[int]):
        if not value:
            value = 65535
        self.node.find('Selected_start_object_id_ref').text = str(value)
        self.node.find('Selected_end_object_id_ref').text = str(value)

    @property
    def a(self):
        return int(self.node.find('Activated_start_object_id_ref').text)
    @a.setter
    def a(self, value:Optional[int]):
        if not value:
            value = 65535
        self.node.find('Activated_start_object_id_ref').text = str(value)
        self.node.find('Activated_end_object_id_ref').text = str(value)

    def getObjectID(self, state:str):
        '''state: N/n, S/s, A/a'''
        if state.lower() == 'n':
            return self.n
        elif state.lower() == 's':
            return self.s
        elif state.lower() == 'a':
            return self.a

    @property
    def isHidden(self):
        return self.n == 65535 and self.s == 65535 and self.a == 65535

# class Object:

#     def __init__(self, node:ET.Element):
#         self.node = node
#         self.id = node.attrib['id']

#     def getObject(self):
#         buffer = []
#         bufferA = []
#         obj = self.node.text
#         bytes_ = base64.b64decode(obj) + b'\0'
#         with open('test2.bin', 'wb') as _:
#             _.write(bytes_)
#         width, height = struct.unpack('>HH', bytes_[3:7])
#         print(width, height)
#         for i in range(7, len(bytes_), 6):
#             b = bytes_[i:i+6]
#             repeat = struct.unpack('>H', b[1:3])[0]
#             print(repeat >> 12, repeat & 0xFFF)
#             repeat = repeat & 0xFFF
#             sleep(0.5)

#             Y = struct.unpack('B', b[0:1])[0]
#             Cb, Cr, A = struct.unpack('BBB', b[3:])
#             buffer +=  [Y, Cb, Cr] * repeat
#             bufferA += [A] * repeat
#         arr = np.array(buffer, dtype=np.uint8).reshape((width, height, 3))
#         arrA = np.array(bufferA, dtype=np.uint8).reshape((width, height))
#         im = Image.fromarray(arr, mode='YCbCr').convert('RGB')
#         a = Image.fromarray(arrA, mode='L')
#         im.putalpha(a)
#         im.show()

# if __name__ == '__main__':
#     dliesTree = ET.parse('project_new.dlies')
#     dliesRoot = dliesTree.getroot()
#     x = Object(dliesRoot.find('DisplaySets/IesDisplaySet/Objects')[-1])
#     x.getObject()
#     # im = Image.new('RGBA', size=(100, 100), color=(16,32,64,128))
#     # im.save('my.png')