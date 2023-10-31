<h1>qgis2opengis</h1>
<p>QGIS plugin to make <b>OpenGIS - open source webgis</b>, from your current QGIS project.</p>
<p>Made with OpenLayers, it replicates as many aspects of the project as it can, including layers, styles (categorized, graduated and svg icon) and other.
No server-side software required.

Full version at https://opengis.it

Improvements and new features listed at [releases](https://github.com/andreaordonselli/qgis2opengis/releases)

Born from the [qgis2web](https://github.com/tomchadwin/qgis2web) v.3.16.0 repository

Demo full version at https://opengis.it/demo
![image](https://github.com/andreaordonselli/qgis2opengis/assets/89784373/6236147d-26e2-4c67-bb8f-236831e7929b)

<h2>Installation</h2>
<ul>
    <li>In QGIS, select <code>Plugins > Manage and Install Plugins...</code></li>
</ul>
<p>or:</p>
<ul>
    <li>Download and unzip to your QGIS plugins directory</li>
</ul>

<h2>Usage</h2>
<p>Prepare your map as far as possible in QGIS, as you want it to appear in
your OpenGIS webmap. Specific tasks you can carry out to improve your OpenGIS include:
</p>
<ul>
    <li>Set background and highlight colours in <code>Project > Project Properties...</code></li>
    <li>Give your layers human-friendly names in the <code>Layers Panel</code> </li>
    <li>Give your layer columns human friendly names via <code>Layer > Properties > Fields > Alias</code></li>
    <li>Hide the columns you don't want to appear in your popups by changing their Edit widget to "Hidden"</li>
    <li>If any of your fields contain image filenames, change their Edit widget to "Photo" to have the images appear in popups</li>
    <li>Style your layers, and set their scale-dependent visibility, if required</li>
</ul>
<p>Run qgis2opengis from the Web menu, or via its icon.</p>
<p>The tabs at the top allow you to set up your project. All options are written
to your QGIS project, so save your project if you want to keep these settings.</p>

<h3>Layer options</h3>
<dl>
    <dt>Popup fields</dt>
        <dd>Specify how each field will be labelled in popups</dd>
    <dt>Popups</dt>
        <dd>Specify, whether or not a layer shows a popup on a click. If not, the layer is not even clickable</dd>
    <dt>Visible</dt>
        <dd>Select whether the layer will be visible on map load. This only
            determines visibility - the layer will be loaded regardless of this
            setting</dd> 
    <dt>Encode to JSON</dt>
        <dd>If unchecked, WFS layers will remain remote WFS layers in the
            webmap. If checked, the layer will be written to a local GeoJSON
            file</dd>
    <dt>Cluster</dt>
        <dd>Cluster point features</dd>
</dl>

<h3>General options</h3>

<h4>Data export</h4>
<dl>
    <dt>Export folder</dt>
        <dd>The folder where the webmap will be saved</dd> 
    <dt>Minify GeoJSON files</dt>
        <dd>Remove unnecessary whitespace from exported GeoJSON to reduce file
            size</dd>
    <dt>Precision</dt>
        <dd>Simplify geometry to reduce file size</dd>
</dl>

<h4>Scale/Zoom</h4>
<dl>
    <dt>Extent</dt>
        <dd>Either match the current QGIS view or show all contents of all
            layers (only local GeoJSON and rasters, not WFS/WMS)</dd>
    <dt>Max zoom level</dt>
        <dd>How far the webmap will zoom in</dd>
    <dt>Min zoom level</dt>
        <dd>How far the webmap will zoom out</dd>
    <dt>Restrict to extent</dt>
        <dd>Prevent panning or zooming beyond the selected extent</dd>
</dl>

<h4>Appearance</h4>
<dl>
    <dt>Add address search</dt>
        <dd>Add field to allow searching for locations (geocode)</dd>
    <dt>Add layers list</dt>
        <dd>Include list of layers (with legend icons, where possible)</dd>
    <dt>Add measure tool</dt>
        <dd>Include interactive measuring widget</dd>
    <dt>Attribute filter</dt>
        <dd>Every supported field of all layers are listed as well as the type and layers they occur in. Selected attributes will be used to filter the webmap and all layers that contain the attribute with the same name.</dd>
    <dt>Geolocate user</dt>
        <dd>Show user's location on map</dd>
    <dt>Highlight on hover</dt>
        <dd>Highlight features on mouseover</dd>
    <dt>Layer search</dt>
        <dd>Add option to search for values in layer field values</dd>
    <dt>Match project CRS</dt>
        <dd>Create webmap in same projection as QGIS project, otherwise the
        webmap is projected in EPSG:3857</dd>
    <dt>Show popups on hover</dt>
        <dd>Show popups when mouse hovers over features</dd>
    <dt>Template</dt>
        <dd>Select HTML template for webmap - add your own templates to the
            /qgis2opengis/templates directory in your current QGIS3 profile 
            folder</dd>
</dl>

<h2>Reporting bugs</h2>
<p>Please report any problems you have with qgis2opengis. Without this feedback, I
am often completely unaware that a problem exists. To ensure no time or effort
is wasted in bug reporting, please follow these steps:</p>
<ol>
    <li>Make sure you are using the latest release of qgis2opengis</li>
    <li>Check the issues on Github to see whether the bug has already been
        reported, and if so, read through all the comments on the issue, and
        add any additional information from your experience of the bug</li>
    <li>Make sure you can reproduce the bug reliably</li>
    <li>Reduce the complexity of your bug conditions as far as you can,
        especially by reducing the number of layers, ideally to one</li>
    <li>Raise a Github issue, including:
    <ul>
        <li>only one bug per Github issue</li>
        <li>the qgis2opengis version (or make it clear you are using Github master
            branch)</li>
        <li>any Python error text/stack trace which occurs</li>
        <li>browser JS console errors - press F12 in qgis2opengis to open the 
            developer toolbar and find the console</li>
        <li>screenshot of your settings</li>
        <li>screenshot of the output</li>
        <li>a link to the data you used, if possible</li>
    </ul></li>
</ol>
<p>The stability of qgis2opengis relies on your bug reports, so please keep them
coming.</p>

<h2>Credits</h2>
<p>qgis2opengis was born as a branch of the qgis2web v.3.16.0 repository, for OpenLayers export only, and adds many improvements and features.</p>
<p>Special thanks go to the creators of qgis2web: Tom Chadwin, Riccardo Klinger, Victor Olaya, Nyall Dawson and to all the users of github.com, stackoverflow.com and gis.stackexchange.com</p>
<ul>
    <li>@tomchadwin</li>
	<li>@volaya</li>
    <li>@riccardoklinger</li>
    <li>@pcav</li>
</ul>

<p>All of this could not exist without the following monumental
software:</p>
<ul>
    <li>QGIS</li>
    <li>OpenLayers</li>
</ul>

<p>Thanks are also due for major code contributions of qgis2web, to:</p>
<ul>
    <li>@akbargumbira</li>
    <li>@lucacasagrande</li>
    <li>@walkermatt</li>
    <li>@boesiii</li>
    <li>@ThomasG77</li>
    <li>@NathanW2</li>
    <li>@nyalldawson (FTP export for Faunalia/ENEL)</li>
    <li>@perliedman</li>
    <li>@olakov</li>
</ul>

<p>In addition, the following libraries have been used for qgis2web:</p>
<ul>
    <li>bridge-style, by @volaya</li>
    <li>ol3-layerswitcher, by @walkermatt</li>
    <li>Autolinker.js, by @gregjacobs</li>
    <li>requestAnimationFrame polyfill, by @paulirish</li>
    <li>Function.prototype.bind polyfill, by @mozilla</li>
    <li>Proj4js, by @madair, @calvinmetcalf, and other</li>
    <li>ol3-search-layer, by @ThomasG77</li>
    <li>OSMBuildings, by @kekscom</li>
    <li>multi-style-layer, by @perliedman</li>
    <li>rbush, by @mourner</li>
    <li>Labelgun, by @JamesMilnerUK</li>
</ul>
