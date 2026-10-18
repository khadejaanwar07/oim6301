# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "marimo",
#     "requests==2.34.2",
# ]
# ///
"""Mini Project 2.
"""

import marimo

__generated_with = "0.25.1"
app = marimo.App(width="medium", sql_output="polars")


@app.cell
def _():
    import marimo as mo

    return (mo,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Mini Project 2

    Your choice of project, what each one asks for, the due date and how it is graded are on the Mini Project 2 page of the course site, linked from the calendar. This notebook is the shape to build it in. Keep the headings, and replace each line in italics with your own.
    """)
    return


@app.cell
def _():
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 1. The Question

    *Who would use this, and what decision does it help them make? Two or three sentences, in words somebody outside this course would understand.*
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    A Chinese carmaker wants to launch a $20,000 electric car in Latin America. Brazil and Mexico are getting harder to enter, with rising tariffs and BYD already selling most of the EVs there, so the strategy team wants to know which other markets are worth a closer look. This tool gives them a shortlist of countries where the car can be shipped exactly as it is built in China, where people can realistically afford it, and where buying imported fuel gives drivers a reason to switch to electric.

    I left out Venezuela, Cuba, Haiti and Puerto Rico on purpose: the first three because of sanctions, a very small private car market, or instability, and Puerto Rico because it follows US trade rules, which put very high tariffs on Chinese EVs. I also left out Brazil and Mexico, because tariffs are going up there and BYD already sells most of the EVs.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 2. My Plan Before AI

    *Before you ask your agent anything, write how you would solve it: the steps, in order, in plain words, in five lines or more. Then answer these two questions:*

    - *What does your loop carry from one step to the next, the way a running total carries its sum?*
    - *Which check will you use in section 6, and which two numbers should agree?*

    *Commit this notebook with the message `mp2: plan before AI`.*
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # 2. My Plan Before AI

    My tool uses two free, public data sources. The World Bank publishes economic figures for every country, such as average income and what each country imports. REST Countries publishes basic facts about each country, including its languages and which side of the road it drives on.

    **Steps**

    1. Get the list of countries the World Bank puts under Latin America & Caribbean. It only sends 20 at a time, so I'll have to ask for each page and put them together into one list. Then check my list has the same number of countries as the total the World Bank gives.
    2. Look up which side of the road China drives on, since that's how the car is built. Then get the driving side and languages for every country in the Americas from REST Countries.
    3. Narrow the list down. Keep a country if it speaks Spanish, Portuguese or French, drives on the same side as China, and isn't one I'm leaving out (Venezuela, Cuba, Haiti, Puerto Rico). I'll keep track of which countries got dropped and why.
    4. For each country that's left, get its GDP per person (average income in US dollars) and what percent of its imports is fuel. Also save the year for each number, since some countries have older data than others.
    5. A country passes if GDP per person is $8,000 or more and fuel is 15% or more of its imports. If one of the numbers is missing I'll mark it "no data" instead. I'll also figure out how many years of average income the $20,000 car would cost in each country.
    6. Sort the countries that passed by fuel share, highest first, because those are the ones where depending on imported fuel hurts the most. Print a table and a sentence that says which country is the best bet and why.
    7. The point of all this is to help a Chinese EV company figure out where in Latin America its $20,000 car makes the most sense to sell, and at the end I should have a short ranked list of countries that pass all three filters, with the top one named.

    **What does my loop carry from one step to the next, the way a running total carries its sum?**

    My loops carry a list that grows instead of a number that grows. When I go through the World Bank's pages, the list of countries collected so far gets each new page's countries added to it, so after the last page it covers the whole region. When I go through the potential countries to consider, the list of country records gets one new record each time, with that country's GDP per person, fuel share, years of income and whether it passed. A running total ends with one sum; my lists end with one row per country.

    **Which check will I use in section 6, and which two numbers should agree?**

    1. The number of countries I collected should equal the total the World Bank reports on its first page.
    2. For the top country, total GDP divided by population for the same year should be close to the GDP per person the World Bank publishes.

    **Which functions will my tool need?**

    - `get_country_page(region, page, per_page)`: a region code and a page number go in; one page of the World Bank's reply comes out.
    - `get_region_countries(region)`: a region code goes in; a list of every country in it comes out (code, name, income group).
    - `get_driving_side(country_code)`: a two-letter code goes in; "right" or "left" comes out.
    - `get_country_details(region_name)`: a REST Countries region goes in; a list of countries with their driving side and languages comes out.
    - `get_latest_value(country_code, indicator)`: a country and an indicator code go in; the latest value and its year come out.
    - `get_value_for_year(country_code, indicator, year)`: the same, but for one chosen year. I need this for the check.

    **Which addresses will they request?**

    - `https://api.worldbank.org/v2/country?region=LCN&format=json&page=1&per_page=20`
    - `https://api.worldbank.org/v2/country/{code}/indicator/{indicator}?format=json&mrnev=1`
    - `https://restcountries.com/v3.1/alpha?codes=CN&fields=cca2,car`
    - `https://restcountries.com/v3.1/region/americas?fields=cca2,car,languages`

    **How will I know I have every record?**

    The World Bank's first page tells me how many pages and how many countries there are. I'll ask for 20 per page so the region takes more than one page and my page loop actually gets used. Then I'll compare the number of countries I collected with the total it reports.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 3. Inputs

    Every number the project starts from goes in the cell below, and nowhere else, so that changing one input changes every result after it.

    Copy in the default inputs for your project from the Mini Project 2 page. If you chose your own project, type your data in here, or ask your agent to generate it with `faker`. The required part reads no file.
    """)
    return


