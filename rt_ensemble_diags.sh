#!/bin/bash

machine=`hostname | cut -c 1`
if [[ $machine == "c" || $machine == "d" ]]; then
    py=/u/donald.e.lippi/miniconda3/bin/python
    export incdate=/u/donald.e.lippi/bin/incdate
fi

# Run at 00 UTC
date2=$(date --date "yesterday" "+%Y%m%d"23)

year=`echo $date2 | cut -c 1-4`
mon=`echo $date2 | cut -c 5-6`
day=`echo $date2 | cut -c 7-8`

################# USER INPUT ##################
expt_name="rrfs_a_conus"
hours=23
figdir="/lfs/h2/emc/ptmp/donald.e.lippi/rrfs_a_diags/figs"
datapath_rt="/lfs/h2/emc/ptmp/emc.lam/rrfs/v0.3.8/nwges"
#datapath_rt="/lfs/h2/emc/ptmp/emc.lam/rrfs/conus/nwges"
datapath="/lfs/h2/emc/da/noscrub/donald.e.lippi/rrfs_mon/ensemble_ob_space_diag"
outdir="/lfs/h2/emc/ptmp/donald.e.lippi/rrfs_a_diags/figs/$year/$mon/$day/"
############ END  USER INPUT ##################

date1=`$incdate $date2 -$hours`
echo $date1 $date2

if [[ ! -L $datapath/$expt_name ]]; then
    ln -sf $datapath_rt ./$expt_name
fi

mkdir -p $outdir
cd $outdir

$py /lfs/h2/emc/da/noscrub/donald.e.lippi/rrfs_mon/ensemble_ob_space_diag/ensemble_diags_profile.py $date1 $date2 $datapath
$py /lfs/h2/emc/da/noscrub/donald.e.lippi/rrfs_mon/ensemble_ob_space_diag/ensemble_diags_time_trace.py $date1 $date2 $datapath

rzdm_config_files=/lfs/h2/emc/da/noscrub/donald.e.lippi/rrfs_mon/config/
cp ${rzdm_config_files}/* .

echo ""
echo "your files are located: $outdir"


#cd $figdir
#ssh-keygen -R emcrzdm.ncep.noaa.gov -f /u/donald.e.lippi/.ssh/known_hosts
#rsync -a * donald.lippi@emcrzdm.ncep.noaa.gov:/home/www/emc/htdocs/mmb/dlippi/rrfs_a/.
