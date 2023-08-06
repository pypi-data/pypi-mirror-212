🍀**ionicons_python**
================

🎯**Description**
------------------
This package containing the icons taken from `ionicons` website for using those easily in Python. You will not only get the basic icons from this package, but also get the social icons too, for example Linkedin, GitHub, Twitter, etc.

🎯**Usage**
------------
Using this package is just a piece of cake🍰. Just install this package using the below command.
```bash
pip install ionicons_python
```
After the installation is complete, use it with any of your favourite framework like **Flet, Streamlit** etc. Here I am giving an example of using **Flet**.

```python
from ionicons_python.ionicons_icons import *
import flet as ft

def main(page: ft.Page):
   page.add(ft.Image(linkedin_icon, width=24, height=24))

ft.app(target=main)
```
Don't use this icons with `Iconbutton` or  `Icon` of **Flet**.  Those only take flet inbuilt icons.

if you want to see all the icons available, visit [this](https://ionic.io/ionicons) website.