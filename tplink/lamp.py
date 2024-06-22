from __future__ import annotations
import asyncio
from kasa import Discover, Credentials, SmartBulb
from kasa.exceptions import AuthenticationException
import time
import colorsys


class LampException(Exception):
    pass


class Lamp():

    class Colors:
        RED: str = "#ff0000"
        GREEN: str = "#00ff00"
        BLUE: str = "#0000ff"
        YELLOW: str = "#ffff00"
        WHITE: str = "#ffffff"
        ORANGE: str = "#ffa500"
        PURPLE: str = "#800080"
        DARK_PURPLE: str = "#6300ff"
        PINK: str = "#ffc0cb"
        BROWN: str = "#a52a2a"
        CYAN: str = "#00ffff"
        MAGENTA: str = "#ff00ff"
        LIME: str = "#00ff00"
        INDIGO: str = "#4b0082"
        VIOLET: str = "#ee82ee"
        GOLD: str = "#ffd700"
        MAROON: str = "#800000"
        OLIVE: str = "#808000"
        NAVY: str = "#000080"
        TEAL: str = "#008080"
        AQUA: str = "#00ffff"


    def __init__(self, username: str, password: str, label: str | None = None, model: str | None = None):
        self.lamp: None | SmartBulb = None
        self.__loop = asyncio.get_event_loop()
        self._lamps: list[SmartBulb] = []
        self._last_hsv_color: tuple = tuple()
        self._search_lamps(label, model, username, password)
    

    @property
    def username(self) -> str:
        self.update()
        return self.lamp.credentials.username # type: ignore
    

    @property
    def brightness(self) -> int:
        self.update()
        return self.lamp.brightness # type: ignore
    

    @property
    def hsv(self) -> tuple[int, int, int]:
        self.update()
        return self.lamp.hsv.hue, self.lamp.hsv.saturation, self.lamp.hsv.value * 100 # type: ignore
    

    @property
    def rgb(self) -> tuple[int, int, int]:
        self.update()
        return self.__hsv_to_rgb(*self.hsv) # type: ignore
    

    @property
    def is_on(self) -> bool:
        self.update()
        return self.lamp.is_on # type: ignore
    

    @property
    def is_off(self) -> tuple[int, int, int]:
        self.update()
        return self.lamp.is_off # type: ignore


    def sleep(self, seconds: float) -> Lamp:
        time.sleep(seconds)
        return self
    

    def all_lamps(self) -> list[SmartBulb]:
        for l in self._lamps:
            self.__loop.run_until_complete(l.update())
        return self._lamps


    def alternate_turn_on_off(self, times: int, sleep_ms: int = 100) -> Lamp:
        if not self.lamp:
            return self
        for i in range(times):
            if self.is_on:
                self.turn_off()
            else:
                self.turn_on()
            self.sleep(sleep_ms/1000)
        return self
    
    
    def blink(self, times: int, sleep_ms: int = 0, step: int = 15, min: int = 1, max: int = 100, end_with_start: bool = True) -> Lamp:
        if not self.lamp:
            return self
        for _ in range(times):
            self.set_brightness(min, sleep_ms, step)
            self.set_brightness(max, sleep_ms, step)
            if end_with_start:
                self.set_brightness(min, sleep_ms, step)
        return self


    def set_last_color(self, transition_ms: int | None = None) -> Lamp:
        return self.__set_color(*[int(n) for n in self._last_hsv_color], transition_ms=transition_ms)


    def set_color_rgbhex(self, hex_color: str, transition_ms: int | None = None) -> Lamp:
        hsv: tuple[float, float, float] = self.__hex_to_hsv(hex_color)
        return self.__set_color(*[int(n) for n in hsv], transition_ms=transition_ms)


    def set_color_rgb(self, r: float, g: float, b: float, transition_ms: int | None = None) -> Lamp:
        hsv: tuple[float, float, float] = self.__rgb_to_hsv(r, g, b)
        return self.__set_color(*[int(n) for n in hsv], transition_ms=transition_ms)


    def set_color_hsv(self, h: int, s: int, v: int, transition_ms: int | None = None) -> Lamp:
        return self.__set_color(h, s, v, transition_ms=transition_ms)


    def update(self) -> Lamp:
        if not self.lamp:
            return self
        self.__loop.run_until_complete(self.lamp.update())
        return self


    def turn_on(self) -> Lamp:
        if not self.lamp:
            return self
        self.__loop.run_until_complete(self.lamp.turn_on())
        return self

    
    def turn_off(self) -> Lamp:
        if not self.lamp:
            return self
        self.__loop.run_until_complete(self.lamp.turn_off())
        return self

    
    def set_brightness(self, percentage: int = 100, sleep_ms: int | None = None, step: int = 1) -> Lamp:
        if not self.lamp:
            return self
        
        percentage = int(percentage)
        if percentage < 1:
            percentage = 1
        if percentage > 100:
            percentage = 100

        self.update()
        brightness = self.lamp.brightness
        diff = brightness - percentage
        
        if sleep_ms is None or diff == 0:
            self.__loop.run_until_complete(self.lamp.set_brightness(percentage))
            return self
        
        for t in range(0, abs(diff), step):
            if diff < 0:
                brightness += step
            else:
                brightness -= step

            try:
                self.__loop.run_until_complete(self.lamp.set_brightness(brightness))
            except:
                continue
            self.sleep(sleep_ms/1000)

        self.__loop.run_until_complete(self.lamp.set_brightness(percentage))
        return self
    

    def _search_lamps(self, label: str | None, model: str | None, username: str, password: str):
        attempts: int = 0
        while True:
            found_devices = self.__loop.run_until_complete(
                Discover.discover(
                    credentials=Credentials(
                        username=username,
                        password=password
                    )
                )
            )
            
            if found_devices or attempts >= 3:
                break
            attempts += 1

        devices = list()
        for d in found_devices.values():
            self.__loop.run_until_complete(d.update())
            if not d.is_bulb:
                continue
            if model and model.lower() != d.model.lower():
                continue
            if label and d.alias and label.lower() != d.alias.lower():
                continue
            devices.append(d)

        if not devices:
            raise LampException("No lamps found for these parameters")

        self._lamps = devices
        if devices:
            self.lamp = devices[0]
            self._last_hsv_color = self.lamp.hsv.hue, self.lamp.hsv.saturation, self.lamp.hsv.value # type: ignore

    
    def __set_color(self, h: int, s: int, v: int | None = None, transition_ms: int | None = None) -> Lamp:
        if not self.lamp:
            return self
        self.update()
        self._last_hsv_color = self.lamp.hsv.hue, self.lamp.hsv.saturation, self.lamp.hsv.value # type: ignore
        self.__loop.run_until_complete(self.lamp.set_hsv(h, s, v, transition=transition_ms))
        self.update()
        return self
    

    def __hex_to_rgb(self, hex_color: str):
        hex_color = hex_color.lstrip('#')
        rgb = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
        return rgb


    def __rgb_to_hsv(self, r: float, g: float, b: float):
        r, g, b = r / 255.0, g / 255.0, b / 255.0
        h, s, v = colorsys.rgb_to_hsv(r, g, b)
        return (h * 360, s * 100, v * 100)


    def __hex_to_hsv(self, hex_color: str):
        rgb = self.__hex_to_rgb(hex_color)
        hsv = self.__rgb_to_hsv(*rgb)
        return hsv
    

    def __hsv_to_rgb(self, h: float, s: float, v: float):
        h, s, v = h / 360.0, s / 100.0, v / 100.0
        r, g, b = colorsys.hsv_to_rgb(h, s, v)
        return (int(r * 255), int(g * 255), int(b * 255))
