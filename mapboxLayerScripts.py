import re
import os
from PyQt5.QtCore import QSize
from qgis.core import (QgsVectorLayer,
                       QgsSingleSymbolRenderer,
                       QgsCategorizedSymbolRenderer,
                       QgsGraduatedSymbolRenderer,
                       QgsRuleBasedRenderer,
                       QgsHeatmapRenderer,
                       QgsSimpleMarkerSymbolLayer,
                       QgsSimpleLineSymbolLayer,
                       QgsSimpleFillSymbolLayer,
                       QgsSymbolLayerUtils,
                       QgsDataSourceUri,
                       QgsRenderContext,
                       QgsExpression,
                       QgsWkbTypes)
from qgis.utils import Qgis
import processing
from qgis2opengis.mapboxStyleScripts import getLayerStyle
from qgis2opengis.mapboxScriptStrings import (popupScript,
                                          popFuncsScript,
                                          pointToLayerFunction,
                                          wfsScript,
                                          clusterScript,
                                          iconLegend)
try:
    from vector_tiles_reader.plugin.util.tile_json import TileJSON
    vt_enabled = True
except:
    vt_enabled = False
from qgis2opengis.exp2js import compile_to_file
from qgis2opengis.utils import (writeTmpLayer, removeSpaces, exportImages, is25d,
                            safeName, handleHiddenField, add25dAttributes,
                            BLEND_MODES, TYPE_MAP, MB_TYPE_MAP)


