from util import *

def write(fp, name, vertices, indices, normals):
	print >>fp, 'solid', name

	for e, (i, j, k) in enumerate(indices):
		print >>fp, 'facet normal %f %f %f' % normals[e]
		print >>fp, 'outer loop'
		print >>fp, 'vertex %f %f %f' % vertices[i]
		print >>fp, 'vertex %f %f %f' % vertices[j]
		print >>fp, 'vertex %f %f %f' % vertices[k]
		print >>fp, 'endloop'
		print >>fp, 'endfacet'

	print >>fp, 'endsolid', name
