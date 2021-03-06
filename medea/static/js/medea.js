$(function () {
    
    // Loading controller
    var controller = Raphael.controller(0, 0, 200, "controller");
    
    // object selection and movement
    var medea = {};
    medea.transform = '<transform class="selectable" translation="0 1 0"/>';
    //TODO: put a slide in the UI to control this parameter
    medea.range = 1; // This defines the sensibility of the controller 
    medea.step = 0.785; // Rotation step
    medea.plane = null;
    medea.selected = null;
    medea.select = function () {
        var highlight = '<shape class="highlight"><sphere radius="0.2"/><appearance><material diffuseColor="1 0 0" transparency=".9"/></appearance></shape>';
        
        return function (ev) {
            console.log(ev.target);
            $(".highlight").remove();
            
            if (ev.target === medea.selected) {
                medea.selected = null;
            } else {
                medea.selected = ev.target;
                $(ev.target).append(highlight);
            }
        };
    }();
    medea.remove = function () {
        if (!medea.selected) return;
        
        $(medea.selected).remove();
        $(".highlight").remove();
    }
    
    //TODO: maybe there is a better (and reliable) way to get the object translation
    //      need to investigate x3dom
    medea.getPos = function (coords) {
        var pos = {x: 0, y: 0, z: 0};
        if (coords) {
            var str = coords.split(" ");
            pos.x = parseFloat(str[0]);
            pos.y = parseFloat(str[1]);
            pos.z = parseFloat(str[2]);
        }
        
        return pos;
    }
    medea.getRotation = function (coords) {
        var rotation = {x: 0, y: 0, z: 0, g: 0};
        if (coords) {
            var str = coords.split(" ");
            rotation.x = parseFloat(str[0]);
            rotation.y = parseFloat(str[1]);
            rotation.z = parseFloat(str[2]);
            rotation.g = parseFloat(str[3]);
        }
        
        return rotation;
    }
    medea.moving = function (vu, vv) {
        if (!medea.selected) return;
        
        // Delta
        var pos = medea.getPos($(medea.selected).attr('translation'));
        
        // TODO: i'd like to implement continuos movement while the cursor is grabbed aroud
        //       varying movement speed based on vx and vy
        
        pos[medea.plane[0]] += vu*medea.range;
        pos[medea.plane[1]] += vv*medea.range;            
        $(medea.selected).attr('translation', pos.x +" "+ pos.y +" "+ pos.z);
    }
    medea.rotate = function (clockwise) {
        if (!medea.selected) return;
        
        var r = medea.getRotation($(medea.selected).attr('rotation'));
        r.y = 1;
        
        r.g += clockwise ? -medea.step : medea.step;
        $(medea.selected).attr('rotation', r.x +" "+ r.y +" "+ r.z +" "+ r.g);
    }

    controller.bind(medea.moving);

    
    // On scene loading i need to bind all selectable transform to the select function 
    $("#x3d_element transform.selectable").click(medea.select);
    $("#remove_bt").click(medea.remove);
    
    
    // Drag&drop handling
    //Cambia il cursore sugli elementi trascinabili per renderli visibili
    $(".draggable").css("cursor", "move");

    $(".draggable")
    //Indica al browser quali elementi sono trascinabili, in questo caso attraverso una classe.
    .attr("draggable", "true")
    //Specifica cosa fare quanto un elemento viene trascinato. In questo caso salvo il contenuto tramite
    // innerHtml
    .bind('dragstart', function(ev) {
        var dt = ev.originalEvent.dataTransfer;
        var html = $('<div>').append($(this).find("inline").clone()).remove().html();
        dt.setData("node", html);
        return true;
    });
    
    //Indica al browser l'elemento (per più elementi fare una classe) in cui puoi trascinare gli oggetti.
    $("#drop")
    //Dragenter indica l'evento "entro nel target mentre sto trascinando qualcosa"
    .bind("dragenter", function (ev) {
        //$(this).css("background-color", "white");
        return false;
    })
    //Dragleave indica l'evento "esco dal target mentre sto trascinando qualcosa"
    .bind("dragleave", function (ev) {
        //$(this).css("background-color", "#acd6ec");
        return false;
    })
    //Dragover indica l'evento "sono sul target mentre sto trascinando qualcosa"
    .bind('dragover', function(ev) {
        //$(this).css("cursor", "copy");
        return false;
    })
    //Dragover indica l'evento "deposito l'elemento che ho trascinato nel target".
    .bind("drop", function (ev) {
        //$(this).css("background-color", "#acd6ec");
        //con questa riga ottengo i dati salvati quando ho iniziato a trascinare l'oggetto'
        var tmp = ev.originalEvent.dataTransfer;
        var node = $(medea.transform).append(tmp.getData("node"));
        
        $(this).find("scene").append(node);
        
        //console.log(window.x3dom.runtime.viewpoint());
        //console.log($("#x3d_element").runtime.getActiveBindable('Viewpoint'));

        // Binding click event to selection function
        $(this).find("scene transform.selectable:last").click(medea.select);
        return false;
    });
    
    // Plane selector
    var planeToggle = function (plane) {
        medea.plane = plane.toLowerCase();
        
        console.log("Active plane: "+ medea.plane);
    }
    
    // Handles the radio button for plane selection
    $("#planes").click(function (ev){
        if ($(ev.target).hasClass("checked")) return;
        $("#planes > button").toggleClass("checked");
        
        planeToggle($(ev.target).html());
    });
    
    // Navigation mode
    $("#nav_mode").click(function (ev) {
        if ($(ev.target).hasClass("checked")) return;
        $("#nav_mode > button").toggleClass("checked");
        
        window.x3dom.runtime[$(ev.target).html()]();
        
        console.log("Nav mode: "+ $(ev.target).html())
    });
    
    // Rotation controllers
    $("#rleft").click(function (ev) {
        medea.rotate(true);
    });
    $("#rright").click(function (ev) {
        medea.rotate(false);
    });
    
    // Initial setup 
    // TODO: create a init() function
    
    // set xy as the active plane
    $("#xy").toggleClass("checked");
    planeToggle($("#xy").html());
    
    // set navigation mode to examine
    $("#examine").toggleClass("checked");
    //window.x3dom.runtime.examine();
});


