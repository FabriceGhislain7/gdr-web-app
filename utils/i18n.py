from flask import session


SUPPORTED_LANGUAGES = ("it", "en")
DEFAULT_LANGUAGE = "en"


TRANSLATIONS = {
    "it": {
        "nav.home": "Home",
        "nav.about": "Chi Siamo",
        "nav.guide": "Guida",
        "nav.main_menu": "Menu Principale",
        "nav.classification": "Classifica",
        "nav.data_analyst": "Data Analyst",
        "nav.game_guide": "Guida di Gioco",
        "nav.login": "Login",
        "nav.signup": "Sign up",
        "nav.edit_profile": "Modifica Profilo",
        "nav.refill_credits": "Ricarica Crediti",
        "nav.logout": "Logout",
        "nav.language": "Lingua",
        "nav.italian": "Italiano",
        "nav.english": "Inglese",
        "header.credits": "crediti",
        "footer.quick_links": "Link Rapidi",
        "footer.all_rights": "Tutti i diritti riservati.",
        "footer.privacy": "Privacy Policy",
        "footer.terms": "Termini di Servizio",
        "footer.version": "Versione",
        "footer.developed_by": "Sviluppato da",
        "footer.developer": "Sviluppatore",
        "footer.phone": "Telefono",
        "footer.portal_desc": "Il tuo portale per avventure fantasy epiche online.",
        "layout.meta_description": "GDR Web App - Gioco di ruolo fantasy online",
        "layout.meta_keywords": "GDR, gioco di ruolo, fantasy, online, web app",
        "menu.profile_management": "Gestione Profilo",
        "menu.profile_desc": "Modifica i tuoi dati personali e gestisci i crediti del tuo account",
        "menu.credits": "Crediti",
        "menu.characters": "Personaggi",
        "menu.edit_profile": "Modifica Profilo",
        "menu.refill_credits": "Ricarica Crediti",
        "menu.your_heroes": "I Tuoi Eroi",
        "menu.heroes_desc": "Crea nuovi personaggi e gestisci il tuo party di avventurieri",
        "menu.warriors": "Guerrieri",
        "menu.mages": "Maghi",
        "menu.rogues": "Ladri",
        "menu.combat": "Combattimento",
        "menu.close": "Chiudi",
        "menu.about_us": "Chi Siamo",
    },
    "en": {
        "nav.home": "Home",
        "nav.about": "About",
        "nav.guide": "Guide",
        "nav.main_menu": "Main Menu",
        "nav.classification": "Leaderboard",
        "nav.data_analyst": "Data Analyst",
        "nav.game_guide": "Game Guide",
        "nav.login": "Login",
        "nav.signup": "Sign up",
        "nav.edit_profile": "Edit Profile",
        "nav.refill_credits": "Refill Credits",
        "nav.logout": "Logout",
        "nav.language": "Language",
        "nav.italian": "Italian",
        "nav.english": "English",
        "header.credits": "credits",
        "footer.quick_links": "Quick Links",
        "footer.all_rights": "All rights reserved.",
        "footer.privacy": "Privacy Policy",
        "footer.terms": "Terms of Service",
        "footer.version": "Version",
        "footer.developed_by": "Developed by",
        "footer.developer": "Developer",
        "footer.phone": "Phone",
        "footer.portal_desc": "Your portal for epic fantasy adventures online.",
        "layout.meta_description": "GDR Web App - Online fantasy role-playing game",
        "layout.meta_keywords": "RPG, role-playing game, fantasy, online, web app",
        "menu.profile_management": "Profile Management",
        "menu.profile_desc": "Edit your personal data and manage your account credits",
        "menu.credits": "Credits",
        "menu.characters": "Characters",
        "menu.edit_profile": "Edit Profile",
        "menu.refill_credits": "Refill Credits",
        "menu.your_heroes": "Your Heroes",
        "menu.heroes_desc": "Create new characters and manage your party of adventurers",
        "menu.warriors": "Warriors",
        "menu.mages": "Mages",
        "menu.rogues": "Rogues",
        "menu.combat": "Combat",
        "menu.close": "Close",
        "menu.about_us": "About Us",
    },
}


def get_current_language() -> str:
    lang = session.get("lang", DEFAULT_LANGUAGE)
    if lang not in SUPPORTED_LANGUAGES:
        return DEFAULT_LANGUAGE
    return lang


def set_current_language(lang: str) -> str:
    selected = (lang or DEFAULT_LANGUAGE).lower().strip()
    if selected not in SUPPORTED_LANGUAGES:
        selected = DEFAULT_LANGUAGE
    session["lang"] = selected
    return selected


def translate(key: str, **kwargs) -> str:
    lang = get_current_language()
    value = TRANSLATIONS.get(lang, {}).get(key, key)
    if kwargs:
        try:
            return value.format(**kwargs)
        except Exception:
            return value
    return value
