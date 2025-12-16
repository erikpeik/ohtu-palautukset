from flask import Flask, render_template, request, session, redirect, url_for
import secrets
from luo_peli import luo_peli
from tuomari import Tuomari
from tekoaly import Tekoaly
from tekoaly_parannettu import TekoalyParannettu

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)


@app.route('/')
def index():
    """Main page for selecting game mode"""
    return render_template('index.html')


@app.route('/start_game', methods=['POST'])
def start_game():
    """Initialize a new game with the selected mode"""
    game_mode = request.form.get('game_mode')

    # Initialize game session
    session['game_mode'] = game_mode
    session['tuomari_ekan_pisteet'] = 0
    session['tuomari_tokan_pisteet'] = 0
    session['tuomari_tasapelit'] = 0
    session['round'] = 1

    # Initialize move statistics
    session['ekan_moves'] = {'k': 0, 'p': 0, 's': 0}
    session['tokan_moves'] = {'k': 0, 'p': 0, 's': 0}

    # Initialize AI if needed
    if game_mode == 'b':
        session['tekoaly_siirto'] = 0
    elif game_mode == 'c':
        session['tekoaly_muisti'] = []
        session['tekoaly_muistin_koko'] = 10

    return redirect(url_for('play_game'))


@app.route('/game')
def play_game():
    """Display the game interface"""
    game_mode = session.get('game_mode')
    round_num = session.get('round', 1)

    tuomari_ekan_pisteet = session.get('tuomari_ekan_pisteet', 0)
    tuomari_tokan_pisteet = session.get('tuomari_tokan_pisteet', 0)
    tuomari_tasapelit = session.get('tuomari_tasapelit', 0)

    game_mode_names = {
        'a': 'Pelaaja vs Pelaaja',
        'b': 'Pelaaja vs Tekoäly',
        'c': 'Pelaaja vs Parannettu Tekoäly'
    }

    return render_template('game.html',
                           game_mode=game_mode,
                           game_mode_name=game_mode_names.get(
                               game_mode, 'Tuntematon'),
                           round=round_num,
                           ekan_pisteet=tuomari_ekan_pisteet,
                           tokan_pisteet=tuomari_tokan_pisteet,
                           tasapelit=tuomari_tasapelit)


@app.route('/make_move', methods=['POST'])
def make_move():
    """Process a move and calculate the result"""
    ekan_siirto = request.form.get('ekan_siirto')
    tokan_siirto = request.form.get('tokan_siirto', '')
    game_mode = session.get('game_mode')

    # Validate first player's move
    if ekan_siirto not in ['k', 'p', 's']:
        return redirect(url_for('game_over'))

    # Determine second player's move based on game mode
    if game_mode == 'a':
        # Player vs Player
        if tokan_siirto not in ['k', 'p', 's']:
            return redirect(url_for('game_over'))
    elif game_mode == 'b':
        # Player vs AI (simple)
        tekoaly_siirto = session.get('tekoaly_siirto', 0)
        tekoaly_siirto = (tekoaly_siirto + 1) % 3
        session['tekoaly_siirto'] = tekoaly_siirto

        if tekoaly_siirto == 0:
            tokan_siirto = "k"
        elif tekoaly_siirto == 1:
            tokan_siirto = "p"
        else:
            tokan_siirto = "s"
    elif game_mode == 'c':
        # Player vs Improved AI
        muisti = session.get('tekoaly_muisti', [])
        muistin_koko = session.get('tekoaly_muistin_koko', 10)

        # Calculate AI move
        if len(muisti) == 0 or len(muisti) == 1:
            tokan_siirto = "k"
        else:
            viimeisin_siirto = muisti[-1]
            k = 0
            p = 0
            s = 0

            for i in range(len(muisti) - 1):
                if viimeisin_siirto == muisti[i]:
                    seuraava = muisti[i + 1]
                    if seuraava == "k":
                        k += 1
                    elif seuraava == "p":
                        p += 1
                    else:
                        s += 1

            if k > p or k > s:
                tokan_siirto = "p"
            elif p > k or p > s:
                tokan_siirto = "s"
            else:
                tokan_siirto = "k"

        # Update memory
        if len(muisti) >= muistin_koko:
            muisti.pop(0)
        muisti.append(ekan_siirto)
        session['tekoaly_muisti'] = muisti

    # Update score using Tuomari logic
    ekan_pisteet = session.get('tuomari_ekan_pisteet', 0)
    tokan_pisteet = session.get('tuomari_tokan_pisteet', 0)
    tasapelit = session.get('tuomari_tasapelit', 0)

    if ekan_siirto == tokan_siirto:
        tasapelit += 1
    elif _eka_voittaa(ekan_siirto, tokan_siirto):
        ekan_pisteet += 1
    else:
        tokan_pisteet += 1

    session['tuomari_ekan_pisteet'] = ekan_pisteet
    session['tuomari_tokan_pisteet'] = tokan_pisteet
    session['tuomari_tasapelit'] = tasapelit
    session['round'] = session.get('round', 1) + 1

    # Store last moves for display
    session['last_ekan_siirto'] = ekan_siirto
    session['last_tokan_siirto'] = tokan_siirto

    # Track move statistics
    ekan_moves = session.get('ekan_moves', {'k': 0, 'p': 0, 's': 0})
    tokan_moves = session.get('tokan_moves', {'k': 0, 'p': 0, 's': 0})
    ekan_moves[ekan_siirto] = ekan_moves.get(ekan_siirto, 0) + 1
    tokan_moves[tokan_siirto] = tokan_moves.get(tokan_siirto, 0) + 1
    session['ekan_moves'] = ekan_moves
    session['tokan_moves'] = tokan_moves

    # Check if either player has reached 5 wins
    if ekan_pisteet >= 5 or tokan_pisteet >= 5:
        session['game_finished'] = True

    return redirect(url_for('round_result'))


