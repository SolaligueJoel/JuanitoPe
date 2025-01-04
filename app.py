from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Lista de canciones disponibles
SONGS = [
    "Bohemian Rhapsody - Queen",
    "Imagine - John Lennon",
    "Wonderwall - Oasis",
    "Someone Like You - Adele",
    "Blinding Lights - The Weeknd",
    "Shape of You - Ed Sheeran"
]

# Lista de canciones seleccionadas
selected_songs = []

@app.route("/")
def index():
    return render_template("index.html", songs=SONGS)

@app.route("/select", methods=["POST"])
def select_song():
    song = request.form.get("song")
    if song and song not in selected_songs:
        selected_songs.append(song)
    return redirect(url_for("index"))

@app.route("/singer")
def singer_view():
    return render_template("singer.html", selected_songs=selected_songs)

if __name__ == "__main__":
    app.run(debug=True)
