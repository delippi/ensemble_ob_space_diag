#!/bin/bash
machine=`hostname | cut -c 1`
if [[ $machine == "d" || $machine == "c" ]]; then
    py=/u/donald.e.lippi/miniconda3/bin/python
    export incdate=/u/donald.e.lippi/bin/incdate
fi


############### USER INPUT ##################
date2=2023031523
hours=23
expt="rrfs_a_conus"
datapath_rt="/lfs/h2/emc/ptmp/emc.lam/rrfs/v0.3.8/nwges/observer_diag/" #2023031612
datapath="/lfs/h2/emc/da/noscrub/donald.e.lippi/rrfs_mon/ensemble_ob_space_diag/" # rrfs_a_conus
figdir="/lfs/h2/emc/ptmp/donald.e.lippi/rrfs_a_diags/figs/"
scriptpath="/lfs/h2/emc/da/noscrub/donald.e.lippi/rrfs_mon/ensemble_ob_space_diag/"
############END USER INPUT ##################

date1=`$incdate $date2 -$hours`
echo $date1 $date2
year=`echo $date2 | cut -c 1-4`
mon=`echo $date2 | cut -c 5-6`
day=`echo $date2 | cut -c 7-8`

if [[ ! -L $expt ]]; then
    ln -sf $datapath_rt ./$expt
fi

outdir="$figdir/$year/$mon/$day/"
mkdir -p $outdir
cd $outdir
$py $scriptpath/ensemble_diags_time_trace.py $date1 $date2 $datapath

# Only copy rzdm files when on WCOSS.
if [[ $machine == "d" || $machine == "c" ]]; then
    rzdm_config_files=/lfs/h2/emc/da/noscrub/donald.e.lippi/rrfs_mon/config/
    cp ${rzdm_config_files}/* .
fi

echo ""
echo "your files are located: $outdir"

