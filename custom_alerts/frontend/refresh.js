let last_timestamp = Date.now()


async function fetch_alerts() {
    while (true) {
        try {
        const response = await window.fetch("/alert/get-alert")
        const json = await response.json()
        if (json.timestamp > last_timestamp) {
            console.log(json.value)
            switch (json.value) {
                case 'pinte':
                    new Audio('songs/burp.mp3').play()
                    break
            }
            last_timestamp = Date.now()
        }

        } catch(error) {
            console.log(error.message)
        }
        
        await new Promise(r => setTimeout(r, 2000));
        }
        
    
} 


fetch_alerts()


