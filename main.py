## mostly ai generated, tweaked & looked over by eric
## main.py file for ESP32's. 


import machine
import sys
import json
import select
from joystick import Joystick
from sh1106 import SH1106_I2C

# ─────────────────────────────────────────────
#  Hardware Configuration  –  update to match your wiring -- google "ESP32 wroom datasheet" to see which pins work for what. 
# ─────────────────────────────────────────────

PIN_JOY_X   = 34
PIN_JOY_Y   = 35
PIN_SHOOT   = 17

PIN_SDA     = 21
PIN_SCL     = 22
I2C_ADDR    = 0x3c
OLED_WIDTH  = 128
OLED_HEIGHT = 64

# How far from centre (%) the stick must move to register a direction
JOY_THRESHOLD = 25

# Which player this controller is (1 or 2) — determines which state to read
PLAYER_ID = 1

# ─────────────────────────────────────────────
#  Peripheral Initialisation
# ─────────────────────────────────────────────

joy = Joystick(
    pinx    = machine.ADC(machine.Pin(PIN_JOY_X)),
    piny    = machine.ADC(machine.Pin(PIN_JOY_Y)),
    invert_x = False,
    invert_y = False,
)

shoot = machine.Pin(PIN_SHOOT, machine.Pin.IN)

i2c  = machine.I2C(0, scl=machine.Pin(PIN_SCL), sda=machine.Pin(PIN_SDA), freq=400_000)
oled = SH1106_I2C(OLED_WIDTH, OLED_HEIGHT, i2c, addr=I2C_ADDR)
oled.sleep(False)

# ─────────────────────────────────────────────
#  Helper Functions
# ─────────────────────────────────────────────

def get_command() -> str:
    """
    Reads joystick + shoot button and returns one command character.
    Priority: shoot > horizontal > vertical
    """
    if shoot.value() == 1:
        return 'S'

    x = joy.get_x()
    y = joy.get_y()

    if x < (50 - JOY_THRESHOLD):
        return 'L'
    if x > (50 + JOY_THRESHOLD):
        return 'R'
    if y < (50 - JOY_THRESHOLD):
        return 'U'
    if y > (50 + JOY_THRESHOLD):
        return 'D'

    return 'N'


def draw_hp_bar(x: int, y: int, width: int, hp: int, max_hp: int):
    """Draws a segmented HP bar at the given position."""
    oled.rect(x, y, width, 6, 1)
    if max_hp > 0 and hp > 0:
        fill_w = int((hp / max_hp) * (width - 2))
        oled.fill_rect(x + 1, y + 1, fill_w, 4, 1)


def bullet_warning(state: dict) -> bool:
    """
    Returns True if any enemy bullet is within 3 tiles of our player.
    Used to flash a warning on the OLED.
    """
    me = state.get("p1" if PLAYER_ID == 1 else "p2", {})
    mx, my = me.get("x", -99), me.get("y", -99)
    for b in state.get("bullets", []):
        if b.get("owner") != PLAYER_ID:
            if abs(b["x"] - mx) + abs(b["y"] - my) <= 3:
                return True
    return False


def render_oled(state: dict, last_cmd: str):
    """
    Draws the full game state onto the OLED.

    Layout (128×64):
    ┌─────────────────────────────┐
    │ TICK 042/200                │  row 0
    │ P1 [========  ] hp  facing  │  row 10
    │ P2 [=====     ] hp  facing  │  row 20
    │ ─────────────────────────── │  row 30
    │ CMD: R    Bullets: 2        │  row 34
    │ Status line / warning       │  row 44
    │ Joy crosshair (bottom right)│  rows 44-63
    └─────────────────────────────┘
    """
    oled.fill(0)

    status   = state.get("status",  "---")
    tick     = state.get("tick",    0)
    p1       = state.get("p1",      {})
    p2       = state.get("p2",      {})
    bullets  = state.get("bullets", [])

    me  = p1 if PLAYER_ID == 1 else p2
    foe = p2 if PLAYER_ID == 1 else p1

    me_label  = "P{}".format(PLAYER_ID)
    foe_label = "P{}".format(2 if PLAYER_ID == 1 else 1)

    # ── Row 0: tick counter ───────────────────────────────────────────────
    oled.text("TICK {}/{}".format(tick, state.get("max_tick", "?")), 0, 0)

    # ── Row 10: our HP bar ────────────────────────────────────────────────
    oled.text(me_label, 0, 10)
    draw_hp_bar(20, 11, 70, me.get("hp", 0), me.get("max_hp", 3))
    oled.text("{}{}".format(
        me.get("hp",     "?"),
        " " + me.get("facing", "?")
    ), 94, 10)

    # ── Row 20: enemy HP bar ──────────────────────────────────────────────
    oled.text(foe_label, 0, 20)
    draw_hp_bar(20, 21, 70, foe.get("hp", 0), foe.get("max_hp", 3))
    oled.text("{}{}".format(
        foe.get("hp",     "?"),
        " " + foe.get("facing", "?")
    ), 94, 20)

    # ── Divider ───────────────────────────────────────────────────────────
    oled.hline(0, 30, OLED_WIDTH, 1)

    # ── Row 34: last command + bullet count ───────────────────────────────
    oled.text("CMD:{} BUL:{}".format(last_cmd, len(bullets)), 0, 34)

    # ── Row 44: status / warning ──────────────────────────────────────────
    if status != "playing":
        status_map = {
            "p1_win": "P1 WINS!",
            "p2_win": "P2 WINS!",
            "draw":   "DRAW!",
        }
        oled.text(status_map.get(status, status.upper()), 0, 44)

    elif not me.get("alive", True):
        oled.text("YOU ARE DEAD", 0, 44)

    elif bullet_warning(state):
        oled.text("!! INCOMING !!", 0, 44)

    else:
        # Show enemy position relative to ours
        ex = foe.get("x", 0) - me.get("x", 0)
        ey = foe.get("y", 0) - me.get("y", 0)
        oled.text("FOE dx:{} dy:{}".format(ex, ey), 0, 44)

    # ── Joystick crosshair (bottom-right 19×19 box) ───────────────────────
    bx, by, bs = 108, 44, 19
    oled.rect(bx, by, bs, bs, 1)
    dot_x = bx + 1 + int((joy.get_x() / 100) * (bs - 3))
    dot_y = by + 1 + int((joy.get_y() / 100) * (bs - 3))
    oled.fill_rect(dot_x, dot_y, 3, 3, 1)

    oled.show()


# ─────────────────────────────────────────────
#  Main Loop
# ─────────────────────────────────────────────

print("Controller Ready. Waiting for JSON state...")

oled.fill(0)
oled.text("P{} CONTROLLER".format(PLAYER_ID), 4, 20)
oled.text("Waiting...", 24, 34)
oled.show()

last_cmd   = 'N'
last_state = {}

while True:
    # ── 1. Read incoming JSON state (non-blocking) ─────────────────────────
    if select.select([sys.stdin], [], [], 0)[0]:
        line = sys.stdin.readline().strip()

        if not line:
            continue

        try:
            state = json.loads(line)

            # ── 2. Determine command ───────────────────────────────────────
            cmd = 'N'
            if state.get("status") == "playing":
                cmd = get_command()

            last_cmd   = cmd
            last_state = state

            # ── 3. Reply to host ───────────────────────────────────────────
            sys.stdout.write(cmd + '\n')

        except ValueError:
            pass

    # ── 4. OLED update ────────────────────────────────────────────────────
    if last_state:
        render_oled(last_state, last_cmd)
