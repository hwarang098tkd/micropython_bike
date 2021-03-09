import utime
from machine import Pin
import neopixel


def wait_pin_change(pin):
    # wait for pin to change value
    # it needs to be stable for a continuous 20ms
    cur_value = pin.value()
    active = 0
    while active < 20:
        if pin.value() != cur_value:
            active += 1
        else:
            active = 0
        # utime.sleep_ms(100)


def debug1():
    global button_GO_up
    global button_GO_down
    global button_up
    global button_down
    #global button_STOP
    print('button_up: ' + str(button_up.value()))
    print('button_down: ' + str(button_down.value()))
    print('button_GO_up: ' + str(button_GO_up.value()))
    print('button_GO_down: ' + str(button_GO_down.value()))
    #print('button_STOP: ' + str(button_STOP.value()))
    print('---------------------------------------------')


class Stepper:
    """Class for stepper motor driven by Easy Driver."""

    def __init__(self, step_pin, dir_pin, sleep_pin):
        print("""Initialise stepper.""")
        self.stp = Pin(step_pin, Pin.OUT)
        self.dir = Pin(dir_pin, Pin.OUT)
        self.slp = Pin(sleep_pin, Pin.OUT)

    def power_on(self):
        print("""Power on stepper.""")
        self.slp.value(1)

    def power_off(self):
        print("""Power off stepper.""")
        self.slp.value(0)

    def direction(self, direct):
        if direct == 'UP':
            self.dir.value(1)
        else:
            self.dir.value(0)

    def move(self):
        delay = 900  # το καταλληλο delay
        print("""Start moving...""")
        while button_up.value() and button_down.value():
            self.stp.value(1)
            utime.sleep_us(delay)
            self.stp.value(0)
            utime.sleep_us(delay)
        self.stp.value(0)  # αυτο για να σβηνει το φωτακι του run , ενας θεος ξερει γιατι
        print("""END moving...""")
        self.power_off()

    def move_away(self):
        utime.sleep(0.2)
        delay = 900  # το καταλληλο delay
        print("""Start moving away...""")
        t_end = utime.time() + 0.5  # συν ενα δευτερολεπτο
        while utime.time() < t_end:
            self.stp.value(1)
            utime.sleep_us(delay)
            self.stp.value(0)
            utime.sleep_us(delay)
        self.stp.value(0)  # αυτο για να σβηνει το φωτακι του run , ενας θεος ξερει γιατι
        print("""END moving away...""")
        self.power_off()


def wheel(pos):
    # Input a value 0 to 255 to get a color value.
    # The colours are a transition r - g - b - back to r.
    if pos < 0 or pos > 255:
        return (0, 0, 0)
    if pos < 85:
        return (255 - pos * 3, pos * 3, 0)
    if pos < 170:
        pos -= 85
        return (0, 255 - pos * 3, pos * 3)
    pos -= 170
    return (pos * 3, 0, 255 - pos * 3)


def rainbow_cycle(wait):
    for j in range(255):
        for i in range(n):
            rc_index = (i * 256 // n) + j
            np[i] = wheel(rc_index & 255)
        np.write()
        utime.sleep_ms(wait)


def main():
    print('Main Module started.')
    global button_up
    global button_down
    button_up = Pin(2, Pin.IN)
    button_down = Pin(14, Pin.IN, Pin.PULL_UP)
    global button_GO_up
    global button_GO_down
    button_GO_up = Pin(4, Pin.IN, Pin.PULL_UP)
    button_GO_down = Pin(5, Pin.IN, Pin.PULL_UP)
    # global button_STOP
    # button_STOP = Pin(0, Pin.IN, Pin.PULL_UP)


    motor_move = 12  # Declare pin for movement
    motor_rotat = 13  # Declarepin for rotation
    motor_enable = 15  # Declare pin for enable

    motor1 = Stepper(motor_move, motor_rotat, motor_enable)
    motor1.power_off()
    global n
    global p

    n = 19
    p = 0
    global np
    np = neopixel.NeoPixel(Pin(p), n)

    while True:
        # rainbow_cycle(1)
        # rainbow_cycle(1)
        # if not button_STOP.value():
        #     print('button STOP')
        #     wait_pin_change(button_STOP)
        #     # debug1()

        if not button_GO_up.value():
            print('button GO UP')
            wait_pin_change(button_GO_up)
            motor1.direction('UP')
            motor1.move()
            # debug1()

        if not button_GO_down.value():  # working
            print('button Go Down')
            wait_pin_change(button_GO_down)
            motor1.direction('DOWN')
            motor1.move()
            # debug1()

        if not button_up.value():
            print('button UP stop moving')
            # wait_pin_change(button_up)
            motor1.direction('DOWN')
            motor1.move_away()
            # debug1()

        if not button_down.value():
            print('button Down stop moving')
            # wait_pin_change(button_down)
            motor1.direction('UP')
            motor1.move_away()
            # debug1()

        # utime.sleep_ms(100)


if __name__ == '__main__':
    main()
