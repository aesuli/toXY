#!/usr/bin/env python

import sys
print(sys.path)

import inkex
import cubicsuperpath
import simpletransform
import simplestyle


""" Inkscape extension that extracts XY coordinates of points defining selected paths. """
class ToXYEffect(inkex.Effect):

    """ Constructor. """
    def __init__(self):
        # Call base class construtor.
        inkex.Effect.__init__(self)
        self.OptionParser.add_option("--xmin",
            action="store", type="float", 
                dest="xmin", default=0.0,
            help="x min (lower left corner)")
        self.OptionParser.add_option("--ymin",
            action="store", type="float", 
                dest="ymin", default=0.0,
            help="y min (lower left corner)")
        self.OptionParser.add_option("--xmax",
            action="store", type="float", 
                dest="xmax", default=1.0,
            help="x max (upper right corner)")
        self.OptionParser.add_option("--ymax",
            action="store", type="float", 
                dest="ymax", default=1.0,
            help="y max (upper right corner)")
        self.OptionParser.add_option("--fontsize",
            action="store", type="float", 
                dest="fontSize", default=10.0,
            help="Font size")

    """ Draw a rectangle """
    def draw_rect(self, x, y, w, h, parent):
            style = {   
            'stroke'        : '#000000',
            'stroke-opacity' : '1',
                'width'         : '1',
                'fill'          : 'none'
           }
            attribs = {
                'style'     : simplestyle.formatStyle(style),
                'height'    : str(h),
                'width'     : str(w),
                'x'         : str(x),
                'y'         : str(y)
           }
            inkex.etree.SubElement(parent, inkex.addNS('rect','svg'), attribs )

    """ Write some text, breaking lines on \'\\n\' """
    def write_text(self, x, y, text, parent):
        style = {   
        'font-size'    : self.options.fontSize,
        'font-style'    : 'normal',
        'font-weight'    : 'normal',
        'fill'    : '#000000',
        'fill-opacity' : '1',
        'stroke' : 'none',
            'font-family':'Sans'
        }
        attribs = {
            'style'     : simplestyle.formatStyle(style),
            'x'         : str(x),
            'y'         : str(y)
        }
        textNode = inkex.etree.SubElement(parent, inkex.addNS('text','svg'), attribs )
        for line in text.split('\n'):
                  tspan = inkex.etree.Element(inkex.addNS("tspan", "svg"))
                  tspan.set(inkex.addNS("role","sodipodi"), "line")
                  tspan.text = line
                  textNode.append(tspan)

    """ Recursively extract paths. """
    def extractPath(self,node,points,transformMatrix=None):
        pathString = node.get('d')
        if pathString:
            id = node.get('id')
            path = cubicsuperpath.parsePath(node.get('d'))
            if transformMatrix:
                simpletransform.applyTransformToPath(transformMatrix,path)
            # reflection on y axys to have y growing toward up direction of the graph
            points[id] = [point[1] for segment in path for point in segment]
            points[id] = [(x,-y) for (x,y) in points[id]]
        elif node.tag==inkex.addNS('g','svg'):
            innerTransform = node.get('transform')
            innerTransformMatrix = simpletransform.parseTransform(innerTransform)
            if innerTransformMatrix:
                if(transformMatrix):
                    transformMatrix = simpletransform.composeTransform(transformMatrix,innerTransformMatrix)
                else:
                    transformMatrix = innerTransformMatrix
            for child in node.iterchildren():
                self.extractPath(child,points,transformMatrix)
        else:
            inkex.debug(node.tag)

    """ toXY effect. """
    def effect(self):
        if len(self.selected)<1:
            inkex.debug("This extension requires that you select at least one path.")
            return

        xrange = self.options.xmax-self.options.xmin
        yrange = self.options.ymax-self.options.ymin
        if xrange<=0 or yrange<=0:
            inkex.debug("Negative ranges, check x-y min-max values.")
            return

        #gathering points from paths
        points = {}
        for id in self.options.ids:
            node = self.selected[id]
            self.extractPath(node,points)

        if not points:
            inkex.debug("No paths found.")
            return

        #boundaries
        xmin = min([point[0] for pointset in points.values() for point in pointset])
        ymin = min([point[1] for pointset in points.values() for point in pointset])

        xdelta = max([point[0] for pointset in points.values() for point in pointset])-xmin
        ydelta = max([point[1] for pointset in points.values() for point in pointset])-ymin
        
        #converting coordinates writing table
        table = "pathId x y\n"
        for id in points.keys():
            points[id] = [((((x-xmin)/xdelta)*xrange)+self.options.xmin,(((y-ymin)/ydelta)*yrange)+self.options.ymin) for (x,y) in points[id]]
            table += "\n".join(['{0} {1:4g} {2:4g}'.format(id,x,y) for (x,y) in points[id]])
            table += "\n"

        #output
        group = inkex.etree.SubElement(self.current_layer, inkex.addNS('g','svg'))
        self.draw_rect(xmin, -ymin-ydelta, xdelta, ydelta,group)
        self.write_text(xmin,-ymin+self.options.fontSize,"{0:4g},{1:4g}".format(self.options.xmin,self.options.ymin),group)
        self.write_text(xmin+xdelta, -ymin-ydelta,"{0:4g},{1:4g}".format(self.options.xmax,self.options.ymax),group)
        self.write_text(xmin, -ymin+self.options.fontSize*2.5, table,group)

e = ToXYEffect()
e.affect()
