#    A collection of tools to interface with manually traced and autosegmented
#    data in FAFB.
#
#    Copyright (C) 2019 Philipp Schlegel
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
import copy
import itertools
import json
import navis
import pymaid
import pyperclip
import requests
import uuid
import webbrowser

import matplotlib.colors as mcl
import numpy as np
import pandas as pd
import seaborn as sns

from urllib.parse import urlparse, parse_qs, quote

from . import utils
from .segmentation import neuron_to_segments
from ..utils import make_iterable

__all__ = ['decode_url', 'encode_url']

NGL_URL = 'https://ngl.flywire.ai'
MINIMAL_SCENE = {'layers': [{'source': 'precomputed://gs://microns-seunglab/drosophila_v0/alignment/image_rechunked',
                             'type': 'image',
                             'blend': 'default',
                             'shaderControls': {},
                             'name': 'Production-image'
                             },
                            {'source': 'graphene://https://prod.flywire-daf.com/segmentation/1.0/{dataset}',
                             'type': 'segmentation_with_graph',
                             'selectedAlpha': 0.14,
                             'segments': [],
                             'skeletonRendering': {'mode2d': 'lines_and_points', 'mode3d': 'lines'},
                             'graphOperationMarker': [{'annotations': [], 'tags': []},
                                                      {'annotations': [], 'tags': []}],
                             'pathFinder': {'color': '#ffff00',
                                            'pathObject': {'annotationPath': {'annotations': [], 'tags': []},
                                                           'hasPath': False}
                                            },
                             'name': 'Production-segmentation_with_graph'},
                              {"source": "precomputed://gs://flywire_neuropil_meshes/whole_neuropil/brain_mesh_v141.surf",
                               "type": "segmentation",
                               "objectAlpha": 0.2,
                               "ignoreSegmentInteractions": True,
                               "segmentColors": { "1": "#808080"},
                               "segments": ["1"],
                                "skeletonRendering": {"mode2d": "lines_and_points",
                                                      "mode3d": "lines"},
                               "name": "brain_mesh_v141.surf",
                               "visible": True
                                }],
                 'navigation': {'pose': {'position': {'voxelSize': [4, 4, 40],
                                                      'voxelCoordinates': [118073, 57192, 4070]}},  # default
                                'zoomFactor': 2.8},  # Zoom in 2d
                 'perspectiveOrientation': [0, 0, 0, 1],  # This is a frontal perspective in 3d
                 'perspectiveZoom': 21000,  # Zoom in 3d
                 'jsonStateServer': 'https://globalv1.flywire-daf.com/nglstate/post',
                 'selectedLayer': {'layer': 'Production-segmentation_with_graph',
                                   'visible': True},
                 'layout': 'xy-3d'}
STATE_URL = "https://globalv1.flywire-daf.com/nglstate"
session = None


