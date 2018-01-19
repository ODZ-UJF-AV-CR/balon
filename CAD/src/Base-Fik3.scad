a = 9;       // Šířka krabičky (počet obsazených dírek)
b = 14;      // Délka krabičky (počet obsazených dírek)
d = 2.5;     // Průměr trnů a šířka hlavních příček (>1)  

pedestal_height = 2;   // designed for use the MLAB standard 12mm screws.
mount_hole = 3.5;

MLAB_grid = 10.16;
MLAB_grid_xoffset = 6.75;  // Celková délka destičky max 22 cm
MLAB_grid_yoffset = 6.75;  // Max 10 cm

drat = 2;  // Průměr otvoru na dráty
o = MLAB_grid;   //Vzdálenost okrajů od děr v plošňáku


$fn=20;


difference () {
    minkowski()
    {
  cube([MLAB_grid*(b-1)+2*MLAB_grid_xoffset, MLAB_grid*(a-1)+2*MLAB_grid_yoffset, pedestal_height]);          // base plastics brick
        cylinder(r=d/2,h=0.1);
    }
  union() {
    // MLAB grid holes
    grid_list = [for (j = [MLAB_grid_xoffset : MLAB_grid: MLAB_grid*b], i = [MLAB_grid_yoffset :MLAB_grid: MLAB_grid*a]) [j, i] ];
    for (j = grid_list) {
            translate (concat(j, [0]))
            cylinder (h = 2*pedestal_height, r= mount_hole/2);
    }
    
  
    
    
    }
}