def writeVectorLayer(layer, safeLayerName, usedFields, highlight,
                     popupsOnHover, popup, outputProjectFileName, wfsLayers,
                     cluster, visible, json, legends, new_src, canvas, zIndex,
                     restrictToExtent, extent, feedback, labelCode, vtLabels,
                     vtStyles, useMultiStyle, useHeat, useVT, useShapes,
                     useOSMB, vtSources, layers):
    vts = layer.customProperty("VectorTilesReader/vector_tile_url")
    feedback.showFeedback("Writing %s as JSON..." % layer.name())
    zIndex = zIndex + 400
    markerFolder = os.path.join(outputProjectFileName, "markers")
    labeltext, vtLabels = getLabels(layer, safeLayerName,
                                    outputProjectFileName, vts, vtLabels)
    labelCode += labeltext
    new_pop = getPopups(layer, safeLayerName, highlight, popupsOnHover, popup,
                        vts)
    renderer = layer.renderer()
    layer_transp = 1 - (float(layer.opacity()) / 100)
    style = ""
    useMapUnits = False

    if is25d(layer, canvas, restrictToExtent, extent):
        useOSMB = True
        shadows = ""
        renderer = layer.renderer()
        renderContext = QgsRenderContext.fromMapSettings(canvas.mapSettings())
        fields = layer.fields()
        renderer.startRender(renderContext, fields)
        for feat in layer.getFeatures():
            if isinstance(renderer, QgsCategorizedSymbolRenderer):
                classAttribute = renderer.classAttribute()
                attrValue = feat.attribute(classAttribute)
                catIndex = renderer.categoryIndexForValue(attrValue)
                categories = renderer.categories()
                symbol = categories[catIndex].symbol()
            elif isinstance(renderer, QgsGraduatedSymbolRenderer):
                classAttribute = renderer.classAttribute()
                attrValue = feat.attribute(classAttribute)
                ranges = renderer.ranges()
                for range in ranges:
                    if (attrValue >= range.lowerValue() and
                            attrValue <= range.upperValue()):
                        symbol = range.symbol().clone()
            else:
                symbol = renderer.symbolForFeature(feat, renderContext)
            symbolLayer = symbol.symbolLayer(0)
            if not symbolLayer.paintEffect().effectList()[0].enabled():
                shadows = "'2015-07-15 10:00:00'"
        renderer.stopRender(renderContext)
        new_obj = """
        var osmb = new OSMBuildings(map).date(new Date({shadows}));
        osmb.set(json_{sln});""".format(shadows=shadows, sln=safeLayerName)
    elif isinstance(renderer, QgsHeatmapRenderer):
        useHeat = True
        new_obj = heatmapLayer(layer, safeLayerName, renderer)
    elif vts is not None:
        useVT = True
        if vts in vtStyles:
            new_obj = ""
            addVT = False
        else:
            vtSources.append("""
        "%s": {
            "url": "%s",
            "type": "vector"
        }""" % (safeName(vts), vts))
            new_obj = VTLayer(vts)
            vtStyles[vts] = {}
            addVT = True
        geom = TYPE_MAP[layer.wkbType()].replace("Multi", "")
        mbGeom = MB_TYPE_MAP[geom]
        mblayers = getLayerStyle(layer)
        for count, mblayer in enumerate(mblayers):
            markerType = mblayer["type"]
            paint = mblayer["paint"]
            try:
                layout = mblayer["layout"]
                if layout["text-font"]:
                    layout["text-font"] = ["Open Sans Regular"]
            except:
                layout = "{}"
            layers.append("""
        {
            "id": "lyr_%s_%d",
            "type": "%s",
            "source": "%s",
            "source-layer": "%s",
            "layout": %s,
            "paint": %s
        }""" % (safeLayerName, count, markerType, safeName(vts),
                layer.name(), layout, paint))
        vtStyle = vtStyles[vts]
        if layer.name() not in vtStyle:
            vtStyle[layer.name()] = ["", "", ""]
        isLayer = False
        if geom == "Point":
            index = 0
            isLayer = True
        if geom == "LineString":
            index = 1
            isLayer = True
        if geom == "Polygon":
            index = 2
            isLayer = True
        if isLayer:
            vtStyles[vts][layer.name()][index] = style
        style = ""
    else:
        mblayers = getLayerStyle(layer)
        markerType = mblayers[0]["type"]
        (legend, symbol) = getLegend(layer, renderer, outputProjectFileName,
                                     safeLayerName)
        legends[safeLayerName] = legend
        (new_obj, legends, wfsLayers,
         useMultiStyle) = getLayer(layer, renderer, safeLayerName,
                                   outputProjectFileName, usedFields, legends,
                                   cluster, json, wfsLayers, markerType,
                                   useMultiStyle, symbol)
        layerType = ""
        for count, mblayer in enumerate(mblayers):
            type = mblayer["type"]
            if type != layerType:
                layerType = type
                try:
                    layout = mblayer["layout"]
                    if layout["text-font"]:
                        layout["text-font"] = ["Open Sans Regular"]
                except:
                    layout = "{}"
                paint = mblayer["paint"]
                layers.append("""
        {
            "id": "lyr_%s_%d",
            "type": "%s",
            "source": "%s",
            "layout": %s,
            "paint": %s
        }
""" % (safeLayerName, count, type, safeLayerName, layout, paint))
    blend = BLEND_MODES[layer.blendMode()]
    if vts is None:
        new_obj = u"""{style}
        map.createPane('pane_{sln}');
        map.getPane('pane_{sln}').style.zIndex = {zIndex};
        map.getPane('pane_{sln}').style['mix-blend-mode'] = '{blend}';
        {new_obj}""".format(style=style, sln=safeLayerName, zIndex=zIndex,
                            blend=blend, new_obj=new_obj)
    if usedFields != 0:
        new_src += new_pop
    new_src += """
""" + new_obj
    if is25d(layer, canvas, restrictToExtent, extent):
        pass
    elif vts is not None:
        if addVT:
            sln = safeName(vts)
            new_src += """
        map.addLayer(layer_""" + sln + """);"""
    else:
        new_src += """
        bounds_group.addLayer(layer_""" + safeLayerName + """);"""
        if visible:
            if cluster is False:
                new_src += """
        map.addLayer(layer_""" + safeLayerName + """);"""
            else:
                new_src += """
        cluster_""" + safeLayerName + """.addTo(map);"""
    feedback.completeStep()
    return (new_src, legends, wfsLayers, labelCode, vtLabels, vtStyles,
            useMapUnits, useMultiStyle, useHeat, useVT, useShapes, useOSMB,
            vtSources, layers, new_pop)


