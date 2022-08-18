# FDA + State Space Research

## State Space
- https://en.wikipedia.org/wiki/State-space_representation
- http://www.akhatib.com/simple-state-space-model-of-a-pendulum/

## Notes

### first state space demonstration: pendulum
In order to start integrating state space with FDA, I decided to make sure I fully understood state space and create my own model of a simple 2D pendulum. Through my research, I found the general time-invariant state space form and the states and inputs required for a simple pendulum. In order to visualize the equation, I used matplotlib to graph the dynamics (derivative) of the equation at every point in a certain range.

- looked at representations of a state space, found phase space
	- apply state space prediction and plot dynamics at every point
- got gravitational constant wrong, spent a while debugging

## first fda tests
In order to

- began by researching scikit-fda python library
- after looking through documentation for a while, found the page "Conversion between FDataGrid and FDataBasis", which characterizes a basis function based on given data using a least squares calculation
- set up a testing visualization layout that shows different basis functions and different numbers of basis functions
