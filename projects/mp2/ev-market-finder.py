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

__generated_with = "0.24.2"
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
    My tool gets its data from the World Bank, which publishes economic numbers for every country, like average income and what each country imports. I also need to know which countries are in Latin America and drive on the same side as China. REST Countries used to give that for free, but its free version has been retired and the new one needs a key. Since every Spanish, Portuguese and French speaking country in Latin America drives on the right like China, I'll type that list into my inputs instead.

    **Steps**

    1. Get the list of countries the World Bank puts under Latin America & Caribbean. It only sends 20 at a time, so I'll have to ask for each page and put them together into one list. Then check my list has the same number of countries as the total the World Bank gives.
    2. Narrow the list down. Keep a country if it's on my list of Latin American countries and isn't one I'm leaving out (Venezuela, Cuba, Haiti, Puerto Rico, Brazil, Mexico). I'll keep track of which countries got dropped and why.
    3. For each country that's left, get its GDP per person (average income in US dollars) and what percent of its imports is fuel. Also save the year for each number, since some countries have older data than others.
    4. A country passes if GDP per person is $8,000 or more and fuel is 15% or more of its imports. If one of the numbers is missing I'll mark it "no data" instead. I'll also figure out how many years of average income the $20,000 car would cost in each country.
    5. Save everything to a CSV in projects/mp2/data/.
    6. Sort the countries that passed by fuel share, highest first, because those are the ones where depending on imported fuel hurts the most. Print a table and a sentence that says which country is the best bet and why.

    The point of all this is to help a Chinese EV company figure out where in Latin America its $20,000 car makes the most sense to sell, and at the end I should have a short ranked list of countries that pass all three filters, with the top one named.

    **What does my loop carry from one step to the next, the way a running total carries its sum?**

    My loops carry a list that grows instead of a number that grows. When I go through the World Bank's pages, the list of countries collected so far gets each new page's countries added to it, so after the last page it covers the whole region. When I go through the countries that are left, the list of country records gets one new record each time, with that country's GDP per person, fuel share, years of income and whether it passed. A running total ends with one sum; my lists end with one row per country.

    **Which check will I use in section 6, and which two numbers should agree?**

    1. The number of countries I collected should equal the total the World Bank reports on its first page.
    2. For the top country, total GDP divided by population for the same year should be close to the GDP per person the World Bank publishes.

    **Which functions will my tool need?**

    - `get_country_page(region, page, per_page)`: a region code, a page number and a page size go in; one page of the World Bank's reply comes out.
    - `get_region_countries(region, per_page)`: a region code and a page size go in; a list of every country in it comes out (code, name, income group).
    - `get_latest_value(country_code, indicator)`: a country and an indicator code go in; the latest value and its year come out.
    - `get_value_for_year(country_code, indicator, year)`: the same, but for one chosen year. I need this for the check.

    **Which addresses will they request?**

    - `https://api.worldbank.org/v2/country?region=LCN&format=json&page=1&per_page=20`
    - `https://api.worldbank.org/v2/country/{code}/indicator/{indicator}?format=json&mrnev=1`
    - `https://api.worldbank.org/v2/country/{code}/indicator/{indicator}?format=json&date={year}`

    **How will I know I have every record?**

    The World Bank's first page tells me how many pages and how many countries there are. I'll ask for 20 per page so the region takes more than one page and my page loop actually gets used. Then I'll compare the number of countries I collected with the total it reports.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    My original plan is in my first "mp2: plan before AI" commit. I revised it in "mp2: plan before AI (final)" after REST Countries turned out to need a key (see section 7).
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
    page_size = 20

    # Spanish-, Portuguese- and French-speaking countries in the World Bank's
    # Latin America & Caribbean group. All drive on the right, like China,
    # so the car ships without changes.
    latin_american_codes = [
        "AR", "BO", "BR", "CL", "CO", "CR", "CU", "DO", "EC", "SV", "GT",
        "HT", "HN", "MX", "NI", "PA", "PY", "PE", "PR", "UY", "VE",
    ]

    # Venezuela, Cuba, Haiti, Puerto Rico, Brazil, Mexico
    excluded_countries = ["VE", "CU", "HT", "PR", "BR", "MX"]

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
        car_price_dollars,
        check_tolerance_percent,
        excluded_countries,
        fuel_indicator,
        fuel_limits_to_test,
        gdp_indicator,
        latin_american_codes,
        min_fuel_import_share,
        min_gdp_per_person,
        page_size,
        population_indicator,
        region_code,
        renewable_indicator,
        total_gdp_indicator,
    )


