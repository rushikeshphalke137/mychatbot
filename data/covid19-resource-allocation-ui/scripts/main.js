//*******************
// global variables
//*******************
//root holder for all global variables
var globals = {};
//map for the applicaiton

//code start for check device is mobile or nottabMenu
globals.mobileDevice = function() {
    var check = false;
    (function(a) {
        if (/(android|bb\d+|meego).+mobile|avantgo|bada\/|blackberry|blazer|compal|elaine|fennec|hiptop|iemobile|ip(hone|od)|iris|kindle|lge |maemo|midp|mmp|mobile.+firefox|netfront|opera m(ob|in)i|palm( os)?|phone|p(ixi|re)\/|plucker|pocket|psp|series(4|6)0|symbian|treo|up\.(browser|link)|vodafone|wap|windows ce|xda|xiino/i.test(a) || /1207|6310|6590|3gso|4thp|50[1-6]i|770s|802s|a wa|abac|ac(er|oo|s\-)|ai(ko|rn)|al(av|ca|co)|amoi|an(ex|ny|yw)|aptu|ar(ch|go)|as(te|us)|attw|au(di|\-m|r |s )|avan|be(ck|ll|nq)|bi(lb|rd)|bl(ac|az)|br(e|v)w|bumb|bw\-(n|u)|c55\/|capi|ccwa|cdm\-|cell|chtm|cldc|cmd\-|co(mp|nd)|craw|da(it|ll|ng)|dbte|dc\-s|devi|dica|dmob|do(c|p)o|ds(12|\-d)|el(49|ai)|em(l2|ul)|er(ic|k0)|esl8|ez([4-7]0|os|wa|ze)|fetc|fly(\-|_)|g1 u|g560|gene|gf\-5|g\-mo|go(\.w|od)|gr(ad|un)|haie|hcit|hd\-(m|p|t)|hei\-|hi(pt|ta)|hp( i|ip)|hs\-c|ht(c(\-| |_|a|g|p|s|t)|tp)|hu(aw|tc)|i\-(20|go|ma)|i230|iac( |\-|\/)|ibro|idea|ig01|ikom|im1k|inno|ipaq|iris|ja(t|v)a|jbro|jemu|jigs|kddi|keji|kgt( |\/)|klon|kpt |kwc\-|kyo(c|k)|le(no|xi)|lg( g|\/(k|l|u)|50|54|\-[a-w])|libw|lynx|m1\-w|m3ga|m50\/|ma(te|ui|xo)|mc(01|21|ca)|m\-cr|me(rc|ri)|mi(o8|oa|ts)|mmef|mo(01|02|bi|de|do|t(\-| |o|v)|zz)|mt(50|p1|v )|mwbp|mywa|n10[0-2]|n20[2-3]|n30(0|2)|n50(0|2|5)|n7(0(0|1)|10)|ne((c|m)\-|on|tf|wf|wg|wt)|nok(6|i)|nzph|o2im|op(ti|wv)|oran|owg1|p800|pan(a|d|t)|pdxg|pg(13|\-([1-8]|c))|phil|pire|pl(ay|uc)|pn\-2|po(ck|rt|se)|prox|psio|pt\-g|qa\-a|qc(07|12|21|32|60|\-[2-7]|i\-)|qtek|r380|r600|raks|rim9|ro(ve|zo)|s55\/|sa(ge|ma|mm|ms|ny|va)|sc(01|h\-|oo|p\-)|sdk\/|se(c(\-|0|1)|47|mc|nd|ri)|sgh\-|shar|sie(\-|m)|sk\-0|sl(45|id)|sm(al|ar|b3|it|t5)|so(ft|ny)|sp(01|h\-|v\-|v )|sy(01|mb)|t2(18|50)|t6(00|10|18)|ta(gt|lk)|tcl\-|tdg\-|tel(i|m)|tim\-|t\-mo|to(pl|sh)|ts(70|m\-|m3|m5)|tx\-9|up(\.b|g1|si)|utst|v400|v750|veri|vi(rg|te)|vk(40|5[0-3]|\-v)|vm40|voda|vulc|vx(52|53|60|61|70|80|81|83|85|98)|w3c(\-| )|webc|whit|wi(g |nc|nw)|wmlb|wonu|x700|yas\-|your|zeto|zte\-/i.test(a.substr(0, 4))) check = true;
    })(navigator.userAgent || navigator.vendor || window.opera);
    return check;
};
//code end for check device is mobile or not

var userAgentForTablet = navigator.userAgent.toLowerCase();
var isTablet = /(ipad|tablet|(android(?!.*mobile))|(windows(?!.*phone)(.*touch))|kindle|playbook|silk|(puffin(?!.*(IP|AP|WP))))/.test(userAgentForTablet);
var isLandscape = (window.orientation == 90 || window.orientation == -90) ? true : false;


//code start for check mobile orientation
function checkOrientation() {
    isLandscape = (window.orientation == 90 || window.orientation == -90) ? true : false;
    //if (isTablet && !isLandscape )) {
    if ((isTablet && !isLandscape)) {
        $('.map').click(); //for mobile default map selected
    } else if ((globals.mobileDevice() && (window.orientation == 90 || window.orientation == -90)) && (!isTablet)) {
        $('.supported-content').addClass('invisibleHeight0');
        $('.not-supported').addClass('d-flex');
        $('.not-supported').removeClass('d-none');
    } else {
        $('.not-supported').addClass('d-none');
        $('.not-supported').removeClass('d-flex');
        $('.supported-content').removeClass('invisibleHeight0');
        $('.charts').click();
    }
}
window.addEventListener("orientationchange", checkOrientation, false);
//window.addEventListener("load", checkOrientation, false);
//code end for check mobile orientation


globals.map = null;

//store REST API URL for corresponding polygon
globals.mapServiceUrls = {
    State: "https://services2.arcgis.com/8k2PygHqghVevhzy/arcgis/rest/services/NCOV_World_Countries_States_Provinces_wUnknown/FeatureServer/0",
}

globals.configuration = null;

//join function to retrieve data in CSV column for a given Name & render field index
globals.getRegionMapValue = null;

//join function for setting up infoWindow
globals.getRegionInfo = null;

//selected date (from datepicker), '1-aug-09' is the default
globals.selectedDate = null;

globals.selectedScenario = null;
globals.scenariosDirectory = null;

//file used for rendering
globals.renderFile = null;

//render field index in the csv file's attribute list
//update whenever a range slider is enabed (overlay mode) or a field is selected (single mode)
globals.renderFieldIndex = "Projected Demand (%)";

//QueryTask and Query, used in display level selection, e.g., choose a state
globals.queryTask = null;
globals.query = null;

//added for manually picking counties
globals.queriedRegionNames = [];
globals.queriedRegionNumbers = [];

globals.selectedRegionNum = 0;
globals.selectedRegionName = "";

globals.rawData = {};

globals.jsonData = {};
globals.timelineJsonData = {};
globals.regionData = {};

globals.minHospitalCapacity = 80;
globals.maxHospitalCapacity = 120;

globals.isCapacitySliderApplied = false;
globals.isDurationSliderApplied = false;

globals.hospitalDuration = 8;

globals.regionDataNameColumn = "HRRCITY";
globals.regionDataBedsColumn = "DHS_Beds";
globals.selectedTimelineIndex = 0;

