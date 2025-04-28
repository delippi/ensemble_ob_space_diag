#!/bin/bash

cd /lfs/h2/emc/da/noscrub/donald.e.lippi/rrfs_mon/ensemble_ob_space_diag

machine=`hostname | cut -c 1`
if [[ $machine == "c" || $machine == "d" ]]; then
    py=/apps/spack/python/3.8.6/intel/19.1.3.304/pjn2nzkjvqgmjw4hmyz43v5x4jbxjzpk/bin/python
    export incdate=/u/donald.e.lippi/bin/incdate
fi

############### USER INPUT ##################
#date2=2023031923
date2=$(date --date "1 hour ago" "+%Y%m%d%H")
date1="${date2:0:8}00"
#expt="rrfs_a_na"
expt="v1.0"
#expt="$expt v0.8.5"
datapath="/lfs/h2/emc/da/noscrub/donald.e.lippi/rrfs_mon/ensemble_ob_space_diag/"
figdir="/lfs/h2/emc/ptmp/donald.e.lippi/rrfs_a_diags/figs/"
tmpdir="/lfs/h2/emc/ptmp/donald.e.lippi/rrfs_a_diags/tmp/"
scriptpath="/lfs/h2/emc/da/noscrub/donald.e.lippi/rrfs_mon/ensemble_ob_space_diag/"
unzip="YES"
#unzip="NO"
############END USER INPUT ##################

export ndate=/u/donald.e.lippi/bin/ndate

echo $date1 $date2
date=$date1

set -x
# Unzip diag files and store in tmp directory
while [[ $date -le $date2 ]]; do
echo $date
pdy=${date:0:8}
year=${date:0:4}
mon=${date:4:2}
day=${date:6:2}
cyc=${date:8:2}
for exp in $expt; do
  cd $tmpdir
  mkdir -p $tmpdir/$exp/enkfrrfs.${pdy}
  cd $datapath/$exp/enkfrrfs.${pdy}
  #rsync -av --include='*/' --include='diag_conv_uv_ges*' --include='diag_conv_t_ges*' --include='diag_conv_q_ges*' --exclude='*' ${pdy}* $tmpdir/$exp/.
  #rsync -a --include='*/' --include='diag_conv_uv_ges*' --include='diag_conv_t_ges*' --include='diag_conv_q_ges*' --exclude='*' ${date} $tmpdir/$exp/.
  rsync -a --include='*/' --include='diag_conv_uv_ges*' --include='diag_conv_t_ges*' --include='diag_conv_q_ges*' --exclude='*' ${cyc} $tmpdir/$exp/enkfrrfs.${pdy}/.
  cd $tmpdir/$exp/enkfrrfs.${pdy}
  if [[ $unzip == "YES" ]]; then
    gunzip -rkf ${cyc}/
  fi
done
date=`$ndate 1 $date`
done
datapath=$tmpdir

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
