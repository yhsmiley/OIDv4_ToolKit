import os

image_dir = './data/train/Woman'
num_keep = 20000

for root, dirs, files in os.walk(image_dir):
	for file in files:
		if file.endswith('.jpg'):
			if num_keep <= 0:
				os.remove(os.path.join(image_dir, file))
				print("{} removed".format(file))
			num_keep -= 1