require([
        "esri/Color",
        "esri/geometry/Extent",
        "esri/graphic",
        "esri/dijit/Legend",
        "esri/InfoTemplate",
        "esri/layers/FeatureLayer",
        "esri/layers/GraphicsLayer",
        "esri/map",
        "esri/renderers/ClassBreaksRenderer",
        "esri/symbols/SimpleFillSymbol",
        "esri/symbols/SimpleLineSymbol",
        "esri/renderers/SimpleRenderer",
        "esri/TimeExtent",
        "esri/dijit/TimeSlider",
        "esri/tasks/query",
        "esri/tasks/QueryTask",
        "esri/toolbars/draw",
        "esri/urlUtils",
        "dojo/on",
        "dojo/parser",
        "dojo/_base/array",
        "dojo/_base/lang",
        "dijit/registry",
        "dijit/Tooltip",
        "dojox/data/CsvStore",
        "dijit/layout/BorderContainer",
        "dijit/layout/ContentPane",
        "dojo/domReady!"
    ],
    function(
        Color, Extent, Graphic, Legend, InfoTemplate,
        FeatureLayer, GraphicsLayer, Map, ClassBreaksRenderer,
        SimpleFillSymbol, SimpleLineSymbol, SimpleRenderer,
        TimeExtent, TimeSlider,
        Query, QueryTask, Draw, urlUtils,
        on, parser, arrayUtils,
        lang, registry, Tooltip,
        CsvStore
    ) {
        parser.parse();
        $(document).ready(function() {
            $("#allToggleButton").bootstrapToggle("on");
        });

        $.getJSON("data_us_durations/supported_scenarios.json")
            //$.getJSON("data_va/supported_scenarios.json")
            .done(function(json) {
                globals.configuration = json.configuration;
                globals.scenarios = json.scenarios;
                globals.selectedScenario = globals.scenarios[0];
                globals.scenariosDirectory = globals.selectedScenario.directory;

                $('.applicationTitle').html(globals.configuration.application_title);
                $('#notice').text(globals.configuration.noticeMessage);

                $('#queryByName')[0].value = "";
                globals.durationSlider.noUiSlider.set(globals.configuration.defaultDuration);
                globals.hospitalDuration = globals.configuration.defaultDuration;

                loadRegionData();
                setupMapLayer();
                renderScenarios();
                executeDefaultWorkflow();
            })
            .fail(function(jqxhr, textStatus, error) {
                var err = textStatus + ", " + error;
                console.log("Request Failed to load 'supported_scenarios.json' file. Reason :: " + err);
                $('#overlay').hide();
            });

        // This is to hide Application in Mobile's landscape mode
        if (globals.mobileDevice() || isTablet) { //if its a mobile device
            $('#renderField button:eq(0) ').html("<span class='fa fa-bed' aria-hidden='true'></span>");
            $('#renderField button:eq(1) ').html("<span class='fa fa-users' aria-hidden='true'></span>");
        } else {

            $('.mobilemapChartDataRow').html("");
            $('.mobileQueryBoxRow').html("");
            $('.mobileMapRenderOption').html("");
        }

        $('.applyHospitalCapacity').on('click', function(e) {
            $('#overlay').show();
            updateHospitalCapacity();
        });

        $('.applyHospitalDuration').on('click', function(e) {
            $('#overlay').show();
            updateHospitalDuration();
        });

        bindMenuEvents();
        bindChartAndDataTab();
        bindSearchAndResetButton();
        bindSliderEvents();


        function executeDefaultWorkflow() {
            // Clear all Tooltips
            $('[data-toggle="tooltip"]').tooltip('dispose');

            scenarioChanged = true;

            updateDataForTimeline();

            if (globals.selectedDate == undefined || globals.selectedDate == null) {
                globals.selectedDate = globals.timelineJsonData[0]["date"];
                scenarioChanged = false;
            }

            globals.renderFile = globals.scenariosDirectory + "/duration" + globals.hospitalDuration + "/nssac_ncov_ro_" + globals.selectedDate + ".csv";

            getCSVDataAndRendering();

            if (scenarioChanged) {
                $('#timeline .content').removeClass('content-selected');
                $('#timeline #date-' + globals.selectedDate).addClass('content-selected');
            }

            if ($('#allToggleButton')[0].checked) {
                if (globals.selectedRegionNum != 0) {
                    renderSelectedRegionsChart(globals.selectedRegionNum, globals.selectedRegionName);
                } else if (globals.queriedRegionNames.length != 0) {
                    renderQueriedRegionsChart();
                } else {
                    renderSummaryDataChart();
                }
            } else {
                renderAllScenarios();
            }

            // Select default option as Charts
            if (globals.mobileDevice() || (isTablet && !isLandscape)) {
                $('.map').click(); //for mobile default map selected
            } else {
                $('.charts').click(); //for except mobile chart by default selected
            }

            // Initialize all Tooltips
            $('[data-toggle="tooltip"]').tooltip();

            // Initialize Query Tooltip
            $('[data-toggle="popover"]').popover();
        }

        //initial setup for the map, globals.query and globals.queryTask to query this level by NAME
        function setupMapLayer() {
            globals.defaultExtent = new Extent(globals.configuration.extent);

            var mapMinZoomLevel = globals.configuration.min_zoom_level;
            var mapZoomLevel = globals.configuration.zoom_level;
            if (globals.mobileDevice()) {
                globals.defaultExtent = new Extent(globals.configuration.extentMobile);
                mapZoomLevel = (mapZoomLevel >= 2) ? parseInt(mapZoomLevel) - 1 : mapZoomLevel;
                mapMinZoomLevel = (mapMinZoomLevel >= 2) ? parseInt(mapMinZoomLevel) - 1 : mapMinZoomLevel;
            }

            globals.map = new Map("mapCanvas", {
                basemap: "gray",
                extent: globals.defaultExtent,
                zoom: mapZoomLevel,
                minZoom: mapMinZoomLevel
            });
            globals.map.infoWindow.resize(280, 210);

            var symbol = new SimpleFillSymbol(
                SimpleFillSymbol.STYLE_SOLID,
                new SimpleLineSymbol(
                    SimpleLineSymbol.STYLE_SOLID,
                    new Color([128, 128, 128]), 1),
                new Color([255, 255, 255, 0.5])
            );

            var outline_state_layer = new FeatureLayer(globals.mapServiceUrls.State, {
                id: "outline_state_layer",
                mode: esri.layers.FeatureLayer.MODE_ONDEMAND,
                outFields: ["NAME", "ISO_3"]
            });

            outline_state_layer.setRenderer(new SimpleRenderer(symbol));
            globals.map.addLayers([outline_state_layer]);

            var infoTemplate = new InfoTemplate(
                "Region : ${" + globals.configuration.layer_attribute + "}",
                "${" + globals.configuration.layer_attribute + ":globals.getRegionInfo}"
            );

            var layer = new FeatureLayer(globals.configuration.layer_url, {
                id: "data_layer",
                mode: esri.layers.FeatureLayer.MODE_ONDEMAND,
                infoTemplate: infoTemplate,
                outFields: globals.configuration.out_fields,
                opacity: 0.8
            });

            layer.setRenderer(new SimpleRenderer(symbol));
            globals.map.addLayers([layer]);

            //setup QueryTask (for filter by region)
            setQueryTask();

            globals.map.on("update-end", function() {
                $('#overlay').hide();
            });

            layer.on("update-end", function() {
                $('#overlay').hide();
            });
        }

        function setQueryTask() {
            globals.queryTask = new QueryTask(globals.configuration.layer_url);
            globals.query = new Query();
            globals.query.outSpatialReference = {
                "wkid": 4326
            };
            globals.query.returnGeometry = true;
            globals.query.outFields = [globals.configuration.layer_attribute];

        }

        function getCSVDataAndRendering() {
            fileURL = globals.renderFile;
            $.ajax({
                url: fileURL,
                async: false,
                success: function(csv) {
                    var items = $.csv.toObjects(csv);
                    var jsonobject = JSON.stringify(items);
                    globals.jsonData = JSON.parse(jsonobject);
                },
                dataType: "text",
                complete: function() {
                    if (!globals.renderFieldIndex)
                        globals.renderFieldIndex = "Projected Demand (%)";

                    if (globals.isCapacitySliderApplied)
                        applyCapacitySliderOnSummaryData();

                    showCSVDataInTable(globals.jsonData);
                    setMapRenderer();
                }
            });
        }

        $("#scenariosDropdown").change(function() {
            renderAllScenarios();
        });

        function readDataFromCSVFile(file) {
            $.ajax({
                url: file,
                async: false,
                success: function(csv) {
                    var items = $.csv.toObjects(csv);
                    var jsonobject = JSON.stringify(items);

                    globals.timelineJsonData = JSON.parse(jsonobject);
                    //globals.rawData = JSON.parse(jsonobject);
                },
                dataType: "text",
                complete: function() {}
            });
        }

        function setMapRenderer() {
            renderLegend();
        }

        function renderLegend() {
            //clear out the current legend
            clearDIV("legend");

            //reference the legend div
            var legendDiv = document.getElementById("legend");
            //create a new table to hold the legend items
            var table = document.createElement("table");
            table.id = "legend_table0";

            var renderer = new ClassBreaksRenderer(null, globals.getRegionMapValue);

            var numClasses = 5;
            //different colors for different attribute
            var colors = [];
            if (globals.renderFieldIndex == 'Projected Demand (%)') {

                colors.push(new Color([189, 201, 225]));
                colors.push(new Color([116, 169, 207]));
                colors.push(new Color([43, 140, 190]));
                colors.push(new Color([4, 90, 141]));
                colors.push(new Color([3, 72, 112]));

                globals.minHospitalCapacity = Number(globals.minHospitalCapacity);
                globals.maxHospitalCapacity = Number(globals.maxHospitalCapacity);

                var breakDifference = Number((globals.maxHospitalCapacity - globals.minHospitalCapacity) / 3).toFixed(2);

                // Adding default values for breaks.
                var breakMins = [40, globals.minHospitalCapacity, 90, 100];
                var breakMaxs = [globals.minHospitalCapacity, 89.99, 99.99, globals.maxHospitalCapacity];

                for (i = 1; i < numClasses - 2; i++) {
                    breakMins[i + 1] = Number(globals.minHospitalCapacity + (breakDifference * i)).toFixed(2);
                    breakMaxs[i] = Number(breakMins[i + 1] - 0.01);
                }
                breakMins.push(globals.maxHospitalCapacity);
                breakMaxs.push(500);

            } else {
                numClasses = 6;
                colors.push(new Color([254, 240, 217]));
                colors.push(new Color([253, 212, 158]));
                colors.push(new Color([253, 187, 132]));
                colors.push(new Color([252, 141, 89]));
                colors.push(new Color([227, 74, 51]));
                colors.push(new Color([179, 0, 0]));

                var breakMins = [0, 10, 100, 500, 1000, 10000];
                var breakMaxs = [10, 99, 499, 999, 9999, 299999];
            }

            //add render field to legend
            var tableRow = document.createElement("tr");
            var fieldCell = document.createElement("td");
            fieldCell.setAttribute("colspan", 2);
            tableRow.style.borderBottom = '1px solid gray';
            fieldCell.textContent = globals.renderFieldIndex;
            tableRow.appendChild(fieldCell);
            table.appendChild(tableRow);

            //main loop to add break and set legend (using a table)
            //uses values stored in breakMins and breakMaxs arrays as the breaks
            for (var i = 0; i < numClasses; i++) {
                var BreakMin = breakMins[i];
                var BreakMax = breakMaxs[i];

                renderer.addBreak({
                    minValue: BreakMin,
                    maxValue: BreakMax,
                    symbol: new SimpleFillSymbol(
                        "solid",
                        new SimpleLineSymbol("solid", new Color([128, 128, 128]), 1),
                        colors[i]
                    )
                });

                var tableRow = document.createElement("tr");
                var colorCell = document.createElement("td");

                var hexcolor = ""
                var colorpart = colors[i].r.toString(16)
                if (colorpart == "0") {
                    colorpart = "00"
                }
                if (colorpart.length == 1) { //added condition to cover cases where there is a '0' starting hex code
                    colorpart = "0" + colorpart;
                }
                hexcolor += colorpart;
                var colorpart = colors[i].g.toString(16)
                if (colorpart == "0") {
                    colorpart = "00"
                }
                if (colorpart.length == 1) {
                    colorpart = "0" + colorpart;
                }
                hexcolor += colorpart;
                var colorpart = colors[i].b.toString(16)
                if (colorpart == "0") {
                    colorpart = "00"
                }
                if (colorpart.length == 1) {
                    colorpart = "0" + colorpart;
                }
                hexcolor += colorpart;

                colorCell.setAttribute("style", "background-color: #" + hexcolor + "; width: 15px");

                var labelCell = document.createElement("td");

                var labelText;

                if (i == 0)
                    labelText = "< " + BreakMax.toLocaleString();
                else if (i != numClasses - 1) {
                    if (globals.renderFieldIndex == 'Projected Demand (%)')
                        labelText = Number(BreakMin).toFixed(1).toLocaleString() + " - " + Number(BreakMax).toFixed(1).toLocaleString();
                    else
                        labelText = Number(BreakMin).toLocaleString() + " - " + Number(BreakMax).toLocaleString();
                } else
                    labelText = BreakMin.toLocaleString() + " +";
                labelCell.textContent = labelText;

                tableRow.appendChild(colorCell);
                tableRow.appendChild(labelCell);
                table.appendChild(tableRow);
            }

            globals.map.getLayer("data_layer").setRenderer(renderer);
            globals.map.getLayer("data_layer").redraw();

            //add completed legend table
            legendDiv.appendChild(table);

            $('#overlay').hide();
        }

        function changeDate(selectedDate) {
            globals.selectedDate = selectedDate;
            globals.renderFile = globals.scenariosDirectory + "/duration" + globals.hospitalDuration + "/nssac_ncov_ro_" + selectedDate + ".csv";

            //check whether file exists
            var http = new XMLHttpRequest();
            http.open('HEAD', globals.renderFile, false);
            http.send();
            if (http.status === 404) {
                if ((globals.mobileDevice() || isTablet) && $('#dataView').hasClass('disabled')) {
                    alert("Data for " + selectedDate + " is not available yet.");
                }
            } else {
                renderByFile();
            }
        }

        //Lots of clean up is required before reading the file
        function renderByFile() {
            //clear display option
            clearDIV("legend");
            getCSVDataAndRendering();
        }

        //Change rendering field, this is ONLY for single attribute mode
        function changeRenderField(event) {
            var clickedButton = event.target;

            globals.renderFieldIndex = event.target.value;
            if (!event.target.value) {
                globals.renderFieldIndex = event.target.parentElement.value;
                clickedButton = event.target.parentElement;
            }

            $('.renderField').addClass('disabled');
            $(clickedButton).removeClass('disabled');

            //use new field to render
            setMapRenderer(false);
        }

        globals.getRegionMapValue = function(value) {
            for (var i = 0; i < globals.jsonData.length; i++) {
                var fipsValue = (value.hasOwnProperty("attributes")) ? value.attributes[globals.configuration.layer_attribute] : value;
                var key = Object.keys(globals.jsonData[i])[1];
                var csvFipsValue = globals.jsonData[i][key];

                if (fipsValue == csvFipsValue) {
                    return Number(globals.jsonData[i][globals.renderFieldIndex]);
                }
            }
            return 0;
        }

        globals.getRegionInfo = function(value) {
            var returnValue = '';
            for (var i = 0; i < globals.jsonData.length; i++) {
                var key = Object.keys(globals.jsonData[i])[1];
                if (globals.jsonData[i][key] == value) {
                    returnValue += "<b> Percentage of Occupied Beds:</b><br>&emsp;" + globals.jsonData[i]["Total Projected Demand (Range)"];
                    returnValue += "<br><b>Weekly Hospitalizations:</b><br>&emsp;" + globals.jsonData[i]["Total Hospitalizations (Range)"];

                    var regionNumKey = Object.keys(globals.jsonData[i])[0];
                    globals.selectedRegionNum = globals.jsonData[i][regionNumKey];

                    var regionNameKey = Object.keys(globals.jsonData[i])[1];
                    globals.selectedRegionName = globals.jsonData[i][regionNameKey];

                    if (globals.queriedRegionNames.length != 0) {
                        $('.getQueryResultsBtn').removeClass('d-none');
                        $('.getQueryResultsBtn').addClass('d-flex');
                    }

                    // Clear all Tooltips
                    $('[data-toggle="tooltip"]').tooltip('dispose');

                    updateDataForTimeline();
                    renderSelectedRegion();

                    // Initialize all Tooltips
                    $('[data-toggle="tooltip"]').tooltip();

                    // Initialize Query Tooltip
                    $('[data-toggle="popover"]').popover();

                    $('#timeline .content').removeClass('content-selected');
                    $('#timeline #date-' + globals.selectedDate).addClass('content-selected');

                    break;
                }
            }

            return returnValue;
        }

        function clearDIV(divID) {
            var div = document.getElementById(divID);
            while (div.childNodes.length > 0) {
                div.removeChild(div.childNodes[0]);
            }
        }

        function queryByName() {
            $('#overlay').show();

            var inputStr = $("#queryByName").val();

            if (inputStr.length == 0) {
                $('#overlay').hide();
                return;
            }

            globals.map.infoWindow.hide();
            globals.selectedRegionNum = 0;

            inputStr = inputStr.replace(/%/g, '');
            var inputStrSplit = inputStr.split(",");
            var where = '';

            for (var i = 0; i < inputStrSplit.length; i++) {
                var temp = inputStrSplit[i].trim();
                if (temp == "") continue;

                if (where == '')
                    where += globals.configuration.layer_attribute + " LIKE '%" + temp.toString() + "%'";
                else
                    where += " OR " + globals.configuration.layer_attribute + " LIKE '%" + temp.toString() + "%'";
            }

            //now query correspding layer
            query = new Query();
            query.outSpatialReference = {
                "wkid": 102100
            };
            query.returnGeometry = true;
            //setup QueryTask (for display Level selection)
            var queryTask = new QueryTask(globals.configuration.layer_url);
            query.outFields = globals.configuration.out_fields;

            query.where = where;
            var symbol = new SimpleFillSymbol(
                SimpleFillSymbol.STYLE_BACKWARD_DIAGONAL,
                new SimpleLineSymbol(
                    SimpleLineSymbol.STYLE_SOLID,
                    new Color([102, 255, 255]),
                    2
                ),
                new Color([255, 0, 0])
            );
            var names = [];
            var selectedHRRNum = [];

            queryTask.execute(query, function(fset) {
                globals.map.graphics.clear();
                if (fset.features.length > 0) {
                    for (var i = 0; i < fset.features.length; i++) {
                        //symbol for selected county
                        var graphic = new Graphic(fset.features[i].geometry, symbol);
                        globals.map.graphics.add(graphic);

                        var temp = fset.features[i].attributes[globals.configuration.layer_attribute];
                        var hrrNumber = fset.features[i].attributes[globals.configuration.query_attribute];
                        if (names.indexOf(temp) == -1) {
                            names.push(temp);
                            selectedHRRNum.push(hrrNumber);
                        }
                    }
                    globals.queriedRegionNames = names;
                    globals.queriedRegionNumbers = selectedHRRNum;

                    var extent = esri.graphicsExtent(fset.features);
                    globals.map.setExtent(extent, true);

                    // Clear all Tooltips
                    $('[data-toggle="tooltip"]').tooltip('dispose');

                    updateDataForTimeline();

                    // Initialize all Tooltips
                    $('[data-toggle="tooltip"]').tooltip();

                    // Initialize Query Tooltip
                    $('[data-toggle="popover"]').popover();

                    $('#timeline .content').removeClass('content-selected');
                    $('#timeline #date-' + globals.selectedDate).addClass('content-selected');

                    // Display Chart
                    if ($('#allToggleButton')[0].checked) {
                        renderQueriedRegionsChart();
                    } else {
                        renderAllScenarios();
                    }
                    showCSVDataInTable(globals.jsonData);

                } else {
                    $('.queryResultPopUp')[0].innerHTML = "No result found for <b>" + inputStr + "</b>.";
                    $('#noResultFoundButton').click();
                    $('#overlay').hide(); //need to remove from here later(hide on mobile after query button clicked)
                }
            });

            $('.getQueryResultsBtn').removeClass('d-flex');
            $('.getQueryResultsBtn').addClass('d-none');
        }

        function renderSelectedRegion() {
            var where = globals.configuration.layer_attribute + " = '" + globals.selectedRegionName + "'";

            //now query correspding layer
            query = new Query();
            query.outSpatialReference = {
                "wkid": 102100
            };
            query.returnGeometry = true;
            //setup QueryTask (for display Level selection)
            var queryTask = new QueryTask(globals.configuration.layer_url);
            query.outFields = globals.configuration.out_fields;

            query.where = where;
            var symbol = new SimpleFillSymbol(
                SimpleFillSymbol.STYLE_BACKWARD_DIAGONAL,
                new SimpleLineSymbol(
                    SimpleLineSymbol.STYLE_SOLID,
                    new Color([102, 255, 255]),
                    2
                ),
                new Color([255, 0, 0])
            );

            queryTask.execute(query, function(fset) {
                globals.map.graphics.clear();
                if (fset.features.length > 0) {
                    for (var i = 0; i < fset.features.length; i++) {
                        var graphic = new Graphic(fset.features[i].geometry, symbol);
                        globals.map.graphics.add(graphic);
                    }

                    if ($('#allToggleButton')[0].checked) {
                        renderSelectedRegionsChart(globals.selectedRegionNum, globals.selectedRegionName);
                    } else {
                        renderAllScenarios();
                    }

                    showCSVDataInTable(globals.jsonData);
                    var extent = esri.graphicsExtent(fset.features);
                    globals.map.setExtent(extent, true);
                } else {
                    $('.queryResultPopUp')[0].innerHTML = "No result found for <b>" + inputStr + "</b>.";
                    $('#noResultFoundButton').click();
                }
            });
        }

        function showCSVDataInTable(csvData) {
            var filteredNames = [];
            if (globals.selectedRegionNum != 0) {
                filteredNames.push(globals.selectedRegionName);
            } else if (globals.queriedRegionNames.length != 0) {
                filteredNames = globals.queriedRegionNames;
            }
            var tableHTML = null;
            var lengthMenuOptions = null;
            var downloadOptions = "";
            downloadAllOption = "";

            var regionNameColumn = Object.keys(csvData[0])[1];
            tableHTML = '<table id="example" class="display" cellspacing="0" width="100%">\n<thead><tr>';
            tableHTML += "<th>" + "Region Name" + "</th>";
            tableHTML += "<th>" + "Percentage of Occupied Beds" + "</th>";
            tableHTML += "<th>" + "Weekly Hospitalizations" + "</th>";

            tableHTML += "</tr></thead><tbody>";
            for (var i = 0; i < csvData.length; i++) {
                var name = csvData[i][regionNameColumn];

                if (filteredNames.length > 0 && filteredNames.indexOf(name) == -1)
                    continue;
                else {
                    tableHTML += "<tr>";

                    // Region Name, Hospitalizations (Range), Projected Demand (Range)
                    tableHTML += "<td>" + csvData[i][regionNameColumn] + "</td>";
                    tableHTML += "<td>" + csvData[i]["Total Projected Demand (Range)"] + "</td>";
                    tableHTML += "<td>" + csvData[i]["Total Hospitalizations (Range)"] + "</td>";

                    tableHTML += "</tr>\n";
                }
            }
            tableHTML += "</table>";
            dojo.byId("dataTable").innerHTML = tableHTML;

            if (/Android|webOS|iPhone|iPod|ipad|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent)) {
                lengthMenuOptions = '<select> <option value="10">10</option> <option value="25">25</option>' +
                    '<option value="50">50</option> <option value="-1">All</option> </select>';

                downloadOptions = '<i class="fa fa-download" aria-hidden="true"></i>';
                downloadAllOption = '<i class="fa fa-download float-right" aria-hidden="true"></i>';
            } else {
                lengthMenuOptions = 'Display <select> <option value="10">10</option> <option value="25">25</option>' +
                    '<option value="50">50</option> <option value="-1">All</option> </select>';

                downloadOptions = 'Download';
                downloadAllOption = 'Download All';
            }

            $('table.display').DataTable({
                //dom: 'Blfrtip',
                "order": [
                    // [0, "asc"]
                ],
                scrollX: true,
                scrollCollapse: true,
                //"searching": false,
                "language": {
                    search: '',
                    lengthMenu: lengthMenuOptions
                },
                oLanguage: {
                    "oPaginate": {
                        "sNext": '<i title="Next" class="fa fa-chevron-right" ></i>',
                        "sPrevious": '<i title="Previous" class="fa fa-chevron-left" ></i>'
                    }
                },
                // buttons: [{
                //     extend: 'csvHtml5',
                //     text: downloadOptions,
                //     titleAttr: 'CSV'
                // }, {
                //     extend: 'csvHtml5',
                //     text: downloadAllOption,
                //     titleAttr: 'CSV',
                //     className: 'excelButton',
                //     action: function(e, dt, node, config) {
                //         downloadAll();
                //     }
                // }],
                columnDefs: [{
                    render: function(data, type, full, meta) {
                        return "<div class='text-wrap width-600'>" + data + "</div>";
                    },
                    targets: 0
                }]
            });
        }

        $.fn.DataTable.ext.pager.numbers_length = 5;

        function renderTimeline() {
            var timelineHTML = "";
            timelineHTML = '<div id="timeline" class="d-flex owl-carousel timeline-contener" style="align-items: center;">';
            // Iterate over Summary data and create Timelines
            for (index = 0; index < globals.timelineJsonData.length - 1; index++) {
                actualDateString = globals.timelineJsonData[index]["date"];

                formattedDate = new Date(globals.timelineJsonData[index]["date"].replace(/-/g, "/"));
                representationDate = new Date(formattedDate).toDateString().slice(4).substring(0, 6);

                totalProjectedDemand = Number(globals.timelineJsonData[index]["Total Projected Demand (%)"]).toFixed(2);
                totalHospitalizations = Number(globals.timelineJsonData[index]["Total Hospitalizations (Median)"]);

                totalHospitalizationsRange = globals.timelineJsonData[index]["Total Hospitalizations (Range)"];
                totalProjectedDemandRange = globals.timelineJsonData[index]["Total Projected Demand (Range)"];

                var toolTipText = 'Weekly Hospitalizations [Range] <br>' +
                    '&emsp;<b>' + totalHospitalizationsRange + '</b><br>' +

                    'Percentage of Occupied Beds [Range] <br>' +
                    '&emsp;<b>' + totalProjectedDemandRange + '</b><br>';

                if (index === 0) {
                    timelineHTML +=
                        '<div class="d-flex content content-selected pr-md-2 item" id="date-' + actualDateString + '"' +
                        'data-toggle="popover" data-html="true" data-container=".timeline-contener" data-trigger="hover focus" data-placement="top"' +
                        'data-title="Week ending ' + representationDate + '" data-content="' + toolTipText + '">';
                } else {
                    timelineHTML +=
                        '<div class="d-flex content pr-md-2 item" id="date-' + actualDateString + '"' +
                        'data-toggle="popover" data-html="true" data-container=".timeline-contener" data-trigger="hover focus " data-placement="top"' +
                        'data-title="Week ending ' + representationDate + '" data-content="' + toolTipText + '">';
                }

                timelineHTML += '<div class="d-flex date">' + representationDate + '</div>' +
                    '<div class="content-data" style="flex:1;">' +
                    '<div class="d-flex justify-content-center">' +
                    '<div class="content-data-icon"><i class="fa fa-users"></i></div>' +
                    '<div class="cases">' + numFormatter(totalHospitalizations) + '</div></div>' +
                    '<div class="d-flex justify-content-center">' +
                    '<div class="content-data-icon"><i class="fa fa-bed"></i></div>' +
                    '<div class="beds">' + totalProjectedDemand + ' %</div></div>' +
                    '</div></div>';

            }

            timelineHTML += '</div>';

            $('.timeline-content-section').html(timelineHTML);
            timelineHTML = "";
            $('#timeline').owlCarousel({
                loop: false,
                margin: 5,
                nav: true,
                responsiveClass: true,
                startPosition: globals.selectedTimelineIndex,
                navText: ["<div class='nav-btn timeline-prev-slide'><i class='fa fa-chevron-left' aria-hidden='true'></i></div>", "<div class='nav-btn timeline-next-slide'><i class='fa fa-chevron-right' aria-hidden='true'></i></div>"],
                responsive: {
                    0: {
                        items: 2,
                    },
                    600: {
                        items: 3,
                    },
                    1000: {
                        items: 3,
                    },
                    1281: {
                        items: 4,
                    },
                    1441: {
                        items: 6
                    }
                }
            });

            $('#timeline .content').off().on('click', function(event) {
                selectedDate = event.currentTarget.id.substring(5);
                globals.selectedTimelineIndex = $('#timeline .content').index(this);
                // Remove selection
                $(".content-selected").each(function(i, item) {
                    $(item).removeClass('content-selected');
                });

                // Add selection class to current timeline
                $(event.currentTarget).addClass('content-selected');

                globals.map.infoWindow.hide();
                changeDate(selectedDate);
            });
        }

        var timelineVideo = [];
        var currentSelectedTimeline = 0;
        var selectedDate;
        var isPaused = false;

        $('#playTimelineVideo').off().on('click', function(event) { //stop button clciked timeline video action
            $('#playTimelineVideo').addClass('disableVideoBtn');
            $('#pauseTimelineVideo').removeClass('disableVideoBtn');
            $('#stopTimelineVideo').removeClass('disableVideoBtn');
            $('.scenarioRow, .sliderRow, .mapContainer, .timeline-content').css({ "pointer-events": "none", "opacity": "0.95" });

            $("#timeline .owl-item").each(function(currentLoopingItemIndex, currentLoopingItem) {

                if (!isPaused && currentSelectedTimeline === 0) {
                    $('#timeline').trigger('to.owl.carousel', 0);
                }

                if (currentSelectedTimeline <= currentLoopingItemIndex) { //start from where paused or where end like when click play after complete of play items
                    timelineVideo.push(setTimeout(function() {
                        selectedDate = $(currentLoopingItem).children().attr('id').substring(5);
                        if ((currentLoopingItemIndex !== 0 && $("#timeline .owl-item.active").index($(currentLoopingItem)) !== 0)) { //if its not first element/Item and also not starting from vissible item on slider
                            $('#timeline').trigger('next.owl.carousel');
                        }
                        $("#timeline .content-selected").removeClass('content-selected');
                        $(currentLoopingItem).children().addClass('content-selected');
                        currentSelectedTimeline = currentLoopingItemIndex; //current IteemSelected and data showing for this item
                        if (currentLoopingItemIndex == ($("#timeline .owl-item").length - 1)) { //if last item on play
                            currentSelectedTimeline = 0;
                            isPaused = false;
                            $('.scenarioRow, .sliderRow, .mapContainer, .timeline-content').css({ "pointer-events": "painted", "opacity": "1.0" });
                            $('#playTimelineVideo').removeClass('disableVideoBtn');
                            $('#pauseTimelineVideo').addClass('disableVideoBtn');
                            $('#stopTimelineVideo').addClass('disableVideoBtn');
                        }
                        globals.map.infoWindow.hide();
                        changeDate(selectedDate);
                    }, currentLoopingItemIndex * 2000));
                }
            });
        });

        $('#stopTimelineVideo').off().on('click', function(event) { //stop button clciked timeline video action
            $('#playTimelineVideo').removeClass('disableVideoBtn');
            $('#pauseTimelineVideo').addClass('disableVideoBtn');
            $('.scenarioRow, .sliderRow, .mapContainer, .timeline-content').css({ "pointer-events": "painted", "opacity": "1.0" });
            $('#stopTimelineVideo').addClass('disableVideoBtn');
            timelineVideo.forEach(function(timer) {
                clearTimeout(timer);
            });
            currentSelectedTimeline = 0;
            isPaused = false;
            selectedDate = $("#timeline .owl-item").children('div:first').attr('id').substring(5);
            globals.map.infoWindow.hide();
            changeDate(selectedDate);
            $('#timeline').trigger('to.owl.carousel', 0);
            $("#timeline .owl-item").children().removeClass('content-selected');
            $("#timeline .owl-item").children('div:first').addClass('content-selected');
        });

        $('#pauseTimelineVideo').off().on('click', function(event) { //pause button clciked timeline video action
            $('#playTimelineVideo').removeClass('disableVideoBtn');
            $('#pauseTimelineVideo').addClass('disableVideoBtn');
            $('#stopTimelineVideo').removeClass('disableVideoBtn');
            //when pause cleartimeout so it will start from where it left with new instance
            timelineVideo.forEach(function(timer) {
                clearTimeout(timer);
            });
            isPaused = true;
        });

        function renderScenarios() {

            var scenarioHTML = "";
            for (index = 0; index < globals.scenarios.length; index++) {

                scenarioName = globals.scenarios[index].scenario_display_name_line1;
                scenarioNameSecondLine = globals.scenarios[index].scenario_display_name_line2;
                scenarioDisplayName = scenarioName + "</br>" + scenarioNameSecondLine;
                scenarioDirectory = globals.scenarios[index].directory;

                if (index == 0) {
                    scenarioHTML += '<div class="d-flex selected-scenario scenario-content item" data-scenario-directory="' + scenarioDirectory + '" data-scenario="' + scenarioName + '"' +
                        'data-toggle="popover" data-html="true" data-trigger="hover focus" data-placement="bottom" data-title="' + scenarioDisplayName + '" data-content="' + globals.scenarios[index].description + '">';
                } else {
                    scenarioHTML += '<div class="d-flex scenario-content item" data-scenario-directory="' + scenarioDirectory + '" data-scenario="' + scenarioName + '"' +
                        'data-toggle="popover" data-html="true" data-trigger="hover focus" data-placement="bottom" data-title="' + scenarioDisplayName + '" data-content="' + globals.scenarios[index].description + '">';
                }
                scenarioHTML += '<div class="d-flex mr-1" style="align-items: center;">' +
                    '<img class="scenario-icon" src="images/scenario.png" alt="Scenario"></div>' +
                    '<div class="scenario-name">' + scenarioDisplayName + '</div></div>';
            }

            $('#scenarios').html(scenarioHTML);
            $('#scenarios').owlCarousel({
                loop: false,
                margin: 5,
                nav: true,
                responsiveClass: true,
                navText: ["<div class='nav-btn prev-slide'><i class='fa fa-chevron-left' aria-hidden='true'></i></div>", "<div class='nav-btn next-slide'><i class='fa fa-chevron-right' aria-hidden='true'></i></div>"],
                responsive: {
                    0: {
                        items: 2,
                    },
                    600: {
                        items: 4,
                    },
                    1000: {
                        items: 4,
                    },
                    1281: {
                        items: 5,
                    },
                    1441: { //code added for responsive in large desktop as "Wrapping" Scenario names #38 (git issue number)
                        items: 6
                    }
                }
            });
            $('#scenarios .scenario-content').off().on('click', function(event) {
                $('#overlay').show();
                selectedScenarioDirectory = event.currentTarget.dataset.scenarioDirectory;
                globals.scenariosDirectory = selectedScenarioDirectory;

                // Remove selection
                $(".selected-scenario").each(function(i, item) {
                    $(item).removeClass('selected-scenario');
                });

                // Add selection class to current timeline
                $(event.currentTarget).addClass('selected-scenario');

                globals.map.infoWindow.hide();
                executeDefaultWorkflow();
            });
        }

        function updateDataForTimeline() {
            // Condition to display selected region data.
            if (globals.selectedRegionNum != 0) {
                var regionFile = globals.scenariosDirectory + "/regions/nssac_ncov_ro_summary_region_" + globals.selectedRegionNum + ".csv";
                readDataFromCSVFile(regionFile);
            } else if (globals.queriedRegionNames.length == 0) {
                var summaryFile = globals.scenariosDirectory + "/duration" + globals.hospitalDuration + "/nssac_ncov_ro-summary.csv";
                readDataFromCSVFile(summaryFile);
            } else {
                globals.timelineJsonData = mergeDataAcrossRegions();
            }

            // Once raw data (daily data) is available, apply duration slider on raw data and create timeline data
            if (globals.isDurationSliderApplied)
                applyDurationSliderOnTimelineData();

            renderTimeline();
        }

        function updateHospitalCapacity() {
            // $('#overlay').show();
            globals.isCapacitySliderApplied = true;

            applyCapacitySliderOnSummaryData();
            applyCapacitySliderOnTimelineData();

            renderTimeline();

            if ($('#allToggleButton')[0].checked) {
                if (globals.selectedRegionNum != 0) {
                    renderSelectedRegionsChart(globals.selectedRegionNum, globals.selectedRegionName);
                } else if (globals.queriedRegionNames.length != 0) {
                    renderQueriedRegionsChart();
                } else {
                    renderSummaryDataChart();
                }
            } else {
                renderAllScenarios();
            }

            showCSVDataInTable(globals.jsonData);

            // Hide popup if any on map.
            globals.map.infoWindow.hide();
            setMapRenderer();

            // Initialize all Tooltips
            $('[data-toggle="tooltip"]').tooltip();

            // Initialize Query Tooltip
            $('[data-toggle="popover"]').popover();

            $('#timeline .content').removeClass('content-selected');
            $('#timeline #date-' + globals.selectedDate).addClass('content-selected');
        }

        function applyCapacitySliderOnSummaryData() {
            var percentDemand = globals.minHospitalCapacity / 100;

            for (var i = 0; i < globals.jsonData.length; i++) {
                var beds = Number(globals.regionData[i][globals.regionDataBedsColumn]);

                var med_proj_dem = Number(((percentDemand * beds) + Number(globals.jsonData[i]["Max Occupied Beds"])) * 100 / beds).toFixed(2);
                var lb_proj_dem = Number(((percentDemand * beds) + Number(globals.jsonData[i]["Lower Max Occupied Beds"])) * 100 / beds).toFixed(2);
                var ub_proj_dem = Number(((percentDemand * beds) + Number(globals.jsonData[i]["Upper Max Occupied Beds"])) * 100 / beds).toFixed(2);

                globals.jsonData[i]["Lower Projected Demand Bound"] = lb_proj_dem;
                globals.jsonData[i]["Upper Projected Demand Bound"] = ub_proj_dem;
                globals.jsonData[i]["Total Projected Demand (%)"] = med_proj_dem;
                globals.jsonData[i]["Projected Demand (%)"] = med_proj_dem;

                globals.jsonData[i]["Total Projected Demand (Range)"] = med_proj_dem + "% [" + lb_proj_dem + "% - " + ub_proj_dem + "%]";
            }
        }

        function applyCapacitySliderOnTimelineData() {
            var percentDemand = globals.minHospitalCapacity / 100;

            var cumulativeBeds = getCumulativeBeds();

            for (var i = 0; i < globals.timelineJsonData.length; i++) {

                var med_proj_dem = Number(((percentDemand * cumulativeBeds) + Number(globals.timelineJsonData[i]["Max Occupied Beds"])) * 100 / cumulativeBeds).toFixed(2);
                var lb_proj_dem = Number(((percentDemand * cumulativeBeds) + Number(globals.timelineJsonData[i]["Lower Max Occupied Beds"])) * 100 / cumulativeBeds).toFixed(2);
                var ub_proj_dem = Number(((percentDemand * cumulativeBeds) + Number(globals.timelineJsonData[i]["Upper Max Occupied Beds"])) * 100 / cumulativeBeds).toFixed(2);

                globals.timelineJsonData[i]["Lower Projected Demand Bound"] = lb_proj_dem;
                globals.timelineJsonData[i]["Upper Projected Demand Bound"] = ub_proj_dem;
                globals.timelineJsonData[i]["Total Projected Demand (%)"] = med_proj_dem;
                globals.timelineJsonData[i]["Projected Demand (%)"] = med_proj_dem;

                globals.timelineJsonData[i]["Total Projected Demand (Range)"] = med_proj_dem + "% [" + lb_proj_dem + "% - " + ub_proj_dem + "%]";
            }
        }

        function updateHospitalDuration() {
            $('#overlay').show();

            globals.isDurationSliderApplied = true;

            applyDurationSliderOnTimelineData();
            renderTimeline();

            if ($('#allToggleButton')[0].checked) {
                if (globals.selectedRegionNum != 0) {
                    renderSelectedRegionsChart(globals.selectedRegionNum, globals.selectedRegionName);
                } else if (globals.queriedRegionNames.length != 0) {
                    renderQueriedRegionsChart();
                } else {
                    renderSummaryDataChart();
                }
            } else {
                renderAllScenarios();
            }

            // Hide popup if any on map.
            globals.map.infoWindow.hide();

            globals.renderFile = globals.scenariosDirectory + "/duration" + globals.hospitalDuration + "/nssac_ncov_ro_" + globals.selectedDate + ".csv";
            getCSVDataAndRendering();

            // showCSVDataInTable();
            // setMapRenderer();

            // Initialize all Tooltips
            $('[data-toggle="tooltip"]').tooltip();

            // Initialize Query Tooltip
            $('[data-toggle="popover"]').popover();

            $('#timeline .content').removeClass('content-selected');
            $('#timeline #date-' + globals.selectedDate).addClass('content-selected');
        }

        function applyDurationSliderOnTimelineData() {

            var applyDuration = true;
            // Condition to display selected region data.
            if (globals.selectedRegionNum != 0) {
                var regionFile = globals.scenariosDirectory + "/regions/nssac_ncov_ro_summary_region_" + globals.selectedRegionNum + "-daily.csv";
                globals.rawData = getJSONData(regionFile);
            } else if (globals.queriedRegionNames.length == 0) {
                var summaryFile = globals.scenariosDirectory + "/duration" + globals.hospitalDuration + "/nssac_ncov_ro-summary.csv";
                globals.timelineJsonData = getJSONData(summaryFile);
                applyDuration = false;
            } else {
                globals.rawData = mergeDailyDataAcrossRegions();
            }

            if (applyDuration) {
                var cumulativeBeds = 0;

                if (globals.selectedRegionNum != 0) {
                    for (var i = 0; i < globals.regionData.length; i++) {
                        if (globals.selectedRegionName == globals.regionData[i][globals.regionDataNameColumn]) {
                            cumulativeBeds = Number(globals.regionData[i][globals.regionDataBedsColumn]);
                            break;
                        }
                    }
                } else if (globals.queriedRegionNumbers.length > 0) {
                    for (i = 0; i < globals.queriedRegionNames.length; i++) {
                        var regionName = globals.queriedRegionNames[i] + "";

                        for (var i = 0; i < globals.regionData.length; i++) {
                            if (regionName == globals.regionData[i][globals.regionDataNameColumn]) {
                                cumulativeBeds = cumulativeBeds + Number(globals.regionData[i][globals.regionDataBedsColumn]);
                                break;
                            }
                        }
                    }
                } else {
                    for (var i = 0; i < globals.regionData.length; i++) {
                        cumulativeBeds = cumulativeBeds + Number(globals.regionData[i][globals.regionDataBedsColumn]);
                    }
                }

                var dailyData = globals.rawData;
                for (var i = 0; i < dailyData.length; i++) {
                    dailyData[i]["cumulative"] = Number(dailyData[i]["Total Hospitalizations (Median)"]);
                    dailyData[i]["cumulative_lower_bound"] = Number(dailyData[i]["Lower Hospitalization Bound"]);
                    dailyData[i]["cumulative_upper_bound"] = Number(dailyData[i]["Upper Hospitalization Bound"]);

                    for (j = 1; j < globals.hospitalDuration; j++) {
                        var previousDate = Number(i - j);
                        if (previousDate < 0) break;

                        dailyData[i]["cumulative"] = Number(dailyData[i]["cumulative"]) + Number(dailyData[previousDate]["Total Hospitalizations (Median)"]);
                        dailyData[i]["cumulative_lower_bound"] = Number(dailyData[i]["cumulative_lower_bound"]) + Number(dailyData[previousDate]["Lower Hospitalization Bound"]);
                        dailyData[i]["cumulative_upper_bound"] = Number(dailyData[i]["cumulative_upper_bound"]) + Number(dailyData[previousDate]["Upper Hospitalization Bound"]);
                    }
                }

                var percentDemand = Number(globals.minHospitalCapacity / 100).toFixed(2);

                for (var i = 0; i < globals.timelineJsonData.length; i++) {
                    var currentDate = globals.timelineJsonData[i]["date"];
                    var index = 0;

                    for (index = 0; index < dailyData.length; index++) {
                        if (dailyData[index].date == currentDate) {
                            break;
                        }
                    }

                    var maxCapacity = 0;
                    var maxLowerCapacity = 0;
                    var maxUpperCapacity = 0;

                    for (var j = 0; j < 7; j++) {
                        var cumulative = Number(dailyData[index - j]["cumulative"]);

                        if (cumulative > maxCapacity) {
                            maxCapacity = Number(cumulative);
                            maxLowerCapacity = Number(dailyData[index - j]["cumulative_lower_bound"]);
                            maxUpperCapacity = Number(dailyData[index - j]["cumulative_upper_bound"]);
                        }
                    }

                    var totalProjectedDemand = 100 * ((Number(percentDemand) * cumulativeBeds) + maxCapacity) / cumulativeBeds;
                    var lowerProjectedDemand = 100 * ((Number(percentDemand) * cumulativeBeds) + maxLowerCapacity) / cumulativeBeds;
                    var upperProjectedDemand = 100 * ((Number(percentDemand) * cumulativeBeds) + maxUpperCapacity) / cumulativeBeds;

                    globals.timelineJsonData[i]["Total Projected Demand (%)"] = Number(totalProjectedDemand).toFixed(2);
                    globals.timelineJsonData[i]["Lower Projected Demand Bound"] = Number(lowerProjectedDemand).toFixed(2);
                    globals.timelineJsonData[i]["Upper Projected Demand Bound"] = Number(upperProjectedDemand).toFixed(2);

                    globals.timelineJsonData[i]["Max Occupied Beds"] = maxCapacity;
                    globals.timelineJsonData[i]["Lower Max Occupied Beds"] = maxLowerCapacity;
                    globals.timelineJsonData[i]["Upper Max Occupied Beds"] = maxUpperCapacity;

                    globals.timelineJsonData[i]["Total Projected Demand (Range)"] = Number(totalProjectedDemand).toFixed(2) +
                        "% [" + Number(lowerProjectedDemand).toFixed(2) + "% - " + Number(upperProjectedDemand).toFixed(2) + "%]";
                }
            }

            if (globals.isCapacitySliderApplied)
                applyCapacitySliderOnTimelineData();
        }

        function resetApplication() {
            var queryString = $('#queryByName')[0].value;

            if (globals.selectedRegionNum == 0 && globals.queriedRegionNames.length == 0 && queryString.length == 0 && !globals.isCapacitySliderApplied)
                return;

            globals.isCapacitySliderApplied = false;
            globals.isDurationSliderApplied = false;

            globals.map.graphics.clear();
            globals.map.infoWindow.hide();
            globals.queriedRegionNames = [];
            globals.queriedRegionNumbers = [];
            globals.selectedRegionNum = 0;

            $('#queryByName')[0].value = "";
            globals.map.setExtent(globals.defaultExtent);

            $('.getQueryResultsBtn').removeClass('d-flex');
            $('.getQueryResultsBtn').addClass('d-none');

            globals.rangeSlider.noUiSlider.set([80, 120]);
            globals.durationSlider.noUiSlider.set(globals.configuration.defaultDuration);

            $('#allToggleButton').bootstrapToggle("on");

            // Select first scenario.
            globals.selectedDate = null;
            $('#scenarios .scenario-content').first().click();
        }

        function resetMap() {
            var queryString = $('#queryByName')[0].value;
            if (globals.selectedRegionNum == 0 && globals.queriedRegionNames.length == 0 && queryString.length == 0 && !globals.isCapacitySliderApplied && !globals.isDurationSliderApplied)
                return;

            globals.isCapacitySliderApplied = false;
            globals.isDurationSliderApplied = false;

            globals.map.graphics.clear();
            globals.map.infoWindow.hide();
            globals.queriedRegionNames = [];
            globals.queriedRegionNumbers = [];
            globals.selectedRegionNum = 0;

            $('#queryByName')[0].value = "";
            globals.map.setExtent(globals.defaultExtent);

            $('.getQueryResultsBtn').removeClass('d-flex');
            $('.getQueryResultsBtn').addClass('d-none');

            globals.rangeSlider.noUiSlider.set([80, 120]);
            globals.durationSlider.noUiSlider.set(globals.configuration.defaultDuration);

            $('#allToggleButton').bootstrapToggle("on");

            executeDefaultWorkflow();
        }

        function bindSearchAndResetButton() {
            $('#renderField, #renderFieldMobile').on('click', function(e) {
                changeRenderField(e);
            });

            $('.resetBtn').on('click', function(e) {
                resetMap();
            });

            $('.resetDefault').on('click', function(e) {
                resetApplication();
            });

            $('.queryFilter, .getQueryResultsBtn').on('click', function(e) {
                queryByName();
            });

            //add response to enter key on query input box
            $("#queryByName").keypress(function(event) {
                if (event.keyCode == 13) {
                    queryByName();
                }
            });
        }

    });

