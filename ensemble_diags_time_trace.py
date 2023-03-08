import tictoc
import pyGSI.ensemble_diags
from emcpy.plots.plots import LinePlot, HorizontalLine
from emcpy.plots.create_plots import CreatePlot, CreateFigure
import numpy as np
import matplotlib
import sys

matplotlib.use("Agg")  # Must be called before importing pyplot
import matplotlib.pyplot as plt

tic = tictoc.tic()


def annotate_int(x, y, color, ax):
    for i in range(len(x)):
        value = f"{y[i]:.0f}"
        ax.annotate(value, xy=(x[i], y[i]), rotation=60, ha='center', color=color)


def annotate_float(x, y, color, ax):
    for i in range(len(x)):
        value = f"{y[i]:.2f}"
        ax.annotate(value, xy=(x[i], y[i]), rotation=60, ha='center', color=color)


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
    #datapath = "/lfs/h2/emc/ptmp/donald.e.lippi/rrfs_a_diags/"
    datapath = str(sys.argv[3])
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
plot_zero_line = True  # horizontal line on zero
plot_one_line = True  # horizontal line on one

# Figure settings
suptitle_fontsize = 15  # super title fontsize
title_fontsize = 9  # subplot title fontsizes
xy_label_fontsize = 13  # xy-axes label fontsized
tick_label_fontsize = 10  # xy-axes tick label fontsizes
lw = 1.5  # linewidth
ms = 4  # markersize
ls = ["-", "--", ":", ".-"]  # linestyles: solid, dashed, dotted, dash-dotted

scale_fig_size = 1.2  # =1.2 --> 8*1.2x6*1.2=9.6x7.2 sized fig (1.44 times bigger fig)
umin = -0.5
umax = 3.5
tmin = -0.5
tmax = 2.00
qmin = -0.5
qmax = 2.00

# ********************************************************************
#                   END OF USER SPECIFIED PARAMETERS                *
# ********************************************************************

