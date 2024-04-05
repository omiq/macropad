from adafruit_macropad import usb_hid
from adafruit_macropad import board
from adafruit_macropad import keypad
from adafruit_macropad import neopixel
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode
from adafruit_hid.consumer_control import ConsumerControl
from adafruit_hid.consumer_control_code import ConsumerControlCode
from adafruit_macropad import MacroPad
from time import sleep
macropad = MacroPad()


KEYCODES = (
    Keycode.SEVEN,
    Keycode.EIGHT,
    Keycode.NINE,
    Keycode.FOUR,
    Keycode.FIVE,
    Keycode.SIX,
    Keycode.ONE,
    Keycode.TWO,
    Keycode.THREE,
    Keycode.BACKSPACE,
    Keycode.ZERO,
    Keycode.ENTER,
)

# Default and activated key colours
ON_COLOR = (0, 0, 255)
OFF_COLOR = (5, 5, 10)
macropad.pixels.fill(OFF_COLOR)

# We need to store the encoder value so we can volume up and down
current_volume = macropad.encoder

# OLED display
text_lines = macropad.display_text()
text_lines.show()

# Volume control
cc = ConsumerControl(usb_hid.devices)

# Keyboard emulation
kbd = Keyboard(usb_hid.devices)


# Loop forever
while True:
    
    # Did something happen with keys
    key_event = macropad.keys.events.get()
    if key_event:
        key_number = key_event.key_number
        
        # A key transition occurred.
        if key_event.pressed:
            kbd.press(KEYCODES[key_number])
            macropad.pixels[key_number] = ON_COLOR

        if key_event.released:
            kbd.release(KEYCODES[key_number])
            macropad.pixels[key_number] = OFF_COLOR



    # Raise volume.
    if macropad.encoder > current_volume:
        cc.send(ConsumerControlCode.VOLUME_INCREMENT)
        current_volume = macropad.encoder
                
        # Update the screen
        macropad.display_image("volup.bmp")
    
    # Lower volume.
    if macropad.encoder < current_volume:
        cc.send(ConsumerControlCode.VOLUME_DECREMENT)
        current_volume = macropad.encoder
        
        # Update the screen
        macropad.display_image("voldown.bmp")

    # Rotary button - couple of options here
    macropad.encoder_switch_debounced.update()
    if macropad.encoder_switch_debounced.pressed:
        # Pause or resume playback.
        #cc.send(ConsumerControlCode.PLAY_PAUSE)
        cc.send(ConsumerControlCode.MUTE)
        
        # Update the screen
        macropad.display_image("mute.bmp")



