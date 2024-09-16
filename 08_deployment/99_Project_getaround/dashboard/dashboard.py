# prelude
import os
import streamlit as st

import numpy as np
import pandas as pd

import seaborn as sns
import matplotlib.pyplot as plt

from matplotlib.ticker import PercentFormatter


# -----------------------------------------------------------------------------
from pathlib import Path

k_CurrentDir = Path(__file__).parent  # __file__ is not known in Jupyter context
# k_CurrentDir   = Path.cwd()
k_AssetsDir = "assets"
k_Gold = 1.618  # gold number for ratio
k_Width = 12
k_Height = k_Width / k_Gold
k_WidthPx = 1024
k_HeightPx = k_WidthPx / k_Gold
k_random_state = 0


# -----------------------------------------------------------------------------
def preprocessor(df):
    # drop
    df.drop(columns="Unnamed: 7", inplace=True)
    df.drop_duplicates(inplace=True)

    # format
    df.columns = df.columns.str.lower()
    df.columns = df.columns.str.replace("/", "_")

    # rename
    # df.rename(
    #     columns={
    #         "rental_id": "id",
    #         "previous_ended_rental_id": "previous_id"
    #     },
    #     inplace=True
    # )

    # cast
    df["rental_id"] = df["rental_id"].astype(str)
    df["car_id"] = df["car_id"].astype(str)
    # df['previous_ended_rental_id'] = df['previous_ended_rental_id'].astype(str)
    df["previous_ended_rental_id"] = df["previous_ended_rental_id"].apply(
        lambda x: str(int(x)) if not pd.isna(x) else x
    )

    # other preprocessing should come here
    # df["time_slot"] = (df["hour"]*60 + df["minute"])//k_time_slot_len

    # set index
    # df.set_index('id', inplace=True)

    return df


# -----------------------------------------------------------------------------
def quick_View(df: pd.DataFrame) -> pd.DataFrame:
    """
    Generates a summary DataFrame for each column in the input DataFrame.

    This function analyzes each column in the given DataFrame and creates a summary that includes
    data type, number of null values, percentage of null values, number of non-null values,
    number of distinct values, min and max values, outlier bounds (for numeric columns),
    and the frequency of distinct values.

    Args:
        df (pd.DataFrame): The input DataFrame to analyze.

    Returns:
        pd.DataFrame: A DataFrame containing the summary of each column from the input DataFrame.
                      Each row in the resulting DataFrame represents a column from the input DataFrame
                      with the following information:
                      - "name": Column name
                      - "dtype": Data type of the column
                      - "# null": Number of null values
                      - "% null": Percentage of null values
                      - "# NOT null": Number of non-null values
                      - "distinct val": Number of distinct values
                      - "-3*sig": Lower bound for outliers (mean - 3*std) for numeric columns
                      - "min": Minimum value for numeric columns
                      - "mean" : Mean value for numeric columns
                      - "max": Maximum value for numeric columns
                      - "+3*sig": Upper bound for outliers (mean + 3*std) for numeric columns
                      - "distinct val count": Dictionary of distinct value counts or top 10 values for object columns
    """

    summary_lst = []

    for col_name in df.columns:
        col_dtype = df[col_name].dtype
        num_of_null = df[col_name].isnull().sum()
        percent_of_null = num_of_null / len(df)
        num_of_non_null = df[col_name].notnull().sum()
        num_of_distinct_values = df[col_name].nunique()

        if num_of_distinct_values <= 10:
            distinct_values_counts = df[col_name].value_counts().to_dict()
        else:
            top_10_values_counts = df[col_name].value_counts().head(10).to_dict()
            distinct_values_counts = {
                k: v for k, v in sorted(top_10_values_counts.items(), key=lambda item: item[1], reverse=True)
            }

        if col_dtype != "object":
            max_of_col = df[col_name].max()
            min_of_col = df[col_name].min()
            mean_of_col = df[col_name].mean()
            outlier_hi = df[col_name].mean() + 3 * df[col_name].std()
            outlier_lo = df[col_name].mean() - 3 * df[col_name].std()
        else:
            max_of_col = -1
            min_of_col = 1
            mean_of_col = np.nan
            outlier_hi = -1
            outlier_lo = 1

        summary_lst.append(
            {
                "name": col_name,
                "dtype": col_dtype,
                "# null": num_of_null,
                "% null": (100 * percent_of_null).round(2),
                "# NOT null": num_of_non_null,
                "distinct val": num_of_distinct_values,
                "-3*sig": round(outlier_lo, 2),
                "min": round(min_of_col, 2),
                "mean": round(mean_of_col, 2),
                "max": round(max_of_col, 2),
                "+3*sig": round(outlier_hi, 2),
                "distinct val count": distinct_values_counts,
            }
        )

    df_tmp = pd.DataFrame(summary_lst)
    return df_tmp


