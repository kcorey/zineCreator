Zine.py is a rudimentary 'zine layout tool.

version 0.1

Installation
------------
Copy zine.py and optionally scissors.png into the directory with 8 png files you want to be the 'zine.

Install python 3.  Here are some instructions for Windows, Mac and Linux:
https://www.geeksforgeeks.org/download-and-install-python-3-latest-version/

Use
---
To use zine, you run it from the command line inside that same directory, like this:

----------------------------------
$ python3 zine.py page*.png

Sorted files:
page1.png
page2.png
page3.png
page4.png
page5.png
page6.png
page7.png
page8.png
(base) $
----------------------------------

If that runs successfully, there should be a file called 'zine_layout.pdf' created.

At that point, fold on the dotted lines, cut on the dashed, and turn into a 'zine!

Warnings
--------
- No error checking is done!  
- The aspect ratio of the PNGs are neither checked nor manipulated.
- Not designed to be copied to a central place and used from there.