def getLabels(layer, safeLayerName, outputProjectFileName, vts, vtLabels):
    label_exp = ''
    labeltext = ""
    f = ''
    labelling = layer.labeling()
    if labelling is not None:
        palyr = labelling.settings()
        if palyr and palyr.fieldName and palyr.fieldName != "":
            props = palyr.dataDefinedProperties()
            text = palyr.format()
            bgColor = props.property(palyr.ShapeFillColor).staticValue()
            borderWidth = props.property(palyr.ShapeStrokeWidth).staticValue()
            borderColor = props.property(palyr.ShapeStrokeColor).staticValue()
            x = props.property(palyr.ShapeSizeX).staticValue()
            y = props.property(palyr.ShapeSizeY).staticValue()
            font = text.font()
            fontSize = font.pointSize()
            fontFamily = font.family()
            fontItalic = font.italic()
            fontBold = font.bold()
            fontColor = text.color().name()
            fontUnderline = font.underline()
            xOffset = palyr.xOffset
            yOffset = palyr.yOffset
            styleStart = "'<div style=\"color: %s; font-size: %dpt; " % (
                fontColor, fontSize)
            if props.property(palyr.ShapeDraw).staticValue():
                styleStart += "background-color: %s; " % bgColor
                styleStart += "border: %dpx solid %s; " % (borderWidth,
                                                           borderColor)
                if props.property(palyr.ShapeSizeType).staticValue() == 0:
                    styleStart += "padding: %dpx %dpx; " % (y, x)
                if props.property(palyr.ShapeSizeType).staticValue() == 1:
                    styleStart += "width: %dpx; " % x
                    styleStart += "height: %dpx; " % y
            if fontBold:
                styleStart += "font-weight: bold; "
            if fontItalic:
                styleStart += "font-style: italic; "
            styleStart += "font-family: \\'%s\\', sans-serif;\">' + " % (
                fontFamily)
            styleEnd = " + '</div>'"
            if palyr.isExpression:
                exprFilename = os.path.join(outputProjectFileName, "js",
                                            "qgis2opengis_expressions.js")
                name = compile_to_file(palyr.getLabelExpression(),
                                       "label_%s" % safeLayerName, "Leaflet",
                                       exprFilename)
                js = "%s(context)" % (name)
                js = js.strip()
                f = js
            else:
                fn = palyr.fieldName
                f = "layer.feature.properties['%s']" % handleHiddenField(layer,
                                                                         fn)
            labeltext = ".bindTooltip((" + unicode(f)
            labeltext += " !== null?String(%s%s)%s:'')" % (styleStart,
                                                           unicode(f),
                                                           styleEnd)
            labeltext += ", {permanent: true, offset: [-0, -16], "
            labeltext += "className: 'css_%s'}" % safeLayerName
            labeltext += ");"
            if vts is None:
                labeltext = """
        var i = 0;
        layer_%s.eachLayer(function(layer) {
            var context = {
                feature: layer.feature,
                variables: {}
            };
            layer%s
            labels.push(layer);
            totalMarkers += 1;
              layer.added = true;
              addLabel(layer, i);
              i++;
        });""" % (safeLayerName, labeltext)
            else:
                if palyr.isExpression:
                    labelVal = f
                else:
                    labelVal = "feature.properties['%s']" % palyr.fieldName
                labeltext = """
            if (vtLayer.name === '%s') {
                var latlng = this.vtGeometryToLatLng(feature.geometry[0],
                                                     vtLayer, tileCoords)
                marker = new L.CircleMarker(latlng,
                                            {stroke: false, fill: false});
                marker.bindTooltip(%s,
                                   {permanent: true,
                                    direction: 'center'}).openTooltip();
                this.addUserLayer(marker, tileCoords);
            }""" % (layer.name(), labelVal)
                if vts not in vtLabels:
                    vtLabels[vts] = labeltext
                else:
                    vtLabels[vts] = vtLabels[vts] + labeltext
                labeltext = ""
        else:
            labeltext = ""
    else:
        labeltext = ""
    return labeltext, vtLabels


