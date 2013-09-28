from math import *
from vectors import *

class vec3(object):
	def __init__(self, x=0.0, y=None, z=None):
		if isinstance(x, tuple) or isinstance(x, list):
			x, y, z = map(float, x)
		else:
			x = float(x)
			if y is None:
				y = z = x

		self.x, self.y, self.z = x, y, z

	@staticmethod
	def __from__(obj):
		if isinstance(obj, vec3):
			return obj
		else:
			return vec3(obj)

	def __add__(self, b):
		b = vec3.__from__(b)
		return vec3(self.x + b.x, self.y + b.y, self.z + b.z)

	def __sub__(self, b):
		b = vec3.__from__(b)
		return vec3(self.x - b.x, self.y - b.y, self.z - b.z)

	def __mul__(self, b):
		b = vec3.__from__(b)
		return vec3(self.x * b.x, self.y * b.y, self.z * b.z)

	def __div__(self, b):
		b = vec3.__div__(b)
		return vec3(self.x / b.x, self.y / b.y, self.z / b.z)

def swapyz(vertices):
	return [(x, z, y) for (x, y, z) in vertices]

def translate(vertices, tx, ty, tz):
	return [(x+tx, y+ty, z+tz) for (x, y, z) in vertices]

def scale(vertices, sx, sy=None, sz=None):
	if sy is None:
		sy = sz = sx

	return [(x*sx, y*sy, z*sz) for (x, y, z) in vertices]

def qrotate(vertices, rx, ry, rz, rw):
	return [qv_mult((rw, rx, ry, rz), (x, y, z)) for (x, y, z) in vertices]

def dist(a, b):
	return sqrt((a[0]-b[0])**2 + (a[1]-b[1])**2 + (a[2]-b[2])**2)

def group(iter, count):
	iter = iter.__iter__()
	while True:
		temp = []
		for i in xrange(count):
			temp.append(iter.next())
		yield tuple(temp)

def gennormals(vertices, indices):
	normals = []
	vertices = map(vec3, vertices)

	for i, j, k in indices:
		u = vertices[j] - vertices[i]
		v = vertices[k] - vertices[i]
		normals.append((
			u.y*v.z - u.x*v.y, 
			u.z*v.x - u.x*v.z, 
			u.x*v.y - u.y*v.x
		))

	return normals

def swapwinding(indices):
	return [(j, i, k) for (i, j, k) in indices]

eps = 0.000000001
