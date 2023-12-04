function initSensor() {
    sensor = new LinearAccelerationSensor({ frequency: 60 });
    sensor.onreading = function() {
      i = sensor.x.toFixed(2)
      j = sensor.y.toFixed(2)
      k = sensor.z.toFixed(2)
      $("#output").html(i+"<br>"+j+"<br>"+k+"<br>")
      console.log(i);
      $.ajax({
        url: `http://localhost:80/sensors/data`,
        type: 'POST',
        headers: {
'Content-Type': 'application/json'
},
        data: JSON.stringify({'val':`${i}_${j}_${k}`}),
        processData: false,  // Necessario per FormData
        contentType: false,  // Necessario per FormData
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


//  function logout () {

//  }