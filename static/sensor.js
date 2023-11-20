function initSensor() {
          sensor = new LinearAccelerationSensor({ frequency: 60 });
          sensor.onreading = function() {
            i = sensor.x.toFixed(2)
            j = sensor.y.toFixed(2)
            k = sensor.z.toFixed(2)
            $("#output").html(i+"<br>"+j+"<br>"+k+"<br>")
          }
          sensor.onerror = function(event) {
            if (event.error.name == 'NotReadableError') {
              console.log('Sensor is not available.');
            }
          };
          sensor.start();
          console.log('started')
      }
