# Statistical Analysis of Indian Cricketers

This project compares the batting performance of left-handed and right-handed Indian male cricketers in different game patterns, with a separate analysis for female cricketers.

When we started our project we got doubt that what statistic should we compare for grading a player performance. After the discussion we arrived at a ground breaking final formulae for analysing a player performance. The formulae is given below

\[
S = 0.01 \times \text{Total Runs} + 0.5 \times \text{Strike Rate} + 1.5 \times \text{Total Centuries} + 0.5 \times \text{Total Half-Centuries}
\]

This is very similar to grading a student in DAI. We gave point S to each player based on their performance like runs, strike rate, centuries and halfcenturies. We know that you got doubt about how these people arrived this formulae and how did they decide constants. Don't worry we are here to explain you that only.

## Explanation

We concluded that considering only one factor could lead to an inaccurate evaluation of a player's performance. Using only total runs may introduce a bias towards experienced players who have played more innings and faced more balls, allowing them to accumulate higher scores. On the other hand, relying solely on strike rate may favour players who have faced very few balls but scored quickly. For example, a player who scores 18 runs in a single over achieves a strike rate of 300, but such a small sample is insufficient to judge their overall performance. Furthermore, the number of centuries and half-centuries scored by a player can help estimate their consistency and ability to deliver significant contributions in matches. Therefore, we decided to evaluate players using a weighted scoring system based on total runs, strike rate, and the number of centuries and half-centuries. By observing the statistics of real players, we assigned weights such that every increase of 100 runs contributes 1 point, while every increase of 10 in strike rate contributes 5 points. Centuries and half-centuries are also considered to reward players for consistently scoring substantial runs across matches.

If you are still not satisfied, don't worry we also don't know that much. We can think it as a Grading scheme. In our whole project We will be grading players using this formulae.

The detailed analysis, methodology, results, and conclusions will be documented.


