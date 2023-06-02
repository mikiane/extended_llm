

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
  var originalDisplayValue = document.getElementById("OKButton").style.display;
  document.getElementById("OKButton").style.display = "none";
  
  
    while (true) {
        const { value, done } = await reader.read();
        if (done) break;
        const chunk = textDecoder.decode(value);
        responseDiv.innerHTML += chunk;
        console.log(chunk);
    }
  
  MultilineInput.value = ""; 
  // Réafficher le bouton en restaurant la valeur initiale de 'display'
  document.getElementById("OKButton").style.display = originalDisplayValue;
  
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
    var consigne = "Prendre en considération le l'extrait de la base Brightness suivant : " + contextfound + "\n\n";
  }

  

  console.log("consigne initialisée" + consigne);

  //var system = removeQuotesAndLineBreaks(SystemInput.value);
  var system = "Une IA capable de rédiger du texte en prenant en compte un contexte issu de la base Brightness et en s'appuyant sur celle-ci pour répondre à des instructions.";
  console.log("system initialisé" + system);
  
  var contexte =  removeQuotesAndLineBreaks(responseDiv.innerHTML);
  console.log("contexte initialisé" + contexte);
  
  texte = removeQuotesAndLineBreaks(MultilineInput.value);
  console.log("texte adapté" + texte);
  
  var contexte = getLastChars(contexte);
  model = removeQuotesAndLineBreaks(document.getElementById("model").textContent);
  console.log("modele récupéré" + model);

  openaireq(consigne, contexte, texte, system, model);
  
  
  
  
  
  
  