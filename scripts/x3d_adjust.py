#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# Copyright (C) 2011 Federico Frenguelli
#
# This file is part of Medea.
#
# Medea is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Medea is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Medea.  If not, see <http://www.gnu.org/licenses/>.

import os
import fnmatch
import logging
import argparse

from xml.dom import minidom
#TODO: now using minidom.. maybe it's better to use the ElementTree API (lxml)

# Configuring paths
BASE_PATH = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
X3D_PATH = os.path.join(BASE_PATH, "medea/x3d")
TEXTURES_PATH = "../textures"


# Setup logging
def setup_logger():
    """ Configure logger """
    logger = logging.getLogger("x3d adjust")
    formatter = logging.Formatter(
                    "%(asctime)s - %(name)s - %(levelname)s - %(message)s")

    shandler = logging.StreamHandler()
    shandler.setLevel(logging.DEBUG)
    shandler.setFormatter(formatter)

    fhandler = logging.FileHandler(os.path.join(BASE_PATH, "x3d_adjust.log"))
    fhandler.setLevel(logging.DEBUG)
    fhandler.setFormatter(formatter)

    logger.addHandler(shandler)
    logger.addHandler(fhandler)
    logger.setLevel(logging.DEBUG)

    return logger


LOG = setup_logger()

# Nodes to be removed
NODES_TO_REMOVE = ("NavigationInfo", "Background", "Viewpoint")
TEXTURE_TO_FIX = ("beer_c_png", "beer_b_png", "water_n_png", "water_s_png",
                  "wine_r_png", "wine_w_png", "drink_cola_png", "milk_b_png",
                  "pate_r_png", "pate_b_png", "yogurt_y_png", "yogurt_k_png", 
                  'cheese_b_png', 'cheese_g_png', 'choco_n_png', 
                  'choco_s_png', 'choco_h_png', 'beans_b_png', 'beans_r_png',
                  'biscuit_straw_png', 'biscuit_choco_png', 'peas_g_png',
                  'tuna_b_png', 'tuna_y_png', 'tuna_r_png', 'IM_beer_b_png',)

PLANES_TO_FIX = ("G_beer_cap","G_fridge_side_panel")


# file specific rules
RULES = {
    'minimarket': 
            [{
             'nodes': [('ImageTexture','FloorHerringbone0041_'),
                       ('ImageTexture','FloorsRegular0026_2_S')],
             'attributes': [('repeatS','true'),('repeatT','true')],           
             },
             {
              'nodes': [('Material', 'MA_white_neon')],
              'attributes': [('emissiveColor', '1 1 1'), ('transparency', '0.0')]
             },
             {
             'nodes': [('Material', 'MA_lampglass')],
             'attributes': [('emissiveColor', '1 1 1')]
             }],
}

def process_rules(name, dom):
    """ Process fixing rules as defined in RULES dict
    """
    try:
        file_rules = RULES[name]
    except KeyError:
        LOG.info("No rules found for "+ name)
        return dom
    
    for rule in file_rules:
        for node in rule['nodes']:
        # search for nodes instances in the dom
            for n in get_node_instances(dom, *node):
                for attr in rule['attributes']:
                    n.setAttribute(*attr)

    return dom


def get_node_instances(dom, tag, idn=None):
    """ Search for tag nodes in dom. 
        When idn is passed search for nodes with DEF attributes equals to idn
    """
    l = dom.getElementsByTagName(tag)
    
    if idn: l = filter(lambda e: e.getAttribute("DEF") == idn, l)

    return l


def fix(dom):
    scene = dom.getElementsByTagName("Scene")[0]

    # remove useless nodes
    for tag in NODES_TO_REMOVE:
        for n in dom.getElementsByTagName(tag):
            scene.removeChild(n)
            n.unlink()

    # Fix ImageTexture nodes
    for img in dom.getElementsByTagName("ImageTexture"):
        url = img.getAttribute("url")
        url = os.path.join(TEXTURES_PATH,
                           url.strip('"').split('" "')[0])
        img.setAttribute("url", url)
        img.setAttribute("repeatT", "false")
        img.setAttribute("repeatS", "false")

        if img.getAttribute("DEF") in TEXTURE_TO_FIX:
            fix_alpha_texture(dom, img)

    # Fix solid attribute for planes. There is a problem computing normals on export
    for idxfs in dom.getElementsByTagName("IndexedFaceSet"):
        if idxfs.parentNode.parentNode.getAttribute("DEF") in PLANES_TO_FIX:
            idxfs.setAttribute("solid", "false")

    return dom


def fix_alpha_texture(dom, image):
    tp = dom.createElement("TextureProperties")
    tp.setAttribute("boundaryModeS", "CLAMP_TO_BOUNDARY")
    tp.setAttribute("boundaryModeT", "CLAMP_TO_BOUNDARY")
    image.appendChild(tp)

    mt = dom.createElement("MultiTexture")
    mt.setAttribute("mode", "BLENDTEXTUREALPHA")

    app = image.parentNode
    app.removeChild(image)
    mt.appendChild(image)

    app.insertBefore(mt, app.firstChild)
    
    return dom


def save(filename, data):
    """ Save new x3d to filename """
    LOG.debug("Saving to "+ filename)
    f = open(filename, "w")
    f.write(data)
    f.close()


def clean(directory):
    LOG.debug("Cleaning "+directory+" ...")
    for f in fnmatch.filter(os.listdir(directory), "*_out.x3d"):
        try:
            os.remove(os.path.join(directory, f))
        except OSError, e:
            LOG.error(e)


def main(minify, pattern, source, dest):
    x3dfiles = fnmatch.filter(os.listdir(source), pattern)
    for x3df in x3dfiles:
        dom = fix(minidom.parse(os.path.join(source, x3df)))
        dom = process_rules(os.path.splitext(x3df)[0], dom)
        data = dom.toxml()
       
        # minifing
        if minify:
            data = data.replace("\t", "")
            #data = data.replace("\n", "")

        # saving
        outfile = os.path.join(dest, x3df.replace(".x3d", "_out.x3d"))
        save(outfile, data)
        dom.unlink()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Fix x3d scene exported from blender")
    parser.add_argument('-m', '--minify', help='Minify output file',
                            action='store_true', default=False)

    # TODO: added for future uses. Need to check if path exists.
    # TODO: transform input paths to absolute paths
    parser.add_argument('-s', '--source-dir', help="Source directory for x3dfiles",
                            default=X3D_PATH)
    parser.add_argument('-d', '--destination-dir', help="Destination directory for output files",
                            default=X3D_PATH)

    parser.add_argument('-p', '--pattern', help="File name pattern to match", default="*.x3d")
    parser.add_argument('-c', '--clean', help="Clean old output files (match *_out.x3d). USE CAREFULLY!!!", 
                            action='store_true', default=False)
                            
    args = parser.parse_args()
    
    # when asked try to clean directory 
    if args.clean:
        clean(args.destination_dir)        

    LOG.debug("Minify: "+ str(args.minify))
    main(args.minify, args.pattern, args.source_dir, args.destination_dir)

