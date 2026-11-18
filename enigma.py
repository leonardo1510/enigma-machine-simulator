"""
    Implementation of an Enigma machine simulator.
    The classes PlugLead, Plugboard, Rotor and EnigmaMachine model the physical components; the latter wraps
    all the others and is responsible for encoding/decoding characters with a given configuration.
    Running this file decodes an example message (see the demonstration in enigma.ipynb).
"""
from typing import List, Dict, Tuple
import logging

logger = logging.getLogger(__name__)

# WARNING is the default logging level.
# If you want to change it, just edit the 'level' parameter bellow.

logging.basicConfig(
    level=logging.WARNING,
    format='%(levelname)s:%(filename)s:%(message)s'
    )

# Constants
# Rotor and reflector wirings, alphabet labels, and notch positions.

PATTERNS = {
    "Beta":  {"A":"L","B":"E","C":"Y","D":"J","E":"V","F":"C","G":"N","H":"I","I":"X","J":"W","K":"P","L":"B","M":"Q","N":"M","O":"D","P":"R","Q":"T","R":"A","S":"K","T":"Z","U":"G","V":"F","W":"U","X":"H","Y":"O","Z":"S"},
    "Gamma": {"A":"F","B":"S","C":"O","D":"K","E":"A","F":"N","G":"U","H":"E","I":"R","J":"H","K":"M","L":"B","M":"T","N":"I","O":"Y","P":"C","Q":"W","R":"L","S":"Q","T":"P","U":"Z","V":"X","W":"V","X":"G","Y":"J","Z":"D"},
    "I":     {"A":"E","B":"K","C":"M","D":"F","E":"L","F":"G","G":"D","H":"Q","I":"V","J":"Z","K":"N","L":"T","M":"O","N":"W","O":"Y","P":"H","Q":"X","R":"U","S":"S","T":"P","U":"A","V":"I","W":"B","X":"R","Y":"C","Z":"J"},
    "II":    {"A":"A","B":"J","C":"D","D":"K","E":"S","F":"I","G":"R","H":"U","I":"X","J":"B","K":"L","L":"H","M":"W","N":"T","O":"M","P":"C","Q":"Q","R":"G","S":"Z","T":"N","U":"P","V":"Y","W":"F","X":"V","Y":"O","Z":"E"},
    "III":   {"A":"B","B":"D","C":"F","D":"H","E":"J","F":"L","G":"C","H":"P","I":"R","J":"T","K":"X","L":"V","M":"Z","N":"N","O":"Y","P":"E","Q":"I","R":"W","S":"G","T":"A","U":"K","V":"M","W":"U","X":"S","Y":"Q","Z":"O"},
    "IV":    {"A":"E","B":"S","C":"O","D":"V","E":"P","F":"Z","G":"J","H":"A","I":"Y","J":"Q","K":"U","L":"I","M":"R","N":"H","O":"X","P":"L","Q":"N","R":"F","S":"T","T":"G","U":"K","V":"D","W":"C","X":"M","Y":"W","Z":"B"},
    "V":     {"A":"V","B":"Z","C":"B","D":"R","E":"G","F":"I","G":"T","H":"Y","I":"U","J":"P","K":"S","L":"D","M":"N","N":"H","O":"L","P":"X","Q":"A","R":"W","S":"M","T":"J","U":"Q","V":"O","W":"F","X":"E","Y":"C","Z":"K"},
    "A":     {"A":"E","B":"J","C":"M","D":"Z","E":"A","F":"L","G":"Y","H":"X","I":"V","J":"B","K":"W","L":"F","M":"C","N":"R","O":"Q","P":"U","Q":"O","R":"N","S":"T","T":"S","U":"P","V":"I","W":"K","X":"H","Y":"G","Z":"D"},
    "B":     {"A":"Y","B":"R","C":"U","D":"H","E":"Q","F":"S","G":"L","H":"D","I":"P","J":"X","K":"N","L":"G","M":"O","N":"K","O":"M","P":"I","Q":"E","R":"B","S":"F","T":"Z","U":"C","V":"W","W":"V","X":"J","Y":"A","Z":"T"},
    "C":     {"A":"F","B":"V","C":"P","D":"J","E":"I","F":"A","G":"O","H":"Y","I":"E","J":"D","K":"R","L":"Z","M":"X","N":"W","O":"G","P":"C","Q":"T","R":"K","S":"U","T":"Q","U":"S","V":"B","W":"N","X":"M","Y":"H","Z":"L"},
}

