"""Just some fake data for marketing mix modeling."""

import numpy as np
import pandas as pd
from sklearn.pipeline import make_pipeline

from mamimo.carryover import ExponentialCarryover
from mamimo.saturation import ExponentialSaturation
from mamimo.time_utils import add_date_indicators


def load_fake_mmm():
    """Load the data."""
    np.random.seed(0)

    data = pd.DataFrame(
        {
            "TV": np.random.normal(loc=10000, scale=2000, size=200)
            * np.random.binomial(n=1, p=0.3, size=200),
            "Radio": np.random.normal(loc=5000, scale=1000, size=200)
            * np.random.binomial(n=1, p=0.5, size=200),
            "Banners": np.random.normal(loc=2000, scale=200, size=200)
            * np.random.binomial(n=1, p=0.8, size=200),
        },
        index=pd.date_range(start="2018-01-01", periods=200, freq="w"),
    ).clip(0, np.inf)

    tv_pipe = make_pipeline(
        ExponentialCarryover(window=4, strength=0.5),
        ExponentialSaturation(exponent=0.0001),
    )
    radio_pipe = make_pipeline(
        ExponentialCarryover(window=2, strength=0.2),
        ExponentialSaturation(exponent=0.0001),
    )
    banners_pipe = make_pipeline(ExponentialSaturation(exponent=0.0001))
    date_carryover = ExponentialCarryover(window=10, strength=0.6)

    adstock_data = data.copy().pipe(
        add_date_indicators, some_special_date=["2020-01-05"]
    )
    adstock_data["TV"] = tv_pipe.fit_transform(adstock_data[["TV"]])
    adstock_data["Radio"] = radio_pipe.fit_transform(adstock_data[["Radio"]])
    adstock_data["Banners"] = banners_pipe.fit_transform(adstock_data[["Banners"]])
    adstock_data["some_special_date"] = date_carryover.fit_transform(
        adstock_data[["some_special_date"]]
    )

    sales = (
        10000 * adstock_data["TV"]
        + 8000 * adstock_data["Radio"]
        + 14000 * adstock_data["Banners"]
        + 1000 * np.sin(np.arange(200) * 2 * np.pi / 52)
        + 40 * np.arange(200) ** 1.2
        + 80000 * adstock_data["some_special_date"]
        + 500 * np.random.randn(200)
    )

    data["Sales"] = sales

    return data.rename_axis(index="Date").round(2).clip(0, np.inf)
