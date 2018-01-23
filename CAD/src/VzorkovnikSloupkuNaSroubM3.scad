h = 18;      // Výška horní části

c = 0.8;   // Tloušťka stěn

vt = h-6-c; // Výška trubek
po = 2.8; // Nejmenší vnitří průměr trubky
pt = po + 2.5; //Vnější průměr trubky

$fn=20;

union(){

    for (k = [0 : 8]) {
        translate([k*8, 0, vt/2])
            difference() {
                cylinder(vt, pt/2, pt/2, center = true);
                translate([0, 0, vt/2])
                    cylinder(18, (po+k*0.1)/2, (po+k*0.1)/2, center = true); 
            }
    }
    translate([-5, -5, 0])
        cube([75, 10, 1]);
}