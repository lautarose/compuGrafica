import gi
gi.require_version('Gtk', '3.0')
gi.require_version('Gdk', '3.0')
gi.require_version('GooCanvas', '2.0')
from gi.repository import GLib, Gtk, GooCanvas
from math import pi, cos, sin, radians
from time import localtime
from datetime import datetime

CTR_X = 500 # Coordenada X del centro del reloj
CTR_Y = 500 # Coordenada Y del centro del reloj
RADIUS = 130 # Radio del reloj
SEC_COLOR = 0xCC2F30FF # Color de la manecilla de los segundos
MIN_COLOR = 0xFFFFFFFF # Color de la manecilla de los minutos
HR_COLOR = 0xffa000ff # Color de la manecilla de la hora
BG_COLOR = 0x298ecbcc # Color de fondo del reloj
CONTOUR_RADIUS = 145  # Radio del círculo de contorno
STRAP_COLOR = 0X36403fff # Color de las correas
STRAP_RADIUS = 15 # Radio de las esquinas de las correas

class MainWindow(Gtk.Window):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.connect("destroy", lambda x: Gtk.main_quit())
        self.set_default_size(1000, 1000)

        canvas = GooCanvas.Canvas()
        cvroot = canvas.get_root_item()

        # Correas
        self.correas(cvroot)

        # Botón lateral
        self.lateralbtn = GooCanvas.CanvasRect(
            parent = cvroot,                 # El mismo root que el reloj
            x = CTR_X + RADIUS + 15,         # A la derecha del reloj
            y = CTR_Y - 20,                  # Centrada verticalmente con respecto al reloj
            width = 20,                      # Ancho del rectángulo (horizontal)
            height = 40,                     # Altura del rectángulo (vertical)
            radius_x = 5,                    # Radio de las esquinas en X
            radius_y = 5,                    # Radio de las esquinas en Y
            line_width = 2,                  # Ancho del borde
            stroke_color = 'Black',          # Color del borde
            fill_color = 'Black'             # Color de relleno (negro para que se vea como en la imagen)
        )

        # Marco del reloj
        GooCanvas.CanvasEllipse(
            parent = cvroot,
            center_x = CTR_X,
            center_y = CTR_Y,
            radius_x = CONTOUR_RADIUS + 10,
            radius_y = CONTOUR_RADIUS + 10,
            line_width = 3,  # Grosor del borde
            stroke_color = 'black',
            fill_color_rgba = 0x555757ff, 
        )

        # Fondo
        self.fondo_reloj(cvroot)
        
        # Hora Digital
        self.digital_hora(cvroot)

        # Logo
        self.trademark = GooCanvas.CanvasText(
            parent = cvroot,
            x = CTR_X - 24 ,                      # Posicionamos el texto centrado en el eje X del rectángulo
            y = CTR_Y + 45,                 # Ajustamos la altura para centrar el texto en el rectángulo
            text = 'SNB',            # Hora actual en formato HH:MM
            font = "Sans 18",               # Tipo y tamaño de letra
            fill_color_rgba = 0xB1B1B1FF         # Color del texto (negro para buen contraste con el fondo blanco)
        )

        # Marcas de la hora
        self.hour_marks(cvroot)

        # Manecillas del reloj
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
                    fill_color_rgba = SEC_COLOR,
                    stroke_color_rgba = SEC_COLOR)
        
        # Vidrio del reloj
        GooCanvas.CanvasEllipse(
            parent = cvroot,
            center_x = CTR_X,
            center_y = CTR_Y,
            radius_x = CONTOUR_RADIUS - 5,
            radius_y = CONTOUR_RADIUS - 5,
            stroke_color_rgba= 0xe4fffa05,
            fill_color_rgba= 0xe4fffa05,
        )

        GLib.timeout_add(250, self.on_timer)
        self.add(canvas)
        self.show_all()

    def correas(self, layer):
        # Correa superior del reloj
        self.CorreaSup = GooCanvas.CanvasRect(
            parent=layer,
            x=CTR_X - 75,  # Más ancho (grosor)
            y=CTR_Y - 270,  # Más largo
            width=150,  # Grosor de la correa
            height=150,  # Longitud de la correa
            stroke_color=STRAP_COLOR,
            radius_x=STRAP_RADIUS,
            radius_y=STRAP_RADIUS,
            fill_color_rgba=STRAP_COLOR
        )

        # Correa inferior del reloj
        self.CorreaInf = GooCanvas.CanvasRect(
            parent=layer,
            x=CTR_X - 75,  
            y=CTR_Y + 100 ,
            width=150,
            height=170,  
            stroke_color=STRAP_COLOR,
            radius_x=STRAP_RADIUS,
            radius_y=STRAP_RADIUS,
            fill_color_rgba=STRAP_COLOR
        )

    def fondo_reloj(self, layer):
        # Borde exterior
        GooCanvas.CanvasEllipse(
            parent = layer,
            center_x = CTR_X,
            center_y = CTR_Y,
            radius_x = CONTOUR_RADIUS,
            radius_y = CONTOUR_RADIUS,
            line_width = 5,  # Grosor del borde
            stroke_color_rgba = 0x205968ff,  
            fill_color_rgba= 0x212624ff, 
        )

        # Interior del reloj
        GooCanvas.CanvasEllipse(
            parent = layer,
            center_x = CTR_X,
            center_y = CTR_Y,
            radius_x = CONTOUR_RADIUS,
            radius_y = CONTOUR_RADIUS,
            stroke_color_rgba= 0xdffdf800,
            fill_color_rgba= 0xdffdf822,
        )

    def digital_hora(self, layer):
        # Rectángulo para mostrar la hora
        self.digital_clock = GooCanvas.CanvasRect(
            parent = layer,
            x = CTR_X - 40,                 # Posición a la derecha del centro, pero a la izquierda de las 3 en punto
            y = CTR_Y - 70,                 # Centrado verticalmente respecto al centro del reloj
            width = 80,                     # Ancho del rectángulo (suficiente para mostrar la hora)
            height = 40,                    # Altura del rectángulo
            line_width = 2,                 # Ancho del borde del rectángulo
            radius_x=5,                     # Radio de las esquinas en X
            radius_y=5,                     # Radio de las esquinas en Y
            stroke_color_rgba = 0xBF744FFF, # Color del borde del rectángulo
            fill_color_rgba = 0x205968ff    # Color de fondo del rectángulo
        )

        # Hora actual
        current_time = datetime.now().strftime('%H:%M')

        # Texto de Hora actual en formato HH:MM
        self.digital_time_text = GooCanvas.CanvasText(
            parent = layer,
            x = CTR_X - 35 ,                # Posicionamos el texto centrado en el eje X del rectángulo
            y = CTR_Y - 62,                 # Ajustamos la altura para centrar el texto en el rectángulo
            text = current_time,            # Hora actual en formato HH:MM
            font = "Sans 18",               # Tipo y tamaño de letra
            fill_color = 'White'            # Color del texto
        )

    def hour_marks(self, layer):
        for h in range(60):
            if (h % 5) == 0:
                GooCanvas.CanvasRect(
                        parent = layer,
                        x = CTR_X + RADIUS - 25,    width = 30,
                        y = CTR_Y - 2,              height = 4,
                        line_width = 0.5,
                        stroke_color = 'black',
                        fill_color_rgba = 0xBF744FFF ).rotate(6*h, CTR_X, CTR_Y)


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
