# Vibe koodausta GitHub Copilotilla Issueiden avulla

## Päätyikö Copilot toimivaan ja hyvään ratkaisuun

Copilot pääsi ensimmäisellä iteraatiolla jo toimivaan ratkaisuun, ja mielestäni ihan hyvään sellaiseen. Ei koskenut Varasto classin toteutusta vaan osasi nätisti ottaa sen käyttöön. En keksinyt mitään parannettavaa Copilotin tekemässä koodissa, niin lisäyksenä pyysin hänen tekemään dark ja light teeman vaihtamisen.

## Oliko koodi selkeää

Koodi oli selkeäää ja hyvin jaoteltu seuraaviin routeihin:
- `/`: etusivu
- `/create`: luo uusi varasto
- `/update/:name`: päivittää varaston tiedot
- `/delete/:name`: poistaa varaston

ja käytettään yhtä samaa HTML templateä kaikissa näkymissä.

## Opitko jotain uutta Copilotin tekemää koodia lukiessasi

Flaskin käyttö oli minulle jo entuudestaan tuttua, joten en oppinut siitä mitään uutta. Copilotin tekemä koodi oli kuitenkin hyvin jäsenneltyä ja selkeää, mikä auttoi minua ymmärtämään, miten Flask-sovellus voidaan rakentaa tehokkaasti.
