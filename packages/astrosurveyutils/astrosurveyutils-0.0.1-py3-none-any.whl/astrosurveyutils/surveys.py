import numpy as np
from mocpy import MOC
import matplotlib.pyplot as plt
from astrosurveyutils.utils import get_wcs
from glob import glob
from pathlib import Path
from astropy.coordinates import SkyCoord
import astropy.units as u


class BaseSurvey:

    @property
    def coverage_type(self):
        raise NotImplementedError

    def __init__(self,
                 survey_name: str,
                 filter_name: str,
                 coverage_file: str,
                 lim_mag: float = None,
                 **kwargs):
        self.survey_name = survey_name
        self.coverage_file = coverage_file
        self.filter_name = filter_name
        self.lim_mag = lim_mag
        self.__dict__.update(kwargs)

    def plot_coverage(self):
        raise NotImplementedError


class MOCSurvey(BaseSurvey):
    """
    Class where the survey coverage is given in the healpix multi-order-coverage (MOC)
    format
    See : https://www.ivoa.net/documents/MOC/20190215/WD-MOC-1.1-20190215.pdf
    """

    coverage_type = "moc"

    def plot_coverage(self,
                      ax=None,
                      wcs=None,
                      border=True,
                      **kw_mpl):
        if wcs is None:
            wcs = get_wcs()

        if ax is None:
            plt.figure(figsize=(15, 7))
            ax = plt.subplot(projection=wcs)

        moc = self.get_moc_data()
        moc.fill(ax=ax,
                 wcs=wcs,
                 **kw_mpl)

        if border:
            moc.border(ax=ax, wcs=wcs, alpha=0.7, color="black")
        return ax

    def add_ra_labels(self,
                      ax,
                      wcs,
                      ralabel_dec=-20,
                      ralabel_vals: list = [0, 60, 120, 180, 240, 300],
                      ralabel_labels: list = ['0h', '4h', '8h', '12h', '16h', '20h']
                      ):
        ra_xlabel, ra_ylabel = wcs.all_world2pix(ralabel_vals,
                                                 [ralabel_dec] * len(ralabel_vals), 0)

        for xcrd, ycrd, ra_label in zip(ra_xlabel, ra_ylabel, ralabel_labels):
            ax.text(xcrd, ycrd, ra_label, size=14)

        return ax

    def add_dec_labels(self,
                       ax,
                       wcs,
                       declabel_ra=180,
                       declabel_vals: list = [-60, 60],
                       declabel_labels: list = [r'-60$^{o}$', r'60$^{o}$']
                       ):
        dec_xlabel, dec_ylabel = wcs.all_world2pix([declabel_ra] * len(declabel_vals),
                                                   declabel_vals, 0)

        for xcrd, ycrd, label in zip(dec_xlabel, dec_ylabel, declabel_labels):
            ax.text(xcrd, ycrd, label, size=14)

        return ax

    def get_moc_data(self):
        moc = MOC.from_fits(self.coverage_file)
        return moc

    def contains(self, ra_deg: int | float | list[float],
                 dec_deg: int | float | list[float]) -> np.array(list[bool]):
        if not isinstance(ra_deg, list):
            ra_deg = [ra_deg]
        if not isinstance(dec_deg, list):
            dec_deg = [dec_deg]

        coord = SkyCoord(ra=ra_deg, dec=dec_deg, unit=(u.deg, u.deg))
        moc = self.get_moc_data()
        return moc.contains_skycoords(coord)


known_surveys = []
datadir = Path(__file__).parent.joinpath("data")
maplist = np.sort(glob(f'{datadir.as_posix()}/*-DR*.fits'))
survey_instrument_mapping = {
    'UKIRT': ['dxs', 'gcs', 'gps', 'gps2', 'las', 'las2', 'uds', 'uhs'],
    'VISTA': ['vhs', 'video', 'viking', 'vmc', 'vvv']}

survey_lim_mags = {
    'UKIRT-las': {'Y': 20.834, 'J': 20.51, 'H': 20.19},
    'UKIRT-las2': {'J': 20.51},
    'UKIRT-dxs': {'J': 22.41, 'H': 23.19},
    'UKIRT-gcs': {'Y': 20.734, 'J': 20.51, 'H': 20.19},
    'UKIRT-gps': {'J': 20.71, 'H': 20.39},
    'UKIRT-gps2': {'H': 20.39},
    'UKIRT-uds': {'J': 25.21, 'H': 24.69},
    'UKIRT-uhs': {'J': 20.51},
    'VISTA-viking': {'Y': 22.3, 'J': 22.1, 'H': 21.5},
    'VISTA-vhs': {'Y': 21.2, 'J': 21.2, 'H': 20.6},
    'VISTA-vvv': {'Y': 21.2, 'J': 20.2, 'H': 18.2},
    'VISTA-vmc': {'Y': 21.9, 'J': 21.4},
    'VISTA-video': {'Y': 24.6, 'J': 24.5, 'H': 24.0}
}

survey_database_names = {}
for survey in survey_instrument_mapping['UKIRT']:
    if survey == 'uhs':
        survey_database_names[f'UKIRT-{survey}'] = 'UHSDR1'
    else:
        survey_database_names[f'UKIRT-{survey}'] = 'UKIDSSDR11PLUS'

survey_database_names['VISTA-viking'] = 'VIKINGDR5'
survey_database_names['VISTA-vhs'] = 'VHSDR6'
survey_database_names['VISTA-vvv'] = 'VVVDR5'
survey_database_names['VISTA-vmc'] = 'VMCDR6'
survey_database_names['VISTA-video'] = 'VIDEODR6'

for mapname in maplist:
    survey_name = mapname.split('/')[-1].split('-')[0]
    band_name = mapname.split('/')[-1].split('-')[1]
    survey_instrument = ''
    for instrument in survey_instrument_mapping:
        if survey_name in survey_instrument_mapping[instrument]:
            survey_instrument = instrument

    survey_string = f"{survey_instrument}-{survey_name}"
    full_survey_string = f"{survey_instrument}-{survey_name}-{band_name}"
    known_surveys.append(MOCSurvey(survey_name=full_survey_string,
                                   filter_name=band_name,
                                   coverage_file=mapname,
                                   lim_mag=survey_lim_mags[survey_string][band_name],
                                   wfau_dbname=survey_database_names[survey_string]
                                   ))

known_ukirt_surveys = [x for x in known_surveys if 'UKIRT' in x.survey_name]
known_vista_surveys = [x for x in known_surveys if 'VISTA' in x.survey_name]
