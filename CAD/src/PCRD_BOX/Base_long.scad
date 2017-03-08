a = 6;       // Šířka krabičky (počet obsazených dírek)
b = 9;      // Délka krabičky (počet obsazených dírek)
d = 2.5;     // Průměr trnů a šířka hlavních příček (>1)  

c = 6;
d = 5;


pedestal_height = 2;   // designed for use the MLAB standard 12mm screws.
mount_hole = 3.5;

MLAB_grid = 10.16;
MLAB_grid_xoffset = MLAB_grid/2+d/2; //MLAB_grid-mount_hole-d/2;
MLAB_grid_yoffset = MLAB_grid/2+d/2; //MLAB_grid-mount_hole-d/2;




$fn=20;

union() {

difference () {
    minkowski()
    {
	cube([MLAB_grid*(b-1)+2*MLAB_grid_xoffset, MLAB_grid*(a-1)+2*MLAB_grid_yoffset, pedestal_height]);          // base plastics brick
        cylinder(r=d/2,h=0.1);
    }
    // MLAB grid holes
    grid_list = [for (j = [MLAB_grid_xoffset : MLAB_grid: MLAB_grid*b], i = [MLAB_grid_yoffset :MLAB_grid: MLAB_grid*a]) [j, i] ];
    for (j = grid_list) {
            translate (concat(j, [0]))
            cylinder (h = 2*pedestal_height, r= mount_hole/2);
    }
}

difference() {
 translate([MLAB_grid*(b-1)+2*MLAB_grid_xoffset, ((MLAB_grid*(a-1)+2*MLAB_grid_yoffset)-(MLAB_grid*(5)))/2, 0])
 minkowski()
    {
	cube([150-(MLAB_grid*(b-1)+2*MLAB_grid_xoffset)-d, MLAB_grid*(5), pedestal_height]);          // base plastics brick
        cylinder(r=d/2,h=0.1);
    }
    
  translate([MLAB_grid*(b-1)+2*MLAB_grid_xoffset, ((MLAB_grid*(a-1)+2*MLAB_grid_yoffset)-(MLAB_grid*(5)))/2, 0]) {
    grid_list = [for (j = [MLAB_grid : MLAB_grid: MLAB_grid*4], i = [MLAB_grid :MLAB_grid: MLAB_grid*4]) [j, i] ];
    for (j = grid_list) {
            translate (concat(j, [0]))
            cylinder (h = 2*pedestal_height, r= mount_hole/2); }}
/* translate([MLAB_grid*(b-1)+2*MLAB_grid_xoffset + 5, 0, 0])
    cube([6,6,20], centre = true); */
}
}