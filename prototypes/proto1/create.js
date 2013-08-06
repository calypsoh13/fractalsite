$(document).ready(function () {
    
    // fractal initialization
    sizesetting = parseInt($("#size").val());
    size = Math.pow(2, sizesetting) + 1;
    $("#sizeout").text(size);
    $("#roughnessout").text(parseInt($("#roughness").val()) / 10);
    $("#perturbanceout").text(parseInt($("#perturbance").val()) / 10);
    
    // gaussian initialization
    initializeGaussPoint();
    setGaussVisibility();
     
    // color initialization
    initSpectrumInput($('#color1'));
    initSpectrumInput($('#color2'));
    initSpectrumInput($('#color3'));
    initSpectrumInput($('#color4'));
    initSpectrumInput($('#color5'));

    setColorTypeVisibility();
    setGradStopVisibility();
    updateGradient();
    
    // fractal events
    $("#size").change(function () {
        newsize = Math.pow(2, parseInt($(this).val())) + 1;
        $("#sizeout").text(newsize);
        setGaussXout();
        setGaussYout();
        previewSizeAndPosition();
        adjustSavedGaussForSize(newsize);
    });
    $("#roughness").change(function () {
        $("#roughnessout").text(parseInt($(this).val()) / 10);
    });
    $("#perturbance").change(function () {
        $("#perturbanceout").text(parseInt($(this).val()) / 10);
    });
    
    $("#createFractal").click(function() {
        size = $("#sizeout").text();
        roughness = $("#roughnessout").text();
        perturbance = $("#perturbanceout").text();
        alert ("Server, please create a matrix of size " + size + " with roughness " +
        roughness + " and perturbance " + perturbance + ". Thanks!");
    });
    
    // gaussian events
    $("#filterPlus").click(function() {
        numberPoints = parseInt($("#gaussNumberPoints").val());
        if (numberPoints > 0)
        {
            saveGauss();
        }
        numberPoints += 1;
        $("#gaussNumberPoints").val(numberPoints);
        $("#gaussCurrentPoint").val(numberPoints);
        setGaussVisibility();
        initializeGaussPoint();
        saveGauss();
        updateGaussLabels();
        previewSizeAndPosition();
    });
    
    $("#filterMinus").click(function() {
        numberPoints = parseInt($("#gaussNumberPoints").val());
        currentPoint = parseInt($("#gaussCurrentPoint").val());
        cp = currentPoint;
        if (cp === 1)
        {
            $("#gauss1").val($("#gauss2").val());
            cp = 2;
        }
        if (cp === 2)
        {
            $("#gauss2").val($("#gauss3").val());
            cp = 3;
        }
        if (cp === 3)
        {
            $("#gauss3").val($("#gauss4").val());
            cp = 4;
        }
        if (cp == 4)
        {
            $("#gauss4").val($("#gauss5").val());
            cp = 5;
        }
        $("#gauss5").val("");
        numberPoints = numberPoints - 1;
        if (currentPoint > numberPoints) currentPoint = numberPoints;
        $("#gaussNumberPoints").val(numberPoints);
        $("#gaussCurrentPoint").val(numberPoints);
        setGaussVisibility();
        if (numberPoints > 0)
        {
            loadGauss();
            updateGaussLabels();
            previewSizeAndPosition();
        }
    });
    
    $("#filterNext").click(function() {
        numberPoints = parseInt($("#gaussNumberPoints").val());
        currentPoint = parseInt($("#gaussCurrentPoint").val());
        saveGauss();
        currentPoint += 1;
        if (currentPoint > numberPoints)
        {
            currentPoint = 1;
        }
        $("#gaussCurrentPoint").val(currentPoint);
        loadGauss();
        updateGaussLabels();
        previewSizeAndPosition();
    });
    
    $("#filterPrevious").click(function() {
        numberPoints = parseInt($("#gaussNumberPoints").val());
        currentPoint = parseInt($("#gaussCurrentPoint").val());
        saveGauss();
        currentPoint -= 1;
        if (currentPoint < 1)
        {
            currentPoint = numberPoints;
        }
        $("#gaussCurrentPoint").val(currentPoint);
        loadGauss();
        updateGaussLabels();
        previewSizeAndPosition();
    });
    
    $("#gaussX").change(function() {
        setGaussXout();
        previewSizeAndPosition();
        saveGauss();
    });
    $("#gaussY").change(function() {
        setGaussYout();
        previewSizeAndPosition();
        saveGauss();
    });
    $("#gaussSigmaX").change(function() {
        gsx = parseInt($(this).val());
        gsxAdjust = Math.floor(Math.pow(2, gsx/2) * 100) / 100;
        $("#gaussSigmaXout").text(gsxAdjust);
        previewSizeAndPosition();
        saveGauss();
    });
    $("#gaussSigmaY").change(function() {
        gsy = parseInt($(this).val());
        gsyAdjust = Math.floor(Math.pow(2, gsy/2) * 100) / 100;
        $("#gaussSigmaYout").text(gsyAdjust);
        previewSizeAndPosition();
        saveGauss();
    });
    $("#gaussXout").change(function() {
        setGaussX();
        previewSizeAndPosition();
        saveGauss();
    });
    $("#gaussYout").change(function() {
        setGaussY();
        previewSizeAndPosition();
        saveGauss();
    });

    // color events
    $(".colorType").change(function() {
        updateGradient();
    });
    $(".colorStop").change(function() {
        updateGradient();
    });
    
    $("#useGradient").change(function() {
        setColorTypeVisibility();
        setGradStopVisibility();
        updateGradient();
    });
    
    $("#useHeat").change(function() {
        setColorTypeVisibility();
    });
    
    $(".useStop").click(function() { 
        var id = $(this).attr("id");
        if (!$(this).is(":checked"))
        {
            if (id === "useStop3")
            {
                $("#colorStopLoc3").val($("#colorStopLoc4").val());
                $("#color3").spectrum("set", $("#color4").spectrum("get"));
                if ($("#useStop4").is(":checked"))
                {
                    $("#useStop4").prop("checked", false);
                    $("#useStop3").prop("checked", true);
                    id = "useStop4";
                }
            }
            if (id === "useStop4")
            {
                $("#colorStopLoc4").val($("#colorStopLoc5").val());
                $("#color4").spectrum("set", $("#color5").spectrum("get"));
                $('#colorStopLoc5').val(127);
                $('#color5').spectrum("set", "#777777");
                if ($("#useStop5").is(":checked"))
                {
                    $("#useStop5").prop("checked", false);
                    $("#useStop4").prop("checked", true);
                }
            }
        }
        setGradStopVisibility();
        updateGradient();
    }); 
});

