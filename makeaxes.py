import numpy as np
import matplotlib.pyplot as plt
from scipy.io import readsav

# Utilities
def iscbarkey(k):
    return k.endswith("_cb")
def plotkeys(axd):
    return (k for k in axd.keys() if not iscbarkey(k))
def cbarkeys(axd):
    return (k for k in axd.keys() if iscbarkey(k))
def plotaxs(axd):
    return (ax for k,ax in axd.items() if not iscbarkey(k))
def cbaraxs(axd):
    return (ax for k,ax in axd.items() if iscbarkey(k))
def plotitems(axd):
    return ((k,ax) for k,ax in axd.items() if not iscbarkey(k))
def cbaritems(axd):
    return ((k,ax) for k,ax in axd.items() if iscbarkey(k))

def build_figure():
    """
    build_figure() sets up the basic axes that will be populated in user code.
    """
    fig, axd = plt.subplot_mosaic(
        [['B', '.'],
         ['E', '.'],
         ['waves1', 'waves1_cb'],
         ['waves2', 'waves2_cb'],
         ['langmuir', '.'],
         ['EPLAS', 'EPLAS_cb'],
         ['mainPIPs', 'mainPIPs_cb'],
         ['mainERPA', '.'],
         ['leadingPIP1', 'leadingPIP1_cb'],
         ['leadingPIP2', 'leadingPIP2_cb'],
         ['trailingERPA1', '.'],
         ['trailingERPA2', '.']
        ],
        figsize=(9,9),
        dpi=100,
        gridspec_kw={
            "left":   0.05,
            "right":  0.95,
            "top":    0.95,
            "bottom": 0.05,
            "hspace": 0.2,
            "wspace": 0.02,
            "width_ratios": [97,3]
        }
    )
    # I want to share axes on just the column of plots, not the colorbar axes.
    # In subplot_mosaic() the sharex argument is all or nothing, so we need a workaround.
    shared_axs = list(plotaxs(axd))
    # Yes, shared_axs[0] is the `self` agument to get_shared_x_axes, and also
    # the first agument to join, and also the *second* argument to join (becuase of the splat).
    # According to StackOverflow, that's the correct way to make all the axes in the list mutually shared ¯\_(ツ)_/¯.
    # Making axes shared after they're constructed is not the normal way of doing things.
    # It might have been better to use something other than subplot_mosaic for this, but
    # I wanted to control the colorbar axes, so subplot_mosaic made sense.
    shared_axs[0].get_shared_x_axes().join(shared_axs[0], *shared_axs)

    # Turn off x tick labels for all but the bottom plot (normally, sharex would do this automatically)
    for k,ax in plotitems(axd):
        if k != "trailingERPA2":
            ax.set_xticklabels([])

    # Turn off ticks and tick labels for the colorbars
    # This isn't required since Figure.colorbar() will set all the ticks and labels anyway, but
    # it makes the blank plot look cleaner until all the panels are populated
    for ax in cbaraxs(axd):
        ax.set_xticks([])
        ax.set_yticks([])
        ax.set_xticklabels([])
        ax.set_xticklabels([])

    # Labeling
    axd["trailingERPA2"].set_xlabel("Time (s)")
    axd["B"].set_title("KiNET-X Data Products")

    return fig, axd

def annotate_axes(ax, text, fontsize=18):
    ax.text(0.5, 0.5, text, transform=ax.transAxes,
        ha="center", va="center", fontsize=fontsize, color="darkgrey"
    )

fig, axd = build_figure()

# B
# TODO

# E
# TODO: Time is "seconds since T0" according to a note in the data file.
# There is an array in the datafile that is called 't0' and it has the value array([0., 44., 0.]).
# Does that mean T0 is 00:44:00.0 UT? I don't know.
# TODO: I want the de-spun values
f = readsav("Data/DC_E_Field/52007_TM2_S1-DCEfield_V12D_V34D_V15D_mvm_NBarnes.sav")
axd['E'].plot(f.times_s, f.v12d_s, f.times_s, f.v34d_s, f.times_s, f.v15d_s)
axd['E'].set_ylabel("E (mV/m)")

# Waves
# TODO

# Parallel Waves
# TODO

# Langmuir Probe Density
# TODO: A note in the data file says "Density values may require additional calibration"
# TODO: Time is seconds from 00:44:00.0 UT
f = readsav("Data/Langmuir_Probe/KiNETX_sweptLP_fixedbiasdensity.sav")
axd["langmuir"].plot(f.time_ionsaturation, f.density_ionsaturation)
axd["langmuir"].set_ylabel("Density (cm^-3)")

# EPLAS
# TODO

# Main PIPs
# TODO
# I'm imagining this being some kind of summary plot, but there are a lot of PIPs,
# and they have complicated fields of view, so there's lots of things that could
# go here

# Main ERPA
# TODO
# What are the data products for ERPAs? The main one is electron temperature, but
# what about electron density? Do we care about the differential spectra? Or
# approximate payload potential? What is +4V bias skin current?
# TODO: data includes a tentative time axis, but I don't know what T0 is.


axd["trailingERPA2"].set_xlim([590, 630])
for ax in plotaxs(axd):
    annotate_axes(ax, ax.get_label())

plt.show()
