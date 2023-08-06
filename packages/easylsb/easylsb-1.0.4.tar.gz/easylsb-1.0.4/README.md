<p><span><span style="font-family:Verdana, Arial, Helvetica, sans-serif;line-height:19px;text-indent:26px;"><span style="font-size:14px;"><span style="font-family:Arial;line-height:26px;"><br></span></span></span></span></p>

### This is a simple Python package for steganography
Code to hide information in the given image:
```python
import lsb
from PIL import Image
import numpy as np
img=Image.open('test.png')
img=np.array(img)
info=b'Some information'
hidden=lsb.lsbenc(img,info)
img_hidden=Image.fromarray(hidden)
img_hidden.save('hidden.png')# Must be a PNG,BMP,etc., not JPEG or WEBP
```

Code to get the hidden information from the given image:
```python
import lsb
from PIL import Image
import numpy as np
img=Image.open('test.png')# Must be a PNG,BMP,etc., not JPEG or WEBP
img=np.array(img)
info=lsb.lsbdec(img)
print(info)
```
It's very easy to use the StegSolve tool to get the hidden information, but easylsb package allows you to encrypt the information using DES. 