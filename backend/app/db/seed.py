from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.security import get_password_hash
from app.models import Badge, Challenge, Course, Discussion, Exercise, Lesson, Module, Project, Quiz, QuizQuestion, ResourceItem, User
from app.services.text import slugify


def lesson_markdown(topic: str, module_title: str, level: str) -> str:
    return f"""
# {topic}

## 1. Objectif de la lecon
Comprendre {topic.lower()} et savoir l'utiliser dans un vrai programme Python.

## 2. Explication simple
Une notion Python doit toujours etre reliee a un usage concret. Ici, tu vas apprendre progressivement le concept, puis le manipuler dans un exemple court.

## 3. Exemple concret
Imagine un petit outil qui doit traiter une information: un nom, un score, une liste de fichiers ou une reponse API. La notion **{topic}** permet de structurer ce traitement.

## 4. Exemple de code
```python
message = "Python est clair"
print(message)
```

## 5. Analyse ligne par ligne
- La premiere ligne cree une information nommee.
- La deuxieme ligne affiche cette information.
- Le programme reste lisible car les noms sont explicites.

## 6. Erreurs frequentes
- Aller trop vite sans tester.
- Oublier une parenthese, un deux-points ou une indentation.
- Utiliser un nom trop vague comme `x` ou `data` sans contexte.

## 7. Mini-exercice
Ecris un programme de trois lignes qui utilise {topic.lower()} dans un cas concret.

## 8. Correction
```python
nom = "Ada"
score = 10
print(f"{{nom}} a {{score}} points")
```

## 9. Resume
{topic} est une brique du module **{module_title}**. La bonne pratique est de comprendre le concept, coder un petit exemple, puis le reutiliser dans un projet.

## 10. Quiz rapide
Quelle ligne rend le programme plus lisible ? Une ligne avec un nom clair et une intention precise.

## 11. Challenge bonus
Transforme l'exemple en une fonction reutilisable, puis ajoute une validation d'entree.
""".strip()


def code_example(topic: str) -> list[dict]:
    return [
        {
            "title": f"Exemple simple - {topic}",
            "language": "python",
            "code": "nom = 'Ada'\nprint(f'Bonjour {nom}')",
            "explanation": "Un exemple minimal qui affiche une valeur lisible.",
        },
        {
            "title": "Version avec fonction",
            "language": "python",
            "code": "def saluer(nom: str) -> str:\n    return f'Bonjour {nom}'\n\nprint(saluer('Linus'))",
            "explanation": "La fonction rend le code reutilisable et testable.",
        },
    ]


def make_exercise(topic: str, lesson_slug: str, idx: int, level: str) -> dict:
    types = ["completer du code", "corriger une erreur", "ecrire une fonction"]
    difficulties = ["facile", "moyen", "difficile"]
    return {
        "slug": f"{lesson_slug}-exercice-{idx}",
        "title": f"{topic} - exercice {idx}",
        "description": f"Utilise la notion {topic.lower()} pour produire exactement la sortie attendue.",
        "starter_code": "# Ecris ton code ici\nprint('Python')",
        "expected_output": "Python",
        "solution": "print('Python')",
        "optimized_solution": "message = 'Python'\nprint(message)",
        "explanation": "La correction affiche la sortie attendue. La version optimisee isole la valeur dans une variable.",
        "difficulty": difficulties[(idx - 1) % len(difficulties)],
        "level": level,
        "theme": topic,
        "duration_minutes": 8 + idx * 4,
        "exercise_type": types[(idx - 1) % len(types)],
        "hints": ["Commence par lire la sortie attendue.", "Teste une version minimale.", "Compare chaque caractere affiche."],
        "tests": [{"input": "", "expected_stdout": "Python"}],
        "points": 10 + idx * 5,
    }


