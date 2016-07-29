
data_path = 'data_new/'

model_path = 'model/'

const_rows = 80

const_cols = 200

# 16 + 1 rhythm labels
rhythm_label_num = 17
# none, natural, sharp, flat (not used for now)
pitch_label_num = 4

min_note_frames = 3

pitch_dict = {'C': 0, 'D': 1, 'E': 2, 'F': 3, 'G': 4, 'A': 5, 'B': 6}

pitch_shift = 62

pitch_max_num = 30 #pitch label ranges from 0 to num - 1, 0 represents no pitch