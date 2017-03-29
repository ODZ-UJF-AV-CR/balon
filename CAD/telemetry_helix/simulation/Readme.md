

Source: http://uuki.kapsi.fi/qha_simul.html#software


helix2nec: The model generation software

I simulated a bunch of QHAs and dual QHA combinations using the NEC2 simulation software. To aid in generating the NEC2 models, I wrote a simple and stupid (and incredibly ugly) program in C to automatically generate NEC2 source code according to given QHA dimensions (height, diameter, number of twists and so on). It can generate either a single QHA or multiple QHAs stacked according to your preference. It does not generate QHA dimensions for your design frequency—for that you'll want to use John Coppens's Quadrifilar online calculator. Take the dimensions it gives, and plug them into helix2nec.

If you like, you can download helix2nec.c. It's not pretty. You can also download an example input file, dual_435.helix, which creates a NEC2 model of the 2 m and 70 cm combination, and tells NEC2 to simulate it in the UHF range.

The input file's structure is as follows:

    The first line defines how many helices there will be.
    The following lines define each helix, one helix per line. There must be as many lines as the first line specified. Each line contains, in this order:
        Height of the smaller loop
        Diameter of the smaller loop
        Height of the larger loop
        Diameter of the larger loop
        Bend radius (of the 90-degree turns)
        Wire diameter
        Number of twists in the helix
        Vertical offset of this helix
        Angle offset of this helix (in degrees)
        Feed type: F=feed, T=terminated, O=open, S=shorted 
    All lengths are in millimeters, measured from the center of the conductors. The model must contain precisely one helix with feed type F, other helices must be terminated, open or shorted.
    The last line specifies the start frequency, end frequency, and frequency increment, in MHz. 

This will produce a left-hand helix with standard feedpoint configuration. When the feedpoint is located at the top, the antenna will radiate skyward with right-hand (RHCP) circular polarization. See below for how to choose the twist direction and feedpoint configuration, if you want other polarization or radiation direction. If you want to model a QHA with right-hand twists, specify a negative number for the number of twists in the input file. To get an anti-standard feedpoint, exchange the dimensions of the larger loop and the smaller loop with each other. There is no simple way to move the feedpoint to the bottom, so if that's what you need, just stand on your head when you view the results.

Compiling the program:

   gcc -ohelix2nec helix2nec.c -lm

Using the program:

    ./helix2nec single_869.helix helix.nec
    nec2c -ihelix.nec -ohelix.out
    xnecview helix.out