CORE_COURSES = [
    {
        "title": "Parcours Debutant Python",
        "level": "Debutant",
        "duration": "10 semaines",
        "track": "debutant",
        "description": "Pars de zero: installation, premiers programmes, variables, conditions, boucles, fonctions et collections.",
        "objectives": ["Ecrire des scripts simples", "Comprendre les erreurs", "Construire des programmes console"],
        "final_projects": ["Jeu du nombre mystere", "Carnet de contacts", "Mini quiz console"],
        "modules": [
            ("Introduction a Python", ["Qu'est-ce que Python", "Pourquoi apprendre Python", "Installer Python", "Installer VS Code", "Utiliser le terminal", "Lancer son premier programme", "Comprendre un fichier py", "Afficher du texte avec print", "Comment lire une erreur"]),
            ("Variables et types de donnees", ["Variables", "Nombres entiers", "Nombres decimaux", "Chaines de caracteres", "Booleens", "Conversion de types", "Nommage des variables", "Bonnes pratiques", "Erreurs frequentes"]),
            ("Operations", ["Addition", "Soustraction", "Multiplication", "Division", "Division entiere", "Modulo", "Puissance", "Priorites mathematiques", "Operations sur les chaines", "Formatage de texte"]),
            ("Conditions", ["if", "elif", "else", "Comparaisons", "Operateurs logiques", "Conditions imbriquees", "Cas pratiques", "Erreurs frequentes"]),
            ("Boucles", ["while", "for", "range", "break", "continue", "Boucles imbriquees", "Parcourir une chaine", "Exercices de repetition", "Mini-jeux"]),
            ("Fonctions", ["Creer une fonction", "Parametres", "Valeurs de retour", "return", "Scope", "Fonctions utiles", "Decouper un programme", "Documentation de fonctions", "Exercices progressifs"]),
            ("Listes", ["Creer une liste", "Ajouter un element", "Supprimer un element", "Modifier un element", "Parcourir une liste", "Trier une liste", "Slicing", "Listes imbriquees", "Exercices pratiques"]),
            ("Dictionnaires", ["Creer un dictionnaire", "Cles et valeurs", "Ajouter une donnee", "Modifier une donnee", "Supprimer une donnee", "Parcourir un dictionnaire", "Dictionnaires imbriques", "Cas concrets"]),
            ("Tuples et sets", ["Tuples", "Difference entre tuple et liste", "Sets", "Supprimer les doublons", "Operations sur les ensembles", "Utilisations concretes"]),
            ("Entrees utilisateur", ["input", "Conversion des entrees", "Validation", "Menus interactifs", "Programmes en console"]),
        ],
    },
    {
        "title": "Parcours Python Intermediaire",
        "level": "Intermediaire",
        "duration": "12 semaines",
        "track": "intermediaire",
        "description": "Passe du script simple au projet structure: erreurs, fichiers, modules, POO, algorithmes, tests, APIs et bases de donnees.",
        "objectives": ["Organiser un projet", "Tester du code", "Consommer une API", "Utiliser SQLite"],
        "final_projects": ["Gestionnaire de budget", "Application meteo avec API", "Analyseur de texte"],
        "modules": [
            ("Gestion des erreurs", ["try", "except", "else", "finally", "Lever une exception", "Creer ses propres erreurs", "Deboguer efficacement"]),
            ("Fichiers", ["Lire un fichier", "Ecrire dans un fichier", "Modifier un fichier", "Fichiers texte", "Fichiers CSV", "Fichiers JSON", "Gestion des chemins", "pathlib"]),
            ("Modules et packages", ["Importer un module", "Creer son propre module", "Utiliser pip", "Environnements virtuels", "requirements.txt", "Structure d'un projet Python"]),
            ("Programmation orientee objet", ["Classes", "Objets", "Attributs", "Methodes", "Constructeur", "self", "Encapsulation", "Heritage", "Polymorphisme", "Methodes magiques", "Dataclasses", "Cas pratiques"]),
            ("Comprehensions", ["List comprehensions", "Dict comprehensions", "Set comprehensions", "Generateurs", "Expressions conditionnelles"]),
            ("Fonctions avancees", ["Arguments par defaut", "args", "kwargs", "Fonctions lambda", "map", "filter", "zip", "enumerate", "sorted", "Decorateurs simples"]),
            ("Algorithmique", ["Complexite", "Recherche lineaire", "Recherche binaire", "Tri a bulles", "Tri par selection", "Tri rapide", "Recursion", "Structures de donnees", "Piles", "Files", "Arbres simples", "Graphes simples"]),
            ("Tests", ["Pourquoi tester", "assert", "unittest", "pytest", "Tests unitaires", "Tests d'integration", "Couverture de tests", "Organisation des tests"]),
            ("APIs", ["Comprendre une API", "Requetes HTTP", "GET", "POST", "PUT", "DELETE", "JSON", "Utiliser requests", "Authentification API", "Gerer les erreurs API"]),
            ("Bases de donnees", ["Introduction SQL", "SQLite", "Creer une table", "Ajouter des donnees", "Lire des donnees", "Modifier des donnees", "Supprimer des donnees", "Relations simples", "Utiliser Python avec SQLite", "Introduction a SQLAlchemy"]),
        ],
    },
    {
        "title": "Parcours Python Avance",
        "level": "Avance",
        "duration": "16 semaines",
        "track": "avance",
        "description": "Approfondis Python: architecture, typage, logging, async, performance, web, data, automatisation, IA, securite et deploiement.",
        "objectives": ["Ecrire du code professionnel", "Construire une API", "Automatiser des taches", "Deployer un projet"],
        "final_projects": ["API REST FastAPI", "Dashboard de donnees", "Portfolio Python complet"],
        "modules": [
            ("Python professionnel", ["Architecture de projet", "Clean code", "Typage avec type hints", "mypy", "Logging", "Configuration", "Variables d'environnement", "Documentation", "Packaging", "Deploiement"]),
            ("Programmation avancee", ["Decorateurs avances", "Context managers", "Iterators", "Generators", "Coroutines", "Asyncio", "Multithreading", "Multiprocessing", "Optimisation", "Profiling"]),
            ("Web avec Python", ["Flask", "FastAPI", "Routes", "Templates", "Formulaires", "Authentification", "Middleware", "Base de donnees", "API REST", "Documentation automatique", "Deploiement web"]),
            ("Data avec Python", ["NumPy", "pandas", "Nettoyage de donnees", "Analyse de donnees", "Visualisation matplotlib", "Visualisation seaborn", "Jupyter Notebook", "Lire CSV Excel JSON", "GroupBy", "Statistiques simples"]),
            ("Automatisation", ["Automatiser des fichiers", "Automatiser des emails", "Automatiser des rapports", "Planifier des scripts", "Web scraping", "BeautifulSoup", "Selenium", "Automatiser Excel", "Automatiser PDF", "Creer des scripts utiles"]),
            ("Intelligence artificielle", ["Introduction au machine learning", "scikit-learn", "Preparer des donnees", "Entrainer un modele", "Evaluer un modele", "Classification", "Regression", "Sauvegarder un modele", "Projet IA simple"]),
            ("Securite et bonnes pratiques", ["Gestion des mots de passe", "Variables secretes", "Eviter les injections SQL", "Securite des APIs", "Validation des entrees", "Permissions", "Bonnes pratiques de deploiement"]),
            ("Deploiement", ["Git", "GitHub", "README professionnel", "Docker", "Deploiement Render Railway VPS", "CI CD simple", "Tests automatiques", "Versioning"]),
        ],
    },
]