def encode_url(segments=None, annotations=None, coords=None, skeletons=None,
               seg_colors=None, seg_groups=None, invis_segs=None,
               dataset='production', scene=None, ngl_url=None,
               open_browser=False, to_clipboard=False, short=True):
    """Encode data as FlyWire neuroglancer scene.

    Parameters
    ----------
    segments :      int | list of int, optional
                    Segment IDs to have selected.
    annotations :   (N, 3) array or dict of {name: (N, 3) array}, optional
                    Array or dict of xyz coordinates that will be added as
                    annotation layer(s). Should be in voxel coordinates. If you
                    need more control over this, see :func:`fafbseg.flywire.add_annotation_layer`.
    coords :        (3, ) array, optional
                    (X, Y, Z) voxel coordinates to center on.
    skeletons :     navis.TreeNeuron | navis.CatmaidNeuron | NeuronList
                    Skeleton(s) to add as annotation layer(s).
    seg_colors :    str | tuple | list | dict, optional
                    Single color (name or RGB tuple), or list or dictionary
                    mapping colors to ``segments``. Can also be a numpy array
                    of labels which will be automatically turned into colors.
    seg_groups :    list | dict, optional
                    List or dictionary mapping segments to groups. Each group
                    will get its own annotation layer.
    invis_segs :    int | list, optional
                    Selected but invisible segments.
    dataset :       'production' | 'sandbox'
                    Segmentation dataset to use.
    scene :         dict | str, optional
                    If you want to edit an existing scene, provide it either
                    as already decoded dictionary or as string that can be
                    interpreted by :func:`fafbseg.flywire.decode_url`.
    open_brower :   bool
                    If True, will open the url in a new tab of your webbrowser.
                    By default, we will first try to open in Google Chrome and
                    failing that fall back to your default browser.
    to_clipboard :  bool
                    If True, will copy URL to clipboard.
    short :         bool
                    If True, will make a shortened URL.

    Returns
    -------
    url :           str

    """
    # Translate "production"/"sandbox" into the corresponding dataset
    dataset = utils.FLYWIRE_DATASETS.get(dataset, dataset)

    # If scene provided as str, decode into dictionary
    if isinstance(scene, str):
        scene = decode_url(scene, ret='full')
    elif isinstance(scene, dict):
        # Do not modify original scene! We need to deepcopy here!
        scene = copy.deepcopy(scene)

    # If no scene provided, prepare the minimal scene
    if not scene:
        # Do not modify original scene! We need to deepcopy here!
        scene = copy.deepcopy(MINIMAL_SCENE)
        scene['layers'][1]['source'] = scene['layers'][1]['source'].format(dataset=dataset)

        if dataset == utils.FLYWIRE_DATASETS['sandbox']:
            scene['layers'][1]['name'] = 'sandbox-segmentation-FOR PRACTICE ONLY'
            scene['selectedLayer']['layer'] = 'sandbox-segmentation-FOR PRACTICE ONLY'

    # At this point scene HAS to be a dictionary
    if not isinstance(scene, dict):
        raise TypeError(f'Expected `scene` as dict or str, got "{type(scene)}"')

    # First add selected segments
    seg_layer_ix = [i for i, l in enumerate(scene['layers']) if (l['type'] == 'segmentation_with_graph' or l['name'] == 'flywire_v141_m526')]

    if not seg_layer_ix:
        scene['layers'].append(MINIMAL_SCENE['layers'][1].copy())
        scene['layers'][-1]['source'] = scene['layers'][-1]['source'].format(dataset=dataset)
        seg_layer_ix = -1

        if dataset == utils.FLYWIRE_DATASETS['sandbox']:
            scene['layers'][-1]['name'] = 'sandbox-segmentation-FOR PRACTICE ONLY'
    else:
        seg_layer_ix = seg_layer_ix[0]

    # If provided, add segments
    if not isinstance(segments, type(None)):
        # Force to list and make strings
        segments = make_iterable(segments, force_type=str).tolist()

        # Add to, not replace already selected segments
        if isinstance(seg_groups, type(None)):
            present = scene['layers'][seg_layer_ix].get('segments', [])
            scene['layers'][seg_layer_ix]['segments'] = present + segments


    if not isinstance(seg_groups, type(None)):
        if not isinstance(seg_groups, dict):
            if not navis.utils.is_iterable(seg_groups):
                raise TypeError(f'`seg_groups` must be dict or iterable, got "{type(seg_groups)}"')
            if len(seg_groups) != len(segments):
                raise ValueError(f'Got {len(seg_groups)} groups for {len(segments)} segments.')

            seg_groups = np.asarray(seg_groups)

            if seg_groups.dtype != object:
                seg_groups = [f'group_{i}' for i in seg_groups]

            # Turn into dictionary
            seg_groups = dict(zip(segments, seg_groups))

        # Check if dict is {id: group} or {group: [id1, id2, id3]}
        is_list = [isinstance(v, (list, tuple, set, np.ndarray)) for v in seg_groups.values()]
        if not any(is_list):
            groups = {}
            for s, g in seg_groups.items():
                if not isinstance(g, str):
                    raise TypeError(f'Expected seg groups to be strings, got {type(g)}')
                groups[g] = groups.get(g, []) + [s]
        elif all(is_list):
            groups = seg_groups
        else:
            raise ValueError('`seg_groups` appears to be a mix of {id: group} '
                             'and {group: [id1, id2, id3]}.')

        for g in groups:
            scene['layers'].append(copy.deepcopy(scene['layers'][seg_layer_ix]))
            scene['layers'][-1]['name'] = f'{g}'
            scene['layers'][-1]['segments'] = [str(s) for s in groups[g]]
            scene['layers'][-1]['visible'] = False

    if not isinstance(invis_segs, type(None)):
        # Force to list and make strings
        invis_segs = make_iterable(invis_segs, force_type=str).tolist()

        # Add to, not replace already selected segments
        present = scene['layers'][seg_layer_ix].get('hiddenSegments', [])
        scene['layers'][seg_layer_ix]['hiddenSegments'] = present + invis_segs

    # All present segments
    seg_layer = scene['layers'][seg_layer_ix]
    #all_segs = seg_layer.get('segments', []) + seg_layer.get('hiddenSegments', [])
    all_segs = segments

    # See if we need to assign colors
    if not isinstance(seg_colors, type(None)):
        if isinstance(seg_colors, str):
            seg_colors = {s: seg_colors for s in all_segs}
        elif isinstance(seg_colors, tuple) and len(seg_colors) == 3:
            seg_colors = {s: seg_colors for s in all_segs}
        elif isinstance(seg_colors, (np.ndarray, pd.Series, pd.Categorical)) and seg_colors.ndim == 1:
            if len(seg_colors) != len(all_segs):
                raise ValueError(f'Got {len(seg_colors)} colors for {len(all_segs)} segments.')

            uni_ = np.unique(seg_colors)
            if len(uni_) > 20:
                # Note the +1 to avoid starting and ending on the same color
                pal = sns.color_palette('hls', len(uni_) + 1)
                # Shuffle to avoid having two neighbouring clusters with
                # similar colours
                rng = np.random.default_rng(1985)
                rng.shuffle(pal)
            elif len(uni_) > 10:
                pal = sns.color_palette('tab20', len(uni_))
            else:
                pal = sns.color_palette('tab10', len(uni_))
            _colors = dict(zip(uni_, pal))
            seg_colors = {s: _colors[l] for s, l in zip(all_segs, seg_colors)}
        elif not isinstance(seg_colors, dict):
            if not navis.utils.is_iterable(seg_colors):
                raise TypeError(f'`seg_colors` must be dict or iterable, got "{type(seg_colors)}"')
            if len(seg_colors) < len(all_segs):
                raise ValueError(f'Got {len(seg_colors)} colors for {len(all_segs)} segments.')

            # Turn into dictionary
            seg_colors = dict(zip(all_segs, seg_colors))

        # Turn colors into hex codes
        # Also make sure keys are int (not np.int64)
        # Not sure but this might cause issue on Windows systems
        # But JSON doesn't like np.int64... so we're screwed
        seg_colors = {str(s): mcl.to_hex(c) for s, c in seg_colors.items()}

        # Assign colors
        scene['layers'][seg_layer_ix]['segmentColors'] = seg_colors

        # Also color each groups
        if not isinstance(seg_groups, type(None)):
            for l in scene['layers']:
                if l['name'] in groups:
                    l['segmentColors'] = {s: seg_colors[s] for s in l['segments']}

    # Set coordinates if provided
    if not isinstance(coords, type(None)):
        coords = np.asarray(coords)
        if not coords.ndim == 1 and coords.shape[0] == 3:
            raise ValueError('Expected coords to be an (3, ) array of x/y/z '
                             f'coordinates, got {coords.shape}')
        scene['navigation']['pose']['position']['voxelCoordinates'] = coords.round().astype(int).tolist()

    if not isinstance(annotations, type(None)):
        if isinstance(annotations, np.ndarray):
            scene = add_annotation_layer(annotations, scene)
        elif isinstance(annotations, dict):
            for l, an in annotations.items():
                scene = add_annotation_layer(an, scene, name=l)

    if not isinstance(skeletons, type(None)):
        if isinstance(skeletons, navis.NeuronList):
            for n in skeletons:
                scene = add_skeleton_layer(n, scene)
        else:
            scene = add_skeleton_layer(skeletons, scene)

    if short:
        url = shorten_url(scene)
    else:
        scene_str = json.dumps(scene).replace("'",
                                              '"').replace("True",
                                                           "true").replace("False",
                                                                           "false")
        if not ngl_url:
            ngl_url = NGL_URL

        url = f'{ngl_url}/#!{quote(scene_str)}'

    if open_browser:
        try:
            wb = webbrowser.get('chrome')
        except BaseException:
            wb = webbrowser

        wb.open_new_tab(url)

    if to_clipboard:
        pyperclip.copy(url)
        print('URL copied to clipboard.')

    return url


