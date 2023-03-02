import tictoc
import pyGSI.ensemble_diags
from emcpy.plots.plots import LinePlot, VerticalLine, HorizontalSpan
from emcpy.plots.create_plots import CreatePlot, CreateFigure
import numpy as np
import matplotlib
import sys
import warnings

matplotlib.use("Agg")  # Must be called before importing pyplot
import matplotlib.pyplot as plt

tic = tictoc.tic()

warnings.simplefilter("ignore")


def annotate_int(x, y, z, color, ax):
    for i in range(len(z)):
        value = f"{z[i]:.0f}"
        ax.annotate(value, xy=(x, y[i]), rotation=0, ha='right', color=color, fontsize=7)


expt_names = []
# ********************************************************************
#                        USER SPECIFIED PARAMETERS                  *
# ********************************************************************
n_mem = 30
expt_names.append("rrfs_a_conus")
# expt_names.append("rrfs_a_na")
# expt_names.append("just uncomment for a second experiment")

delt = 1  # 1-hourly data
try:
    date1 = str(sys.argv[1])
    date2 = str(sys.argv[2])
    datapath = "/lfs/h2/emc/ptmp/donald.e.lippi/rrfs_a_diags/"
except IndexError:
    date1 = "2023011819"
    date2 = "2023011900"
    datapath = "../diags/"

# Example if EnKF is only run 18-00Z
# skip_enkf_hours = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18]
skip_enkf_hours = []

# Filtering parameters
hem = None  # GL, NH, TR, SH, CONUS, or None. Overrides lat/lon max/mins filter options.

p_max = 1050.0  # maximum pressure (mb) for including observation in calculations
p_min = 100.0  # minimum pressure (mb) for including observation in calculations

lat_max = 90.0  # maximum latitude (deg N) for including observation in calculations
lat_min = 0.0  # minimum latitude (deg N) for including observation in calculations

lon_max = 360.0  # maximum latitude (deg E) for including observation in calculations
lon_min = 0.0  # minimum latitude (deg E) for including observation in calculations

error_max = 40.0  # maximum error standard deviation for including observation in calculations
error_min = 0.000001  # minimum error standard deviation for including observation in calculations

ob_types = ["u", "v", "t", "q"]  # supported types: u, v, t, and q
codes_uv = [280, 281, 282, 220, 221, 230, 231, 232, 233, 234, 235]
codes_tq = [180, 181, 182, 120, 130, 131, 132, 133, 134, 135]

# Plotting parameters
plot_bias = True  # mean of (forecast - observation)
plot_rms = True  # rms of (F-O)
plot_std_dev = False  # standard deviation of (F-O)
plot_total_spread = True  # total spread (standard deviation)
plot_spread = True  # ensemble spread (standard deviation)
plot_ob_error = True  # observation error standard deviation
plot_cr = True  # consistency ratio (total spread/rmsi)**2
plot_ser = False  # spread error ratio (intraensemble std_dev/ rms)
plot_zero_line = True  # vertical line on zero
plot_one_line = True  # vertical line on one

# Figure settings
suptitle_fontsize = 15  # super title fontsize
title_fontsize = 8  # subplot title fontsizes
xy_label_fontsize = 13  # xy-axes label fontsized
tick_label_fontsize = 10  # xy-axes tick label fontsizes
lw = 1.5  # linewidth
ms = 4  # markersize
ls = ["-", "--", ":", ".-"]  # linestyles: solid, dashed, dotted, dash-dotted

scale_fig_size = 1.2  # =1.2 --> 8*1.2x6*1.2=9.6x7.2 sized fig (1.44 times bigger fig)
levtop = 125
levbot = 925  # plot limits
sigthresh = 0.99  # significance threshold (p-value)
umin = -1.0
umax = 5.0
tmin = -1.0
tmax = 3.00
qmin = -1.0
qmax = 3.00

# ********************************************************************
#                   END OF USER SPECIFIED PARAMETERS                *
# ********************************************************************

for expt_name in expt_names:
    # Call main function - for experiments
    levels, levels_up, levels_down, dates, bias, rms, std_dev, spread, ob_error, total_spread, num_obs_total, num_obs_assim, cr, ser = pyGSI.ensemble_diags.profile(
        datapath,
        date1,
        date2,
        expt_names,
        n_mem,
        delt,
        skip_enkf_hours,
        ob_types,
        codes_uv,
        codes_tq,
        hem,
        p_max,
        p_min,
        lat_max,
        lat_min,
        lon_max,
        lon_min,
        error_max,
        error_min,)

