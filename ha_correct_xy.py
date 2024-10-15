#!/usr/bin/env python3

import os
import sys
import astropy.io.fits as pyfits
import numpy

if __name__ == "__main__":

    x = int(sys.argv[1])
    y = int(sys.argv[2])

    xy_dict = dict(x=x, y=y)
    fn_r = "r/0/%(x)d,%(y)d/calexp-r-0-%(x)d,%(y)d.fits" % xy_dict
    fn_n622 = "N662/0/%(x)d,%(y)d/calexp-N662-0-%(x)d,%(y)d.fits" % xy_dict

    hdu_r = pyfits.open(fn_r)
    hdu_r.info()
    img_r = hdu_r[1].data

    hdu_ha = pyfits.open(fn_n622)
    img_ha = hdu_ha[1].data

    # define filter widths
    fw_r = 117
    fw_ha = 14.54

    r_minus_ha = (img_r * fw_r - img_ha * fw_ha) / (fw_r - fw_ha)
    ha_contsub = img_ha - r_minus_ha

    out_hdu = pyfits.HDUList([
        pyfits.PrimaryHDU(header=hdu_r[0].header),
        pyfits.ImageHDU(header=hdu_ha[1].header, data=ha_contsub), ])

    out_fn = sys.argv[3]
    print("writing results to %s" % (out_fn))
    out_hdu.writeto(out_fn, overwrite=True)

    if (len(sys.argv) > 5):
        # this means we can also boost the image
        boost_f = float(sys.argv[4])
        boosted = img_r + boost_f * ha_contsub
        # boosted = r_minus_ha + boost_f * ha_contsub

        boost_hdu = pyfits.HDUList([
            pyfits.PrimaryHDU(header=hdu_r[0].header),
            pyfits.ImageHDU(header=hdu_ha[1].header, data=boosted), ])

        out_fn = sys.argv[5]
        print("writing boosted results to %s" % (out_fn))
        boost_hdu.writeto(out_fn, overwrite=True)
