# Calculate the eccentricity of minimal disclosing ellipsoid of a point swamp
import numpy as np
from numpy import linalg


def eccentricity_pts(*args, **kwargs):
    """Calculate the eccentricity of points
    Returns:
    eccentricity = min(radii) / max(radii) of ellipsoid
    """
    c, r, rot = min_ellips_pts(*args, **kwargs)
    return np.min(r) / np.max(r)


def min_ellips_pts(P=None, tolerance=0.01):
    """ Find the minimum volume ellipsoid which holds all the points

    Based on
    http://www.mathworks.com/matlabcentral/fileexchange/9542
    http://cctbx.sourceforge.net/current/python/scitbx.math.minimum_covering_ellipsoid.html
    https://github.com/minillinim/ellipsoid

    Here, P is a numpy array of N dimensional points like this:
    P = [[x,y,z,...], <-- one point per line
         [x,y,z,...],
         [x,y,z,...]]

    Returns:
    center, radii, rotation
    """
    N, d = np.shape(P)
    d = float(d)

    # Q will be our working array
    Q = np.vstack([np.copy(P.T), np.ones(N)]) 
    QT = Q.T

    # initializations
    err = 1.0 + tolerance
    u = (1.0 / N) * np.ones(N)

    # Khachiyan Algorithm
    while err > tolerance:
        V = np.dot(Q, np.dot(np.diag(u), QT))
        M = np.diag(np.dot(QT , np.dot(linalg.inv(V), Q)))    # M the diagonal vector of an NxN matrix
        j = np.argmax(M)
        maximum = M[j]
        step_size = (maximum - d - 1.0) / ((d + 1.0) * (maximum - 1.0))
        new_u = (1.0 - step_size) * u
        new_u[j] += step_size
        err = np.linalg.norm(new_u - u)
        u = new_u

    # center of the ellipse 
    center = np.dot(P.T, u)

    # the A matrix for the ellipse
    A = linalg.inv(
                   np.dot(P.T, np.dot(np.diag(u), P)) - 
                   np.array([[a * b for b in center] for a in center])
                   ) / d

    # Get the values we'd like to return
    U, s, rotation = linalg.svd(A)
    radii = 1.0/np.sqrt(s)

    return center, radii, rotation
