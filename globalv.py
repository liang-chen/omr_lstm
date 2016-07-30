
data_path = 'data_new/'

model_path = 'model/'

const_rows = 80

const_cols = 200

# 16 + 1 rhythm labels
rhythm_label_num = 17

dur_max_num = 16
legitimate_dur = [1,2,3,4,6,8,12,16]
rhythmToDur = {0:0, 1:1, 2:2, 3:3, 4:4, 5:6, 6:8, 7:12, 8:16, 9:1, 10:2, 11:3, 12:4, 13:6, 14:8, 15:12, 16:16}
DurToRhythm = {0:0, 1:1, 2:2, 3:3, 4:4, 6:5, 8:6, 12:7, 16:8}
DurToRest = {0:0, 1:9, 2:10, 3:11, 4:12, 6:13, 8:14, 12:15, 16:16}

# none, natural, sharp, flat (not used for now)
pitch_label_num = 4

min_note_frames = 1

pitch_dict = {'C': 0, 'D': 2, 'E': 4, 'F': 5, 'G': 7, 'A': 9, 'B': 11}

pitch_inverse_dict = {0: 'C', 2: 'D', 4: 'E', 5: 'F', 5: 'G', 7: 'A', 11: 'B'}

pitch_shift = 65 # pitch ranges from 66 - 96 (31 different ones)

pitch_max_num = 32 #pitch label ranges from 0 to num - 1, 0 represents no pitch