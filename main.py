import streamlit as st
from music21 import converter, note, chord, pitch, key, tempo, environment, stream
from mode_rules import mode_rules
import tempfile
import io

us = environment.UserSettings()
us['lilypondPath'] = ''

st.title("Mode Changer")
st.write("Upload a MusicXML file and change its mode!")


#Get file name
uploaded_file = st.file_uploader("Choose a MusicXML file", type=["mxl", "musicxml"])
if uploaded_file:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mxl") as tmp:
        tmp.write(uploaded_file.read())
        tmp_path = tmp.name

    #User Input for Keys
    tonic = st.text_input("Enter the MAJOR key signature (e.g., 'C', 'G', 'D', etc.):")
    target_mode = st.text_input("Enter the mode to change to (e.g., 'Dorian', 'Mixolydian', etc.):")

    #Load the file
    try:
        score = converter.parse(tmp_path)
    except Exception as e:
        st.error(f"Error loading file: {e}")
        st.stop()




#Function for rules for changing
def change_mode(score, tonic, target_mode,):
    #Rules for each key(kinda)
    rules = mode_rules.get(tonic, {}).get(target_mode, {})


    #Loops through all the piece
    for n in score.recurse().notes:
        #Replaces notes
        if isinstance(n, note.Note):
            step = n.pitch.name
            
            if step in rules:
                n.pitch = pitch.Pitch(rules[step] + str(n.pitch.octave))

           #Replaces chords to not break!
        elif isinstance(n, chord.Chord):
            for p in n.pitches:
                step = p.name
                
                if step in rules:
                    # Update pitch in-place

                    new_pitch = pitch.Pitch(rules[step] + str(p.octave))
                    p.name = new_pitch.name
                    p.octave = new_pitch.octave
    return score


if st.button("Change Mode"):
        changed = change_mode(score, tonic, target_mode)

        # Add tempo mark
        tempo_mark = tempo.MetronomeMark(number=60)
        changed.append(tempo_mark)

        # Reset key signature visually
        new_key = key.KeySignature(0)
        for part in changed.parts:
            first_measure = part.measure(0) or part.measure(1)
            if first_measure:
                first_measure.insert(0, new_key)

        #Create MIDI output
        midi_bytes = io.BytesIO()
        mf = changed.write("midi")
        with open(mf, "rb") as f:
             midi_bytes.write(f.read())
        midi_bytes.seek(0)

        #Create MusicXML output
        xml_bytes = io.BytesIO()
        xml_path = changed.write("musicxml")
        with open(xml_path, "rb") as f:
            xml_bytes.write(f.read())
        xml_bytes.seek(0)

        st.success("Mode changed successfully!")
        st.download_button(
            label="Download Changed MIDI",
            data=midi_bytes,
            file_name= target_mode + " " + uploaded_file.name + ".midi",
            mime="audio/midi"
        )
        st.download_button(
            label="Download Changed MusicXML",
            data=xml_bytes,
            file_name= target_mode + " " + uploaded_file.name + ".musicxml",
            mime="application/vnd.recordare.musicxml+xml"
        )





