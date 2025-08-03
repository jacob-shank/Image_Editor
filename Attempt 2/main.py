from Picture import Picture

image: Picture = Picture("TestE")
image.uniform_crop(10)
image.saveAs(".jpg")