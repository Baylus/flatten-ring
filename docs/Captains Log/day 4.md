# V0.9

Going to have to slow down on these updates. Will likely start using one major version a day and then using minor versions for the several throughout the day. Starting today with 0.9.

## Changes

- Giving a reward for choosing a new move, that will offset the penalty they accrue from their repeated move choice.
This is interesting, because technically, they could do repeated moves enough to earn them stockpiled points that they can "cash in" when they do a repeated move, where the fitness loss function will actually give them fitness points for having done that action. I think this works out well, and I am making the reward lower than the penalty. Hopefully a mix of 3 new moves and then you earn a free repeat move.
- Increasing Tarnished's survival factor, so he doesnt fall off the cliffs as much in the beginning so that he can learn better habits earlier. Currently, if he makes it to the end, he gets (0.3 factor * 1000 max updates) 300 fitness, which is equivalent to a win. It might seem like a lot and may incentivize him to run away, but I think by the time he learns to stick to the platform long enough to attack, we will see him learn to farm his points from attack margit instead.

### Bug Fixes
- There was an error in calculating losses, and how I was being very forgiving with losses for tarnished because of the fact that he used to lose fitness by taking damage, which is no longer in effect. So he has been ice skating his way to pick up as many points as possible before yeeting himself off of the cliffs