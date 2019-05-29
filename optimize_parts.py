#!/usr/bin/env python3

import os, sys, re, shutil, glob

if len(sys.argv) < 2:
	sys.exit((
		"\nUsage: optimize_parts output_path\n"
		"Optimize each LDraw part in this script's directory then put the result in 'output_path'\n"
	))

os.chdir('./')
outpath = sys.argv[1]

if not os.path.isdir(outpath):
	os.mkdir(outpath)

for fn in glob.glob(os.path.join(outpath, '*')):
	os.remove(fn)

shutil.copyfile('LDConfig.ldr', os.path.join(outpath, 'LDConfig.ldr'))
shutil.copyfile('LDConfig_lic.ldr', os.path.join(outpath, 'LDConfig_lic.ldr'))
os.mkdir(os.path.join(outpath, 'parts'))
os.mkdir(os.path.join(outpath, 'parts', 's'))
os.mkdir(os.path.join(outpath, 'parts', '8'))
os.mkdir(os.path.join(outpath, 'parts', '48'))

trimWhitespace = re.compile('\n\ns+')

for idx, fn in enumerate(glob.glob('parts/**', recursive=True)):
	try:
		if os.path.isdir(fn):
			continue
		lines = []
		if idx % 100 == 0:
			print('.', end='')
		with open(fn, encoding='utf-8') as f:
			for i, line in enumerate(f):
				line = re.sub(trimWhitespace, ' ', line).strip()
				if line.startswith('0 !HISTORY') or line.startswith('0 !LDRAW') or len(line) < 3:
					continue
				lines.append(line + '\n')

		with open(os.path.join(outpath, fn), 'w', encoding='utf-8') as f:
			f.writelines(lines)
	except:
		print('\n**Failed to fix file:', fn)
		print('error:' , sys.exc_info()[0])
		print('value:' , sys.exc_info()[1])
		print('stack:' , sys.exc_info()[2])
