#!/bin/bash

machine=`hostname | cut -c 1`
if [[ $machine == "c" || $machine == "d" ]]; then
    py=/apps/spack/python/3.8.6/intel/19.1.3.304/pjn2nzkjvqgmjw4hmyz43v5x4jbxjzpk/bin/python
    export incdate=/u/donald.e.lippi/bin/incdate
fi

# Run at 00 UTC
date2=$(date --date "yesterday" "+%Y%m%d"23)

############### USER INPUT ##################
#date2=2023031923
hours=23
expt="rrfs_a_na"
#expt="$expt v0.7.9"
expt="$expt v0.8.1"
datapath="/lfs/h2/emc/da/noscrub/donald.e.lippi/rrfs_mon/ensemble_ob_space_diag/"
figdir="/lfs/h2/emc/ptmp/donald.e.lippi/rrfs_a_diags/figs/"
scriptpath="/lfs/h2/emc/da/noscrub/donald.e.lippi/rrfs_mon/ensemble_ob_space_diag/"
############END USER INPUT ##################

date1=`$incdate $date2 -$hours`
echo $date1 $date2
year=`echo $date2 | cut -c 1-4`
mon=`echo $date2 | cut -c 5-6`
day=`echo $date2 | cut -c 7-8`

#unlink ./$expt
#unlink ./rrfs_a_na
#ln -sf $datapath_na ./rrfs_a_na
#ln -sf $datapath_conus ./rrfs_a_conus


outdir="$figdir/$year/$mon/$day/"
mkdir -p $outdir
cd $outdir
$py $scriptpath/ensemble_diags_profile.py $date1 $date2 $datapath
$py $scriptpath/ensemble_diags_time_trace.py $date1 $date2 $datapath

# Only copy rzdm files when on WCOSS.
if [[ $machine == "d" || $machine == "c" ]]; then
    rzdm_config_files=/lfs/h2/emc/da/noscrub/donald.e.lippi/rrfs_mon/config/
    cp ${rzdm_config_files}/* .
fi

echo ""
echo "your files are located: $outdir"

echo "Done making figs. Now upload to rzdm..."
# upload to rzdm
cd $figdir
cd /lfs/h2/emc/ptmp/donald.e.lippi/rrfs_a_diags/figs/
ssh-keygen -R emcrzdm.ncep.noaa.gov -f /u/donald.e.lippi/.ssh/known_hosts
rsync -a * donald.lippi@emcrzdm.ncep.noaa.gov:/home/www/emc/htdocs/mmb/dlippi/rrfs_a/.

echo "Done uploading."
