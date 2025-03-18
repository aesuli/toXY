#!/usr/bin/env python
"""Inkscape extension that extracts XY coordinates of points defining selected paths."""

import pathlib
from lxml import etree
import inkex
from inkex.transforms import Transform
from inkex.paths import Path


class ToXYEffect(inkex.EffectExtension):

    def add_arguments(self, pars):
        pars.add_argument(
            "--xmin",
            type=float,
            dest="xmin",
            default=0.0,
            help="x min (lower left corner)",
        )
        pars.add_argument(
            "--ymin",
            type=float,
            dest="ymin",
            default=0.0,
            help="y min (lower left corner)",
        )
        pars.add_argument(
            "--xmax",
            type=float,
            dest="xmax",
            default=1.0,
            help="x max (upper right corner)",
        )
        pars.add_argument(
            "--ymax",
            type=float,
            dest="ymax",
            default=1.0,
            help="y max (upper right corner)",
        )
        pars.add_argument(
            "--fontsize",
            type=float,
            dest="fontSize",
            default=8,
            help="Font size",
        )
        pars.add_argument(
            "--write_output_file",
            type=inkex.Boolean,
            dest="write_output_file",
            default=False,
            help="Write to output file",
        )
        pars.add_argument(
            "--output_file",
            type=pathlib.Path,
            dest="output_file",
            default=None,
            help="Optional output file",
        )

    def draw_rect(self, x, y, w, h, parent):
        """Draw a rectangle"""
        style = {
            "stroke": "#000000",
            "stroke-opacity": "1",
            "width": "1",
            "fill": "none",
        }
        attribs = {
            "style": str(inkex.Style(style)),
            "height": str(h),
            "width": str(w),
            "x": str(x),
            "y": str(y),
        }
        etree.SubElement(parent, inkex.addNS("rect", "svg"), attribs)

    def write_text(self, x, y, text, parent):
        """Write some text, breaking lines on \'\\n\'"""
        style = {
            "font-size": self.options.fontSize,
            "font-style": "normal",
            "font-weight": "normal",
            "fill": "#000000",
            "fill-opacity": "1",
            "stroke": "none",
            "font-family": "Sans",
        }
        attribs = {"style": str(inkex.Style(style)), "x": str(x), "y": str(y)}
        text_node = etree.SubElement(parent, inkex.addNS("text", "svg"), attribs)
        for line in text.split("\n"):
            tspan = etree.Element(inkex.addNS("tspan", "svg"))
            tspan.set(inkex.addNS("role", "sodipodi"), "line")
            tspan.text = line
            text_node.append(tspan)

    def extract_path(self, node, points, transform=None):
        """Recursively extract paths."""
        pathString = node.get("d")
        if pathString:
            id = node.get("id")
            path = inkex.paths.CubicSuperPath(node.get("d"))
            transf = Transform(transform) @ Transform(node.get("transform", None))
            path = Path(path).transform(transf).to_superpath()
            # reflection on y axys to have y growing toward up direction of the graph
            points[id] = [point[1] for segment in path for point in segment]
            points[id] = [(x, -y) for (x, y) in points[id]]
        elif node.tag == inkex.addNS("g", "svg"):
            transf = Transform(transform) @ Transform(node.get("transform", None))
            for child in node.iterchildren():
                self.extract_path(child, points, transf)
        else:
            inkex.utils.debug(node.tag)

    def effect(self):
        """toXY effect."""
        if len(self.svg.selected) < 1:
            inkex.utils.debug("This extension requires that you select at least one path.")
            return

        xrange = self.options.xmax - self.options.xmin
        yrange = self.options.ymax - self.options.ymin
        if xrange <= 0 or yrange <= 0:
            inkex.utils.debug("Negative ranges, check x-y min-max values.")
            return

        # gathering points from paths
        points = {}
        for id in self.options.ids:
            node = self.svg.selected[id]
            self.extract_path(node, points)

        if not points:
            inkex.utils.debug("No paths found.")
            return

        # remove duplicate points
        for path_id, coordinates in points.items():
            dedup_coordinates = []
            for coord in coordinates:
                if len(dedup_coordinates) == 0 or coord != dedup_coordinates[-1]:
                    dedup_coordinates.append(coord)
            points[path_id] = dedup_coordinates

        # boundaries
        xmin = min([point[0] for pointset in points.values() for point in pointset])
        ymin = min([point[1] for pointset in points.values() for point in pointset])

        xdelta = max([point[0] for pointset in points.values() for point in pointset]) - xmin
        ydelta = max([point[1] for pointset in points.values() for point in pointset]) - ymin

        # converting coordinates writing table
        table = "pathId idx x y\n"
        for id in list(points.keys()):
            points[id] = [
                (
                    (((x - xmin) / xdelta) * xrange) + self.options.xmin,
                    (((y - ymin) / ydelta) * yrange) + self.options.ymin,
                )
                for (x, y) in points[id]
            ]
            table += "\n".join([f"{id} {idx} {x:4g} {y:4g}" for idx, (x, y) in enumerate(points[id])])
            table += "\n"

        # output
        group = etree.SubElement(self.svg.get_current_layer(), inkex.addNS("g", "svg"))
        self.draw_rect(xmin, -ymin - ydelta, xdelta, ydelta, group)
        self.write_text(
            xmin,
            -ymin + self.options.fontSize,
            "{0:4g},{1:4g}".format(self.options.xmin, self.options.ymin),
            group,
        )
        self.write_text(
            xmin + xdelta,
            -ymin - ydelta,
            "{0:4g},{1:4g}".format(self.options.xmax, self.options.ymax),
            group,
        )
        self.write_text(xmin, -ymin + self.options.fontSize * 2.5, table, group)

        # optionally write to external output file
        if self.options.write_output_file:
            try:
                with open(self.options.output_file, "w") as f:
                    f.write(table)
            except OSError as e:
                inkex.utils.debug(e)


if __name__ == "__main__":
    e = ToXYEffect()
    e.run()