EXTRA_TRACKS = [
    ("Parcours Automatisation", "Intermediaire", "automatisation", ["Scripts utiles", "Pathlib en profondeur", "CSV et JSON", "Emails automatiques", "Rapports quotidiens", "Planification", "Scraping robuste", "Selenium", "Excel et PDF", "CLI de productivite", "Logs et reprise sur erreur", "Projet final automation"]),
    ("Parcours Programmation orientee objet", "Intermediaire", "poo", ["Modeliser un domaine", "Classe et instance", "Attributs controles", "Methodes pures", "Heritage utile", "Composition", "Protocoles", "Dataclasses", "Methodes magiques", "Design patterns simples", "Tests OO", "Refactoring"]),
    ("Parcours Developpement Web avec Python", "Avance", "web", ["HTTP", "Flask", "FastAPI", "Schemas Pydantic", "Routes REST", "Authentification JWT", "SQLAlchemy", "Migrations", "Templates", "Middleware", "Tests API", "Deploiement"]),
    ("Parcours Data Science avec Python", "Avance", "data", ["NumPy pratique", "pandas series", "pandas dataframe", "Nettoyage", "Jointures", "GroupBy", "Visualisation", "Notebook propre", "Statistiques", "Dashboard", "Pipeline data", "Projet final data"]),
    ("Parcours Intelligence Artificielle avec Python", "Avance", "ia", ["ML en clair", "Jeu de donnees", "Pretraitement", "Train test split", "Regression", "Classification", "Metriques", "Validation croisee", "Sauvegarde modele", "API de prediction", "Ethique", "Projet final IA"]),
    ("Parcours Algorithmique et logique", "Intermediaire", "algo", ["Logique booleenne", "Complexite", "Recherche", "Tris", "Recursion", "Piles", "Files", "Hash maps", "Arbres", "Graphes", "Backtracking", "Challenges chrono"]),
    ("Parcours Preparation portfolio developpeur Python", "Avance", "portfolio", ["Choisir ses projets", "README efficace", "Git propre", "Tests visibles", "Architecture", "API portfolio", "Dashboard portfolio", "Deploiement", "CI simple", "Presentation", "Entretien technique", "Roadmap emploi"]),
]

