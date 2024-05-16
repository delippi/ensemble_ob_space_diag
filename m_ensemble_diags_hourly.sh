#!/bin/bash

cd /lfs/h2/emc/da/noscrub/donald.e.lippi/rrfs_mon/ensemble_ob_space_diag

machine=`hostname | cut -c 1`
if [[ $machine == "c" || $machine == "d" ]]; then
    py=/apps/spack/python/3.8.6/intel/19.1.3.304/pjn2nzkjvqgmjw4hmyz43v5x4jbxjzpk/bin/python
    export incdate=/u/donald.e.lippi/bin/incdate
fi

############### USER INPUT ##################
#date2=2023031923
date1=$(date --date "24 hour ago" "+%Y%m%d%H")
date2=$(date --date "18 hour ago" "+%Y%m%d%H")
expt="rrfs_a_na"
#expt="$expt v0.7.9"
#expt="$expt v0.8.1"
#expt="$expt v0.8.3"
expt="$expt v0.8.5"
datapath="/lfs/h2/emc/da/noscrub/donald.e.lippi/rrfs_mon/ensemble_ob_space_diag/"
figdir="/lfs/h2/emc/ptmp/donald.e.lippi/rrfs_a_diags/figs/"
tmpdir="/lfs/h2/emc/ptmp/donald.e.lippi/rrfs_a_diags/tmp/"
scriptpath="/lfs/h2/emc/da/noscrub/donald.e.lippi/rrfs_mon/ensemble_ob_space_diag/"
unzip="YES"
#unzip="NO"
############END USER INPUT ##################

export ndate=/u/donald.e.lippi/bin/ndate

echo $date1 $date2
year=`echo $date2 | cut -c 1-4`
mon=`echo $date2 | cut -c 5-6`
day=`echo $date2 | cut -c 7-8`
pdy=${year}${mon}${day}
date=$date1

# Unzip diag files and store in tmp directory
if [[ $unzip == "YES" ]]; then
while [[ $date -le $date2 ]]; do
for exp in $expt; do
  cd $tmpdir
  #rm -rf $exp
  mkdir -p $tmpdir/$exp
  cd $datapath/$exp
  #rsync -av --include='*/' --include='diag_conv_uv_ges*' --include='diag_conv_t_ges*' --include='diag_conv_q_ges*' --exclude='*' ${pdy}* $tmpdir/$exp/.
  rsync -a --include='*/' --include='diag_conv_uv_ges*' --include='diag_conv_t_ges*' --include='diag_conv_q_ges*' --exclude='*' ${date} $tmpdir/$exp/.
  cd $tmpdir/$exp
  #gunzip -rk ${pdy}*
  gunzip -rkf ${date}
done
date=`$ndate 1 $date`
done
fi
datapath=$tmpdir

outdir="$figdir/$year/$mon/$day/"
mkdir -p $outdir
cd $outdir
#$py $scriptpath/ensemble_diags_profile.py $date1 $date2 $datapath
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
