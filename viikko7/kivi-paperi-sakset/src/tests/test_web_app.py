import pytest
from web_app import app, _eka_voittaa


@pytest.fixture
def client():
    """Create a test client for the Flask application"""
    app.config['TESTING'] = True
    app.config['SECRET_KEY'] = 'test_secret_key'
    with app.test_client() as client:
        yield client


@pytest.fixture
def client_with_session(client):
    """Create a test client with an active session"""
    with client.session_transaction() as session:
        session['game_mode'] = 'a'
        session['tuomari_ekan_pisteet'] = 0
        session['tuomari_tokan_pisteet'] = 0
        session['tuomari_tasapelit'] = 0
        session['round'] = 1
    return client


class TestIndexRoute:
    def test_index_page_loads(self, client):
        """Test that the index page loads successfully"""
        response = client.get('/')
        assert response.status_code == 200
        assert b'Kivi-Paperi-Sakset' in response.data

    def test_index_contains_game_modes(self, client):
        """Test that the index page contains all game mode options"""
        response = client.get('/')
        assert 'Pelaaja vs Pelaaja'.encode('utf-8') in response.data
        assert 'Tekoäly'.encode('utf-8') in response.data
        assert 'Parannettu'.encode('utf-8') in response.data


class TestStartGame:
    def test_start_game_mode_a(self, client):
        """Test starting a player vs player game"""
        response = client.post(
            '/start_game', data={'game_mode': 'a'}, follow_redirects=False)
        assert response.status_code == 302
        assert '/game' in response.location

    def test_start_game_mode_b(self, client):
        """Test starting a player vs AI game"""
        response = client.post(
            '/start_game', data={'game_mode': 'b'}, follow_redirects=False)
        assert response.status_code == 302

        with client.session_transaction() as session:
            assert session['game_mode'] == 'b'
            assert session['tekoaly_siirto'] == 0

    def test_start_game_mode_c(self, client):
        """Test starting a player vs improved AI game"""
        response = client.post(
            '/start_game', data={'game_mode': 'c'}, follow_redirects=False)
        assert response.status_code == 302

        with client.session_transaction() as session:
            assert session['game_mode'] == 'c'
            assert session['tekoaly_muisti'] == []
            assert session['tekoaly_muistin_koko'] == 10

    def test_start_game_initializes_scores(self, client):
        """Test that starting a game initializes scores correctly"""
        client.post('/start_game', data={'game_mode': 'a'})

        with client.session_transaction() as session:
            assert session['tuomari_ekan_pisteet'] == 0
            assert session['tuomari_tokan_pisteet'] == 0
            assert session['tuomari_tasapelit'] == 0
            assert session['round'] == 1


class TestPlayGame:
    def test_play_game_displays_correctly(self, client_with_session):
        """Test that the game page displays correctly"""
        response = client_with_session.get('/game')
        assert response.status_code == 200
        assert 'Pelaaja vs Pelaaja'.encode('utf-8') in response.data

    def test_play_game_shows_scores(self, client_with_session):
        """Test that the game page displays current scores"""
        with client_with_session.session_transaction() as session:
            session['tuomari_ekan_pisteet'] = 2
            session['tuomari_tokan_pisteet'] = 1
            session['tuomari_tasapelit'] = 1

        response = client_with_session.get('/game')
        assert b'2' in response.data
        assert b'1' in response.data


