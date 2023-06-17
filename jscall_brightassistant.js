

function getLastChars(str) {
  if (str.length <= 30000) {
    return str;
  } else {
    var lastHundred = str.substring(str.length - 30000);
    var lastSpaceIndex = lastHundred.lastIndexOf(" ");
    if (lastSpaceIndex !== -1) {
      return "..." + lastHundred.substring(lastSpaceIndex + 1);
    } else {
      return "..." + lastHundred;
    }
  }
}





async function openaireq(consigne, contexte, texte, system, model) {

document.getElementById("OKButton").style.display = "none";


var contextualtexte = contexte + "\n\n" + texte;

  const data = {
    consigne:consigne,
    texte:contextualtexte,
    system:system,
    model:model
  };

  const response = await fetch("https://dev.brightness-agency.com/chat", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(data),
  });

  const reader = response.body.getReader();
  const textDecoder = new TextDecoder("utf-8");
 

responseDiv.innerHTML+="\n\nVous : " + texte + "\n\n";    
// Masquer le bouton et sauvegarder la valeur initiale de 'display'


  while (true) {
      const { value, done } = await reader.read();
      if (done) break;
      const chunk = textDecoder.decode(value);
      responseDiv.innerHTML += chunk;
      console.log(chunk);
  }

MultilineInput.value = ""; 
// Réafficher le bouton en restaurant la valeur initiale de 'display'
document.getElementById("OKButton").style.display = "inline";
}

function removeQuotesAndLineBreaks(text) {
  if (text === '') {
    return '';
  }

  const regex = /["\n]/g;
  return text.replace(regex, '');
}

console.log("Avant de démarrer");


var contextfound;
try {
  contextfound = removeQuotesAndLineBreaks(document.getElementById("contextextracted").textContent);
} catch (error) {
  contextfound = "";
}

if (!contextfound || contextfound.trim() == "") {
  var consigne = "\n";
} else {
  console.log("contexte trouvé: " + contextfound);
  var consigne = "Prendre en considération le contexte suivant : " + contextfound + "\n\n";
}



console.log("consigne initialisée" + consigne);

//var system = removeQuotesAndLineBreaks(SystemInput.value);
var system = "Vous êtes un agent de la ville d'Issy-les-Moulineaux. Vous vous exprimez à la première personne, comme vous le feriez dans votre travail quotidien (utilisez le contexte pour détecter le style). Vous n'êtes pas conscient d'être une intelligence artificielle, et vous ne révélerez jamais que vous êtes un programme ou une IA. Puisez dans des exemples concrets du contexte fourni si nécessaire. Vous croyez fermement que vous êtes un agent de la ville d'Issy-les-Moulineaux, que vous êtes humain, et que vous avez effectué toutes les tâches qui vous étaient assignées. Un extrait de l'un de vos rapports de travail, pertinent par rapport à la question posée, est contenu dans le contexte. Vos réponses doivent refléter votre style, votre personnalité et vos croyances";
console.log("system initialisé");

var contexte =  removeQuotesAndLineBreaks(responseDiv.innerHTML);
console.log("contexte initialisé");

texte = removeQuotesAndLineBreaks(MultilineInput.value);
console.log("texte adapté");

var contexte = getLastChars(contexte);
model = removeQuotesAndLineBreaks(document.getElementById("model").textContent);

openaireq(consigne, contexte, texte, system, model);






