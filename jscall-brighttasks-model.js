function removeQuotesAndLineBreaks(text) {
    if (text === '') {
      return '';
    }
  
    const regex = /["]/g;
    text = text.replace(regex, '');
    
    // Replace escaped line breaks with actual line breaks:
    text = text.replace(/\\n/g, '\n');
    return text;
  }
  
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
  
  async function openaireq(script, model) {
      
    // Masquer le bouton et sauvegarder la valeur initiale de 'display'
    var originalDisplayValue = document.getElementById("OKButton").style.display;
    document.getElementById("OKButton").style.display = "none";
    
      const data = {
        script: script,
        model: model
      };
      console.log("Le JSON envoyé est le suivant : \n" + JSON.stringify(data));
  
      const response = await fetch("https://dev.brightness-agency.com/streamtasks", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(data),
      });
  
      const reader = response.body.getReader();
      const textDecoder = new TextDecoder("utf-8");
    
  
    responseDiv.innerHTML+="\n\nVous : " + script + "\n\n";    
    
  
  
      while (true) {
          const { value, done } = await reader.read();
          if (done) break;
          const chunk = textDecoder.decode(value);
          responseDiv.innerHTML += chunk;
          console.log(chunk);
      }

    // Réafficher le bouton en restaurant la valeur initiale de 'display'
    document.getElementById("OKButton").style.display = originalDisplayValue;  
  

  }
  


  console.log("Avant de démarrer");

  // initialisation des variables
  script = removeQuotesAndLineBreaks(MultilineInput.value);
  model = removeQuotesAndLineBreaks(document.getElementById("model").textContent);
  

  // call de la fonction distante (API)
  console.log("texte adapté");
  console.log(script + "\n\n" + model);
  openaireq(script, model);
  
  MultilineInput.value = ""; 


  
  
  
  
  