@app.cell
def _():
    # Where the data comes from
    region_code = "LCN"
    americas_region = "americas"
    home_country_code = "CN"
    latin_languages = ["Spanish", "Portuguese", "French"]
    excluded_countries = ["VE", "CU", "HT", "PR", "BR", "MX"]
    page_size = 20

    # The car and the filters
    car_price_dollars = 20000
    min_gdp_per_person = 8000
    min_fuel_import_share = 15

    # World Bank indicators
    gdp_indicator = "NY.GDP.PCAP.CD"
    fuel_indicator = "TM.VAL.FUEL.ZS.UN"
    total_gdp_indicator = "NY.GDP.MKTP.CD"
    population_indicator = "SP.POP.TOTL"

    # Section 6 check
    check_tolerance_percent = 1

    # Going further
    fuel_limits_to_test = [10, 15, 20, 25]
    renewable_indicator = "EG.ELC.RNEW.ZS"
    return (
        americas_region,
        car_price_dollars,
        home_country_code,
        min_fuel_import_share,
        min_gdp_per_person,
        page_size,
        region_code,
    )


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 4. The Work

    Add as many cells as you need. Try each step yourself before you ask your agent, and commit as you go.
    """)
    return


@app.cell
def _():
    import requests

    return (requests,)


@app.cell
def _(requests):
    def get_country_page(region, page, per_page):
        page_reply = requests.get(
            "https://api.worldbank.org/v2/country",
            params={"region": region, "format": "json", "page": page, "per_page": per_page},
            timeout=10,
        )
        return page_reply.json()

    return (get_country_page,)


@app.cell
def _(get_country_page):
    def get_region_countries(region, per_page):
        first_page = get_country_page(region, 1, per_page)
        pages = first_page[0]["pages"]

        all_rows = []
        for row in first_page[1]:
            all_rows.append(row)
        for page in range(2, pages + 1):
            next_page = get_country_page(region, page, per_page)
            for row in next_page[1]:
                all_rows.append(row)

        countries = []
        for row in all_rows:
            countries.append(
                {
                    "code": row["iso2Code"],
                    "name": row["name"],
                    "income_group": row["incomeLevel"]["value"],
                }
            )
        return countries

    return (get_region_countries,)


@app.cell
def _(get_region_countries, page_size, region_code):
    latam_countries = get_region_countries(region_code, page_size)
    len(latam_countries)
    return


@app.cell
def _(requests):
    def get_driving_side(country_code):
        side_reply = requests.get(
            "https://restcountries.com/v3.1/alpha",
            params={"codes": country_code, "fields": "cca2,car"},
            timeout=10,
        )
        return side_reply.json()[0]["car"]["side"]

    return (get_driving_side,)


@app.cell
def _(requests):
    def get_country_details(region_name):
        details_reply = requests.get(
            f"https://restcountries.com/v3.1/region/{region_name}",
            params={"fields": "cca2,car,languages"},
            timeout=10,
        )
        details = []
        for country in details_reply.json():
            language_names = []
            for code, language in country.get("languages", {}).items():
                language_names.append(language)
            details.append(
                {
                    "code": country["cca2"],
                    "driving_side": country["car"]["side"],
                    "languages": language_names,
                }
            )
        return details

    return (get_country_details,)


@app.cell
def _(
    americas_region,
    get_country_details,
    get_driving_side,
    home_country_code,
):
    home_side = get_driving_side(home_country_code)
    americas_details = get_country_details(americas_region)
    home_side, len(americas_details)
    return


@app.cell
def _(requests):
    print(requests.get(
        "https://restcountries.com/v3.1/alpha",
        params={"codes": "CN", "fields": "cca2,car"},
        timeout=10,
    ).json())
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 5. The Answer

    *A table of your results in the cell below, printed with `print` and f-strings, then one sentence here that answers the question in section 1, with the number in it.*
    """)
    return


