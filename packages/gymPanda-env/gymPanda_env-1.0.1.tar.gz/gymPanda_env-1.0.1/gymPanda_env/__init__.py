from gym.envs.registration import register

register(
    id='panda',
    entry_point='gymPanda_env.envs:GymEnv_panda',
)

