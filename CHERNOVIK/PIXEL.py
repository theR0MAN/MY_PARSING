from PIL import Image, ImageColor

im = Image.new('1', (3840*2,2160)) # create the Image of size 1 pixel
im.putpixel((100,100), ImageColor.getcolor('red', '1')) # or whatever color you wish
im.show()
im.save('simplePixel.png') # or any image format)                      # View in default viewerw(pixel_plot)
