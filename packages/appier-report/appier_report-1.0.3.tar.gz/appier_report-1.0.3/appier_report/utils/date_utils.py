from datetime import datetime, timedelta


class DateUtils:
    @staticmethod
    def get_date_ranges(start_date: str, end_date: str, date_interval: int = 5) -> list[tuple[str, str]]:
        """
        Get a list of date ranges from **start_date** to **end_date** with **date_interval** days apart.

        Args:
            start_date: Format: YYYY-MM-DD
            end_date: Format: YYYY-MM-DD
            date_interval: Number of days between each date range.
        Returns:
            A list of date ranges in the format of (start_date, end_date).
        """
        date_ranges = []
        start_date = datetime.strptime(start_date, "%Y-%m-%d")
        end_date = datetime.strptime(end_date, "%Y-%m-%d")
        while start_date <= end_date:
            temp_end_date = start_date + timedelta(days=date_interval - 1)
            if temp_end_date > end_date:
                date_ranges.append((start_date.strftime("%Y-%m-%d"), end_date.strftime("%Y-%m-%d")))
                break
            else:
                date_ranges.append((start_date.strftime("%Y-%m-%d"), temp_end_date.strftime("%Y-%m-%d")))
                start_date += timedelta(days=date_interval)
        return date_ranges