class TestMakeMove:
    def test_make_move_player_vs_player_rock_vs_scissors(self, client_with_session):
        """Test player 1 wins with rock vs scissors"""
        response = client_with_session.post('/make_move',
                                            data={'ekan_siirto': 'k',
                                                  'tokan_siirto': 's'},
                                            follow_redirects=False)
        assert response.status_code == 302

        with client_with_session.session_transaction() as session:
            assert session['tuomari_ekan_pisteet'] == 1
            assert session['tuomari_tokan_pisteet'] == 0
            assert session['round'] == 2

    def test_make_move_player_vs_player_tie(self, client_with_session):
        """Test tie game"""
        response = client_with_session.post('/make_move',
                                            data={'ekan_siirto': 'k',
                                                  'tokan_siirto': 'k'},
                                            follow_redirects=False)
        assert response.status_code == 302

        with client_with_session.session_transaction() as session:
            assert session['tuomari_ekan_pisteet'] == 0
            assert session['tuomari_tokan_pisteet'] == 0
            assert session['tuomari_tasapelit'] == 1

    def test_make_move_player_vs_player_paper_vs_rock(self, client_with_session):
        """Test player 1 wins with paper vs rock"""
        response = client_with_session.post('/make_move',
                                            data={'ekan_siirto': 'p',
                                                  'tokan_siirto': 'k'},
                                            follow_redirects=False)

        with client_with_session.session_transaction() as session:
            assert session['tuomari_ekan_pisteet'] == 1

    def test_make_move_player_vs_player_scissors_vs_paper(self, client_with_session):
        """Test player 1 wins with scissors vs paper"""
        response = client_with_session.post('/make_move',
                                            data={'ekan_siirto': 's',
                                                  'tokan_siirto': 'p'},
                                            follow_redirects=False)

        with client_with_session.session_transaction() as session:
            assert session['tuomari_ekan_pisteet'] == 1

    def test_make_move_player_loses(self, client_with_session):
        """Test player 2 wins"""
        response = client_with_session.post('/make_move',
                                            data={'ekan_siirto': 'k',
                                                  'tokan_siirto': 'p'},
                                            follow_redirects=False)

        with client_with_session.session_transaction() as session:
            assert session['tuomari_ekan_pisteet'] == 0
            assert session['tuomari_tokan_pisteet'] == 1

    def test_make_move_invalid_first_player_move(self, client_with_session):
        """Test invalid move from first player redirects to game over"""
        response = client_with_session.post('/make_move',
                                            data={'ekan_siirto': 'x',
                                                  'tokan_siirto': 'k'},
                                            follow_redirects=False)
        assert response.status_code == 302
        assert '/game_over' in response.location

    def test_make_move_invalid_second_player_move(self, client_with_session):
        """Test invalid move from second player redirects to game over"""
        response = client_with_session.post('/make_move',
                                            data={'ekan_siirto': 'k',
                                                  'tokan_siirto': 'invalid'},
                                            follow_redirects=False)
        assert response.status_code == 302
        assert '/game_over' in response.location

    def test_make_move_vs_simple_ai(self, client):
        """Test playing against simple AI"""
        with client.session_transaction() as session:
            session['game_mode'] = 'b'
            session['tuomari_ekan_pisteet'] = 0
            session['tuomari_tokan_pisteet'] = 0
            session['tuomari_tasapelit'] = 0
            session['round'] = 1
            session['tekoaly_siirto'] = 0

        response = client.post('/make_move',
                               data={'ekan_siirto': 'k'},
                               follow_redirects=False)

        assert response.status_code == 302
        with client.session_transaction() as session:
            # AI should have made a move
            assert session['tekoaly_siirto'] == 1
            assert session['last_tokan_siirto'] in ['k', 'p', 's']

    def test_make_move_vs_improved_ai_first_move(self, client):
        """Test playing against improved AI on first move"""
        with client.session_transaction() as session:
            session['game_mode'] = 'c'
            session['tuomari_ekan_pisteet'] = 0
            session['tuomari_tokan_pisteet'] = 0
            session['tuomari_tasapelit'] = 0
            session['round'] = 1
            session['tekoaly_muisti'] = []
            session['tekoaly_muistin_koko'] = 10

        response = client.post('/make_move',
                               data={'ekan_siirto': 'p'},
                               follow_redirects=False)

        assert response.status_code == 302
        with client.session_transaction() as session:
            # AI should default to rock on first move
            assert session['last_tokan_siirto'] == 'k'
            assert 'p' in session['tekoaly_muisti']

    def test_make_move_vs_improved_ai_with_memory(self, client):
        """Test improved AI uses memory"""
        with client.session_transaction() as session:
            session['game_mode'] = 'c'
            session['tuomari_ekan_pisteet'] = 0
            session['tuomari_tokan_pisteet'] = 0
            session['tuomari_tasapelit'] = 0
            session['round'] = 3
            session['tekoaly_muisti'] = ['k', 'p']
            session['tekoaly_muistin_koko'] = 10

        response = client.post('/make_move',
                               data={'ekan_siirto': 's'},
                               follow_redirects=False)

        assert response.status_code == 302
        with client.session_transaction() as session:
            # Memory should be updated
            assert 's' in session['tekoaly_muisti']
            assert len(session['tekoaly_muisti']) == 3

    def test_stores_last_moves(self, client_with_session):
        """Test that last moves are stored in session"""
        client_with_session.post('/make_move',
                                 data={'ekan_siirto': 'k', 'tokan_siirto': 'p'})

        with client_with_session.session_transaction() as session:
            assert session['last_ekan_siirto'] == 'k'
            assert session['last_tokan_siirto'] == 'p'