plot1 = CreatePlot()
plot2 = CreatePlot()
plot3 = CreatePlot()
plot4 = CreatePlot()

print("Finish plotting...", end=" ", flush=True)

y = levels
# PLOT 1: WIND
for ob_type in ob_types:
    plt_list = []
    i_o = ob_types.index(ob_type)
    for expt_name in expt_names:
        i_o = ob_types.index(ob_type)
        i_e = expt_names.index(expt_name)

        # add experiment name to legend (this doesn't actually plot anything.
        x = np.NaN * bias[i_o, i_e]
        lp = LinePlot(x, y)
        lp.color = "black"
        lp.linestyle = ls[i_e]
        lp.linewidth = lw
        lp.marker = "o"
        lp.markersize = ms
        lp.alpha = None
        lp.label = "%s" % (expt_name)
        plt_list.append(lp)

    # Plot mean,sd,totalspread,etc.
    for expt_name in expt_names:  # all experiments go on the same figure
        i_e = expt_names.index(expt_name)

        if plot_bias:
            x = bias[i_o, i_e]
            lp = LinePlot(x, y)
            lp.color = "green"
            lp.linestyle = ls[i_e]
            lp.linewidth = lw
            lp.marker = "o"
            lp.markersize = ms
            lp.markerfacecolor = None
            lp.alpha = None
            lp.label = "bias of F-O"
            if i_e > 0:
                lp.label = None
            plt_list.append(lp)

        if plot_rms:
            x = rms[i_o, i_e]
            lp = LinePlot(x, y)
            lp.color = "red"
            lp.linestyle = ls[i_e]
            lp.linewidth = lw
            lp.marker = "o"
            lp.markersize = ms
            lp.alpha = None
            lp.label = "rms of F-O"
            if i_e > 0:
                lp.label = None
            plt_list.append(lp)

        if plot_std_dev:
            x = std_dev[i_o, i_e]
            lp = LinePlot(x, y)
            lp.color = "magenta"
            lp.linestyle = ls[i_e]
            lp.linewidth = lw
            lp.marker = "o"
            lp.markersize = ms
            lp.alpha = None
            lp.label = "std_dev of F-O"
            if i_e > 0:
                lp.label = None
            plt_list.append(lp)

        if plot_spread:
            x = spread[i_o, i_e]
            lp = LinePlot(x, y)
            lp.color = "cyan"
            lp.linestyle = ls[i_e]
            lp.linewidth = lw
            lp.marker = "o"
            lp.markersize = ms
            lp.alpha = None
            lp.label = "spread (std_dev)"
            if i_e > 0:
                lp.label = None
            plt_list.append(lp)

        if plot_ob_error:
            x = ob_error[i_o, i_e]
            lp = LinePlot(x, y)
            lp.color = "orange"
            lp.linestyle = ls[i_e]
            lp.linewidth = lw
            lp.marker = "o"
            lp.markersize = ms
            lp.alpha = None
            lp.label = "ob_error (std_dev)"
            if i_e > 0:
                lp.label = None
            plt_list.append(lp)

        if plot_total_spread:
            x = total_spread[i_o, i_e]
            lp = LinePlot(x, y)
            lp.color = "navy"
            lp.linestyle = ls[i_e]
            lp.linewidth = lw
            lp.marker = "o"
            lp.markersize = ms
            lp.alpha = None
            lp.label = "total spread (std_dev)"
            if i_e > 0:
                lp.label = None
            plt_list.append(lp)

        if plot_cr:
            x = cr[i_o, i_e]
            lp = LinePlot(x, y)
            lp.color = "gray"
            lp.linestyle = ls[i_e]
            lp.linewidth = lw
            lp.marker = "o"
            lp.markersize = ms
            lp.alpha = None
            lp.label = "consistency ratio"
            if i_e > 0:
                lp.label = None
            plt_list.append(lp)

        if plot_ser:
            x = ser[i_o, i_e]
            lp = LinePlot(x, y)
            lp.color = "black"
            lp.linestyle = ls[i_e]
            lp.linewidth = lw
            lp.marker = "o"
            lp.markersize = ms
            lp.alpha = None
            lp.label = "spread error ratio"
            if i_e > 0:
                lp.label = None
            plt_list.append(lp)

        if plot_zero_line:
            lp = VerticalLine(0)
            lp.color = "black"
            lp.linestyle = "-"
            lp.linewidth = 1
            lp.label = None
            plt_list.append(lp)

        if plot_one_line:
            lp = VerticalLine(1)
            lp.color = "black"
            lp.linestyle = "-"
            lp.linewidth = 1
            lp.label = None
            plt_list.append(lp)

        if ob_type == "u":
            plt_list1 = plt_list
        if ob_type == "v":
            plt_list2 = plt_list
        if ob_type == "t":
            plt_list3 = plt_list
        if ob_type == "q":
            plt_list4 = plt_list

