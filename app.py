from flask import Flask, render_template, request, redirect, url_for, flash, session
import os
from werkzeug.utils import secure_filename
import json
import uuid


USERS_FILE = "./utenti.json"
PRODOTTI_FILE = "./prodotti.json"
UPLOAD_FOLDER = "static/public/prodotti-images"
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif"}

app = Flask(__name__, template_folder="./template")
app.secret_key = 'supersecretkey'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    if '.' in filename:
        estensione = filename.rsplit('.', 1)[1].lower()
        if estensione in ALLOWED_EXTENSIONS:
            return True
    return False


@app.route('/')
@app.route('/index.html')
def index():
    user = session.get('user')

    if user:
        if os.path.exists(USERS_FILE):
            with open(USERS_FILE, 'r') as f:
                utenti = json.load(f)

            utente_trovato = None
            for u in utenti:
                if u.get('email') == user.get('email'):
                    utente_trovato = u
                    break

            if utente_trovato:
                user = utente_trovato
                session['user'] = user

    prodotti = []
    if os.path.exists(PRODOTTI_FILE):
        try:
            with open(PRODOTTI_FILE, 'r') as f:
                contenuto = f.read().strip()
                if contenuto:
                    prodotti = json.loads(contenuto)
                else:
                    prodotti = []
        except json.JSONDecodeError:
            prodotti = []

    return render_template("index.html", user=user, prodotti=prodotti)


@app.route('/carrello.html')
def carrello():
    if 'user' not in session:
        return render_template("carrello_not_logged.html")

    user_data = session['user']
    email_user = user_data['email']
    prodotti = []

    if os.path.exists(PRODOTTI_FILE):
        try:
            with open(PRODOTTI_FILE, 'r') as f:
                contenuto = f.read().strip()
                if contenuto:
                    tutti_prodotti = json.loads(contenuto)
                else:
                    tutti_prodotti = []
        except json.JSONDecodeError:
            tutti_prodotti = []
    else:
        tutti_prodotti = []

    if os.path.exists(USERS_FILE):
        try:
            with open(USERS_FILE, 'r') as u:
                users = json.load(u)
        except json.JSONDecodeError:
            users = []
    else:
        users = []

    for user in users:
        if user.get('email') == email_user:
            if 'carrello' in user:
                carrello = user['carrello']
                for prodotto in carrello:
                    for m in tutti_prodotti:
                        if prodotto['id'] == m['id']:
                            prodotti.append(m)
            break

    return render_template('carrello.html', user=user_data, prodotti=prodotti)


@app.route('/abbigliamento.html')
def abbigliamento():
    user = session.get('user')

    if user:
        if os.path.exists(USERS_FILE):
            with open(USERS_FILE, 'r') as f:
                utenti = json.load(f)

            utente_trovato = None
            for u in utenti:
                if u.get('email') == user.get('email'):
                    utente_trovato = u
                    break

            if utente_trovato:
                user = utente_trovato
                session['user'] = user

    prodotti = []
    if os.path.exists(PRODOTTI_FILE):
        try:
            with open(PRODOTTI_FILE, 'r') as f:
                contenuto = f.read().strip()
                if contenuto:
                    prodotti = json.loads(contenuto)
                else:
                    prodotti = []
        except json.JSONDecodeError:
            prodotti = []
    return render_template("abbigliamento.html", user=user, prodotti=prodotti)


@app.route('/accessori.html')
def accessori():
    user = session.get('user')

    if user:
        if os.path.exists(USERS_FILE):
            with open(USERS_FILE, 'r') as f:
                utenti = json.load(f)

            utente_trovato = None
            for u in utenti:
                if u.get('email') == user.get('email'):
                    utente_trovato = u
                    break

            if utente_trovato:
                user = utente_trovato
                session['user'] = user

    prodotti = []
    if os.path.exists(PRODOTTI_FILE):
        try:
            with open(PRODOTTI_FILE, 'r') as f:
                contenuto = f.read().strip()
                if contenuto:
                    prodotti = json.loads(contenuto)
                else:
                    prodotti = []
        except json.JSONDecodeError:
            prodotti = []
    return render_template("accessori.html", user=user, prodotti=prodotti)