# -----------------------------------------------------------------------------
def classify_value(row):
    value = row["return"]
    if row["booking"] == "consecutive":
        if value <= row["delta"]:
            return "On time"
        elif value > row["delta"]:
            return "Late"
        else:
            return "No Data"
    elif row["booking"] == "not consecutive":
        if value <= 0:
            return "On time"
        elif value > 0:
            return "Late"
        else:
            return "No Data"
    else:
        raise ValueError("Unexpected booking value")


# -----------------------------------------------------------------------------
def main():

    ###########################################################################
    st.title("getaround dashboard")

    ###########################################################################
    st.header("Executive summary")
    st.markdown(
        """
            * If corporate want to promote Connect :
                * Connect : set the Treshold to 1H30 and target 10% of problematic returns
                * Mobile : set the Treshold to 3H00 and target 10% of problematic returns (13% today)
            * If we want to make no differentiation between connect or mobile
                * Set the Treshold to 2H 
                * Target 10 % of the problematic returns (16% today)
            * Let the leaser the ability to add its own Time $\Delta$

        """
    )

    ###########################################################################
    st.header("EDA (Delay Analysis)")
    # Load data
    # df = pd.read_excel('https://full-stack-assets.s3.eu-west-3.amazonaws.com/Deployment/get_around_delay_analysis.xlsx')
    df = pd.read_excel(k_CurrentDir / k_AssetsDir / "get_around_delay_analysis.xlsx", sheet_name="rentals_data")

    # st.write(f"\n\nPreview of the dataset :")
    # st.dataframe(df.sample(15))

    ###########################################################################
    # Clean, preprocess and data overview
    st.subheader("Data overview")
    df = preprocessor(df)
    # st.write(f"\n\nPreview of the preprocessed dataset :")
    # st.dataframe(df.sample(15))

    # Correct a typo.
    # See 08_deployment\99_Project_getaround\03_getarround_pricing.ipynb for the detail
    df.at[16344, "delay_at_checkout_in_minutes"] = np.nan

    df_tmp = quick_View(df)
    # st.write(f"\n\nData overview :")
    st.dataframe(df_tmp.sort_values(by="# null", ascending=False))

    st.markdown(
        """
            ### :orange[**Comments :**]
            * Only 2 values for ``checkin_type`` (mobile, connect) and ``state`` (ended, canceled) 
            * There are "only" 25 uniques value in `time_delta_with_previous_rental_in_minutes` 
            * Again, `previous_ended_rental_id` and `time_delta_with_previous_rental_in_minutes` have the same amount of data
            * Outliers in ``delay_at_checkout_in_minutes`` (max > 3 $\sigma$)
        """
    )

    ###########################################################################
    # Checking types
    st.subheader("About checkin_type")
    counts = df["checkin_type"].value_counts()
    fig, ax = plt.subplots(figsize=(k_Width, k_Height))
    counts.plot.pie(title="checkin_type : weight as %", autopct="%1.1f%%", ax=ax)
    st.pyplot(fig)
    st.markdown(
        """
            ### :orange[**Comments :**]
            * 20% of the checkin/checkout are made via connected cars
        """
    )

    ###########################################################################
    # State
    st.subheader("About state")
    counts = df["state"].value_counts()
    fig, ax = plt.subplots(figsize=(k_Width, k_Height))
    counts.plot.pie(title="state : weight as %", autopct="%1.1f%%", ax=ax)
    st.pyplot(fig)
    st.markdown(
        """
            ### :orange[**Comments :**]
            * 15% of the rentals are canceled
            * Obviously, in these cases, there is no ``delay_at_checkout_in_minutes`` 
            * When there is a rental before the one canceled (`previous_ended_rental_id` != NaN), then a `time_delta_with_previous_rental_in_minutes` also exists 

        """
    )

    ###########################################################################
    # state, consecutive rentals and late returns
    st.subheader("About state, consecutive rentals and late returns")

    df_tmp = df[
        [
            "state",
            "previous_ended_rental_id",
            "delay_at_checkout_in_minutes",
            "time_delta_with_previous_rental_in_minutes",
        ]
    ].copy()
    df_tmp.rename(
        columns={
            "previous_ended_rental_id": "booking",
            "delay_at_checkout_in_minutes": "return",
            "time_delta_with_previous_rental_in_minutes": "delta",
        },
        inplace=True,
    )
    # display(df_tmp.sample(15))
    # display(df_tmp.head(15))

    # df_tmp.loc[pd.notna(df_tmp["booking"]), "booking"] = "consecutive"
    # df_tmp["booking"].fillna("not consecutive", inplace=True)
    df_tmp["booking"] = np.where(pd.notna(df_tmp["booking"]), "consecutive", "not consecutive")
    # display(df_tmp.head(15))

    # convert to string first then replace with meaningful value
    df_tmp["return"] = pd.to_numeric(df_tmp["return"], errors="coerce")
    df_tmp["return"] = df_tmp.apply(classify_value, axis=1)

    df_pivot = df_tmp.pivot_table(index="state", columns=["booking", "return"], aggfunc=len)
    df_pivot["Total"] = df_pivot.sum(axis=1, skipna=True)
    df_pivot.loc["Total"] = df_pivot.sum(axis=0, skipna=True)
    st.dataframe(df_pivot)

    st.markdown(
        """
            ### :orange[**Comments :**]
            * We now have more information about the bookings which are not canceled
            * When 2 bookings are consecutive with a Time $\Delta$ between them most of the rentals are on time (returns happen before `time_delta_with_previous_rental_in_minutes`)
                * See 270 vs 1245 (second line, left hand side in the table above)
            * When there is no Time $\Delta$ (no previous driver) most of the returns are late
                * See 8602 vs 6228 (second line, right hand side in the table above)

        """
    )

    ###########################################################################
    # time_delta_with_previous_rental_in_minutes
    st.subheader("About time_delta_with_previous_rental_in_minutes")
    fig, ax = plt.subplots(figsize=(k_Width, k_Height))
    sns.histplot(
        data=df, x="time_delta_with_previous_rental_in_minutes", hue="checkin_type", hue_order=["connect", "mobile"]
    )  # , bins=100, , kde=True

    ax.set_title("Distribution of time_delta_with_previous_rental_in_minutes")
    ax.set_xlabel("Minutes")
    st.pyplot(fig)

    st.markdown(
        """
            ### :orange[**Comments :**]
            * Surprisingly, no matter the `checkin_type`, the number of Time $\Delta$ do not decrease when its values become extreme
            * The count of Time $\Delta$ close to 12H (720 min.) is similar to the number of Time $\Delta$ close to 2H (120 min.)
            * :orange[**For action :**] get a better understanding on how the Time $\Delta$ is set
                * Is it set per rental after discussing with the driver?
                * When the leasers set the Time $\Delta$ to 12H, are they willing to use the car between 2 rentals?
                * ...

        """
    )

    ###########################################################################
    # How often are drivers late for the next check-in? How does it impact the next driver?
    st.header("How often are drivers late for the next check-in? How does it impact the next driver?")

    st.image("./assets/no_treshold.png", caption="No Threshold", width=800)

    st.markdown(
        """
            ### :orange[**Comments :**]
            There are two cases, depending on whether there is a previous rental or not :
            1. No previous driver (top of the figure, blue)
                * Cars are supposed to be returned before **Checkout**  
                * If not, we call **Delay** (``delay_at_checkout_in_minutes``) the period of time between the **Checkout** and the **Return Time**
                    * The car is considered as returned late
            1. There is a previous driver (bottom of the figure, orange)
                * The owner of the car set a **Time $\Delta$** between the 2 consecutive bookings
                * Length of the **Time $\Delta$** ranges from 0 to 720 min. by steps of 30 min.
                * The **Time $\Delta$** period of time act as a shock absorber if the previous customer is late returning the car
                    * The owner may rent his car less often, but in return, he protects himself from late returns
                    * This avoids a certain amount of friction with unhappy 'next driver'
                * Cars are supposed to be returned before **Checkout** + **Time $\Delta$**
                * If not the car is considered as returned late
                    * The next booking is problematic and it can be canceled
        """
    )

    ###########################################################################
    st.subheader("How often are drivers late for the next check-in?")

    st.markdown(
        """
            We consider a driver is late when :
            1. The transactions is in state `ended`, there is no previous driver (``previous_ended_rental_id`` = Nan) and `delay_at_checkout_in_minutes` is strictly greater than 0 
                * According the last pivot table we know this number is 8602
            1. The transactions is in state `ended`, there is previous driver (``previous_ended_rental_id`` != Nan) and `delay_at_checkout_in_minutes` is strictly greater than ``time_delta_with_previous_rental_in_minutes``
                * According the last pivot table we know this number is 270
            1. The transactions in state `canceled` AND there is a `previous_ended_rental_id` 
                * Again, in this case we can assume that the transaction is cancelled precisely because the previous driver is late.
                * However, we don't know precisely how long after the planned Checkout, the previous driver returned the car
                * According the last pivot table we know this number is 229

            * We then compare this number to the total number of returns (in advance or late). 
                * We do not take into account returns for wich we do have the `delay_at_checkout_in_minutes`
        """
    )

    late1 = len(
        df[
            (df["state"] == "ended")
            & (df["previous_ended_rental_id"].isna())
            & (df["delay_at_checkout_in_minutes"] > 0)
        ]
    )
    st.write(f"Nb of ended transactions with no previous driver with delay > 0 = {late1}")

    late2 = len(
        df[
            (df["state"] == "ended")
            & (df["previous_ended_rental_id"].notna())
            & (df["delay_at_checkout_in_minutes"] > df["time_delta_with_previous_rental_in_minutes"])
        ]
    )
    st.write(f"Nb of ended transactions with a previous driver with delay > time delta = {late2}")

    late3 = len(df[(df["state"] == "canceled") & (df["previous_ended_rental_id"].notna())])
    st.write(f"Nb of canceled transactions with a previous driver = {late3}")

    # We must add late3 !
    total_number_returns = len(df[(df["delay_at_checkout_in_minutes"].notna())]) + late3
    st.write(f"Number of returns concerned = {total_number_returns}")

    percent_late_return = (late1 + late2 + late3) / total_number_returns * 100
    st.write(f"The percentage of late returns = {percent_late_return:.2f}%")

    st.markdown(
        """
            ### :orange[**Comments :**]
            * 55% of the returns are late

        """
    )

    ###########################################################################
    st.subheader("Can we analyze late rental returns more accurately?")

    # compute the content of the column actual_delay
    # actual_delay = delay_at_checkout_in_minutes                   if there is no time_delta_with_previous_rental_in_minutes
    # actual_delay = delay_at_checkout_in_minutes - time_delta      if there is a time_delta_with_previous_rental_in_minutes
    # uncomment the display() if needed
    # if the value in actual_content is positive this mean the return is late, no matter if there is a time delta or not
    def calculate_actual_delay(row):
        if not np.isnan(row["delay_at_checkout_in_minutes"]) and not np.isnan(
            row["time_delta_with_previous_rental_in_minutes"]
        ):
            return row["delay_at_checkout_in_minutes"] - row["time_delta_with_previous_rental_in_minutes"]
        elif np.isnan(row["time_delta_with_previous_rental_in_minutes"]) and not np.isnan(
            row["delay_at_checkout_in_minutes"]
        ):
            return row["delay_at_checkout_in_minutes"]
        else:
            return np.nan

    df_tmp = df[df["state"] == "ended"].copy()
    # display(df_tmp.sample(15))

    df_tmp["actual_delay"] = df.apply(calculate_actual_delay, axis=1)
    # display(df_tmp.sample(15))

    labels_in_order = ["0-10 min", "10-30 min", "30 min-1H", "1H-2H", "2H-6H", "> 6H"]

    categories = pd.cut(df_tmp["actual_delay"], bins=[0, 10, 30, 60, 120, 360, float("inf")], labels=labels_in_order)
    df_tmp["cat_delay"] = categories
    # display(df_tmp.sample(15))

    df_tmp2 = pd.DataFrame(
        round(df_tmp["cat_delay"].value_counts() / len(df_tmp[df_tmp["actual_delay"] > 0]) * 100, 2)
    ).reset_index()
    df_tmp2.columns = ["cat_delay", "delay_%"]

    df_tmp2["cat_delay"] = pd.Categorical(df_tmp2["cat_delay"], categories=labels_in_order, ordered=True)
    df_tmp2.sort_values("cat_delay", inplace=True)
    df_tmp2.set_index("cat_delay", inplace=True)
    # print(df_tmp2)

    df_tmp2["cum_percent"] = df_tmp2["delay_%"].cumsum() / df_tmp2["delay_%"].sum() * 100

    fig, ax = plt.subplots(figsize=(k_Width, k_Height))
    ax.bar(df_tmp2.index, df_tmp2["delay_%"], color="C0")
    ax.yaxis.set_major_formatter(PercentFormatter())
    ax.set_ylabel("Percentage")
    ax.tick_params(axis="y", colors="C0")
    ax.set_title("Distribution of the late returns & their cumulative sum")

    ax2 = ax.twinx()
    ax2.plot(df_tmp2.index, df_tmp2["cum_percent"], color="C1", marker="D", ms=7)
    ax2.yaxis.set_major_formatter(PercentFormatter())
    ax2.set_ylabel("Cumulative sum")
    ax2.set(ylim=(0, 110))
    ax2.tick_params(axis="y", colors="C1")

    st.pyplot(fig)

    st.markdown(
        """
            ### :orange[**Comments :**]
            * More than 50% of the late returns are below 1H
            * Almost 80% of the late returns are below 2H

        """
    )

    ###########################################################################
    # How does it impact the next driver?
    st.header("How often are drivers late for the next check-in? How does it impact the next driver?")

    st.image("./assets/no_treshold.png", caption="No Threshold", width=800)

    st.markdown(
        """
            This point have been already addressed

            We consider as problematic the following kind of returns :
            1. Cars returned after Checkout
                * Because the owner of the car can't use it  
            1. Cars returned after Time $\Delta$
                * Because the next driver can't get the car
            1. The number of bookings which are canceled because the previous driver is late
        """
    )
    ###########################################################################
    # How many rentals would be affected by the feature depending on the threshold and scope we choose?

    st.header("How many rentals would be affected by the feature depending on the threshold and scope we choose?")

    st.image("./assets/with_treshold.png", caption="No Threshold", width=800)

    st.markdown(
        """
            * At this point, it is not clear in the specifications if the Threshold comes in addition to the Time $\Delta$, if it replace it...
            * :orange[**Decision :**] until further notice, we'll assume that Threshold simply replaces Time Delta 
            * The rentals taken into account are :
                * Cars returned after Treshold 
                * No matter if there is (or not) a previous driver
                * We compare `delay_at_checkout_in_minutes` vs Treshold
                * Canceled rentals cannot be taken into account because when there is a previous driver, we don't know pricely at what time the car is returned
            * In order to calculate the impact, for different values of Treshold, we compare the previous number with the number of rentals that are ``ended`` and NOT on the whole dataset (``ended`` + ``canceled``)  
            * The impact should be 100% when Treshold is 0 and 0% when Threshold is infinite

        """
    )

    # see time_delta_with_previous_rental_in_minutes
    thresholds = [
        0,
        30,
        60,
        90,
        120,
        150,
        180,
        210,
        240,
        270,
        300,
        330,
        360,
        390,
        420,
        450,
        480,
        510,
        540,
        570,
        600,
        630,
        660,
        690,
        720,
    ]

    df_tmp = df[df["state"] == "ended"].copy()

    # number of reservations with delay_at_checkout_in_minutes > 0
    # nb_late = len(df_tmp[(df_tmp['delay_at_checkout_in_minutes'] > 0 )])
    # nb = len(df_tmp[(df_tmp['delay_at_checkout_in_minutes'] > 0 )])
    # nb = len(df_tmp)
    nb = len(df_tmp[(df_tmp["delay_at_checkout_in_minutes"].notna())])
    print(nb)

    rates = []
    for t in thresholds:
        # no matter if there is a previous_ended_rental_id or not
        # n is the number of bookings with a delay_at_checkout_in_minutes greater than current threshold (0...720)
        n = len(df_tmp[(df_tmp["delay_at_checkout_in_minutes"] > (t))])
        rates.append(n / nb * 100)
    # display(rates)

    fig, ax = plt.subplots(figsize=(k_Width, k_Height))
    ax.plot(thresholds, rates, color="C1", marker="D", ms=7)
    ax.yaxis.set_major_formatter(PercentFormatter())
    ax.set_ylabel("Affected returns (%)")
    ax.set_xlabel("Threshold (min.)")
    ax.tick_params(axis="y", colors="C0")
    ax.set_title("Percentage of affected returns vs Threshold length")

    # xv and yh are "hand adjusted" to cross at 20%
    xv = 90
    yh = 20  # epsilon
    plt.axvline(x=xv, color="red", linestyle="--")
    plt.axhline(y=yh, color="red", linestyle="--")

    xv1 = 180
    yh1 = 10.7  # epsilon
    plt.axvline(x=xv1, color="blue", linestyle="--")
    plt.axhline(y=yh1, color="blue", linestyle="--")

    st.pyplot(fig)

    st.markdown(
        """
            ### :orange[**Comments :**]
            * We evaluate the percentage of rentals which would be affected
            * Not the percentage of late returns
            * To do so compare the number of returns above Treshold
            * Versus the number of returns with delay information
                * On purpose, we do not take into account returns without information about `delay_at_checkout_in_minutes`
            * If the threshold is set to 0 min., 57% of the returns will exceed the threshold, making 57% of the returns problematic
            * One could be surprised since, earlier, in section **How often are drivers late for the next check-in?** we said that 55% of the returns are late.
            * In fact here we cannot take into account the 229 canceled bookings because they don't have information about the time of return
            * When the Threshold is set to 1H30 then 20% of the returns remains problematic
    
        """
    )

    ###########################################################################
    # What about "mobile" ?
    st.subheader("What about 'mobile' ?")

    # see time_delta_with_previous_rental_in_minutes
    thresholds = [
        0,
        30,
        60,
        90,
        120,
        150,
        180,
        210,
        240,
        270,
        300,
        330,
        360,
        390,
        420,
        450,
        480,
        510,
        540,
        570,
        600,
        630,
        660,
        690,
        720,
    ]

    df_tmp = df[(df["state"] == "ended") & ((df["checkin_type"] == "mobile"))].copy()

    # number of reservations with delay_at_checkout_in_minutes > 0
    # nb_late = len(df_tmp[(df_tmp['delay_at_checkout_in_minutes'] > 0 )])
    # nb = len(df_tmp[(df_tmp['delay_at_checkout_in_minutes'] > 0 )])
    # nb = len(df_tmp)

    nb = len(df_tmp[(df_tmp["delay_at_checkout_in_minutes"].notna())])
    print(nb)

    rates = []
    for t in thresholds:
        # no matter if there is a previous_ended_rental_id or not
        # n is the number of bookings with a delay_at_checkout_in_minutes greater than current threshold (0...720)
        n = len(df_tmp[(df_tmp["delay_at_checkout_in_minutes"] > (t))])
        rates.append(n / nb * 100)
    # display(rates)

    fig, ax = plt.subplots(figsize=(k_Width, k_Height))
    ax.plot(thresholds, rates, color="C1", marker="D", ms=7)
    ax.yaxis.set_major_formatter(PercentFormatter())
    ax.set_ylabel("Affected returns (%)")
    ax.set_xlabel("Threshold (min.)")
    ax.tick_params(axis="y", colors="C0")
    ax.set_title("Mobile - Percentage of affected returns vs Threshold length")

    # xv and yh are "hand adjusted" to cross at 20%
    xv = 105
    yh = 20  # epsilon
    plt.axvline(x=xv, color="red", linestyle="--")
    plt.axhline(y=yh, color="red", linestyle="--")

    st.pyplot(fig)

    ###########################################################################
    # What about "connect" ?
    st.subheader("What about 'connect' ?")

    # see time_delta_with_previous_rental_in_minutes
    thresholds = [
        0,
        30,
        60,
        90,
        120,
        150,
        180,
        210,
        240,
        270,
        300,
        330,
        360,
        390,
        420,
        450,
        480,
        510,
        540,
        570,
        600,
        630,
        660,
        690,
        720,
    ]

    df_tmp = df[(df["state"] == "ended") & ((df["checkin_type"] == "connect"))].copy()

    # number of reservations with delay_at_checkout_in_minutes > 0
    # nb_late = len(df_tmp[(df_tmp['delay_at_checkout_in_minutes'] > 0 )])
    # nb = len(df_tmp[(df_tmp['delay_at_checkout_in_minutes'] > 0 )])
    # nb = len(df_tmp)

    nb = len(df_tmp[(df_tmp["delay_at_checkout_in_minutes"].notna())])
    print(nb)

    rates = []
    for t in thresholds:
        # no matter if there is a previous_ended_rental_id or not
        # n is the number of bookings with a delay_at_checkout_in_minutes greater than current threshold (0...720)
        n = len(df_tmp[(df_tmp["delay_at_checkout_in_minutes"] > (t))])
        rates.append(n / nb * 100)
    # display(rates)

    fig, ax = plt.subplots(figsize=(k_Width, k_Height))
    ax.plot(thresholds, rates, color="C1", marker="D", ms=7)
    ax.yaxis.set_major_formatter(PercentFormatter())
    ax.set_ylabel("Affected returns (%)")
    ax.set_xlabel("Threshold (min.)")
    ax.tick_params(axis="y", colors="C0")
    ax.set_title("Connect - Percentage of affected returns vs Threshold length")

    # xv and yh are "hand adjusted" to cross at 20%
    xv = 49
    yh = 20  # epsilon
    plt.axvline(x=xv, color="red", linestyle="--")
    plt.axhline(y=yh, color="red", linestyle="--")
    st.pyplot(fig)

    ###########################################################################
    # How many problematic cases will it solve depending on the chosen threshold and scope?
    st.header("How many problematic cases will it solve depending on the chosen threshold and scope?")

    st.markdown(
        """
            ### :orange[**Comments :**]
            * The question has been already answered
            * Using the previous graphs we can see :
            * Mobile : if threshold is set to 105 min, 20% returns remains problematic
            * Connect : if threshold is set to 49 min, 20% returns remains problematic  

            ### :orange[**Overall recommendation :**] 
            * If corporate want to promote Connect :
                * Connect : set the Treshold to 1H30 and target 10% of problematic returns
                * Mobile : set the Treshold to 3H00 and target 10% of problematic returns (13% today)
            * If we want to make no differentiation between connect or mobile
                * Set the Treshold to 2H 
                * Target 10 % of the problematic returns (16% today)
            * Let the leaser the ability to add its own Time $\Delta$
        """
    )

    ###########################################################################


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    main()
    os.system(f"streamlit run dashboard.py --server.port={port} --server.enableCORS=true")
