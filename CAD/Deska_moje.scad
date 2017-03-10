mount_hole = 3.5;
pedestal_height2 = 2;
clear = 0.175;
MLAB_grid = 10.16;
gloryHole=14; //pocet der
maximumSize=150;
corner=5;
$fn=20;

module deska () 
{
    difference () 
    {
        minkowski()
        {
            cube([maximumSize-2*corner,maximumSize-2*corner,pedestal_height2]);
            cylinder(r=corner,h=0.1);
        }
        translate([((maximumSize-corner)-(((gloryHole-1)*MLAB_grid)+corner))/2,((maximumSize-corner)-(((gloryHole-1)*MLAB_grid)+corner))/2,0])
        {
            for(i=[0:1:gloryHole-1])
            {
                for(j=[0:1:gloryHole-1])
                {
                    translate ([i*MLAB_grid,j*MLAB_grid,0])
                    {
                    cylinder (h = 2*pedestal_height2, r= mount_hole/2);
                    }
                }
            }
        }
    }
}


deska();