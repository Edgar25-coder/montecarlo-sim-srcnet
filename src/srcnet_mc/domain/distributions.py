import numpy as np

from scipy.special import gamma


def beta_parameters(
    mean,
    variance,
):

    kappa = (
        mean * (1.0 - mean) / variance
        - 1.0
    )

    alpha = mean * kappa

    beta = (1.0 - mean) * kappa

    return alpha, beta


def sample_beta(
    rng,
    mean,
    variance,
):

    alpha, beta = beta_parameters(
        mean,
        variance,
    )

    return rng.beta(alpha, beta)


def lognormal_parameters(
    mean,
    cv,
):

    sigma2 = np.log(
        1.0 + cv**2
    )

    mu = np.log(
        mean
        /
        np.sqrt(1.0 + cv**2)
    )

    return mu, np.sqrt(sigma2)


def sample_lognormal(
    rng,
    mean,
    cv,
):

    mu, sigma = lognormal_parameters(
        mean,
        cv,
    )

    return rng.lognormal(
        mean=mu,
        sigma=sigma,
    )


def weibull_scale(
    mean_lifetime,
    shape,
):

    return (
        mean_lifetime
        /
        gamma(
            1.0 + (1.0 / shape)
        )
    )


def sample_weibull(
    rng,
    mean_lifetime,
    shape,
):

    theta = weibull_scale(
        mean_lifetime,
        shape,
    )

    return (
        theta
        * rng.weibull(shape)
    )


def sample_poisson(
    rng,
    rate,
):

    return rng.poisson(rate)