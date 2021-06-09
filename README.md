# toXY
## An Inkscape plugin to convert graphs in PDF files into numbers

It is rather common that a scientific paper presents most of its results in graphs, reporting in text just a few exact numeric values for some relevant cases.

The missing exact numerical information could prevent other researchers to fully compare their results with those of that paper.

When the paper is in PDF format (99.999% of the cases), and it is relatively recent, the exact numerical information is very likely included in the paper, because graphs are almost always included in <a href="http://en.wikipedia.org/wiki/Vector_graphics">vectorial</a> form.

toXY is an <a href="http://www.inkscape.org/">Inkscape</a> plugin that converts curves in a graph into a table of numbers.

Note that although the plugin works fine, I cannot keep the responsibility for you that the numbers will be always exact. 
Always check if the returned values are sound with respect to what is reported in the paper.
**Always check the values with the original authors before including them in any new publication.**

## Installation

I assume you already have Inkscape installed. This extension is compatible with Inkscape for version 1.0 and higher.

Close Inkscape.
Copy the two files (`toXY.inx` and `toXY.py`) into the extensions directory of Inkscape, which is usually located:
 * on Windows: `C:\Program Files\Inkscape\share\extensions`
 * on Linux: `/usr/share/inkscape/extensions`
 * on MacOS: `$HOME/.config/inkscape/extensions` or `/Applications/Inkscape.app/Contents/Resources/extensions`, depending on the OS version.

On Linux/MacOS you may also have to change the file permissions:
```
> chmod 755 toXY.py
> chmod 644 toXY.inx
```

## Usage

Start Inkscape.

Drag and drop the PDF file into Inkscape.

In the "PDF Import Settings" dialog select the page that contains the graph to be converted, click OK.

![](https://github.com/aesuli/toXY/blob/main/PdfConvert1.png?raw=true)

Now the page is a group of objects in the drawing, select it, and repeatedly ungroup it (Ctrl+Shift+G), until you get the message _No groups to ungroup in the selection_ (see the lower part of the second image down here).

![](https://github.com/aesuli/toXY/blob/main/PdfConvert2.png?raw=true)
![](https://github.com/aesuli/toXY/blob/main/PdfConvert3.png?raw=true)

Zoom (if needed) and select the curves you want to convert into numbers.

![](https://github.com/aesuli/toXY/blob/main/PdfConvert4.png?raw=true)

Run the toXY plugin from the Extensions, Generate from Path menus.

![](https://github.com/aesuli/toXY/blob/main/PdfConvert5.png?raw=true)

Set the proper values for the lower left corner and upper right corner to match the bounds of the curves you want to convert into numbers.
Click Apply.

![](https://github.com/aesuli/toXY/blob/main/PdfConvert6.png?raw=true)

A very long text box will appear below the graph. Each line reports the X and Y coordinates of a point (adjusted to the lower and upper corner coordinates you entered) and to which curve it belongs. Copy and paste it wherever you like.

![](https://github.com/aesuli/toXY/blob/main/PdfConvert7.png?raw=true)

For example, I copied the data into Excel and, after a minor clean up, I have got back an exact replica of the graph.

![](https://github.com/aesuli/toXY/blob/main/PdfConvert8.png?raw=true)

Optionally you can also output the contents of the box to a file which uses the same formatting as the text box. 

## License

Copyright 2021 Andrea Esuli <andrea@esuli.it>

Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.

2. Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.

3. Neither the name of the copyright holder nor the names of its contributors may be used to endorse or promote products derived from this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
