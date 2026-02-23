from flask import Flask, request, jsonify, render_template

app = Flask(__name__)


accounts = {
    "100": {"name": "Kasa", "balance": 0},
    "600": {"name": "Yurtiçi Satışlar", "balance": 0},
    "770": {"name": "Genel Yönetim Giderleri", "balance": 0}
}


def ai_analiz(cumle):
    cumle = cumle.lower()
 
    if any(kelime in cumle for kelime in ["aldım", "ödedim", "fatura", "yemek", "yakıt"]):
        return "770", "100"  # Borç: Gider, Alacak: Kasa
 
    elif any(kelime in cumle for kelime in ["sattım", "geldi", "tahsil", "kazanç"]):
        return "100", "600"  # Borç: Kasa, Alacak: Gelir
    return "100", "100"      # Belirsiz durum


@app.route('/')
def index():
  
    return '''
        <h1>AI Muhasebe Asistanı</h1>
        <form action="/ai-add" method="post">
            Ne yaptınız? (Örn: 300 TL fatura ödedim): <br>
            <input type="text" name="text" style="width:300px;" required>
            <button type="submit">AI ile Kaydet</button>
        </form>
        <br><a href="/balance-sheet">Mizanı Gör</a>
    '''

@app.route('/ai-add', methods=['POST'])
def ai_add():
    user_text = request.form['text']
    

    amount = 0
    for kelime in user_text.split():
        if kelime.isdigit():
            amount = float(kelime)
            break
            

    debit, credit = ai_analiz(user_text)
    

    if amount > 0:
        accounts[debit]['balance'] += amount
        accounts[credit]['balance'] -= amount
        return f"<h3>AI Sonucu:</h3> <p>Cümle: {user_text}</p> <p>Tahmin: {accounts[debit]['name']} (+), {accounts[credit]['name']} (-)</p> <p>Tutar: {amount} TL</p> <a href='/'>Geri Dön</a>"
    else:
        return "Tutar anlaşılamadı. Lütfen rakam içeren bir cümle kurun. <a href='/'>Geri Dön</a>"

@app.route('/balance-sheet')
def get_balances():
    return jsonify(accounts)

if __name__ == '__main__':
    app.run(debug=True)


def ai_analiz(cumle):
    cumle = cumle.lower()
    

    gelir_kelimeleri = ["sattım", "geldi", "tahsil", "kazandım", "ödeme aldım", "satış", "hakediş"]
    

    gider_kelimeleri = ["aldım", "ödedim", "fatura", "yemek", "yakıt", "harcadım", "masraf"]

    if any(k in cumle for k in gelir_kelimeleri):
        return "100", "600", "Gelir (Satış)" # Borç: 100 (Kasa), Alacak: 600 (Gelir)
    
    elif any(k in cumle for k in gider_kelimeleri):
        return "770", "100", "Gider (Harcama)" # Borç: 770 (Gider), Alacak: 100 (Kasa)
    
    return "100", "100", "Belirsiz"

@app.route('/ai-add', methods=['POST'])
def ai_add():
    user_text = request.form['text']

    import re
    numbers = re.findall(r'\d+', user_text)
    amount = float(numbers[0]) if numbers else 0
            
    debit, credit, tur = ai_analiz(user_text)
    
    if amount > 0 and tur != "Belirsiz":
  
        accounts[debit]['balance'] += amount
        accounts[credit]['balance'] -= amount 

        
        return f"""
            <h3>İşlem Başarılı!</h3>
            <p>{amount} TL tutarındaki {tur} kaydı yapıldı.</p>
            <p>3 saniye içinde ana sayfaya yönlendiriliyorsunuz...</p>
    
            <meta http-equiv="refresh" content="3;url=/">
        """
    else:

        return "İşlem anlaşılamadı. Lütfen '500 TL satış yaptım' gibi net bir cümle kurun. <a href='/'>Geri Dön</a>"