LABELS = ["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z"]

NOTCHES = {
    "I":   "Q",
    "II":  "E",
    "III": "V",
    "IV":  "J",
    "V":   "Z"
}

# Enigma Machine classes implementation.

class PlugLead:
    """
    Blueprint for the PlugLead object, responsible for creating the connection between two letters inside the PlugBoard.
    The class takes as input the following parameter(s):

        - mapping:str =  a str of len 2 used for creating the mapping between the two letters
    
    The class has the following method(s):

        - check_mapping() = A class method that checks if a str of len=2 is given as input. 
                            If the check fails, it returns a ValueError.

        - encode() = it takes a str as input, and returns the corresponding str value found inside the mappping dictionary
                     created once the PlugLead is initialized.

    """

    @classmethod
    def check_mapping(cls, mapping: str):
        if len(mapping) != 2:
            logger.error("Input mapping should be of len=2.")
            raise ValueError

    def __init__(self, mapping: str):
        self.check_mapping(mapping)
        self.raw_mapping = mapping
        self.mapping = {mapping[0]: mapping[1], mapping[1]: mapping[0]}
        

    def __str__(self) -> str:
        return f"Plug {self.raw_mapping}."
    
    def __repr__(self) -> str:
        return f"Plug {self.raw_mapping}."
    
    def encode(self, character:str) -> str:
        if character not in self.mapping:
            logger.debug("PlugLead for character %s not found. Returning character.", character)
            return character
        else:
            logger.info("PlugLead for character found. Returning %s.", self.mapping.get(character))
            return self.mapping.get(character)


class Plugboard:
    """
    Blueprint for the PlugBoard object.
    The class has the following method(s):

        - add() =  it adds a new PlugLead object to the PlugBoard. It takes a Pluglead object an input
                   and, since it is a procedure, it does not return anything.

        - encode() = it is responsible for the encoding and decoding of a character using the PlugLeads previously added. It takes
                    a str as input and returns the encoded/decoded character.
    """
    def __init__(self):
        self.plug_limit = 10
        self.raw_plugboard = set()
        self.plugboard = set()
    
    def __str__(self) -> str:
        return f"Plugboard {self.plugboard}."
    
    def __repr__(self) -> str:
        return f"Plugboard {self.plugboard}."

    def add(self, plug_lead: PlugLead):
        if len(self.plugboard) == self.plug_limit:
            return None
        elif (not plug_lead.raw_mapping in self.raw_plugboard) and (not plug_lead.raw_mapping[::-1] in self.raw_plugboard):
            self.raw_plugboard.add(plug_lead.raw_mapping)
            self.plugboard.add(plug_lead)
        else:
            logger.warning("Lead duplicato %s ignorato", plug_lead.raw_mapping)

    def encode(self, character: str) -> str:

        encoded_char = None

        for plug in self.plugboard:
            if character in plug.mapping:
                encoded_char = plug.mapping.get(character, None)
                break
        
        if encoded_char is None:
            logger.debug("PlugLead for character %s not found. Returning character.", character)
            return character
        
        logger.info("PlugLead for character found. Returning %s.", encoded_char)
        return encoded_char