@app.cell
def _():
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 4. The Work

    Add as many cells as you need. Try each step yourself before you ask your agent, and commit as you go.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Every country in the region
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

    print(f"{len(latam_countries)} countries in the region:")
    for _country in latam_countries:
        print(_country["name"])
    return (latam_countries,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Filter 1: Latin American, same side of the road as China, not left out

    My plan used REST Countries for driving side and languages, but it retired its free address after I wrote the plan, and the new version needs a key. Since every Spanish, Portuguese and French speaking country in Latin America drives on the right like China, I typed that list into the Inputs cell instead. All the economic data still comes live from the World Bank.
    """)
    return


@app.cell
def _(excluded_countries, latam_countries, latin_american_codes):
    candidates = []
    screened_out = []
    for _country in latam_countries:
        if _country["code"] in excluded_countries:
            screened_out.append((_country["name"], "left out by choice"))
        elif _country["code"] in latin_american_codes:
            candidates.append(
                {
                    "code": _country["code"],
                    "name": _country["name"],
                    "income_group": _country["income_group"],
                }
            )
        else:
            screened_out.append((_country["name"], "not Latin American, or drives on the left"))

    len(candidates), len(screened_out)
    return (candidates,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Filters 2 and 3: GDP per person and fuel share of imports
    """)
    return


@app.cell
def _(requests):
    def get_latest_value(country_code, indicator):
        value_reply = requests.get(
            f"https://api.worldbank.org/v2/country/{country_code}/indicator/{indicator}",
            params={"format": "json", "mrnev": 1},
            timeout=10,
        )
        value_page = value_reply.json()

        result = {"value": None, "year": None}
        if len(value_page) == 2:
            if value_page[1] is None:
                result = {"value": None, "year": None}
            else:
                result = {"value": value_page[1][0]["value"], "year": value_page[1][0]["date"]}
        return result

    return (get_latest_value,)


@app.cell
def _(
    candidates,
    car_price_dollars,
    fuel_indicator,
    gdp_indicator,
    get_latest_value,
    min_fuel_import_share,
    min_gdp_per_person,
):
    country_records = []
    for _country in candidates:
        _gdp = get_latest_value(_country["code"], gdp_indicator)
        _fuel = get_latest_value(_country["code"], fuel_indicator)

        _failed_rules = []
        _years_of_income = None
        if _gdp["value"] is None:
            _status = "no data"
            _failed_rules.append("no GDP data")
        elif _fuel["value"] is None:
            _status = "no data"
            _failed_rules.append("no fuel data")
        else:
            _years_of_income = round(car_price_dollars / _gdp["value"], 1)
            if _gdp["value"] < min_gdp_per_person:
                _failed_rules.append("GDP per person")
            if _fuel["value"] < min_fuel_import_share:
                _failed_rules.append("fuel share")
            if len(_failed_rules) == 0:
                _status = "pass"
            else:
                _status = "fail"

        country_records.append(
            {
                "name": _country["name"],
                "code": _country["code"],
                "income_group": _country["income_group"],
                "gdp_per_person": _gdp["value"],
                "gdp_year": _gdp["year"],
                "fuel_import_share": _fuel["value"],
                "fuel_year": _fuel["year"],
                "years_of_income": _years_of_income,
                "status": _status,
                "failed_rules": ", ".join(_failed_rules),
            }
        )

    len(country_records)
    return (country_records,)


@app.cell
def _():
    ### Saving what I fetched
    return


@app.cell
def _(country_records, mo):
    _lines = ["name,code,income_group,gdp_per_person,gdp_year,fuel_import_share,fuel_year,years_of_income,status"]
    for _r in country_records:
        _lines.append(
            f'"{_r["name"]}",{_r["code"]},"{_r["income_group"]}",{_r["gdp_per_person"]},'
            f'{_r["gdp_year"]},{_r["fuel_import_share"]},{_r["fuel_year"]},{_r["years_of_income"]},{_r["status"]}'
        )

    _data_dir = mo.notebook_dir() / "data"
    try:
        _data_dir.mkdir(parents=True, exist_ok=True)
        screen_csv = _data_dir / "latam_ev_screen.csv"
        screen_csv.write_text("\n".join(_lines) + "\n")
        _where = f"wrote {screen_csv.parent.name}/{screen_csv.name}"
    except OSError as _error:
        _where = f"could not write into {_data_dir.name}/: {_error}"

    _where
    return


@app.cell
def _():
    ### Sorting the results
    return


