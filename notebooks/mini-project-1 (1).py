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

    1. Prices are representative estimates and all of the data was last checked on 11/8/2026
    2. The schedules come from Patriots.com and TDGarden.com. Four Celtics ticket prices are Vivid Seats listings, and the other prices are representative estimates. The MBTA costs are based on the $2.40 subway fare and the $20 Patriots event train.
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
    # All amounts are in US dollars
    monthly_budget = 150
    transport_mode = "MBTA"

    # Round-trip cost from Babson to each venue, one dictionary per way of getting there
    mbta_costs = {"TD Garden": 6, "Gillette": 25}
    rideshare_costs = {"TD Garden": 28, "Gillette": 50}
    drive_costs = {"TD Garden": 18, "Gillette": 30}
    # For the sake of simplicity of the model, dynamic pricing is not considered, and costs are pre-allocated based on data. 

    # One tuple per game: date, team, opponent, venue, ticket, food, other
    games = [
        ("2026-10-11", "Patriots", "Raiders", "Gillette", 95, 25, 10),
        ("2026-10-18", "Patriots", "Jets", "Gillette", 90, 25, 10),
        ("2026-10-22", "Bruins", "Predators", "TD Garden", 55, 20, 5),
        ("2026-10-23", "Celtics", "Knicks", "TD Garden", 181, 20, 5),
        ("2026-10-24", "Bruins", "Sharks", "TD Garden", 50, 20, 5),
        ("2026-10-26", "Celtics", "Bulls", "TD Garden", 49, 20, 5),
        ("2026-10-27", "Celtics", "Nets", "TD Garden", 41, 20, 5),
        ("2026-10-30", "Celtics", "Bulls", "TD Garden", 90, 20, 5),
        ("2026-10-31", "Bruins", "Blackhawks", "TD Garden", 70, 20, 5),
        ("2026-11-02", "Bruins", "Golden Knights", "TD Garden", 65, 20, 5),
        ("2026-11-04", "Celtics", "Bucks", "TD Garden", 70, 20, 5),
        ("2026-11-08", "Patriots", "Packers", "Gillette", 140, 25, 10),
        ("2026-11-08", "Bruins", "Panthers", "TD Garden", 85, 20, 5),
        ("2026-11-12", "Bruins", "Canadiens", "TD Garden", 110, 20, 5),
        ("2026-11-14", "Bruins", "Wild", "TD Garden", 60, 20, 5),
        ("2026-11-15", "Celtics", "Mavericks", "TD Garden", 65, 20, 5),
        ("2026-11-16", "Celtics", "Magic", "TD Garden", 55, 20, 5),
        ("2026-11-17", "Bruins", "Kings", "TD Garden", 60, 20, 5),
        ("2026-11-21", "Bruins", "Capitals", "TD Garden", 75, 20, 5),
        ("2026-11-27", "Celtics", "Hawks", "TD Garden", 75, 20, 5),
        ("2026-12-06", "Patriots", "Bills", "Gillette", 160, 25, 10),
        ("2026-12-10", "Patriots", "Vikings", "Gillette", 130, 25, 10),
    ]
    len(games)
    return (
        drive_costs,
        games,
        mbta_costs,
        monthly_budget,
        rideshare_costs,
        transport_mode,
    )


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 4. The Work

    Add as many cells as you need. Try each step yourself before you ask your agent, and commit as you go.
    """)
    return


@app.cell
def _(drive_costs, mbta_costs, rideshare_costs, transport_mode):
    #choosing the transport cost
    if transport_mode == "MBTA":
        transport_costs = mbta_costs
    elif transport_mode == "Rideshare":
        transport_costs = rideshare_costs
    else:
        transport_costs = drive_costs
    transport_costs
    return (transport_costs,)


@app.cell
def _():
    # The label function
    def value_label(percent):
        if percent < 40:
            return "Excellent Value"
        elif percent < 60:
            return "Good Value"
        elif percent < 80:
            return "Expensive"
        elif percent <= 100:
            return "Poor Fit"
        else:
            return "Over Budget"

    #check
    value_label(48)
    return (value_label,)


@app.cell
def _(games, monthly_budget, transport_costs, value_label):
    #The loop
    results = []
    cheapest_so_far = None
    for _date, _team, _opponent, _venue, _ticket, _food, _other in games:
        _transport = transport_costs[_venue]
        _total = _ticket + _transport + _food + _other
        _percent = _total / monthly_budget * 100
        _row = {
            "Date": _date,
            "Team": _team,
            "Opponent": _opponent,
            "Ticket": _ticket,
            "Transport": _transport,
            "Food": _food,
            "Other": _other,
            "Total": _total,
            "Percent": _percent,
            "Label": value_label(_percent),
        }
        results.append(_row)
        if cheapest_so_far is None:
            cheapest_so_far = _row
        elif _percent < cheapest_so_far["Percent"]:
            cheapest_so_far = _row
    cheapest_so_far
    return cheapest_so_far, results


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 5. The Answer

    *A table of your results in the cell below, printed with `print` and f-strings, then one sentence here that answers the question in section 1, with the number in it.*
    """)
    return


