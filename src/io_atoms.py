from ase.io import read, write
from .calc import eccentricity_pts
from pathlib import Path

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
        for i, ec in enumerate(scores):
            imgs_[i].info.pop("")
            imgs_[i].info.update(eccentricity=ec)
    return imgs_, scores

def convert(infile, outfile=None, force_xyz=True, **kwargs):
    try:
        infile = Path(infile)
        images = read(infile, index=":") # read all trajectories
    except (IOError, FileNotFoundError):
        print("Cannot read input file")
        return False

    if outfile is None:
        outfile = infile.with_suffix(".xyz")
    else:
        outfile = Path(outfile)
        if (outfile.suffix != ".xyz") and (not force_xyz):
            print(" I'll try to save with {0} format anyway, however .xyz format is recommended.".format(outfile.suffix))
        else:
            outfile = outfile.with_suffix(".xyz")

    images_, scores = sort_images(images, **kwargs)
    write(outfile.resolve().as_posix(), images_)
