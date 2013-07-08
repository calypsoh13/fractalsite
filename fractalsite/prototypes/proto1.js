$(document).ready(function () {
    sizesetting = parseInt($("#size").val());
    size = Math.pow(2, sizesetting) + 1;
    $("#sizeout").text(size);
    $("#roughnessout").text(parseInt($("#roughness").val()) / 10);
    $("#perturbanceout").text(parseInt($("#perturbance").val()) / 10);
    gx = parseInt($("#gaussX").val());
    gxAdjust = (size-1)/128 * gx + 128;
    $("#gaussXout").val(gxAdjust);
    gy = parseInt($("#gaussY").val());
    gyAdjust = (size-1)/128 * gy + 128;
    $("#gaussYout").val(gyAdjust);
    gsx = parseInt($("#gaussSigmaX").val());
    $("#gaussSigmaXout").text(Math.pow(2, gsx/2));
    gsy = parseInt($("#gaussSigmaY").val());
    $("#gaussSigmaYout").text(Math.pow(2, gsy/2));
     
    $("#size").change(function () {
        $("#sizeout").text(Math.pow(2, parseInt($(this).val())) + 1);
        setGaussXout();
        setGaussYout();
        previewSizeAndPosition();
    });
    $("#roughness").change(function () {
        $("#roughnessout").text(parseInt($(this).val()) / 10);
    });
    $("#perturbance").change(function () {
        $("#perturbanceout").text(parseInt($(this).val()) / 10);
    });
    $("#gaussX").change(function() {
        setGaussXout();
        previewSizeAndPosition();
    });
    $("#gaussY").change(function() {
        setGaussYout();
        previewSizeAndPosition();
    });
    $("#gaussSigmaX").change(function() {
        gsx = parseInt($(this).val());
        gsxAdjust = Math.floor(Math.pow(2, gsx/2) * 100) / 100;
        $("#gaussSigmaXout").text(gsxAdjust);
        previewSizeAndPosition();
    });
    $("#gaussSigmaY").change(function() {
        gsy = parseInt($(this).val());
        gsyAdjust = Math.floor(Math.pow(2, gsy/2) * 100) / 100;
        $("#gaussSigmaYout").text(gsyAdjust);
        previewSizeAndPosition();
    });
    $("#gaussXout").change(function() {
        gxOut = parseInt($(this).val());
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
        previewSizeAndPosition();
    });
    $("#gaussYout").change(function() {
        gyOut = parseInt($(this).val());
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
        previewSizeAndPosition();
    });
});

function setGaussXout() {
    gxSetting = parseInt($("#gaussX").val());
    size = parseInt($("#sizeout").text());
    // alert(gxSetting + " " + size);
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