@app.cell
def _(results):
    print(f"{'Date':<12}{'Team':<10}{'Opponent':<16}{'Ticket':>9}{'Transport':>11}{'Food':>9}{'Other':>9}{'Total':>10}{'% Budget':>10}  {'Label':<15}")
    print("-----------------------------------------------------------------------------------------------------------------")
    for _row in results:
        _ticket = f"${_row['Ticket']:,.2f}"
        _transport = f"${_row['Transport']:,.2f}"
        _food = f"${_row['Food']:,.2f}"
        _other = f"${_row['Other']:,.2f}"
        _total = f"${_row['Total']:,.2f}"
        _percent = f"{_row['Percent']:.1f}%"
        print(f"{_row['Date']:<12}{_row['Team']:<10}{_row['Opponent']:<16}{_ticket:>9}{_transport:>11}{_food:>9}{_other:>9}{_total:>10}{_percent:>10}  {_row['Label']:<15}")
    return


@app.cell
def _(cheapest_so_far, monthly_budget, transport_mode):
    print(
        f"With a ${monthly_budget:,.2f} monthly budget and {transport_mode} as transportation, "
        f"the best value is the {cheapest_so_far['Team']} vs. {cheapest_so_far['Opponent']} "
        f"on {cheapest_so_far['Date']}: ${cheapest_so_far['Total']:,.2f} in all, "
        f"{cheapest_so_far['Percent']:.1f}% of the budget ({cheapest_so_far['Label']})."
    )
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
    **Check 1: Calculating one manually.** I worked out the Celtics vs. Nets game on Oct 27 without
    the code. The calculation is \$41 ticket + \$6 MBTA + \$20 food + \$5 other = \$72, and \$72 out of a \$150
    budget is 48.0%. The program gives the same: \$72.00 and 48.0%. I have checked again by the code below:
    """)
    return


@app.cell
def _(results):
    hand_total = 72
    hand_percent = 48.0

    # The same game, as the program worked it out in section 4
    for _row in results:
        if _row["Date"] == "2026-10-27":
            program_total = _row["Total"]
            program_percent = _row["Percent"]

    print(f"Total:    by hand ${hand_total:,.2f}   program ${program_total:,.2f}")
    print(f"% Budget: by hand {hand_percent:.1f}%      program {program_percent:.1f}%")
    print(f"Totals match: {hand_total == program_total}")
    print(f"Percents match: {hand_percent == program_percent}")
    return


@app.cell
def _(games, results, transport_costs):
    tickets_so_far = 0
    transport_so_far = 0
    food_so_far = 0
    other_so_far = 0
    for _date, _team, _opponent, _venue, _ticket, _food, _other in games:
        tickets_so_far = tickets_so_far + _ticket
        transport_so_far = transport_so_far + transport_costs[_venue]
        food_so_far = food_so_far + _food
        other_so_far = other_so_far + _other
    parts_sum = tickets_so_far + transport_so_far + food_so_far + other_so_far

    totals_so_far = 0
    for _row in results:
        totals_so_far = totals_so_far + _row["Total"]

    print(f"Tickets ${tickets_so_far:,.2f} + transport ${transport_so_far:,.2f} + food ${food_so_far:,.2f} + other ${other_so_far:,.2f} = ${parts_sum:,.2f}")
    print(f"Sum of the 22 totals = ${totals_so_far:,.2f}")
    print(f"Match: {parts_sum == totals_so_far}")
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
    **What the AI gave me:** In section 4, the agent's first version of the loop chose the
    cheapest game with `if cheapest_so_far is None or _percent < cheapest_so_far["Percent"]:`,
    and in section 6 it compared the two numbers with `and` and printed the result with
    `print("Match:", ...)`. Earlier, its first inputs cell in section 3 also stored the
    transport costs as a dictionary inside a dictionary (`transport_costs["Gillette"]["MBTA"]`).

    **What I changed:** I asked whether we had covered all of this in class, and checked each
    line against my four class notebooks. `or`, `and`, a `print` with a comma, and a dictionary
    inside a dictionary were not in any of them. I had the agent rewrite them using only what
    we covered:
    - the `or` became an `if / elif` (cell 5 in section 4),
    - check 1 now matches the game by its date alone, so it no longer needs `and` (section 6),
    - each comparison is printed with an f-string,
    - the transport costs became three flat dictionaries, one per mode, like `closing_prices`
      in notebook 3 (section 3).

      **How I knew the change was right:** After the rewrite I re-ran every cell. The results
    did not change - the best game is still the Celtics vs. Nets on Oct 27 at \$72.00 (48.0%),
    the parts and the totals in check 2 both add up to \$2,698.00, and every check prints True.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 8. Going Further

    *Take at least one step past the main task, in any direction, and use your agent as much as you like. It does not have to work. State what you tried, what you found, and where it is in this notebook.*
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **What I tried:** I asked whether the best-value game changes with the way the student
    travels. The cell below runs the whole comparison three times, once for each
    transportation method (MBTA, Rideshare, Drive), with a loop inside a loop. The outer
    loop goes through the three methods and the inner loop goes through all 22 games.

    **What I found:** The best game is the same every time, the **Celtics vs. Nets on Oct 27**,
    because its \$41 ticket is the cheapest of all 22 and every TD Garden game has the same
    transport cost. What changes is the price and how many games fit the budget. By MBTA it
    costs \$72 (48%, Good Value) and 17 of 22 games fit in \$150. By rideshare it costs \$94
    (62.7%, Expensive) and only 15 fit. Driving costs \$84 (56%). Taking the MBTA instead of a
    rideshare saves the student \$22 on this game. Here, we assume that the budget remains the same.
    """)
    return


