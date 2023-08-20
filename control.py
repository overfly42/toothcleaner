import RPi.GPIO as GPIO
from time import sleep
import counter
import logging
import subprocess


BTN_START_COUNTING = 7
BTN_REPEAT_COUNTING = 11
BTN_CHOOSE_DIRECTION = 13



class master_control_program():
    def __init__(self) -> None:
        self.init_logging()
        self.setup()
        self.count_direction = counter.count_direction.up
        self.state_maschine = counter.init_state_maschine(self.get_direction)

#region Callbacks
    def callback_start(self,data):
        self.logger.info('Callback start triggered',extra=self.base_data)
        #set volumn to 20%
        proc = subprocess.Popen('/usr/bin/amixer sset Master 5%', shell=True, stdout=subprocess.PIPE)
        proc.wait()
        proc = subprocess.Popen('bluetoothctl connect 41:42:00:00:00:FA', shell=True, stdout=subprocess.PIPE)
        proc.wait()
        self.state_maschine.running = True
        #if self.state_maschine.running == False:
        #    self.state_maschine.enter_state()
    
    def callback_repeat(self,data):
        self.logger.info('Callback repeat triggered',extra=self.base_data)
        counter.REPEAT = True

    def callback_change_direction(self,data):
        self.logger.info('Callback change_direction triggered with current state: {}'.format(self.count_direction),extra=self.base_data)
        self.count_direction = counter.count_direction.up if self.count_direction == counter.count_direction.down else counter.count_direction.down
#endregion
#region External functions
    def get_direction(self):
        return self.count_direction
#endregion    
#region setup
    def init_logging(self):
        FORMAT = '%(asctime)s %(clientip)-15s %(user)-8s %(message)s'
        logging.basicConfig(format=FORMAT)
        self.base_data = {'clientip': '192.168.178.33', 'user': 'toothcleaner'}
        self.logger = logging.getLogger('Interaction')
        self.logger.setLevel(logging.INFO)

    def setup(self):
        self.logger.info('Starting Setup',extra=self.base_data)
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(BTN_START_COUNTING,GPIO.IN)
        GPIO.setup(BTN_REPEAT_COUNTING,GPIO.IN)
        GPIO.setup(BTN_CHOOSE_DIRECTION,GPIO.IN)
        #Set Callbacks
        GPIO.add_event_detect(BTN_START_COUNTING,GPIO.RISING,callback=self.callback_start)
        GPIO.add_event_detect(BTN_REPEAT_COUNTING,GPIO.RISING,callback=self.callback_repeat)
        GPIO.add_event_detect(BTN_CHOOSE_DIRECTION,GPIO.RISING,callback=self.callback_change_direction)
        self.logger.info('Setup Done',extra=self.base_data)
#endregion
if __name__ == '__main__':
    mcp = master_control_program()
    while True:
        mcp.state_maschine.enter_state()
        sleep(5)