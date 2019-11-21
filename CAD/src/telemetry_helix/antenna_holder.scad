include <../parameters.scad>
draft = false;
$fn =  draft ? 50 :100;


module 888_3006(draft){    /////// 1. díl (AZ, YAW)

    length_screw_behind_nut = 3;
    head_screw_diameter = 13 + 0.2;		//průměr válcové hlavy šroubu
    head_screw_height = 8 + 0.2;		//výška válcové hlavy šroubu
    // pro dily ze skupiny 3 (888_30**)
    g3_0_cone1 = 70;
    g3_0_cone2 = 45;
    g3_0_cone_height = 25;
    g3_0_cone_top_height = 11;
    g3_0_height = 100;
    g3_0_bearing_bolt_len = 50;
    g3_0_srcew_dist = 55;
    height = ALU_profile_width;
    magnet_d = 80;
    antenna_pipe_outer_diameter =  16.2 + global_clearance;
    platform_height = 52;
    nut_size = 28; //šířka křídel matky na střeše
    cable_diameter=5;


    difference(){
        union(){

            hull(){
                cylinder(r = g3_0_cone1, h = 5, $fn = draft?50:100);
                translate([0,0, height/2 - 5])
                    cylinder(r = magnet_d/2 , h = 5, $fn=draft?50:100);
            }

            cylinder(r1=g3_0_cone2, r2=g3_0_cone2/4, h=g3_0_height, $fn=draft?50:100);

                for (i = [0:3]){
                    rotate([0, 0, i*90])
                        translate([g3_0_srcew_dist, 0, 30-18-5])
                            cylinder(h=6, d=M6_nut_diameter+5, $fn=50);
                }

        }

        // srouby pri pridelani na strechu
        for (i = [0:3]){
            rotate([0, 0, i*90])
            {
                // Washer
                translate([g3_0_srcew_dist, 0, 0])
                    cylinder(h = M8_washer_thickness, d = 19);
                // Nut hole
                translate([g3_0_srcew_dist, 0, M8_washer_thickness+layer_thickness])
                    cylinder(h = M6_nut_height - layer_thickness, d = M6_nut_diameter);
                // Bolt hole
                translate([g3_0_srcew_dist, 0, M8_washer_thickness + M6_nut_height + layer_thickness])
                    cylinder(h = platform_height, d = M6_screw_diameter);

            }
        }

        translate([0, 0, g3_0_height - g3_0_height /3 ])
        {
            rotate([90, 0, 0])
                cylinder(h = 150, d = M3_screw_diameter, $fn = 50, center = true);

            translate([0, -15,0])
              rotate([90, 0, 0])
                  cylinder(h = 150, d = M3_nut_diameter, $fn = 6);
            translate([0, 15,0])
              rotate([-90, 0, 0])
                  cylinder(h = 150, d = M3_nut_diameter, $fn = 6);
        }
        cylinder(h = 1000, d = 16 + global_clearance, $fn = draft?10:100);

        rotate([0, 0, -45])
            translate([0,-cable_diameter/2,0])
            cube([g3_0_cone1, cable_diameter,cable_diameter]);


    }
}

888_3006(draft);