# Calculate all observation space statistics
dates, bias, rms, std_dev, spread, ob_error, total_spread, num_obs_total, num_obs_assim, cr, ser = pyGSI.ensemble_diags.time_trace(
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
# ****************************************************************************

# Define the x-axis (time UTC)
x_str = [str(item).zfill(4) for item in range(0, 2400, 100)]
x = [int(item) for item in x_str]

# Prepare for plotting
for ob_type in ob_types:  # make a new figure for each observation type
    i_o = ob_types.index(ob_type)
    if ob_type == "u" or ob_type == "v":
        codes = codes_uv
        units = 'm/s'
        ymin = umin
        ymax = umax
    elif ob_type == "t":
        codes = codes_tq
        units = 'K'
        ymin = tmin
        ymax = tmax
    elif ob_type == "q":
        codes = codes_tq
        units = 'g/kg'
        ymin = qmin
        ymax = qmax

    plot1 = CreatePlot()
    plt_list = []

    for expt_name in expt_names:
        i_o = ob_types.index(ob_type)
        i_e = expt_names.index(expt_name)

        # add experiment name to legend (this doesn't actually plot anything.
        y = np.NaN * bias[i_o, i_e, :]
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
            y = bias[i_o, i_e, :]
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
            y = rms[i_o, i_e, :]
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
            y = std_dev[i_o, i_e, :]
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
            y = spread[i_o, i_e, :]
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
            y = ob_error[i_o, i_e, :]
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
            y = total_spread[i_o, i_e, :]
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
            y = cr[i_o, i_e, :]
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
            y = ser[i_o, i_e, :]
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
            lp = HorizontalLine(0)
            lp.color = "black"
            lp.linestyle = "-"
            lp.linewidth = 1
            lp.label = None
            plt_list.append(lp)

        if plot_one_line:
            lp = HorizontalLine(1)
            lp.color = "black"
            lp.linestyle = "-"
            lp.linewidth = 1
            lp.label = None
            plt_list.append(lp)


    # Plot number of obs
    plot2 = CreatePlot()
    plt_list2 = []
    for expt_name in expt_names:
        # Total number of observations
        i_e = expt_names.index(expt_name)
        y = num_obs_total[i_o, i_e, :]
        lp = LinePlot(x, y)
        lp.color = "black"
        lp.linestyle = ls[i_e]
        lp.linewidth = lw
        lp.marker = "o"
        lp.markersize = ms
        lp.alpha = None
        lp.label = "total"
        if i_e > 0:
            lp.label = None
        plt_list2.append(lp)

        # Number of observations assimilated
        y = num_obs_assim[i_o, i_e, :]
        lp = LinePlot(x, y)
        lp.color = "gray"
        lp.linestyle = ls[i_e]
        lp.linewidth = lw
        lp.marker = "o"
        lp.markersize = ms
        lp.alpha = None
        lp.label = "assim"
        if i_e > 0:
            lp.label = None
        plt_list2.append(lp)

    ncols = 1  # len(expt_names)

    # Plot 1
    plot1.plot_layers = plt_list
    title = f"Filtered by:\n{ob_type}{codes},  {p_max:.1f}-{p_min:.1f} hPa,  {lat_min:.1f}-{lat_max:.1f} degN,  {lon_min:.1f}-{lon_max:.1f} degE,  {error_min:.6f}-{error_max:.1f} err"

    plot1.add_title(title, loc="left", fontsize=title_fontsize, color="red", style="italic")
    plot1.add_ylabel(f"stats ({units})", fontsize=xy_label_fontsize)
    plot1.add_grid()
    plot1.set_xticks(x)
    plot1.set_xticklabels(x_str, rotation=90)
    plot1.set_ylim(ymin, ymax)
    plot1.add_legend(loc="upper left", bbox_to_anchor=(1, 1), fancybox=True, framealpha=0.80, ncols=ncols)

    # Plot 2
    plot2.plot_layers = plt_list2
    plot2.add_xlabel("Time (UTC)", fontsize=xy_label_fontsize)
    plot2.add_ylabel("Number of Observations", fontsize=xy_label_fontsize)
    plot2.add_grid()
    plot2.set_xticks(x)
    plot2.set_xticklabels(x_str, rotation=90)
    plot2.add_legend(loc="upper left", bbox_to_anchor=(1, 1), fancybox=True, framealpha=0.80, ncols=ncols)

    # Figure
    fig = CreateFigure(nrows=2, ncols=1, figsize=((8 + ncols * 1) * scale_fig_size, 6 * scale_fig_size))
    fig.plot_list = [plot1, plot2]

    sdate = dates[0]
    edate = dates[-1]

    fig.create_figure()  # must go before add_suptitle

    # Annotate Stats
    lannotate = False
    lannotate = True
    if lannotate:
        # Plot 1 - annotations
        # annotate_float(x, bias[i_o, i_e, :], "green", plt.subplot(211))
        # annotate_float(x, rms[i_o, i_e, :], "red", plt.subplot(211))
        # annotate_float(x, std_dev[i_o, i_e, :], "magenta", plt.subplot(211))
        # annotate_float(x, spread[i_o, i_e, :], "cyan", plt.subplot(211))
        # annotate_float(x, ob_error[i_o, i_e, :], "orange", plt.subplot(211))
        # annotate_float(x, total_spread[i_o, i_e, :], "navy", plt.subplot(211))
        # annotate_float(x, cr[i_o, i_e, :], "gray", plt.subplot(211))
        # annotate_float(x, ser[i_o, i_e, :], "black", plt.subplot(211))

        # Plot 2 - annotations
        annotate_int(x, num_obs_assim[i_o, i_e, :], "gray", plt.subplot(212))
        # annotate_int(x, num_obs_total[i_o, i_e, :], "black", plt.subplot(212))

    fig.add_suptitle(f"{ob_type}: Ensemble DA Obs Space Diagnostics ({sdate}-{edate})", ha="center", fontsize=suptitle_fontsize)
    fig.tight_layout()  # must go after add_suptitle
    fig.save_figure(f"./obs_diag_{sdate}-{edate}_{ob_type}.png")

# Calculate time to run script
tictoc.toc(tic, "Done. ")