def getPopups(layer, safeLayerName, highlight, popupsOnHover, popup, vts):
    if vts is not None:
        return "", ""
    fields = layer.fields()
    field_names = popup.keys()
    field_vals = popup.values()
    table = ""
    for field in popup:
        tablestart = "'<table>\\"
        row = ""
        for field, val in zip(field_names, field_vals):
            fieldIndex = fields.indexFromName(unicode(field))
            editorWidget = layer.editorWidgetSetup(fieldIndex).type()
            displayName = layer.attributeDisplayName(fieldIndex).replace("'",
                                                                         "\\'")
            if (editorWidget == 'Hidden'):
                continue

            row += """
                    <tr>\\"""
            if val == 'inline label':
                row += """
                        <th scope="row">"""
                row += displayName
                row += """</th>\\
                        <td>"""
            else:
                row += """
                        <td colspan="2">"""
            if val == "header label":
                row += '<strong>'
                row += displayName
                row += '</strong><br />'
            row += "' + "
            row += "(e.features[0].properties[\'" + unicode(field) + "\'] "
            row += "!== null ? "

            if (editorWidget == 'Photo'):
                row += "'<img src=\"images/' + "
                row += "String(e.features[0].properties['" + unicode(field)
                row += r"']).replace(/[\\\/:]/g, '_').trim()"
                row += " + '\">' : '') + '"
            else:
                row += "autolinker.link("
                row += "e.features[0].properties['" + unicode(field)
                row += "'].toLocaleString()) : '') + '"

            row += """</td>\\
                    </tr>\\"""
        tableend = """
                </table>'"""
        table = tablestart + row + tableend
    new_pop = ""
    if popup != 0 and table != "":
        new_pop = popupScript(safeLayerName, table, highlight, popupsOnHover)
    return new_pop


def getLegend(layer, renderer, outputProjectFileName, safeLayerName):
    if isinstance(renderer, QgsSingleSymbolRenderer):
        symbol = renderer.symbol()
        legendIcon = QgsSymbolLayerUtils.symbolPreviewPixmap(symbol,
                                                             QSize(16, 16))
        legendIcon.save(os.path.join(outputProjectFileName, "legend",
                                     safeLayerName + ".png"))
        legend = ('<img src="legend/' + safeLayerName + '.png" /> ')
        legend += layer.name()
    else:
        if isinstance(renderer, QgsCategorizedSymbolRenderer):
            classes = renderer.categories()
        elif isinstance(renderer, QgsGraduatedSymbolRenderer):
            classes = renderer.ranges()
        elif isinstance(renderer, QgsRuleBasedRenderer):
            classes = renderer.rootRule().children()
        legend = layer.name().replace("'", "\\'") + "<br />"
        legend += "<table>"
        for cnt, c in enumerate(classes):
            symbol = c.symbol()
            legend = iconLegend(symbol, c, outputProjectFileName,
                                safeLayerName, legend, cnt)
        legend += "</table>"
        symbol = classes[0].symbol()
    return (legend, symbol)


def getLayer(layer, renderer, safeLayerName, outputProjectFileName, usedFields,
             legends, cluster, json, wfsLayers, markerType, useMultiStyle,
             symbol):
    if layer.geometryType() == QgsWkbTypes.PointGeometry:
        (new_obj,
         wfsLayers,
         useMultiStyle) = pointLayer(layer, safeLayerName, cluster, usedFields,
                                     json, wfsLayers, markerType, symbol,
                                     useMultiStyle)
    else:
        (new_obj, wfsLayers,
         useMultiStyle) = nonPointLayer(layer, safeLayerName, usedFields,
                                        json, wfsLayers, symbol, useMultiStyle)
    return new_obj, legends, wfsLayers, useMultiStyle


