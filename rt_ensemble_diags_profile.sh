#!/bin/bash

debug="NO"

py=/u/donald.e.lippi/miniconda3/bin/python

export incdate=/u/donald.e.lippi/bin/incdate

datapath="/lfs/h2/emc/ptmp/donald.e.lippi/rrfs_a_diags/"

runtime=$(date --date "2 hour ago" "+%Y%m%d%H")
runtime=$(date --date "24 hour ago" "+%Y%m%d%H")


year=`echo $runtime | cut -c 1-4`
mon=`echo $runtime | cut -c 5-6`
day=`echo $runtime | cut -c 7-8`

#year=2023
#mon=03
#day=03
cyc=23

runtime=${year}${mon}${day}${cyc}
hours=23
#hours=17

if [[ $debug == "YES" ]]; then
    #run manually
    runtime=$(date --date "now" "+%Y%m%d"00)
    runtime=2023021412
    hours=12
fi


date2=$runtime
date1=`$incdate $date2 -$hours`
echo $date1 $date2

year=`echo $date2 | cut -c 1-4`
mon=`echo $date2 | cut -c 5-6`
day=`echo $date2 | cut -c 7-8`


if [[ $debug == "YES" ]]; then
    outdir="./"
else
    outdir=/lfs/h2/emc/ptmp/donald.e.lippi/rrfs_a_diags/figs/$year/$mon/$day/
    mkdir -p $outdir
fi
cd $outdir

$py /lfs/h2/emc/da/noscrub/donald.e.lippi/rrfs_mon/ensemble_ob_space_diag/ensemble_diags_profile.py $date1 $date2 $datapath

rzdm_config_files=/lfs/h2/emc/da/noscrub/donald.e.lippi/rrfs_mon/config/
cp ${rzdm_config_files}/* .

echo ""
echo "your files are located: $outdir"