function getCumulativeBeds() {
    var cumulativeBeds = 0;

    // If user has clicked on any region then, cumulative beds will be count of that region only.
    // Else cumulative beds for all regions.
    if (globals.selectedRegionNum != 0) {
        for (var i = 0; i < globals.regionData.length; i++) {
            if (globals.selectedRegionName == globals.regionData[i][globals.regionDataNameColumn]) {
                cumulativeBeds = Number(globals.regionData[i][globals.regionDataBedsColumn]);
                break;
            }
        }
    } else if (globals.queriedRegionNames.length != 0) {
        for (i = 0; i < globals.queriedRegionNames.length; i++) {
            var regionName = globals.queriedRegionNames[i] + "";

            for (var i = 0; i < globals.regionData.length; i++) {
                if (regionName == globals.regionData[i][globals.regionDataNameColumn]) {
                    cumulativeBeds = cumulativeBeds + Number(globals.regionData[i][globals.regionDataBedsColumn]);
                    break;
                }
            }
        }
    } else {
        for (var i = 0; i < globals.regionData.length; i++) {
            cumulativeBeds = cumulativeBeds + Number(globals.regionData[i][globals.regionDataBedsColumn]);
        }
    }
    return cumulativeBeds;
}

function applyCapacitySliderOnScenarioData(currentData) {
    var percentDemand = globals.minHospitalCapacity / 100;

    var cumulativeBeds = getCumulativeBeds();

    for (var i = 0; i < currentData.length; i++) {

        var med_proj_dem = Number(((percentDemand * cumulativeBeds) + Number(currentData[i]["Max Occupied Beds"])) * 100 / cumulativeBeds).toFixed(2);
        var lb_proj_dem = Number(((percentDemand * cumulativeBeds) + Number(currentData[i]["Lower Max Occupied Beds"])) * 100 / cumulativeBeds).toFixed(2);
        var ub_proj_dem = Number(((percentDemand * cumulativeBeds) + Number(currentData[i]["Upper Max Occupied Beds"])) * 100 / cumulativeBeds).toFixed(2);

        currentData[i]["Lower Projected Demand Bound"] = lb_proj_dem;
        currentData[i]["Upper Projected Demand Bound"] = ub_proj_dem;
        currentData[i]["Total Projected Demand (%)"] = med_proj_dem;
        currentData[i]["Projected Demand (%)"] = med_proj_dem;

        currentData[i]["Total Projected Demand (Range)"] = med_proj_dem + "% [" + lb_proj_dem + "% - " + ub_proj_dem + "%]";
    }
    return currentData;
}

