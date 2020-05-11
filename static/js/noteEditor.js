// SideBars width
const SBWIDTH = [40, 20]
const COLOR_THEME = [
  '#F25C05', // Note fill
  '#F28705', // Note stroke
  50, // Background and light notes
  30, // Dark notes
  80  // Grid
]

var win_w = 600;
var win_h = 400;
var canvas;
var sc = [10, 20]; // Grid scale
// Grid shift
var x = 0;
var y = 816;
// Pos of start of drawing a note,
// (-1,-1) - not drawing
var startX = -1;
var startY = -1;
var toDraw;

var controlsDiv;
var slidersDiv;
var vScrollSlider;
var hScaleSlider;
var vScaleSlider;
var resetButton;

function loadSettings() {
  if (settings.length >= openedEditor + 1) {
    sc = settings[openedEditor].sc;
    x = settings[openedEditor].x;
    y = settings[openedEditor].y;

    hScaleSlider.value(sc[0]);
    vScaleSlider.value(sc[1]);
    vScaleSlider.elt.dispatchEvent(new Event('input'))
    vScrollSlider.value(y);
    drawEditor();
  } else {
    loadDefault();
    settings.push({});
    saveSettings();
  }
}

function loadDefault() {
  sc = [10, 20];
  x = 0;
  y = 816;
  
  hScaleSlider.value(sc[0]);
  vScaleSlider.value(sc[1]);
  vScaleSlider.elt.dispatchEvent(new Event('input'))
  vScrollSlider.value(y);
  drawEditor();
}

function saveSettings() {
  settings[openedEditor].sc = sc;
  settings[openedEditor].x = x;
  settings[openedEditor].y = y;
  drawEditor();
}

function setupCanvas() {
  div.style.position = 'relative';
  div.style.boxShadow = `0 0 10px 2px ${COLOR_THEME[0]}`;
  div.style.margin = '50px 10px';
  div.style.borderRadius = '5px';
  div.style.background = color(COLOR_THEME[3]);
  
  win_w = div.clientWidth;
  canvas = createCanvas(win_w, win_h);
  canvas.elt.style.display = 'block';
  canvas.elt.style.borderRadius = '5px';
  canvas.elt.style.borderBottom = `1px solid ${COLOR_THEME[0]}`;
  canvas.parent("noteEditor");
  
  controlsDiv = createDiv();
  controlsDiv.parent('noteEditor');
  controlsDiv.id('controlsDiv');
  controlsDiv.elt.style.display = 'flex';
  controlsDiv.elt.style.justifyContent = 'space-between';
  controlsDiv.elt.style.alignItems = 'center';
  controlsDiv.elt.style.padding = '4px 4px 4px 8px';
  
  slidersDiv = createDiv();
  slidersDiv.parent('controlsDiv');
  slidersDiv.id('slidersDiv');
  slidersDiv.elt.style.display = 'flex';
  slidersDiv.elt.style.alignItems = 'center';
}

function setupVScroll() {
  let max = 121 * sc[1] - win_h + SBWIDTH[1];
  vScrollSlider = createSlider(0, max, max / 2.5, 0.1);
  vScrollSlider.parent('#noteEditor')
  vScrollSlider.class('slider');
  
  vScrollSlider.elt.style.cssText = `
    transform: rotate(90deg);
    width: ${win_h - 40}px;
    position: absolute;
    top: ${win_h / 2}px;
    left: ${-win_h / 2 + 26}px;
  `;
  
  y = vScrollSlider.value();
  vScrollSlider.elt.addEventListener('input', function() {
    y = vScrollSlider.value();
  });
  
  vScrollSlider.mouseWheel(function(event) {
    vScrollSlider.value(vScrollSlider.value() + event.deltaY);
    y = vScrollSlider.value();
    drawEditor();
    return false;
  })
}

