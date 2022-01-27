import os
path = '/home/User/Documents/file.txt'
basename = os.path.basename(path)

# Print the basename name 
name = basename.split(".")[0]
print(name)

fileList = ['.DS_Store', '.DS_Store', '.tif', 'a1', 'a2', 'a3', 'a4', 'a5', 'a6', 'b1', 'b2', 'b3', 'b4', 'b5', '    b6', 'c1', 'c2', 'c3', 'c4', 'c5', 'c6', 'imgs_a', 'imgs_b', 'imgs_c']

new_result = [c for c in fileList if len(c)<3]
print(new_result)