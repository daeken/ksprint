import json, os
import cfg, mu
from util import *

class PartLoader(object):
	def __init__(self):
		self.loaded = {}
		self.reloaded = False
		self.loadCache()

	def loadCache(self):
		if not os.path.exists('parts.cache'):
			self.reload()
			return
		self.parts = json.loads(file('parts.cache').read())

	def reload(self):
		if self.reloaded:
			return
		self.reloaded = True
		self.parts = {}

		dirs = os.walk('gamedata')
		for path, dirs, fns in dirs:
			if 'part.cfg' in fns:
				self.addPart(path)

		self.saveCache()

	def saveCache(self):
		with file('parts.cache', 'w') as fp:
			fp.write(json.dumps(self.parts))

	def addPart(self, path):
		data = cfg.read(path + '/part.cfg')
		if 'PART' not in data:
			print data
			print 'skipping'
			return

		part = data['PART'][0]
		name = part['name']
		model = path + '/' + part['mesh']
		if 'rescaleFactor' in part:
			scale = float(part['rescaleFactor'])
		else:
			scale = 1.0

		self.parts[name] = model, scale

	def getPart(self, name):
		if name in self.loaded:
			return self.loaded[name]

		if name not in self.parts:
			self.reload()
			if name not in self.parts:
				print 'Part not found:', name
				return None

		model, rescale = self.parts[name]
		verts, indices, normals = mu.load(model)
		if rescale != 1.0:
			verts = scale(verts, rescale)

		self.loaded[name] = verts, indices, normals

		return verts, indices, normals
PartLoader = PartLoader()
