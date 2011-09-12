(function (Raphael) {
    Raphael.controller = function (x, y, size, element) {
        return new Controller(x, y, size, element);
    };
    
    var Controller = function (x, y, size, element) {
        // *** start drawing controller
        size = size || 200;
        var size2 = size / 2,
            size5 = size / 5,
            size10 = size / 10;
            padding = size * 0.02,
            width = size * 0.02;
        
        var r = element ? Raphael(element, size, size) : Raphael(x, y, size, size);
        
        // Controller area
        var rect = r.rect(-size2 + padding, -size2 + padding, size - padding, size - padding);
        rect.attr({stroke: "#222", "stroke-width": width, fill: "#cfa"});
        
        var area = r.set();
        area.push(rect,
            rect.clone().translate(size - padding, 0).attr({fill: "#fea"}),
            rect.clone().translate(0, size - padding).attr({fill: "#faa"}),
            rect.clone().translate(size - padding, size - padding).attr({fill: "#acf"})
        );
        //area.rotate(45, size2, size2);
        this.area = area;
        
        // Controller cursor
        var cursor = r.circle(size2, size2, size10/2);
        cursor.attr({stroke: "#222", "stroke-width": width, fill: "#fff"});
        this.cursor = cursor;
        // *** end drawing controller
        
        // Private callback on cursor drag
        this._movecback = null;
        this._startcback = null;
        this._stopcback = null;
        
        // Events
        // Cursor drag
        var lbound = padding*2;
        var rbound = size - lbound;
        var t = this; 
        this.cursor.drag(
            function (dx, dy) {
                this.attr({
                    cx: Math.min(Math.max(this.ox + dx, lbound), rbound),
                    cy: Math.min(Math.max(this.oy + dy, lbound), rbound)
                })
                
                if (typeof t._movecback === 'function') {
                    var vx = (dx / this.ox) - (this.odx / this.ox),
                        vy = (-dy / this.oy) - (this.ody / this.oy);
                     
                    t._movecback(vx, vy);
                    this.odx = dx, this.ody = -dy;
                }
            },
            function () {
                this.ox = this.attr("cx");
                this.oy = this.attr("cy");
                
                this.odx = 0;
                this.ody = 0;
                
                if (typeof t._startcback === 'function') t._startcback(); 
                /*
                // makes the cursor blinking
                var that = this;
                var glowing = function () {
                    that.animate(
                        {"50%": {opacity: .2},
                         "100%": {opacity: 1, callback: glowing}}, 1000);
                };
                glowing();
                */
            },
            function () {
                this.stop();
                this.attr({cx: this.ox, cy: this.oy, opacity: 1});
                
                if (typeof t._stopcback === 'function') t._stopcback();
            }
        );
    };
    
    // Binding callback functions
    Controller.prototype.bind = function (move, start, stop) {
        if (typeof move === 'function') this._movecback = move;
            
        if (typeof start === 'function') this._startcback = start;
           
        if (typeof stop === 'function') this._stopcback = stop;
    };
})(window.Raphael);