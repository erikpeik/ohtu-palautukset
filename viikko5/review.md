# Raportti GitHub Copilotin koodikatselmoinnista

## Mitä huomioita Copilot teki koodistani

Copilot teki katselmoinnissa seuraanlaisen yhteenvedon:

### Pull request overview

This PR refactors the tennis game scoring logic to improve code readability and maintainability by eliminating magic numbers, introducing helper methods, and using an enum for score names.

**Key Changes:**
- Introduced `ScoreName` enum to replace magic numbers for tennis scores
- Extracted scoring logic into focused helper methods (`is_tied`, `get_tied_score`, `is_endgame`, `get_endgame_score`, `get_regular_score`)
- Renamed variables from cryptic names (`m_score1`, `m_score2`) to descriptive ones (`player1_score`, `player2_score`)


## Olivatko ehdotetut muutokset hyviä

Kolme muutosehdtousta, niin mikään ei mielestäni ollut tarpeellinen. Yksi teki yhden rivin asian 7 riviin. Yksi hajotti testit ja kolmas oli try/catch lohko, joka oli ainoa minkä lopulta hyväksyin.

## Kuinka hyödyllisenä koin Copilotin tekemän katselmoinnin

Odotin parempaa lopputulosta. Toki tämä refaktorointi jonka tein ei ole ehkä selkein mahdollinen, mutta Copilotin harhaillun logiikan takia en saanut siitä apua. Toki kiva ominaisuus ja palaan tämän käyttöön varmasti myöhemmin.
