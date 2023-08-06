"""

# trmnl_colors v-4.0.5
## Add colors to the static WOrLd!


colors module is made to colorize the output of terminal when the code runs on command line, With that there are functions for adding basic text colors (Total 10 including invsisble) and or text formats such as Bold, Italics, Underline, Light or Strikethrough to your code.

But wait there is more! use background colors, filled Variants which can be accessed by calling thier specific name and 'bg' postfix as in background. Here is an example describing with  use case:
```python
from trmnl_colors import *
bluebg()
print("Hello")
reset()
```

* Each color can be accessed by calling thier particular name and the first letter of the format at the postfix.
```python
from trmnl_colors import *
yellowB()
print("Hello") # After every color call remember to call the reset function.
# Outputs Hello in yellow color in Bold text
reset()
```
* For example:Call clr.redB() for red color with text format Bold, S for strikethrough D for Default U for Underline I for Italics L is for special lighter color substitute for each color.


* There are also filled color variants in which the font color and the background color match each other making them viable for specific type of color operations. 

* There is a special function called reset() which is basically the default white so that the color function gets reset it is recommended to use this function after every usage of a color to mantain the color of the terminal.
* 
* PS if you want to create blocks of colors for decoration purposes use filled variants e.g. clr.whitefilled() 

Explore & stay Creative
### by: Idris-Vohra :O

"""
def blackD(): # Default
    print("\033[0;30m",end="")

def blackB(): # Bold
    print("\033[1;30m",end="")

def blackL(): # Light
    print("\033[2;30m",end="")

def blackI(): # Italics
    print("\033[3;30m",end="")

def blackU(): # Underline
    print("\033[4;30m",end="")

def blackS(): # Strikethrough
    print("\033[9;30m",end="")

# Red:-
def redD(): # Default 
    print("\033[0;31m",end="")

def redB(): # Bold
    print("\033[1;31m",end="")

def redL(): # Light
    print("\033[2;31m",end="")

def redI(): # Italics
    print("\033[3;31m",end="")

def redU(): # Underline
    print("\033[4;31m",end="")

def redS(): # Strikethrough
    print("\033[9;31m",end="")


# Green:-
def greenD():
    print("\033[0;32m",end="")

def greenB():
    print("\033[1;32m",end="")

def greenL():
    print("\033[2;32m",end="")

def greenI():
    print("\033[3;32m",end="")

def greenU():
    print("\033[4;32m",end="")

def greenS():
    print("\033[9;32m",end="")


# Yellow:-
def yellowD():
    print("\033[0;33m",end="")

def yellowB():
    print("\033[1;33m",end="")

def yellowL():
    print("\033[2;33m",end="")

def yellowI():
    print("\033[3;33m",end="")

def yellowU():
    print("\033[4;33m",end="")

def yellowS():
    print("\033[9;33m",end="")


# Blue:-
def blueD():
    print("\033[0;34m",end="")

def blueB():
    print("\033[1;34m",end="")

def blueL():
    print("\033[2;34m",end="")

def blueI():
    print("\033[3;34m",end="")

def blueU():
    print("\033[4;34m",end="")

def blueS():
    print("\033[9;34m",end="")


# Magenta:-
def magentaD():
    print("\033[0;35m",end="")

def magentaB():
    print("\033[1;35m",end="")

def magentaL():
    print("\033[2;35m",end="")

def magentaI():
    print("\033[3;35m",end="")

def magentaU():
    print("\033[4;35m",end="")

def magentaS():
    print("\033[9;35m",end="")


# Cyan:-
def cyanD():
    print("\033[0;36m",end="")

def cyanB():
    print("\033[1;36m",end="")

def cyanL():
    print("\033[2;36m",end="")

def cyanI():
    print("\033[3;36m",end="")

def cyanU():
    print("\033[4;36m",end="")

def cyanS():
    print("\033[9;36m",end="")

# Grey:-
def greyD():
    print("\033[0;90m",end="")

def greyB():
    print("\033[1;90m",end="")

def greyL():
    print("\033[2;90m",end="")

def greyI():
    print("\033[3;90m",end="")

def greyU():
    print("\033[4;90m",end="")

def greyS():
    print("\033[9;90m",end="")

# White:
def reset():
    print("\033[0;0m",end='');

def whiteB():
    print("\033[0;1m",end="")

def whiteL():
    print("\033[0;2m",end="")

def whiteI():
    print("\033[0;3m",end="")

def whiteU():
    print("\033[0;4m",end="")

def whiteS():
    print("\033[0;8m",end="")


# fill variants:
def redfill():
    print("\033[31;41m",end='')

def yellowfill():
    print("\033[33;43m",end='')

def greenfill():
    print("\033[32;42m",end='')

def bluefill():
    print("\033[34;44m",end='')

def magentafill():
    print("\033[35;45m",end='')

def cyanfill():
    print("\033[36;46m",end='')

def whitefill():
    print("\033[37;47m",end='')

def blackfill():
    print("\033[30;40m",end='')

def greyfill():
    print("\033[90;100m",end='')

# Background:
def blackbg():
    print("\033[7;30m",end="")

def redbg():
    print("\033[7;31m",end="")
    
def greenbg():
    print("\033[7;32",end="")

def yellowbg():
    print("\033[7;33m",end="")

def bluebg():
    print("\033[7;34m",end="")

def magentabg():
    print("\033[7;35m",end="")

def cyanbg():
    print("\033[7;36m",end="")

def whitebg():
    print("\033[7;37m",end="")

def greybg():
    print("\033[7;90m",end="")

# Invisible:
def invisible():
    print("\033[0;8m",end="")
    
    