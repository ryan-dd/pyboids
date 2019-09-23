# pyboids
This purpose of this project is to simulate flock and swarm behavior with agents.
It is based on boids.
Agents have attraction, repulsion, and orientation behavior based on their local state.
There are other branches of this repo with variations on the boids model.

## Getting Started

Run the simulation by running:
```bash
python -m pyboids.simulation
```

Change these parameters in boids_model.py for interesting things to happen:
```python
zone_of_repulsion_width

zone_of_orientation_width

zone_of_attraction_width
```
### Requirements
SciPy

Scikit-learn

NumPy

PyQtgraph

## License

MIT © Ryan Day
