import os
import pickle

def fig(fig, path, fname, extra_fmt='pdf'):
    """
    Save figure fig with given filename to given path.

    Parameters
    ----------
    fig: figure
        Instance of figure to save
    path: str
        Path to save directory
    fname: str
        Filename of file to save
    """

    # Make dir
    os.makedirs(path, exist_ok=True)
    # Save
    fig.savefig(path + fname + '.png')

    # Create svg directory
    svg_path = path + f'/{extra_fmt}/'
    os.makedirs(svg_path, exist_ok=True)
    # Save
    fig.savefig(svg_path + fname + f'.{extra_fmt}')


def var(var, path, fname):
    """
    Save variable var with given filename to given path.

    Parameters
    ----------
    var: any
        Variable to save
    path: str
        Path to save directory
    fname: str
        Filename of file to save
    """

    # Make dir
    os.makedirs(path, exist_ok=True)

    # Save
    file_path = path + fname
    f = open(file_path, 'wb')
    pickle.dump(var, f)
    f.close()