PROJECT_TITLES = [
    ("Calculatrice", "Debutant", "Console"), ("Convertisseur d'unites", "Debutant", "Console"), ("Generateur de mot de passe", "Debutant", "Securite"), ("Jeu du nombre mystere", "Debutant", "Jeu"), ("Pierre feuille ciseaux", "Debutant", "Jeu"),
    ("Gestionnaire de notes", "Debutant", "Console"), ("Todo list console", "Debutant", "Console"), ("Mini quiz", "Debutant", "Jeu"), ("Generateur de phrases", "Debutant", "Texte"), ("Carnet de contacts", "Debutant", "Fichiers"),
    ("Gestionnaire de fichiers", "Intermediaire", "Automatisation"), ("Bot Discord simple", "Intermediaire", "Bot"), ("Scraper web", "Intermediaire", "Scraping"), ("Application meteo avec API", "Intermediaire", "API"), ("Systeme de connexion", "Intermediaire", "Auth"),
    ("Gestionnaire de budget", "Intermediaire", "Data"), ("Analyseur de texte", "Intermediaire", "Texte"), ("Generateur de factures", "Intermediaire", "PDF"), ("Sauvegarde automatique", "Intermediaire", "Automation"), ("Interface Tkinter", "Intermediaire", "GUI"),
    ("API REST FastAPI", "Avance", "Web"), ("Application web complete", "Avance", "Web"), ("Dashboard de donnees", "Avance", "Data"), ("Bot automatise", "Avance", "Bot"), ("Systeme de recommandation simple", "Avance", "IA"),
    ("Scraping avance", "Avance", "Scraping"), ("Analyse pandas", "Avance", "Data"), ("Mini moteur de recherche", "Avance", "Algo"), ("Gestionnaire de base de donnees", "Avance", "DB"), ("Portfolio developpeur Python", "Avance", "Portfolio"),
    ("CLI de notes", "Debutant", "CLI"), ("Timer Pomodoro", "Debutant", "Productivite"), ("Validateur de mots de passe", "Debutant", "Securite"), ("Journal personnel JSON", "Debutant", "Fichiers"), ("Simulateur de des", "Debutant", "Jeu"),
    ("Explorateur CSV", "Intermediaire", "Data"), ("Renommeur de fichiers", "Intermediaire", "Automation"), ("Mini CRM", "Intermediaire", "DB"), ("API de citations", "Intermediaire", "API"), ("Bot de rappel", "Intermediaire", "Bot"),
    ("Service d'auth JWT", "Avance", "Securite"), ("Pipeline ETL", "Avance", "Data"), ("Microservice Docker", "Avance", "DevOps"), ("Crawler asynchrone", "Avance", "Async"), ("Tableau Kanban web", "Avance", "Web"),
    ("Analyseur de logs", "Avance", "Automation"), ("API de prediction ML", "Avance", "IA"), ("Generateur de rapports PDF", "Avance", "PDF"), ("Systeme de tests automatise", "Avance", "Tests"), ("Assistant portfolio complet", "Avance", "Portfolio"),
]

RESOURCE_TITLES = [
    "Cheatsheet variables", "Cheatsheet conditions", "Cheatsheet boucles", "Cheatsheet fonctions", "Cheatsheet listes", "Cheatsheet dictionnaires", "Glossaire Python", "Erreurs frequentes", "Raccourcis VS Code", "Commandes terminal utiles",
    "Guide virtualenv", "Guide pip", "Guide Git", "README professionnel", "Conseils portfolio", "Conseils stage", "Conseils entretien", "Documentation officielle Python", "Bonnes pratiques securite", "Plan de revision 30 jours",
]

