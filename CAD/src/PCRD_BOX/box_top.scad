h = 30;      // Výška horní části
s = 10;      // Výška spodní části
a = 5;       // Šířka krabičky (počet obsazených dírek)
b = 8;      // Délka krabičky (počet obsazených dírek)
d = 3;     // Průměr trnů a šířka hlavních příček (>1)
MLAB_grid = 10.16;
pedestal_height = 2; 

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






module konstrukce1()
{
  union() {
      // Hlavní příčky
     translate([0,(MLAB_grid*(a+1))/2,0]) 
      roundcube([d-2*roh,MLAB_grid*(a+1),d-2*roh],center = true, corner= roh);
     
     translate([(MLAB_grid*(b+1))/2,0,0])       
      roundcube([MLAB_grid*(b+1),d-2*roh,d-2*roh],corner= roh); 
      
     translate([0, 0, h/2])
      cylinder(h, d/2, d/2, center = true);
      
      //Vedlejší příčky - ve směru x
      for(i = [1:a]) {
     translate([(MLAB_grid*(b+1))/2,MLAB_grid*i,-d/4+roh/2])
      roundcube([MLAB_grid*(b+1),d-2*roh,(d-2*roh)/2],corner = roh);
      }
      //Vedlejší příčky - ve směru y
      for(i = [1:b]) {
     translate([MLAB_grid*i, (MLAB_grid*(a+1))/2, -d/4+roh/2])
      roundcube([d-2*roh, MLAB_grid*(a+1), (d-2*roh)/2],corner=roh);
      }
      //Vedlejší příčky - ve směru z
      for(i = [1:a]) {
     translate([0, MLAB_grid*i, h/2])
      cylinder(h, d/2, d/2, center = true);
      }
      for(i = [1:b]) {
     translate([MLAB_grid*i, 0, h/2])
      cylinder(h, d/2, d/2, center = true);
      }
      
      
 // ZAOBLENI ROHU    
  hull() {
difference() {
            union() {
    translate([0,(MLAB_grid*(a+1))/2,0]) 
      roundcube([d-2*roh,MLAB_grid*(a+1),d-2*roh],center = true, corner= roh);
     
     translate([(MLAB_grid*(b+1))/2,0,0])       
      roundcube([MLAB_grid*(b+1),d-2*roh,d-2*roh],corner= roh); 
      
     translate([0, 0, h/2-d/2+2*roh])
      roundcylinder(h, (d/2-roh), corner = roh);
            }
      translate([0,(MLAB_grid*(a+1))/2 + d,0]) 
        cube([20*d,MLAB_grid*(a+1)+d,20*d], center = true);
     
      translate([(MLAB_grid*(b+1))/2 + d,0,0]) 
        cube([MLAB_grid*(b+1)+d,20*d,20*d], center = true);
            
      translate([0, 0, -d/2 + d])
        cylinder(h + d, 20*d);
        }
    }
    
    
    
}
}
konstrukce1();
translate([(MLAB_grid*(b+1)),0,0]) 
mirror(1,0,1) konstrukce1();
translate([0,(MLAB_grid*(a+1)),0])
mirror([0,1,0]) konstrukce1();
translate([(MLAB_grid*(b+1)),0,0]) 
mirror(1,0,1)
translate([0,(MLAB_grid*(a+1)),0])
mirror([0,1,0]) konstrukce1();

// Konkrétní trny procházející plošným spojem
 translate([MLAB_grid*1, MLAB_grid*2, (h + s + pedestal_height)/2-d/2+2*roh])
       roundcylinder(h + s + pedestal_height, (d/2-roh), corner = roh);
 translate([MLAB_grid*4, MLAB_grid*5, (h + s + pedestal_height)/2-d/2+2*roh])
       roundcylinder(h + s + pedestal_height, (d/2-roh), corner = roh);
 translate([MLAB_grid*5, MLAB_grid*2, (h + s + pedestal_height)/2-d/2+2*roh])
       roundcylinder(h + s + pedestal_height, (d/2-roh), corner = roh);
 translate([MLAB_grid*8, MLAB_grid*5, (h + s + pedestal_height)/2-d/2+2*roh])
       roundcylinder(h + s + pedestal_height, (d/2-roh), corner = roh);
/* translate([MLAB_grid*10, MLAB_grid*1, (h + s + pedestal_height)/2-d/2+2*roh])
       roundcylinder(h + s + pedestal_height, (d/2-roh), corner = roh);
 translate([MLAB_grid*15, MLAB_grid*5, (h + s + pedestal_height)/2-d/2+2*roh])
       roundcylinder(h + s + pedestal_height, (d/2-roh), corner = roh);


*/


