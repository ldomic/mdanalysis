"""Clock Diagrams  --- :mod:`MDAnalysis.visualization.lintools.clock`
=====================================================================

.. autofunction:: create_clock_diagram
"""

import _io
from typing import List, Optional
import numpy
import io
import matplotlib.pyplot as plt


def create_clock_diagram(resname: str, resid: Optional[str], values: List[int]) -> _io.StringIO:
    """
    This function takes residue name and ID, as well as a list of normalised
    values of some measurement (i.e. between 0 and 1) to create a clock
    diagram for a single residue.

    These diagrams have mainly been used to compare a variable between repetitions
    of simulations - e.g. is the residue always close to a ligand or does the beta factor
    change depending on simulation circumstances, however, other uses could be possible.

    Parameters
    ----------
    resname : str
        Residue name
    resid : Optional[str]
        Residue ID (optional)
    values: List[int]
        List of normalized (0-1) values

    Returns
    -------
    fileobject : _io.StringIO
        A String IO fileobject containing the SVG of the clock diagram


    Examples
    --------
    Generate clock diagram and save it to a file::

        clock_diagram = create_clock_diagram("GLY", "932", [0.3, 0.5, 0.6])
        clock_diagram.seek(0)
        with(open("test.svg", "w")) as f:
            f.write(clock_diagram.getvalue())

    .. image:: GLY_932.svg
    """
    if not all(value >= 0 or value <= 1 for value in values):
        raise ValueError("The value list must contain normalised values between 0 and 1.")
    if len(values) > 5:
        raise ValueError("The value list has to contain no more than 5 items.")

    cmap = plt.get_cmap("viridis_r")

    side = 2.25
    plt.figure(figsize=(side, side))

    rings = []

    ring_number = len(values)
    colors = [cmap(i) for i in numpy.linspace(0, 1, ring_number)]

    if ring_number <= 2:
        width = 0.3
    else:
        width = 0.2

    for idx, pie_value in enumerate(values):
        ring, _ = plt.pie(
            [pie_value, 1 - pie_value],
            radius=0.9 + width * (idx + 1), startangle=90, colors=[colors[idx], "white"], counterclock=False)
        rings.append(ring)
    plt.setp(rings, width=width)

    if not resid:
        plot_center = -side / 2 + 0.9
        plot_text = f'{resname}'
    else:
        plot_center = -side / 2 + 0.67
        plot_text = f'{resname}\n{resid}'

    plt.text(-0.0, plot_center, plot_text, ha='center', size=25, fontweight='bold')
    fileobject = io.StringIO()
    plt.savefig(fileobject, format="svg", dpi=300, transparent=True)
    return fileobject
