import os
import sqlite3
from flask import Flask, request, redirect, render_template, render_template_string, g
from markupsafe import escape


app = Flask(__name__)
DATABASE = os.path.join(os.path.dirname(__file__), 'shared', 'database.db')


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = escape(request.form['username'])
        tg_username = escape(request.form['tg_username'])

        db = get_db()
        db.execute(
            "INSERT INTO users (username, tg_username, manifest) VALUES (?, ?, '')",
            (username, tg_username)
        )
        db.commit()

        return redirect('/login')

    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        tg_username = request.form.get('tg_username')
        db = get_db()
        user = db.execute("SELECT id FROM users WHERE tg_username = ?", (tg_username,)).fetchone()
        if user:
            user_id = user[0]
            return f'''
                <script>
                    localStorage.setItem("authorized", "{user_id}");
                    window.location.href = "/profile/{user_id}";
                </script>
            '''
        else:
            return "Пользователь не найден 😢", 404

    return render_template('login.html')


@app.route('/profile/<int:user_id>', methods=['GET', 'POST'])
def profile(user_id):
    db = get_db()

    if user_id == 1135:
        username = "mirror_berry"
        manifest = "он пытался предупредить других..."
        rendered = "<p>Привет, это mirror_berry. Я бросил работу над проектом StrawberryBest и ушёл из их сообщества.</p>" \
        "<p>Всё, что они делают - часами смотрят евровидение разных годов и выращивают клубнику. Возможно, в жертву были принесены несколько несогласных. К счастью, когда моё несогласие раскроют, я буду уже в другой стране.</p>" \
        "<p>В любом случае, я бы не стал доверять людям, у которых некто А.М.Бабанов в списке 'сАмЫх ярКиХ кЛубНиЧеК', что за треш, я так и знал, что он какой-то сектант.</p>"\
        "<p>Если ты можешь, расскажи правду. Но только тем, кому можешь доверять.</p>"\
        "<p>Держи - AB3QAYQAGMAHEADSAB4QAXYAMMAHKABRAB2AA7I=. Это тебе понадобится. И удачи.</p>"

        return render_template(
            'profile.html',
            username=username,
            user_id=user_id,
            original_manifest=manifest,
            rendered_manifest=rendered
        )

    if request.method == 'POST':
        new_manifest = request.form.get("manifest", "")
        db.execute("UPDATE users SET manifest = ? WHERE id = ?", (new_manifest, user_id))
        db.commit()

    user = db.execute("SELECT username, manifest FROM users WHERE id = ?", (user_id,)).fetchone()

    if user:
        username, manifest = user
        rendered = escape(manifest)

        return render_template(
            'profile.html',
            username=username,
            user_id=user_id,
            original_manifest=manifest,
            rendered_manifest=rendered
        )
    else:
        return "Профиль не найден", 404


@app.route('/hall_of_fame')
def hall_of_fame():
    db = get_db()
    users = db.execute("SELECT username, manifest FROM users").fetchall()
    return render_template('hall_of_fame.html', users=users)


@app.route('/diary')
def diary():
    return "<p>Иногда зеркало показывает больше, чем нужно... 🍓</p>"


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
