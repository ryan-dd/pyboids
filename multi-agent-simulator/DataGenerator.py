import numpy as np
from numpy import random
from scipy import spatial
from scipy.spatial import distance
from numpy import linalg

class DataGenerator:

    def __init__(self):
        pass

    @staticmethod
    def random_3d_data():
        NumAgents=10
        WorldDimension = 100
        data = []
        for _ in range(1000):
            data.append(WorldDimension*(random.rand(NumAgents,3)-0.5))
        return data

    @staticmethod
    def random_2d_data():
        NumAgents=10
        WorldDimension = 100
        data = []
        for _ in range(1000):
            data.append(WorldDimension*(random.rand(2, NumAgents)-0.5))
        return data

    def initialize_flock_dynamic_2d(self):
        NumAgents= 10
        WorldDimension = 20
        
        self.all_positions = WorldDimension*(random.rand(NumAgents,2)-0.5)
        self._all_agent_vectors = 2*(random.rand(NumAgents,2)-0.5)

        zone_of_repulsion_width = 2
        zone_of_orientation_width = 1
        zone_of_attraction_width = 2

        self._zor_max = zone_of_repulsion_width
        self._zoo_min = self._zor_max
        self._zoo_max = self._zoo_min+zone_of_orientation_width
        self._zoa_min = self._zoo_max
        self._zoa_max = self._zoa_min+zone_of_attraction_width

        # Max angle of rotation for agent
        self.theta = np.pi/8

    # TODO add stochastic effect, rotating it by angle taken at random from Gaussian distribution
    # With standard deviation sigma

    def update_flock_2d(self):     
        distance_matrix = spatial.distance_matrix(self.all_positions,self.all_positions)
        updated_agent_vectors = np.zeros((len(self._all_agent_vectors),2))

        for i, distances_for_agent_i in enumerate(distance_matrix): 
            # TODO If neighbors are in blind spot, exclude them from all calculations                  
            repulsion_neighbors = distances_for_agent_i <= self._zor_max
  
            # Don't include distance to itself in dr calculations
            repulsion_neighbors[i] = False

            repulsion_neighbor_indices = np.where(repulsion_neighbors)[0]
            if (len(repulsion_neighbor_indices) != 0):
                dr = -self._find_d(self.all_positions,repulsion_neighbor_indices,i)
                agent_vector = self._all_agent_vectors[i]
                self._update_agent_vector(dr,agent_vector)
            else:    
                use_do = False
                use_da = False
                attraction_neighbors = np.where((distances_for_agent_i > self._zoa_min) & (distances_for_agent_i <= self._zoa_max),1,0)
                an_indices = np.where(attraction_neighbors)[0]                
                if (len(an_indices) != 0):
                    use_da = True
                    da = self._find_d(self.all_positions,an_indices,i)
                
                orientation_neighbors = np.where((distances_for_agent_i > self._zoo_min) & (distances_for_agent_i <= self._zoo_max),1,0)
                on_indices = np.where(orientation_neighbors)[0]
                if (len(on_indices) != 0):
                    use_do = True
                    do = self._find_do(self._all_agent_vectors,on_indices)
               
                if use_do and use_da:
                    dfinal = 0.5*da+0.5*do
                elif use_da:
                    dfinal = da
                elif use_do:
                    dfinal = do
                else:
                    dfinal = [0,0]
                # If dfinal is 0 vector or no neighbors detected, leave the agent vector the same
                if np.array_equal(dfinal, [0,0]):
                    updated_agent_vectors[i] = self._all_agent_vectors[i]
                else:
                    agent_vector = self._all_agent_vectors[i]
                    updated_agent_vector = self._update_agent_vector(dfinal,agent_vector)
                    updated_agent_vectors[i] = updated_agent_vector
        self._all_agent_vectors = updated_agent_vectors
        self._update_positions()
        return self.all_positions

    def _update_agent_vector(self,dfinal,agent_vector):
        # Find angle between vectors and rotate it in the right direction
        angle = self._angle_between(agent_vector,dfinal)
        if angle < self.theta:
            agent_vector = dfinal
        else:
            agent_vector = self._rotate(agent_vector,np.sign(angle)*self.theta)
        return agent_vector

    def _angle_between(self, v1, v2):
        return np.arccos(np.clip(np.dot(v1, v2), -1.0, 1.0))
    
    def _rotate(self, vector, theta):
        c, s = np.cos(theta), np.sin(theta)
        R = np.array(((c,-s), (s, c)))
        return (R.dot(vector))

    def _find_d(self, position, indices, i):
        # Equation 1 and 3 in couzin paper
        # Get relevant neighbor agent positions
        agents = np.take(position, indices, axis=0)
        # Calulate Vectors of agent to all other agents
        rij = agents - position[i]
        # Normalize everything
        vectors = (rij)/linalg.norm(rij)
        # Normalize it again? not sure about this one.
        normalized_vectors = vectors/linalg.norm(vectors)
        return np.sum(normalized_vectors,axis=0)

    def _find_do(self, vectors, indices):
        # Equation 2 in couzin paper
        agent_vectors = np.take(vectors,indices, axis=0)
        normalized_vectors = agent_vectors/linalg.norm(agent_vectors)
        return np.sum(normalized_vectors,axis=0)

    def _update_positions(self):
        self.all_positions += self._all_agent_vectors

    
       
if __name__ == '__main__':
    generator = DataGenerator()
    generator.initialize_flock_dynamic()
    generator.update_flock()
    generator.update_flock()