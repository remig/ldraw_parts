#!/usr/bin/env python3

import os, sys, re, shutil, glob
from pathlib import Path

j = os.path.join

if len(sys.argv) < 2:
	sys.exit((
		"\nUsage: optimize_parts input_ldraw_lib_path\n"
		"Optimize each LDraw part in the specified `input_ldraw_lib_path` folder then put the result in this repo's local `parts` folder\n"
	))

os.chdir('./')
inLdrawPath = sys.argv[1]
outpath = './parts_new'

if not os.path.isdir(inLdrawPath):
	print(f'error: specified LDraw path {inLdrawPath} does not exist')
elif not os.path.isdir(j(inLdrawPath, 'parts')):
	print(f'error: specified LDraw path {inLdrawPath} does not contain necessary"parts" folder')
elif not os.path.isdir(j(inLdrawPath, 'p')):
	print(f'error: specified LDraw path {inLdrawPath} does not contain necessary "p" folder')

for fn in glob.glob(j(outpath, '*')):
	if not os.path.isdir(fn):
		os.remove(fn)

shutil.copyfile(j(inLdrawPath, 'LDConfig.ldr'), "LDConfig_original.ldr")

Path(outpath).mkdir(exist_ok=True)
Path(j(outpath, 's')).mkdir(exist_ok=True)
Path(j(outpath, '8')).mkdir(exist_ok=True)
Path(j(outpath, '48')).mkdir(exist_ok=True)

trimWhitespace = re.compile('\n\ns+')
trimComments = re.compile('//.*$')

def fixOneFile(idx, fullFn, fn):
	try:
		if os.path.isdir(fullFn):
			return
		lines = []
		if idx % 100 == 0:
			print('.', end='')
		with open(fullFn, encoding='utf-8') as f:
			for line in f:
				line = re.sub(trimComments, '', line)
				line = re.sub(trimWhitespace, ' ', line).strip()
				if line.startswith('0 !HISTORY') or line.startswith('0 !LDRAW') or len(line) < 3:
					continue
				lines.append(line + '\n')

		with open(j(outpath, fn), 'w', encoding='utf-8') as f:
			f.writelines(lines)
	except:
		print('\n**Failed to fix file:', fullFn)
		print('error:' , sys.exc_info()[0])
		print('value:' , sys.exc_info()[1])
		print('stack:' , sys.exc_info()[2])

for idx, fn in enumerate(glob.glob(j(inLdrawPath, 'p/**'), recursive=True)):
	if fn.endswith('png'):
		continue
	fixOneFile(idx, fn, re.sub('^.*/p/', '', fn))

for idx, fn in enumerate(glob.glob(j(inLdrawPath, 'parts/**'), recursive=True)):
	if fn.endswith('png'):
		continue
	fixOneFile(idx, fn, re.sub('^.*/parts/', '', fn))

