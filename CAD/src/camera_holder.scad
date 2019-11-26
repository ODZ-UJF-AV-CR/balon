include <parameters.scad>


wall_thickness = 1.5;
wall_size = 5;
wall_height = camera_first_button_height+camera_buttons_distance*2+20;
bottom_thickness = 2;

protection_wire_diameter = 2;

side_difference = (camera_thickness_center-camera_thickness_side)/2;
center_to_side_distance = sqrt( pow(side_difference, 2) + pow(camera_width/2, 2) );
angle = atan( (camera_width/2) / (side_difference) );
main_radius = (center_to_side_distance/2) / cos(angle);

module bottom(height=1, offset=1) {
    linear_extrude(height = height)
    offset(delta=offset)
    intersection() {
        translate([-50, -camera_width/2, 0])
            square([100, camera_width]);

        translate([main_radius-camera_thickness_center/2, 0, 0])
            circle(r=main_radius, $fn=500);

        translate([-main_radius+camera_thickness_center/2, 0, 0])
            circle(r=main_radius, $fn=500);
    }
}

difference() {
    union() {
        bottom(wall_height+bottom_thickness, wall_thickness);

        translate([0, 0, wall_height-protection_wire_diameter-wall_thickness*4])
        difference() {
            hull() {
                translate([0, 0, bottom_thickness+(protection_wire_diameter+wall_thickness*4)/2])
                    cube([camera_thickness_side+wall_thickness, camera_width+wall_thickness*2, protection_wire_diameter+wall_thickness*4], center=true);

                translate([0, -camera_width/2-wall_thickness*2, bottom_thickness+wall_thickness*3])
                    rotate([0, 90, 0])
                        cylinder(d=protection_wire_diameter+wall_thickness*2, h=camera_thickness_side+wall_thickness, $fn=50, center=true);

                translate([0, camera_width/2+wall_thickness*2, bottom_thickness+wall_thickness*3])
                    rotate([0, 90, 0])
                        cylinder(d=protection_wire_diameter+wall_thickness*2, h=camera_thickness_side+wall_thickness, $fn=50, center=true);
            }
            translate([0, -camera_width/2-wall_thickness*2, bottom_thickness+wall_thickness*3])
                rotate([0, 90, 0])
                    cylinder(d=protection_wire_diameter, h=camera_thickness_side+wall_thickness*2, $fn=50, center=true);

            translate([0, camera_width/2+wall_thickness*2, bottom_thickness+wall_thickness*3])
                rotate([0, 90, 0])
                    cylinder(d=protection_wire_diameter, h=camera_thickness_side+wall_thickness*2, $fn=50, center=true);
        }
    }

    translate([0, 0, bottom_thickness])
        bottom(wall_height+1, 0);

    translate([0, 0, bottom_thickness+wall_height/2+wall_size])
        cube([100, camera_width-wall_size*2, wall_height], center=true);

    cylinder(d=camera_screw_diameter, h=bottom_thickness*3, $fn=20, center=true);

    translate([camera_usb_translate_x, camera_usb_translate_y, 0])
        cube([usb_height, usb_width, bottom_thickness*3], center=true);

    //buttons
    translate([0, 0, bottom_thickness+camera_first_button_height])
        rotate([-90, 0, 0])
            cylinder(d=camera_buttons_diameter, h=100, $fn=20);

    translate([0, 0, bottom_thickness+camera_first_button_height+camera_buttons_distance])
        rotate([-90, 0, 0])
            cylinder(d=camera_buttons_diameter, h=100, $fn=20);

    translate([0, 0, bottom_thickness+camera_first_button_height+camera_buttons_distance*2])
        rotate([-90, 0, 0])
            cylinder(d=camera_buttons_diameter, h=100, $fn=20);
}