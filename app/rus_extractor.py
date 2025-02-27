import calendar
from datetime import datetime
from pullenti_wrapper.processor import Processor, DATE, MONEY
from pullenti_wrapper.referent import DateReferent, MoneyReferent, DateRangeReferent

processor = Processor([DATE, MONEY])

def extract_entities(message):
    analysis_result = processor(message)

    dates = []
    date_intervals = []
    sums = []

    for entity in analysis_result.matches:
        referent = entity.referent
        if isinstance(referent, DateReferent):
            day = referent.day
            month = referent.month
            year = referent.year

            if day != 0 and month != 0 and year != 0:
                dates.append(f"{year}-{month:02d}-{day:02d}")
            elif day != 0 and month != 0:
                current_year = datetime.now().year
                dates.append(f"{current_year}-{month:02d}-{day:02d}")
            elif month != 0 and year != 0:
                last_day = calendar.monthrange(year, month)[1]
                date_intervals.append(f"{year}-{month:02d}-01|{year}-{month:02d}-{last_day}")
            elif month != 0:
                current_year = datetime.now().year
                last_day = calendar.monthrange(current_year, month)[1]
                date_intervals.append(f"{current_year}-{month:02d}-01|{current_year}-{month:02d}-{last_day}")

        elif isinstance(referent, MoneyReferent):
            sums.append(round(referent.value))
        elif isinstance(referent, DateRangeReferent):
            start_date = referent.slots[0].value
            start_day = start_date.day
            start_month = start_date.month
            start_year = start_date.year

            if start_day != 0 and start_month != 0 and start_year != 0:
                start_date_str = f"{start_year}-{start_month:02d}-{start_day:02d}"
            elif start_day != 0 and start_month != 0:
                current_year = datetime.now().year
                start_date_str = f"{current_year}-{start_month:02d}-{start_day:02d}"
            else:
                continue

            end_date = referent.slots[1].value
            end_day = end_date.day
            end_month = end_date.month
            end_year = end_date.year

            if end_day != 0 and end_month != 0 and end_year != 0:
                end_date_str = f"{end_year}-{end_month:02d}-{end_day:02d}"
            elif end_day != 0 and end_month != 0:
                current_year = datetime.now().year
                end_date_str = f"{current_year}-{end_month:02d}-{end_day:02d}"
            else:
                continue
            date_intervals.append(f"{start_date_str}|{end_date_str}")

    return {
        'dates': dates,
        'date_intervals': date_intervals,
        'moneys': sums
    }