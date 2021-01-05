#!/usr/bin/env python3

import mapnik
import string
import argparse

# This is a list of prefixes of AGS (Amtliche Gemeindeschlüssel) IDs that
# identify municipalities and have a hierarchical structure. Prefixes
# therefore identify Gemeinden (municipalities), Landkreise (counties),
# Regierungsbezirke or Länder (states).
AGS_prefixes = ['06435', '06440', '09677', '09672', '09671', '06535', '06631']
image_width = 5000
image_height = 5000
shapefile = 'vg250_2019-01-01.utm32s.shape.ebenen/vg250_ebenen/VG250_GEM.shp'
shapefile_projection = '+proj=utm +zone=32 +ellps=GRS80 +towgs84=0,0,0,0,0,0,0 +units=m +no_defs'

colors = ['#330000', '#ff1100', '#8c5c54', '#991f00', '#662a14', '#f28861', '#ccb4a3', '#ff7700', '#8c4100', '#f2a561', '#331b00', '#664b14', '#bf8c00', '#b2a46b', '#f2e961', '#71735c', '#ccff00', '#708c00', '#eeffcc', '#445924', '#85ff66', '#1c8c49', '#003318', '#a3ccbc', '#29332f', '#33ffc9', '#00665f', '#66f5ff', '#00ccff', '#005266', '#00aaff', '#001f33', '#7aa6cc', '#174273', '#001859', '#919ef2', '#6a52cc', '#574573', '#2d2933', '#b6a3cc', '#4d0080', '#ad33ff', '#bc7acc', '#f200d2', '#660044', '#ff66b8', '#cc7a9b', '#8c0025', '#735c62', '#ff667a', '#ffcccf']


def create_rule(AGS_prefix, color):
    c = str(mapnik.Color(color))
    rule = string.Template("""
<Rule>
    <Filter>(([ADE]=6) and [AGS].match(&apos;^$prefix.*&apos;))</Filter>
    <PolygonSymbolizer fill="$area_color"/>
    <LineSymbolizer />
    <TextSymbolizer placement="interior" face-name="DejaVu Sans Bold" halo-radius="2" halo-fill="white" size="16">[GEN]</TextSymbolizer>
</Rule>
""").substitute(prefix=AGS_prefix, area_color=c)
    # add textsymbolizer
    #p.name = mapnik.Expression('[GEN]')
    return rule

def build_stylesheet(shapefile, projection, AGS_prefixes):
    # returns xml_string, mapnik.Box2d
    shp = mapnik.Shapefile(file=shapefile)
    # we only want to show municipality from the following counties
    rules = []
    e = None
    for i, f in enumerate(f for f in shp.all_features() if any(f['AGS'].startswith(p) for p in AGS_prefixes)):
        if e is None:
            e = f.envelope()
        else:
            e = e + f.envelope()
        color = colors[i%len(colors)]
        r = create_rule(f['AGS'], color)
        rules.append(r)
    style = string.Template("""
<Style name="Gemeinden">
$rules
</Style>
""").substitute(rules=''.join(rules))
    layer = string.Template("""
<Layer name="Grenzen" srs="$projection">
    <StyleName>Gemeinden</StyleName>
    <Datasource>
        <Parameter name="file">$shapefile</Parameter>
        <Parameter name="type">shape</Parameter>
    </Datasource>
</Layer>
""").substitute(projection=projection, shapefile=shapefile)
    stylesheet = string.Template("""<?xml version="1.0" encoding="utf-8"?>
<Map srs="$projection" background-color="rgb(211,211,211)">
$style
$layer
</Map>""").substitute(style=style, layer=layer, projection=projection)
    return stylesheet, e

def main(imagefilename, xmlfilename):
    m = mapnik.Map(image_width, image_height)
    m.srs = shapefile_projection
    m.background = mapnik.Color('lightgrey')
    style, envelope = build_stylesheet(shapefile, shapefile_projection, AGS_prefixes)
    mapnik.load_map_from_string(m, style)
    m.zoom_to_box(envelope)
    mapnik.render_to_file(m, imagefilename)
    if xmlfilename:
        mapnik.save_map(m, xmlfilename)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='create an image with municipalities.')
    parser.add_argument('output_image', type=str, help='the output image')
    parser.add_argument('--xml', dest='xml', metavar='xml_output', default='', help='save the intermediate xml to a file')
    args = parser.parse_args()
    main(args.output_image, args.xml)
