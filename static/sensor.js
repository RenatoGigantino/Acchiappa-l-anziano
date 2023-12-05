function initSensor() {
  sensor = new LinearAccelerationSensor({ frequency: 60 });
  sensor.onreading = function() {
    i = sensor.x.toFixed(2)
    j = sensor.y.toFixed(2)
    k = sensor.z.toFixed(2)

    // Sostituisci la soglia con il valore desiderato
    const soglia_i = 2.0;
    const soglia_j = 2.0;
    const soglia_k = 2.0;

    $("#output").html(i+"<br>"+j+"<br>"+k+"<br>")
    console.log(i);

    if (Math.abs(parseFloat(i)) > soglia_i || Math.abs(parseFloat(j)) > soglia_j || Math.abs(parseFloat(k)) > soglia_k) {
      // Se uno dei valori supera la soglia, invia la mail
      mail();

      // Effettua una richiesta AJAX per inviare i valori al database
      $.ajax({
        url: `http://localhost:80/sensors/data`,
        type: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        data: JSON.stringify({'val':`${i}_${j}_${k}`}),
        processData: false,
        contentType: false,
        success: function(data) {
          // Gestisci la risposta qui, se necessario
          console.log(data);
        },
        error: function(error) {
          // Gestisci gli errori qui, se necessario
          console.error('Errore nella richiesta:', error);
        }
      });
    }
  };

  sensor.onerror = function(event) {
    if (event.error.name == 'NotReadableError') {
      console.log('Sensor is not available.');
    }
  };

  sensor.start();
  console.log('started')
}



// ho aggiunto questa funzione (con un bottone per comodita' di debug) 
// per provare a scrivere uno script che chiamasse l'api definita in main.py con root /sendemail
// logicamente questa funzione andrebbe chiamata quando i valori registrati
// dal sensore (quindi fare un if nella funzione sopra) rileva una caduta
// da qui viene chiamata l'api che gestisce l'invio della mail
async function mail(){
  // console.log("ciao")
  try {
      const response = await fetch('http://localhost:80/sendemail', {
          method: 'GET',
          mode: "cors",
          headers: {
              'Accept': 'application/json',
              'Content-Type': 'application/json',
          },
      });
      const json = await response.json();
  } catch (error) {
      // console.log("qui")
      console.error(error);
  }
  
}


function logout() {
  // Effettua una richiesta AJAX per eseguire il logout
  $.ajax({
      url: 'http://localhost:80/logout', // Assicurati di utilizzare l'URL corretto per il logout
      type: 'GET',
      success: function (data) {
          // Gestisci la risposta qui, se necessario
          console.log(data);
          // Reindirizza l'utente alla pagina di login o a un'altra pagina appropriata
          window.location.href = "login.html"; // Cambia '/login' con il percorso desiderato
      },
      error: function (error) {
          // Gestisci gli errori qui, se necessario
          console.error('Errore nella richiesta di logout:', error);
      }
  });
}
