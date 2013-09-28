import sys
from struct import *
from util import *

class bread(object):
	def __init__(self, fp):
		self.fp = fp

	def int32(self):
		return unpack('<l', self.fp.read(4))[0]

	def single(self):
		return unpack('<f', self.fp.read(4))[0]

	def str(self):
		return self.fp.read(ord(self.fp.read(1)))

	def peekchr(self):
		data = self.fp.read(1)
		if len(data) == 0:
			return -1
		c = unpack('B', data)
		self.fp.seek(-1, 1)
		return c

	def bool(self):
		return ord(self.fp.read(1)) != 0

def readChild(br, transforms=None):
	if transforms is None:
		transforms = []
	ignore = 'fairing', 'canopy'
	name = br.str()
	pos = (br.single(), br.single(), br.single())
	rot = (br.single(), br.single(), br.single(), br.single())
	scale = (br.single(), br.single(), br.single())
	transforms = [(pos, rot, scale)] + transforms

	meshes = []

	#print 'CHILD', name, pos, rot, scale
	while br.peekchr() != -1:
		type = br.int32()
		#print type, '%08x' % type
		if type == 0:
			meshes += readChild(br, transforms)
		elif type == 1:
			#print 'returning game object'
			if name in ignore:
				return []
			return meshes
		elif type == 2:
			readAnimation(br)
		elif type == 7:
			meshes.append((transforms, readMesh(br))) # shared mesh?
		elif type == 8:
			readMeshRenderer(br)
		elif type == 10:
			num = br.int32()
			for i in xrange(num):
				readMaterial(br)
		elif type == 12:
			readTextures(br)
		elif type == 24:
			readTagAndLayer(br)
		elif type == 25: # collision mesh
			trigger = br.bool()
			convex = br.bool()
			mesh = readMesh(br)
		elif type == 27: # capsule collider
			trigger = br.bool()
			radius = br.single()
			height = br.single()
			dir = br.int32()
			center = br.single(), br.single(), br.single()
		elif type > 31:
			continue
		else:
			print 'foo -- unknown', type
			sys.exit(1)

	if name in ignore:
		return []
	return meshes

def readTagAndLayer(br):
	tag, layer = br.str(), br.int32()
	#print 'tag and layer', tag, layer

def readMesh(br):
	verts = []
	inds = []
	entrytype = br.int32()
	assert entrytype == 13 # meshstart

	num, num2 = br.int32(), br.int32()
	num3 = 0
	while True:
		entrytype = br.int32()
		if entrytype == 22: # meshend
			break
		elif entrytype == 14: # meshverts
			verts.append([(br.single(), br.single(), br.single()) for i in xrange(num)])
		elif entrytype == 15: # meshuv
			uv = [(br.single(), br.single()) for i in xrange(num)]
		elif entrytype == 16: # meshuv2
			uv2 = [(br.single(), br.single()) for i in xrange(num)]
		elif entrytype == 17: # meshnormals
			normals = [(br.single(), br.single(), br.single()) for i in xrange(num)]
		elif entrytype == 18: # meshtangents
			tangents = [(br.single(), br.single(), br.single(), br.single()) for i in xrange(num)]
		elif entrytype == 19: # meshtriangles
			num4 = br.int32()
			inds.append([br.int32() for i in xrange(num4)])
		else:
			print entrytype
			assert False

	return verts, inds

def readMeshRenderer(br):
	if soh >= 1:
		castShadows = br.bool()
		receiveShadows = br.bool()

	num = br.int32()
	for i in xrange(num):
		j = br.int32()

def readMaterial(br):
	name = br.str()
	#print 'material named', name

	type = br.int32()
	#print 'material type', type
	if type == 1:
		readMaterialTexture(br)
	elif type == 2:
		material = readMaterialTexture(br)
		color = readColor(br)
		float = br.single()
	elif type == 3:
		first = readMaterialTexture(br)
		second = readMaterialTexture(br)
	elif type == 4:
		first = readMaterialTexture(br)
		second = readMaterialTexture(br)
		color = readColor(br)
		float = br.single()
	elif type == 5:
		first = readMaterialTexture(br)
		second = readMaterialTexture(br)
		color = readColor(br)
	elif type == 6:
		first = readMaterialTexture(br)
		color = readColor(br)
		float = br.single()
		second = readMaterialTexture(br)
		color2 = readColor(br)
	elif type == 7:
		first = readMaterialTexture(br)
		second = readMaterialTexture(br)
		color = readColor(br)
		float = br.single()
		third = readMaterialTexture(br)
		color2 = readColor(br)
	elif type == 13:
		first = readMaterialTexture(br)
		color = readColor(br)
	else:
		print 'foo', type
		assert False

def readMaterialTexture(br):
	unk = br.int32()
	scale = br.single(), br.single()
	offset = br.single(), br.single()

def readColor(br):
	return br.single(), br.single(), br.single(), br.single()

def readTextures(br):
	num = br.int32()
	for i in xrange(num):
		text = br.str()
		type = br.int32()
		#print text, type

def readAnimation(br):
	num = br.int32()
	for i in xrange(num):
		text = br.str()
		#print 'animation', text
		bounds = (br.single(), br.single(), br.single()), (br.single(), br.single(), br.single())
		wrapmode = br.int32()
		num2 = br.int32()
		for j in xrange(num2):
			text2 = br.str()
			text3 = br.str()
			#print 'keyframe', `text2`, `text3`
			type = br.int32()
			prewrap = br.int32()
			postwrap = br.int32()
			num3 = br.int32()
			for k in xrange(num3):
				time = br.single()
				value = br.single()
				itangent = br.single()
				otangent = br.single()
				tanmode = br.int32()
	text4 = br.str()
	#print 'unknown', `text4`
	auto = br.bool()

def load(fn):
	global soh

	br = bread(file(fn, 'rb'))

	assert br.int32() == 0x00012AFF
	soh = br.int32()
	name = br.str()

	meshes = readChild(br)

	av = []
	ai = []
	for transforms, (verts, inds) in meshes:
		assert len(verts) == 1
		assert len(inds) == 1
		verts = verts[0]
		for i, t in enumerate(transforms):
			print i, t
		step = 1
		for pos, rot, size in transforms[::step]:
			verts = scale(verts, size[0], size[1], size[2])
			verts = translate(verts, pos[0], pos[1], pos[2])
			verts = qrotate(verts, *rot)
		off = len(av)
		av += verts
		ai += [ind+off for ind in inds[0]]

	assert (len(ai) % 3) == 0
	inds = list(group(ai, 3))
	normals = gennormals(av, inds)

	return av, inds, normals
