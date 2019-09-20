#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 14 11:36:47 2015

Programa para gerar os mosaicos das UFs
Usuário pode escolher a UF (ou Brasil), a data e e as bandas
Específico para trabalhar com MOD13Q1

@author: daniel

2/mar/2015 - Me dei conta que a resolucao de saida estava menor que o necessario
olhando outras imagens processadas pelo MRT, fixei a resolucao de saida do gdalwar em 0.002 (-tr)
"""

import argparse
from pymodis.convertmodis_gdal import createMosaicGDAL
import glob, os
import estados_v2
import subprocess

parser = argparse.ArgumentParser(description='Programa para gerar mosaicos MODIS das UFs. Por defaul extrai apenas EVI')

parser.add_argument('uf', help='Unidade da federacao para gerar mosaico')
parser.add_argument('ano', help='Ano do mosaico a ser gerado', type=int)
parser.add_argument('doy', help='Dia do ano (DOY) para gerar mosaico', type=int, choices=range(1,356,16))
parser.add_argument('outdir', help='pasta onde salvar mosaico')

parser.add_argument('--input', help='pasta onde se encontram imagens brutas', default='mod13q1/brutas')
# quais as bandas extrair? padrão extrai EVI
parser.add_argument('--ndvi', help='Extrai NDVI', action='store_true')
parser.add_argument('--evi', help='Extrai EVI', action='store_true')
parser.add_argument('--r_nir', help='Extrai red e NIR', action='store_true')
parser.add_argument('--day', help='Extrai Dia do ano', action='store_true')
parser.add_argument('--pr', help='Extrai Pixel Reliability', action='store_true')

args = parser.parse_args()

UF = eval('estados_v2.'+args.uf)
tiles = UF.tiles

lista = []
for t in tiles:
    basename = 'MOD13Q1.A{0}{1:03}.{2}.*.hdf'.format(args.ano, args.doy, t)
    lista = lista + glob.glob(os.path.join(args.input,basename))

#print lista

# gerando lista de subset
subset = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ,0 ,0]
bandas = ['250m 16 days NDVI', '250m 16 days EVI', 'QA', '250m 16 days red reflectance',
          '250m 16 days NIR reflectance', 'blue', 'MIR', 'view_zenith', 'sun_zenith', 'rel_az',
          '250m 16 days composite day of the year', '250m 16 days pixel summary QA']

bandas_s = ['250m_16_days_NDVI', '250m_16_days_EVI', 'QA', 'red', 'NIR', 'blue', 'MIR', 'view_zenith', 'sun_zenith',
            'rel_az', 'DOY', 'sumQA']          
        
if args.ndvi:
    subset[0] = 1
if args.evi:
    subset[1] = 1
if args.r_nir:
    subset[3] = 1
    subset[4] = 1
if args.day:
    subset[10] = 1
if args.pr:
    subset[11] = 1
if subset.count(1) == 0:
    #extrair apenas EVI
    subset[1] = 1    
    
bandas_extract = [b for i,b in zip(subset, bandas) if i == 1]
bandas_simples = [b for i,b in zip(subset, bandas_s) if i == 1]

# vendo se data já foi processada
# verifica apenas se arquivo existe
# ainda não pensei em como resolver isso...
#for b in bandas_simples:
#    saida = os.path.join(args.outdir, '{0}.A{1}{2:03}_{3}.tif'.format(args.uf, args.ano, args.doy, b))
#    try:
#        open(saida)
#        print 'Mosaico {0} já existe. Próxima...'.format(saida)
#        continue
#    except IOError:
#        pass

#out_tiff = '{0}.A{1}{2:03}.tif'.format(args.uf, args.ano, args.doy)
out_base = '{0}.A{1}{2:03}'.format(args.uf, args.ano, args.doy)

print 'Gerando mosaico virtual para {0} na data {1}{2:03}'.format(args.uf, args.ano, args.doy)

mosaico = createMosaicGDAL(lista, subset, 'GTiff')
mosaico.write_vrt(os.path.join(args.outdir, out_base))
#mosaico.run(os.path.join(args.outdir, out_tiff))

# reprojetando
# preciso adicionar a barra (\) manualmente no nome do arquivo porque o write_vrt coloca espaco no nome
# gdalwarp precisa da barra enquanto que o os.remove, usado mais tarde, não aceita a barra
print 'Reprojetando e cortando as {0} bandas para {1}, data {2}{3:03}'.format(len(bandas_extract), args.uf, args.ano, args.doy)
for b in range(len(bandas_extract)):
    entrada = os.path.join(args.outdir, out_base+'_'+bandas_extract[b]+'.vrt')
    saida_tmp = os.path.join(args.outdir, '{0}.A{1}{2:03}.{3}.temp.vrt'.format(args.uf, args.ano, args.doy, bandas_simples[b]))
    saida = os.path.join(args.outdir, '{0}.A{1}{2:03}.{3}.tif'.format(args.uf, args.ano, args.doy, bandas_simples[b]))
    
    comando = 'gdalwarp -of VRT -t_srs epsg:4326 -tr 0.002 0.002 {0} {1}'.format(entrada.replace(' ','\ '), saida_tmp)
    #print comando
    subprocess.call(comando, shell=True)

    # recortando
    comando = 'gdal_translate -co TILED=YES -co blockxsize=512 -co blockysize=512 -co compress=deflate -projwin {0} {1} {2} {3} {4} {5}'.format(UF.xmin, UF.ymax, UF.xmax, UF.ymin, saida_tmp, saida)
    #print comando    
    subprocess.call(comando, shell=True)
    
    os.remove(os.path.join(args.outdir, out_base+'_{0}.vrt'.format(bandas_extract[b])))
    os.remove(saida_tmp)

