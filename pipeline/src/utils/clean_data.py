import numpy as np

def get_eeg_data(f):
    return np.array(f['result']['data'])

def get_times(f):
    return np.array(f['result']['times'])

def get_electrode_coords(f, coords = "euclidian"):
    base = f['result']['chanlocs']
    if coords == "euclidian":
        x = [base[e[0]][:][0][0] for e in base['X']] 
        y = [base[e[0]][:][0][0] for e in base['Y']]
        z = [base[e[0]][:][0][0] for e in base['Z']] 
        return zip(x, y, z)
    elif coords == "spherical":
        t = [base[e[0]][:][0][0] for e in base['sph_theta']]
        p = [base[e[0]][:][0][0] for e in base['sph_phi']]
        r = [base[e[0]][:][0][0] for e in base['sph_radius']]
        return zip(t, p, r)
    else:
        raise Exception("Pick spherical or euclidian coordinates")

    
