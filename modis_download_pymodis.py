#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Created on Wed Feb 12 10:40:48 2014

@author: daniel
Programa para baixar arquivos MODIS do servidor do USGS
Usa biblioteca pyModis
"""

from pymodis import downmodis
import argparse
import estados_v2

parser = argparse.ArgumentParser(description = 'Programa para baixar dados MODIS do servidor da USGS')

parser.add_argument('dest_dir', help='Pasta onde dados serão salvos')

group = parser.add_mutually_exclusive_group()
group.add_argument('-uf', help = 'Baixa todos os tiles do estado')
group.add_argument('-tile', help = 'Baixa apenas um tile', choices = ["h11v08", "h12v08", "h13v08", "h10v09", "h11v09", "h12v09", "h13v09", "h14v09", "h11v10", "h12v10", "h13v10", "h14v10", "h12v11", "h13v11", "h14v11", "h13v12"])

parser.add_argument('-p', '--produto', help='Produto que será baixado', choices=['MOD13Q1.005'], default='MOD13Q1.005')

parser.add_argument('-data_final', help='Data do último período a ser baixado, formato YYYY-MM-DD. Padrão é data de hoje.')
parser.add_argument('-delta', help='Quantas imagens baixar, retroativo à data_final', type=int, default=1)

args = parser.parse_args()

def main(args):
    # vendo lista de tiles

    if args.tile == None and args.uf == None:
        print 'É preciso definir uf ou tile'
        return
        
    if args.tile:
        tiles = str(args.tile)
    else:
        UF = eval('estados_v2.'+args.uf)
        tiles = UF.tiles
    
    if args.data_final != None:
        # usuário esta trocando a data de download
        modisDown = downmodis.downModis(destinationFolder=args.dest_dir, tiles=tiles, product=args.produto, today=args.data_final, delta=args.delta)
    else:
        modisDown = downmodis.downModis(destinationFolder=args.dest_dir, tiles=tiles, product=args.produto, delta=args.delta)
    
    modisDown.connect()
    modisDown.downloadsAllDay()
    return

if __name__ == '__main__':
    main(args)