@app.route('/modelliInScala.html')
def modelli_in_scala():
    user = session.get('user')

    if user:
        if os.path.exists(USERS_FILE):
            with open(USERS_FILE, 'r') as f:
                utenti = json.load(f)

            utente_trovato = None
            for u in utenti:
                if u.get('email') == user.get('email'):
                    utente_trovato = u
                    break

            if utente_trovato:
                user = utente_trovato
                session['user'] = user

    prodotti = []
    if os.path.exists(PRODOTTI_FILE):
        try:
            with open(PRODOTTI_FILE, 'r') as f:
                contenuto = f.read().strip()
                if contenuto:
                    prodotti = json.loads(contenuto)
                else:
                    prodotti = []
        except json.JSONDecodeError:
            prodotti = []
    return render_template("modelliInScala.html", user=user, prodotti=prodotti)


@app.route('/profilo.html')
def profilo():
    if 'user' in session:
        user_data = session['user']
        user_email = user_data.get('email')

        # Controlla che esista il file prodotti
        if not os.path.exists(PRODOTTI_FILE):
            flash("Nessun prodotto trovato.", "warning")
            prodotti_venditore = []
        else:
            with open(PRODOTTI_FILE, 'r') as f:
                prodotti = json.load(f)

            # Filtra i prodotti del venditore
            prodotti_venditore = [
                prodotto for prodotto in prodotti if prodotto.get('venditore_email') == user_email
            ]

        return render_template('profilo.html', user=user_data, prodotti=prodotti_venditore)
    else:
        return render_template('not_logged_in.html')


