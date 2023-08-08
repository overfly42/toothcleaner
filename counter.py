from concurrent.futures import process
from enum import Enum
import pyttsx3  
from time import sleep

DEBUG_OUTPUT = False
COUNTER_VALUE = 5
TIMER_SLEEP = 0.75
REPEAT = False

class count_direction(Enum):
    up=0,
    down=1

class base_state():
    def __init__(self,voice) -> None:
        super().__init__()
        self.next_state = None
        self.voice = voice
        self.words = {'german':None}
        self.select_language('german')
    def enter_state(self):
        raise NotImplementedError('Base Class is accessed')
    def enter_next_state(self):
        raise NotImplementedError('Base Class is accessed')
    def get_current_state(self):
        return self.current_state
    def set_next_state(self,next_state):
        self.next_state = next_state
    def get_supported_languages(self)->list:
        return self.words.keys()
    def select_language(self,lang:str):
        if not lang in self.get_supported_languages():
            raise NotImplementedError("The language {} is not supported by now".format(lang))
        self.language=lang
    def speak(self,text:str):
        self.voice.say(text)
        self.voice.runAndWait()
        sleep(TIMER_SLEEP)
        
class area_state(base_state):
    '''
        Each area represents one of three areas of each region e.g. chewing area
    '''
    def __init__(self,voice,get_count_dir) -> None:
        '''
            Parameters:
                voice:
                    The voice processing e.g. pyttsx3 engine
                get_count_dir:
                    function which returns count_direction without parameter
        '''
        super().__init__(voice)
        self.words['german'] = ['Kaufläche','Außenseite','Innenseite']
        self.region_count_max = len(self.words['german'])
        self.upcounting = []
        self.upcounting.extend(range(1,COUNTER_VALUE+1)) 
        self.downcounting = self.upcounting.copy()
        self.downcounting.reverse()
        self.countdirection = get_count_dir
    def process_state(self,word:str):
        global REPEAT
        if DEBUG_OUTPUT:
            print(word)
        else:
            self.speak(word)
        for i in range(len(self.upcounting)):
            if self.countdirection() == count_direction.up:
                text = self.upcounting[i]
            else:
                text = self.downcounting[i]
            if DEBUG_OUTPUT:
                print(text)
            else:
                self.speak(text)
        if REPEAT:
            REPEAT = False
            self.process_state(word)
        
    def enter_state(self):
        self.region_count = 0
        for word in self.words[self.language]:
            self.process_state(word)
        self.enter_next_state()
    def enter_next_state(self):
        self.next_state.enter_state()

class region_state(base_state):
    '''
        Each region represents a region within the mouth. Upper / lower left/center/right
    '''
    def __init__(self,voice) -> None:
        super().__init__(voice)
        self.reset()
        self.words['german'] = {'start':'Beginnen','stop':'Fertig','continue':'Nächste Seite'}
    def reset(self):
        self.area_count = 0
        self.area_count_max = 6
        self.running = False
    def enter_state(self):
        if not self.running:
            return
        self.running = False
        #match self.area_count:
        #    case 0:
        #        text = self.words[self.language]['start']
        #    case 5:
        #        text = self.words[self.language]['stop']
        #    case _:
        #        text = self.words[self.language]['continue']
        if self.area_count == 0:
            text = self.words[self.language]['start']
        elif self.area_count == 5:
            text = self.words[self.language]['stop']
        else :
            text = self.words[self.language]['continue']
        if DEBUG_OUTPUT:
            print(text)
        else:
            self.speak(text)
        self.area_count = self.area_count+1
        if self.area_count == self.area_count_max:
            self.running = False
            return
        self.enter_next_state()
    def enter_next_state(self):
        self.next_state.enter_state()

def default_count_dir() -> count_direction:
    return count_direction.down

def init_state_maschine(func_count_dir=default_count_dir)->region_state:
    '''
        Initalizes the state maschine and connects it. also returns the main state
    '''
    voice = pyttsx3.init()  
    voice.setProperty('rate',175)
    voice.setProperty('voice','german-mbrola-7')
    area = area_state(voice,func_count_dir)
    region = region_state(voice)
    area.set_next_state(region)
    region.set_next_state(area)
    return region

if __name__ == '__main__':
    state = init_state_maschine()
    state.enter_state()