function applyDurationSliderOnScenarioData(scenariosDirectory, currentData) {

    var dailyData = {};
    // Condition to display selected region data.
    if (globals.selectedRegionNum != 0) {
        var regionFile = scenariosDirectory + "/regions/nssac_ncov_ro_summary_region_" + globals.selectedRegionNum + "-daily.csv";
        dailyData = getJSONData(regionFile);
    } else if (globals.queriedRegionNames.length != 0) {
        dailyData = mergeDailyDataAcrossRegions(scenariosDirectory);
    }

    var cumulativeBeds = getCumulativeBeds();

    for (var i = 0; i < dailyData.length; i++) {
        dailyData[i]["cumulative"] = Number(dailyData[i]["Total Hospitalizations (Median)"]);
        dailyData[i]["cumulative_lower_bound"] = Number(dailyData[i]["Lower Hospitalization Bound"]);
        dailyData[i]["cumulative_upper_bound"] = Number(dailyData[i]["Upper Hospitalization Bound"]);

        for (j = 1; j < globals.hospitalDuration; j++) {
            var previousDate = Number(i - j);
            if (previousDate < 0) break;

            dailyData[i]["cumulative"] = Number(dailyData[i]["cumulative"]) + Number(dailyData[previousDate]["Total Hospitalizations (Median)"]);
            dailyData[i]["cumulative_lower_bound"] = Number(dailyData[i]["cumulative_lower_bound"]) + Number(dailyData[previousDate]["Lower Hospitalization Bound"]);
            dailyData[i]["cumulative_upper_bound"] = Number(dailyData[i]["cumulative_upper_bound"]) + Number(dailyData[previousDate]["Upper Hospitalization Bound"]);
        }
    }

    var percentDemand = Number(globals.minHospitalCapacity / 100).toFixed(2);

    for (var i = 0; i < globals.timelineJsonData.length; i++) {
        var currentDate = globals.timelineJsonData[i]["date"];

        //var index = dailyData.findIndex(obj => obj.date == currentDate);

        for (var index = 0; index < dailyData.length; index++) {
            if (dailyData[index].date == currentDate) {
                break;
            }
        }

        var maxCapacity = 0;
        var maxLowerCapacity = 0;
        var maxUpperCapacity = 0;

        for (var j = 0; j < 7; j++) {
            var cumulative = Number(dailyData[index - j]["cumulative"]);

            if (cumulative > maxCapacity) {
                maxCapacity = Number(cumulative);
                maxLowerCapacity = Number(dailyData[index - j]["cumulative_lower_bound"]);
                maxUpperCapacity = Number(dailyData[index - j]["cumulative_upper_bound"]);
            }
        }

        var totalProjectedDemand = 100 * ((Number(percentDemand) * cumulativeBeds) + maxCapacity) / cumulativeBeds;
        var lowerProjectedDemand = 100 * ((Number(percentDemand) * cumulativeBeds) + maxLowerCapacity) / cumulativeBeds;
        var upperProjectedDemand = 100 * ((Number(percentDemand) * cumulativeBeds) + maxUpperCapacity) / cumulativeBeds;

        currentData[i]["Total Projected Demand (%)"] = Number(totalProjectedDemand).toFixed(2);
        currentData[i]["Lower Projected Demand Bound"] = Number(lowerProjectedDemand).toFixed(2);
        currentData[i]["Upper Projected Demand Bound"] = Number(upperProjectedDemand).toFixed(2);

        currentData[i]["Max Occupied Beds"] = maxCapacity;
        currentData[i]["Lower Max Occupied Beds"] = maxLowerCapacity;
        currentData[i]["Upper Max Occupied Beds"] = maxUpperCapacity;

        currentData[i]["Total Projected Demand (Range)"] = Number(totalProjectedDemand).toFixed(2) +
            "% [" + Number(lowerProjectedDemand).toFixed(2) + "% - " + Number(upperProjectedDemand).toFixed(2) + "%]";
    }
    return currentData;
}