BADGES = [
    ("first_lesson", "Premier programme", "Tu as termine ta premiere lecon.", "lessons_done", 1),
    ("ten_lessons", "10 lecons terminees", "Tu as installe une habitude solide.", "lessons_done", 10),
    ("fifty_lessons", "50 lecons terminees", "Tu avances comme dans une vraie ecole.", "lessons_done", 50),
    ("first_exercise", "Premier exercice", "Tu as valide ton premier exercice.", "exercises_passed", 1),
    ("ten_exercises", "10 exercices termines", "Tu as resolu 10 exercices.", "exercises_passed", 10),
    ("hundred_exercises", "100 exercices termines", "Tu as resolu 100 exercices.", "exercises_passed", 100),
    ("first_project", "Premier projet termine", "Tu as soumis ton premier projet.", "projects_done", 1),
    ("five_projects", "5 projets termines", "Tu construis un vrai portfolio.", "projects_done", 5),
    ("quiz_runner", "Quiz Runner", "Tu as reussi 5 quiz.", "quizzes_passed", 5),
    ("xp_500", "Codeur junior", "Tu as gagne 500 XP.", "xp", 500),
    ("xp_1200", "Developpeur intermediaire", "Tu as gagne 1200 XP.", "xp", 1200),
    ("xp_2500", "Developpeur confirme", "Tu as gagne 2500 XP.", "xp", 2500),
    ("xp_5000", "Python Master", "Tu as gagne 5000 XP.", "xp", 5000),
]


def ensure_users(db: Session) -> None:
    if not db.scalar(select(User).where(User.email == "admin@python.local")):
        db.add(User(username="admin", email="admin@python.local", password_hash=get_password_hash("Admin123!"), role="admin"))
    if not db.scalar(select(User).where(User.email == "demo@python.local")):
        db.add(User(username="demo", email="demo@python.local", password_hash=get_password_hash("Demo123!"), role="user"))


def seed_badges(db: Session) -> None:
    if db.scalar(select(Badge)):
        return
    for index, (code, title, description, rule_type, value) in enumerate(BADGES):
        db.add(Badge(code=code, title=title, description=description, icon="award", xp_required=value if rule_type == "xp" else 0, rule_type=rule_type, rule_value=value))


