#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  reloj.py
#
#  Copyright 2024 john <jcoppens@vostro.ampr.net>
#

import gi
gi.require_version('Gtk', '3.0')
gi.require_version('Gdk', '3.0')
gi.require_version('GooCanvas', '2.0')
from gi.repository import GLib, Gtk, GooCanvas
from math import pi, cos, sin, radians
from time import localtime

CTR_X = 300
CTR_Y = 300
RADIUS = 250
SEC_COLOR = 0xffa000ff
MIN_COLOR = 0xffa000ff
HR_COLOR = 0xffa000ff
BG_COLOR = 0x298ecbcc
CONTOUR_RADIUS = 270  # Radio del círculo de contorno

class MainWindow(Gtk.Window):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.connect("destroy", lambda x: Gtk.main_quit())
        self.set_default_size(600, 600)

        canvas = GooCanvas.Canvas()
        cvroot = canvas.get_root_item()

        # Agregar el círculo de contorno
        GooCanvas.CanvasEllipse(
            parent = cvroot,
            center_x = CTR_X,
            center_y = CTR_Y,
            radius_x = CONTOUR_RADIUS,
            radius_y = CONTOUR_RADIUS,
            line_width = 3,  # Grosor del borde
            stroke_color = 'Black',  # Color del borde
            fill_color_rgba= BG_COLOR # Relleno con gradiente
        )

        self.fixed_decorations(cvroot)

        self.hrs = GooCanvas.CanvasPolyline(
                    parent = cvroot,
                    line_width = 12,
                    stroke_color_rgba = HR_COLOR)

        self.mins = GooCanvas.CanvasPolyline(
                    parent = cvroot,
                    line_width = 7,
                    stroke_color_rgba = MIN_COLOR)

        self.mins_ctr = GooCanvas.CanvasEllipse(
                    parent = cvroot,
                    center_x = CTR_X, center_y = CTR_Y,
                    radius_x = 7, radius_y = 7,
                    line_width = 3,
                    stroke_color_rgba = MIN_COLOR)

        self.secs = GooCanvas.CanvasPolyline(
                    parent = cvroot,
                    line_width = 2,
                    stroke_color_rgba = SEC_COLOR)

        self.secs_ctr = GooCanvas.CanvasEllipse(
                    parent = cvroot,
                    center_x = CTR_X, center_y = CTR_Y,
                    radius_x = 4, radius_y = 4,
                    line_width = 2,
                    stroke_color_rgba = SEC_COLOR)

        GLib.timeout_add(250, self.on_timer)
        self.add(canvas)
        self.show_all()


    def fixed_decorations(self, layer):
        for h in range(60):
            if (h % 15) == 0:
                GooCanvas.CanvasRect(
                        parent = layer,
                        x = CTR_X + RADIUS - 40,    width = 40,
                        y = CTR_Y - 10,             height = 20,
                        line_width = 2,
                        stroke_color = 'Black',
                        fill_color = 'Yellow').rotate(90*h, CTR_X, CTR_Y)

            elif (h % 5) == 0:
                GooCanvas.CanvasRect(
                        parent = layer,
                        x = CTR_X + RADIUS - 20,    width = 20,
                        y = CTR_Y - 4,              height = 8,
                        line_width = 1.5,
                        stroke_color = 'Black',
                        fill_color = 'Yellow').rotate(6*h, CTR_X, CTR_Y)

            else:
                GooCanvas.CanvasEllipse(
                        parent = layer,
                        x = CTR_X + RADIUS - 25,    width = 8,
                        y = CTR_Y - 4,              height = 8,
                        line_width = 1,
                        stroke_color = 'Black',
                        fill_color = 'Yellow').rotate(6*h, CTR_X, CTR_Y)


    def on_timer(self):
        s = localtime()[5]
        m = localtime()[4]
        h = localtime()[3]

        sangle = radians(-90 + 6*s)
        mangle = radians(-90 + 6*m + 0.1*s)
        hangle = radians(-90 + 30*h)

        points = GooCanvas.CanvasPoints.new(2)
        points.set_point(0, CTR_X, CTR_Y)
        points.set_point(1, CTR_X + RADIUS*1.05 * cos(sangle),
                            CTR_Y + RADIUS*1.05 * sin(sangle))
        self.secs.set_property('points', points)

        points = GooCanvas.CanvasPoints.new(2)
        points.set_point(0, CTR_X, CTR_Y)
        points.set_point(1, CTR_X + RADIUS*0.8 * cos(mangle),
                            CTR_Y + RADIUS*0.8 * sin(mangle))
        self.mins.set_property('points', points)

        points = GooCanvas.CanvasPoints.new(2)
        points.set_point(0, CTR_X, CTR_Y)
        points.set_point(1, CTR_X + RADIUS*0.55 * cos(hangle),
                            CTR_Y + RADIUS*0.55 * sin(hangle))
        self.hrs.set_property('points', points)

        return True

    def run(self):
        Gtk.main()


def main(args):
    mainwdw = MainWindow()
    mainwdw.run()

    return 0

if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))