def add_skeleton_layer(x, scene):
    """Add skeleton as new layer to scene.

    Parameters
    ----------
    x :             navis.TreeNeuron | pymaid.CatmaidNeuron | int
                    Neuron to generate a URL for. Integers are interpreted as
                    CATMAID skeleton IDs. CatmaidNeurons will automatically be
                    transformed to FlyWire coordinates. Neurons are expected to
                    be in nanometers and will be converted to voxels.
    scene :         dict
                    Scene to add annotation layer to.

    Returns
    -------
    modified scene : dict

    """
    if not isinstance(scene, dict):
        raise TypeError(f'`scene` must be dict, got "{type(scene)}"')
    scene = scene.copy()

    if not isinstance(x, (navis.TreeNeuron, navis.NeuronList, pd.DataFrame)):
        x = pymaid.get_neuron(x)

    if isinstance(x, navis.NeuronList):
        if len(x) > 1:
            raise ValueError(f'Expected a single neuron, got {len(x)}')

    #if isinstance(x, pymaid.CatmaidNeuron):
    #    x = xform.fafb14_to_flywire(x, coordinates='nm')

    if not isinstance(x, (navis.TreeNeuron, pd.DataFrame)):
        raise TypeError(f'Expected skeleton, got {type(x)}')

    if isinstance(x, navis.TreeNeuron):
        nodes = x.nodes
    else:
        nodes = x

    # Generate list of segments
    not_root = nodes[nodes.parent_id >= 0]
    loc1 = not_root[['x', 'y', 'z']].values
    loc2 = nodes.set_index('node_id').loc[not_root.parent_id.values,
                                          ['x', 'y', 'z']].values
    stack = np.dstack((loc1, loc2))
    stack = np.transpose(stack, (0, 2, 1))

    stack = stack / [4, 4, 40]

    return add_annotation_layer(stack, scene)