def seed_courses(db: Session) -> None:
    if db.scalar(select(Course)):
        return
    course_index = 1
    module_global_index = 1
    for data in CORE_COURSES:
        course = Course(
            slug=slugify(data["title"]),
            title=data["title"],
            description=data["description"],
            level=data["level"],
            track_type=data["track"],
            order_index=course_index,
            estimated_duration=data["duration"],
            objectives=data["objectives"],
            final_projects=data["final_projects"],
        )
        db.add(course)
        db.flush()
        for module_index, (module_title, topics) in enumerate(data["modules"], start=1):
            module = Module(
                course_id=course.id,
                title=f"Module {module_global_index}: {module_title}",
                description=f"Module progressif sur {module_title.lower()} avec lecons, quiz, exercices et projets courts.",
                level=data["level"],
                order_index=module_index,
                estimated_duration="3 a 5 h",
            )
            db.add(module)
            db.flush()
            for lesson_index, topic in enumerate(topics, start=1):
                base_slug = slugify(f"{module.title}-{topic}")
                lesson = Lesson(
                    module_id=module.id,
                    slug=base_slug,
                    title=topic,
                    content=lesson_markdown(topic, module.title, data["level"]),
                    code_examples=code_example(topic),
                    order_index=lesson_index,
                    difficulty="facile" if data["level"] == "Debutant" else "moyen" if data["level"] == "Intermediaire" else "difficile",
                    objectives=[f"Comprendre {topic.lower()}", "Coder un exemple", "Eviter les erreurs frequentes"],
                    common_errors=["Syntaxe incomplete", "Nom de variable peu clair", "Absence de test rapide"],
                    tips=["Ecris d'abord une version simple.", "Lis les erreurs de haut en bas.", "Decoupe le probleme."],
                    mini_exercise={"prompt": f"Cree un exemple utilisant {topic.lower()}.", "expected": "Un programme court et lisible."},
                    summary=f"Lecon sur {topic} dans {module_title}.",
                )
                db.add(lesson)
                db.flush()
                for ex_index in range(1, 4):
                    exercise_data = make_exercise(topic, lesson.slug, ex_index, data["level"])
                    db.add(Exercise(lesson_id=lesson.id, **exercise_data))
                quiz = Quiz(lesson_id=lesson.id, title=f"Quiz rapide - {topic}", description=f"Verifie que tu as compris {topic}.", difficulty=lesson.difficulty, time_limit_minutes=6)
                db.add(quiz)
                db.flush()
                db.add_all([
                    QuizQuestion(quiz_id=quiz.id, question=f"A quoi sert {topic} ?", question_type="qcm", options=["Structurer une idee", "Supprimer Python", "Changer de langage"], correct_answer="Structurer une idee", explanation="La notion sert a structurer un programme Python.", points=1),
                    QuizQuestion(quiz_id=quiz.id, question="Vrai ou faux: il faut tester souvent son code.", question_type="vrai/faux", options=["vrai", "faux"], correct_answer="vrai", explanation="Des tests frequents reduisent les erreurs.", points=1),
                ])
            module_quiz = Quiz(module_id=module.id, title=f"Quiz final - {module_title}", description="Quiz de validation du module.", difficulty=data["level"], time_limit_minutes=12)
            db.add(module_quiz)
            db.flush()
            db.add_all([
                QuizQuestion(quiz_id=module_quiz.id, question=f"Quel est le bon reflexe dans {module_title} ?", question_type="qcm", options=["Coder puis tester", "Copier sans comprendre", "Ignorer les erreurs"], correct_answer="Coder puis tester", explanation="Le cycle court code/test est essentiel.", points=2),
                QuizQuestion(quiz_id=module_quiz.id, question="Un code lisible aide la maintenance.", question_type="vrai/faux", options=["vrai", "faux"], correct_answer="vrai", explanation="La lisibilite est une competence professionnelle.", points=1),
            ])
            module_global_index += 1
        course_index += 1

    for extra_title, level, track, topics in EXTRA_TRACKS:
        course = Course(
            slug=slugify(extra_title),
            title=extra_title,
            description=f"Parcours specialise pour progresser en {extra_title.lower()} avec des exercices et projets orientes portfolio.",
            level=level,
            track_type=track,
            order_index=course_index,
            estimated_duration="6 a 10 semaines",
            objectives=["Renforcer les bases", "Construire des projets", "Documenter son travail"],
            final_projects=[f"Projet final {track}", "Projet portfolio", "Challenge de validation"],
        )
        db.add(course)
        db.flush()
        chunk_size = 4
        for module_index in range(0, len(topics), chunk_size):
            module_topics = topics[module_index : module_index + chunk_size]
            module_title = f"Specialisation {track} {module_index // chunk_size + 1}"
            module = Module(course_id=course.id, title=module_title, description=f"Bloc de competence {module_title.lower()}.", level=level, order_index=module_index + 1, estimated_duration="4 h")
            db.add(module)
            db.flush()
            for lesson_index, topic in enumerate(module_topics, start=1):
                slug = slugify(f"{course.title}-{module.title}-{topic}")
                lesson = Lesson(
                    module_id=module.id,
                    slug=slug,
                    title=topic,
                    content=lesson_markdown(topic, module.title, level),
                    code_examples=code_example(topic),
                    order_index=lesson_index,
                    difficulty="moyen" if level == "Intermediaire" else "difficile",
                    objectives=[f"Maitriser {topic.lower()}", "Appliquer sur un cas concret"],
                    common_errors=["Ne pas isoler les fonctions", "Ne pas ecrire de README", "Ne pas tester"],
                    tips=["Travaille par petites iterations.", "Ajoute un exemple reproductible."],
                    mini_exercise={"prompt": f"Ecris un mini script lie a {topic.lower()}.", "expected": "Un resultat verifiable."},
                    summary=f"Lecon specialisee: {topic}.",
                )
                db.add(lesson)
                db.flush()
                for ex_index in range(1, 4):
                    db.add(Exercise(lesson_id=lesson.id, **make_exercise(topic, lesson.slug, ex_index, level)))
                quiz = Quiz(lesson_id=lesson.id, title=f"Quiz rapide - {topic}", description="Validation courte.", difficulty=lesson.difficulty, time_limit_minutes=6)
                db.add(quiz)
                db.flush()
                db.add_all([
                    QuizQuestion(quiz_id=quiz.id, question=f"Pourquoi travailler {topic} ?", question_type="qcm", options=["Pour coder des projets utiles", "Pour eviter Python", "Pour supprimer les tests"], correct_answer="Pour coder des projets utiles", explanation="Le but est l'application concrete.", points=1),
                    QuizQuestion(quiz_id=quiz.id, question="Un projet portfolio doit etre documente.", question_type="vrai/faux", options=["vrai", "faux"], correct_answer="vrai", explanation="La documentation montre ton raisonnement.", points=1),
                ])
        course_index += 1