def pointLayer(layer, safeLayerName, cluster, usedFields, json, wfsLayers,
               markerType, symbol, useMultiStyle):
    if layer.providerType() == 'WFS' and json is False:
        p2lf = ""
        slCount = symbol.symbolLayerCount()
        if slCount < 1:
            slCount = 1
        for sl in range(slCount):
            p2lf += pointToLayerFunction(safeLayerName, sl)
        (new_obj,
         scriptTag,
         useMultiStyle) = buildPointWFS(p2lf, safeLayerName, layer, cluster,
                                        symbol, useMultiStyle)
        wfsLayers += wfsScript(scriptTag)
    else:
        attrText = layer.attribution()
        attrUrl = layer.attributionUrl()
        layerAttr = '<a href="%s">%s</a>' % (attrUrl, attrText)
        (new_obj,
         useMultiStyle) = buildPointJSON(symbol, safeLayerName, usedFields,
                                         markerType, layerAttr, useMultiStyle)
        if cluster:
            new_obj += clusterScript(safeLayerName)
    return new_obj, wfsLayers, useMultiStyle


def nonPointLayer(layer, safeLayerName, usedFields, json, wfsLayers, symbol,
                  useMultiStyle):
    if layer.providerType() == 'WFS' and json is False:
        (new_obj, scriptTag,
         useMultiStyle) = buildNonPointWFS(safeLayerName, layer, symbol,
                                           useMultiStyle)
        wfsLayers += wfsScript(scriptTag)
    else:
        attrText = layer.attribution().replace('\n', ' ').replace('\r', ' ')
        attrUrl = layer.attributionUrl()
        layerAttr = u'<a href="%s">%s</a>' % (attrUrl, attrText)
        new_obj, useMultiStyle = buildNonPointJSON(safeLayerName, usedFields,
                                                   layerAttr, symbol,
                                                   useMultiStyle)
    return new_obj, wfsLayers, useMultiStyle


def heatmapLayer(layer, safeLayerName, renderer):
    attrText = layer.attribution()
    if attrText != "":
        attrUrl = layer.attributionUrl()
        layerAttr = '<a href="%s">%s</a>' % (attrUrl, attrText)
    else:
        layerAttr = ""
    hmRadius = renderer.radius() * 2
    hmWeight = renderer.weightExpression()
    if hmWeight is not None and hmWeight != "":
        hmWeightId = layer.fieldNameIndex(hmWeight)
        hmWeightMax = layer.maximumValue(hmWeightId)
    else:
        hmWeight = ""
        hmWeightMax = 1
    colorRamp = renderer.colorRamp()
    hmStart = colorRamp.color1().name()
    hmEnd = colorRamp.color2().name()
    hmRamp = "{0: '" + hmStart + "', "
    hmStops = colorRamp.stops()
    for stop in hmStops:
        hmRamp += unicode(stop.offset) + ": '" + stop.color.name() + "', "
    hmRamp += "1: '" + hmEnd + "'}"
    new_obj = """
        var %(sln)s_hm = geoJson2heat(json_%(sln)s,
                                      '%(hmWeight)s');
        var layer_%(sln)s = new L.heatLayer(%(sln)s_hm, {
            attribution: '%(attr)s',
            radius: %(hmRadius)d,
            max: %(hmWeightMax)d,
            minOpacity: 1,
            gradient: %(hmRamp)s});
        """ % {"sln": safeLayerName, "hmWeight": hmWeight, "attr": layerAttr,
               "hmWeightMax": hmWeightMax, "hmRamp": hmRamp,
               "hmRadius": hmRadius}
    return new_obj


