# Asteroids
Using Python Arcade to practice OOP principles.

On this project, I had to use OOP basic principles such as inheritance and polymorphism to create the classic arcade game, Asteroids.

What does it do?
The game consists of a spaceship that destroys asteroids using a laser. The spaceship maintains its speed and direction when floating, just as happens in space. The user can rotate the ship and accelerate to change its speed and or direction.
The laser is shooted by the front of the spaceship at the shipping speed plus the shooting speed. In case they don't hit anything, they disappear in a certain period, avoiding them to remain floating in space.
The asteroids work with hierarchy. Each one has its random acceleration, rotation speed, and direction.
The game starts in Level 1 with five "big" asteroids surrounding the ship. Every time the user hits one of these asteroids with the laser, it would break into two smaller "medium" asteroids. When the laser hits any medium asteroid, this fragments into two "small" asteroids. These are destroyed (disappear) on the laser hit.
All the objects are wrapped in the screen. So if any item goes off a side of the screen, it reappears on the opposite side.
The ship is destroyed when hit by any asteroid independent of its size.
Every time the user destroys all the asteroids it goes to the next level, which adds one more big asteroid to the previous account. Level one starts with five asteroids, level 2 with six, and so on.

What was the most challenging?
Set up the spaceship gravity, having inertia while flying, giving the user the sensation that the ship is floating in space.

What did I like the most?
To implement the interplay of the different objects that float in space. Also, use inheritance to create different kinds of Asteroids.

What would I improve?
I would create lives for the spaceship and hit levels. In this way, it would take more than a single hit to destroy the ship, but it will lose a "life percentage" according to the size of the asteroid it hit.
