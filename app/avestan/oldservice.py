from app.avestan.alphabet import (
    avestan_to_latin_alphabet,
    avestan_sequences,
    avestant_letters,
    latin_to_avestan_alphabet,
    latin_sequences,
    latin_letters,
)

def from_avestan_script(provided: str, system: str) -> str:
    sequence_indexes = []
    invalid_chars = []
    transliterated = []

    for seq in avestan_sequences:
        if seq in provided:
            sequence_indexes.append(provided.index(seq))

    for i, c in enumerate(provided):
        to_be_added = ""
        if c not in avestant_letters:
            invalid_chars.append(c)
        if i in sequence_indexes:
            to_be_added = avestan_to_latin_alphabet[f"{c}{provided[i+1]}"][system]
        elif i - 1 in sequence_indexes:
            pass
        else:
            to_be_added = avestan_to_latin_alphabet[c][system]

        if system == "ipa":
            to_be_added = to_be_added[1:-1]
        transliterated.append(to_be_added)

    if invalid_chars:
        raise Exception("SHEEET: " + ",".join(ic for ic in invalid_chars))

    return "".join(transliterated)[::-1] if system != "ipa" else "/" + "".join(transliterated) + "/"


def from_latin_script(provided: str) -> str:
    sequence_indexes = []
    invalid_chars = []
    transliterated = []

    for seq in latin_sequences:
        if seq in provided:
            sequence_indexes.append(provided.index(seq))

    for i, c in enumerate(provided.lower()):
        to_be_added = ""
        if c not in latin_letters:
            invalid_chars.append(c)
        if i in sequence_indexes:
            to_be_added = latin_to_avestan_alphabet[f"{c}{provided[i+1]}"]
        elif i - 1 in sequence_indexes:
            pass
        else:
            to_be_added = latin_to_avestan_alphabet[c]

        transliterated.append(to_be_added)

    if invalid_chars:
        raise Exception("SHEEET: " + ",".join(ic for ic in invalid_chars))

    return "".join(transliterated)[::-1]

print(from_avestan_script(provided="𐬀𐬢𐬭𐬀", system="hoffmann"))
print(from_avestan_script(provided="𐬘𐬈𐬲𐬛𐬥𐬀", system="hoffmann"))
print("𐬘𐬈𐬰𐬭𐬛𐬥𐬀")

print(from_latin_script(provided="vaŋuhī"))
print(from_latin_script(provided="xšapā"))