@app.cell
def _(not_passed, ranked_shortlist):
    print("Countries that pass all three filters, highest fuel share first")
    print()
    print(f"{'Country':<22}{'GDP/person':>12}{'Year':>6}{'Fuel % imports':>16}{'Year':>6}{'Years of income':>17}")
    for _r in ranked_shortlist:
        print(
            f"{_r['name']:<22}"
            f"{_r['gdp_per_person']:>12,.0f}"
            f"{_r['gdp_year']:>6}"
            f"{_r['fuel_import_share']:>16.1f}"
            f"{_r['fuel_year']:>6}"
            f"{_r['years_of_income']:>17.1f}"
        )

    print()
    print("Countries that did not pass")
    print()
    print(f"{'Country':<22}{'Status':<10}{'Why':<28}")
    for _r in not_passed:
        print(f"{_r['name']:<22}{_r['status']:<10}{_r['failed_rules']:<28}")
    return


@app.cell
def _(
    candidates,
    car_price_dollars,
    min_fuel_import_share,
    min_gdp_per_person,
    ranked_shortlist,
):
    if len(ranked_shortlist) == 0:
        answer_sentence = (
            f"No Latin American country that drives on China's side has GDP per person of at least "
            f"${min_gdp_per_person:,} and fuel at {min_fuel_import_share}% or more of its imports, "
            f"so the limits need another look before picking a market."
        )
    else:
        _best = ranked_shortlist[0]
        _names = []
        for _r in ranked_shortlist:
            _names.append(_r["name"])
        answer_sentence = (
            f"{_best['name']} looks like the best first market for the ${car_price_dollars:,} EV: "
            f"GDP per person is ${_best['gdp_per_person']:,.0f} ({_best['gdp_year']}), so the car costs "
            f"about {_best['years_of_income']} years of average income, and fuel is "
            f"{_best['fuel_import_share']:.1f}% of everything it imports ({_best['fuel_year']}). "
            f"{len(ranked_shortlist)} of {len(candidates)} countries passed: {', '.join(_names)}."
        )

    print(answer_sentence)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 6. How I Know These Numbers Are Right

    *At least one check that reaches a result a second, independent way. Name what you compared and what came out.*
    """)
    return


@app.cell
def _():
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 7. Working With the Agent

    *Pick one piece of AI output you did not accept as-is. What did it give you, what did you change, and how did you know? Point to the commit or the cell.*

    *If the agent got it right the first time: what did you do to verify that?*
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 8. Going Further

    *Take at least one step past the main task, in any direction, and use your agent as much as you like. It does not have to work. State what you tried, what you found, and where it is in this notebook.*
    """)
    return


if __name__ == "__main__":
    app.run()
