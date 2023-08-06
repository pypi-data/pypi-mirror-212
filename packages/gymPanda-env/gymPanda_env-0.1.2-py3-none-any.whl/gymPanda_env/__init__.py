from gym.envs.registration import register

register(
    id='gymPanda-v0',
    entry_point='gymPanda.envs:GymEnv_panda',
)