// gaussian methods

function initializeGaussPoint() {
    // gaussian initialization
    size = parseInt($("#sizeout").text());
    mid = (size-1)/2;
    $("#gaussX").val(0);
    $("#gaussXout").val(mid);
    $("#gaussY").val(0);
    $("#gaussYout").val(mid);
    $("#gaussSigmaX").val(0);
    $("#gaussSigmaXout").text(1);
    $("#gaussSigmaY").val(0);
    $("#gaussSigmaYout").text(1);
}

function setGaussVisibility() {
    numPoints = parseInt($("#gaussNumberPoints").val());
    if (numPoints > 0)
    {
        $(".gaussInputs").show();
        $("#filterMinus").show();
    }
    else
    {
        $(".gaussInputs").hide();
        $("#filterMinus").hide();
    }
    if (numPoints > 1)
    {
        $("#filterNext").show();
        $("#filterPrevious").show();
    }
    else
    {
        $("#filterNext").hide();
        $("#filterPrevious").hide();
    }
    
    $("#filterPlus").prop("disabled", numPoints > 4);
}

function saveGauss() {
    var point = {};
    point.size = $("#sizeout").text();
    point.x = $("#gaussXout").val();
    point.y = $("#gaussYout").val();
    point.sigX = $("#gaussSigmaXout").text();
    point.sigY = $("#gaussSigmaYout").text();
    point.sigXsetting = $("#gaussSigmaX").val();
    point.sigYsetting = $("#gaussSigmaY").val();
    pointNumber = $("#gaussCurrentPoint").val();
    saveItem = $("#gauss" + pointNumber);
    savePoint = JSON.stringify(point);
    $(saveItem).val(savePoint);
}

