---
title: "Fully stressed and strained design"
date: 2017-04-15
categories:
  - "Technology"
  - "Research"
summary: "Explaining Fully Stressed Design, a heuristic for minimizing the mass of a lattice structure."
---

Fully Stressed Design (FSD) is a heuristic-based optimization method that minimizes the mass of a lattice structure by adjusting the cross section area of each bar.

The method iteratively updates the array of areas A with respect to the stress utilization ratio of each bar, i.e. for a particular bar, it’s area increases if it experiences too much stress, and decreases if it does not. The iteration stops when each bar is fully stressed, i.e. it’s stress is at yield, hence the name.

Basically, it is the computer doing what engineers have been doing for a long long time. Namely, the engineer sizes how thick each steel girder should be in a building so that the building doesn’t fall down, but still be cheap enough to be built, and doesn’t take up more usable floor space than necessary.

Now imagine if this engineer has in his hands not just steel but aluminum, or titanium, or magnesium. How would he pick the material the girder should be, in addition to picking the size.

Now, suppose we are using hollow metal tubes, and we can pick any radius or side length we wish because of some magical fabrication technologies, how can we, as engineers, choose wisely?
