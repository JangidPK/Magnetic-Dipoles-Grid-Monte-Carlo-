# Magnetic Dipole Simulation

A Monte Carlo simulation of dipolar magnetic particles on a 2D toroidal grid with real-time Pygame visualization.

The interaction energy of magnetic field $\textbf{H}$ with dipole is given by 
$$E_{DH} = - \textbf{m}_i \cdot \textbf{H}$$

The dipole dipole interaction is given by 

$$E_{DD} = \frac{\mu_0}{4\pi r_{ji}^3} \left( \textbf{m}_i\cdot \textbf{m}_j\right) - 3 (\textbf{m}_i \cdot \vec{\textbf{r}}_{ji} ) (\textbf{m}_j \cdot \vec{\textbf{r}}_{ji} ) $$

Wher $\textbf{m}_i, \textbf{m}_j$ are the dipole moments of two particles. $\textbf{r}_{ji}$ is the unit vector drawn from particle $i$ to $j$ and $r_{ji}$ is the distance.

![](assets/shot.png)


## Features

- 2D grid of magnetic particles
- Monte Carlo simulation with Metropolis criterion
- Pygame-based animation of particle motion

## Structure

- `grid.py` — Simulation logic (dipoles, energy, movement)
- `animator.py` — Visualization with Pygame
- `config.py` — Simulation parameters
- `main.py` — Entry point
- `assets/` — Folder for the images

## Requirements

- Python 3.x
- `pygame`, `numpy`

```bash
pip install pygame numpy