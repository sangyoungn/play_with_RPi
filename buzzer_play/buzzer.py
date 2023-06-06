# Refer to https://sourceforge.net/p/raspberry-gpio-python/wiki/Home/
# for RPi_GPIO module
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# Refer to https://docs.python.org/3/library/time.html
import time

class Buzzer:
    '''
    p = Buzzer(2) # Buzzer is connected to GPIO_2 (Pin 3). 

    p.play('O4C3D3E3FGABO5C3R2')

    The argument notes is a string which can contain following notes.
    
    Ox where x is an integer indicating an octave. 
        The notes afterward will be referenced to the specified octave. 
    Ty where y is an integer indicating the tempo. 
        The number of the tempo represents the number of quater notes played in a minute. 
    Rz, Cz, C#z, Dz, D#z, Ez, Fz, F#z, Gz, G#z, Az, A#z, Bz where z is an integer representing the duration of playing. 
        R represents the Rest, C to B do steps in a musical scale. 
        z can be 
            1 representing a whole note, 
            2 a half note, 
            3 a quater note, 
            4 a eighth note, and so on. 
            0 is used only with R.
    '''
    NOTES = ('C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B')

    def __init__(self, port=None):
        '''
        port: The port number. This shall be represened in the port number of GPIO.BCM.
        '''
        if(port==None):
            raise ValueError('The port number of a GPIO must be specified.')
        self._beingPlayed = False
        self._octave = 4
        self._tempo = 90
        self._previous_note = 0
        GPIO.setup(port, GPIO.OUT)
        self._control = GPIO.PWM(port, 1000)

    def __del__(self):
        self.stop_tone()

    def _isPlaying(self)->bool:
        '''
        Return the flag if a tone is playing now.
        '''
        return self._beingPlayed
    
    def _setPlaying(self):
        '''
        Set the flag to indicate a tone is playing now.
        '''
        self._beingPlayed = True

    def _resetPlaying(self):
        '''
        Reset the flag to indicate any tone isn't playing now.
        '''
        self._beingPlayed = False
    
    def _nextNote(self, playingNotes:str)->tuple[str, int, str]:
        '''
        Returns next note to play extracted fron the string and remaining string.
        '''

        index = 0

        if playingNotes[index].isalpha():
            # The first of the string must be a alphabet.
            # Only one character shall represent a step.
            step = playingNotes[index].upper()
            index += 1

            if index < len(playingNotes):
                # Next, it can be a '#'
                if playingNotes[index]=='#':
                    # Add '#' to the scale.
                    step+=playingNotes[index]
                    index += 1
                
                # If a alphabet character comes again, 
                # it means a note is done. No more processing.
                # This means we follow the length of previous note.
                elif playingNotes[index].isalpha():
                    if step == 'O' or step == 'T':
                        raise ValueError('A numeric argument is required for O or T.')
                    if self._previous_note != 0:
                        note = self._previous_note
                    else:
                        # No previous note? Let's use a quaterer note by default.
                        note = 3
                    # The remaining string is for processing next time.
                    remaining = playingNotes[index:]
                
                # A number is coming. It must be a lenth of a note.
                elif playingNotes[index].isnumeric():
                    # Let's store the number in a variable.
                    note = playingNotes[index]
                    index += 1
                    for ii in range(index, len(playingNotes)):
                        # If a number comes again, add to the variable.
                        if playingNotes[ii].isnumeric():
                            note = note+playingNotes[ii]
                        else: # If not, that's it.
                            index = ii
                            break
                    note = int(note) # Convert the string to int.
                    if step in Buzzer.NOTES:
                        self._previous_note = note
                    remaining = playingNotes[index:]
            else:
                # It was the last character representing a step without numeric argument.
                if step == 'O' or step == 'T':
                        raise ValueError('A numeric argument is required for O or T.')
                if self._previous_note != 0:
                    note = self._previous_note
                else:
                    note = 3
                remaining = playingNotes[index:]
        else:
            raise ValueError('The format of the notes string is wrong.')
        
        # print(step, note, remaining)
        return step, note, remaining


    def calculateFreq(self, step)->float:
        '''
        Calculate and return the frequecy with a give scale.
        The argument, step can be 
        'C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B'.
        '''
        if not ((step in Buzzer.NOTES) or step=='R'):
            raise ValueError('Not a valid name of a step.')
        
        if (step=='R'):
            # If it is a Rest, return 0 of freq.
            freq = 0
        else:
            # The reference scale is 'A', whose frequency in O4 is 440 Hz.
            # Each scale has the frequency of 2**(1/12) times of that of previous one.
            # 440*(2**(octave-4))*2**((step-10)/12)
            freq = 440.0*(2**(self._octave-4))*2**(((Buzzer.NOTES.index(step)+1)-10)/12)

        return freq

    def calculateDuration(self, note:int)->float:
        '''
        Calculate and return the duration of the tone.
        The argument, note has a type int and can be
        0: NOP, 1: Whole Note, 2: Half Note, 3: Quater Note,
        4: Eighth Note, 5: Sixteenth Note, 6: 32nd Notes, ...
        '''
        if type(note) !=  int:
            raise TypeError('The type of int is expected.')
        if note == 0: # This indicate no retention.
            return 0
        
        # The tempo here means how many quater notes are played in a minute.
        # So, a quatoer note is played for (1/tempo) and
        # a whole note is played for 4*(1/tempo).
        # A half note is played for a half of a whole note,
        # a quatoer note is played for a quater, and so on.
        duration = 4*(60/self._tempo)*(1/(2**(note-1)))

        return duration


    def change_tempo(self, tempo:int):
        '''
        Change the tempo of current play.
        The argument, tempo represents how many quauter notes are played in a minute.
        '''
        if tempo != 0:
            self._tempo = tempo
        else:
            raise ValueError('0 of tempo is not allowed.')
        
    def change_octave(self, octave:int):
        '''
        Change the octave of the current play.
        The argument, octave shalle be a integer between 1 and 8.
        '''
        if octave >= 1 and octave <= 8:
            self._octave = octave
        else:
            raise ValueError('The octave should be between 1 and 8.')

    def start_tone(self):
        '''
        Helper method to start a tone of the preconfigured frequency.
        '''
        self._control.start(50)
        self._setPlaying()

    def stop_tone(self):
        '''
        Helper method to stop a tone currently being played.
        '''
        self._control.stop() # Immediately stop the tone.
        self._resetPlaying()

    def play_tone(self, freq=1000, duration=0):
        '''
        Play a tone with a given frequency for a duration.
        The tone will not stop unless the frequency is 0.
        '''
        # If freq is zero, we will be silent. That is, it is same as Rest.
        if freq != 0:
            self._control.ChangeFrequency(freq)
            if not self._isPlaying():
                self.start_tone()
        else:
            self.stop_tone()

        if(duration !=0): 
            time.sleep(duration)

    def play(self, notes:str):
        '''
        The main method to play notes.
        '''

        playing_notes = notes
        while (len(playing_notes)!=0):
            # We get next note and param to play and keep the rest of notes.
            step, note, playing_notes = self._nextNote(playing_notes)
            # print(scale, note, playing_notes)
            if step == 'T':
                self.change_tempo(note)
                continue
            if step == 'O':
                self.change_octave(note)
                continue

            self.play_tone(self.calculateFreq(step), self.calculateDuration(note))
        self.stop_tone()

if __name__ == '__main__':
    p = Buzzer(2) # Buzzer is connected to GPIO_2 (Pin 3). 

    p.play('O4C3D3E3FGABO5C3R2')

    p.play('O4T90A4A5G5F4G4A4R0A4R0A3')
    p.play('G4R0G4R0G3A4R0A4R0A3')
    p.play('A4A5G5F4G4A4R0A4R0A3')
    p.play('G4R0G4A4A5G5F2')
    p.play('R3')

    p.play('O4T140G3R0G3E4F4G3A3R0A3G2G3O5C3E3D4C4D2D3R3')
    p.play('E3R0E3D3R0D3C3D4C4O4A3A3G3R0G3R0G3E4D4C2C3R3')
    p.play('D3R0D3E3C3D3R0D3E3G3A3O5C3E3D4C4D2D3R3')
    p.play('E3R0E3D3R0D3C3D4C4O4A3R0A3G3R0G3R0G3E4D4C2C3R3')