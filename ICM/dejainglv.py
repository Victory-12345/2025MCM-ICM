import pandas as pd

# Load the provided files
summer_oly_path = 'summerOly_programs.xlsx'
chn_path = 'USA.xlsx'


summer_oly = pd.read_excel(summer_oly_path)
chn = pd.read_excel(chn_path)


# Step 1: Summarize summerOly_programs.xlsx by Sport
summer_oly_grouped = summer_oly.groupby('Sport').sum().reset_index()

# Step 2: Define a function to calculate award rates
def calculate_award_rates(country_df, summer_oly_df):
    # Merge country data with summer olympics data on 'Sport' and 'Year'
    merged = country_df.merge(
        summer_oly_df.melt(id_vars=["Sport"], var_name="Year", value_name="Total_Events"),
        how="left",
        on=["Sport", "Year"]
    )

    # Calculate award rates
    for medal in ["Gold", "Silver", "Bronze"]:
        merged[f"{medal}_Rate"] = merged[medal] / merged["Total_Events"]

    # Select relevant columns for output
    award_rates = merged[["Sport", "Year", "Gold_Rate", "Silver_Rate", "Bronze_Rate"]]

    return award_rates

# Step 3: Prepare the country data
def prepare_country_data(country_df):
    # Ensure the format matches expectations
    return country_df.rename(columns={"Year": "Year"})

chn_prepared = prepare_country_data(chn)


# Step 4: Calculate award rates for CHN and JPN
chn_award_rates = calculate_award_rates(chn_prepared, summer_oly_grouped)


# Step 5: Save the resulting award rates to new Excel files
chn_award_rates.to_excel("USA_award_rates.xlsx", index=False)

