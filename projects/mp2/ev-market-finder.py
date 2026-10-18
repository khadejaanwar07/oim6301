# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "marimo",
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
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    I left out Venezuela, Cuba, Haiti and Puerto Rico on purpose. The first three have been removed due to sanctions, a very small private car market or instability, and Puerto Rico because it has been remvoved since it follows US trade rules, which put very high tariffs on Chinese EVs.
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

    I opened the World Bank and REST Countries addresses in my browser first. The World Bank sends back a list of two parts: the first part is about pages (page, pages, per_page, total) and the second is the actual countries. When a country has no value for an indicator, the second part comes back empty (null). REST Countries sends a list of countries, and each one has a `car` field with the side of the road it drives on.

    **Steps**

    1. Get every country the World Bank puts in Latin America & Caribbean (region code LCN), page by page, and check that I have as many as the total it reports.
    2. Ask REST Countries which side of the road China drives on, then get the driving side and languages of every country in the Americas.
    3. Keep the countries that speak Spanish, Portuguese or French, drive on the same side as China, and are not on my exclusion list. Keep a list of the ones I drop and why.
    4. For each country left, ask the World Bank for its latest GDP per person and its fuel imports as a share of all imports, along with the year each number is from.
    5. Mark each country pass, fail or no data against my limits ($8,000 GDP per person, 15% fuel share), and work out how many years of average income the $20,000 car costs there.
    6. Save the records to a CSV in projects/mp2/data/.
    7. Rank the countries that pass by fuel share, highest first, since that is where expensive imported fuel hurts most, then print a table and one sentence naming the top market.

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

    **Which check will I use in section 6, and which two numbers should agree?**

    1. The number of countries I collected should equal the World Bank's reported total.
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
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 4. The Work

    Add as many cells as you need. Try each step yourself before you ask your agent, and commit as you go.
    """)
    return


@app.cell
def _():
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 5. The Answer

    *A table of your results in the cell below, printed with `print` and f-strings, then one sentence here that answers the question in section 1, with the number in it.*
    """)
    return


@app.cell
def _():
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
