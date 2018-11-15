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
        NumAgents= 200
        WorldDimension = 20

        # Matrix of size NumAgentsx2 giving x and y positions of the NumAgents
        # between - WorldDimension/2 and WorldDimension/2
        self.all_positions = WorldDimension*(random.rand(NumAgents,2)-0.5)
        # Matrix of size NumAgentsx2 giving an orientation for each agent with
        # an initial value of a vector between [-1, -1] and [1, 1]
        self._all_agent_vectors = 2*(random.rand(NumAgents,2)-0.5)

        zone_of_repulsion_width = 1
        zone_of_orientation_width = 3
        zone_of_attraction_width = 30

        self._zor_max = zone_of_repulsion_width
        self._zoo_min = self._zor_max
        self._zoo_max = self._zoo_min+zone_of_orientation_width
        self._zoa_min = self._zoo_max
        self._zoa_max = self._zoa_min+zone_of_attraction_width

        # Max angle of rotation for agent
        self.theta = np.pi/4

    # TODO add stochastic effect, rotating it by angle taken at random from Gaussian distribution
    # With standard deviation sigma

    def update_flock_2d(self):
        # Matrix giving all pairwise distances between agents
        distance_matrix = spatial.distance_matrix(self.all_positions,self.all_positions)
        # Initialize a vector that will contain updated agent orientations
        updated_agent_vectors = np.zeros((len(self._all_agent_vectors),2))

        for i, distances_for_agent_i in enumerate(distance_matrix):
            # TODO If neighbors are in blind spot, exclude them from all calculations
            repulsion_neighbors = distances_for_agent_i <= self._zor_max

            # Don't include distance to itself in dr calculations
            repulsion_neighbors[i] = False

            repulsion_neighbor_indices = np.where(repulsion_neighbors)[0]
            # If there are any repulsion neighbors, set orientation accordingly
            if (len(repulsion_neighbor_indices) != 0):
                # Determine the net direction of repulsion and turn toward it
                dr = -self._find_d(self.all_positions,repulsion_neighbor_indices,i)
                agent_vector = np.copy(self._all_agent_vectors[i])
                self._update_agent_vector(dr,agent_vector)
            # Otherwise base orientation on attraction and orientation neighbors
            else:
                use_do = False # True if there are any orientation neighbors
                use_da = False # True if there are any attraction neighbors
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
                    agent_vector = np.copy(self._all_agent_vectors[i])
                    updated_agent_vector = self._update_agent_vector(dfinal,agent_vector)
                    updated_agent_vectors[i] = updated_agent_vector
        # Move agents forward in the direction of their orientation by a magnitude of one
        self._all_agent_vectors = updated_agent_vectors
        self._update_positions()
        return self.all_positions

    def _update_agent_vector(self,dfinal,agent_vector):
        # Find angle between vectors and rotate it in the right direction
        angle = self._angle_between(agent_vector,dfinal)
        if np.abs(angle) < self.theta:
            agent_vector = dfinal
        else:
            """ It encountered an invalid angle """
            agent_vector = self._rotate(agent_vector,np.sign(angle)*self.theta)
        return agent_vector

    def _angle_between(self, A, B):
        # Returns a value between [-pi, pi] of the angle from A to B
        # return np.arccos(np.clip(np.dot(v1, v2), -1.0, 1.0))
        # return np.arccos(A.dot(B)/(np.linalg.norm(A)*np.linalg.norm(B)))
        return np.arctan2(B[1],B[0]) - np.arctan2(A[1],A[0])

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
        rij_normalized = (rij)/linalg.norm(rij)
        # Normalize it again? not sure about this one.
        normalized_vectors = rij_normalized/linalg.norm(rij_normalized)
        return np.sum(normalized_vectors,axis=0)

    def _find_do(self, vectors, indices):
        # Equation 2 in couzin paper
        agent_vectors = np.take(vectors,indices, axis=0)
        """It's running into an issue where it's not allowing division"""
        normalized_vectors = agent_vectors/linalg.norm(agent_vectors)
        return np.sum(normalized_vectors,axis=0)

    def _update_positions(self):
        self.all_positions += self._all_agent_vectors



if __name__ == '__main__':
    generator = DataGenerator()
    generator.initialize_flock_dynamic_2d()
    generator.update_flock_2d()
    generator.update_flock_2d()
