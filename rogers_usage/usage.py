
import re
import lxml.html

from collections import namedtuple

DailyBreakdown = namedtuple('DailyBreakdown', ['detail', 'totals'])

# -- URLs --
current_usage_url = 'https://www.rogers.com/web/myrogers/internetUsageBeta?actionTab=CurrentUsageSummary'
monthly_history_url = 'https://www.rogers.com/web/myrogers/internetUsageBeta?actionTab=PreviousMonthlyHistory'
day_to_day_url = 'https://www.rogers.com/web/myrogers/internetUsageBeta?actionTab=DayToDay'

def _condense_whitespace(string):
    # Note: \xa0 is Unicode non-breakable space, for whatever reason even
    #       re.UNICODE couldn't get \s to match it.
    return re.sub(r'[\s\xa0]+', ' ', string, re.UNICODE | re.M).strip()

def _format_cell_data(cell):
    cell_data = cell.text_content()
    cell_data = cell_data.strip()
    return _condense_whitespace(cell_data)

def current_usage_info(session):
    response = session.get(current_usage_url)
    html = lxml.html.fromstring(response.text)

    def convert(text):
        m = re.search(r'(\d+(?:\.\d+)?) GB', text)
        if m:
            return float(m.group(1))

        m = re.search(r'(\d+(?:\.\d+)?) MB', text)
        if m:
            return float(m.group(1)) / 1024.0

    tds = html.cssselect('#usageInformation')[0].xpath('.//td')
    info = {
        'download_usage': convert(_condense_whitespace(tds[2].text_content())),
        'upload_usage'  : convert(_condense_whitespace(tds[4].text_content())),
        'total_usage'   : convert(_condense_whitespace(tds[6].text_content())),
        'allowance'     : convert(_condense_whitespace(tds[8].text_content())),
        'billing_period': re.sub(r'Details for ?', '', _condense_whitespace(html.cssselect('#currentBillingPeriod')[0].text_content())),
    }
    info['left'] = info['allowance'] - info['total_usage']

    return info

def previous_monthly_usage(session):
    response = session.get(monthly_history_url)
    html = lxml.html.fromstring(response.text)

    rows = html.cssselect(".internetUsageDataContainer tr")
    result = []
    for row in rows:
        result.append(map(_format_cell_data, row.cssselect('td')))

    return result

def current_month_daily_breakdown(session):
    summary_markers = [
        '',
        'Total Usage (GB)',
        'Usage Allowance',
        'Additional Use',
        'Usage',
    ]

    response = session.get(day_to_day_url)
    html = lxml.html.fromstring(response.text)
    rows = html.cssselect(".internetUsageDataContainer .mainSection tr")
    data = []
    summary = []

    for row in rows:
        row = map(_format_cell_data, row.cssselect('td'))
        if row[0] in summary_markers:
            cleaned = [ td for td in row if td ]
            if len(cleaned):
                summary.append(cleaned)
        else:
            data.append(row)

    return DailyBreakdown(data, summary)