def add_annotation_layer(annotations, scene, name=None, connected=False):
    """Add annotations as new layer to scene.

    Parameters
    ----------
    annotations :   numpy array
                    Coordinates [in 4x4x40 voxels] for annotations. The format
                    determines the type of annotation::
                        - point: (N, 3) of x/y/z coordinates
                        - line: (N, 2, 3) pairs x/y/z coordinates for start and
                          end point for each line segment
                        - ellipsoid: (N, 4) of x/y/z/radius

    scene :         dict
                    Scene to add annotation layer to.
    name :          str
                    Name of the annotation layer.
    connected :     bool (TODO)
                    If True, point annotations will be treated as a segment of
                    connected points.

    Returns
    -------
    modified scene : dict

    """
    if not isinstance(scene, dict):
        raise TypeError(f'`scene` must be dict, got "{type(scene)}"')
    scene = scene.copy()

    annotations = np.asarray(annotations)

    # Generate records
    records = []
    if annotations.ndim == 2 and annotations.shape[1] == 3:
        for co in annotations.round().astype(int).tolist():
            records.append({'point': co,
                            'type': 'point',
                            'tagIds': [],
                            'id': str(uuid.uuid4())})
    elif annotations.ndim == 2 and annotations.shape[1] == 3:
        for co in annotations.round().astype(int).tolist():
            records.append({'center': co,
                            'type': 'ellipsoid',
                            'id': str(uuid.uuid4())})
    elif annotations.ndim == 3 and annotations.shape[1] == 2 and annotations.shape[2] == 3:
        for co in annotations.round().astype(int).tolist():
            start, end = co[0], co[1]
            records.append({'pointA': start,
                            'pointB': end,
                            'type': 'line',
                            'id': str(uuid.uuid4())})
    else:
        raise ValueError('Expected annotations to be x/y/z coordinates of either'
                         '(N, 3), (N, 4) or (N, 2, 3) shape for points, '
                         f'ellipsoids or lines, respectively. Got {annotations.shape}')

    if not name:
        existing_an_layers = [l for l in scene['layers'] if l['type'] == 'annotation']
        name = f'annotation{len(existing_an_layers)}'

    an_layer = {"type": "annotation",
                "annotations": records,
                "annotationTags": [],
                "voxelSize": [4, 4, 40],
                "name": name}

    scene['layers'].append(an_layer)

    return scene


