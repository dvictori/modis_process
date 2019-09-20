# -*- coding: utf-8 -*-
"""
Created on Tue Dec 20 15:23:01 2011

@author: daniel

parte do programa para extrair imagens NDVI, EVI
dos estados brasileiros
aqui são definidos os estados: tiles, limites

Tb estou adicionando uma área especial: Mapito
"""

import os

class UF():
    '''Classe para definir os limites e tiles de cada estado
    tiles é uma lista, limites são float'''
    def __init__(self, sigla, xmin, xmax, ymin, ymax, tiles):
        self.sigla = sigla
        self.xmax = xmax
        self.xmin = xmin
        self.ymax =  ymax
        self.ymin = ymin
        self.tiles = tiles
 
# "iniciando" os estados
ac = UF("ac", -74.5, -66, -12, -7, ["h10v09", "h11v09", "h11v10"])
al = UF("al", -39, -35, -11, -8, ["h1v09", "h14v10"])
am = UF("am", -74, -56, -10, -2, ["h11v08", "h12v08", "h10v09", "h11v09", "h12v09"])
ap = UF("ap", -55, -49, -2, 4, ["h12v08", "h13v08", "h12v09"])
ba = UF("ba", -47, -37, -19, -8, ["h13v09", "h14v09" , "h13v10", "h14v10"])
ce = UF("ce", -42, -37, -8, -2, ["h13v09", "h14v09"])
#df = UF("df", -49, -47, -17, -15, ["h13v10"])
es = UF("es", -42, -39, -22, -17, ["h14v10", "h14v11"])
go = UF("go", -54, -45, -20, -12, ["h12v10", "h13v10"])
ma = UF("ma", -49, -41, -11, -1, ["h13v09", "h13v10"])
mg = UF("mg", -52, -39, -23, -14, ["h13v10", "h14v10", "h13v11", "h14v11"])
ms = UF("ms", -59, -50, -25, -17, ["h12v10", "h13v10", "h12v11", "h13v11"])
mt = UF("mt", -62, -50, -19, -7, ["h11v09", "h12v09", "h13v09", "h11v10", "h12v10", "h13v10"])
pa = UF("pa", -59, -46, -10, 2, ["h12v08", "h13v08", "h12v09", "h13v09"])
pb = UF("pb", -39, -34, -9, -6, ["h14v09"])
pe = UF("pe", -42, -34, -10, -3, ["h13v09", "h14v09"])
pi = UF("pi", -46, -40, -11, -2, ["h13v09", "h14v09", "h13v10"])
pr = UF("pr", -55, -48, -27, -22, ["h13v11"])
rj = UF("rj", -45, -40, -24, -20, ["h13v11", "h14v11"])
rn = UF("rn", -39, -34, -7, -4, ["h14v09"])
ro = UF("ro", -67, -59, -14, -7, ["h11v09", "h11v10", "h12v10"])
rr = UF("rr", -65, -58, -2, 5.5, ["h11v08", "h12v08", "h11v09"])
rs = UF("rs", -58, -49, -34, -27, ["h13v11", "h13v12"])
sc = UF("sc", -54, -48, -30, -25, ["h13v11"])
se = UF("se", -39, -36, -12, -9, ["h14v09", "h14v10"])
sp = UF('sp', -53.5, -44, -25.5, -19.5, ['h13v11', 'h13v10'])
to = UF("to", -51, -45, -14, -5, ["h13v09", "h13v10"])
mapito = UF("mapito", -49, -41, -18, -5, ["h13v09", "h13v10"])
ba_sano = UF("ba_sano", -47, -42, -16, -8, ["h13v09", "h13v10"])
safer = UF("safer", -63, -42, -34, -7, ["h13v12", "h13v11", "h14v11", "h12v11", "h11v10", "h12v10", "h13v10", "h14v10", "h12v09", "h13v09", "h11v09"])
brasil = UF("brasil", -74.5, -34, -34, 5.5, ["h11v08", "h12v08", "h13v08", "h10v09", "h11v09", "h12v09", "h13v09", "h14v09", "h11v10", "h12v10", "h13v10", "h14v10", "h12v11", "h13v11", "h14v11", "h13v12"])
feijao = UF("feijao", -51, -20, -43, -13, ["h13v10"])
sc_pr = UF("sc_pr", -55, -48, -30, -22, ["h13v11"])
ba_menor = UF("ba_menor", -40.5, -39, -18, -16.5, ["h13v10","h14v10"])
sudeste = UF("sudeste", -54, -39, -25.5, -14, ["h13v10", "h14v10", "h13v11", "h14v11"])
