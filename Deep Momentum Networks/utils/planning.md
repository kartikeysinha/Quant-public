X_t(i) -> Trading signal in the range [-1, 1]
r_t_t+1(i): One-day return of asset i.  -> can be calculated using pct_change() or diff()
Ohm: Set of all M possible prediction prediction & target tuples across all N assets & T time steps.
sigma_t(i): ex-ante volatility estimate -> computed using an exponentially weighted moving std. dev. with a 60-day span on r_t_t+1(i)  -> rolling(window=60).std_dev()


We need a function that calculates the return captured by a trading rule for asset i at time t.
R(i, t)   ==   X_t(i) * (sigma_tgt / sigma_t(i)) * r_t_t+1(i)
          == At time t, for asset i:  trading signal  *  returns scaled to target volatility.
          == At time t, for asset i: trading signal [-1, 1]  *  target_vol  *  one day returns  /  ex-ante vol


We need a function that calculates average return over 'ohm':
- -1 * (1 / M) * sum_of_returns_over_ohm(R(i, t))   ==   mue_R


Need two loss functions:
- loss_mean_returns()   ==   - mue_R
- loss_sharpe()   ==   -1 * (mue_R * sqrt(252)) / ( sqrt( sum_over_ohm( R(i, t)^2 / M  - mue_R^2 ) ) )
This will help calibrate the size and position.

