from scipy.spatial import distance
import numpy as np
from numpy import random
from scipy import spatial
from sklearn import preprocessing

class Boids:

    def __init__(self):
        pass

    def initialize_boids(self):
        NumAgents= 200
        WorldDimension = 12

        # NumAgents x 2 matrix to hold all x and y positions of agents, which
        # are initialized between -WorldDimension/2 and WorldDimension/2
        self.all_positions = WorldDimension*(random.rand(NumAgents,2)-0.5)

        # Velocity in x and y, replacing the old orientation matrix
        self._boid_velocities = np.ones((NumAgents,2))*-1
        #self._boid_velocities = (random.rand(NumAgents,2)-0.5)
        # Normalize the velocity vectors using least squares normalization
        self._boid_velocities = preprocessing.normalize(self._boid_velocities, norm='l2')

        zone_of_repulsion_width = 1
        zone_of_orientation_width = 0.1
        zone_of_attraction_width = 5
        self.tau = 1 # time step
        self.limit_angle = np.pi/4 # maximum turn angle

        self._zor_max = zone_of_repulsion_width
        self._zoo_min = self._zor_max
        self._zoo_max = self._zoo_min+zone_of_orientation_width
        self._zoa_min = self._zoo_max
        self._zoa_max = self._zoa_min+zone_of_attraction_width



    def update_boids(self):
        # Matrix giving all pairwise distances between agents
        all_distances = spatial.distance_matrix(self.all_positions,self.all_positions)
        # Initialize a vector that will contain updated agent orientations
        new_velocity = np.copy(self._boid_velocities)

        for i, boid_position in enumerate(self.all_positions):
            if i < 100:
                vfinal = preprocessing.normalize(np.ones((1,2)), norm='l2')
                vfinal = self._limit_vector(vfinal[0], self._boid_velocities[i])
                new_velocity[i] = vfinal
            else:
                # Update velocity for agent i
                distances = all_distances[i,:]

                # This appears to be unused
                agents_to_ignore = self._find_ignore_neighbors(boid_position,i)

                # Find velocity vectors for each of the formation rules
                v1 = self._attraction_rule(boid_position,distances)
                v2 = self._repulsion_rule(boid_position,distances,i)
                v3 = self._orientation_rule(boid_position,distances)
                # Scale all velocities by the time step
                v1 = np.multiply(self.tau,v1)
                v2 = np.multiply(self.tau,v2)
                v3 = np.multiply(self.tau,v3)

                # Find the total resultant velocity vector
                vfinal = np.add(v1, v2)
                vfinal = np.add(vfinal,v3)
                jitter = (random.rand(1,2)-0.5) # between 0.5 and 1.5
                vfinal = np.add(vfinal,jitter)
                vfinal = preprocessing.normalize(vfinal, norm='l2')
                vfinal = self._limit_vector(vfinal[0], self._boid_velocities[i])
                new_velocity[i] = vfinal

        normalize_new_velocity = preprocessing.normalize(new_velocity, norm='l2')
        self.all_positions += normalize_new_velocity*self.tau # update positions
        self._boid_velocities = normalize_new_velocity # Store velocities for next iteration
        return self.all_positions

    def _limit_vector(self, vfinal, v_agent_i):
        angle = self._angle_between(vfinal,v_agent_i) # Included angle of velocity vectors
        angle = self._get_smaller_complement(angle) # Normalizes angle to [-pi, pi]
        # Limit the turn by the minimum turn angle
        if np.abs(angle) < self.limit_angle:
            return vfinal
        else:
            return self._rotate(v_agent_i,np.sign(angle)*self.limit_angle)

    def _get_smaller_complement(self, angle):
        if angle >= 0:
            angle2 = 2*np.pi - angle
        else:
            angle2 = 2*np.pi + angle
        if (abs(angle) < abs(angle2)):
            return angle
        else:
            return angle2

    def _angle_between(self,vfinal,voriginal):
        # Returns a value between [-2pi, 2pi] of the angle from voriginal to vfinal
        angle = np.arctan2(vfinal[1],vfinal[0]) - np.arctan2(voriginal[1],voriginal[0])
        return angle

    def _rotate(self, vector, theta):
        c, s = np.cos(theta), np.sin(theta)
        R = np.array([[c,-s], [s, c]])
        return (R.dot(vector))

    def _find_ignore_neighbors(self, boid_position, i):
        other_agent_vectors = preprocessing.normalize(self.all_positions - boid_position, norm='l2')
        angles = np.dot(other_agent_vectors,self._boid_velocities[i])
        angle_constant = 0.9
        ignore_neighbor_indices = np.where((angles < angle_constant) & (angles > -angle_constant),1,0)
        pass

    def _attraction_rule(self, boid_position, distances):
        attraction_neighbors = np.where((distances > self._zoa_min) & (distances <= self._zoa_max),1,0)
        attraction_neighbors_indices = np.where(attraction_neighbors)[0]
        if (len(attraction_neighbors_indices) != 0):
            attraction_neighbors = np.take(self.all_positions, attraction_neighbors_indices, axis=0)
            #attraction_neighbors = preprocessing.normalize(attraction_neighbors)
            center_of_mass = np.mean( attraction_neighbors,axis=0)
            v1 = center_of_mass-boid_position
            return v1
        else:
            return [0,0]

    def _repulsion_rule(self, boid_position, distances,i):
        repulsion_neighbors = np.where((distances <= self._zor_max),1,0)
        repulsion_neighbors_indices = np.where(repulsion_neighbors)[0]
        repulsion_neighbors[i] = False
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

    def _test_rotate(self):
        angle = np.pi/4
        vector = (1,0)
        rotated_vector = self._rotate(vector,angle)
        print(rotated_vector)

    def _test_compliment(self):
        ang = 6
        smallest_compliment = self._get_smaller_complement(ang)
        print(smallest_compliment)
        print(ang+smallest_compliment)

    def _test_limit(self):
        v1 = [0,1]
        v2 = [-1,0]
        #vfinal, vagenti
        v1limited = self._limit_vector(v1, v2)
        print(v1limited)



if __name__ == '__main__':
    boids = Boids()
    boids.initialize_boids()
    # boids._test_compliment()
    boids._test_limit()

    # vfinal = np.array([0.0,-1.0])
    # voriginal = np.array([1.0,0.0])

    # angle = boids._angle_between(vfinal,voriginal)
    # angle_final = boids._get_smaller_complement(angle)

    # boids._limit_vector(vfinal, voriginal)

    # vfinal = np.array([[0.0,-1.0]])
    # voriginal = np.array([[1.0,0.0]])
    # boids._limit_vector(vfinal, voriginal)
