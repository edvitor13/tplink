from tplink.custom_lamp import CustomLamp
from tplink.lamp import Lamp

# CustomLamp Class
lamp = CustomLamp("emailtapoaccount@example.com", "PasswordTapoAccount", model="L530")
lamp.error(1)
lamp.success(1)
lamp.warning(1)
lamp.info(1)
lamp.turn_on()
lamp.set_brightness(1)

# Normal Lamp Class
lamp2 = Lamp("emailtapoaccount@example.com", "PasswordTapoAccount", label="Lâmpada Quarto", model="L530")
(
    lamp2
        .set_color_rgb(255, 0, 255)
        .turn_on()
        .set_color_rgbhex(lamp.Colors.RED)
        .sleep(10)
        .turn_off()
)
