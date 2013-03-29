
import re
import lxml.html
import session

current_usage_url = 'https://www.rogers.com/web/myrogers/internetUsageBeta?actionTab=CurrentUsageSummary'

def current_usage_info(session):
    response = session.get(current_usage_url)
    html = lxml.html.fromstring(response.text)

    def clean_text(text):
        # Note: \xa0 is Unicode non-breakable space, for whatever reason even
        #       re.UNICODE couldn't get \s to match it.
        return re.sub(r'[\s\xa0]+', ' ', text, re.UNICODE).strip()

    def convert(text):
        m = re.search(r'(\d+(?:\.\d+)?) GB', text)
        if m:
            return float(m.group(1))

        m = re.search(r'(\d+(?:\.\d+)?) MB', text)
        if m:
            return float(m.group(1)) / 1024.0

    tds = html.cssselect('#usageInformation')[0].xpath('.//td')
    info = {
        'download_usage': convert(clean_text(tds[2].text_content())),
        'upload_usage'  : convert(clean_text(tds[4].text_content())),
        'total_usage'   : convert(clean_text(tds[6].text_content())),
        'allowance'     : convert(clean_text(tds[8].text_content())),
        'billing_period': re.sub(r'Details for ?', '', clean_text(html.cssselect('#currentBillingPeriod')[0].text_content())),
    }
    info['left'] = info['allowance'] - info['download_usage']

    return info
