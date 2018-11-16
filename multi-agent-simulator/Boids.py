from scipy.spatial import distance
import numpy as np
from numpy import random
from scipy import spatial
from sklearn import preprocessing

class Boids:
    
    def __init__(self):
        pass

    def initialize_boids(self):
        NumAgents= 300
        WorldDimension = 150

        self.all_positions = WorldDimension*(random.rand(NumAgents,2)-0.5)
        
        self._boid_velocities = np.ones((NumAgents,2))
        
        self._boid_velocities = preprocessing.normalize(self._boid_velocities, norm='l2')

        zone_of_repulsion_width = 5
        zone_of_orientation_width = 5
        zone_of_attraction_width = 5

        self._zor_max = zone_of_repulsion_width
        self._zoo_min = self._zor_max
        self._zoo_max = self._zoo_min+zone_of_orientation_width
        self._zoa_min = self._zoo_max
        self._zoa_max = self._zoa_min+zone_of_attraction_width

        self.tau = 1
        
    # TODO add stochastic effect, rotating it by angle taken at random from Gaussian distribution
    # With standard deviation sigma

    def update_boids(self):
        all_distances = spatial.distance_matrix(self.all_positions,self.all_positions)
        new_velocity = np.copy(self._boid_velocities)

        for i, boid_position in enumerate(self.all_positions):
            distances = all_distances[i,:]
            v1 = self._attraction_rule(boid_position,distances)
            v2 = self._repulsion_rule(boid_position,distances,i)
            v3 = self._orientation_rule(boid_position,distances)
            v1 = np.multiply(self.tau,v1)
            v2 = np.multiply(self.tau,v2)
            v3 = np.multiply(self.tau*30,v3)
            
            vfinal = np.add(v1, v2)
            vfinal = np.add(vfinal,v3)
            jitter = random.rand(1,2)*10
            vfinal = np.add(vfinal,jitter) 
            new_velocity[i] = vfinal
        
        normalize_new_velocity = new_velocity
        normalize_new_velocity = preprocessing.normalize(new_velocity, norm='l2')        
        self.all_positions += normalize_new_velocity
        self._boid_velocities = normalize_new_velocity
        return self.all_positions

    def _attraction_rule(self, boid_position, distances):
        attraction_neighbors = np.where((distances > self._zoa_min) & (distances <= self._zoa_max),1,0)
        attraction_neighbors_indices = np.where(attraction_neighbors)[0]
        if (len(attraction_neighbors_indices) != 0):
            attraction_neighbors = np.take(self.all_positions, attraction_neighbors_indices, axis=0)
            center_of_mass = np.mean(attraction_neighbors,axis=0)
            v1 = center_of_mass-boid_position
            return v1
        else:
            return [0,0]

    def _repulsion_rule(self, boid_position, distances,i):
        repulsion_neighbors = np.where((distances <= self._zor_max),1,0)
        repulsion_neighbors_indices = np.where(repulsion_neighbors)[0]
        if (len(repulsion_neighbors_indices) != 0):
            repulsion_neighbors = np.take(self.all_positions, repulsion_neighbors_indices, axis=0)
            center_of_mass = np.mean(repulsion_neighbors,axis=0)
            v1 = center_of_mass-boid_position
            return -v1
        else:
            return [0,0]

    def _orientation_rule(self, boid_position, distances):
        orientation_neighbors = np.where((distances > self._zoo_min) & (distances <= self._zoo_max),1,0)
        on_indices = np.where(orientation_neighbors)[0]
        if (len(on_indices) != 0):
            orientation_neighbors = np.take(self._boid_velocities,on_indices, axis=0)
            average_velocity = np.mean(orientation_neighbors,axis=0)
            return average_velocity
        else:
            return [0,0]


if __name__ == '__main__':
    boids = Boids()
    boids.initialize_boids()
    boids.update_boids()
    boids.update_boids()

