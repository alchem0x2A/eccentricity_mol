from ase.io import read, write
from .calc import eccentricity_pts

def ecc_atoms(atoms):
    """Return scalar eccentricity of a given ase.atoms.Atoms object"""
    try:
        ec = eccentricity_pts(atoms.positions)
        return ec
    except Exception:
        return 0                # An error


def sort_images(images, small_first=True, save_ecc=True):
    """Sort images according to the eccentricity, 
       by default the images with smallest eccentricity first
    """
    imgs_ = images.copy()
    imgs_.sort(key=ecc_atoms, reverse=(not small_first))
    scores = list(map(ecc_atoms, imgs_))
    # Save the eccentricity info inside the atoms.info field
    if save_ecc:
        for ec, i in enumerate(scores):
            imgs_[i].info.update(eccentricity=ec)
    return imgs_, scores
