"""
Geodemographic Subcluster Integration
======================================
Assigns each agent a geodemographic subcluster and adjusts their NTS-derived
trip probabilities using cluster-level contextual priors.

Subclusters (9 total):
    1.1  Affluent Suburban Professionals
    1.2  Urban Digital Millennials
    2.1  Value-Driven Young Spenders
    2.2  Price-Sensitive Digital Shoppers
    3.1  Established Families
    3.2  Suburban Empty Nesters
    3.3  High-End Consumers
    4.1  Affluent Rural Empty Nester Consumers
    4.2  Rural Retirees

z-scores are derived from the geodemographic clustering analysis and converted
to probability priors via sigmoid(z * gamma), keeping values in (0, 1).

Assignment Modes
----------------
  TEST_MODE = True  →  random uniform draw from 9 subclusters (for development)
  TEST_MODE = False →  postcode-sector lookup (see placeholder below)

============================================================
SUBCLUSTER ASSIGNMENT — PRODUCTION MODE
------------------------------------------------------------
Replace the random assignment below with a postcode → subcluster
lookup once the external lookup table is available.
Set TEST_MODE = False in config.py to activate.

Expected format: dict mapping postcode sector prefix to subcluster label
  e.g. POSTCODE_SUBCLUSTER_LOOKUP = {'L1': '1.2', 'WA10': '3.1', ...}

POSTCODE_SUBCLUSTER_LOOKUP = {}  # <-- insert lookup dict here
============================================================
"""

import numpy as np
import pandas as pd

# ---------------------------------------------------------------------------
# All 9 subcluster labels
# ---------------------------------------------------------------------------
ALL_SUBCLUSTERS = ['1.1', '1.2', '2.1', '2.2', '3.1', '3.2', '3.3', '4.1', '4.2']

# ---------------------------------------------------------------------------
# Composite z-scores per subcluster per trip parameter
#
# Source: geodemographic clustering analysis z-score table.
# Each entry is the unweighted mean of the driving feature z-scores for that
# parameter (see implementation plan for feature→parameter mapping).
#
# Column order matches ALL_SUBCLUSTERS:
#   1.1    1.2    2.1    2.2    3.1    3.2    3.3    4.1    4.2
# ---------------------------------------------------------------------------
CLUSTER_Z_SCORES = {
    # --- Grocery modes ---
    # Drivers: int_acc_yes, Online Often, IUC Online Retail Engagement,
    #          No cars or vans in household
    'prob_online': [
         0.35,   1.10,   0.50,   0.45,  -0.10,   0.10,   1.05,   0.50,  -0.30
    ],

    # Drivers: Convenience (shopping), high_PT_sub_bua_access,
    #          Urban Setting, Less than £50
    'prob_convenience': [
        -0.10,   1.10,   1.20,   0.80,   0.20,  -0.10,  -0.60,  -1.40,  -0.80
    ],

    # Drivers: high_car_access_supermarket, Discounter, More than 100,
    #          Mid Range (shopping)
    'prob_bulk': [
         0.55,  -0.80,  -1.00,  -0.60,   1.05,   0.60,   1.10,   1.40,   0.70
    ],

    # --- NTS trip types ---
    # Drivers: Premium (shopping), people_payoff_creditcard_always,
    #          Cinema_Theatre_Concert, people_2_holidays
    'prob_trip_comparison': [
         0.55,  -0.80,  -0.60,  -0.45,   0.05,   0.70,   1.20,   0.70,   0.35
    ],

    # Drivers: Dining_and_Social_Activities, Urban Setting,
    #          people_payoff_creditcard_always, Cinema_Theatre_Concert
    'prob_trip_food_drink': [
         0.65,  -0.60,  -0.85,  -0.80,  -0.05,   0.75,   1.25,   0.95,   0.25
    ],

    # Drivers: Cinema_Theatre_Concert, Hobbies_and_creative,
    #          people_who_gamble, high_PT_sub_bua_access
    'prob_trip_entertainment': [
         0.20,  -0.35,  -0.20,   0.10,  -0.15,   0.35,   1.00,   0.40,  -0.25
    ],

    # Drivers: Yes_Insurance, yes_investments, have_pets, Urban Setting
    'prob_trip_service': [
         0.45,  -0.25,  -0.50,  -0.45,   0.30,   0.55,   1.10,   1.05,   0.45
    ],
}

