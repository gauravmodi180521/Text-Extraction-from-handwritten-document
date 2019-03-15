#SEGMENTATING CONNECTED COMPONENTS USING LABELING CLUSTERS
def get_connected_components(binarized_image):
	label = -1
	objs = []
	find = []

	def passed_neighbours(row, col, columns):
		ngbrs = []
		if(row == 0):
			if(col == 0):
				return ngbrs
			else:
				ngbrs.append((row, col-1))
				return ngbrs
		elif(col == 0):
			ngbrs.append((row-1, col))
			ngbrs.append((row-1, col+1))
			return ngbrs
		elif(col == columns-1):
			ngbrs.append((row-1, col))
			ngbrs.append((row, col-1))
			ngbrs.append((row-1, col-1))
			return ngbrs
		else:
			ngbrs.append((row, col-1))
			ngbrs.append((row-1, col-1))
			ngbrs.append((row-1, col))
			ngbrs.append((row-1, col+1))
			return ngbrs
	
	def find_cluster(x):
		if(find[(-x)-1] != x):
			x = find[(-x)-1]
		return x

	def combine_objs(relobjs):
		row_min = min([ele[0] for ele in relobjs])
		row_max = max([ele[1] for ele in relobjs])
		column_min = min([ele[2] for ele in relobjs])
		column_max = max([ele[3] for ele in relobjs])
		return (row_min, row_max, column_min, column_max)

	img = binarized_image
	rows, cols = img.shape
	for row in range(rows):
		for col in range(cols):
			if(img[row, col] == 0):
				ngbrs = passed_neighbours(row, col, cols)
				ngbrs = [ngbr for ngbr in ngbrs if(img[ngbr[0], ngbr[1]] != 255)]
				if(len(ngbrs) == 0):
					img[row, col] = label
					find.append(label)
					objs.append((row, row, col, col))
					label -= 1
				else:
					finds = list(set([find_cluster(img[ngbr[0], ngbr[1]]) for ngbr in ngbrs]))
					relobjs = [objs[(-a)-1] for a in finds if objs[(-a)-1] is not None]
					leastval = max(finds)
					img[row, col] = leastval
					relobjs.append((row, row, col, col))
					combined_objs = combine_objs(relobjs)
					for a in finds:
						find[(-a)-1] = leastval

					for a in finds:
						objs[(-a)-1] = None

					objs[(-leastval)-1] = combined_objs

	for row in range(rows):
		for col in range(cols):
			if(img[row, col] != 255):
				img[row, col] = find_cluster(img[row, col])

	objs = [o for o in objs if o is not None]
	objs = list(filter(lambda x: x[0] != x[1] and x[2] != x[3], objs))
	return objs