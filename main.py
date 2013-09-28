import craft, stl
import commands, sys
from util import *

def main(fn):
	parts = craft.load(fn)

	verts, inds, normals = [], [], []

	for pos, rot, (_v, _i, _n) in parts:
		off = len(verts)
		_v = translate(_v, pos[0], pos[1], pos[2])
		_v = qrotate(_v, *rot)
		verts += _v
		inds += [tuple(j + off for j in i) for i in _i]
		normals += _n

	verts = swapyz(scale(verts, 20))
	inds = swapwinding(inds)

	bottom = None
	for (_, __, z) in verts:
		if bottom is None or z < bottom:
			bottom = z

	verts = translate(verts, 0, 0, -bottom)

	with file(fn + '.stl', 'w') as fp:
		stl.write(fp, fn.split('/')[-1], verts, inds, normals)

	commands.getoutput('open %s.stl' % fn)

if __name__=='__main__':
	main(*sys.argv[1:])