class Rotor:
    """
    Blueprint for the Rotor object.

    The class takes as input the following parameter(s):

        - current_position:str = the starting position of the Rotor object.

        - setting:int = the fixed setting of the Rotor object.

    The class has the following method(s):

        - _modify_positioning() = it modifies the position of the Rotor object when a new character needs to be encoded/decoded, and, if needed, during 
                                  the initialization of the Enigma machine. It takes as input the position, a str representing the current position of the rotor, and 
                                  an int representing the setting, thus the offset that needs to be applied to calculate the right next position. Since it is a procedure,
                                  it does not return anything.

        - encode_right_to_left() = it encodes/decodes a character when it is flowing from right to left. it takes a character str as input and it returns
                                   the encoded/decoded character.

        - encode_left_to_right() = it encodes/decodes a character when it is flowing from left to right. it takes a character str as input and it returns
                                   the encoded/decoded character.
    """

    def __init__(self, pattern: str, current_position: str, setting: int):
        self.pattern = pattern

        self.right_pattern = PATTERNS.get(self.pattern)
        self.left_pattern = {v:k for k,v in PATTERNS.get(self.pattern).items()}

        self.position = {LABELS[n]:n+1 for n in range(len(LABELS))}
        self.numbered_position = {n+1: LABELS[n] for n in range(len(LABELS))}

        self.ring_setting = {LABELS[n]:abs(n)+1 for n in range(-1,-(len(LABELS) + 1),-1)}
        self.ring_setting["A"] = 1
        self.numbered_ring_setting = {v:k for k,v in self.ring_setting.items()}

        self.setting = setting

        self.current_position = current_position

    def __str__(self) -> str:
        return f"Rotor with pattern {self.pattern} and position {self.current_position}."
    
    def __repr__(self) -> str:
        return f"Rotor with pattern {self.pattern} and position {self.current_position}."
    
    def _modify_positioning(self, position: str, setting: int):

        if setting != 1:
            index_position = LABELS.index(position)
            index_position = index_position-setting
            position = LABELS[index_position + 1]

        self.position[position] = 1

        position_index = LABELS.index(position)
        left_position_labels = LABELS[0:position_index]
        right_position_labels = LABELS[(position_index + 1):]

        left_counter = 26
        for label in sorted(left_position_labels,reverse=True):
            self.position[label] = left_counter
            left_counter -= 1
        
        right_counter = 2
        for label in right_position_labels:
            self.position[label] = right_counter
            right_counter += 1

        self.numbered_position = {v:k for k,v in self.position.items()}

    def encode_right_to_left(self, character: str) -> str:
        return self.right_pattern.get(character)
    
    def encode_left_to_right(self, character: str) -> str:
        return self.left_pattern.get(character)