def seed_projects(db: Session) -> None:
    if db.scalar(select(Project)):
        return
    for index, (title, level, category) in enumerate(PROJECT_TITLES, start=1):
        db.add(
            Project(
                slug=slugify(title),
                title=title,
                description=f"Projet concret: {title}. Il permet de transformer les notions Python en competence visible.",
                level=level,
                category=category,
                estimated_duration="2 h" if level == "Debutant" else "6 h" if level == "Intermediaire" else "12 h",
                objective=f"Construire {title.lower()} avec un code clair, testable et documente.",
                skills=["Python", category, "Tests", "Documentation"],
                specifications="Le programme doit etre lisible, decoupe en fonctions, valider les entrees et fournir un README clair.",
                steps=["Analyser le besoin", "Ecrire une version minimale", "Ajouter les validations", "Tester", "Documenter", "Ajouter une amelioration"],
                starter_code="# Point de depart\ndef main():\n    print('Projet Python')\n\nif __name__ == '__main__':\n    main()",
                hints=["Commence petit.", "Teste une fonction a la fois.", "Ajoute un README."],
                final_code="def main():\n    print('Projet termine')\n\nif __name__ == '__main__':\n    main()",
                improvements=["Ajouter des tests", "Ajouter une interface", "Sauvegarder les donnees", "Preparer un deploiement"],
                bonus="Ajoute une version plus robuste avec configuration et logs.",
                difficulty="facile" if level == "Debutant" else "moyen" if level == "Intermediaire" else "difficile",
            )
        )


def seed_resources(db: Session) -> None:
    if db.scalar(select(ResourceItem)):
        return
    for index, title in enumerate(RESOURCE_TITLES, start=1):
        kind = "cheatsheet" if "Cheatsheet" in title else "guide" if "Guide" in title or "Conseils" in title else "memo"
        db.add(ResourceItem(title=title, slug=slugify(title), kind=kind, level="Tous niveaux", content=f"# {title}\n\nFiche pratique en francais avec exemples Python, erreurs frequentes et conseils d'application.", tags=[kind, "python", "memo"]))


def seed_challenges(db: Session) -> None:
    if db.scalar(select(Challenge)):
        return
    themes = ["Boucles", "Fonctions", "Listes", "Dictionnaires", "POO", "Fichiers", "API", "Algo", "Data", "Securite"]
    levels = ["Debutant", "Intermediaire", "Avance"]
    for index in range(1, 31):
        theme = themes[(index - 1) % len(themes)]
        level = levels[(index - 1) % len(levels)]
        title = f"Challenge {index}: {theme} chrono"
        db.add(
            Challenge(
                title=title,
                slug=slugify(title),
                description=f"Resous un probleme court sur {theme.lower()} en temps limite.",
                level=level,
                theme=theme,
                duration_minutes=15 + index,
                starter_code="# Complete la fonction\ndef solution():\n    return 'Python'\n\nprint(solution())",
                solution="def solution():\n    return 'Python'\n\nprint(solution())",
                tests=[{"expected_stdout": "Python"}],
                points=30 + index,
            )
        )


def seed_community(db: Session) -> None:
    if db.scalar(select(Discussion)):
        return
    demo = db.scalar(select(User).where(User.email == "demo@python.local"))
    db.add_all([
        Discussion(user_id=demo.id if demo else None, title="Comment bien commencer Python ?", slug="comment-bien-commencer-python", body="Partagez vos routines d'apprentissage et vos premiers projets.", theme="debutant", pinned=True),
        Discussion(user_id=demo.id if demo else None, title="Vos projets portfolio", slug="vos-projets-portfolio", body="Publiez vos projets et demandez un retour constructif.", theme="portfolio", pinned=False),
        Discussion(user_id=demo.id if demo else None, title="Defi hebdomadaire", slug="defi-hebdomadaire", body="Cette semaine: automatiser une tache repetee.", theme="challenge", pinned=True),
    ])


def seed_all(db: Session) -> None:
    ensure_users(db)
    seed_badges(db)
    seed_courses(db)
    seed_projects(db)
    seed_resources(db)
    seed_challenges(db)
    seed_community(db)
    db.commit()
