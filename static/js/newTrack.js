var notes = [[]];
var settings = [{}];
var openedEditor = 0;
var form = document.getElementById('form');
var div = document.getElementById("noteEditor");
var instMax = 5;

function addInstrument() {
    if (notes.length == instMax - 1) {
        document.getElementById('add').style.display = "none";
    }
    if (notes.length >= instMax) {
        alert(`Вы не можете добавить более ${instMax} инструментов`)
        return;
    }

    let newInst = document.createElement('div');
    newInst.id = "inst" + notes.length;
    newInst.className = "instrument";

    let nameP = document.createElement('p')
    let newInstName = document.getElementById("instName0").cloneNode(true);
    newInstName.id = "instName" + notes.length;
    nameP.appendChild(newInstName);
    newInst.appendChild(nameP);

    let btnEdit = document.getElementById("0").cloneNode(true);
    btnEdit.id = notes.length;
    newInst.appendChild(btnEdit);

    document.getElementById('instruments').appendChild(newInst);

    notes.push([]);

    openEditor(notes.length - 1);
}

function openEditor(index) {
    saveSettings();
    document.getElementById('inst' + openedEditor).style.boxShadow = 'none';
    openedEditor = parseInt(index);
    document.getElementById('inst' + openedEditor).style.boxShadow = '0 0 10px 0 #F25C05';
    loadSettings();
}

function sendForm() {
    let res = {}
    res.title = document.getElementById("title").value;
    res.tempo = parseInt(document.getElementById("tempo").value);
    res.instruments = [];
    for (let i = 0; i < notes.length; i++) {
        let instName = document.getElementById("instName" + i);
        res.instruments.push([instName.options[instName.selectedIndex].value]);
        for (let note of notes[i]) {
            res.instruments[i].push([note.x, note.y, note.dur])
        }
    }

    var xhr = new XMLHttpRequest();
    xhr.open("POST", "/track", true);
    xhr.setRequestHeader("Content-Type", "application/json");
    xhr.onreadystatechange = function () {
        if (xhr.readyState === 4 && xhr.status === 200) {
            window.location.replace(xhr.responseText);
        }
    };
    xhr.send(JSON.stringify(res));
}