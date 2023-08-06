

import math
import numpy as np
from typing import Tuple

from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import rdShapeHelpers

from scipy.spatial import ConvexHull
from scipy import constants as const

from gufe import LigandAtomMapping, SmallMoleculeComponent
from gufe.mapping import AtomMapping

import logging

log = logging.getLogger(__name__)

"""
    Metrics
"""
# simple metrics
eukli = lambda x, y: np.sqrt(np.sum(np.square(y - x)))
rms_func = lambda x: np.sqrt(np.mean(np.square(x)))



############# Old IMPLEMENTATION IDEA for pure 3D mapping - To Be deleted
# Working with graphs:
def _build_graph(molA: Chem.Mol, molB: Chem.Mol, max_d: float = 0.95) -> nx.Graph:
    """
    This function builds a full graph, with the exception of filtering for max_d

    Parameters
    ----------
    molA : Chem.Mol
        _description_
    molB :  Chem.Mol
        _description_
    max_d : float, optional
        _description_, by default 0.95

    Returns
    -------
    nx.Graph
        constructed graph
    """

    aA = molA.GetConformer().GetPositions()
    aB = molB.GetConformer().GetPositions()

    G = nx.Graph()

    mol1_length = mol2_start = len(aA)
    mol2_length = len(aB)

    for n in range(mol1_length + mol2_length):
        G.add_node(n)

    edges = []
    for n1, atomPosA in enumerate(aA):
        for n2, atomPosB in enumerate(aB, start=mol2_start):
            dist = vector_eucledean_dist(atomPosA, atomPosB)
            color = "red" if (dist > max_d) else "green"
            e = (
                n1,
                n2,
                {"dist": vector_eucledean_dist(atomPosA, atomPosB), "color": color},
            )
            if dist > max_d:
                continue
            else:
                edges.append((e[0], e[1], vector_eucledean_dist(atomPosA, atomPosB)))
    G.add_weighted_edges_from(edges)

    return G


# modified MST
def _get_mst_chain_graph(graph):
    """
    This function uses a graph and returns its edges in order of an MST according to Kruskal algorithm, but filters the edges such no branching occurs in the tree (actually not really a tree anymore I guess...).
    The 'no-branching' translate to no atom can be mapped twice in the final result.

    Parameters
    ----------
    graph : nx.Graph
        _description_

    Returns
    -------
    dict[int, int]
        resulting atom mapping
    """
    gMap = {}
    min_edges = nx.minimum_spanning_edges(
        nx.MultiGraph(graph), weight="weight", algorithm="kruskal"
    )
    for n1, n2, w, attr in min_edges:
        if (
            n1 in gMap.keys()
            or n1 in gMap.values()
            or n2 in gMap.keys()
            or n2 in gMap.values()
        ):
            continue
        else:
            gMap[n1] = n2

    return gMap


def get_geom_Mapping(
    molA: SmallMoleculeComponent, molB: SmallMoleculeComponent, max_d: float = 0.95
):
    """
    This function is a networkx graph based implementation to build up an Atom Mapping purely on 3D criteria.

    Parameters
    ----------
    molA : SmallMoleculeComponent
        _description_
    molB : SmallMoleculeComponent
        _description_
    max_d : float, optional
        _description_, by default 0.95

    Returns
    -------
    AtomMapping
        resulting 3d Atom mapping
    """
    mol1_length = molA._rdkit.GetNumAtoms()
    G = _build_graph(molA=molA._rdkit, molB=molB._rdkit, max_d=max_d)
    gMap = _get_mst_chain_graph(G)
    map_dict = {
        k % mol1_length: v % mol1_length for k, v in gMap.items()
    }  # cleanup step due to graph build up.
    return AtomMapping(molA, molB, map_dict)