function setupHScale() {
  hScaleSlider = createSlider(5, 20, sc[0], 0.1);
  hScaleSlider.parent('slidersDiv');
  hScaleSlider.elt.style.marginRight = '10px';
  hScaleSlider.elt.addEventListener('input', function() {
    let newSc = hScaleSlider.value();
    
    // Change x to zoom into the center of viewport
    x += (x + win_w / 2 - SBWIDTH[0] / 2) / sc[0] * (newSc - sc[0]);
    if (x < 0) x = 0;
    
    sc[0] = newSc;
  });
}

function setupVScale() {
  vScaleSlider = createSlider(12, 40, sc[1], 0.1);
  vScaleSlider.parent('slidersDiv');
  
  vScaleSlider.elt.addEventListener('input', function() {
    let newSc = vScaleSlider.value();
    
    // Stay on the same note
    y += (y + win_h / 2 - SBWIDTH[1] / 2) / sc[1] * (newSc - sc[1]);
    
    sc[1] = newSc;
    
    // Refresh the limit
    vScrollSlider.elt.max = 121 * sc[1] - win_h + SBWIDTH[1];
    
    // Syncronize y and slider
    vScrollSlider.value(y);
    y = vScrollSlider.value();
  });
}

function setupButton() {
  resetButton = createButton('✕');
  resetButton.parent('controlsDiv');
  resetButton.elt.type = "button";
  resetButton.elt.onclick = function() {
    notes[openedEditor] = [];
    drawEditor();
  }
}

function drawHints() {
  noStroke();
  for (let i = 0; i < 121; i++) {
    let note = (i + 11) % 12;
    let drawY = i * sc[1] + SBWIDTH[1] - y;
    
    // if outside the canvas
    if (drawY < -sc[1]) {continue}
    else if (drawY > win_h) {break}
      
    switch (note) {
      // Black notes
      case 1:case 3:case 5:case 8:case 10:
        fill(COLOR_THEME[3]);
        rect(SBWIDTH[0], drawY, win_w - SBWIDTH[0], sc[1]);
        break;
      // C notes
      case 11:
        fill(COLOR_THEME[1])
        textAlign(RIGHT, CENTER);
        textSize(12);
        text("C" + (8 - i / 12), SBWIDTH[0] - 30, drawY, 30, sc[1]);
    }
  }
  
  // Background of sidebar on top
  fill(COLOR_THEME[2]);
  rect(SBWIDTH[0], 0, win_w - SBWIDTH[0], SBWIDTH[1]);
  
  // Numeration of beats
  let beat = Math.floor(x / (sc[0] * 8)) + 2;
  for (let i = 41 + sc[0] * 8 - (x % (sc[0] * 8));
       i <= win_w; i += sc[0] * 8) {
    fill(COLOR_THEME[1])
    textAlign(LEFT, TOP);
    textSize(SBWIDTH[1] * 0.5);
    text(beat, i, 1, SBWIDTH[1], SBWIDTH[1]);
    beat++;
  }
}

function drawGrid() {
  stroke(COLOR_THEME[4]);
  // Horizontal
  for (let i = SBWIDTH[1] + sc[1] - (y % sc[1]);
       i <= win_h; i += sc[1]) {
    line(SBWIDTH[0], i, win_w, i);
  }
  // Vertical
  for (let i = SBWIDTH[0] + sc[0] - (x % sc[0]);
       i <= win_w; i += sc[0]) {
    line(i, SBWIDTH[1] * 0.75, i, win_h);
  }
  // Vertical bolder
  stroke(COLOR_THEME[1]);
  for (let i = SBWIDTH[0] + sc[0] * 8 - (x % (sc[0] * 8));
       i <= win_w; i += sc[0] * 8) {
    line(i, SBWIDTH[1] * 0.5, i, win_h);
  }
  
  // Sidebars separators
  stroke(COLOR_THEME[0]);
  line(SBWIDTH[0], 0, SBWIDTH[0], win_h);
  line(SBWIDTH[0], SBWIDTH[1], win_w, SBWIDTH[1]);
}

