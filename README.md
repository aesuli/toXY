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

I assume you already have Inkscape installed. This extension is compatible with Inkscape for version 1.3 and higher. For Inkscape 1.2 refer to [this version of the code](https://github.com/aesuli/toXY/tree/inkscape_v1.2)

### Installation from Inkscape

This is the preferred way to install the extension.

Download the latest release from GitHub as a zip file.

Open Inkscape, select "Extensions" on the menu bar, and the "Manage Extensions".
Select the "Install Packages" tab, and then the button with the image of a folder.
Select the zip file you downloaded, and click "Open".
Close the "Extensions" window and restart Inkscape to conclude the installation.

### Manual installation

Close Inkscape if it is running.
Copy the two files (`toXY.inx` and `toXY.py`) into the extensions directory of Inkscape, which is usually located:
 * on Windows: `%userprofile%\AppData\Roaming\inkscape\extensions` or `C:\Program Files\Inkscape\share\extensions`
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

![](https://github.com/aesuli/toXY/blob/main/images/PDFConvert1.png?raw=true)

Now the page is a group of objects in the drawing, select it, and repeatedly ungroup it (Ctrl+Shift+G), until you get the message _No groups to ungroup in the selection_ (see the lower part of the second image down here).

![](https://github.com/aesuli/toXY/blob/main/images/PDFConvert2.png?raw=true)
![](https://github.com/aesuli/toXY/blob/main/images/PDFConvert3.png?raw=true)

Zoom (if needed) and select the curves you want to convert into numbers.

![](https://github.com/aesuli/toXY/blob/main/images/PDFConvert4.png?raw=true)

Run the toXY plugin from the Extensions, Generate from Path menus.

![](https://github.com/aesuli/toXY/blob/main/images/PDFConvert5.png?raw=true)

Set the proper values for the lower left corner and upper right corner to match the bounds of the curves you want to convert into numbers.
Click Apply.

![](https://github.com/aesuli/toXY/blob/main/images/PDFConvert6.png?raw=true)

A very long text box will appear below the graph. Each line reports the X and Y coordinates of a point (adjusted to the lower and upper corner coordinates you entered) and to which curve it belongs. Copy and paste it wherever you like.

If you set a filename in the plugin window, you can have the same output directly saved to a text file. 

![](https://github.com/aesuli/toXY/blob/main/images/PDFConvert7.png?raw=true)


![](https://github.com/aesuli/toXY/blob/main/images/PDFConvert7-2.png?raw=true)

For example, I copied the data into a spreadsheet and, after a minor clean up, I have got back an exact replica of the graph.

![](https://github.com/aesuli/toXY/blob/main/images/PDFConvert8.png?raw=true)

## License

See the [license file](COPYING).
