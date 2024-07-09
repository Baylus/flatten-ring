# V.10

So, stuff I have noticed from watching the replays is that Tarnished doesn't know well enough to avoid doing repeat actions. So he ends up losing more and more fitness points. However if he runs off the edge, he can't repeat actions, so he does that before he makes a ton of mistakes.

So, I am ramping up rewards a ton and toning down a ton those penalties, nearly eliminating them. Specifically the action penalty is cut to 10%. At this point, doing a new action will pay for 5 repeat actions, which means that it will start getting rewarded fairly quickly by doing new actions.

I am also cranking up a variety of pure rewards, like surviving, proximity to margit, and dealing damage (I know, a pipe dream for sure). I also want to enforce that it doesnt fall off the cliff. At this point, there should be enough reward for moving around with Margit that he will risk moving around the edges, hopefully.

## Changes
- Cut repeat action penalty to 10%
- Increase survival factor
- Increase reward from proximity to Margit
- Increase reward from dealing damage
- Increase reward from winning
- Increase penalty for falling off the cliff


## Results

Probably one of the most disappointing runs so far. By the time we reached 100 generations, Tarnished had gotten so afraid of acting at all that he simply learned how to make it to the cliff as quick as possible before he had made too many mistakes to get punished. So he was electing to die before making too many mistakes. Sigh.

Consulted the wizard. They are thinking that it would be best to:
- reset the repeated action penalty once a new action is made. 
- Give a flat reward for the number of unique actions made in the game.

A couple valuable insights they gave about my configurations was:
```
pop_size = 500

n_generations = 200

activation_default = "tanh"  # Consider experimenting with 'relu' or 'leaky_relu'

mutation_rate = 0.25
mutate_add_node = 0.01  # Good, consider slightly higher if too few new nodes
mutate_delete_node = 0.005  # Good
mutate_add_connection = 0.1  # Good, ensures new connections are frequently tested
mutate_delete_connection = 0.1  # Good

mate_only_prob = 0.2  # Good
survival_threshold = 0.2  # Good

compatibility_threshold = 3.0  # Good, but monitor and adjust based on speciation performance

elite_fraction = 0.01  # Good, ensures top performers are preserved

species_fitness_func = "max"  # Good
max_stagnation = 20  # Good, prevents long periods without improvement

initial_connection = "partial_directed"  # Good for initial diversity
```
Adjust Based on Observations:
    If you observe too many species with little improvement, lower the compatibility threshold.
    If stagnation occurs frequently, consider increasing mutation rates or adjusting the stagnation parameters.

