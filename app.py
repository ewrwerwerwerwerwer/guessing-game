
import random
from flask import Flask, render_template, request, session, redirect, url_for

app = Flask(__name__)
app.secret_key = "change-this-to-a-random-secret-key"


@app.route("/", methods=["GET", "POST"])
def home():
    message = ""
    message_type = "info"

    if request.method == "POST":
        action = request.form.get("action")

        # Start a new game
        if action == "start" or action == "restart":
            difficulty = request.form.get("difficulty", "easy").lower()

            difficulties = {
                "easy": 20,
                "medium": 50,
                "hard": 100
            }

            if difficulty not in difficulties:
                message = "Invalid difficulty. Please choose again."
                return render_template(
                    "index.html",
                    message=message,
                    message_type="error"
                )

            session["max_number"] = difficulties[difficulty]
            session["correct_number"] = random.randint(
                1, difficulties[difficulty]
            )
            session["attempts"] = 0
            session["max_attempts"] = 10
            session["difficulty"] = difficulty
            session["playing"] = True
            session["won"] = False

            return redirect(url_for("home"))

        # Process a guess
        elif action == "guess" and session.get("playing"):
            guess_text = request.form.get("guess", "").strip()

            try:
                guess = int(guess_text)
            except ValueError:
                message = "Enter a valid whole number!"
                message_type = "error"
                return render_template(
                    "index.html",
                    message=message,
                    message_type=message_type
                )

            max_number = session["max_number"]

            if guess < 1 or guess > max_number:
                message = f"Enter a number from 1 to {max_number}!"
                message_type = "error"
            else:
                session["attempts"] += 1
                attempts = session["attempts"]
                correct_number = session["correct_number"]

                if guess == correct_number:
                    session["playing"] = False
                    session["won"] = True
                    message = (
                        f"You guessed it in {attempts} "
                        f"attempt(s)! 🎉"
                    )
                    message_type = "success"

                elif attempts >= session["max_attempts"]:
                    session["playing"] = False
                    session["won"] = False
                    message = (
                        f"Game over! The number was "
                        f"{correct_number}."
                    )
                    message_type = "error"

                elif guess > correct_number:
                    message = "Too high! Try a lower number."
                    message_type = "info"

                else:
                    message = "Too low! Try a higher number."
                    message_type = "info"

    return render_template(
        "index.html",
        message=message,
        message_type=message_type,
        playing=session.get("playing", False),
        won=session.get("won", False),
        attempts=session.get("attempts", 0),
        max_attempts=session.get("max_attempts", 10),
        max_number=session.get("max_number", 100),
        difficulty=session.get("difficulty", "easy")
    )


if __name__ == "__main__":
    app.run(debug=True)
