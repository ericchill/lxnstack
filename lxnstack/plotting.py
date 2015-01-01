# lxnstack is a program to align and stack atronomical images
# Copyright (C) 2013-2015  Maurizio D'Addona <mauritiusdadd@gmail.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from PyQt4 import Qt, QtCore, QtGui

import numpy as np

import translation as tr
import utils

# NOTE: The naming scheme for markers an lines is compatible
#        with matplotlib because of a possible future impementation

MARKER_TYPES = [
    ('',tr.tr('None')),
    ('.',tr.tr('point')),
    (',',tr.tr('pixel')),
    ('o',tr.tr('circle')),
    ('s',tr.tr('square')),
    ('+',tr.tr('plus')),
    ('*',tr.tr('star')),
    ('v',tr.tr('triangle down')),
    ('^',tr.tr('triangle up')),
    ('<',tr.tr('triangle left')),
    ('>',tr.tr('triangle right')),
    ('h',tr.tr('hexagon1')),
    ('H',tr.tr('hexagon2')),
    ('p',tr.tr('pentagon')),
    ('1',tr.tr('tri down')),
    ('2',tr.tr('tri up')),
    ('3',tr.tr('tri left')),
    ('4',tr.tr('tri right')),
    ('x',tr.tr('x')),
    ('d',tr.tr('thin diamond')),
    ('D',tr.tr('diamond')),
    ('_',tr.tr('horizontal line')),
    ('|',tr.tr('vertical line'))]

LINE_TYPES = [
    ('',tr.tr('None')),
    ('-',tr.tr('solid')),
    ('--',tr.tr('dash')),
    (':',tr.tr('dot')),
    ('-.',tr.tr('dash dot')),
    ('-..',tr.tr('dash dot dot'))]

BAR_TYPES = [('',tr.tr('None')),
             ('|',tr.tr('Vertical only')),
             ('_',tr.tr('Horizontal only')),
             ('+',tr.tr('Both'))]

COLORS = [
    ('cyan', tr.tr('cyan')),
    ('magenta', tr.tr('magenta')),
    ('green', tr.tr('green')),
    ('gray', tr.tr('gray')),
    ('red', tr.tr('red')),
    ('blue', tr.tr('blue')),
    ('yellow', tr.tr('yellow')),
    ('darkcyan', tr.tr('dark cyan')),
    ('darkmagenta', tr.tr('dark magenta')),
    ('darkgreen', tr.tr('dark green')),
    ('black', tr.tr('black')),
    ('darkred', tr.tr('dark red')),
    ('darkblue', tr.tr('dark blue')),
    ('darkyellow', tr.tr('dark yellow'))]


def getDarkerColor(color):
    color_idx = getColorIndex(color)
    dark_idx = color_idx + len(COLORS)/2
    return getColor(dark_idx)

def getMarkerType(index):
    return MARKER_TYPES[index % len(MARKER_TYPES)][0]


def getLineType(index):
    return LINE_TYPES[index % len(LINE_TYPES)][0]

def getBarType(index):
    return BAR_TYPES[index % len(BAR_TYPES)][0]

def getColor(index):
    return COLORS[index % len(COLORS)][0]

def getLineTypeIndex(marker):
    for i in LINE_TYPES:
        if i[0] == marker:
            return LINE_TYPES.index(i)
    raise ValueError('cannot find line type '+str(marker))


def getMarkerTypeIndex(marker):
    for i in MARKER_TYPES:
        if i[0] == marker:
            return MARKER_TYPES.index(i)
    raise ValueError('cannot find marker type '+str(marker))

def getBarTypeIndex(bar):
    for i in BAR_TYPES:
        if i[0] == bar:
            return BAR_TYPES.index(i)
    raise ValueError('cannot find line type '+str(bar))

def getColorIndex(color):
    for i in COLORS:
        if i[0] == color:
            return COLORS.index(i)
    raise ValueError('cannot find color '+str(color))

def getQtColor(color):
    if color == "red":
        color=QtCore.Qt.red
    elif color == "green":
        color=QtCore.Qt.green
    elif color == "blue":
        color=QtCore.Qt.blue
    elif color == "yellow":
        color=QtCore.Qt.yellow
    elif color == "cyan":
        color=QtCore.Qt.cyan
    elif color == "magenta":
        color=QtCore.Qt.magenta
    elif color == "darkred":
        color=QtCore.Qt.darkRed
    elif color == "gray":
        color=QtCore.Qt.gray
    elif color == "darkyellow":
        color=QtCore.Qt.darkYellow
    elif color == "darkgreen":
        color=QtCore.Qt.darkGreen
    elif color == "darkcyan":
        color=QtCore.Qt.darkCyan
    elif color == "darkblue":
        color=QtCore.Qt.darkBlue
    elif color == "darkmagenta":
        color=QtCore.Qt.darkMagenta
    elif color == "black":
        color=QtCore.Qt.black
    else:
        color=QtCore.Qt.black
    return color


