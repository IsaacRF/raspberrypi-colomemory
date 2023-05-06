from gpiozero import Button, LED, TonalBuzzer
from gpiozero.tones import Tone
from time import sleep
import random

class Color:
    def __init__(self, led: LED, button: Button, sound: Tone):
        self.led = led
        self.button = button
        self.sound = sound
    
    def is_on(self):
        return self.button.is_pressed
        
color_red = Color(LED(25), Button(17), Tone('C4'))
color_yellow = Color(LED(24), Button(4), Tone('D4'))
color_green = Color(LED(23), Button(3), Tone('E4'))
color_blue = Color(LED(18), Button(2), Tone('F4'))
colors = [color_red, color_yellow, color_green, color_blue]

speaker = TonalBuzzer(5)
positive_sound = ["A5", "G5", "A5", "G5"]
negative_sound = ["A4", "G4", "F4", "E4", "D4", "C4"]
bootup_sound = ["C4", "D4", "E4", "F4", "G4", "A4"]

# Round sequence of colors
sequence = []

def lights_on():
    for color in colors:
        color.led.on()
        
def lights_off():
    for color in colors:
        color.led.off()
        
def flash_lights():
    for _ in range(3):
        lights_on()
        sleep(0.25)
        lights_off()
        sleep(0.25)

def play_sound(sound):
    for note in sound:
        speaker.play(note)
        sleep(0.03)
        speaker.stop()
        sleep(0.1)
        
def show_round_results(result: bool):
    light_result = light3 if result else light1
    sound_result = positive_sound if result else negative_sound
    
    light_result.on()
    play_sound(sound_result)

# Bootup sequence
play_sound(bootup_sound)
flash_lights()

while True:
    # Add a random new color to the sequence
    new_color = random.choice(colors)
    sequence.append(new_color)
    
    # Play current sequence
    for color in sequence:
        color.led.on()
        speaker.play(color.sound)
        sleep(0.5)
        color.led.off()
        speaker.stop()
        sleep(0.25)
        
    # Get player's input
    for color_seq in sequence:
        guess = None
        
        while guess == None:
            for color in colors:
                if color.button.is_pressed:
                    guess = colors.index(color)
                    
        if colors[guess] == color_seq:
            # Guess is right
            color_seq.led.on()
            speaker.play(color_seq.sound)
            sleep(0.25)
            color_seq.led.off()
            speaker.stop()
            sleep(0.25)
        else:
            # Fail
            color_red.led.blink(0.25, 0.25)
            play_sound(negative_sound)
            sleep(1)
            color_red.led.off()
            
            sequence = []
            break