@app.cell
def _(country_records):
    shortlist = []
    tested_records = []
    not_passed = []
    for _r in country_records:
        if _r["status"] == "pass":
            shortlist.append(_r)
            tested_records.append(_r)
        elif _r["status"] == "fail":
            tested_records.append(_r)
            not_passed.append(_r)
        else:
            not_passed.append(_r)

    _ranking = []
    for _r in shortlist:
        _ranking.append((_r["fuel_import_share"], _r["code"]))

    ranked_shortlist = []
    for _share, _code in sorted(_ranking, reverse=True):
        for _r in shortlist:
            if _r["code"] == _code:
                ranked_shortlist.append(_r)

    len(ranked_shortlist), len(not_passed)
    return not_passed, ranked_shortlist, tested_records


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


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Check 1 The number of countries I collected should match the total the World Bank reports.
    """)
    return


@app.cell
def _(get_country_page, latam_countries, page_size, region_code):
    reported_total = get_country_page(region_code, 1, page_size)[0]["total"]
    print(f"Countries I collected:      {len(latam_countries)}")
    print(f"World Bank says there are:  {reported_total}")
    print(f"Same: {len(latam_countries) == reported_total}")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Check 2 - For the top country, total GDP divided by population (same year) should be really close to the GDP per person the World Bank reports.
    """)
    return


@app.cell
def _(requests):
    def get_value_for_year(country_code, indicator, year):
        year_reply = requests.get(
            f"https://api.worldbank.org/v2/country/{country_code}/indicator/{indicator}",
            params={"format": "json", "date": year},
            timeout=10,
        )
        year_page = year_reply.json()

        value = None
        if len(year_page) == 2:
            if year_page[1] is None:
                value = None
            else:
                value = year_page[1][0]["value"]
        return value

    return (get_value_for_year,)


@app.cell
def _(
    check_tolerance_percent,
    get_value_for_year,
    population_indicator,
    ranked_shortlist,
    tested_records,
    total_gdp_indicator,
):
    if len(ranked_shortlist) > 0:
        _check = ranked_shortlist[0]
    else:
        _check = tested_records[0]

    _total_gdp = get_value_for_year(_check["code"], total_gdp_indicator, _check["gdp_year"])
    _population = get_value_for_year(_check["code"], population_indicator, _check["gdp_year"])
    _computed = _total_gdp / _population
    _difference = round((_computed - _check["gdp_per_person"]) / _check["gdp_per_person"] * 100, 2)

    _close = False
    if _difference < check_tolerance_percent:
        if _difference > -check_tolerance_percent:
            _close = True

    print(f"{_check['name']}, {_check['gdp_year']}")
    print(f"GDP per person (World Bank):  ${_check['gdp_per_person']:,.2f}")
    print(f"Total GDP / population:       ${_computed:,.2f}")
    print(f"Difference: {_difference}%   Within {check_tolerance_percent}%: {_close}")
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
    **What it gave me:** The agent wrote two functions, `get_driving_side` and `get_country_details`, that asked REST Countries which side of the road China and every country in the Americas drive on. The code looked fine, but when I ran it I got `KeyError: 0` on the line `return side_reply.json()[0]['car']['side']`.

    **How I knew something was wrong:** The error meant the reply wasn't a list like the code expected. I added a cell that printed the raw reply instead of picking pieces out of it, and the reply said this version of the API had been deprecated. The agent had written code for an address that no longer works the way it used to.

    **What I changed:** The new version of REST Countries needs an API key, which would have meant setting up a `.env` file and a new package. Since every Spanish, Portuguese and French speaking country in Latin America drives on the right like China, I deleted both functions and typed the list of Latin American country codes into my Inputs cell instead. I rewrote the filter cell to check each World Bank country against that list. The GDP and fuel data still comes live from the World Bank.

    **How I checked the fix:** The filter cell now shows (15, 27): 21 Latin American countries minus the 6 I leave out is 15, and 42 minus 15 is 27, which matches the World Bank's total of 42.

    You can see the fix in the Filter 1 cell in section 4 and in the country list in the Inputs cell.
    """)
    return


@app.cell
def _():
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Reading It Back

    ## get_region_countries

    **What goes in:** A region code, like "LCN" for Latin America & Caribbean, and how many countries to ask for on each page.

    **What comes out:** One list with every country in that region. Each country is a small record with its two-letter code, its name and its income group.

    **How it works:** It asks the World Bank for page 1 first, because that page also says how many pages there are in total. Then it goes through the rest of the pages one by one and adds each page's countries to the same list. At the end it keeps only the three fields I need from each country.

    **A line I had to ask about:** `for page in range(2, pages + 1):`. I didn't get why it starts at 2 and ends at pages + 1. It starts at 2 because page 1 was already fetched above the loop, and it's pages + 1 because range stops one before the last number, so to include the last page you have to go one past it. With 3 pages, range(2, 4) gives 2 and 3.

    ## get_latest_value

    **What goes in:** A country's two-letter code and the World Bank code for the number I want, like NY.GDP.PCAP.CD for GDP per person.

    **What comes out:** The most recent value the World Bank has for that country, and the year it's from. If there's no value, it gives back None for both instead of crashing.

    **How it works:** It asks the World Bank for one indicator for one country, with mrnev=1, which means "the most recent year that actually has a value." The reply comes back as two parts, info about the reply and then the data, so it takes the value and year from the second part.

    **A line I had to ask about:** `if value_page[1] is None:`. I didn't know why this was needed if the request worked. It turns out that when a country has no data for an indicator, the World Bank still answers, but the data part comes back empty (None). Without this check the code would try to read a value from nothing and stop with an error, so it would break the whole loop over one missing country.

    ## My prediction

    I'm changing `min_fuel_import_share` in the Inputs cell from 15 to 10.

    I expect the shortlist to grow from 4 countries to 6, because my Going Further table showed 6 countries passing at 10%. The 2 new countries should show up at the bottom of the ranking, since the list is sorted by fuel share and they have lower shares than the original four. Panama should still be the top market, so the answer sentence should still name Panama with the same numbers, but it should now say 6 of 15 countries passed instead of 4.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## What happened

    I changed min_fuel_import_share from 15 to 10 and the notebook reran everything after it. The shortlist grew from 4 countries to 6, as I predicted. The two new countries are Uruguay and Costa Rica, and they came in at the bottom of the ranking, since they import less fuel as a share of everything they buy than the original four. Panama stayed on top with the same numbers: GDP per person of $19,790 (2025), so the car costs about 1.0 years of average income, and fuel is 19.3% of its imports (2025). The answer sentence now says 6 of 15 countries passed: Panama, Dominican Republic, Peru, Chile, Uruguay and Costa Rica.

    It matched my prediction. The agents summary said the new countries were Peru and Costa Rica, but Peru was already on the list at 15%, so I checked the answer sentence against my earlier shortlist instead of trusting the summary.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 8. Going Further

    *Take at least one step past the main task, in any direction, and use your agent as much as you like. It does not have to work. State what you tried, what you found, and where it is in this notebook.*
    """)
    return


