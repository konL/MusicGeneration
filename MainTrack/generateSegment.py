
#将segmentSpot的输出粘贴至等号后面，再减去第一个时间，就得到了一系列分割点
def preprocess(spotPartition):
    partitions =spotPartition
    for i in range(len(partitions)):
        partitions[i] -= partitions[0]
    return partitions

#分割midi
import pretty_midi
def splitMIDI(midi_name,spotPartion):


    midi_name = midi_name
    pm = pretty_midi.PrettyMIDI(midi_name + '.mid')
    partitions =preprocess(spotPartion)
    for partition in range(len(partitions)-1):
        start_time = partitions[partition]
        end_time = partitions[partition + 1]

        new_midi= pretty_midi.PrettyMIDI()
        for instr_num in range (len(pm.instruments)):
            instrument = (pm.instruments[instr_num])

            notes_velocity=[]
            notes_pitch=[]
            notes_start = []
            notes_end = []

        # 找出start_time之后的第一个音符编号记作note_num
            for start_note_num in range (len(instrument.notes)):
                note = instrument.notes[start_note_num]
                start = note.start
                if start >= start_time:
                    break

            for end_note_num in range (len(instrument.notes)):
                note = instrument.notes[end_note_num]
                end = note.end
                if end > end_time:
                    break
        #将原midi中，区间内的音符记下
            for k in range(start_note_num,end_note_num):
                note = instrument.notes[k]
                notes_pitch.append(note.pitch)
                notes_start.append(note.start)
                notes_end.append(note.end)
                notes_velocity.append(note.velocity)

            program = instrument.program
            is_drum = instrument.is_drum
            name = instrument.name
            inst = pretty_midi.Instrument(program=program, is_drum=is_drum, name=name)
            new_midi.instruments.append(inst)

        # 粘到新midi里
            for i in range (end_note_num - start_note_num):
                inst.notes.append(pretty_midi.Note(notes_velocity[i], notes_pitch[i], notes_start[i]-float(start_time), notes_end[i]-float(start_time)))

        new_midi.write('segmented part'+str(partition)+'.mid')


spotPartion = [0.0, 9.465704202651978, 13.404264211654663, 18.470292568206787, 23.992305755615234, 29.031289100646973, 34.557311058044434, 39.699891567230225, 46.48798394203186]#填入之前获得的分割点
#spotPArtion from segmentSpot
splitMIDI('data/0002',spotPartion)