@app.route('/round_result')
def round_result():
    """Display the result of the last round"""
    ekan_siirto = session.get('last_ekan_siirto')
    tokan_siirto = session.get('last_tokan_siirto')
    game_mode = session.get('game_mode')
    game_finished = session.get('game_finished', False)

    siirto_names = {'k': 'Kivi', 'p': 'Paperi', 's': 'Sakset'}

    # Determine round winner
    if ekan_siirto == tokan_siirto:
        result = "Tasapeli!"
    elif _eka_voittaa(ekan_siirto, tokan_siirto):
        result = "Pelaaja 1 voitti kierroksen!"
    else:
        if game_mode == 'a':
            result = "Pelaaja 2 voitti kierroksen!"
        else:
            result = "Tietokone voitti kierroksen!"

    return render_template('round_result.html',
                           ekan_siirto=siirto_names.get(ekan_siirto, ''),
                           tokan_siirto=siirto_names.get(tokan_siirto, ''),
                           result=result,
                           ekan_pisteet=session.get('tuomari_ekan_pisteet', 0),
                           tokan_pisteet=session.get(
                               'tuomari_tokan_pisteet', 0),
                           tasapelit=session.get('tuomari_tasapelit', 0),
                           game_finished=game_finished)


@app.route('/game_over')
def game_over():
    """Display final game results"""
    ekan_pisteet = session.get('tuomari_ekan_pisteet', 0)
    tokan_pisteet = session.get('tuomari_tokan_pisteet', 0)
    tasapelit = session.get('tuomari_tasapelit', 0)
    game_mode = session.get('game_mode')

    # Get move statistics
    ekan_moves = session.get('ekan_moves', {'k': 0, 'p': 0, 's': 0})
    tokan_moves = session.get('tokan_moves', {'k': 0, 'p': 0, 's': 0})

    # Clear session
    session.clear()

    return render_template('game_over.html',
                           ekan_pisteet=ekan_pisteet,
                           tokan_pisteet=tokan_pisteet,
                           tasapelit=tasapelit,
                           game_mode=game_mode,
                           ekan_moves=ekan_moves,
                           tokan_moves=tokan_moves)


def _eka_voittaa(eka, toka):
    """Check if first player wins - reuses Tuomari logic"""
    if eka == "k" and toka == "s":
        return True
    elif eka == "s" and toka == "p":
        return True
    elif eka == "p" and toka == "k":
        return True
    return False


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
