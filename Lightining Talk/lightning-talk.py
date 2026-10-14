# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "marimo",
# ]
# ///
"""Lightning Talk: The change in Robotics through AI.

Marimo version of the slides in `Lightning Talk_Khadeja Anwar.pptx`, one cell per slide.
"""

import marimo

__generated_with = "0.25.1"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo

    return (mo,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # LIGHTNING TALK

    ### The change in Robotics through AI

    Khadeja Anwar
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Programming and Training

    **Before**

    Engineers coded every movement. Great at one repetitive job, lost in anything messy or new.

    **Now**

    AI models learn from recorded demonstrations, the way chatbots learn from text and adapt to new objects.

    AI has transformed robots from machines that follow fixed instructions into machines that learn from examples.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Where does the data come from?

    Chatbots learned from the whole internet. There's no internet of robot movements, so companies are building one.

    **Training facilities**

    Apptronik opened a dedicated data-collection and training center in Austin.

    **Data marketplaces**

    Kinectic Block sells first-person video and teleoperation recordings.

    **AI Models**

    The AI model used to teach robots is vision language action (VLA) models. Pi0, from Physical Intelligence, GR00T, from NVIDIA and RT-2, from Google DeepMind.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Boston Dynamics Atlas Robots (60 seconds)

    _This slide holds an embedded video in the original PowerPoint; it isn't reproduced here. See the slide in `Lightning Talk_Khadeja Anwar.pptx` for the clip._
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Discussion

    Should countries compete to build the most advanced robots, or should they set global limits on what robots can do?
    """)
    return


if __name__ == "__main__":
    app.run()
