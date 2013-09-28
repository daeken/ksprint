def read(fn):
	def readchild(fp):
		elem = { }
		type = None
		for line in fp:
			line = line.strip()
			if len(line) == 0:
				continue
			if '=' in line:
				k, v = [x.strip() for x in line.split('=', 1)]
				elem[k] = v
			elif line == '}':
				break
			elif line.endswith('{'):
				if line == '{':
					assert type != None
				else:
					assert type == None
					type = line[:-1].strip()
				if type not in elem:
					elem[type] = []
				elem[type].append(readchild(fp))
			else:
				type = line
		return elem

	with file(fn, 'r') as fp:
		return readchild(fp)
