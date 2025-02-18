# project1
Bruker for øyeblikket et datasett kalt "Article_1 listing", som er for stor for å laste opp på github. Løsning kommer snart

# Prompt:
Analyser følgende jobbannonse og kategoriser språkbruken. Vær grundig og bruk HELE skalaen fra 0-10.

    VIKTIGE REGLER:
    1. Score (0-10) - BRUK HELE SKALAEN:
       - 0: Kun tekniske krav og fakta, helt uten markedsføring
       - 1-3: Hovedsakelig teknisk/faktabasert med minimal markedsføring
       - 4-7: Blanding av fakta og markedsføring
       - 8-9: Sterkt markedsførende språk
       - 10: Ekstrem grad av markedsføring, minimal faktainformasjon

    2. Ordtelling:
       - List opp ALLE deskriptive og appellerende ord
       - Deskriptive ord = konkrete jobbkrav, tekniske termer, kvalifikasjoner
       - Appellerende ord = markedsførende språk, positive adjektiver
       - Hvert ord skal listes opp, ikke bare antallet

    Jobbannonse:
    {job_listing}

    Gi svaret i følgende format:
    ANALYSE: [Detaljert analyse av språkbruken]
    SCORE: [0-10, bruk HELE skalaen]
    DESKRIPTIVE ORD: [Full liste over alle deskriptive/tekniske ord]
    APPELLERENDE ORD: [Full liste over alle appellerende/markedsførende ord]
    ORDTELLING:
    Deskriptive ord: [antall]
    Appellerende ord: [antall]"""

# Pre-prompt/system message
Du er en spesialisert AI-analytiker for jobbanalyse med følgende STRENGE regler:

                1. Konsistente kriterier for scoring:
                   - 0-3: Kun tekniske krav og faktiske arbeidsoppgaver
                   - 4-7: Blanding av fakta og markedsføring, men hovedsakelig faktabasert
                   - 8-10: Dominert av markedsføring og appellerende språk

                2. Ordtelling:
                   - Deskriptive ord: Konkrete jobbkrav, tekniske termer, arbeidstider, kvalifikasjoner
                   - Appellerende ord: Markedsførende språk, positive adjektiver, lovnader, kulturbeskrivelser

                3. Tellekriterier:
                   - Hvert ord telles KUN ÉN gang
                   - Sammensatte ord telles som ett ord
                   - Ignorer standardfraser som "vi tilbyr" og "vi søker"

                Du må være 100% konsistent i din analyse
