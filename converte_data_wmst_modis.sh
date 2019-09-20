#!/bin/bash
# shell para converter série temporal modis no formato necessário para entrar no WMST
# passa nome do arquivo de YYYYDOY para YYYYMMDD
# Também comprime imagens gera overviews
# processa todas as imagens tif que estão dentro da pasta em questao

datas=([1]='0101' [17]='0117' [33]='0202' [49]='0218'\
 [65]='0306' [81]='0322' [97]='0407' [113]='0423' [129]='0509'\
 [145]='0525' [161]='0610' [177]='0626' [193]='0712' [209]='0728'\
 [225]='0813' [241]='0829' [257]='0914' [273]='0930' [289]='1016'\
 [305]='1101' [321]='1117' [337]='1203' [353]='1219')

for i in *.tif; do
    uf=`echo $i | awk -F '.' '{print $1}'`
    ano=`echo $i | awk -F '.' '{print substr($2,2,4)}'`
    doy_str=`echo $i | awk -F '.' '{print substr($2,6,3)}' | sed 's/0*//'`
    doy_int=$((doy_str))
    prod=`echo $i | awk -F '.' '{print $3}'`
    
    saida=$uf".A"$ano${datas[$doy_int]}"."$prod"_wmst.tif"
    #echo $saida
    # gdalwarp cm o cutline é para cortar imagem p/ o Brasil
    # depois comprime, gera os tiles internos e as pirâmides
    gdalwarp -dstnodata -3000 -cutline brasil_buff50_wgs84.shp $i temp_$i
    gdal_translate -co "COMPRESS=deflate" -co "TILED=YES" -co "BLOCKXSIZE=512" -co "BLOCKYSIZE=512" temp_$i $saida
    #gdal_translate -co "COMPRESS=deflate" -co "TILED=YES" -co "BLOCKXSIZE=512" -co "BLOCKYSIZE=512" $i $saida
    gdaladdo -r cubic $saida 2 4 8 16 32 64 128
    rm temp_$i
done