def decode_url(url, format='brief'):
    """Decode neuroglancer URL.

    Parameters
    ----------
    url :       str | list of str
                URL(s) to decode. Can be shortened URL. Note that not all
                `format` work with multiple URLs.
    format :    "segments" | "visible" | "annotations" | "brief" | "dataframe" | "full"
                What to return:
                 - "segments" returns only segments (visible and invisible)
                 - "visible" returns only visible segments
                 - "annotations" returns only annotations
                 - "brief" only returns position (in voxels),  selected
                   segment IDs and annotations
                 - "dataframe" returns a frame with segment IDs and which
                   layers they came from
                 - "full" returns entire scene

    Returns
    -------
    list
                If format is "segments", "visible" or "annotations".
    dict
                If format is "full" or "brief".
    DataFrame
                If format='dataframe'.

    Examples
    --------
    >>> from fafbseg import flywire
    >>> flywire.decode_url('https://ngl.flywire.ai/?json_url=https://globalv1.flywire-daf.com/nglstate/6267328375291904')
    {'position': [132715.625, 55805.6796875, 3289.61181640625],
     'annotations': [],
     'selected': ['720575940621039145']}

    """
    if isinstance(url, list):
        if format != 'dataframe':
            raise ValueError('Can only parse multiple URLs if format="dataframe"')
        return pd.concat([decode_url(u, format=format) for u in url], axis=0)

    assert isinstance(url, (str, dict))
    assert format in ('brief', 'full', 'dataframe', 'segments', 'visible', "annotations")

    query = parse_qs(urlparse(url).query, keep_blank_values=True)

    if 'json_url' in query:
        # Fetch state
        token = utils.get_chunkedgraph_secret()
        r = requests.get(query['json_url'][0], headers={'Authorization': f"Bearer {token}"})
        r.raise_for_status()

        scene = r.json()
    else:
        scene = query

    if format == 'brief':
        seg_layers = [l for l in scene['layers'] if 'segmentation_with_graph' in l.get('type')]
        an_layers = [l for l in scene['layers'] if l.get('type') == 'annotation']
        return {'position': scene['navigation']['pose']['position'].get('voxelCoordinates', None),
                'annotations': [a for l in an_layers for a in l.get('annotations', [])],
                'selected': [s for l in seg_layers for s in l.get('segments', [])]}
    elif format == 'dataframe':
        segs = []
        seg_layers = [l for l in scene['layers'] if 'segmentation' in l.get('type')]
        for l in seg_layers:
            for s in l.get('segments', []):
                segs.append([int(s), l['name']])
        return pd.DataFrame(segs, columns=['segment', 'layer'])

    return scene


