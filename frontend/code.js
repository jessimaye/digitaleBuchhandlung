// Beispiel-Bücher als Daten
let data = [
    {id:1, titel: "Veilchen", autor:"Sarah Müller", reihe:"keine Angabe", bild:"images/cover_veilchen.png", rueckseite: "images/buchruecken_veilchen.png", preis: 10, leseprobe: "Es war einmal..."},
    {id:2, titel: "Gänseblümchen", autor:"Sarah Müller", reihe:"keine Angabe"},
    {id:3, titel: "Nelke", autor:"Max Schmidt", reihe:"keine Angabe"},
    {id:4, titel: "Tulpe", autor:"Nele Neu", reihe:"Blumenwiese"},
    {id:5, titel: "Distel", autor:"Mele Alt", reihe:"Blumenwiese"},
];

//Suchfunktion

function filterBooks(){
    //Abfragen der Sucheingabe und der ausgewählten Kategorien
    let searchInput = document.getElementById("search-input").value.toLowerCase();
    let checkedBoxes = Array.from(document.querySelectorAll(".search-category:checked"));

    //Warnhinweis, wenn keine Kategorie ausgewählt wurde
    if (checkedBoxes.length === 0){
        alert("Bitte eine Kategorie auswählen");
        return;
    }

    //Umwandeln des Arrays in eine Liste
    
    let categories = [];
    
    for (element of checkedBoxes){
        categories.push(element.value);
    }

    //Abgleich der ausgewählten Kategorien und der Sucheingabe mit den hinterlegten Büchern/Daten
    //Buch kommt in die Ergebnisse, wenn mindestens eine der ausgewählten Kategorien den gesuchten Begriff enthält
    //Passt mindestens eine Kategorie? -> True, ist der Suchbegriff in dieser Kategorie enthalten? -> True
    let results = data.filter(book =>
        categories.some(category =>
            book[category].toLowerCase().includes(searchInput))
        )
    
    displayResults(results);

}


//Anzeigen der Suchergebnisse 
function displayResults(books){
    let container = document.getElementById("results")
    container.innerHTML = "";

    //Wenn kein passendes Buch zur Sucheingabe gefunden wurde

    if(books.length === 0){
        container.innerHTML = "Keine Ergebnisse gefunden";
        return;
    }

    //Gefundene Bücher mit Titel, Autor und Link auf Detailseite anzeigen
    books.forEach(book => {
        let div = document.createElement("div");
        div.className = "book";
        div.innerHTML = '<a href="detail.html?id=' + book.id + '">' + "<strong>" + book.titel + "</strong><br>" + "Autor:" + book.autor + "<br>" + "<p></p>";
        container.appendChild(div);
    });

}

//Buch über ID aus den Daten für Detailanzeige finden
function findDetails() {
    let params = new URLSearchParams(window.location.search);
    let id = Number(params.get("id"));

    let book = data.find (book => book.id == id);

    document.getElementById("details").innerHTML =
    "<h1>" +book.titel + "</h1>" + 
    "Autor:" + book.autor + "<br>" +
    "<p></p>" + 
    '<div class ="cover-wrapper">'+
        '<img src="' + book.bild + '"height="450px" width="300px">' +
        '<img src="' + book.rueckseite + '"height="450px" width="300px" class="hover">' +
    "</div>" +
    "<p></p>" +
    "Preis: " + book.preis + " Euro" +
    "<p></p>" +
    "Leseprobe: " + book.leseprobe;
}

//Chatbot, Kommunikation mit dem Flask-Backend, um auf das RAG-Modell zugreifen zu können
//nimmt Frage und sendet sie weiter an die Flask-Schnittstelle, die die Frage an die Rag-Pipeline übergibt und die Antwort zurückgibt
//erstellt neues div mit der User-Frage und der Antwort

let history = [];

async function send() {
    let input = document.getElementById("chat_input");
    let question = input.value.trim();
    if (!question) return; //wenn keine Frage gestellt wird, wird die API nicht aufgerufen

    addMessage("user",question);
    input.value = "";

    let response = await fetch("/chat", {
        method: "POST",
        headers: {"Content-Type":"application/json"},
        body: JSON.stringify({question,history})
    });

    let data = await response.json();
    if (data.error) {
        addMessage ("assistant", "Fehler:" + data.error);
    } else {
        addMessage("assistant", data.answer);
        history = data.history;
    }
}

function addMessage (role, content){
    let chat = document.getElementById("chat");
    let div = document.createElement("div");
    div.className = role;
    div.innerHTML = `<div class="message">${content.replace(/\n/g, "<br>")}</div>`;
    chat.appendChild(div);
    chat.scrollTop = chat.scrollHeight;
}

document.getElementById("chat_input").addEventListener("keypress", e => {
    if (e.key === "Enter") send();
});