function drawNotes() {
  stroke(COLOR_THEME[1]);
  fill(COLOR_THEME[0])
  for (let n of notes[openedEditor]) {n.draw();}
}

function Note(nx1, ny1, nx2) {
  this.x = Math.floor((nx1 + x - SBWIDTH[0]) / sc[0]);
  this.y = Math.floor((ny1 + y - SBWIDTH[1]) / sc[1]);
  this.dur = 0;
  this.setX2 = function(nx2) {
    this.dur = Math.floor((nx2 + x - SBWIDTH[0]) / sc[0]) - this.x + 1;
    if (this.dur < 0) {
      this.dur = 0;
    }
  }
  this.setX2(nx2);
  
  this.draw = function() {
    let drawX = this.x * sc[0] + SBWIDTH[0] - x;
    let drawY = this.y * sc[1] + SBWIDTH[1] - y;
    let drawW = this.dur * sc[0];
    let drawH = sc[1];
    if (drawX > SBWIDTH[0] - drawW && drawX < win_w &&
        drawY > SBWIDTH[1] - drawH && drawY < win_h) {
      if (drawX <= SBWIDTH[0]) {
        drawW += drawX - SBWIDTH[0] - 1;
        drawX = SBWIDTH[0] + 1;
      }
      if (drawY <= SBWIDTH[1]) {
        drawH += drawY - SBWIDTH[1] - 1;
        drawY = SBWIDTH[1] + 1;
      }
      rect(drawX, drawY, drawW, drawH, 2);
    }
  }
  
}

function setup() {
  setupCanvas();
  setupVScroll();
  setupHScale();
  setupVScale();
  setupButton();
  drawEditor();
  saveSettings();
}

// Drawing happens only after visual changes
function draw() {if (toDraw) {drawEditor()}}

function drawEditor() {
  background(COLOR_THEME[2]);
  drawHints();
  drawGrid();
  drawNotes();
  updateDur();
}

function mouseWheel(event) {
  if (0 < mouseX && mouseX < win_w &&
      0 < mouseY && mouseY < win_h) {
    if (SBWIDTH[0] < mouseX) {
      x += event.delta / 2;
      if (x < 0) {
        x = 0;
      }
    }
    drawEditor();
    
    return false;
  }
}

function mousePressed() {
  toDraw = true;
  if (SBWIDTH[0] < mouseX && mouseX < win_w &&
      SBWIDTH[1] < mouseY && mouseY < win_h) {
    startX = mouseX;
    startY = mouseY;
    lastNote = new Note(startX, startY, mouseX)
    notes[openedEditor].push(lastNote);
    
    // if clicked existing note
    for (let i = 0; i < notes[openedEditor].length - 1; i++) {
      let note = notes[openedEditor][i];
      if (note.x <= lastNote.x &&
          lastNote.x < note.x + note.dur &&
          lastNote.y == note.y) {
        notes[openedEditor].splice(i, 1);
        notes[openedEditor].pop();
        startX = -1;
        startY = -1;
        break;
      }
    }
    drawEditor();
    
    return false;
  }
}

function mouseReleased() {
  toDraw = false;
  if (startX > 0) {
    let lastNote = notes[openedEditor][notes[openedEditor].length - 1];
    if (lastNote.dur == 0) {
      notes[openedEditor].pop();
    } else {
      // if overlay delete all underlying
      for (let i = 0; i < notes[openedEditor].length - 1; i++) {
        let note = notes[openedEditor][i];
        if (lastNote.y == note.y &&
            lastNote.x <= note.x &&
            note.x < lastNote.x + lastNote.dur) {
          notes[openedEditor].splice(i, 1);
          i--;
        }
      }
    }
  }
  startX = -1;
  startY = -1;
  drawEditor();
}

function updateDur() {
  if (startX >= 0 && notes[openedEditor].length > 0) {
    notes[openedEditor][notes[openedEditor].length - 1].setX2(mouseX);
  }
}

function windowResized() {
  win_w = div.clientWidth;
  resizeCanvas(win_w, win_h);
  drawEditor();
}