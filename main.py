from music21 import *
from mode_rules import mode_rules

us = environment.UserSettings()
us['lilypondPath'] = r"C:/LilyPond/bin/lilypond.exe"

#Get file name
file_name = input("What is the file called?\n")

score = converter.parse(file_name+".mxl")

# What key they want/already have
tonic = input("What is the major key signature\n")

target_mode = input("What mode do you want to change to?\n")




#Function for rules for changing
def change_mode(score, tonic, target_mode,):
    #Rules for each key(kinda)
    rules = mode_rules.get(tonic, {}).get(target_mode, {})


    #Loops through all the piece
    for n in score.recurse().notes:
        #Replaces notes
        if isinstance(n, note.Note):
            step = n.pitch.step
            n.pitch.accidental = None
            if step in rules:
                n.pitch = pitch.Pitch(rules[step] + str(n.pitch.octave))

           #Replaces chords to not break!
        elif isinstance(n, chord.Chord):
            for p in n.pitches:
                step = p.step
                p.accidental = None
                if step in rules:
                    # Update pitch in-place

                    new_pitch = pitch.Pitch(rules[step] + str(p.octave))
                    p.name = new_pitch.name
                    p.octave = new_pitch.octave
    return score


if __name__ == "__main__":
    # Load the sheet music


    # Change the mode
    changed = change_mode(score, tonic, target_mode)

    tempo_mark = tempo.MetronomeMark(number=60)
    changed.append(tempo_mark)

    new_key = key.KeySignature(0)

    for part in changed.parts:
        # Try measure 0 first (pickup), fallback to measure 1
        first_measure = part.measure(0)
        if first_measure is None:
            first_measure = part.measure(1)
        if first_measure is not None:
            first_measure.insert(0, new_key)


    # Save the result as
    #changed.write("musicxml", file_name + target_mode + "_version.mxl")
    changed.show('lily.pdf')
    changed.show('midi')
    #Success Output
    print("Enjoy!\n")