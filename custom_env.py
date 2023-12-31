import gym
from gym import spaces
import numpy as np
import pygame

# Màu sắc
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)
black = (0, 0, 0)

class CustomGridEnv(gym.Env):
    def __init__(self):
        super(CustomGridEnv, self).__init__()
        self.grid_size = 5
        self.action_space = spaces.Discrete(25) 
        self.observation_space = spaces.MultiBinary(25)
        self.bs_state = np.ones((5, 5), dtype=int) 
        self.bs_load = np.full((5, 5), 0.1, dtype=float) 
        self.traffic_demand = np.full((5, 5), 1, dtype=float)  
        self.performance_metrics = {"traffic_coverage": 0, "energy_saving": 0}
        self.total_P_all_ON = np.sum(self.bs_load)  # Total power when all BSs are ON

        pygame.init()

        self.window_width = 800
        self.window_height = 600

        self.screen = pygame.display.set_mode((self.window_width, self.window_height))
        pygame.display.set_caption('Base Station Environment Visualization')


    def reset(self):
        self.bs_state = np.ones((5, 5), dtype=int)  # Reset the state of all BS to ON
        self.bs_load = np.full((5, 5), 0.1, dtype=float)  # Reset the load of all BS to 0.1
        self.performance_metrics = {"traffic_coverage": 0, "energy_saving": 0}
        return self.bs_state

    def step(self, action):
        if self.bs_state[action // 5][action % 5] == 0:
            return self.bs_state, -1, False, {}

        total_load_active_neighbors = 0
        row, col = action // 5, action % 5

        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

        active_neighbor_count = 0
        for dr, dc in directions:
            nr, nc = row + dr, col + dc
            if 0 <= nr < 5 and 0 <= nc < 5 and self.bs_state[nr][nc] == 1:
                active_neighbor_count += 1

        if active_neighbor_count == 0:
            return self.bs_state, -1, False, {}

        load_to_redistribute = self.bs_load[row][col]
        load_per_active_neighbor = load_to_redistribute / active_neighbor_count

        for dr, dc in directions:
            nr, nc = row + dr, col + dc
            if 0 <= nr < 5 and 0 <= nc < 5 and self.bs_state[nr][nc] == 1:
                self.bs_load[nr][nc] += load_per_active_neighbor

        self.bs_load[row][col] = 0 

        total_energy_before = np.sum(self.bs_load)
        self.bs_state[row][col] = 0
        total_energy_after = np.sum(self.bs_load)
        # reward = total_energy_before - total_energy_after
        reward = (np.sum(self.bs_load) - total_energy_after) - 100 * np.sum(self.bs_state)

        self.performance_metrics["traffic_coverage"] = np.sum(self.bs_load) / np.sum(self.traffic_demand) * 100
        self.performance_metrics["energy_saving"] = (self.total_P_all_ON - total_energy_after) / self.total_P_all_ON * 100

        return self.bs_state, reward, False, {"load_distribution_factor": load_per_active_neighbor}

    def render(self, mode='human'):
        # Print the state of BSs as a 5x5 matrix
        print("BS matrix:")
        for row in self.bs_state:
            print(row)
        print("BS Loads:")
        for row in self.bs_load:
            print(row)
        print("Performance Metrics:")
        print("Traffic Coverage: {:.2f}%".format(self.performance_metrics["traffic_coverage"]))
        print("Energy Saving: {:.2f}%".format(self.performance_metrics["energy_saving"]))
        self.draw_environment(self.bs_state, self.bs_load)

    def draw_environment(self, bs_state, bs_load):
        # Xóa màn hình
        self.screen.fill(white)

        # Kích thước và vị trí ban đầu cho trạm BS
        bs_radius = 20
        bs_x = 100
        bs_y = 100

        font = pygame.font.Font(None, 24)

        for row in range(5):
            for col in range(5):
                bs_center = (bs_x, bs_y)
                if bs_state[row][col] == 1:
                    pygame.draw.circle(self.screen, green, bs_center, bs_radius)  # Trạm BS ON
                else:
                    pygame.draw.circle(self.screen, red, bs_center, bs_radius)  # Trạm BS OFF

                text = font.render(f'{bs_load[row][col]:.2f}', True, black)
                text_rect = text.get_rect(center=(bs_x, bs_y + bs_radius + 20))
                self.screen.blit(text, text_rect)

                bs_x += 2 * bs_radius + 50
            bs_x = 100
            bs_y += 2 * bs_radius + 50

        pygame.display.flip()


# custom_env = CustomGridEnv()
# observation = custom_env.reset()
# custom_env.render()

# pygame.time.delay(2000)


# for _ in range(1000):
#     action = custom_env.action_space.sample()
#     print(action)
#     observation, reward, done, _ = custom_env.step(action)
#     custom_env.render()
#     print(f"Reward: {reward}, Done: {done}")

#     pygame.time.delay(2000)

# pygame.quit()
