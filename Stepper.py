import time
from machine import Pin, Timer

class StepperMotor:
    # Define Stepper Motor Step Sequences
    wave_steps = [0x01, 0x02, 0x04, 0x08]
    full_steps = [0x03, 0x06, 0x0C, 0x09]
    half_steps = [0x01, 0x03, 0x02, 0x06, 0x04, 0x0C, 0x08, 0x09]

    # Construct the Stepper Motor Object
    # Mode 0 = Wave Step, Mode 1 = Full Step, Mode 2 = Half Step
    def __init__(self, pin0, pin1, pin2, pin3, mode=1, delay=3):
        # Define GPIO pins for stepper motor
        self.pins = [
            Pin(pin0, Pin.OUT),
            Pin(pin1, Pin.OUT),
            Pin(pin2, Pin.OUT),
            Pin(pin3, Pin.OUT)
        ]

        # Set delay between steps (in milliseconds)
        self.delay = delay

        # Validate mode input
        if mode < 0 or mode > 2:
            mode = 1

        # Set operating mode
        self.mode = mode

        # Timer and step tracking for non-blocking rotation
        self._timer = None
        self._steps_remaining = 0
        self._current_step = 0

    # Setter for Delay
    def set_delay(self, delay):
        self.delay = delay

    # Setter for Mode
    def set_mode(self, mode):
        if mode < 0 or mode > 2:
            mode = 1
        self.mode = mode

    # Rotate the Stepper Motor
    def set_step(self, index):
        step_sequence = []
        if self.mode == 0:
            step_sequence = self.wave_steps
        elif self.mode == 1:
            step_sequence = self.full_steps
        else:
            step_sequence = self.half_steps

        # Handle differing lengths of step sequences
        index = index % len(step_sequence)

        # Set GPIO pins based on step sequence
        self.pins[0].value(1 if (step_sequence[index] & 0x01) else 0)
        self.pins[1].value(1 if (step_sequence[index] & 0x02) else 0)
        self.pins[2].value(1 if (step_sequence[index] & 0x04) else 0)
        self.pins[3].value(1 if (step_sequence[index] & 0x08) else 0)

    # Callback for internal timer
    # After delay timer, increment the current step
    def _timer_callback(self, t):
        if self._steps_remaining > 0:
            self.set_step(self._current_step)
            self._current_step += 1
            self._steps_remaining -= 1
        elif self._steps_remaining == -1:
            # Rotate until stopped
            self.set_step(self._current_step)
            self._current_step += 1

            # Roll over to reduce memory usage
            if self._current_step >= 256:
                self._current_step = 0
        else:
            self.stop_rotation()

    # Start rotation for a given number of revolutions (non-blocking)
    def start_rotation(self, revolutions):
        if revolutions == -1:
            # Rotate indefinitely
            self._steps_remaining = -1
            self._current_step = 0
        else:
            steps_per_revolution = 512  # Assuming 512 steps per revolution
            total_steps = int(revolutions * steps_per_revolution)
            self._steps_remaining = total_steps
            self._current_step = 0

        # Cleanup any existing timer
        if self._timer:
            self._timer.deinit()
        
        # Initialize and start the timer for non-blocking rotation
        self._timer = Timer(2)
        self._timer.init(period=self.delay, mode=Timer.PERIODIC, callback=self._timer_callback)

    # Stop the motor rotation
    def stop_rotation(self):
        if self._timer:
            self._timer.deinit()
            self._timer = None
        self._steps_remaining = 0