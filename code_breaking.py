"""
    Code-breaking routines for five Enigma-encrypted messages.

    Each `code_break_N` function brute-forces the unknown part of the machine configuration
    (reflector, starting positions, rotors / ring settings, plug leads, or a modified reflector wiring),
    using a known word in the plaintext (a "crib") to recognise the correct decryption.

    Running this file prints the decrypted messages and the recovered settings.
    The commented blocks inside some functions show how every candidate result can optionally be dumped
    to JSON files to inspect the whole search space.
"""

from enigma import *
import random
from itertools import combinations, combinations_with_replacement, product
import json
from typing import Dict

########################## CODE 1 ##########################

def code_break_1():
    print("Code Breaking: Code 1.")

    plugboard = Plugboard()
    plugboard.add(PlugLead("KI"))
    plugboard.add(PlugLead("XN"))
    plugboard.add(PlugLead("FL"))

    word = "DMEXBMKYCVPNQBEDHXVPZGKMTFFBJRPJTLHLCHOTKOYXGGHZ"

    for reflector in ["A", "B", "C"]:

        enigma = EnigmaMachine(
                rotors=[Rotor("Beta","M",4), Rotor("Gamma","J",2), Rotor("V","M",14)],
                reflector=Rotor(reflector,"A",1),
                plugboard=plugboard
            )
    
        enigma._init_rotors()

        new_word = ""
        for w in word:

            new_w = enigma.encode_character(w)
            new_word += new_w

        if "SECRETS" in new_word:
                print(f"Word {new_word} found with Reflector {reflector}")
                return {
                    "Reflector": reflector,
                    "Output": new_word
                }

# ########################## CODE 2 ##########################

def code_break_2():
    print("Code Breaking: Code 2.")

    plugboard = Plugboard()
    plugboard.add(PlugLead("VH"))
    plugboard.add(PlugLead("PT"))
    plugboard.add(PlugLead("ZG"))
    plugboard.add(PlugLead("BJ"))
    plugboard.add(PlugLead("EY"))
    plugboard.add(PlugLead("FS"))

    word = "CMFSUPKNCBMUYEQVVDYKLRQZTPUFHSWWAKTUGXMPAMYAFITXIJKMH"

    combs = product(LABELS, repeat=3)

    # OUPUT_PATH = "combinations_results.json"
    # result = {}

    for comb in combs:

        comb = list(comb)

        enigma = EnigmaMachine(
                rotors=[Rotor("Beta",comb[0],23), Rotor("I",comb[1],2), Rotor("III",comb[2],10)],
                reflector=Rotor("B","A",1),
                plugboard=plugboard
            )
        
        enigma._init_rotors()

        new_word = ""
        for w in word:

            new_w = enigma.encode_character(w)
            new_word += new_w

        # result["".join(comb)] = new_word

        if "UNIVERSITY" in new_word:
                print(f"Word {new_word} found with starting positions: {comb}")
                return {
                    "StartingPos": comb,
                    "Output": new_word
                }


    # with open(OUPUT_PATH, "w") as f:
    #     data = json.dumps(result)
    #     f.write(data)

# ########################## CODE 3 ##########################

