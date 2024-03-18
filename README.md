## snp.py<nolink>

A Python script used to create .pngs for both the PowerPoint and screen display elements. This script is responsible for almost all image processing tasks.

**How does it work?**

1. User provides a "config.png".

![config.png](https://i.imgur.com/tykqnIs.png)

2. The script takes an array/list of RGBA values provided by the user and searches for them in the "config.png" file. For each index 'i' in the array, it identifies the positions of the first and last pixels with the corresponding RGBA values. Additionally, it calculates the region enclosed by these two pixels for the specified 'i' index.

3. Function `setup()` returns :
	* A turple of the size of "config.png".
		*  → (x, y)

	* An array/list of all first and last positions of RGBA pixels searched for.
	
		* → [ **[ (0, 0) , (100, 50) ]** , [ ( ... ) , ( ... ) ] , ... ]

	* The sizes of regions bounded by RGBA pixels searched for.
		* → [ **(100, 50)** , ( ... , ... ) , ... ]

```python
snp.py
------------------------------------------------------
config_path = "path\\to\\config.png"
search_rgba = [ (255, 0, 0, 255) ]

output = setup( config_path , search_rgba )
# = ( (500, 500), [ [ (0, 0) , (100, 50) ] ], [ (100, 50) ] )
```

4. The user provides or the script generates an array/list of items to be pasted onto a copy of "base.png". All elements in the list are of type `string` and the script recognises strings with `\`'s in them as image paths.

	* Further implementations of the script is supplied with an input folder `.\\input\\images` that stores the .jpg to be loaded.

5. Function `paste()` loops through list/array of elements and pastes each one on the same copy of "base.png". Some procedures are applied respective of the element being pasted :
	* Image :
		* Image is resized to fit region bounded by RGBA pixels searched for, for 'i' index in the array.

	* Text :
		* Font is applied along with a preset or calculated font size. The script centers the text in the region bounded by RGBA pixels searched for.

	* Grayscale and transparency masks can be applied by passing an array/list of same length as the array/list of elements. 
		* `"T"` indicates the use of a transparency mask.
		
		* `"G"` indicates the use of a grayscale mask.

		* Any other values are ignored.

_**[Note] :** The data item at an index in the RGBA positions list/array corresponds to the data item in the list/array of elements to be pasted at that same index._

6. Function `paste()` returns a PIL Image object of the modified copy of "base.png".

![Imgur](https://i.imgur.com/Hev782M.png)
*"config.png" was used as base image to show how the elements are pasted withing the regions.*

```python
snp.py
------------------------------------------------------
if __name__ == "__main__" :
	config_path = "path\\to\\config.png"
	base_path   = "path\\to\\base.png"

	search_rgba = [
	(255, 0, 0, 255),
	(0, 255, 0, 255),
	(0, 0, 255, 255),
	(255, 255, 0, 255),
	(255, 0, 255, 255)
	]

	elements   = ["path\\to\\input\\images\\7.jpg", "7", "Wu", "Liuqi", "Chicken Island"]

	font_paths = ["path\\to\\assets\\Martian_Mono\\static\\MartianMono-Medium.ttf" for _ in range(4)]
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
	base.save("path\\to\\example.png", quality=100, optimize=True)
```
_**[Note] :** `.\\input\\images` is used to maintain a certain uniformity/standard but an absolute path works too._
