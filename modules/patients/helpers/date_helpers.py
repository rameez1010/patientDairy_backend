from datetime import datetime, timedelta


def parse_collection_date(collection_date: str) -> str:
    """Parse and format collection date"""
    month_map = {
        "Jan": "01",
        "Feb": "02",
        "Mar": "03",
        "Apr": "04",
        "May": "05",
        "Jun": "06",
        "Jul": "07",
        "Aug": "08",
        "Sep": "09",
        "Oct": "10",
        "Nov": "11",
        "Dec": "12",
    }

    try:
        new_date = datetime.strptime(collection_date, "%Y-%m-%d")
        new_date += timedelta(days=1)
        return new_date.strftime("%Y-%m-%d")
    except ValueError:
        pass

    try:
        year, month_str, day = collection_date.split("-")
        month = month_map.get(month_str)
        if not month:
            raise ValueError(f"Invalid month abbreviation: {month_str}")

        new_date_str = f"{year}-{month}-{day}"
        new_date = datetime.strptime(new_date_str, "%Y-%m-%d")
        new_date += timedelta(days=1)
        return new_date.strftime("%Y-%m-%d")
    except ValueError:
        raise ValueError(f"Invalid date format: {collection_date}. Expected formats are YYYY-MM-DD or YYYY-Mon-DD.")
