draw_mandala = None  # Quick fix applied
e = None  # Quick fix applied
turtle = None  # Quick fix applied
random = None  # Quick fix applied
clear_and_redraw = None  # Quick fix applied
color_cycle = None  # Quick fix applied
quit_prog = None  # Quick fix applied
save_canvas = None  # Quick fix applied
math = None  # Quick fix applied
draw_layer = None  # Quick fix applied
datetime = None  # Quick fix applied
# mandala.py
# Animated mandala / spirograph-like pattern using turtle
# Save the window with 's' key, quit with 'q' key.

import turtle
import random
import math
from datetime import datetime

# ---------- Configuration ----------
WIDTH, HEIGHT = 900, 700
BG_COLOR = "#0b1020"
NUM_LAYERS = 28         # number of concentric loops
ITERATIONS = 360        # degrees per layer (higher => smoother)
BASE_RADIUS = 120       # base radius for patterns
ANGLE_STEP = 5          # angle step for drawing each layer
SCALE_FACTOR = 0.92     # how each successive layer scales
PENSIZE_START = 2.2
ROTATION_PER_LAYER = 7  # degrees rotation offset between layers
PALETTE = [
    "#FF6B6B", "#FFD93D", "#6BCB77", "#4D96FF",
    "#8F7AFE", "#FF7ACD", "#5EFCE8", "#FFE8D6"
]

# ---------- Setup screen ----------
screen = turtle.Screen()
screen.setup(WIDTH, HEIGHT)
screen.title("Mandala — Turtle Graphics")
screen.bgcolor(BG_COLOR)
screen.tracer(False)  # manual screen updates for smoother drawing

# ---------- Turtle ----------
pen = turtle.Turtle()
pen.hideturtle()
pen.speed(0)
pen.penup()
pen.goto(0, 0)
pen.pendown()
pen.setheading(0)

# ---------- Helpers ----------
def color_cycle(i):
    """Return a color from palette with interpolation for variety."""
    c1 = PALETTE[i % len(PALETTE)]
    # occasionally pick a slightly randomized brightness
    return c1

def draw_layer(radius, points, color, pen_size, offset_angle=0):
    """Draw one spiro-like circular layer made of arcs."""
    pen.pensize(pen_size)
    pen.color(color)
    pen.penup()
    # start at angle 0 with radius offset
    angle = offset_angle
    r = radius
    # move to first point
    x = r * math.cos(math.radians(angle))
    y = r * math.sin(math.radians(angle))
    pen.goto(x, y)
    pen.pendown()
    for a in range(0, 360, ANGLE_STEP):
        a2 = a + offset_angle
        # modulate radius slightly with a sine to get a petal effect
        mod = 0.15 * radius * math.sin(math.radians(a2 * (random.uniform(0.9, 1.1))))
        rr = r + mod
        x = rr * math.cos(math.radians(a2))
        y = rr * math.sin(math.radians(a2))
        pen.goto(x, y)
    pen.penup()

def draw_mandala():
    """Draw multiple layers with shrinking size and rotation."""
    screen.tracer(False)
    radius = BASE_RADIUS
    pen_size = PENSIZE_START
    for layer in range(NUM_LAYERS):
        # pick color and maybe slightly randomize it
        color = color_cycle(layer)
        offset = layer * ROTATION_PER_LAYER
        # Slight jitter to keep it lively
        jitter = random.uniform(-3.0, 3.0)
        draw_layer(radius * (1 + jitter/100.0), ITERATIONS, color, pen_size + layer*0.04, offset)
        radius *= SCALE_FACTOR
        pen_size *= 0.98
        # update screen per few layers for smooth animation
        if layer % 2 == 0:
            screen.update()
    screen.update()

# ---------- Interaction ----------
def save_canvas():
    """Save the canvas to a postscript file (can convert to PNG externally)."""
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"mandala_{ts}.eps"
    canvas = screen.getcanvas()
    try:
        canvas.postscript(file=filename)
        print(f"Saved drawing as {filename} (EPS). Convert to PNG with external tools.")
    except Exception as e:
        print("Save failed:", e)

def clear_and_redraw():
    pen.clear()
    pen.home()
    draw_mandala()

def quit_prog():
    turtle.bye()

# Key bindings
screen.listen()
screen.onkey(save_canvas, "s")
screen.onkey(clear_and_redraw, "r")
screen.onkey(quit_prog, "q")

# ---------- Run ----------
if __name__ == "__main__":
    # Intro quick shimmer animation: change palette random seed for variety
    random.seed()
    # Draw several passes with tiny palette shifts for nicer depth
    for pass_no in range(3):
        # slightly rotate global palette by permuting
        random.shuffle(PALETTE)
        draw_mandala()
        # small pause-like step: overlay a faint stroke for depth
        pen.color("#000000")
        pen.pensize(0.4)
        pen.goto(0, 0)
        screen.update()

    # Final update
    screen.tracer(True)
    screen.update()
    print("Done drawing. Press 's' to save .eps, 'r' to redraw, 'q' to quit.")
    turtle.done()