class EnigmaMachine:
    """
    Blueprint for the Enigma Machine object.

    The class takes as input the following parameter(s):

        - rotors:list(Rotor) = list of the Rotors building the inner motor of the EnigmaMachine object.
        
        - reflector:Rotor = an additional Rotor object used as reflecot. Compared to the other Rotors, the reflector does not rotate and it always maps the 
                            same letter base don the selected pattern.
        - plugboard:Plugboard = a Plugboard object

    The class has the following method(s):

        - _init_rotors() = it sets the rotors to their starting position at startup. Since it is a procedure, it does not return anything.

        - _encode_right_to_left() = it encodes/decodes a character when it is flowing from right to left. It takes the following 
                                    input parameters: a character str, a rotor, the previous rotor position and a booolean value set as True
                                    if the rotor is in the rightmost position. It returns a tuple containing the encoded/decoded character and an int representing
                                    the actual position of the encoded/decoded character.

        - _encode_left_to_right() = it encodes/decodes a character when it is flowing from left to right. It takes the following 
                                    input parameters: a character str, a rotor, the previous rotor position and a booolean value set as True
                                    if the rotor is in the leftmost position. It returns a tuple containing the encoded/decoded character and an int representing
                                    the actual position of the encoded/decoded character.
        
        - _reflector() = this method is responsible for activating the reflector. It takes a str as input and returns the encoded/decoded character.

        - _change_position() = an helper method used to update the position of the rotors whenever they it their notch position. It encompasses both
                               the 3 and 4 rotors scenario. Since it is a procedure, it does not return anything.

        - encode_character() = it is the main method of the EnigmaClass. It simulates the entire EnigmaMachine process of encoding/decoding a charcater.
                               It takes a str an input and returns the encoded/decoded character.
    """

    def __init__(self, rotors: List[Rotor], reflector: Rotor, plugboard: Plugboard = None):
        self.rotors = rotors
        self.reflector = reflector
        self.plugboard = plugboard

        self.notch_list = [False] * len(rotors)

    def __str__(self) -> str:
        return f"Enigma Machine with Rotors {self.rotors}, Reflector {self.reflector}, and PlugBoard {self.plugboard}."
    
    def __repr__(self) -> str:
        return f"Enigma Machine with Rotors {self.rotors}, Reflector {self.reflector}, and PlugBoard {self.plugboard}."

    def _init_rotors(self):

        logger.info("Init Enigma: rotors=%s reflector=%s plugboard=%d leads",
                [r.pattern for r in self.rotors],
                self.reflector.pattern,
                len(self.plugboard.plugboard) if self.plugboard else 0)

        for el in self.rotors:
            el._modify_positioning(el.current_position, el.setting)

    #ENCODING METHODS
    def _encode_right_to_left(self, rotor: Rotor, char: str, previous_rotor_position: int = None, first_rotor: bool = False) -> Tuple[str,int]:
        if first_rotor:

            number_to_encode = LABELS.index(char) + 1

            char_to_encode = rotor.numbered_position.get(number_to_encode)

            different_encoded_letter = rotor.encode_right_to_left(char_to_encode)
            char_number = rotor.position.get(different_encoded_letter)

            return different_encoded_letter, char_number
        else:

            char_to_encode = rotor.numbered_position.get(previous_rotor_position)

            different_encoded_letter = rotor.encode_right_to_left(char_to_encode)

            char_number = rotor.position.get(different_encoded_letter)
            return different_encoded_letter, char_number
    
    def _encode_left_to_right(self, rotor: Rotor, char: str, previous_rotor_position: int = None, first_rotor: bool = False) -> Tuple[str,int]:
        if first_rotor:
            number_to_encode = LABELS.index(char) + 1

            char_to_encode = rotor.numbered_position.get(number_to_encode)

            different_encoded_letter = rotor.encode_left_to_right(char_to_encode)
            char_number = rotor.position.get(different_encoded_letter)

            return different_encoded_letter, char_number
        else:
            char_to_encode = rotor.numbered_position.get(previous_rotor_position)

            different_encoded_letter = rotor.encode_left_to_right(char_to_encode)
            char_number = rotor.position.get(different_encoded_letter)
            return different_encoded_letter, char_number
    
    def _reflector(self, char: str) -> str:
        return self.reflector.encode_right_to_left(char) or self.reflector.encode_left_to_right(char)
    
    def _change_position(self):

        if len(self.rotors) == 4:
            left, middle_first, middle_second, right = self.rotors[0], self.rotors[1], self.rotors[2], self.rotors[3]

            right_at_notch = right.current_position == NOTCHES.get(right.pattern,"")
            middle_first_at_notch = middle_first.current_position == NOTCHES.get(middle_first.pattern,"")
            middle_second_at_notch = middle_second.current_position == NOTCHES.get(middle_second.pattern,"")

            step_right = True
            step_middle_second = right_at_notch or middle_second_at_notch
            step_middle_first = middle_second_at_notch
            step_left = False

            if step_right:
                idx = LABELS.index(self.rotors[3].current_position)
                self.rotors[3].current_position = LABELS[(idx + 1) % 26]
                self.rotors[3]._modify_positioning(self.rotors[3].current_position, self.rotors[3].setting)

            if step_middle_second:
                idx = LABELS.index(self.rotors[2].current_position)
                self.rotors[2].current_position = LABELS[(idx + 1) % 26]
                self.rotors[2]._modify_positioning(self.rotors[2].current_position, self.rotors[2].setting)

            if step_middle_first:
                idx = LABELS.index(self.rotors[1].current_position)
                self.rotors[1].current_position = LABELS[(idx + 1) % 26]
                self.rotors[1]._modify_positioning(self.rotors[1].current_position, self.rotors[1].setting)

            if step_left:
                idx = LABELS.index(self.rotors[0].current_position)
                self.rotors[0].current_position = LABELS[(idx + 1) % 26]
                self.rotors[0]._modify_positioning(self.rotors[0].current_position, self.rotors[0].setting)
        
        else:

            left, middle, right = self.rotors[0], self.rotors[1], self.rotors[2]

            right_at_notch = right.current_position == NOTCHES.get(right.pattern,"")
            middle_at_notch = middle.current_position == NOTCHES.get(middle.pattern,"")

            step_right = True
            step_middle = right_at_notch or middle_at_notch
            step_left = middle_at_notch

            if step_right:
                idx = LABELS.index(self.rotors[2].current_position)
                self.rotors[2].current_position = LABELS[(idx + 1) % 26]
                self.rotors[2]._modify_positioning(self.rotors[2].current_position, self.rotors[2].setting)

            if step_middle:
                idx = LABELS.index(self.rotors[1].current_position)
                self.rotors[1].current_position = LABELS[(idx + 1) % 26]
                self.rotors[1]._modify_positioning(self.rotors[1].current_position, self.rotors[1].setting)

            if step_left:
                idx = LABELS.index(self.rotors[0].current_position)
                self.rotors[0].current_position = LABELS[(idx + 1) % 26]
                self.rotors[0]._modify_positioning(self.rotors[0].current_position, self.rotors[0].setting)
    
    def encode_character(self, char: str) -> str:

        self._change_position()

        encoded_charcater = self.plugboard.encode(char) if self.plugboard else char

        for rotor in self.rotors[-1::-1]:

            if self.rotors.index(rotor) == (len(self.rotors) - 1):
                encoded_charcater, char_number = self._encode_right_to_left(rotor, encoded_charcater, first_rotor= True)
            else:
                encoded_charcater, char_number = self._encode_right_to_left(rotor, char, previous_rotor_position=char_number)
        
        encoded_charcater = LABELS[char_number - 1]
        encoded_charcater = self._reflector(encoded_charcater)

        for rotor in self.rotors:

            if self.rotors.index(rotor) == 0:
                encoded_charcater, number = self._encode_left_to_right(rotor, encoded_charcater, first_rotor= True)
            else:
                encoded_charcater, number = self._encode_left_to_right(rotor, encoded_charcater, previous_rotor_position=number)
        final_char =  LABELS[number-1]

        final_char = self.plugboard.encode(final_char) if self.plugboard else final_char

        logger.debug("%s -> %s", char, final_char)
        return final_char 
            


