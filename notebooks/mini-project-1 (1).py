# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "marimo",
# ]
# ///
"""Mini Project 1.
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
    # Mini Project 1

    Your choice of project, what each one asks for, the due date and how it is graded are on the Mini Project 1 page of the course site, linked from the calendar. This notebook is the shape to build it in. Keep the headings, and replace each line in italics with your own.

    Save it in your course repository as `projects/mp1/<your-tool>.py`, named for what it does, such as `loan-schedule.py`, and open it with `uv run marimo edit`.
    """)
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
    Babson graduate student has a monthly entertainment budget and wants to see a Boston
    pro sports game this fall. There are 22 upcoming home games which include 5 Patriots games at
    Gillette Stadium, 8 Celtics and 9 Bruins games at TD Garden. This section names
    the three teams and their venues rather than listing every game. The full list with
    each game's date, opponent, and prices is in section 3. A game costs more than the
    ticket, because getting there from Babson, food, and other spending add up.

    **Which of these games is the best value for the student given their budget and
    how they plan to get there?**

    The tool adds up the full cost of each game (ticket, round-trip transportation from Babson, food, and other spending) which shows what share of the monthly budget it uses, labels each game from Excellent Value to Over Budget, and names the game that uses the smallest share. Changing the budget or the transportation method in section 3 updates every result.

    Prices are representative estimates and all of the data was last checked on 11/8/2026
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 2. My Plan Before AI

    *Before you ask your agent anything, write how you would solve it: the steps, in order, in plain words, in five lines or more. Then answer these two questions:*

    - *What does your loop carry from one step to the next, the way a running total carries its sum?*
    - *Which check will you use in section 6, and which two numbers should agree?*

    *Commit this notebook with the message `mp1: plan before AI`.*
    """)
    return


@app.cell
def _():
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 2. My Plan Before AI

    **Inputs**

    - The student's monthly entertainment budget (for example $150)
    - The student's transportation method: MBTA, Rideshare, or Drive
    - 22 upcoming games, each with a date, team, opponent, venue, ticket price, food
      estimate, and other spending
    - The round-trip cost from Babson to each venue (TD Garden and Gillette Stadium) for
      each transportation method

    **Steps**

    1. Start with no "cheapest game so far" as the starting value of the loop.
    2. Go through the games one at a time. For each game:
        - Look up the transportation cost for its venue and the student's method.
        - Add up the total: ticket + transportation + food + other.
        - Divide the total by the budget to get the % of the budget it uses.
        - Give it a label: under 40% is Excellent Value, 40% to under 60% is Good Value,
          60% to under 80% is Expensive, 80% to 100% is Poor Fit and over 100% is Over Budget.
        - If it uses a smaller percentage than the cheapest game so far, it becomes the new cheapest.
        - Save its results for the table.
    3. Print a table with one row per game with the date, team, opponent, ticket, transport, food,
       other, total, percentage of budget and label.
    4. Print one sentence naming the best-value game, with its date, total, and % of budget.

    **What does my loop carry from one step to the next?**

    The cheapest game found so far and the percentage of the budget it uses. Each game is compared
    against it so after the last game it holds the answer. The loop also builds up the
    list of results that the table prints.

    **Which check will I use in section 6, and which two numbers should agree?**

    I will work out the total and % of the budget for one game, for example Celtics vs. Nets on Oct 27,
    by hand and compare my numbers next to the program's since they should be the same. As a second
    check, tickets + transport + food + other added up over all 22 games should equal the
    22 totals added up.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 3. Inputs

    Every number the project starts from goes in the cell below, and nowhere else, so that changing one input changes every result after it.

    Copy in the default inputs for your project from the Mini Project 1 page. If you chose your own project, type your data in here, or ask your agent to generate it with `faker`. The required part reads no file.
    """)
    return


@app.cell
def _():
    # Your inputs.
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
