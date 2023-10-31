from env.custom_env import CustomGridEnv
import gym
from gym import spaces
import numpy as np
import pygame

custom_env = CustomGridEnv()
observation = custom_env.reset()
custom_env.render()

pygame.time.delay(2000)

# for _ in range(custom_env.action_space.n):  # Lặp qua tất cả các giá trị trong không gian hành động
#     action_sample = custom_env.action_space.sample()
#     print(action_sample)


for _ in range(10):
    action = custom_env.action_space.sample()
    print(action)
    observation, reward, done, _ = custom_env.step(action)
    custom_env.render()
    print(f"Reward: {reward}, Done: {done}")

    pygame.time.delay(2000)

pygame.quit()