# Statistical Analysis of Indian Cricketers

This project compares the batting performance of left-handed and right-handed Indian male cricketers in different game formats, with a separate analysis for female cricketers.

When we started our project, we had a doubt about which statistics we should compare to grade a player's performance. After discussion, we arrived at a groundbreaking final formula for analysing a player's performance. The formula is given below:

**S = (0.01 × Total Runs) + (0.5 × Strike Rate) + (1.5 × Total Centuries) + (0.5 × Total Half-Centuries)**

This is very similar to grading a student in DAI. We assigned a score, S, to each player based on their performance in terms of runs, strike rate, centuries, and half-centuries. We know that you might be wondering how we arrived at this formula and how we decided on the constants. Don't worry; we are here to explain that.

## Explanation

We concluded that considering only one factor could lead to an inaccurate evaluation of a player's performance. Using only total runs may introduce a bias towards experienced players who have played more innings and faced more balls, allowing them to accumulate higher scores. On the other hand, relying solely on strike rate may favour players who have faced very few balls but scored quickly. For example, a player who scores 18 runs in a single over achieves a strike rate of 300, but such a small sample is insufficient to judge their overall performance.

Furthermore, the number of centuries and half-centuries scored by a player can help estimate their consistency and ability to deliver significant contributions in matches. Therefore, we decided to evaluate players using a weighted scoring system based on total runs, strike rate, and the number of centuries and half-centuries. By observing the statistics of real players, we assigned weights such that every increase of 100 runs contributes 1 point, while every increase of 10 in strike rate contributes 5 points. Centuries and half-centuries are also considered to reward players for consistently scoring substantial runs across matches.

If you are still not satisfied, don't worry; we don't know that much either. We can think of it as a grading scheme. Throughout our project, we will be grading players using this formula.


Here is the analysis for Left hand batsman and Right Hand Batsman in T20 Format.

## 📊 Statistics Summary —RIGHT HAND BATSMEN (250 Players)

| Column | Count | Mean | Variance |
|:---|---:|---:|---:|
| Total Runs | 250 | 913.9040 | 2569835.4285 |
| Strike Rate | 250 | 122.5667 | 482.9646 |
| Centuries | 206 | 0.3107 | 1.6786 |
| Half Centuries | 206 | 4.7718 | 141.9331 |
| S | 250 | 72.7724 | 778.1117 |

## 📊 Statistics Summary — LEFT HAND BATSMEN(68 Players)

| Column | Count | Mean | Variance |
|:---|---:|---:|---:|
| Total Runs | 68 | 1500.5000 | 3463373.6866 |
| Strike Rate | 68 | 131.2804 | 508.0896 |
| Centuries | 67 | 0.3731 | 0.9344 |
| Half Centuries | 67 | 6.8507 | 135.1895 |
| S | 67 | 84.7283 | 924.3277 |


The detailed analysis, methodology, results, and conclusions will be documented.
