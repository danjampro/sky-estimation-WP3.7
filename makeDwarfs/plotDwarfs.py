"""
Code to plot the injected sources over patch boundaries.
"""
import os
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
        box = geometry.box(br=[series["br0"], series["br1"]],
                           bl=[series["bl0"], series["bl1"]],
                           tl=[series["tl0"], series["tl1"]],
                           tr=[series["tr0"], series["tr1"]])
        boxes.append(box)
    return boxes



def get_galaxy_ellipses(data, size_key="DiskHalfLightRadius", size_scaling=1):
    """

    """
    pass
