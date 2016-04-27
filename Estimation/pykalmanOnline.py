import numpy as np
import matplotlib.pyplot as pk
from pykalman.datasets import load_robot
from pykalman import KalmanFilter

# Initialize the Kalman Filter
data = load_robot()
kf = KalmanFilter(
    data.transition_matrix,
    data.observation_matrix,
    data.initial_transition_covariance,
    data.initial_observation_covariance,
    data.transition_offsets,
    data.observation_offset,
    data.initial_state_mean,
    data.initial_state_covariance,
    random_state=0
)

# Estimate mean and covariance of hidden state distribution iteratively.  This
# is equivalent to
#
#   >>> (filter_state_means, filtered_state_covariance) = kf.filter(data)
n_timesteps = data.observations.shape[0]
n_dim_state = data.transition_matrix.shape[0]
filtered_state_means = np.zeros((n_timesteps, n_dim_state))
filtered_state_covariances = np.zeros((n_timesteps, n_dim_state, n_dim_state))
for t in range(n_timesteps - 1):
    if t == 0:
        filtered_state_means[t] = data.initial_state_mean
        filtered_state_covariances[t] = data.initial_state_covariance
    filtered_state_means[t + 1], filtered_state_covariances[t + 1] = (
        kf.filter_update(
            filtered_state_means[t],
            filtered_state_covariances[t],
            data.observations[t + 1],
            transition_offset=data.transition_offsets[t],
        )
    )

# draw estimates
pk.figure()
lines_true = pk.plot(data.states, color='b')
lines_filt = pk.plot(filtered_state_means, color='r')
pk.legend((lines_true[0], lines_filt[0]), ('true', 'filtered'))
pk.show()