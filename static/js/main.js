var current_page = 1;
var selected_roof = 0;
var page2_override = true;

function hide(el){
    el.attr("hidden", "");
}

function show(el){
    el.removeAttr("hidden");
}

function show_error(msg){
    show($("#error-msg-container"));
    $("#error-msg-contents").text(msg);
}

function hide_error(){
    hide($("#error-msg-container"));
}

function resize_error_msg(){
    var win_w = $(window).width();
    var win_h = $(window).height();
    $("#error-msg").css("margin-left", Math.min(win_w, (win_w / 2) - 150));
    $("#error-msg").css("margin-top", Math.min(win_h, (win_h / 2) - 125));
}

function generate_roof_output(area){
    var watt_per_sqm = 175;
    var output = 0;
    if(selected_roof == 1){
        output = area * watt_per_sqm * 0.6;
    } else if(selected_roof == 2){
        output = area * watt_per_sqm * 0.4;
    } else if(selected_roof == 3){
        output = area * watt_per_sqm;
    } else if(selected_roof == 4){
        output = area *  watt_per_sqm * 0.65;
    }
    return output;
}

function generate_results(){
    var lat = place.geometry.location.lat();
    var lng = place.geometry.location.lng();
    $.ajax("/get_area?lat=" + lat + "&lng=" + lng).done(function(resp){

        $("#area").text(generate_roof_output(parseFloat(resp)));
    });
}

$(document).ready(function(){
    //var roofsel = $("#roof-selector");
    //$("#windowwidth").text($(window).width());
    resize_error_msg();
    $("#search-ok").click(function(){
        if(place == ""){
            show_error("Please select a location.");
        } else {
            hide($("#search"));
            show($("#roof-selector"));
            current_page = 2;
        }
    });
    $("#roof-ok").click(function(){
       if(place == "" && !page2_override){
           show_error("Please select a location");
       } else {
           if(selected_roof == 0 && !page2_override){
               show_error("Please select a roof");
           } else {
               hide($("#roof-selector"));
               show($("#results-page"));
               current_page = 3;
               generate_results();
           }
       }
    });

    $("#error-ok").click(function(){
        hide_error();
    })

    $("#nav-1").click(function(){
        if(current_page != 1){

            if(current_page == 2){
                hide($("#roof-selector"));
                show($("#search"));
                current_page = 1;
            } else if (current_page == 3){
                hide($("#results-page"));
                show($("#search"));
                current_page = 1;
            }  else if (current_page == 4){
                hide($("#heritage-page-page"));
                show($("#search"));
                current_page = 1;
            }
        }
    });
    $("#nav-2").click(function(){
        if(current_page == 1) {
            if (place == "" && !page2_override) {
                show_error("Please select a location.");
            } else {
                hide($("#search"));
                show($("#roof-selector"));
                current_page = 2;
            }
        } else if(current_page == 3){
            hide($("#results-page"));
            show($("#roof-selector"));
            current_page = 2;
        }else if(current_page == 4){
            hide($("#heritage-page"));
            show($("#roof-selector"));
            current_page = 2;
        }
    });
    $("#nav-3").click(function(){
        if(current_page == 1) {
            if (place == "") {
                show_error("Please select a location.");
            } else {
                if(selected_roof == 0){
                    show_error("Please select a roof type (page 2)");
                } else {
                    hide($("#search"));
                    show($("#results-page"));
                    current_page = 3;
                    generate_results();
                }
            }
        } else if(current_page == 2){
             if (place == "") {
                 show_error("Please select a location.");
             }else {
                 if(selected_roof == 0){
                     show_error("Please select a roof type (page 2)");
                    }
                 else {
                    hide($("#roof-selector"));
                    show($("#results-page"));
                    current_page = 3;
                 }
             }
        }else if(current_page == 4){
            hide($("#heritage-page"));
            show($("#results-page"));
            current_page = 3;
        }
    })
    $("#roof-1").click(function(){
        selected_roof = 1;
        $("#roof-1").addClass("selected-roof");
        $("#roof-2").removeClass("selected-roof");
        $("#roof-3").removeClass("selected-roof");
        $("#roof-4").removeClass("selected-roof");
    });
    $("#roof-2").click(function(){
        selected_roof = 2;
         $("#roof-1").removeClass("selected-roof");
        $("#roof-2").addClass("selected-roof");
        $("#roof-3").removeClass("selected-roof");
        $("#roof-4").removeClass("selected-roof");
    });
    $("#roof-3").click(function(){
        selected_roof = 3;
         $("#roof-1").removeClass("selected-roof");
        $("#roof-2").removeClass("selected-roof");
        $("#roof-3").addClass("selected-roof");
        $("#roof-4").removeClass("selected-roof");
    });
    $("#roof-4").click(function(){
        selected_roof = 4;
         $("#roof-1").removeClass("selected-roof");
        $("#roof-2").removeClass("selected-roof");
        $("#roof-3").removeClass("selected-roof");
        $("#roof-4").addClass("selected-roof");
    });
})


$( window ).resize(function() {
  //$( "body" ).prepend( "<div>" + $( window ).width() + "</div>" );
    //console.log($(window).width());
    //$("#windowwidth").text($(window).width());
    resize_error_msg();
});