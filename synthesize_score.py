import assemble
import mono_score_generator
import argparse

if __name__ == '__main__':
	meas_num = 10
	parser = argparse.ArgumentParser(description='Process some integers.')
	parser.add_argument('meas', metavar='N', type=int, nargs='+',
			                    help='number of measures')
	args = parser.parse_args()
	meas_num = args.meas[0]
	print "Synthesize",meas_num,"scores."
	mono_score_generator.generate_score_files(meas_num)
	assemble.generate_label(meas_num)
