import cv2

img = cv2.imread("flag.png",0)

for i in range(img.shape[0]):
	for j in range(img.shape[1]):
		pxl = img[i][j]
		if pxl != 255:
			img[i][j] = 0
				
				
MAX = 50
MIN = 6


def check_square_fit(i,j,l):
	for x in range(i,i+l):
		for y in range(j,j+l):
			if x >= img.shape[0] or y >= img.shape[1] or img[x][y] == 255:
				return False
	return True

def change_color(i,j,l):
	for x in range(i,i+l):
		for y in range(j,j+l):
			img[x][y] = 127
					
constraints = ""	
counter = 0		
possible = list()
done = False
for i in range(img.shape[0]):
	for j in range(img.shape[1]):
		if img[i][j] != 255:
			for l in range(MAX, MIN,-1):
				if(check_square_fit(i,j,l)):
					possible.append(tuple((i,j,l)))
					#print("Y is between [" + str(i) + "," + str(i + l) + "]")
					#print("X is between [" + str(j) + "," + str(j + l) + "]")
					#print("----------")
					counter += 1
					constraints += "(" +  str(j)  + " < X < " + str(j + l) + ") && (" +  str(i)  + " < Y < " + str(i + l) + ") || "
					change_color(i,j,l)
cv2.imshow('ImageWindow', img)
cv2.waitKey()						

for i in range(img.shape[0]):
	for j in range(img.shape[1]):
		pxl = img[i][j]
		if pxl == 255 or pxl == 0:
			img[i][j] = 0
		elif pxl == 127:
			img[i][j] = 255
				
				
					
cv2.imshow('ImageWindow', img)
cv2.waitKey()			
#print(possible)
print(constraints[:-4])
#print(counter)			
					