def code_break_3():
    print("Code Breaking: Code 3.")

    plugboard = Plugboard()
    plugboard.add(PlugLead("FH"))
    plugboard.add(PlugLead("TS"))
    plugboard.add(PlugLead("BE"))
    plugboard.add(PlugLead("UQ"))
    plugboard.add(PlugLead("KD"))
    plugboard.add(PlugLead("AL"))

    word = "ABSKJAKKMRITTNYURBJFWQGRSGNNYJSDRYLAPQWIAGKJYEPCTAGDCTHLCDRZRFZHKNRSDLNPFPEBVESHPY"

    AVAILABLE_ROTORS = ["II", "IV", "Beta", "Gamma"]
    AVALABLE_RING_SETTINGS = [n+1 for n in range(26) if all(int(x) % 2 == 0 for x in str(n+1))]

    # rotor_combs = product(AVAILABLE_ROTORS, repeat=3)
    # ring_combs = product(AVALABLE_RING_SETTINGS, repeat=3)

    # OUPUT_PATH = "combinations_results_3.json"
    # result = {}

    for rotor_comb in product(AVAILABLE_ROTORS, repeat=3):

        rotor_comb = list(rotor_comb)

        # result[" ".join(rotor_comb)] = {}

        for reflector in ["A", "B", "C"]:

            # result[" ".join(rotor_comb)][reflector] = {}

            for ring_comb in product(AVALABLE_RING_SETTINGS, repeat=3):

                ring_comb = list(ring_comb)

                enigma = EnigmaMachine(
                        rotors=[Rotor(rotor_comb[0],"E",ring_comb[0]), Rotor(rotor_comb[1],"M",ring_comb[1]), Rotor(rotor_comb[2],"Y",ring_comb[2])],
                        reflector=Rotor(reflector,"A",1),
                        plugboard=plugboard
                    )
            
                enigma._init_rotors()

                new_word = ""
                for w in word:

                    new_w = enigma.encode_character(w)
                    new_word += new_w

                if "THOUSANDS" in new_word:
                    print(f"Word {new_word} found with Rotors: {rotor_comb}, Reflector: {reflector}, and RingSettings: {ring_comb}.")
                    return {
                        "Rotors": rotor_comb,
                        "Reflector": reflector,
                        "RingSettings": ring_comb,
                        "Output": new_word
                    }
                # result[" ".join(rotor_comb)][reflector][" ".join([str(e) for e in ring_comb])] = new_word

        # with open(OUPUT_PATH, "w") as f:
        #     data = json.dumps(result)
        #     f.write(data)

# ########################## CODE 4 ##########################

def code_break_4():
    print("Code Breaking: Code 4.")

    def _init_plugboard_4():
        plugboard = Plugboard()
        plugboard.add(PlugLead("WP"))
        plugboard.add(PlugLead("RJ"))
        plugboard.add(PlugLead("VF"))
        plugboard.add(PlugLead("HN"))
        plugboard.add(PlugLead("CG"))
        plugboard.add(PlugLead("BS"))

        return plugboard

    word = "SDNTVTPHRBNWTLMZTQKZGADDQYPFNHBPNHCQGBGMZPZLUAVGDQVYRBFYYEIXQWVTHXGNW"

    AVAILABLE_PLUGS = list(set(LABELS) - set(["A", "I"]) - set("WPRJVFHNCGBS"))

    # rotor_combs = product(AVAILABLE_ROTORS, repeat=3)
    # ring_combs = product(AVALABLE_RING_SETTINGS, repeat=3)

    # OUPUT_PATH = "combinations_results_4.json"
    # result = {}

    for plug in AVAILABLE_PLUGS:

        for second_plug in AVAILABLE_PLUGS:

            if second_plug == plug:
                continue
            
            plugboard = _init_plugboard_4()
            plugboard.add(PlugLead(f"A{plug}"))
            plugboard.add(PlugLead(f"I{second_plug}"))
            

            enigma = EnigmaMachine(
                    rotors=[Rotor("V","S",24), Rotor("III","W",12), Rotor("IV","U",10)],
                    reflector=Rotor("A","A",1),
                    plugboard=plugboard
                )

            enigma._init_rotors()

            new_word = ""
            for w in word:

                new_w = enigma.encode_character(w)
                new_word += new_w

            possible_answer = []
            if "TUTOR" in new_word:
                    print(f"Word {new_word} found with first PlugLead: A{plug}, and second PlugLeaf: I{second_plug}.")
                    possible_answer.append({
                        "First PlugLead": f"A{plug}",
                        "Second PlugLead": f"I{second_plug}",
                        "Output": new_word
                    })

    return possible_answer
            # result[f"A{plug}, I{second_plug}"] = new_word

    # with open(OUPUT_PATH, "w") as f:
    #     data = json.dumps(result)
    #     f.write(data)