# Sigmoid sharpness parameter (γ = 1.5 per plan)
_SIGMOID_GAMMA = 1.5


def _sigmoid(x):
    """Numerically stable sigmoid."""
    return 1.0 / (1.0 + np.exp(-np.clip(x, -50, 50)))


def _build_priors(gamma: float = _SIGMOID_GAMMA) -> dict:
    """
    Converts raw z-scores to probability priors via sigmoid(z * gamma).
    Returns dict: {subcluster_label: {param: prior_value}}
    """
    priors = {sc: {} for sc in ALL_SUBCLUSTERS}
    for param, zscores in CLUSTER_Z_SCORES.items():
        transformed = _sigmoid(np.array(zscores) * gamma)
        for sc, val in zip(ALL_SUBCLUSTERS, transformed):
            priors[sc][param] = float(val)
    return priors


# Pre-built priors at import time
_PRIORS = _build_priors()


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def get_cluster_priors(subcluster_label: str) -> dict:
    """
    Returns a dict of {param_name: prior_probability} for the given subcluster.

    Parameters
    ----------
    subcluster_label : str  e.g. '1.2'

    Returns
    -------
    dict  e.g. {'prob_online': 0.75, 'prob_bulk': 0.31, ...}
    """
    return _PRIORS.get(subcluster_label, {p: 0.5 for p in CLUSTER_Z_SCORES})


def assign_subcluster(postcode: str = None, test_mode: bool = True) -> str:
    """
    Assigns a geodemographic subcluster label to an agent.

    Parameters
    ----------
    postcode  : str   Agent's postcode (used in production mode).
    test_mode : bool  If True, assigns a random subcluster uniformly.

    Returns
    -------
    str  Subcluster label, e.g. '1.2'
    """
    if test_mode:
        return str(np.random.choice(ALL_SUBCLUSTERS))

    # --- PRODUCTION MODE ---
    # Uncomment and populate POSTCODE_SUBCLUSTER_LOOKUP at the top of this file,
    # then implement the postcode → sector → subcluster lookup below.
    # sector = str(postcode)[:4].strip().upper() if postcode else ''
    # return POSTCODE_SUBCLUSTER_LOOKUP.get(sector, np.random.choice(ALL_SUBCLUSTERS))

    # Fallback: random until lookup is implemented
    return str(np.random.choice(ALL_SUBCLUSTERS))


def apply_cluster_blend(attributes_df: pd.DataFrame,
                        subcluster_col: str = 'Geo_Subcluster',
                        blend_weight_col: str = 'Cluster_Blend_Weight') -> pd.DataFrame:
    """
    Blends each agent's NTS-derived trip probabilities with their
    subcluster-level contextual prior.

    Formula (per agent i, per parameter p):
        p_final = clip((1 - w_i) * p_NTS + w_i * mu_subcluster, 0, 1)

    where w_i is the agent's individual blend weight (U(0.3, 0.7)).

    Parameters
    ----------
    attributes_df    : pd.DataFrame  Agent attributes (modified in-place copy).
    subcluster_col   : str           Column containing subcluster labels.
    blend_weight_col : str           Column containing per-agent blend weights.

    Returns
    -------
    pd.DataFrame  Modified copy of attributes_df.
    """
    df = attributes_df.copy()
    params = list(CLUSTER_Z_SCORES.keys())

    # Only blend parameters that actually exist in the DataFrame
    params_present = [p for p in params if p in df.columns]
    if not params_present:
        return df

    for sc in ALL_SUBCLUSTERS:
        mask = df[subcluster_col] == sc
        if not mask.any():
            continue

        priors = get_cluster_priors(sc)
        w = df.loc[mask, blend_weight_col].values.reshape(-1, 1)

        for param in params_present:
            mu = priors[param]
            p_nts = df.loc[mask, param].values
            p_final = (1.0 - w.ravel()) * p_nts + w.ravel() * mu
            df.loc[mask, param] = np.clip(p_final, 0.0, 1.0)

    # Re-normalise grocery mode probabilities so they sum to 1
    grocery_cols = ['prob_online', 'prob_bulk', 'prob_convenience']
    grocery_present = [c for c in grocery_cols if c in df.columns]
    if len(grocery_present) == 3:
        row_sums = df[grocery_present].sum(axis=1).replace(0, 1.0)
        df[grocery_present] = df[grocery_present].div(row_sums, axis=0)

    return df
