def printImg(data, name):
    w = len(data)
    h = len(data[0])
    img = Image.new('RGB', (w, h) )
    for x in range(w):
        for y in range(h):
            blue = int( 256 * data[x][y] )
            img.putpixel( (x,y), (0,0,blue) )
    img.save(name, 'PNG')


def TestTopographyFile(tp_file):
    print('Testing topography %s' % tp_file)
    
    # Data reading
    with open(tp_file, 'rb') as level:
        # Read seed, 8 bytes
        b_seed = level.read(8)
        seed = int.from_bytes(b_seed, sys.byteorder)
        # Read max X sectors, 8 bytes
        b_max_xSec = level.read(8)
        max_xSec = int.from_bytes(b_max_xSec, sys.byteorder)
        # read max Y sectors, 8 bytes
        b_max_ySec = level.read(8)
        max_ySec = int.from_bytes(b_max_ySec, sys.byteorder)
        # read sector width, 8 bytes
        b_sect_width = level.read(8)
        sect_width = int.from_bytes(b_sect_width, sys.byteorder)
        # read sector height, 8 bytes
        b_sect_height = level.read(8)
        sect_height = int.from_bytes(b_sect_height, sys.byteorder)
        
        
        img_width = max_xSec * sect_width
        img_height = max_ySec * sect_height
        img = Image.new('RGB', (img_width, img_height) )
        
        xOff = 0
        for xSec in range(max_xSec):
            yOff = 0
            for ySec in range(max_ySec):
                b_red = level.read(1)
                red = int.from_bytes(b_red, sys.byteorder)
                for x in range(sect_width):
                    for y in range(sect_height):
                        b_green = level.read(1)
                        green = int.from_bytes(b_green, sys.byteorder)
                        img.putpixel( (x+xOff,y+yOff), (red, green, 0) )
                yOff += sect_height
            xOff += sect_width
    
    img_name = tp_file.rstrip('dat') + 'png'
    img.save(img_name)
    print('Results written to %s' % img_name)


def TestReadSectorTopography(topography, biome, lvl_path, xSect, ySect):
    width = len(topography)
    height = len(topography[0])
    
    img = Image.new('RGB', (width,height) )
    
    for x in range(width):
        for y in range(height):
            img.putpixel((x,y), (0, topography[x][y], 0) )
    
    img.save('%s/sect_%d_%d_topography_b%d.png' % (lvl_path, xSect, ySect, biome) )


