
// OpenSCAD script for a 2.4GHz "quadrifilar helix antenna".
// -------------------------------------------------------------
// Dimensions calculated with John Coppens webpage java script
// @ http://jcoppens.com/ant/qfh/calc.en.php
// Input params:
// Center frequency = 2450 MHz
// Numbers of turns = 0.5
// Length of one turn = 1
// Bending radius = 1
// Width/height ratio = 0.44
// -------------------------------------------------------------


$fn=40;
SLICES=20;
PI = 3.14159265358979;

D1 = 17.9; // mm large helix1 diameter.
D2 = 17.1; // mm small helix2 diameter.
HH1 = 40.8; // mm height of helix1.
HH2 = 38.8; // mm height of helix2.

WIRE = 3; // mm diameter.

CYLH = 45; // mm height of support cylinder.
CYLH2 = CYLH/2; // the half-height of the support cylinder.

HWIRE11 = CYLH2-HH1/2; // place the four hole-pairs at these heights.
HWIRE12 = CYLH2-HH2/2;
HWIRE21 = CYLH2+HH1/2;
HWIRE22 = CYLH2+HH2/2;

// some internal calculations. quite hairy math.
THETA1 = atan2(HH1,D1*PI); // Thetas are used for projecting the wirechannel cross-section onto the xy-plane.
THETA2 = atan2(HH2,D2*PI);
echo("theta1=",THETA1,"  -  theta2=",THETA2);

XSI1 = ((CYLH/HH1*180)-180); // extra rotation beyond the height of helix1. half above, half below.
XSI2 = ((CYLH/HH2*180)-180); // extra rotation beyond the height of helix2.
echo("xsi1=",XSI1," - xsi2=",XSI2);


// test helix1.
module helix1(rot1=0)
{
	linear_extrude(height=50, twist=-XSI1-180, slices=SLICES) 
		rotate([0,0,rot1-XSI1/2]) translate([D1,0,0]) projection() scale([1,1/sin(THETA1),1]) wirechannel();
}

// test helix2.
module helix2(rot2=90)
{
	color("red") linear_extrude(height=50, twist=-XSI2-180, slices=SLICES) 
		rotate([0,0,rot2-XSI2/2]) translate([D2,0,0]) projection() scale([1,1/sin(THETA2),1]) wirechannel();
}



// definition of the wire channel by CSG. 
// used for projecting outline onto the xy-plane.
module wirechannel()
{
	difference()
	{
		cylinder(h=2, r=WIRE/2*1.8, center=true);
		translate([0,0,-0.1]) cylinder(h=3, r=WIRE/2, center=true);
		translate([1.5*WIRE,0,0]) cube([3*WIRE,WIRE,4], center=true);
	}
}

// definition of elliptic cylinder by CSG.
// used for projecting outline onto xy-plane.
module ellipse_base()
{
	scale([1,D2/D1,1]) difference() { cylinder(h=1, r1=(D1-WIRE/2)); translate([0,0,-0.2]) cylinder(h=2, r1=(D1-WIRE/2.1)); }
}

// just a elliptic torus.
// (penalty for using $fn quality.)
module torus(Rmajor=10, Rminor=1, h1=25)
{
	translate([0,0,h1]) scale([1,D2/D1,1]) rotate_extrude(convexity = 10) translate([Rmajor, 0, 0]) circle(r = Rminor); 
}

// the composite structure of support cylinder, wire channels, holes and cut-outs.
module composite()
{
	difference()
	{
		union()
		{
			// combine all elements in one extrude and twist.
			// helix1's.
			linear_extrude(height=HWIRE21, twist=-XSI1/2-180, slices=SLICES)
			{
				rotate([0,0,0-XSI1/2]) translate([D1,0,0]) projection() scale([1,1/sin(THETA1),1]) wirechannel();
				rotate([0,0,180-XSI1/2]) translate([D1,0,0]) projection() scale([1,1/sin(THETA1),1]) wirechannel();
			}
			// helix2's.
			linear_extrude(height=HWIRE22, twist=-XSI2/2-180, slices=SLICES)
			{
				rotate([0,0,90-XSI2/2]) translate([D2,0,0]) projection() scale([1,1/sin(THETA2),1]) wirechannel();
				rotate([0,0,270-XSI2/2]) translate([D2,0,0]) projection() scale([1,1/sin(THETA2),1]) wirechannel();
			}
			// elliptic support cylinder.
			linear_extrude(height=CYLH, twist=-XSI1/2-180, slices=SLICES)
			{
				rotate([0,0,0-XSI1/2]) projection(cut=true) ellipse_base();
			}

			// half-height marker on cylinder
			rotate([0,0,90]) torus(Rmajor=(D1-WIRE/2), Rminor=0.2, h1=CYLH2);
		}
		union()
		{
			// lower hole pairs.
			translate([0,0,HWIRE11]) rotate([0,90,0]) cylinder(h=3*HH1, r=WIRE/2, center=true);
			translate([0,0,HWIRE12]) rotate([90,0,0]) cylinder(h=3*HH1, r=WIRE/2, center=true);

			// upper hole slots.
			translate([0,0,HWIRE21]) rotate([0,90,0]) cylinder(h=3*HH1, r=WIRE/2, center=true);
			translate([0,0,HWIRE22]) rotate([90,0,0]) cylinder(h=3*HH1, r=WIRE/2, center=true);

			translate([0,0,HWIRE21+CYLH2]) cube([CYLH,WIRE,CYLH], center=true);
			translate([0,0,HWIRE22+CYLH2]) cube([WIRE,CYLH,CYLH], center=true);
		}
	}
}

module drillholes()
{
	// lower hole pairs.
	translate([0,0,HWIRE11]) rotate([0,90,0]) cylinder(h=3*HH1, r=WIRE/3, center=true);
	translate([0,0,HWIRE12]) rotate([90,0,0]) cylinder(h=3*HH1, r=WIRE/3, center=true);

	// upper hole pairs.
	translate([0,0,HWIRE21]) rotate([0,90,0]) cylinder(h=3*HH1, r=WIRE/3, center=true);
	translate([0,0,HWIRE22]) rotate([90,0,0]) cylinder(h=3*HH1, r=WIRE/3, center=true);
}

//wirechannel();
//helix1(rot1=0);
//helix1(rot1=180);
//helix2(rot2=90);
//helix2(rot2=270);
//drillholes();

// MAIN()
composite();




