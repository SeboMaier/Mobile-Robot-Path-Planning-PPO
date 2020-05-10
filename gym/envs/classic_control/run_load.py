import gym
from stable_baselines.common.policies import MlpPolicy
from stable_baselines.gail import generate_expert_traj, ExpertDataset
from stable_baselines.common.vec_env import VecNormalize, DummyVecEnv
from stable_baselines.common import set_global_seeds, make_vec_env, vec_env
from stable_baselines import PPO2

LOAD_TO_TRAIN = False

if __name__ == '__main__':
    env_id = "Simulation-v0"

    # Create the vectorized environment

    #env = SubprocVecEnv([make_env(env_id, i) for i in range(num_cpu)])
    # Stable Baselines provides you with make_vec_env() helper
    # which does exactly the previous steps for you:
    model = PPO2.load("PPO2_10k_1")
    venv = DummyVecEnv([lambda: gym.make("Simulation-v0")])
    nvenv = VecNormalize(venv, norm_obs=True, norm_reward=False)
    model.set_env(nvenv)

    model.learn(total_timesteps=100000, tb_log_name="PPO2_110k_1")
    model.save("PPO2_110k_1")
    # model.learn(total_timesteps=5000000, tb_log_name="PPO2_5M_1")
    # model.save("PPO2_5M_1")
    # model.learn(total_timesteps=5000000, tb_log_name="PPO2_10M_2")
    # model.save("PPO2_10M_2")
    # model.learn(total_timesteps=5000000, tb_log_name="PPO2_15M_3")
    # model.save("PPO2_15M_3")
    # model.learn(total_timesteps=5000000, tb_log_name="PPO2_20M_4")
    # model.save("PPO2_20M_4")
    # model.learn(total_timesteps=5000000, tb_log_name="PPO2_25M_5")
    # model.save("PPO2_25M_5_5")
    # model.learn(total_timesteps=5000000, tb_log_name="PPO2_30M_5")
    # model.save("PPO2_30M_5")
    # model.learn(total_timesteps=5000000, tb_log_name="PPO2_35M_5")
    # model.save("PPO2_35M_5")
    # model.learn(total_timesteps=5000000, tb_log_name="PPO2_40M_5")
    # model.save("PPO2_40M_5")
    # model.learn(total_timesteps=5000000, tb_log_name="PPO2_45M_5")
    # model.save("PPO2_45M_5")
    # model.learn(total_timesteps=5000000, tb_log_name="PPO2_50M_5")
    # model.save("PPO2_50M_5")


    # tensorboard --logdir=logs --host localhost --port 8088
    # http://localhost:8088/