// Query Search auto suggestion
function querySearchAutocomplete() {
    $(function() {
        var arrayOfTotalRegions = [];
        var regionData = globals.regionData;
        for (var i = 0; i < globals.regionData.length; i++) {
            var HRRCITY = 'HRRCITY'
            if (regionData[i].hasOwnProperty(HRRCITY)) {
                arrayOfTotalRegions.push(globals.regionData[i]["HRRCITY"]);
            } else {
                arrayOfTotalRegions.push(globals.regionData[i]["#VHASS_Region"]);
            }
        }

        function split(val) {
            return val.split(/,\s*/);
        }

        function extractLast(term) {
            return split(term).pop();
        }
        $("#queryByName").autocomplete({
            source: function(request, response) {
                var filteredRegionData = arrayOfTotalRegions;
                var term = request.term;
                var selectedRegionData = term.split(',');
                for (var i = 0; i < selectedRegionData.length; i++) {
                    selectedRegionData[i] = selectedRegionData[i].trim()
                }

                //filteredRegionData = filteredRegionData.filter(val => !selectedRegionData.includes(val));

                filteredRegionData = filteredRegionData.filter(function(val) {
                    return !selectedRegionData.includes(val);
                });

                response($.ui.autocomplete.filter(
                    filteredRegionData, extractLast(request.term)));
            },
            select: function(event, ui) {

                var terms = split(this.value);
                terms.pop();
                terms.push(ui.item.value);
                this.value = terms.join(", ");
                return false;
            },
            focus: function() {
                return false;
            }
        });
    });
}