function loadGauss() {
    pointNumber = $("#gaussCurrentPoint").val();
    getItem = $("#gauss" + pointNumber);
    getPoint = $(getItem).val();
    point = JSON.parse(getPoint);
    $("#gaussXout").val(point.x);
    setGaussX();
    $("#gaussYout").val(point.y);
    setGaussY();
    $("#gaussSigmaX").val(point.sigXsetting);
    $("#gaussSigmaY").val(point.sigYsetting);
    $("#gaussSigmaXout").text(point.sigX);
    $("#gaussSigmaYout").text(point.sigY);
    previewSizeAndPosition();
}

function setGaussXout() {
    gxSetting = parseInt($("#gaussX").val());
    size = parseInt($("#sizeout").text());
    increment = (size-1)/128;
    offset = increment * 64;
    gx = increment * gxSetting + offset;
    $("#gaussXout").val(gx);
}

function setGaussYout() {
    gySetting = parseInt($("#gaussY").val());
    size = parseInt($("#sizeout").text());
    increment = (size-1)/128;
    offset = increment * 64;
    gy = increment * gySetting + offset;
    $("#gaussYout").val(gy);
}

function setGaussX() {
    gxOut = parseInt($("#gaussXout").val());
    size = parseInt($("#sizeout").text());
    increment = (size-1)/128;
    offset = 64 * increment
    gxSetting = (gxOut - offset) / increment;
    sign = 1;
    if (gxSetting < 0) sign = -1;
    gxSetting = Math.floor(Math.abs(gxSetting)) *  sign;
    // limit the setting to -80 to 80
    if (gxSetting < -80 || gxSetting > 80)
    {
        gxSetting = Math.max(-80, Math.min(80, gxSetting));
        gxOut = increment * gxSetting + offset;
    }
    $("#gaussXout").val(gxOut);
    $("#gaussX").val(gxSetting);
}

function setGaussY() {
    gyOut = parseInt($("#gaussYout").val());
    size = parseInt($("#sizeout").text());
    increment = (size-1)/128;
    offset = 64 * increment;
    gySetting = (gyOut - offset) / increment;
    sign = 1;
    if (gySetting < 0) sign = -1;
    gySetting = Math.floor(Math.abs(gySetting)) *  sign;
    // limit the setting to -80 to 80
    if (gySetting < -80 || gySetting > 80)
    {
        gySetting = Math.max(-80, Math.min(80, gySetting));
        gyOut = increment * gySetting + offset;
    }
    $("#gaussYout").val(gyOut);
    $("#gaussY").val(gySetting);
}

function previewSizeAndPosition() {
    size = parseInt($("#sizeout").text());
    gsx = parseFloat($("#gaussSigmaXout").text());
    gsy = parseFloat($("#gaussSigmaYout").text());
    xSize = Math.floor(129 * gsx);
    ySize = Math.floor(129 * gsy);
    $("#gaussPreview").css("background-size", xSize + "px " + ySize + "px"); 
    gx = parseInt($("#gaussXout").val());
    gy = parseInt($("#gaussYout").val());
    tempx = 2 * (gx-1)/(size -1);
    tempy = 2 * (gy-1)/(size -1);
    locX = (tempx - gsx) * 65;
    locY = (tempy - gsy) * 65;
    $("#gaussPreview").css("background-position-x", locX);
    $("#gaussPreview").css("background-position-y", locY);
}

function adjustSavedGaussForSize(newSize) {
    numberPoints = parseInt($("#gaussNumberPoints").val());
    for (var i = 1; i <= numberPoints; i++)
    {
        pointNumber = i;
        item = $("#gauss" + pointNumber);
        getPoint = $(item).val();
        point = JSON.parse(getPoint);
        point.x = point.x/(point.size-1) * (newSize -1);
        point.y = point.y/(point.size -1) * (newSize -1);
        point.size = newsize;
        setPoint = JSON.stringify(point);
        $(item).val(setPoint);
    }
}

