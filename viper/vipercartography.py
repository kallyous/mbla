import importlib, viper
from viper.vipermethods import grid2D, gridToStr, ReadTopographyAt, LoadStoredSector
if viper.DEBUG:
    from viper.viperdebug import *

class LandLevel():
    def __init__(self, wid, lvl):
        self.wid = wid
        self.xSec = viper.WORLDS[wid]['xSec']
        self.ySec = viper.WORLDS[wid]['ySec']
        self.name = u'%s #%d' % (viper.WORLDS[wid]['name'], lvl)
        self.path = u'%s/%d' % (viper.WORLDS[wid]['path'], lvl)
        self.topo_path = u'%s/level-meta.dat' % self.path
        self.sectors = grid2D(self.xSec, self.ySec, None)
    
    def loadSector(self, x, y):
        sector_file = u'%s/level-%d-%d.txt' % (self.path, x, y)
        data_str = ''
        try:
            with open(sector_file, 'r') as sf:
                for line in sf:
                    data_str += line
        except:
            print('%s sector %d %d do not exists.' % (self.name, x, y) )
            return False
        else:
            print('Loaded %s sector %d %d:' % (self.name, x, y) )
            return True           


    def saveSector(self, x, y):
        file_name = u'%s/level-%d-%d.txt' % (self.path, x, y)
        biome = self.sectors[x][y].biome
        owner = self.sectors[x][y].owner
        data_str = u'%s\n%s\n%d %d\n' % (biome, owner, x, y)
        data_str += 'data_map ground\n'
        data_str += gridToStr(self.sectors[x][y].ground_map)
        data_str += 'data_map floor\n'
        data_str += gridToStr(self.sectors[x][y].floor_map)
        data_str += 'data_map walls\n'
        data_str += gridToStr(self.sectors[x][y].wall_map)
        data_str += 'data_map roof\n'
        data_str += gridToStr(self.sectors[x][y].roof_map)
        with open(file_name, 'w') as sector_file:
            sector_file.write(data_str)
    
    def newSector(self, xSect, ySect):
        topography, biome = ReadTopographyAt(self.topo_path, xSect, ySect)
        self.sectors[xSect][ySect] = Sector()
        self.sectors[xSect][ySect].Generate(topography, biome, viper.WORLDS[self.wid]['generator'])
        self.saveSector(xSect, ySect)
        #TestReadSectorTopography(topography, biome, self.path, xSect, ySect)


class Sector():
    def __init__(self, file=None):
        if file == None:
            self.ground_map = []
            self.floor_map = []
            self.wall_map = []
            self.roof_map = []
            self.objs = []
            self.ent = []
        else: self.Load(file)
    
    def Generate(self, topography, biome, generator):
        # Import the given script/module
        gen = importlib.import_module(generator)
        sector_data = gen.GenerateTerrain(topography, biome)
        self.ground_map = sector_data['ground']
        self.floor_map = sector_data['floor']
        self.wall_map = sector_data['walls']
        self.roof_map = sector_data['roof']
        self.biome = sector_data['biome']
        self.objs = sector_data['objects']
        self.ent = sector_data['entities']
        self.owner = sector_data['owner']
    
    def Load(self, file_path):
        sector_data = LoadStoredSector(file_path)
        self.ground_map = sector_data['ground']
        self.floor_map = sector_data['floor']
        self.wall_map = sector_data['walls']
        self.roof_map = sector_data['roof']
        self.biome = sector_data['biome']
        self.objs = sector_data['objects']
        self.ent = sector_data['entities']
        self.owner = sector_data['owner']
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    