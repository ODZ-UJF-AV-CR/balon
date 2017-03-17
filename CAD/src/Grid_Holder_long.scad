h = 5;      // Výška sloupků

a = 8;       // Výška  (počet  dírek)
b = 7;      // Délka (počet dírek)
d = 2.5;     // Průměr trnů (>1)
c = 2;   // Tloušťka stěn

mount_hole = 3.5;

drat = 1.5;  // Průměr/výška otvoru na dráty

okraj = 2;  // šířka horního okraje

MLAB_grid = 10.16;
pedestal_height = 2; 

ot = MLAB_grid;         //Vzdálenost okraje od děr v plošňáku pro stranu s tunelem
o = 4;   //Vzdálenost zbylých okrajů od děr v plošňáku



$fn=20;

roh =0.5; // Zaoblení hran

// Kvádr a válec se zaoblenými hranami
module roundcube(size,center=true,corner) {
  minkowski() {
    cube(size,center);
    sphere(corner);
  }
}

module roundcylinder(size, r, center=true, corner) {
  minkowski() {
    cylinder(size, r, r, center);
    sphere(corner);
  }
}





difference(){
   union(){ cube([(b-1)*MLAB_grid+o,2*o+MLAB_grid,c]);
    cube([c,2*o+MLAB_grid,o+a*MLAB_grid]);}

     union() {
    // MLAB grid holes
    grid_list1 = [for (j = [ 2*MLAB_grid : MLAB_grid: MLAB_grid*(b-2)], i = [o :MLAB_grid: MLAB_grid*2]) [j, i] ];
    for (j = grid_list1) {
            translate (concat(j, [1]))
            cylinder (h = 2*c, r= mount_hole/2, center = true);
    }
  grid_list2 = [for (k = [ 2*MLAB_grid : MLAB_grid: MLAB_grid*a], l = [o :MLAB_grid: MLAB_grid*2]) [k, l] ];
    for (k = grid_list2) {
            rotate([0,-90,0])
            translate (concat(k, [-1]))
            cylinder (h = 2*c, r= mount_hole/2, center = true);
    }
    }
    
}  
translate([(b-1)*MLAB_grid, o, h/2 + roh])
roundcylinder(h, r=d/2-roh, center = true, corner=roh);

translate([(b-1)*MLAB_grid, o+MLAB_grid, h/2 + roh])
roundcylinder(h, r=d/2-roh, center = true, corner=roh);

/*translate([(b-2)*MLAB_grid, o, h/2 + roh])
roundcylinder(h, r=d/2-roh, center = true, corner=roh);

translate([(b-2)*MLAB_grid, o+MLAB_grid, h/2 + roh])
roundcylinder(h, r=d/2-roh, center = true, corner=roh); */

// Příčky    
 
     hull() {
       
      translate([0, o-d/2, 0]) 
        cube([MLAB_grid + 2*o, d, 2]);
         
      translate([0, o-d/2, 0]) 
        cube([2, d , MLAB_grid + 2*o]);
     }
     hull() {
     
       translate([0, o+MLAB_grid-d/2, 0]) 
        cube([MLAB_grid + 2*o, d, 2]);
         
      translate([0, o+MLAB_grid-d/2, 0]) 
        cube([2, d, MLAB_grid + 2*o]);
    }             
    
    
 