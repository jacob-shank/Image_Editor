from Picture import Picture

image: Picture = Picture("TestE")
image.setBlackPoint(60,255)
image.setWhitePoint(200,255)
image.saveAs(".jpg")

pass