def getQtLine(line_type):
    if line_type == '-':
        linetype = QtCore.Qt.SolidLine
    elif line_type == '--':
        linetype = QtCore.Qt.DashLine
    elif line_type == ':':
        linetype = QtCore.Qt.DotLine
    elif line_type == '-.':
        linetype = QtCore.Qt.DashDotLine
    elif line_type == '-..':
        linetype = QtCore.Qt.DashDotDotLine
    return linetype
            

def drawRegularPolygon(painter, x, y, sides, size, rot=0):
    points = []
    angles = np.linspace(0, 2*np.pi, sides, False)
    r0 = np.deg2rad(rot)
    for a in angles:
        an = a + r0
        px = x + size*np.cos(an)
        py = y + size*np.sin(an)
        points.append(QtCore.QPointF(px, py))
    painter.drawPolygon(*points)

def drawFlake(painter, x, y, sides, size, rot=0):
    lines = []
    angles = np.linspace(0, 2*np.pi, sides, False)
    r0 = np.deg2rad(rot)
    for a in angles:
        an = a + r0
        px = x + size*np.cos(an)
        py = y + size*np.sin(an)
        lines.append(QtCore.QLineF(x, y, px, py))
    painter.drawLines(*lines)

def drawStar(painter, x, y, sides, size1, size2, rot=0):
    points = []
    angles = np.linspace(0, 2*np.pi, sides, False)
    a0 = angles[1]/2.0
    r0 = np.deg2rad(rot)
    for a in angles:
        a1 = a + r0
        a2 = a + a0 + r0
        px1 = x + size1*np.cos(a1)
        py1 = y + size1*np.sin(a1)
        px2 = x + size2*np.cos(a2)
        py2 = y + size2*np.sin(a2)

        p1 = QtCore.QPointF(px1, py1)
        p2 = QtCore.QPointF(px2, py2)

        points.append(p1)
        points.append(p2)

    painter.drawPolygon(*points)


def drawFinder(painter, x, y, r=7, l=4):
    painter.drawEllipse(Qt.QPointF(x,y),r,r)
    painter.drawLine(Qt.QPointF(x-r-l,y),Qt.QPointF(x-r+l,y))
    painter.drawLine(Qt.QPointF(x+r-l,y),Qt.QPointF(x+r+l,y))
    painter.drawLine(Qt.QPointF(x,y-l-r),Qt.QPointF(x,y-r+l))
    painter.drawLine(Qt.QPointF(x,y+r+l),Qt.QPointF(x,y+r-l))


def drawCross(painter, x, y, size, rot=0, prop=0.5):
    a1 = np.deg2rad(rot-90*prop)
    a2 = np.deg2rad(rot+90*prop)

    x11 = x + size*np.cos(a1)
    y11 = y + size*np.sin(a1)
    x12 = x - size*np.cos(a1)
    y12 = y - size*np.sin(a1)
    line1 = QtCore.QLineF(x11, y11, x12, y12)
    
    x21 = x + size*np.cos(a2)
    y21 = y + size*np.sin(a2)
    x22 = x - size*np.cos(a2)
    y22 = y - size*np.sin(a2)
    line2 = QtCore.QLineF(x21, y21, x22, y22)

    painter.drawLines(line1, line2)


