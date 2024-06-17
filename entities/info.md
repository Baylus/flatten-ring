There are a couple of abilities that lock up a character's movement, or add extreme complexity. I am going to list the things that may be complicated for the AI to understand, and thus take many more generations for the AI to work out the kinks of them. I will provide information on what these mechanics would be, and whether I am considering them yet.

Note: The method I will be using to handle multi tick actions is to simply ignore the output of the AI

### Dodge
Tarnished dodges out of the way, increasing speed briefly and slowing down while approaching target destination. Destination/angle is dependent on current movement actions, no movement yields straight forward dodge.

Provides Iframes for most of the dodge, except for a little bit at the end of the movement.

I will be using a linear decay to the speed, despite it not making as much kinetic sense as a logarithmic curve.