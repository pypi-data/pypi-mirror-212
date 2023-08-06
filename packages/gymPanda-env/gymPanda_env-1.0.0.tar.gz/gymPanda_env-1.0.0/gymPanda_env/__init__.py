from gym.envs.registration import register

register(
    id='gymPanda-v0',
    entry_point='gymPanda_env.envs:GymEnv_panda',
)