function bindMenuEvents() {
    $('.moreOptionDropDown').off().on("click", function(e) {
        e.stopPropagation();
        $('#optionMenu').removeClass('displayNone');
        $('#optionMenu').toggle();
    });

    $('.hamburgerIcon').click(function(e) {
        e.stopPropagation();
        $('.optionMenu').toggle();
    });

    $(document).click(function() {
        if (this.id != 'optionMenu') {
            $(".optionMenu").hide();
        }
    });
}

function bindChartAndDataTab() {
    $('.charts').on('click', function(e) {
        $('.data').removeClass('selectedFilter');
        $('.charts').addClass('selectedFilter');
        $('#dataTable').parent().addClass('d-none');
        $('.charContainerHeight').show();
        if (globals.mobileDevice() || (isTablet && !isLandscape)) {
            $('.map').removeClass('selectedFilter');
            $('#mapContainerRow').addClass('invisibleHeight0');
            $('.projectionsRow').addClass('invisibleHeight0');
            $('.foot-note-chart').removeClass('d-none');

            if ($('#allToggleButton')[0].checked) {
                if (globals.selectedRegionNum != 0) {
                    renderSelectedRegionsChart(globals.selectedRegionNum, globals.selectedRegionName);
                } else if (globals.queriedRegionNames.length != 0) {
                    renderQueriedRegionsChart();
                } else {
                    renderSummaryDataChart();
                }
            } else {
                renderAllScenarios();
            }
        }
        $('#chartDataTableContainerRow').css('height', '100%');
        $('#chartdiv').parent().removeClass('invisibleHeight0');
        $('#allToggleButton').parent().removeClass('d-none');
        $('#scenariosDropdown').parent().removeClass('d-none');
    });

    $('.data').on('click', function(e) {
        $('.charts').removeClass('selectedFilter');
        $('.data').addClass('selectedFilter');
        $('#chartdiv').parent().addClass('invisibleHeight0');
        if (globals.mobileDevice() || (isTablet && !isLandscape)) {
            $('.charContainerHeight').hide();
            $('.map').removeClass('selectedFilter');
            $('#mapContainerRow').addClass('invisibleHeight0');
            $('.projectionsRow').addClass('invisibleHeight0');
            $('.foot-note-chart').removeClass('d-none');
        }
        $('.charContainerHeight').hide();
        $('#dataTable').parent().removeClass('d-none');
        $('#allToggleButton').parent().addClass('d-none');
        $('#scenariosDropdown').parent().addClass('d-none');
        $('#chartDataTableContainerRow').css('height', '100%');
        $($.fn.dataTable.tables(true)).DataTable().columns.adjust();
    });

    $('.map').on('click', function(e) {
        $('.charts').removeClass('selectedFilter');
        $('.data').removeClass('selectedFilter');
        $('.tabMenu .map').addClass('selectedFilter');
        $('#chartDataTableContainerRow').css('height', 'auto');
        $('#chartdiv').parent().addClass('invisibleHeight0');
        $('#dataTable').parent().addClass('d-none');
        $('#mapContainerRow').removeClass('invisibleHeight0');
        $('.projectionsRow').removeClass('invisibleHeight0');

        if (globals.mobileDevice() || (isTablet && !isLandscape)) {
            $('.charContainerHeight').hide();
            $('#allToggleButton').parent().addClass('d-none');
            $('#scenariosDropdown').parent().addClass('d-none');
            $('.foot-note-chart').addClass('d-none');
        }
    });
}

