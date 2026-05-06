import machine


class Joystick:

    def __init__(
        self,
        pinx: machine.ADC,
        piny: machine.ADC,
        invert_x: bool = False,
        invert_y: bool = False,
        deadzone: float = 5.0,
        # Backwards-compatible aliases for the old camelCase parameter names
        invertX: bool = None,
        invertY: bool = None,
    ):
        self.x_pin    = pinx
        self.y_pin    = piny
        self.invert_x = invert_x if invertX is None else invertX
        self.invert_y = invert_y if invertY is None else invertY
        self.deadzone = deadzone

        # Record resting position as the centre reference point (0.0 – 100.0)
        self.x_centre = (pinx.read_u16() / 65535) * 100.0
        self.y_centre = (piny.read_u16() / 65535) * 100.0

    # ------------------------------------------------------------------ #

    def _read_axis(self, pin: machine.ADC, centre: float, invert: bool) -> float:
        raw = (pin.read_u16() / 65535) * 100.0

        # Rescale each half of the range independently so the full
        # physical travel always maps to 0 – 100, regardless of where
        # the stick happens to rest.
        #
        # Lower half: [0, centre]   → [0,  50]
        # Upper half: [centre, 100] → [50, 100]
        if raw < centre:
            scaled = (raw / centre) * 50.0 if centre > 0 else 0.0
        else:
            remaining = 100.0 - centre
            scaled = 50.0 + ((raw - centre) / remaining) * 50.0 if remaining > 0 else 100.0

        # Clamp just in case of ADC noise at the extremes
        scaled = max(0.0, min(100.0, scaled))

        # Snap to neutral inside the deadzone
        if abs(scaled - 50.0) < self.deadzone:
            scaled = 50.0

        value = (100.0 - scaled) if invert else scaled
        return round(value, 2)

    # ------------------------------------------------------------------ #

    def get_x(self) -> float:
        return self._read_axis(self.x_pin, self.x_centre, self.invert_x)

    def get_y(self) -> float:
        return self._read_axis(self.y_pin, self.y_centre, self.invert_y)

    def get_pos(self) -> list:
        """Returns [x_pct, y_pct] — always in the range 0.0 – 100.0."""
        return [self.get_x(), self.get_y()]