def drawMarker(painter, x, y, size, marker_type=""):
    
    if not marker_type:
        return
    
    half = size/2.0
    x1 = x - half
    y1 = y - half
    x2 = x + half
    y2 = y + half
    
    if marker_type == '.':
        painter.drawEllipse(QtCore.QPointF(x, y), 1, 1)

    elif marker_type == ',':
        painter.drawPoint(QtCore.QPointF(x, y))

    elif  marker_type == 'o':
        painter.drawEllipse(QtCore.QPointF(x, y), half, half)

    elif  marker_type == 's':
        painter.drawRect(QtCore.QRectF(x1, y1, size, size))

    elif  marker_type == '+':
        drawCross(painter, x, y, half, 45)

    elif  marker_type == '*':
        drawStar(painter, x, y, 5, half, half/2.0, -90)

    elif  marker_type == 'v':
        drawRegularPolygon(painter, x, y, 3, half, 90)

    elif  marker_type == '^':
        drawRegularPolygon(painter, x, y, 3, half, 270)

    elif  marker_type == '<':
        drawRegularPolygon(painter, x, y, 3, half, 180)

    elif  marker_type == '>':
        drawRegularPolygon(painter, x, y, 3, half, 0)

    elif  marker_type == 'h':
        drawRegularPolygon(painter, x, y, 6, half, 0)

    elif  marker_type == 'H':
        drawRegularPolygon(painter, x, y, 6, half, 90)
    
    elif  marker_type == 'p':
        drawRegularPolygon(painter, x, y, 5, half, -90)
    
    elif  marker_type == '1':
        drawFlake(painter, x, y, 3, half, 90)

    elif  marker_type == '2':
        drawFlake(painter, x, y, 3, half, 270)

    elif  marker_type == '3':
        drawFlake(painter, x, y, 3, half, 180)

    elif  marker_type == '4':
        drawFlake(painter, x, y, 3, half, 0)

    elif  marker_type == 'x':
        drawCross(painter, x, y, half, 0)

    elif  marker_type == 'd':
        drawRegularPolygon(painter, x, y, 4, half)

    elif  marker_type == 'D':
        drawRegularPolygon(painter, x, y, 4, half)

    elif  marker_type == '_':
        painter.drawLine(QtCore.QLineF(x1, y, x2, y))
        
    elif  marker_type == '|':
        painter.drawLine(QtCore.QLineF(x, y1, x, y2))
        
    else:
        pass

def drawErroBar(painter, x, y, xh, xl, yh, yl, bar_type):
    
    if bar_type == '|':
        painter.drawLine(Qt.QPointF(x, y+yh), Qt.QPointF(x, y-yl))
    elif bar_type == '_':
        painter.drawLine(Qt.QPointF(x+xh, y), Qt.QPointF(x-xl, y))
    elif bar_type == '+':
        painter.drawLine(Qt.QPointF(x, y+yh), Qt.QPointF(x, y-yl))
        painter.drawLine(Qt.QPointF(x+xh, y), Qt.QPointF(x-xl, y))
    else:
        pass


