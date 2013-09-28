import cfg
from part import PartLoader

def load(fn):
	parts = []
	craft = cfg.read(fn)
	for part in craft['PART']:
		type = part['part'].rsplit('_', 1)[0]
		print type
		model = PartLoader.getPart(type)
		if model == None:
			continue

		pos = map(float, part['pos'].split(','))
		rot = map(float, part['rot'].split(','))

		parts.append((pos, rot, model))

	return parts

if __name__=='__main__':
	import sys
	load(sys.argv[1])
