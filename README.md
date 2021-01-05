# german-municipalities-mapper
Create (regional) maps of german municipalities

## Requirements
- Python 3
- mapnik 3
- python-mapnik 3: https://github.com/mapnik/python-mapnik/tree/v3.0.x
- data source from the Bundesamt für Kartographie und Geodäsie: https://gdz.bkg.bund.de/index.php/default/catalog/product/view/id/789/s/verwaltungsgebiete-1-250-000-ebenen-stand-31-12-vg250-ebenen-31-12/category/8/ . Go to the tab "Direktdownload" and download the UTM32s file.

Download and unzip the linked data and configure the path to VG250_GEM.shp on top of render-map.py.