########################## CODE 5 ##########################

def code_break_5():
    print("Code Breaking: Code 5.")

    #New dictionary containing the old rotor patterns
    OLD_PATTERNS = {
        "A": PATTERNS.get("A"),
        "B": PATTERNS.get("B"),
        "C": PATTERNS.get("C"),
    }

    #Word to decode
    word = "HWREISXLGTTBYVXRCWWJAKZDTVZWKBDJPVQYNEQIOTIFX"

    #List of possible social media
    social_media = ["FACEBOOK", "INSTAGRAM", "GOOGLE", "SNAPCHAT", "LINKEDIN"]

    #Plugboard initialization
    plugboard = Plugboard()
    plugboard.add(PlugLead("UG"))
    plugboard.add(PlugLead("IE"))
    plugboard.add(PlugLead("PO"))
    plugboard.add(PlugLead("NX"))
    plugboard.add(PlugLead("WT"))


    def get_wires(refl):
        """From the 26 mappings, it returns 13 wires as tuples."""

        seen, wires = set(), []
        for k, v in refl.items():
            if k not in seen:
                wires.append((k, v))
                seen.update([k, v])
        return wires

    def recombine(w1, w2):
        """It swaps the end of two wires and returns the two possible rewiring configurations."""

        (a, b), (c, d) = w1, w2
        return [((a, c), (b, d)),
                ((a, d), (b, c))]

    def build_reflector(base_wires, touched_idx, new_pairs):
        """It re-builds the new reflector with the new pairs."""

        d = {}
        for i, (x, y) in enumerate(base_wires):
            if i not in touched_idx:
                d[x] = y
                d[y] = x
        for (x, y) in new_pairs:
            d[x] = y
            d[y] = x
        return d

    def candidate_reflectors(base_name):
        """It yelds a possible reflector configuration to test."""

        wires = get_wires(OLD_PATTERNS[base_name])
        for four in combinations(range(13), 4):
            a, b, c, d = four

            for (i, j), (k, l) in [((a, b), (c, d)),
                                ((a, c), (b, d)),
                                ((a, d), (b, c))]:
                for new1 in recombine(wires[i], wires[j]):
                    for new2 in recombine(wires[k], wires[l]):
                        yield build_reflector(wires, set(four), new1 + new2), new1, new2

    def find_refector_conf():
        """Functinon to test new reflector configurations."""

        for reflector in ["A", "B", "C"]:
            for refl_dict, new1, new2 in candidate_reflectors(reflector):

                PATTERNS["CUSTOM"] = refl_dict

                enigma = EnigmaMachine(
                    rotors=[Rotor("V","A",6), Rotor("II","J",18), Rotor("IV","L",7)],
                    reflector=Rotor("CUSTOM","A",1),
                    plugboard=plugboard,
                )

                enigma._init_rotors()

                out = "".join(enigma.encode_character(c) for c in word)
                if any(s in out for s in social_media):
                    print(f"""
Word {out} found with Reflector: {reflector} with the following modifications:\n
- {new1};
- {new2}.\n
The resultant New Reflector is: \n
{refl_dict}
                        """)
                    return {
                        "Reflector": reflector,
                        "FirstModification": new1,
                        "SecondModification": new2,
                        "NewReflector": refl_dict,
                        "Output": out
                    }
                
    return find_refector_conf()

if __name__ == "__main__":

    print(" ")
    print("#"*100)
    code_break_1()

    print("#"*100)
    print(" ")
    
    print("#"*100)
    code_break_2()

    print("#"*100)
    print(" ")
    
    print("#"*100)
    code_break_3()

    print("#"*100)
    print(" ")
    
    print("#"*100)
    for answ in code_break_4():
        print("Possible Answers\n")
        print(answ)

    print("#"*100)
    print(" ")
    
    print("#"*100)
    code_break_5()
    print("#"*100)