class Plot(object):

    def __init__(self):
        self.xdata = []
        self.ydata = []
        self.xerr = []
        self.yerr = []
        self.name = ""
        self.color = "cyan"
        self.marker_type='s'
        self.line_type='-'
        self.bar_type="|"
        self.int_param=4
        self.marker_size=6
        self.line_width=1.25
        self._shown=True
        self._inverted_y=False

    def hide(self):
        self._shown=False

    def show(self):
        self._shown=True

    def isHidden(self):
        return not self._shown
    
    def isVisible(self):
        return self._shown

    def setVisible(self, val):
        if val:
            self.show()
        else:
            self.hide()

    def setInvertedY(self, inverted=True):
        self._inverted_y=inverted

    def setIterpolationOrder(self, val):
        self.int_param = val

    def getIterpolationOrder(self):
        return self.int_param

    def getMarkerType(self):
        return self.marker_type

    def getColor(self):
        return self.color

    def getLineType(self):
        return self.line_type

    def getBarType(self):
        return self.bar_type

    def getLineWidth(self):
        return self.line_width

    def getMarkerSize(self):
        return self.marker_size

    def setName(self, name):
        self.name=str(name)

    def getName(self):
        return self.name

    def getYMinMax(self):
        if self.ydata:
            return min(self.ydata), max(self.ydata)
        else:
            return (0, 1)
    
    def getXMinMax(self):
        if self.xdata:
            return min(self.xdata), max(self.xdata)
        else:
            return (0, 1)

    def setColor(self, color):
        self.color=color

    def setColorIndex(self, index):
        self.color=getColor(index)

    def setLineTypeIndex(self, index):
        self.line_type=getLineType(index)

    def setBarTypeIndex(self, index):
        self.bar_type=getBarType(index)

    def setMarkerTypeIndex(self, index):
        self.marker_type=getMarkerType(index)

    def setMarkerSize(self, val):
        self.marker_size=val

    def setLineWidth(self, val):
        self.line_width=val

    def drawQtLegendElement(self, painter, x, y):
        maincolor = getQtColor(self.color)
        border_color = getQtColor(getDarkerColor(self.color))
        txth = painter.fontMetrics().xHeight()
        if self.line_type:            
            linetype = getQtLine(self.line_type)
            painter.setPen(Qt.QPen(maincolor, self.line_width, linetype))
            painter.drawLine(QtCore.QLineF(x, y, x + 25, y))

        painter.setPen(Qt.QPen(border_color, self.marker_size/10))
        painter.setBrush(maincolor)
        if self.marker_type:
            drawMarker(painter, x+13, y, self.marker_size, self.marker_type)
        painter.setPen(getQtColor("black"))
        painter.drawText(x+30, y+txth/2, self.getName())

    def drawQt(self, painter, hrange, vrange=(0, 1), offset=(60, 60)):
        if self.isHidden():
            return

        surface_window = painter.window()
        w = surface_window.width()
        h = surface_window.height()

        data_x = self.xdata
        data_y = self.ydata
        xerr = self.xerr
        yerr = self.yerr

        pcount = len(data_y)

        ax_ext = getAxisExtents(data_x, hrange)

        minx = ax_ext[0]
        maxx = ax_ext[1]
        miny = ax_ext[2]
        maxy = ax_ext[3]

        if self._inverted_y:
            x1 = offset[0]
            y1 = offset[1]
            x_scale = (w - 2*offset[0]) / (maxx-minx)
            y_scale = (h - 2*offset[1]) / (maxy-miny)
        else:
            x1 = offset[0]
            y1 = h - offset[1]
            x_scale = (w - 2*offset[0]) / (maxx-minx)
            y_scale = -(h - 2*offset[1]) / (maxy-miny)

        maincolor = getQtColor(self.color)
        border_color = getQtColor(getDarkerColor(self.color))

        if self.line_type:            
            linetype = getQtLine(self.line_type)
            painter.setPen(Qt.QPen(maincolor, self.line_width, linetype))
            points = []
            # Now signal will be interpolated and all
            # high frequency noise will be removed
            for p in utils.interpolate(data_x, data_y, 10, 4, self.int_param):
                x = (p[0]-minx)*x_scale + x1
                y = (p[1]-miny)*y_scale + y1
                points.append(Qt.QPointF(x, y))
                # drawMarker(painter,x,y,r1,r2,False,True) # debug purpose only
            if points:
                painter.drawPolyline(*points)

        painter.setPen(Qt.QPen(border_color, self.marker_size/10))
        painter.setBrush(maincolor)
        
        for i in range(pcount):
            x = (data_x[i]-minx)*x_scale + x1
            y = (data_y[i]-miny)*y_scale + y1
            if self.marker_type:
                drawMarker(painter, x, y, self.marker_size, self.marker_type)
            if self.bar_type:
                yr = yerr[i]
                xr = xerr[i]

                try:
                    if isinstance(yr, (tuple, list, np.ndarray)) and len(yr)>1:
                        yh = yr[0]*y_scale
                        yl = yr[1]*y_scale
                    else:
                        yh = yr*y_scale
                        yl = yh
                except:
                    yh = 0
                    yl = 0

                try:
                    if isinstance(xr, (tuple, list, np.ndarray)) and len(xr)>1:
                        xh = xr[0]*x_scale
                        xl = xr[1]*x_scale
                    else:
                        xh = xr*x_scale
                        xl = xh
                except:
                    xh = 0
                    xl = 0

                drawErroBar(painter, x, y,  xh, xl, yh, yl, self.bar_type)

    def savePlot(self, widget, title, name, y_inverted=False):
        plot = Qt.QImage(1600, 1200, Qt.QImage.Format_ARGB32)
        fname = str(Qt.QFileDialog.getSaveFileName(
            None,
            tr.tr("Save the chart"),
            os.path.join(self.current_dir, title+'.jpg'),
            "JPEG (*.jpg *.jpeg);;" +
            "PNG (*.png);;PPM (*.ppm);;" +
            "TIFF (*.tiff *.tif);;" +
            "All files (*.*)",
            None,
            utils.DIALOG_OPTIONS))
        #self.simplifiedLightCurvePaintEvent(widget, chart, name, y_inverted)
        plot.save(fname, quality=100)


def getAxisExtents(data_x=(0, 1), data_y=(0, 1)):
    if not data_x or not data_y:
        return (0, 1, 0, 1)

    miny = data_y[0]
    maxy = data_y[-1]
    minx = utils.floor5(data_x[0], 2)
    maxx = utils.ceil5(data_x[-1], 2)
    
    delta_x = maxx - minx
    delta_y = maxy - miny
    
    x_padding = delta_x * 0.05
    y_padding = delta_y * 0.05
    
    minx -= x_padding
    maxx += x_padding
    miny -= y_padding
    maxy += y_padding
    
    return minx, maxx, miny, maxy


