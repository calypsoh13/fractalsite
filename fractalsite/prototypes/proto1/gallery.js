$(document).ready(function () {
    images = 
        ["../plasma.png", 
         "../gauss1025sig1.png",
         "../aaa.png", 
         "../bbb.png",
         "../ccc.png", 
         "../ddd.png",
         "../eee.png",
         "../fff.png"];
    $("#images").val(JSON.stringify(images));
    
    var img = new Image();
    img.onload = function() {
        $("#imageSize").text(this.width + " x " + this.height);
    };
    
    img.src = images[0];
    
    setImages(0);
    
    $("#thumbp3").click( function() {
        setImages(-3);
    });    
    $("#thumbp2").click( function() {
        setImages(-2);
    });    
    $("#thumbp1").click( function() {
        setImages(-1);
    });    
    $("#thumbn3").click( function() {
        setImages(3);
    });    
    $("#thumbn2").click( function() {
        setImages(2);
    });    
    $("#thumbn1").click( function() {
        setImages(1);
    });
});

function setImages(increment){
    images = JSON.parse($("#images").val());
    len = images.length;
    current = parseInt($("#currentImage").val());
    current = cycleValue(current + increment, len);
    $("#currentImage").val(current);
    
    if (len < 7)
    {   
        $("#thumbn3").hide();
        $("#thumbp3").hide();
    }
    else
    {
        $("#thumbn3").show();
        $("#thumbp3").show();
        n = cycleValue(current + 3, len);
        p = cycleValue(current - 3, len);
        $("#thumbn3").prop("src", images[n]);
        $("#thumbp3").prop("src", images[p]);
    }
    if (len < 5)
    {   
        $("#thumbn2").hide();
        $("#thumbp2").hide();
    }
    else
    {
        $("#thumbn2").show();
        $("#thumbp2").show();
        n = cycleValue(current + 2, len);
        p = cycleValue(current - 2, len);
        $("#thumbn2").prop("src", images[n]);
        $("#thumbp2").prop("src", images[p]);
    }
    if (len < 3)
    {   
        $("#thumbn1").hide();
        $("#thumbp1").hide();
    }
    else
    {
        $("#thumbn1").show();
        $("#thumbp1").show();
        n = cycleValue(current + 1, len);
        p = cycleValue(current - 1, len);
        $("#thumbn1").prop("src", images[n]);
        $("#thumbp1").prop("src", images[p]);
    }
    if (len > 0)
    {
        $("#fullImage").prop("src", images[current]);
        width = $("#fullImage").prop("naturalWidth");
        height = $("#fullImage").prop("naturalHeight");
        $("#imageSize").text(width + " x " + height);
    }
    else
    {
        // show no image message
    }
}

function cycleValue(value, length)
{
    result = value;
    while (result < 0)
    {
        result += length;
    }
    while (result >= length)
    {
        result -= length;
    }
    return result;
}


