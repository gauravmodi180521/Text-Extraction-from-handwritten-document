#LINE SEGMENTING
def get_line(binarized_image):
	img = binarized_image
	rows, cols = img.shape
	density_list = []
	for row in range(rows):
		density = 0
		for col in range(cols):
			if img[row, col] == 0:
				density += 1
		density_list.append(density)

	coordinates = []
	i = 0
	while(i < rows):
		a = 0
		b = 0
		if density_list[i] != 0:
			a = i-1
			while(density_list[i] != 0):
				i += 1
			b = i
			coordinates.append((0, b, cols-1, a))
		else:
			i += 1			
	return coordinates

#SEGMENTING CHARACTERS
def get_chars(binarized_image, line_coordinates):
	img = binarized_image
	rows, cols = img.shape
	lcs = line_coordinates
	char_list = []
	for lc in lcs:
		density_list = []
		for col in range(lc[0], lc[2]):
			density = 0
			for row in range(lc[3], lc[1]):
				if img[row, col] == 0:
					density += 1
			density_list.append(density)
		char_list.append(density_list)

	character_coordinates = []
	for line in range(len(lcs)):
		coordinates = []
		i = lcs[line][0]
		while(i < lcs[line][2]):
			a = 0
			b = 0
			if char_list[line][i] != 0:
				a = i-1
				while(char_list[line][i] != 0):
					i += 1
				b = i
				coordinates.append((a, lcs[line][1], b, lcs[line][3]))
			else:
				i += 1
		character_coordinates.append(coordinates)
	return character_coordinates

#OUTLINE DISTANCE FOR WORD SEGMENTATION
def get_outline(coo):
	min_outline = 100
	max_outline = 0
	for coi in range(len(coo) - 1):
		if(coo[coi+1][0] - coo[coi][2] > max_outline):
			max_outline = coo[coi+1][0] - coo[coi][2]
		if(coo[coi+1][0] - coo[coi][2] < min_outline):
			min_outline = coo[coi+1][0] - coo[coi][2]	
	return min_outline, max_outline	