def shorten_url(scene, ngl_url=None, state_url=None, refresh_session=False):
    """Generate short url for given scene.

    Parameters
    ----------
    scene :             dict | str
                        Scene to encode as short URL. Can be dict or a full URL.
    ngl_url :           str, optional
                        Base neuroglancer URL. If not provided will use the
                        FlyWire neuroglancer.
    state_url :         str, optional
                        URL for the state server. If not provided will use the
                        default state server for FlyWire.
    refresh_session :   bool
                        If True will force refreshing the session.

    Returns
    -------
    shortened URL :  str

    """
    if not isinstance(scene, (dict, str)):
        raise TypeError(f'Expected `scene` to be dict or string, got "{type(scene)}"')

    if not state_url:
        state_url = STATE_URL

    if not ngl_url:
        ngl_url = NGL_URL

    if isinstance(scene, str):
        scene = decode_url(scene)

    global session

    if not session or refresh_session:
        session = requests.Session()
        # Load token
        token = utils.get_chunkedgraph_secret()

        # Generate header and cookie
        auth_header = {"Authorization": f"Bearer {token}"}
        session.headers.update(auth_header)
        cookie_obj = requests.cookies.create_cookie(name='middle_auth_token',
                                                    value=token)
        session.cookies.set_cookie(cookie_obj)

    # Upload state
    url = f'{state_url}/post'
    resp = session.post(url, data=json.dumps(scene))
    resp.raise_for_status()

    return f'{ngl_url}/?json_url={resp.json()}'


def neurons_to_url(x, top_N=1, downsample=False, coordinates='nm'):
    """Find FlyWire segments overlapping with given neuron(s) and create URLs.

    Parameters
    ----------
    x :             NeuronList w/ TreeNeurons
                    Must be in FlyWire (FAFB14.1) nanometer space.
    top_N :         int, float
                    How many overlapping fragments to include in the URL. If >= 1
                    will treat it as the top N fragments. If < 1 will treat as "all
                    fragments that collectively make up this fraction of the neuron".
    downsample :    int, optional
                    Factor by which to downsample the skeleton before adding to
                    FlyWire scene.

    Returns
    -------
    pandas.DataFrame

    """
    assert isinstance(x, navis.NeuronList)
    assert not x.is_degenerated
    assert isinstance(x[0], navis.TreeNeuron)

    ol = neuron_to_segments(x, coordinates=coordinates)

    data = []
    for n in navis.config.tqdm(x, desc='Creating URLs'):
        if n.id not in ol.columns:
            print(f'No overlapping fragments found for neuron {n.label}. Check '
                  '`coordinates` parameter?')

        this = ol[n.id].sort_values(ascending=False)
        pct = this / this.sum()

        if top_N >= 1:
            to_add = this.index[:top_N]
        else:
            to_add = this.index[: np.where(pct.cumsum() > top_N)[0][0] + 1]

        if downsample:
            n = navis.downsample_neuron(n, downsample)

        url = encode_url(segments=to_add, skeletons=n)

        row = [n.id, n.name, url]

        if top_N >= 1:
            for i in to_add:
                row += [i, pct.loc[i]]
        else:
            row.append(len(to_add))

        data.append(row)

    cols = ['id', 'name', 'url']
    if top_N >= 1:
        for i in range(top_N):
            cols += [f'seg_{i + 1}', f'conf_{i + 1}']
    else:
        cols.append('n_segs')

    return pd.DataFrame(data, columns=cols)


def generate_open_ends_url(x):
    """Generate a FlyWire URL with potential open ends for given neuron.

    Parameters
    ----------
    x :     root ID | navis.TreeNeuron | mesh
            ID of neuron to generate open ends for.

    """
    pass
