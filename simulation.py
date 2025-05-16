# grid.py

import numpy as np
from config import N_ATOMS, GRID_WIDTH, GRID_HEIGHT, TEMPERATURE, H

class GridSetup:
    def __init__(self):
        self.n_atoms = N_ATOMS
        self.H = H
        self.total_energy = 0
        self.n_gridx = GRID_WIDTH
        self.n_gridy = GRID_HEIGHT
        self.pos = []
        self.dipole = []
        self.grid = np.ones((self.n_gridx, self.n_gridy), dtype=int) * (-1)
        self.moves = [(1, 0),  # East
                      (1, -1), # Southeast
                      (0, -1), # South
                      (-1,-1), # Southwest
                      (-1, 0), # West
                      (-1, 1), # Northwest
                      (0, 1),  # North
                      (1, 1)   # Northeast
                      ] 
        
        np.random.seed(24)
        self._prepare()

    def _prepare(self):
        for atom_id in range(self.n_atoms):
            while True:
                x, y = np.random.randint(0, self.n_gridx), np.random.randint(0, self.n_gridy)
                if (x, y) not in self.pos:
                    self.pos.append((x, y))
                    dipol_x = np.random.randint(-1, 2)
                    dipol_y = np.sqrt(1 - dipol_x**2)
                    self.dipole.append((dipol_x, dipol_y))
                    self.grid[x, y] = atom_id
                    break

    def calculate_energy(self, atom_id):

        # Define the relative positions of the neighbors
        sq2 = np.sqrt(2)
        rxy = [(1, 0), (1, -1), (0, -1), (-1,-1), (-1, 0), (-1, 1), (0, 1), (1, 1)]
        # rxy = [(1, 0), (1/sq2, -1/sq2), (0, -1), (-1/sq2,-1/sq2), (-1, 0), (-1/sq2, 1/sq2), (0, 1), (1/sq2, 1/sq2)]
        n_neigh = len(rxy)

        # Calculate energy for the atom at atom_id
        energy = 0
        for neigh in range(n_neigh):
            nx = (self.pos[atom_id][0] + rxy[neigh][0]) % self.n_gridx
            ny = (self.pos[atom_id][1] + rxy[neigh][1]) % self.n_gridy
            neigh_id = self.grid[nx, ny]

            if neigh_id != -1:

                pos_vec = rxy[neigh]
                distance = np.sqrt(pos_vec[0]**2 + pos_vec[1]**2)
                pos_vec /= distance

                dip_self = self.dipole[atom_id]
                dip_neigh = self.dipole[neigh_id]

                term1 = dip_self[0]*dip_neigh[0] + dip_self[1]*dip_neigh[1]
                term2 = dip_self[0]*pos_vec[0] + dip_self[1]*pos_vec[1]
                term3 = dip_neigh[0]*pos_vec[0] + dip_neigh[1]*pos_vec[1]
                energy += (term1 - 3 * (term2 * term3)) / distance**3

        return energy

    def rotate(self):
        atom_id = np.random.randint(self.n_atoms)
        
        dipole = self.dipole[atom_id]

        magnetic_energy_before = -(dipole[0]* self.H[0] + dipole[1]* self.H[1])        
        
        # Rotate the dipole moment by angle rotate_by on the xy plane
        rotate_by = (1-2*np.random.random())* (np.pi/16)
        new_dipole = (dipole[0] * np.cos(rotate_by) - dipole[1] * np.sin(rotate_by),
                      dipole[0] * np.sin(rotate_by) + dipole[1] * np.cos(rotate_by))
        
        self.dipole[atom_id] = new_dipole
        magnetic_energy_after =  - (self.dipole[atom_id][0]* self.H[0] + 
                                     self.dipole[atom_id][1]* self.H[1]) 
        
        delta_E = magnetic_energy_after - magnetic_energy_before


        if np.exp(-delta_E / TEMPERATURE) < np.random.rand():
            # Revert rotation
            self.dipole[atom_id] = dipole
        else:
            self.total_energy += delta_E



    def move(self):
        while True:
            atom_id = np.random.randint(self.n_atoms)
            empty_neigh = []
            for i, (dx, dy) in enumerate(self.moves):
                nx = (self.pos[atom_id][0] + dx) % self.n_gridx
                ny = (self.pos[atom_id][1] + dy) % self.n_gridy
                if self.grid[nx, ny] == -1:
                    empty_neigh.append(i)

            if empty_neigh:
                break

        direction = np.random.choice(empty_neigh)
        rev_dir = (direction + 4) % 8
        cur_x, cur_y = self.pos[atom_id]
        new_x = (cur_x + self.moves[direction][0]) % self.n_gridx
        new_y = (cur_y + self.moves[direction][1]) % self.n_gridy

        energy_before = self.calculate_energy(atom_id)

        # Move
        self.pos[atom_id] = (new_x, new_y)
        self.grid[cur_x, cur_y] = -1
        self.grid[new_x, new_y] = atom_id

        energy_after = self.calculate_energy(atom_id)
        delta_E = energy_after - energy_before

        # if np.exp(-delta_E / TEMPERATURE) < np.random.rand():
        if delta_E > 0:
            # Revert move
            rev_x = (new_x + self.moves[rev_dir][0]) % self.n_gridx
            rev_y = (new_y + self.moves[rev_dir][1]) % self.n_gridy
            self.pos[atom_id] = (rev_x, rev_y)
            self.grid[new_x, new_y] = -1
            self.grid[rev_x, rev_y] = atom_id
        else:
            self.total_energy += delta_E
