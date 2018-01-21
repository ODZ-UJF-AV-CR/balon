h = 30;      // Výška horní části
s = 4;      // Výška spodní části
a = 4;       // Šířka krabičky (počet obsazených dírek)
b = 9;      // Délka krabičky (počet obsazených dírek)
d = 1.8;     // Průměr trnů a šířka hlavních příček (>1)
c = 0.8;   // Tloušťka stěn

drat = 1.5;  // Průměr/výška otvoru na dráty

okraj = 2;  // šířka horního okraje

clear = 0.4;      // K otvoru na matičku
nut_size = 6.6;     // K otvoru na matičku

MLAB_grid = 10.16;
pedestal_height = 2; 

ot = 6*MLAB_grid/11;         //Vzdálenost okraje od děr v plošňáku pro stranu s tunelem
o = MLAB_grid/2+d/2;   //Vzdálenost zbylých okrajů od děr v plošňáku

tp = 1.4;  // Tloušťka přepážky

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
  difference() {
  union() {
      // Hlavní příčky
     translate([0,(MLAB_grid*(a-1))/2+o,0]) 
      roundcube([d-2*roh, MLAB_grid*(a-1)+2*o, d-2*roh],center = true, corner= roh);
     
     translate([(MLAB_grid*(b-1))/2+ot,0,0])       
      roundcube([MLAB_grid*(b-1)+2*ot, d-2*roh, d-2*roh],corner= roh); 
      
     translate([0, 0, h/2])
      cylinder(h, d/2, d/2, center = true);
      
 
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
   

 //Pacička

translate([ot-MLAB_grid, o,h-1.5]) {
    difference() {  
        hull() {
        translate([0,-3/7*MLAB_grid,0])
            cube([MLAB_grid-ot-0.2,2*3/7*MLAB_grid,1.5]);
            cylinder(1.5, 3/7*MLAB_grid, 3/7*MLAB_grid);
        translate([MLAB_grid-ot-c, -3/7*MLAB_grid, -3*h/4])
            cube([c-0.2, 2*3/7*MLAB_grid, 1.5]);
        }
    translate([0,0,1.5/2+0.4])   
    cylinder(3, 3.5/2, 3.5/2, center = true);
    translate([0,0,-h/2])
    rotate(0)
    cylinder (h-1.5, r= (nut_size+clear)/2, center = true, $fn=6);
    } 
}

  
}

/* // Oříznutí sloupků
translate([0,0, h - 10]) 
        cube([MLAB_grid*(b)+o,MLAB_grid*(a)+o,20*d]); */
    
/* //Pacička

translate([o-MLAB_grid, o,h -d/2]) {
    difference() {  
        union() {
    translate([0,-3.5,0])
    cube([MLAB_grid-o,2*3.5,d/2]);
    cylinder(d/2, 1/3*MLAB_grid, 1/3*MLAB_grid);
        }
        
    cylinder(h, 3.5/2, 3.5/2, center = true);
    } 
}
 
// Horní příčka k pacičce
translate([-d/2, 0, h - d/2])
    cube([d/2,MLAB_grid*(a-1)+2*o,d/2]);

*/

}







}
konstrukce1();

  



//Zrcadlení

translate([MLAB_grid*(b-1)+2*ot,0,0]) 
mirror(1,0,1) konstrukce1();
translate([0,MLAB_grid*(a-1)+2*o,0])
mirror([0,1,0]) konstrukce1();
translate([MLAB_grid*(b-1)+2*ot,0,0]) 
mirror(1,0,1)
translate([0,MLAB_grid*(a-1)+2*o,0])
mirror([0,1,0]) konstrukce1();



