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

    def flock_dynamic(self):
        NumAgents= 10
        WorldDimension = 20
        
        all_positions = WorldDimension*(random.rand(NumAgents,2)-0.5)
        all_agent_vectors = 2*(random.rand(NumAgents,2)-0.5)

        zone_of_repulsion_width = 2
        zone_of_orientation_width = 1
        zone_of_attraction_width = 2

        zor_max = zone_of_repulsion_width
        zoo_min = zor_max
        zoo_max = zoo_min+zone_of_orientation_width
        zoa_min = zoo_max
        zoa_max = zoa_min+zone_of_attraction_width

        self.theta = np.pi/8

        distance_matrix = spatial.distance_matrix(all_positions,all_positions)
        
        for i, distances_for_agent_i in enumerate(distance_matrix):             
            repulsion_neighbors = distances_for_agent_i <= zor_max
            repulsion_neighbors[i] = False
            # TODO If neighbors are in blind spot, make their indice false right here       
            repulsion_neighbor_indices = np.where(repulsion_neighbors)[0]
            if (len(repulsion_neighbor_indices) != 0):
                dr = -self.find_d(all_positions,repulsion_neighbor_indices,i)
                self.update_agent_vector(dr,i)
            else:    
                use_do = False
                use_da = False

                attraction_neighbors = np.where((distances_for_agent_i > zoa_min) & (distances_for_agent_i <= zoa_max),1,0)
                an_indices = np.where(attraction_neighbors)[0]                
                if (len(an_indices) != 0):
                    use_da = True
                    da = self.find_d(all_positions,an_indices,i)
                
                orientation_neighbors = np.where((distances_for_agent_i > zoo_min) & (distances_for_agent_i <= zoo_max),1,0)
                on_indices = np.where(orientation_neighbors)[0]
                if (len(on_indices) != 0):
                    use_do = True
                    do = self.find_do(all_agent_vectors,on_indices)
                
                if use_do and use_da:
                    dfinal = 0.5*da+0.5*do
                elif use_da:
                    dfinal = da
                elif use_do:
                    dfinal = do
                else:
                    dfinal = [0,0]
                if not np.array_equal(dfinal, np.array([0,0])):
                    self.update_agent_vector(dfinal,all_agent_vectors[i])
                    # Find angle and rotate it in the right direction
    
    def update_agent_vector(self,dfinal,agent_vector):
        angle = self.angle_between(agent_vector,dfinal)
        if angle < self.theta:
            agent_vector = dfinal
        else:
            agent_vector = self.rotate(agent_vector,np.sign(angle)*self.theta)
            pass

    def angle_between(self, v1, v2):
        return np.arccos(np.clip(np.dot(v1, v2), -1.0, 1.0))

    def find_d(self, position, indices, i):
        # equation 1 and 3 in couzin paper
        # Get agent positions
        agents = np.take(position, indices, axis=0)
        # Calulate Vectors of agent to all other agents
        rij = agents - position[i]
        # Normalize everything
        vectors = (rij)/linalg.norm(rij)
        normalized_vectors = vectors/linalg.norm(vectors)
        return np.sum(normalized_vectors,axis=0)

    def find_do(self, vectors, indices):
        # equation 2 in couzin paper
        agent_vectors = np.take(vectors,indices, axis=0)
        normalized_vectors = agent_vectors/linalg.norm(agent_vectors)
        return np.sum(normalized_vectors,axis=0)

    def rotate(self, vector, theta):
        c, s = np.cos(theta), np.sin(theta)
        R = np.array(((c,-s), (s, c)))
        return (R.dot(vector))



        # Other calculation - sum all orientation vectors, 
        # sum all attraction vectors, and then if either are zero
        # then just use the other one otherwise use the average of both
        # If this results in zero vector or no individuals detected, use old vector

        # Stochastic effect is rotating it by angle taken at random from Gaussian distribution
        # With standard deviation sigma

        #They then turn with turning rate theta towards desired direction. 
        # Assume each agent acts as constant speed

if __name__ == '__main__':
    generator = DataGenerator()
    generator.flock_dynamic()