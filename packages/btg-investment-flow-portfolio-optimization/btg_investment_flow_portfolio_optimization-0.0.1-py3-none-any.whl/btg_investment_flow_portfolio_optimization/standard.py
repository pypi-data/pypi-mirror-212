from btg_investment_flow_portfolio_optimization.portfolio_optimization import (
    PortfolioOptimizer,
)

import pandas as pd


class StandardPortfolioOptimizer(PortfolioOptimizer):
    @staticmethod
    def sum_between_dates(df, start_date, end_date, quantile):
        """Calculate the sum of a quantile between two dates."""
        df.index = pd.to_datetime(df.index)
        start_date = pd.to_datetime(start_date)
        end_date = pd.to_datetime(end_date)
        mask = (df.index >= start_date) & (df.index <= end_date)
        subset_df = df.loc[mask]

        # Set negative values to zero
        subset_df.loc[subset_df[quantile] < 0, quantile] = 0

        return subset_df[quantile].sum()

    def generate_time_slots(self, start_date, end_date):
        """Generate a list of intervals representing the starting and ending points of each time slot"""
        time_slots = []
        current_date = start_date
        while current_date <= end_date:
            if current_date.weekday() < 4:  # It's a weekday, but not Friday
                time_slots.append(
                    (
                        current_date.replace(hour=9, minute=0, second=0),
                        current_date.replace(hour=16, minute=0, second=0),
                    )
                )
                next_day = current_date + pd.DateOffset(days=1)
                time_slots.append(
                    (
                        current_date.replace(hour=17, minute=0, second=0),
                        next_day.replace(hour=8, minute=0, second=0),
                    )
                )
            elif current_date.weekday() == 4:  # It's Friday
                time_slots.append(
                    (
                        current_date.replace(hour=9, minute=0, second=0),
                        current_date.replace(hour=16, minute=0, second=0),
                    )
                )
                next_monday = current_date + pd.DateOffset(
                    days=(7 - current_date.weekday() % 7)
                )
                time_slots.append(
                    (
                        current_date.replace(hour=17, minute=0, second=0),
                        next_monday.replace(hour=8, minute=0, second=0),
                    )
                )
            current_date += pd.DateOffset(days=1)
        return time_slots

    def optimize(self, quantile="0.5"):
        recommendations = {}

        # Convert date to datetime
        start_date = min(
            pd.to_datetime(df["quantiles"].index.min())
            for df in self.forecasts.values()
        )
        end_date = max(
            pd.to_datetime(df["quantiles"].index.max())
            for df in self.forecasts.values()
        )

        # Generate the time slots
        time_slots = self.generate_time_slots(start_date, end_date)

        # Loop through all series in forecasts
        for series_name in self.forecasts:
            # Make sure our index is a DateTimeIndex
            df = self.forecasts[series_name]["quantiles"].copy()
            df.index = pd.to_datetime(df.index)

            # Loop through all time slots
            for start_time_slot, end_time_slot in time_slots:
                # Use sum_between_dates function to sum the data within this time slot
                sum_quantile = self.sum_between_dates(
                    df, start_time_slot, end_time_slot, quantile
                )

                # Add the sum for this time slot to the recommendations
                timeslot_str = f"{start_time_slot.strftime('%A / %Y-%m-%d %H:%M:%S')} - {end_time_slot.strftime('%A / %Y-%m-%d %H:%M:%S')}"
                if timeslot_str not in recommendations:
                    recommendations[timeslot_str] = 0
                recommendations[timeslot_str] += sum_quantile

        return recommendations