common_title = f"{p_max:.1f}-{p_min:.1f} hPa\n{lat_min:.1f}-{lat_max:.1f} degN,  {lon_min:.1f}-{lon_max:.1f} degE\n{error_min:.6f}-{error_max:.1f} err"

plt_list = []
n_plots = 0
for ob_type in ob_types:
    i_o = ob_types.index(ob_type)
    if ob_type == "u":
        plot1.plot_layers = plt_list1
        title = f"Filtered by:\nu{codes_uv}\n{common_title}"
        plot1.add_title(title, loc="left", fontsize=title_fontsize, color="red", style="italic")
        plot1.add_ylabel("pressure (hPa)", fontsize=xy_label_fontsize)
        plot1.add_xlabel("u stats (mps)", fontsize=xy_label_fontsize)
        plot1.set_xlim(umin, umax)
        plot1.set_ylim(levbot, levtop)
        plot1.add_grid()
        plt_list.append(plot1)
        n_plots = n_plots + 1

    if ob_type == "v":
        plot2.plot_layers = plt_list2
        title = f"Filtered by:\nv{codes_uv}\n{common_title}"
        plot2.add_title(title, loc="left", fontsize=title_fontsize, color="red", style="italic")
        plot2.add_xlabel("v stats (mps)", fontsize=xy_label_fontsize)
        plot2.set_xlim(umin, umax)
        plot2.set_ylim(levbot, levtop)
        plot2.add_grid()
        plt_list.append(plot2)
        n_plots = n_plots + 1

    if ob_type == "t":
        plot3.plot_layers = plt_list3
        title = f"Filtered by:\nt{codes_tq}\n{common_title}"
        plot3.add_title(title, loc="left", fontsize=title_fontsize, color="red", style="italic")
        plot3.add_xlabel("t stats (K)", fontsize=xy_label_fontsize)
        plot3.set_xlim(tmin, tmax)
        plot3.set_ylim(levbot, levtop)
        plot3.add_grid()
        plt_list.append(plot3)
        n_plots = n_plots + 1

    if ob_type == "q":
        plot4.plot_layers = plt_list4
        title = f"Filtered by:\nq{codes_tq}\n{common_title}"
        plot4.add_title(title, loc="left", fontsize=title_fontsize, color="red", style="italic")
        plot4.add_xlabel("q stats (g/kg)", fontsize=xy_label_fontsize)
        plot4.set_xlim(qmin, qmax)
        plot4.set_ylim(levbot, levtop)
        plot4.add_grid()
        plt_list.append(plot4)
        plot4.add_legend(loc="upper left", bbox_to_anchor=(1, 1), fancybox=True, framealpha=0.80, ncols=1)
        n_plots = n_plots + 1

# Figure
fig = CreateFigure(nrows=1, ncols=n_plots, figsize=((3.5 * n_plots) * scale_fig_size, 6 * scale_fig_size))
fig.plot_list = plt_list
fig.create_figure()

# Annotate Stats
lannotate = False
lannotate = True
if lannotate:
    annotate_int(umax, y, num_obs_assim[0, i_e, :], "gray", plt.subplot(141))
    annotate_int(umax, y, num_obs_assim[1, i_e, :], "gray", plt.subplot(142))
    annotate_int(tmax, y, num_obs_assim[2, i_e, :], "gray", plt.subplot(143))
    annotate_int(qmax, y, num_obs_assim[3, i_e, :], "gray", plt.subplot(144))

sdate = dates[0]
edate = dates[-1]
fig.add_suptitle(f"Ensemble DA Obs Space Diagnostics ({sdate}-{edate})", ha="center", fontsize=suptitle_fontsize)
fig.tight_layout()  # must go after add_suptitle
fig.save_figure(f"./obs_diag_profiles_{sdate}-{edate}.png")

# Calculate time to run script
tictoc.toc(tic, "Done. ")