function bindSliderEvents() {
    globals.rangeSlider = document.getElementById('slider-range');

    noUiSlider.create(globals.rangeSlider, {
        start: [80, 120],
        step: 1,
        tooltips: true,
        format: wNumb({
            decimals: 0
        }),
        range: {
            'min': [40],
            'max': [170]
        },
        connect: true
    });

    globals.rangeSlider.noUiSlider.on('update', function(values, handle) {
        globals.minHospitalCapacity = values[0];
        globals.maxHospitalCapacity = values[1];
    });

    // HOSPITAL DURATION SLIDER
    globals.durationSlider = document.getElementById('duration-slider');

    noUiSlider.create(globals.durationSlider, {
        start: 7,
        step: 1,
        tooltips: true,
        animate: false,
        format: wNumb({
            decimals: 0
        }),
        range: {
            min: 1,
            max: 14
        }
    });

    globals.durationSlider.noUiSlider.on('update', function(values, handle) {
        globals.hospitalDuration = values[handle];
    });
}

function loadRegionData() {
    if (globals.configuration.region == 'vhass') {
        globals.regionDataNameColumn = "#VHASS_Region";
        globals.regionDataBedsColumn = "Beds";
    } else {
        globals.regionDataNameColumn = "HRRCITY";
        globals.regionDataBedsColumn = "DHS_Beds";
    }

    var fileURL = globals.configuration.regionFile;

    $.ajax({
        url: fileURL,
        async: false,
        success: function(csv) {
            var items = $.csv.toObjects(csv);
            var jsonobject = JSON.stringify(items);
            globals.regionData = JSON.parse(jsonobject);
            //To get auto-suggestion for QuerySearch, Region data must be loaded (git 67)
            querySearchAutocomplete();
        },
        dataType: "text",
        complete: function() {

        }
    });
}

