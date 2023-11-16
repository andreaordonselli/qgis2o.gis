<h1>qgis2opengis</h1>

![image](https://www.opengis.it/a_opengis/icon/logo_opengis/opengis_logo.png)

QGIS plugin to make <b>Lite version of OpenGIS - open source webgis</b>, starting from your current QGIS project.

Made with OpenLayers, it replicates as many aspects of the project as it can, including layers, styles (categorized, graduated and svg icon) and other.
No server-side software required.

Born from the [qgis2web](https://github.com/tomchadwin/qgis2web) v.3.16.0 repository, introduces improvements and new features listed at [releases](https://github.com/andreaordonselli/qgis2opengis/releases)

Demo Lite version at https://opengis.it/lite-version/
![lite](https://github.com/andreaordonselli/qgis2opengis/assets/89784373/a013e5a8-fe79-4fec-aa6d-fd6a024de1a5)

Demo Full version at https://opengis.it/full-version/
![full](https://github.com/andreaordonselli/qgis2opengis/assets/89784373/d10b5b6d-3d0d-4715-be90-87e69fb9ec1d)
</br>
</br>
</br>
[<img src="https://github.com/andreaordonselli/qgis2opengis/assets/89784373/d4f36894-4fe1-4a3a-80c9-5a838b06abac">](https://www.opengis.it/buy-me-a-coffee/)</br>
<b>🎁 Donate a coffee to become OpenGIS Supporter and receive the latest Full version as a gift 🎁</b>
</br>
</br>
<h2>Differences between Lite and Full Version</h2>

<table>
<thead>
<tr>
<th>OpenGIS Lite Version</th>
<th>OpenGIS Full Version</th>
</tr>
</thead>
<tbody>
<tr>
<td>logo and title</td>
<td>logo and title</td>
</tr>
<tr>
<td>measure length / area</td>
<td>measure length /area / circle</td>
</tr>
<tr>
<td>search address</td>
<td>search address, locate with GPS</td>
</tr>
<tr>
<td>search for feature data</td>
<td>search for multi-feature data</td>
</tr>
<tr>
<td>basic popup</td>
<td>advanced browsable popup with current geometry highlighting</td>
</tr>
<tr>
<td>clusters for points and labels</td>
<td>clusters for points and labels</td>
</tr>
<tr>
<td>basic layerswitcher</td>
<td>advanced layerswitcher with transparency / zoom extension /<br/> move layers / legend / reduced themes /<br/> automatic open-close based on monitor size
</tr>
<tr>
<td>scalebar</td>
<td>scalebar and scale-control</td>
</tr>
<tr>
<td>single symbology / categorized / graduated / svg / raster also in bands</td>
<td>single symbology / categorized and merged /<br/> graduated / svg / raster also in bands</td>
</tr>
<tr>
<td>basic browser printing</td>
<td>advanced printing, orientation customization, sheet size,</br>
margins, legend, north, scale, title</td>
</tr>
<tr>
<td>-</td>
<td>integration with ol-ext and jquery libraries</td>
</tr>
<tr>
<td>-</td>
<td>increase openlayers library version from 3 to 6.15.1</td>
</tr> 
<tr>
<td>-</td>
<td>reserved version protected by access credentials</td>
</tr> 
<tr>
<td>-</td>
<td>coordinates in different crs</td>
</tr>  
<tr>
<td>-</td>
<td>bookmarks (zoom in selected areas e.g. neighborhoods)</td>
</tr>
<tr>
<td>-</td>
<td>label repetition along a linear path</td>
</tr> 
<tr>
<td>-</td>
<td>drawing tools</td>
</tr>
<tr>
<td>-</td>
<td>navigable mini map</td>
</tr>
<tr>
<td>-</td>
<td>permalink (shareable link to the displayed map)</td>
</tr>
<tr>
<td>-</td>
<td>google streetview</td>
</tr>
<tr>
<td>-</td>
<td>descriptive sidebar divided into tabs, graphics optimized for smartphones</td>
</tr>
<tr>
<td>-</td>
<td>query wms layer</td>
</tr>
<tr>
<td>-</td>
<td>coordinates when moving the mouse in different epsg</td>
</tr>
</tbody>
</table>

<h2>OpenGIS Pro Version</h2>
It is possible to access the Pro version only with hosting on OpenGIS servers, write to us at <a href="mailto:info@opengis.it">info@opengis.it</a> for more information.</br>
The Pro version is like the Full version with added ones:
<li>thematic maps with related permalink. instant filter of the layers present in the layerswitcher.</li>
<li>table view of layer attributes with quick or in-depth search filters on one or more fields</li>
<li>spatial query (querying features of layers chosen through personalized intersection with drawn geometries, selection in map or cadastral particles) with result in table that can be grouped by layer or other, downloadable in xlsx or docx.</li>
Demo Pro version at https://opengis.it/demo/

<h2>Installation and usage</h2>

See OpenGIS Knowledge base at https://www.opengis.it/docs/

<h2>OpenGIS Lite Update Plan</h2>
<li>update help with some basic advice useful for setting up the map</li>
<li>improved layerswitcher with reduced symbologies and predefined base layer "White background"</li>
<li>wms layer query as full version</li>
<li>show project coordinates</li>
<li>improve popup by inserting queried layer title</li>
<li>layer, layer group tree management as in qgis</li>
<li>bug fix that doesn't allow writing apostrophes in layer names</li>
<li>improve visibility for smartphones (deactivate visibility of measurement tools and more)</li>

<h2>Reporting bugs</h2>
<p>Please report any problems you have with OpenGIS. Without this feedback, I
am often completely unaware that a problem exists. To ensure no time or effort
is wasted in bug reporting, please follow these steps:</p>
<ol>
    <li>Make sure you are using the latest release of plugin</li>
    <li>Check the issues on Github to see whether the bug has already been
        reported, and if so, read through all the comments on the issue, and
        add any additional information from your experience of the bug</li>
    <li>Make sure you can reproduce the bug reliably</li>
    <li>Reduce the complexity of your bug conditions as far as you can,
        especially by reducing the number of layers, ideally to one</li>
    <li>Raise a Github issue, including:
    <ul>
        <li>only one bug per Github issue</li>
        <li>the plugin version</li>
        <li>any Python error text/stack trace which occurs</li>
        <li>browser JS console errors - press F12 in browser to open the 
            developer toolbar and find the console</li>
        <li>screenshot of your settings</li>
        <li>screenshot of the output</li>
        <li>a link to the data you used, if possible</li>
    </ul></li>
</ol>
<p>The stability of OpenGIS relies on your bug reports, so please keep them
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
    <li>rbush, by @mourner</li>
    <li>Labelgun, by @JamesMilnerUK</li>
</ul>