function updateGaussLabels() {
    currentPoint = parseInt($("#gaussCurrentPoint").val());
    $("#xLabel").text("X"+currentPoint);
    $("#yLabel").text("Y"+currentPoint);
    $("#sigmaXLabel").text("sigma X"+currentPoint);
    $("#sigmaYLabel").text("sigma Y" + currentPoint);
}

// color methods
function setGradStopVisibility() {
    if ($("#useStop4").is(":checked"))
    {
        $("#colorRow5").show();
    }
    else
    {   
        $("#colorRow5").hide();
    }
    
    if ($("#useStop3").is(":checked"))
    {
        $("#colorRow4").show();
    }
    else
    {
        $("#colorRow4").hide();
    }
}

function initSpectrumInput(item) {
    var color = "#777777";
    if ($(item).attr("id") === "color1") 
    {
        color = "#000000";
    }
    if ($(item).attr("id") === "color2") 
    {
        color = "#ffffff";
    }
    $(item).spectrum({
        color: color,
        className: 'spectrum',
        showAlpha:true,
        showInitial:true,
        showInput:true,
        showPalette: true,
        palette: [
            ['red', 'green', 'blue'], 
            ['#ffff00', '#00ffff', '#ff00ff'],
            ['black', '#777777', 'white']
        ],
        change: function(c) {
            updateGradient();
            }
    });
}

function setColorTypeVisibility() {
    if ($("#useHeat").is(":checked"))
    {
        $(".gradientInputs").hide();
        $(".heatInputs").show();
    }
    else
    {
        $(".gradientInputs").show();
        $(".heatInputs").hide();
    }
}

function updateGradient() {
    var gradElement = document.getElementById("gradientPreview");
    var color1 = $("#color1").spectrum("get").toRgbString();
    var color2 = $("#color2").spectrum("get").toRgbString();
    var color3 = $("#color3").spectrum("get").toRgbString();
    var color4 = $("#color4").spectrum("get").toRgbString();
    var color5 = $("#color5").spectrum("get").toRgbString();
    var stop1 = Math.round($("#colorStopLoc1").val()/ 2.55)/100;
    var stop2 = Math.round($("#colorStopLoc2").val()/ 2.55)/100;
    var stop3 = Math.round($("#colorStopLoc3").val()/ 2.55)/100;
    var stop4 = Math.round($("#colorStopLoc4").val()/ 2.55)/100;
    var stop5 = Math.round($("#colorStopLoc5").val()/ 2.55)/100;
    
    var bgi = "background-image: "
    var lingrad = "linear-gradient(left, "
    var end = ");\n";
    var cs = " color-stop("

    var stopA = color1 + " " + stop1*100 + "%, " + color2 + " " + stop2*100 + "%";
    var stopB = cs + stop1 + ", " + color1 + "), " + cs + stop2 + ", " + color2 + ")";
    if ($("#useStop3").is(":checked"))
    {
        stopA = stopA + ", " + color3 + " " + stop3*100 + "%";
        stopB = stopB + ", " + cs + stop3 + ", " + color3 + ")";
        if ($("#useStop4").is(":checked"))
        {
            stopA = stopA + ", " + color4 + " " + stop4*100 + "%";
            stopB = stopB + ", " + cs + stop4 + ", " + color4 + ")";
            if ($("#useStop5").is(":checked"))
            {
                stopA = stopA + ", " + color5 + " " + stop5*100 + "%";
                stopB = stopB + ", " + cs + stop5 + ", " + color5 + ")";
            }
        }
    }

    gradElement.style.background=lingrad + stopA  + ")";
    gradElement.style.background="-o-" + lingrad + stopA +")";
    gradElement.style.background="-moz-" + lingrad + stopA +")";
    gradElement.style.background="-webkit-" + lingrad + stopA +")";
    gradElement.style.background="-ms-" + lingrad + stopA +")";
    gradElement.style.background="-webkit-gradient(linear, left top, right top," + stopB + ")";
}