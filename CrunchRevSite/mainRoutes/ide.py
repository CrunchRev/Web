"""
2024, Written by the CrunchRev Authors

Route module description: controls everything under /ide/
"""

@app.route("/ide/welcome", methods=["GET"])
def welcomeide():
    return render_template("welcomeide.html")