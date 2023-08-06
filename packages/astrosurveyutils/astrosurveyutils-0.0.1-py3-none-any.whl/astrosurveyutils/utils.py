from astropy.io import fits
from astropy.io.fits import HDUList
import numpy as np
from astropy.wcs import WCS


def fix_mapfile_header(mapname, newfilename):
    hdulist = fits.open(mapname, "update")
    hdu = hdulist[1]
    hdulist[1].header['MOCORDER'] = hdulist[0].header["HPXMOC"]
    newhdu = HDUList(hdulist)
    # newfilename = mapname.split('/')[-1].replace('.fits','_annotated.fits')
    newhdu.writeto(f"{newfilename}", overwrite=True)
    return newfilename


def get_wcs():
    wcs = WCS(naxis=2)
    wcs.wcs.ctype = ["RA---AIT", "DEC--AIT"]
    wcs.wcs.crval = [0.0, 0.0]
    wcs.wcs.cdelt = np.array([-0.675, 0.675])
    wcs.wcs.crpix = [240.5, 120.5]

    return wcs