if __name__ == "__main__":
    
    # Set up your own Enigma machine and try encoding/decoding words.

    # PlugBoard Init
    plugboard = Plugboard()
    plugboard.add(PlugLead("PC"))
    plugboard.add(PlugLead("XZ"))
    plugboard.add(PlugLead("FM"))
    plugboard.add(PlugLead("QA"))
    plugboard.add(PlugLead("ST"))
    plugboard.add(PlugLead("NB"))
    plugboard.add(PlugLead("HY"))
    plugboard.add(PlugLead("OR"))
    plugboard.add(PlugLead("EV"))
    plugboard.add(PlugLead("IU"))

    #Enigma Machine Init

    enigma = EnigmaMachine(rotors=[Rotor("IV","E",18), Rotor("V","Z",24), Rotor("Beta","G",3), Rotor("I","P",5)], reflector=Rotor("A","A",1), plugboard = plugboard)
    enigma._init_rotors()

    new_word = ""
    for w in "BUPXWJCDPFASXBDHLBBIBSRNWCSZXQOLBNXYAXVHOGCUUIBCVMPUZYUUKHI":
        new_w = enigma.encode_character(w)
        new_word += new_w

    print(f"The word 'BUPXWJCDPFASXBDHLBBIBSRNWCSZXQOLBNXYAXVHOGCUUIBCVMPUZYUUKHI' is: {new_word}")
