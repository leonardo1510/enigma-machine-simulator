# Enigma Machine Simulator

An object-oriented Python simulation of the Enigma machine (plugboard, rotors, reflector, ring settings, turnover and double-stepping), plus a set of crib-based brute-force routines that break five Enigma-encrypted messages.

## Contents

| File | Description |
|---|---|
| `enigma.py` | The simulator: `PlugLead`, `Plugboard`, `Rotor`, `EnigmaMachine`. |
| `code_breaking.py` | Five brute-force routines (`code_break_1` ... `code_break_5`) that recover the missing machine settings. |
| `enigma.ipynb` | Walkthrough of the machine, sanity checks, and the code-breaking results. |

## The simulator

* **`PlugLead("AG")`** connects two letters (in both directions); invalid leads (e.g. `"AA"`) raise an error.
* **`Plugboard`** holds up to 10 leads (`add(...)`) and encodes a character through them.
* **`Rotor(pattern, position, ring_setting)`** supports the wirings `I`-`V`, `Beta`, `Gamma` and the reflectors `A`, `B`, `C`.
* **`EnigmaMachine(rotors, reflector, plugboard)`** supports 3 or 4 rotors, rotor turnover (including the double step) and encodes whole strings; the same call encodes and decodes.

```python
from enigma import *

plugboard = Plugboard()
for pair in ["HL", "MO", "AJ", "CX", "BZ", "SR", "NI", "YW", "DG", "PK"]:
    plugboard.add(PlugLead(pair))

machine = EnigmaMachine(
    rotors=[Rotor("I", "A", 1), Rotor("II", "A", 1), Rotor("III", "Z", 1)],  # (wiring, start position, ring setting)
    reflector=Rotor("B", "A", 1),
    plugboard=plugboard,
)
machine._init_rotors()
print("".join(machine.encode_character(c) for c in "HELLOWORLD"))  # RFKTMBXVVW
```

### Logging
The module uses Python's standard `logging`: `WARNING` (default) reports unexpected conditions such as a full plugboard or duplicate leads, `INFO` records machine set-up, and `DEBUG` gives per-character encoding traces. Change the level in the `logging.basicConfig` call in `enigma.py`.

## Code breaking

Each message comes with a crib (a word expected in the plaintext) and partial knowledge of the settings. The missing part is brute-forced and a candidate is accepted when its decryption contains the crib.

| Code | Unknown | Search space | Recovered |
|---|---|---|---|
| 1 | Reflector | `A`, `B`, `C` | Reflector `C` |
| 2 | Starting positions | 26^3 | `I M G` |
| 3 | Rotors, reflector, ring settings | even-numbered rotors and even ring settings only | Rotors `II Gamma IV`, reflector `C`, ring settings `24 8 20` |
| 4 | Two plug leads (`A?`, `I?`) | 25 x 25 | `AT` and `IK` |
| 5 | Reflector with two rewired wire pairs | every way of swapping the ends of two pairs of wires in `A`, `B`, `C` | Reflector `B` with `A-P, Y-I` and `B-Q, R-E` |

Running the script prints every decrypted message and the settings found (a few seconds in total):

```bash
python code_breaking.py
```

Some functions contain commented-out blocks showing how all candidates can be dumped to JSON files to inspect the whole search space.

## Running

Requires Python 3.8+ and no third-party packages for the simulator. To open the notebook:

```bash
pip install -r requirements.txt
jupyter notebook enigma.ipynb
```

## License
MIT
