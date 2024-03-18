from PIL import Image, ImageDraw, ImageFont, ImageOps

FILL_COLOUR   = (255, 255, 255, 255)
STROKE_WIDTH  = 0
STROKE_COLOUR = (0, 0, 0, 255)

def setup(config_path, search_rgba) :
	"""
	Loops through each pixel in config file and finds first and last positions of each rgba value.

	Returns (list of first and last rgba positions) and (list of bounding boxes formed by rgba pixels)
	"""
	print(f"\n===============\n Configuration\n===============\n")

	# Loads config image
	config 		 = Image.open(config_path).convert("RGBA")
	cfg_x, cfg_y = config.size
	print(f"Loading   | {config_path}")

	# Searches for rgba values
	rgba_positions = [[False, False] for _ in range(len(search_rgba))]
	print(f"Searching | {search_rgba}")

	for x in range(cfg_x) :
		for y in range(cfg_y) :
			pixel = config.getpixel((x, y)) # Reads rgba value

			# Found
			if pixel in search_rgba :

				# If [False, False] -> First pixel founf
				if not(rgba_positions[search_rgba.index(pixel)][0]) :
					rgba_positions[search_rgba.index(pixel)][0] = (x, y)

				# Overwrites last pixel found
				else :
					rgba_positions[search_rgba.index(pixel)][1] = (x, y)

	print(f"Found     | {rgba_positions}")

	# Calculates bounding boxes
	bounding_box_sizes = []

	for i in rgba_positions :
		size_x = i[1][0] - i[0][0]
		size_y = i[1][1] - i[0][1]

		bounding_box_sizes.append((size_x, size_y))
		print(f"Calc Size | {i} = {(size_x, size_y)}")

	# Releases memory
	config.close()
	return (cfg_x, cfg_y), rgba_positions, bounding_box_sizes

def paste(base_path, elements, paste_filters, positions, bounding_box_sizes, font_paths, font_sizes) :
	"""
	Paste each item in elements list on a base image.
	Order in which elements are pasted is dependent on the elements position/index in the list.
	Images to be pasted are stored in elements list as file paths. For example : .//input.png

	Returns modified base image object (PIL.Image)
	"""
	print(f"\n==============\n Pasting Card\n==============\n")

	# Loads in base image
	base = Image.open(base_path).convert("RGBA")
	print(f"Loading     | {base_path}")
	
	# Loops through elements list and performs paste appropriately
	text_pasted = 0

	for i in range(len(elements)) :
		item = elements[i]
		box  = bounding_box_sizes[i]
		fltr = paste_filters[i]

		# Item is an image
		if "\\" in item :

			# Load in image
			img = Image.open(item).convert("RGBA")
			print(f"Loading     | {item}")

			# Resizes image to fit bounding box
			img = img.resize(box, Image.LANCZOS)
			print(f"Resizing    | {box}")

			# Applies filter
			if fltr == "G" :
				img = ImageOps.grayscale(img)

			# Pastes image on base image
			# positions[i][0] is the top left pixel location of bounding box

			# Conserve transparency
			if fltr == "T" :
				base.paste(img, positions[i][0], mask=img)

			else :
				base.paste(img, positions[i][0])

			print(f"Pasting     | {item}")

		elif type(item) is str :
			draw = ImageDraw.Draw(base)

			# Setup font
			f_path = font_paths[text_pasted]
			f_size = font_sizes[text_pasted]

			font = ImageFont.truetype(f_path, f_size)

			# Calculates size of text on image with chosen font and font size
			# Centers the text within bounding box
			text_size  = draw.textbbox(xy = (0, 0), text = item, font = font)
			x_centered = abs((box[0] - text_size[2]) // 2)
			y_centered = abs((box[1] - text_size[3]) // 2)

			x = positions[i][0][0] + x_centered
			y = positions[i][0][1] + y_centered

			# Pastes text
			draw.text(
				xy 			 = (x, y),
				text 		 = item,
				fill 		 = STROKE_COLOUR,
				font 		 = font,
				stroke_width = STROKE_WIDTH,
				stroke_fill  = STROKE_COLOUR
				)

			text_pasted += 1
			print(f"Pasting     | {item}")

		else :
			pass

	return base

if __name__ == "__main__" :
	config_path = "D:\\code\\tournament\\assets\\images\\config.png"
	base_path   = "D:\\code\\tournament\\assets\\images\\base.png"

	search_rgba = [
	(255, 0, 0, 255),
	(0, 255, 0, 255),
	(0, 0, 255, 255),
	(255, 255, 0, 255),
	(255, 0, 255, 255)
	]

	elements   = ["D:\\code\\tournament\\input\\images\\7.jpg", "7", "Wu", "Liuqi", "Chicken Island"]

	font_paths = ["D:\\code\\tournament\\assets\\Martian_Mono\\static\\MartianMono-Medium.ttf" for _ in range(4)]
	font_sizes = [80 for _ in range(4)]
	
	# Finding RGBA pixel positions and regions
	cfg_size, positions, bounding_box_sizes = setup(config_path, search_rgba)

	# Used to apply grayscale mask or conserve transparency of .png
	paste_filters = [False for _ in positions]

	base = paste(
		base_path 	  	   = config_path, 
		elements  	  	   = elements, 
		positions 	  	   = positions,
		paste_filters 	   = paste_filters,
		bounding_box_sizes = bounding_box_sizes, 
		font_paths 		   = font_paths, 
		font_sizes 		   = font_sizes
		)

	# Shows the modified .png
	base.show()

	# Saves/Outputs .png
	base.save("D:\\code\\tournament\\assets\\images\\example.png", quality=100, optimize=True)