@app.route('/login.html', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        if not os.path.exists(USERS_FILE):
            flash('Nessun utente registrato. Per favore registrati prima.', 'warning')
            return redirect(url_for('register'))

        with open(USERS_FILE, 'r') as f:
            users = json.load(f)

        for user in users:
            if user['email'] == email and user['password'] == password:
                session['user'] = user
                flash('Login effettuato con successo!', 'success')
                return redirect(url_for('index'))

        flash('Credenziali non valide. Riprova.', 'danger')
        return redirect(url_for('login'))

    return render_template("login.html")


@app.route('/register.html', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        password = request.form['password']

        nuovo_utente = {
            "nome": nome,
            "email": email,
            "password": password,
            "prodotti_in_vendita": 0,
            "vendite_concluse": 0,
            "guadagni": 0.0
        }

        if os.path.exists(USERS_FILE):
            with open(USERS_FILE, 'r') as f:
                try:
                    utenti = json.load(f)
                except json.JSONDecodeError:
                    utenti = []
        else:
            utenti = []

        for utente in utenti:
            if utente['email'] == email:
                flash('Utente già registrato. Prova a fare il login.', 'warning')
                return redirect(url_for('login'))

        utenti.append(nuovo_utente)

        with open(USERS_FILE, 'w') as f:
            json.dump(utenti, f, indent=4)

        flash('Registrazione completata con successo! Ora puoi accedere.', 'success')
        return redirect(url_for('login'))

    return render_template("register.html")


@app.route('/logout')
def logout():
    session.pop('user', None)
    flash('Logout effettuato con successo.', 'info')
    return redirect(url_for('index'))


@app.route('/nuovoProdotto', methods=['GET', 'POST'])
def nuovoProdotto():
    if 'user' not in session:
        flash('Devi essere loggato per aggiungere un prodotto.', 'warning')
        return redirect(url_for('login'))

    if request.method == 'POST':
        nome = request.form['nome']
        descrizione = request.form['descrizione']
        prezzo = request.form['prezzo']
        categoria = request.form['categoria']
        team = request.form['team']
        immagine = request.files['immagine']

        prodotto_id = str(uuid.uuid4())

        if immagine and allowed_file(immagine.filename):
            estensione = os.path.splitext(secure_filename(immagine.filename))[1]
            nuovo_nome_immagine = prodotto_id + estensione

            os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
            img_path = os.path.join(app.config['UPLOAD_FOLDER'], nuovo_nome_immagine)
            immagine.save(img_path)

            percorso_relativo = f"public/prodotti-images/{nuovo_nome_immagine}"
        else:
            flash('Immagine non valida o mancante.', 'danger')
            return redirect(url_for('index'))

        venditore = session['user']

        nuovo_prodotto = {
            "id": prodotto_id,
            "nome": nome,
            "descrizione": descrizione,
            "prezzo": float(prezzo),
            "immagine": percorso_relativo,
            "venditore_nome": venditore.get("nome"),
            "venditore_email": venditore.get("email"),
            "categoria": categoria,
            "team": team
        }

        # Carica prodotti esistenti
        if os.path.exists(PRODOTTI_FILE):
            try:
                with open(PRODOTTI_FILE, 'r') as f:
                    prodotti = json.load(f)
            except json.JSONDecodeError:
                prodotti = []
        else:
            prodotti = []

        # Aggiungi nuovo prodotto
        prodotti.append(nuovo_prodotto)

        with open(PRODOTTI_FILE, 'w') as f:
            json.dump(prodotti, f, indent=4)

        # AGGIORNA NUMERO DI PRODOTTI VENDUTI
        if os.path.exists(USERS_FILE):
            with open(USERS_FILE, 'r') as f:
                try:
                    utenti = json.load(f)
                except json.JSONDecodeError:
                    utenti = []

            for utente in utenti:
                if utente.get("email") == venditore.get("email"):
                    prodotti_attuali = utente.get("prodotti_in_vendita", 0)
                    utente["prodotti_in_vendita"] = prodotti_attuali + 1
                    session['user']['prodotti_in_vendita'] = utente["prodotti_in_vendita"]
                    break

            with open(USERS_FILE, 'w') as f:
                json.dump(utenti, f, indent=4)

        flash('Prodotto aggiunto con successo!', 'success')
        return redirect(url_for('index'))

    return render_template("nuovoProdotto.html")









@app.route('/prodotto/<id>')
def prodotto(id):
    user_data = session.get('user')

    if os.path.exists(PRODOTTI_FILE):
        with open(PRODOTTI_FILE, 'r') as f:
            try:
                prodotti = json.load(f)
            except json.JSONDecodeError:
                flash("Errore nella lettura del file dei prodotti.", "danger")
                return redirect(url_for("index"))

            for prod in prodotti:
                if prod.get("id") == id:
                    # Passa user_data solo se non è None
                    return render_template("pagina_prodotto.html", prodotto=prod, prodotti=prodotti, user=user_data)

    flash("Prodotto non trovato.", "danger")
    return redirect(url_for("index"))


@app.route('/aggiungi_al_carrello/<prodotto_id>', methods=['POST'])
def aggiungi_al_carrello(prodotto_id):
    if 'user' not in session:
        flash("Devi essere loggato per aggiungere al carrello.", "warning")
        return redirect(url_for('login'))

    user_email = session['user']['email']

    if not os.path.exists(PRODOTTI_FILE):
        flash("Prodotto non trovato.", "danger")
        return redirect(url_for("index"))

    with open(PRODOTTI_FILE, 'r') as f:
        prodotti = json.load(f)

    prodotto_trovato = None
    for p in prodotti:
        if p['id'] == prodotto_id:
            prodotto_trovato = p
            break

    if not prodotto_trovato:
        flash("Prodotto non trovato.", "danger")
        return redirect(url_for("index"))

    categoria = prodotto_trovato['categoria']

    if not os.path.exists(USERS_FILE):
        flash("Errore interno. Nessun file utenti.", "danger")
        return redirect(url_for("index"))

    with open(USERS_FILE, 'r') as f:
        utenti = json.load(f)

    for utente in utenti:
        if utente.get("email") == user_email:
            if 'carrello' not in utente:
                utente['carrello'] = []

            # Controlla se il prodotto è già nel carrello
            prodotto_gia_presente = any(
                prodotto.get("id") == prodotto_id for prodotto in utente['carrello']
            )
            if prodotto_gia_presente:
                flash("Il prodotto è già presente nel carrello.", "info")
                return redirect(request.referrer or url_for("index"))

            utente['carrello'].append({
                "id": prodotto_id,
                "categoria": categoria
            })
            break
    else:
        flash("Utente non trovato.", "danger")
        return redirect(url_for("index"))

    with open(USERS_FILE, 'w') as f:
        json.dump(utenti, f, indent=4)

    flash("Prodotto aggiunto al carrello!", "success")
    return redirect(request.referrer or url_for("index"))




@app.route('/rimuovi_dal_carrello/<prodotto_id>', methods=['POST'])
def rimuovi_dal_carrello(prodotto_id):
    if 'user' not in session:
        flash("Devi essere loggato per modificare il carrello.", "warning")
        return redirect(url_for('login'))

    user_data = session['user']
    email_utente = user_data['email']

    if not os.path.exists(USERS_FILE):
        flash("File utenti non trovato.", "danger")
        return redirect(url_for('carrello'))

    with open(USERS_FILE, 'r') as f:
        utenti = json.load(f)

    # Trova l'utente con l'email specificata
    for utente in utenti:
        if utente.get("email") == email_utente:
            if "carrello" in utente and isinstance(utente["carrello"], list):
                carrello_originale = utente["carrello"]
                carrello_aggiornato = [
                    prodotto for prodotto in carrello_originale
                    if prodotto.get("id") != prodotto_id
                ]
                utente["carrello"] = carrello_aggiornato

                with open(USERS_FILE, 'w') as f_out:
                    json.dump(utenti, f_out, indent=4)

                flash("Prodotto rimosso dal carrello con successo.", "success")
                return redirect(url_for('carrello'))

            else:
                flash("Nessun prodotto da rimuovere nel carrello.", "info")
                return redirect(url_for('carrello'))

    flash("Utente non trovato.", "danger")
    return redirect(url_for('carrello'))



@app.route('/elimina_prodotto/<prodotto_id>', methods=['POST'])
def elimina_prodotto(prodotto_id):
    if 'user' not in session:
        flash("Devi essere loggato per eliminare un prodotto.", "warning")
        return redirect(url_for('login'))

    user_email = session['user']['email']

    # Carica i prodotti
    if not os.path.exists(PRODOTTI_FILE):
        flash("File prodotti non trovato.", "danger")
        return redirect(url_for('profilo'))

    with open(PRODOTTI_FILE, 'r') as f:
        prodotti = json.load(f)

    prodotti_aggiornati = []
    prodotto_trovato = False

    for p in prodotti:
        if p['id'] == prodotto_id and p.get('venditore_email') == user_email:
            prodotto_trovato = True
            # Elimina l'immagine se esiste
            immagine_path = os.path.join('static', p.get('immagine', ''))
            if os.path.exists(immagine_path):
                try:
                    os.remove(immagine_path)
                except Exception as e:
                    app.logger.error(f"Errore eliminando immagine {immagine_path}: {e}")
        else:
            prodotti_aggiornati.append(p)

    if not prodotto_trovato:
        flash("Prodotto non trovato o non autorizzato.", "warning")
        return redirect(url_for('profilo'))

    # Salva il file aggiornato dei prodotti
    with open(PRODOTTI_FILE, 'w') as f:
        json.dump(prodotti_aggiornati, f, indent=4)

    # Aggiorna il contatore dell'utente
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, 'r') as f:
            utenti = json.load(f)

        for utente in utenti:
            if utente['email'] == user_email:
                utente['prodotti_in_vendita'] = max(utente.get('prodotti_in_vendita', 1) - 1, 0)
                session['user']['prodotti_in_vendita'] = utente['prodotti_in_vendita']
                break

        with open(USERS_FILE, 'w') as f:
            json.dump(utenti, f, indent=4)

    flash("Prodotto eliminato con successo.", "success")
    return redirect(url_for('profilo'))



@app.route('/vendita/<prodotto_id>', methods=['POST'])
def vendita(prodotto_id):
    if 'user' not in session:
        flash("Devi essere loggato per concludere una vendita.", "warning")
        return redirect(url_for('login'))

    if not os.path.exists(PRODOTTI_FILE) or not os.path.exists(USERS_FILE):
        flash("Errore interno. File mancanti.", "danger")
        return redirect(url_for("index"))

    with open(PRODOTTI_FILE, 'r') as f:
        prodotti = json.load(f)

    prodotto = next((p for p in prodotti if p['id'] == prodotto_id), None)
    if not prodotto:
        flash("Prodotto non trovato.", "danger")
        return redirect(url_for("index"))

    email_venditore = prodotto.get("venditore_email")
    prezzo = float(prodotto.get("prezzo", 0))

    # Carica utenti
    with open(USERS_FILE, 'r') as f:
        utenti = json.load(f)

    for utente in utenti:
        if utente.get("email") == email_venditore:
            utente['vendite_concluse'] = utente.get('vendite_concluse', 0) + 1
            utente['guadagni'] = float(utente.get('guadagni', 0.0)) + prezzo
            break
    else:
        flash("Venditore non trovato.", "danger")
        return redirect(url_for("index"))

    # Salva modifiche
    with open(USERS_FILE, 'w') as f:
        json.dump(utenti, f, indent=4)

    flash("Vendita registrata con successo!", "success")
    return redirect(url_for("index"))


if __name__ == "__main__":
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    app.run(host="127.0.0.1", port=5555, debug=True)