def VTLayer(json_url):
    sln = safeName(json_url)
    try:
        key = json_url.split("?")[1]
    except:
        key = ""
    json = TileJSON(json_url)
    json.load()
    tile_url = json.tiles()[0].split("?")[0]
    key_url = "%s?%s" % (tile_url, key)
    styleSuffix = safeName(json_url)
    vtJS = """
        var layer_%s = L.vectorGrid.protobuf("%s", {
            rendererFactory: L.svg.tile,
            //onEachFeature: label_%s,
            vectorTileLayerStyles: style_%s
        });""" % (sln, key_url, sln, styleSuffix)
    return vtJS


def buildPointJSON(symbol, sln, usedFields, markerType, layerAttr,
                   useMultiStyle):
    slCount = symbol.symbolLayerCount()
    multiStyle = ""
    if slCount > 1:
        multiStyle = ".multiStyle"
        useMultiStyle = True
    pointJSON = """
        var layer_{sln} = new L.geoJson%s(json_{sln}, {{
            attribution: '{attr}',
            pane: 'pane_{sln}',""" % multiStyle
    if usedFields != 0:
        pointJSON += """
            onEachFeature: pop_{sln},"""
    if slCount > 1:
        pointJSON += """
            pointToLayers: ["""
        for sl in range(slCount):
            pointJSON += """function (feature, latlng) {{
                var context = {{
                    feature: feature,
                    variables: {{}}
                }};
                return L.{markerType}(latlng, """
            pointJSON += """style_{sln}_%s(feature));
            }},""" % sl
    else:
        pointJSON += """
            pointToLayer: function (feature, latlng) {{
                var context = {{
                    feature: feature,
                    variables: {{}}
                }};
                return L.{markerType}(latlng, style_{sln}_0(feature));
            }},"""
    if slCount > 1:
        pointJSON += """
        ]}});"""
    else:
        pointJSON += """
        }});"""
    pointJSON = pointJSON.format(sln=sln, markerType=markerType,
                                 attr=layerAttr)
    return (pointJSON, useMultiStyle)


def buildPointWFS(p2lf, layerName, layer, cluster_set, symbol, useMultiStyle):
    attrText = layer.attribution()
    attrUrl = layer.attributionUrl()
    layerAttr = '<a href="%s">%s</a>' % (attrUrl, attrText)
    scriptTag = getWFSScriptTag(layer, layerName)
    p2ls = ""
    slCount = symbol.symbolLayerCount()
    multiStyle = ""
    p2lStart = "pointToLayer: "
    p2lEnd = ""
    if slCount > 1:
        multiStyle = ".multiStyle"
        useMultiStyle = True
        p2lStart = "pointToLayers: ["
        p2lEnd = "],"
        for sl in range(slCount):
            p2ls += "pointToLayer_%s_%s, " % (layerName, sl)
    else:
        p2ls = "pointToLayer_%s_0, " % layerName
    new_obj = p2lf + """
        var layer_{layerName} = L.geoJson{multiStyle}(null, {{
            attribution: '{layerAttr}',
            pane: 'pane_{layerName}',
            {p2lStart}{p2ls}{p2lEnd}
            onEachFeature: pop_{layerName}
        }});""".format(layerName=layerName, multiStyle=multiStyle,
                       layerAttr=layerAttr, p2lStart=p2lStart, p2ls=p2ls,
                       p2lEnd=p2lEnd)
    if cluster_set:
        new_obj += """
        var cluster_{layerName} = """.format(layerName=layerName)
        new_obj += "new L.MarkerClusterGroup({showCoverageOnHover: false});"
    new_obj += """
        function get{layerName}Json(geojson) {{
            layer_{layerName}""".format(layerName=layerName)
    new_obj += ".addData(geojson);"
    if cluster_set:
        new_obj += """
            cluster_{layerName}.add""".format(layerName=layerName)
        new_obj += "Layer(layer_{layerName});".format(layerName=layerName)
    new_obj += """
            setBounds();
        };"""
    return new_obj, scriptTag, useMultiStyle


