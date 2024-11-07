import numpy as np
import pandas as pd


def bayesian_comparison(df, metric_name, metric_mean, metric_numerator, metric_denominator):
    # Initialize lists to store results
    results = []

    # Separate control from other buckets
    control = df[df['bucket'] == 'control']
    treatment_buckets = df['bucket'].unique()
    treatment_buckets = treatment_buckets[treatment_buckets != 'control']

    # Ensure control is not empty before proceeding
    if not control.empty:
        control_metric = control[metric_mean].values[0]

        # Compare control vs control (bucket 'control' vs 'control')
        results.append({
            'metric_name': metric_name,
            'bucket': 'control',
            'control_numerator': control[metric_numerator].iloc[0],
            'control_denominator': control[metric_denominator].iloc[0],
            'treatment_numerator': control[metric_numerator].iloc[0],
            'treatment_denominator': control[metric_denominator].iloc[0],
            'control_metric': control_metric,
            'treatment_metric': control_metric,
            'treatment_posterior_mean': 0,
            'control_posterior_mean': 0,
            'relative_change_mean': 0.0,
            'chance_to_win': 0.5,
            '95%_CI_lower': 0.0,
            '95%_CI_upper': 0.0
        })

        # Iterate over treatment buckets
        for bucket in treatment_buckets:
            treatment_bucket_df = df[df['bucket'] == bucket]
            treatment_metric = treatment_bucket_df[metric_mean].values[0] if not treatment_bucket_df.empty else np.nan
            treatment_numerator = treatment_bucket_df[metric_numerator].values[
                0] if not treatment_bucket_df.empty else np.nan
            treatment_denominator = treatment_bucket_df[metric_denominator].values[
                0] if not treatment_bucket_df.empty else np.nan

            # Prior parameters (using non-informative priors)
            alpha_prior, beta_prior = 1, 1

            # Control posterior parameters
            alpha_control = alpha_prior + control[metric_numerator].iloc[0]
            beta_control = beta_prior + (control[metric_denominator].iloc[0] - control[metric_numerator].iloc[
                0])  # Failures (total - retained)

            # Treatment posterior parameters
            alpha_treatment = alpha_prior + treatment_numerator
            beta_treatment = beta_prior + (treatment_denominator - treatment_numerator)

            # Simulate from the posterior distributions
            control_posterior_samples = np.random.beta(alpha_control, beta_control, 10000)
            treatment_posterior_samples = np.random.beta(alpha_treatment, beta_treatment, 10000)

            # Calculate relative change
            relative_change = (treatment_posterior_samples - control_posterior_samples) / control_posterior_samples

            treatment_posterior_mean = treatment_posterior_samples.mean()
            control_posterior_mean = control_posterior_samples.mean()

            # Calculate chance to win
            chance_to_win = (treatment_posterior_samples > control_posterior_samples).mean()

            # Calculate 95% credible interval
            lower_bound = np.percentile(relative_change, 2.5)
            upper_bound = np.percentile(relative_change, 97.5)

            # Store results
            results.append({
                'metric_name': metric_name,
                'bucket': bucket,
                'control_numerator': control[metric_numerator].iloc[0],
                'control_denominator': control[metric_denominator].iloc[0],
                'treatment_numerator': treatment_numerator,
                'treatment_denominator': treatment_denominator,
                'control_metric': control_metric,
                'treatment_metric': treatment_metric,
                'treatment_posterior_mean': treatment_posterior_mean,
                'control_posterior_mean': control_posterior_mean,
                'relative_change_mean': relative_change.mean(),
                'chance_to_win': chance_to_win,
                '95%_CI_lower': lower_bound,
                '95%_CI_upper': upper_bound
            })

    # Convert results to a DataFrame
    results_df = pd.DataFrame(results)
    return results_df


# Assuming df is your data, call the function and display the result
# df = cells.bp
# metric_name = 'm1_retention'
# metric_mean = 'retention_rate_confirmed'
# metric_numerator = 'activity_confirmed'
# metric_denominator = 'cohort'
# results_df = bayesian_comparison(df, metric_name, metric_mean, metric_numerator, metric_denominator)
# results_df.sort_values(['bucket'])
#
# results_df
