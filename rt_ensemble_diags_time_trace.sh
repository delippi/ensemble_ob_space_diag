#!/bin/bash

py=/home/Donald.E.Lippi/miniconda3/bin/python

export incdate=/home/Donald.E.Lippi/bin/incdate

outdir="./"
#/mnt/lfs1/BMC/wrfruc/chunhua/May2022_retro/Ens_Ctrl/NCO_dirs/nwges/para/RRFS_CONUS/observer_diag
datapath="/mnt/lfs1/BMC/wrfruc/chunhua/May2022_retro/Ens_Ctrl/NCO_dirs/nwges/para/"  # RRFS_CONUS/observer_diag

hours=23
date2=2022051223
date1=`$incdate $date2 -$hours`
echo $date1 $date2

year=`echo $date2 | cut -c 1-4`
mon=`echo $date2 | cut -c 5-6`
day=`echo $date2 | cut -c 7-8`

cd $outdir
$py /mnt/lfs1/data_untrusted/Donald.E.Lippi/ensemble_ob_space_diag/ensemble_diags_time_trace.py $date1 $date2 $datapath

echo ""
echo "your files are located: $outdir"