def buildNonPointJSON(safeName, usedFields, layerAttr, symbol, useMultiStyle):
    if usedFields != 0:
        onEachFeature = u"""
            onEachFeature: pop_{safeName},""".format(safeName=safeName)
    else:
        onEachFeature = u""
    styles = u""
    slCount = symbol.symbolLayerCount()
    multiStyle = u""
    styleStart = "style: "
    styleEnd = ""
    if slCount > 1:
        multiStyle = u".multiStyle"
        useMultiStyle = True
        styleStart = u"styles: ["
        styleEnd = u"]"
        for sl in range(slCount):
            styles += u"""style_%s_%s,""" % (safeName, sl)
    else:
        styles = u"""style_%s_0,""" % safeName
    new_obj = u"""
        var layer_{safeName} = new L.geoJson{multiStyle}(json_{safeName}, {{
            attribution: '{attr}',
            pane: 'pane_{safeName}',{onEachFeature}
            {styleStart}{styles}{styleEnd}
        }});"""
    new_obj = new_obj.format(safeName=safeName, multiStyle=multiStyle,
                             attr=layerAttr, onEachFeature=onEachFeature,
                             styleStart=styleStart, styles=styles,
                             styleEnd=styleEnd)
    return new_obj, useMultiStyle


def buildNonPointWFS(layerName, layer, symbol, useMultiStyle):
    attrText = layer.attribution()
    attrUrl = layer.attributionUrl()
    layerAttr = '<a href="%s">%s</a>' % (attrUrl, attrText)
    scriptTag = getWFSScriptTag(layer, layerName)
    styles = ""
    slCount = symbol.symbolLayerCount()
    multiStyle = ""
    styleStart = "style: "
    styleEnd = ""
    if slCount > 1:
        multiStyle = ".multiStyle"
        useMultiStyle = True
        styleStart = "styles: ["
        styleEnd = "],"
        for sl in range(slCount):
            styles += """style_%s_%s,""" % (layerName, sl)
    else:
        styles = """style_%s_0,""" % layerName
    new_obj = """
        var layer_{layerName} = L.geoJson{multiStyle}(null, {{
            attribution: '{attr}',
            {styleStart}{styles}{styleEnd}
            pane: 'pane_{layerName}',
            onEachFeature: pop_{layerName}
        }});"""
    new_obj += """
        function get{layerName}Json(geojson) {{
            layer_{layerName}"""
    new_obj = new_obj.format(layerName=layerName, multiStyle=multiStyle,
                             attr=layerAttr, styleStart=styleStart,
                             styles=styles, styleEnd=styleEnd)
    new_obj += ".addData(geojson);"
    new_obj += """
        };"""
    return new_obj, scriptTag, useMultiStyle


def getWFSScriptTag(layer, layerName):
    layerSource = layer.source()
    if ("retrictToRequestBBOX" in layerSource or
            "restrictToRequestBBOX" in layerSource):
        provider = layer.dataProvider()
        uri = QgsDataSourceUri(provider.dataSourceUri())
        wfsURL = uri.param("url")
        wfsTypename = uri.param("typename")
        wfsSRS = uri.param("srsname")
        layerSource = wfsURL
        layerSource += "?SERVICE=WFS&VERSION=1.0.0&"
        layerSource += "REQUEST=GetFeature&TYPENAME="
        layerSource += wfsTypename
        layerSource += "&SRSNAME="
        layerSource += wfsSRS
    scriptTag = re.sub(r'SRSNAME\=EPSG\:\d+', 'SRSNAME=EPSG:4326', layerSource)
    scriptTag += "&outputFormat=text%2Fjavascript&format_options=callback%3A"
    scriptTag += "get" + layerName + "Json"
    return scriptTag
