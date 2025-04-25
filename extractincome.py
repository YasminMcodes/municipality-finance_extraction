import csv
import requests
from bs4 import BeautifulSoup
import pandas as pd
from collections import defaultdict


def clean_currency(v):
    return v.replace('.', '').replace(',', '.').replace('€', '').strip()


def fetch_all_income_data(slug: str, year: int):
    if year <= 2015:
        base = f"http://storico.openbilanci.it/bilanci/{slug}/entrate/dettaglio"
    else:
        base = f"https://openbilanci.it/armonizzati/bilanci/{slug}/entrate/dettaglio"

    variants = [
        f"{base}?year={year}&type=consuntivo&cas_com_type=cassa",
        f"{base}?year={year}&type=preventivo"
    ]

    soup = None
    for url in variants:
        try:
            resp = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
            resp.raise_for_status()
        except requests.RequestException:
            continue

        candidate = BeautifulSoup(resp.content, 'html.parser')
        content = candidate.find('div', id='content') or candidate.find('div', id='main-content')
        if content and content.find('div', class_='panel-heading'):
            soup = candidate
            print(url)
            break

    if soup is None:
        print(f"❌ None of the URL variants returned data for {slug}/{year}")
        return None

    content = soup.find('div', id='content')
    if not content:
        print(f"⚠️ No #content found for {slug}/{year}")
        return None

    all_headings = content.find_all('div', class_='panel-heading')

    data: dict[str, str] = {}
    for hd in all_headings:
        if hd.find_parent('div', class_='panel-collapse'):
            continue

        val_p = hd.find('p', class_='h3')
        if not val_p:
            continue
        raw = val_p.get_text(strip=True)
        value = clean_currency(raw)

        if (h2 := hd.find('h2')):
            label = h2.get_text(strip=True)
        elif (a := hd.find('a', attrs={'data-original-title': True})):
            label = a['data-original-title'].strip()
        else:
            entry = hd.find('div', class_='entry')
            if not entry:
                continue
            if (span := entry.find('span')):
                label = span.get_text(strip=True)
            else:
                texts = list(entry.stripped_strings)
                label = texts[1] if len(texts) > 1 else texts[0]

        data[label] = value
        print(f"✅ {label} → {value}")

    return data


# ─── Load CSV ──────────────────────────────────────────────────────
df = pd.read_csv("defaulted_municipalities.csv")  # must have 'municipality', 'province', 'year'

# ─── Loop and collect data ─────────────────────────────────────────
all_data = []
all_columns = set()

for _, row in df.iterrows():
    if pd.isna(row['Municipality']) or pd.isna(row['Province']):
        print(f"⚠️ Skipping row with missing municipality or province: {row.to_dict()}")
        continue

    municipality = str(row['Municipality']).strip().lower().replace(' ', '-')
    province = str(row['Province']).strip().lower()

    year = int(row['year'])
    slug = f"{municipality}-comune-{province}"

    print(f"Fetching: {slug} {year}")
    income_data = fetch_all_income_data(slug, year)

    row_data = {
        "municipality": row['Municipality'],
        "province": row['Province'],
        "year": year
    }

    if income_data:
        row_data.update(income_data)
        all_columns.update(income_data.keys())
    else:
        print(f"⚠️ No data for {slug} in {year}")

    all_data.append(row_data)

# ─── Write to CSV ──────────────────────────────────────────────────
final_columns = ['municipality', 'province', 'year'] + sorted(all_columns)
with open("income_data.csv", "w", newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=final_columns)
    writer.writeheader()
    for row in all_data:
        full_row = {col: row.get(col, "NA") for col in final_columns}
        writer.writerow(full_row)

print("✅ Saved to income_data.csv")