@app.cell
def _():
    ## How much does the shortlist depend on my 15% fuel limit?
    return


@app.cell
def _(fuel_limits_to_test, min_gdp_per_person, tested_records):
    print(f"{'Fuel limit %':>12}{'Countries passing':>19}")
    for _limit in fuel_limits_to_test:
        _count = 0
        for _r in tested_records:
            if _r["gdp_per_person"] >= min_gdp_per_person:
                if _r["fuel_import_share"] >= _limit:
                    _count = _count + 1
        print(f"{_limit:>12}{_count:>19}")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **What I tried:** I picked 15% as the cutoff for "depends on imported fuel," but that number was my own judgment, so I wanted to see what happens if the team picks a different one. I reran the same filter at 10%, 15%, 20% and 25%, using the data I already had, so it didn't need any new requests.

    **What I found:** At 10%, 6 countries passed. At 15% it was 4, and at 20% and 25% none passed. So every country on my shortlist gets between 15% and 20% of its imports from fuel, and the answer depends a lot on where the cutoff is. If the team decided "high dependence" means 20%, the tool would say no market qualifies. That's worth telling them, because the 15% line is a judgment call, not a hard rule.

    **Where it is:** The first cell in section 9. It uses `fuel_limits_to_test` from the Inputs cell, so the team can try other limits by changing that list.
    """)
    return


@app.cell
def _():
    ## Can the power grid charge the car cleanly?** Share of electricity from renewables for each country on the shortlist. This data is often a few years old, so I show the year.
    return


@app.cell
def _(get_latest_value, ranked_shortlist, renewable_indicator):
    print(f"{'Country':<22}{'Renewable % of power':>22}{'Year':>6}")
    for _r in ranked_shortlist:
        _renewable = get_latest_value(_r["code"], renewable_indicator)
        if _renewable["value"] is None:
            print(f"{_r['name']:<22}{'no data':>22}")
        else:
            print(f"{_r['name']:<22}{_renewable['value']:>22.1f}{_renewable['year']:>6}")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **What I tried:** An EV is only as cheap and clean as the electricity behind it, so for each country on the shortlist I asked the World Bank for the share of its electricity that comes from renewables.

    **What I found:** Panama had the highest renewable share at 69.0%, then Peru at 61.8%, Chile at 48.1%, and the Dominican Republic at 17.1%, all from 2021. Panama is also top of my main ranking, so it looks even stronger: drivers would be switching from imported fuel to mostly local clean power. The Dominican Republic is the weak spot. It passes the fuel filter, but most of its electricity still comes from fossil fuels, so the "run your car on local power" pitch doesn't really work there. The data is from 2021, so it shows the general picture rather than today's grid.

    One thing I'd check before trusting Panamas number: a lot of goods pass through Panama's canal and free trade zone, so its import figures might include fuel that gets sold on to other countries rather than used there.

    **Where it is:** The second cell in section 9. It uses `renewable_indicator` from the Inputs cell and the same `get_latest_value` function as the main task.
    """)
    return


@app.cell
def _(mo):
    mo.md(r"""
    ## 10. Time Spent

    6.5
    """)
    return


if __name__ == "__main__":
    app.run()