def getChartDivision(vmin, vmax, n=10):
    if n == 0:
        return []
    step = (vmax-vmin)/float(n)
    arr = np.arange(vmin, vmax, step)
    return arr


def drawAxis(painter, data_x=(0, 1), data_y=(0, 1),
             x_offset=60.0, y_offset=60.0, axis_name=('x', 'y'),
             inverted_y=False, x_str_func=str, y_str_func=utils.getSciStr):

    surface_window = painter.window()

    w = surface_window.width()
    h = surface_window.height()
    
    gm1 = 1.00
    gm2 = 2.00
    gm3 = 8.00
    
    ax_ext = getAxisExtents(data_x, data_y)
    
    minx = ax_ext[0]
    maxx = ax_ext[1]
    miny = ax_ext[2]
    maxy = ax_ext[3]

    text_height = painter.fontMetrics().height()

    if inverted_y:
        x1 = x_offset
        y1 = y_offset
        x2 = w - x_offset
        y2 = h - y_offset
        y3 = gm3
        x_scale = (w - 2*x_offset) / (maxx-minx)
        y_scale = (h - 2*y_offset) / (maxy-miny)
        txt_y_corr = -4
    else:
        x1 = x_offset
        y1 = h - y_offset
        x2 = w - x_offset
        y2 = y_offset
        y3 = -gm3
        x_scale = (w - 2*x_offset) / (maxx-minx)
        y_scale = -(h - 2*y_offset) / (maxy-miny)
        txt_y_corr = text_height

    pxy1 = Qt.QPointF(x1, y1)
    px2 = Qt.QPointF(x2, y1)
    py2 = Qt.QPointF(x1, y2)

    # draw x-axis
    painter.setPen(Qt.QPen(QtCore.Qt.black, 1, QtCore.Qt.SolidLine))
    painter.drawLine(pxy1, py2)
    painter.drawText(Qt.QPointF(x2, y1-y3), utils.brakets(axis_name[0]))
    count = 1
    
    p0 = Qt.QPointF(x1, y1 + txt_y_corr)
    
    for x in getChartDivision(minx,
                              maxx,
                              utils.floor5(w/50.0, 0)):
        if x < minx:
            continue
        elif x > maxx:
            break
        count ^= 1
        stxt = x_str_func(x)
        stxt_y_off = gm1 + gm2*count
        stxt_x_off = painter.fontMetrics().width(stxt)/2
        painter.setPen(Qt.QPen(QtCore.Qt.black, 1, QtCore.Qt.SolidLine))

        p1 = Qt.QPointF((x-minx)*x_scale + x1, y1)
        p2 = Qt.QPointF((x-minx)*x_scale + x1, y1 - stxt_y_off*y3)
        p3 = Qt.QPointF((x-minx)*x_scale + x1 - stxt_x_off,
                        y1 - stxt_y_off*y3 + txt_y_corr)
        p4 = Qt.QPointF((x-minx)*x_scale + x1, y2)

        painter.drawLine(p1, p2)
        painter.drawText(p3, stxt)
        painter.setPen(Qt.QPen(QtCore.Qt.gray, 1, QtCore.Qt.DotLine))
        painter.drawLine(p1, p4)

    # draw y-axis
    painter.setPen(Qt.QPen(QtCore.Qt.black, 1, QtCore.Qt.SolidLine))
    painter.drawLine(pxy1, px2)
    painter.drawText(Qt.QPointF(10, y2-y3-20), utils.brakets(axis_name[1]))
    for y in getChartDivision(utils.sciFloor5(miny, 1),
                              utils.sciCeil5(maxy, 1),
                              utils.floor5(h/50, 0)):
        if y <= miny:
            continue
        elif y > maxy:
            break
        painter.setPen(Qt.QPen(QtCore.Qt.black, 1, QtCore.Qt.SolidLine))
        p1 = Qt.QPointF(2*x1/3, (y-miny)*y_scale + y1)
        p2 = Qt.QPointF(x1, (y-miny)*y_scale + y1)
        p3 = Qt.QPointF(5, (y-miny)*y_scale + y1)
        p4 = Qt.QPointF(x2, (y-miny)*y_scale + y1)
        painter.drawLine(p1, p2)
        painter.drawText(p3, y_str_func(y))
        painter.setPen(Qt.QPen(QtCore.Qt.gray, 1, QtCore.Qt.DotLine))
        painter.drawLine(p2, p4)