@app.cell
def _(
    drive_costs,
    games,
    mbta_costs,
    monthly_budget,
    rideshare_costs,
    value_label,
):
    all_modes = [
        ("MBTA", mbta_costs),
        ("Rideshare", rideshare_costs),
        ("Drive", drive_costs),
    ]

    print(f"{'Mode':<11}{'Best game':<30}{'Total':>10}{'% Budget':>10}  {'Label':<16}{'Within budget':>13}")
    print("------------------------------------------------------------------------------------------")
    for _mode, _costs in all_modes:
        _best = None
        _within = 0
        for _date, _team, _opponent, _venue, _ticket, _food, _other in games:
            _total = _ticket + _costs[_venue] + _food + _other
            _percent = _total / monthly_budget * 100
            if _percent <= 100:
                _within = _within + 1
            if _best is None:
                _best = (_date, _team, _opponent, _total, _percent)
            elif _percent < _best[4]:
                _best = (_date, _team, _opponent, _total, _percent)
        _game = f"{_best[1]} vs. {_best[2]} ({_best[0]})"
        _total_text = f"${_best[3]:,.2f}"
        _percent_text = f"{_best[4]:.1f}%"
        _within_text = f"{_within} of {len(games)}"
        print(f"{_mode:<11}{_game:<30}{_total_text:>10}{_percent_text:>10}  {value_label(_best[4]):<16}{_within_text:>13}")
    return


if __name__ == "__main__":
    app.run()
