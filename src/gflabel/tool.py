import subprocess

label_base = ["pred", "predbox", "plain", "cullenect", "modern", "none"]
label_style = ["", "embossed", "debossed", "embedded"]
antrieb = ["spax", "torx"]
schraubenkopf = ["hex", "countersunk", "panhead", "socket", "button", "round", "flat"]
dateiendung = ["svg", "stl"]

_daten = {}

_schraubenkopf = schraubenkopf[1]  # "countersunk"
_label_base = label_base[3]        # "cullenect"
_antrieb = ""
_label_style = label_style[1]      # "embossed"

_width = 36
# while True:
#     try:
#         index = int(input("Enter width in mm: "))
#         if 0 <= index < 100:
#             _width = index
#             break
#         else:
#             print("Invalid size, 0-100 possible")
#     except ValueError:
#         print("Invalid size, 0-100 possible.")
        
_height = 11
# while True:
#     try:
#         index = int(input("Enter width in mm: "))
#         if 0 <= index < 100:
#             _height = index
#             break
#         else:
#             print("Invalid size, 0-100 possible")
#     except ValueError:
#         print("Invalid size, 0-100 possible.")

#_label_base = input("Enter Label base: pred,predbox,plain,cullenect,modern,none")
#while True:
eingabe = input("Enter Label base: pred,predbox,plain,cullenect,modern,none (default): ")
if eingabe in label_base:
    _label_base = eingabe
#elif not input:
#    _label_base = none
#        break
    #else:
    #    print("Invalid parameter, please use: pred, predbox, plain, cullenect, modern, none (default)")

# head
#while True:
eingabe = input("Enter head type: hex, countersunk (default), panhead, socket, button, round, flat: ")
if eingabe in schraubenkopf:
    _schraubenkopf = eingabe
#        break
#elif not input:
#    _schraubenkopf = "countersunk"
    #else:
    #    print("Invalid parameter, please use: hex, countersunk (default), panhead, socket, button, round, flat")

# Read input file
with open("liste.txt", "r", encoding="utf-8") as f:
    for line in f:
        line = line.strip()
        if line:
            _daten[line] = "VZ"

# Process each item
def build_and_run_command():
    for key, value in _daten.items():
        einheiten = key.split(',')

        if einheiten[0] == "HD-20":
            _antrieb = "torx"
        elif einheiten[0] in ("TX-20", "TX-25"):
            _antrieb = "spax"
        else:
            _antrieb = "torx"

        schraub = einheiten[1].split('x')
        durch = schraub[0]
        lang = schraub[1]

        dateiname = f"{_antrieb[0]}{einheiten[1]}."

        __label_base = f"{_label_base}" if _label_style else ""
        __label_style = f"--style {_label_style}" if _label_style else ""
        __width = f"--width {_width}mm" if _width else ""
        __height = f"--height {_height}mm" if _height else ""

        if _label_base == "cullenect":
            befehl = (
                f"gflabel {__label_base} {__label_style} "
                f"\"{{head({_antrieb})}}\\n{{medium({einheiten[0]})}} {{60|100}} {{bolt({lang},{_schraubenkopf})}}\\n {einheiten[1]} {{small({value})}}\" "
                f"-o out\\{dateiname}{dateiendung[0]} -o out\\{dateiname}{dateiendung[1]}"
        )
        else:
            befehl = (
                f"gflabel {__label_base} {__label_style} {__width} {__height} "
                f"\"{{head({_antrieb})}}\\n{{medium({einheiten[0]})}} {{60|100}} {{bolt({lang},{_schraubenkopf})}}\\n {einheiten[1]} {{small({value})}}\" "
                f"-o out\\{dateiname}{dateiendung[0]} -o out\\{dateiname}{dateiendung[1]}"
        )
#gflabel cullenect  "{head(torx)}\n{smedium(HD-20)} {60|100}{bolt(70,countersunk)}\n5,0x70 {small(VZ)}" -o t5.0x70.svg

        subprocess.run(befehl, shell=True)


if __name__ == "__main__":
    build_and_run_command()
