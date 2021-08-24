# TrafficLightControl

This project aimed at figuring out a way to control traffic lights using reinforcement learning. 
Unfortunately it did not workk out because of two major probelms:

1) The simulation we used in sumo was completely random. Real life traffic is never random and usually follows a pattern.
2) In normal Q learning, we create a Q table that contains a value for each [ state, action ] pair. But what is the number of states and the actions which can be taken in that state are very high. (check [Test csv graph](https://github.com/Gr33nMayhem/TrafficLightControl/blob/main/MP3%20Reinforcement%20learning%20Implementation%20complete%20with%20Brute%20Force%20Approach/test.csv))

Check out [Video 1](https://github.com/Gr33nMayhem/TrafficLightControl/blob/main/MP3%20Reinforcement%20learning%20Implementation%20complete%20with%20Brute%20Force%20Approach/Video%20Tutorial%20on%20how%20to%20train%20part1.mp4) and [Video 2](https://github.com/Gr33nMayhem/TrafficLightControl/blob/main/MP3%20Reinforcement%20learning%20Implementation%20complete%20with%20Brute%20Force%20Approach/Video%20Tutorial%20on%20how%20to%20train%20part2.mp4) to learn how you can train using the simulation yourself.
