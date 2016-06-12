import assemble
import mono_score_generator

if __name__ == '__main__':
	meas_num = 100
	mono_score_generator.generate_score_files(meas_num)
	assemble.generate_label(meas_num)
