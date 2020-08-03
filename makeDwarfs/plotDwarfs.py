"""
Code to plot the injected sources over patch boundaries.
"""
import os
import pandas as pd
import numpy as np
from astropy.io import fits
from deepscan import geometry

# Tracts currently being used for source injections
# Would be nice to read this in from a config file in future.
TRACTS = [9615,  # (GAMA15)
          9697,  # (VVDS)
          9813]  # (COSMOS)


def load_patch_catalogue(tracts=TRACTS):
    """

    """
    # Specify file where the patch catalogue is stored
    path = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
    filename = os.path.join(path, "data", "hsc_patches.csv")

    # Load the patch catalogue
    df = pd.read_csv(filename)

    # Select patches we are interested in
    cond = np.isin(df["tract_id"].values, tracts)
    df = df[cond].reset_index(drop=True)

    return df


def load_galaxy_catalogue(filename):
    """

    """
    data = fits.getdata(filename)
    return data


def get_patch_boxes(df_patch):
    """

    """
    boxes = []
    for i in range(df_patch.shape[0]):
        series = df_patch.iloc[i]
        box = geometry.Box(br=[series["br_ra"], series["br_dec"]],
                           bl=[series["bl_ra"], series["bl_dec"]],
                           tl=[series["tl_ra"], series["tl_dec"]],
                           tr=[series["tr_ra"], series["tr_dec"]])
        boxes.append(box)
    return boxes


def get_galaxy_ellipses(data, size_scaling=3):
    """ """
    n_sources = data["raJ2000"].size
    axrats = data["b_d"]/data["a_d"]
    thetas = data["pa_disk"] * np.pi/180
    sizes = data["DiskHalfLightRadius"] * size_scaling / 3600
    ras = data["raJ2000"] * 180 / np.pi
    decs = data["decJ2000"] * 180 / np.pi

    ellipses = []
    for i in range(n_sources):
        e = geometry.Ellipse(x0=ras[i], y0=decs[i], q=axrats[i], theta=thetas[i], a=sizes[i])
        ellipses.append(e)

    return ellipses
