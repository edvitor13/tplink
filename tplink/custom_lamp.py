from .lamp import Lamp


class CustomLamp(Lamp):
    def error(self, sleep: int = 60) -> Lamp:
        return (
            self.set_color_rgbhex(self.Colors.RED)
                .turn_off()
                .alternate_turn_on_off(10)
                .turn_on()
                #.set_brightness(1, 0, 25)
                .blink(10, step=10)
                .sleep(sleep)
                .turn_off()
        )
    

    def success(self, sleep: int = 60) -> Lamp:
        return (
            self.set_color_rgbhex(self.Colors.GREEN)
                .turn_off()
                .turn_on()
                .blink(10, step=10)
                .sleep(sleep)
                .turn_off()
        )

    
    def warning(self, sleep: int = 60) -> Lamp:
        return (
            self.set_color_rgbhex(self.Colors.YELLOW)
                .turn_off()
                .turn_on()
                .blink(10, step=10)
                .sleep(sleep)
                .turn_off()
        )
    

    def info(self, sleep: int = 60) -> Lamp:
        return (
            self.set_color_rgbhex(self.Colors.BLUE)
                .turn_off()
                .turn_on()
                .blink(10, step=10)
                .sleep(sleep)
                .turn_off()
        )