$('#allToggleButton').on('change', function(e) {
    if (this.checked) {
        $(".scenarioDropdown").hide();
        if (globals.selectedRegionNum != 0) {
            renderSelectedRegionsChart(globals.selectedRegionNum, globals.selectedRegionName);
        } else if (globals.queriedRegionNames.length != 0) {
            renderQueriedRegionsChart();
        } else {
            renderSummaryDataChart();
        }
    } else {
        $(".scenarioDropdown").show();
        renderAllScenarios();
    }
});

//Csv object data read function
function processData(data) {
    var csvRows = [];
    var headers = Object.keys(data[0]);
    csvRows.push(headers.join(","));

    for (var i = 0; i < data.length; i++) {
        var row = data[i];

        var values = headers.map(function(header) {
            var escaped = ('' + row[header.replace(/"/g, '\\"')]);
            return escaped;
        });

        // ES6 version
        // var values = headers.map(header => {
        //     var escaped = ('' + row[header.replace(/"/g, '\\"')]);
        //     return escaped;
        // });
        csvRows.push(values.join(','));
    }
    return csvRows.join('\n');
}


// Download  all functionality 
function downloadAll() {
    var zip = new JSZip();
    var filesObject = [];

    //Iterate scenarios list and get summary file
    $.each(globals.scenarios, function(key, val1) {

        var summaryFile = val1.directory + "/duration" + globals.hospitalDuration + "/nssac_ncov_ro-summary.csv";
        var rawData = getJSONData(summaryFile);
        // Iterate directory and get date wise file list
        $.each(rawData, function(key, val) {
            for (var i = 1; i <= globals.hospitalDuration; i++) {
                var rFile = val1.directory + "/duration" + i + "/nssac_ncov_ro_" + val.date + ".csv";
                filesObject.push(rFile);
            }
        });

    });


    for (var i = 0; i < filesObject.length; i++) {
        var content = getJSONData(filesObject[i]);
        //Function for read conetnt of csv data 
        var csvFileData = processData(content);
        var splitFilePath = filesObject[i].split("/");
        splitFilePath = splitFilePath[1] + "/" + splitFilePath[2] + "/" + splitFilePath[3];
        // Add csv file and csv data
        zip.file(splitFilePath, csvFileData);
    }
    //Genarate zip file 
    zip.generateAsync({ type: "blob" })
        .then(function(content) {
            saveAs(content, "All-Scenarios.zip");
        });
}