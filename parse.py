"""
Robert Kim
Python 3
"""

import csv
import os
import os.path as op
import shutil


def isFloat(s):
	try:
		float(s)
		return True
	except ValueError:
		return False


def main():
	homedir = op.dirname(op.abspath(__file__))
	indir = 'unsorted_data'
	outdir = 'sorted_data'
	os.makedirs(outdir, exist_ok=True)
	if not op.exists(outdir):
		os.makedirs(outdir)

	with open('QC.csv') as csvfile:
		reader = csv.DictReader(csvfile)
		header = reader.fieldnames
		csvarr = list(reader)

	flist = []
	for root, dirs, files in os.walk(op.join(homedir, indir), topdown=True):
		dirs[:] = [d for d in dirs if d not in ['py_output']]
		for f in [f for f in files if '._' not in f]:
			x = op.join(root, f).split(os.sep)

			if any(s in x for s in ['Female', 'Male']):
				for row in [row for row in csvarr if not isFloat(row['Subject'])]:
					subj = row['Subject'][0:2]
					if row['Subject'][-1] == 'F':
						sex = 'Female'
					else:
						sex = 'Male'

					if all([row['Group'] == x[-5], sex == x[-4], subj == x[-3], row['Filename'] == x[-1]]):
						flist.append([root, f])
			else:
				for row in csvarr:
					if all([row['Group'] == x[-4], row['Subject'] == x[-3], row['Filename'] == x[-1]]):
						flist.append([root, f])

	os.chdir(outdir)

	n = len(op.join(homedir, indir))
	for row in flist:
		newdir = row[0][n+1: ]
		os.makedirs(newdir, exist_ok=True)
		shutil.copyfile(op.join(*row), op.join(newdir, row[1]))
		print('COPYING {}'.format(op.join(*row)))

	checklist = []
	for root, dirs, files in os.walk(op.join(homedir, outdir)):
		for f in files:
			checklist.append(op.join(root, f))

	if len(flist) == len(checklist):
		print('SUCCESSFULLY COMPLETED')
	else:
		print('COMPLETED WITH ERRORS')


if __name__ == '__main__':
	main()