// Obal klece
    difference() {
        union() {
translate([-d/2,0,0]) 
cube([c, MLAB_grid*(a-1)+2*o, h]);

translate([0,-d/2,0]) 
cube([(MLAB_grid*(b-1))+2*ot, c, h]);

translate([0,0,-d/2]) 
cube([(MLAB_grid*(b-1))+2*ot, (MLAB_grid*(a-1))+2*o, c]);
            
translate([(MLAB_grid*(b-1))+2*ot+d/2-c,0,0]) 
cube([c, MLAB_grid*(a-1)+2*o, h]);

translate([0,(MLAB_grid*(a-1))+2*o+d/2-c,0]) 
cube([(MLAB_grid*(b-1))+2*ot, c, h]);
            
// Horní příčky
translate([okraj/2-d/2, (MLAB_grid*(a-1)+2*o)/2, h-1.5*okraj])
   difference() {
    cube([okraj,MLAB_grid*(a-1)+2*o,3*okraj], center = true);  
    translate([okraj/2,0,0])
    rotate([0,15,0])
    cube([okraj,MLAB_grid*(a-1)+2*o,10*okraj], center = true);   
   } 
        
translate([(MLAB_grid*(b-1))+2*ot-okraj/2+d/2, (MLAB_grid*(a-1)+2*o)/2, h - 1.5*okraj])
    difference() {
    cube([okraj,MLAB_grid*(a-1)+2*o, 3*okraj], center = true);
    translate([-okraj/2,0,0])    
    rotate([0,-15,0])
    cube([okraj,MLAB_grid*(a-1)+2*o,10*okraj], center = true);   
   } 
        
translate([(MLAB_grid*(b-1)+2*ot)/2, okraj/2-d/2, h - 1.5*okraj])
    difference() { 
   cube([MLAB_grid*(b-1)+2*ot, okraj, 3*okraj], center = true);
  
   translate([0,okraj/2,0])
    rotate([-15, 0, 0])
   cube([MLAB_grid*(b-1)+2*ot, okraj, 10*okraj], center = true);
   }
       
 translate([(MLAB_grid*(b-1)+2*ot)/2, (MLAB_grid*(a-1))+2*o-okraj/2+d/2, h - 1.5*okraj])
    difference() { 
   cube([MLAB_grid*(b-1)+2*ot, okraj, 3*okraj], center = true);
   translate([0,-okraj/2,0])
    rotate([15, 0, 0])
   cube([MLAB_grid*(b-1)+2*ot, okraj, 10*okraj], center = true);
   }
 
 
   
// Přepážka 1 - u otvoru na dráty
       translate([MLAB_grid, o+MLAB_grid*1.5, (h-5)/2-d/2+c])
       cube([tp, MLAB_grid*(a)+2*d-c, h-5], center = true);
    
        } 
        
//Otvor na dráty
        translate([-5, ((MLAB_grid*(a-1))+2*o)/2,h])
    cube([13,MLAB_grid-d,2*drat],center=true);      
     
/*  translate([2.5*okraj-d/2, (MLAB_grid*(a-1)+2*o)/2, h])
   cube([5*okraj-1.9,MLAB_grid,2], center = true);     */
           
        
/*    translate([-5, ((MLAB_grid*(a-1))+2*o)/2,h])
    rotate([0,90,0])
    cylinder(10, drat/2, drat/2, centre=true);
        
    translate([-5, ((MLAB_grid*(a-1))+2*o)/2+drat,h])
    rotate([0,90,0])
    cylinder(10, drat/2, drat/2, centre=true);
        
    translate([-5, ((MLAB_grid*(a-1))+2*o)/2-drat,h])
    rotate([0,90,0])
    cylinder(10, drat/2, drat/2, centre=true);
    
    translate([-5, ((MLAB_grid*(a-1))+2*o)/2-2*drat,h])
    rotate([0,90,0])
    cylinder(10, drat/2, drat/2, centre=true);
        
    translate([-5, ((MLAB_grid*(a-1))+2*o)/2+2*drat,h])
    rotate([0,90,0])
    cylinder(10, drat/2, drat/2, centre=true); */
    }
    

    


    
/*
    
    // Konkrétní trny procházející plošným spojem
 translate([ot+MLAB_grid*1, o, (h + s + pedestal_height)/2-d/2+2*roh])
       roundcylinder(h + s + pedestal_height, (d/2-roh), corner = roh);
 translate([ot+MLAB_grid*4, o+MLAB_grid*3, (h + s + pedestal_height)/2-d/2+2*roh])
       roundcylinder(h + s + pedestal_height, (d/2-roh), corner = roh);
 translate([ot+MLAB_grid*5, o, (h + s + pedestal_height)/2-d/2+2*roh])
       roundcylinder(h + s + pedestal_height, (d/2-roh), corner = roh);
 translate([ot+MLAB_grid*8, o+MLAB_grid*3, (h + s + pedestal_height)/2-d/2+2*roh])
       roundcylinder(h + s + pedestal_height, (d/2-roh), corner = roh);
       
  
   */
 
   