class TestRoundResult:
    def test_round_result_displays_moves(self, client):
        """Test that round result page displays moves correctly"""
        with client.session_transaction() as session:
            session['last_ekan_siirto'] = 'k'
            session['last_tokan_siirto'] = 's'
            session['game_mode'] = 'a'
            session['tuomari_ekan_pisteet'] = 1
            session['tuomari_tokan_pisteet'] = 0
            session['tuomari_tasapelit'] = 0

        response = client.get('/round_result')
        assert response.status_code == 200
        assert b'Kivi' in response.data
        assert b'Sakset' in response.data

    def test_round_result_shows_winner(self, client):
        """Test that round result shows the correct winner"""
        with client.session_transaction() as session:
            session['last_ekan_siirto'] = 'k'
            session['last_tokan_siirto'] = 's'
            session['game_mode'] = 'a'
            session['tuomari_ekan_pisteet'] = 1
            session['tuomari_tokan_pisteet'] = 0
            session['tuomari_tasapelit'] = 0

        response = client.get('/round_result')
        assert 'Pelaaja 1 voitti kierroksen!'.encode('utf-8') in response.data

    def test_round_result_shows_tie(self, client):
        """Test that round result shows tie correctly"""
        with client.session_transaction() as session:
            session['last_ekan_siirto'] = 'k'
            session['last_tokan_siirto'] = 'k'
            session['game_mode'] = 'a'
            session['tuomari_ekan_pisteet'] = 0
            session['tuomari_tokan_pisteet'] = 0
            session['tuomari_tasapelit'] = 1

        response = client.get('/round_result')
        assert b'Tasapeli!' in response.data


class TestGameOver:
    def test_game_over_displays_scores(self, client):
        """Test that game over page displays final scores"""
        with client.session_transaction() as session:
            session['tuomari_ekan_pisteet'] = 3
            session['tuomari_tokan_pisteet'] = 2
            session['tuomari_tasapelit'] = 1
            session['game_mode'] = 'a'

        response = client.get('/game_over')
        assert response.status_code == 200
        assert b'3' in response.data
        assert b'2' in response.data
        assert b'1' in response.data

    def test_game_over_clears_session(self, client):
        """Test that game over clears the session"""
        with client.session_transaction() as session:
            session['tuomari_ekan_pisteet'] = 3
            session['tuomari_tokan_pisteet'] = 2
            session['game_mode'] = 'a'

        client.get('/game_over')

        with client.session_transaction() as session:
            assert 'tuomari_ekan_pisteet' not in session
            assert 'game_mode' not in session


class TestWinLogic:
    def test_rock_beats_scissors(self):
        """Test that rock beats scissors"""
        assert _eka_voittaa('k', 's') == True

    def test_scissors_beats_paper(self):
        """Test that scissors beats paper"""
        assert _eka_voittaa('s', 'p') == True

    def test_paper_beats_rock(self):
        """Test that paper beats rock"""
        assert _eka_voittaa('p', 'k') == True

    def test_rock_loses_to_paper(self):
        """Test that rock loses to paper"""
        assert _eka_voittaa('k', 'p') == False

    def test_scissors_loses_to_rock(self):
        """Test that scissors loses to rock"""
        assert _eka_voittaa('s', 'k') == False

    def test_paper_loses_to_scissors(self):
        """Test that paper loses to scissors"""
        assert _eka_voittaa('p', 's') == False

    def test_tie_returns_false(self):
        """Test that ties return False"""
        assert _eka_voittaa('k', 'k') == False
        assert _eka_voittaa('p', 'p') == False
        assert _eka_voittaa('s', 's') == False


class TestGameFlow:
    def test_complete_game_flow(self, client):
        """Test a complete game flow from start to finish"""
        # Start game
        response = client.post(
            '/start_game', data={'game_mode': 'a'}, follow_redirects=True)
        assert response.status_code == 200

        # Play first round - player 1 wins
        response = client.post('/make_move',
                               data={'ekan_siirto': 'k', 'tokan_siirto': 's'},
                               follow_redirects=True)
        assert response.status_code == 200

        # Check session
        with client.session_transaction() as session:
            assert session['tuomari_ekan_pisteet'] == 1
            assert session['round'] == 2

        # Play second round - tie
        response = client.post('/make_move',
                               data={'ekan_siirto': 'p', 'tokan_siirto': 'p'},
                               follow_redirects=True)

        with client.session_transaction() as session:
            assert session['tuomari_tasapelit'] == 1
            assert session['round'] == 3

        # End game
        response = client.get('/game_over', follow_redirects=True)
        assert response.status_code == 200

    def test_multiple_rounds_score_tracking(self, client_with_session):
        """Test that scores are tracked correctly across multiple rounds"""
        # Round 1: Player 1 wins
        client_with_session.post('/make_move',
                                 data={'ekan_siirto': 'k', 'tokan_siirto': 's'})

        # Round 2: Player 2 wins
        client_with_session.post('/make_move',
                                 data={'ekan_siirto': 's', 'tokan_siirto': 'k'})

        # Round 3: Tie
        client_with_session.post('/make_move',
                                 data={'ekan_siirto': 'p', 'tokan_siirto': 'p'})

        with client_with_session.session_transaction() as session:
            assert session['tuomari_ekan_pisteet'] == 1
            assert session['tuomari_tokan_pisteet'] == 1
            assert session['tuomari_tasapelit'] == 1
            assert session['round'] == 4
