document.getElementById("submit").addEventListener('click', event => {
    event.preventDefault();
    const url = window.location.href;

    var data = {
        action: document.getElementById('action').value,
    };

    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': document.getElementsByName('csrfmiddlewaretoken')[0].value,
        },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(data => {
        const dict = JSON.parse(data);
        if('action' in dict){
            const success = dict['success'];
            alert(success);

            const action = dict['action'];
            switch(action){
                case 'start':
                    document.getElementById('start_server').classList.add('hidden');
                    document.getElementById('stop_server').classList.remove('hidden');
                    break;

                case 'stop':
                    document.getElementById('start_server').classList.remove('hidden');
                    document.getElementById('stop_server').classList.add('hidden');
                    break;

                default:
                    break;
            }
        }

        if('error' in dict){
            const error = dict['error'];
            alert(error);
        }
    })
    .catch(error => {
        console.error('Une erreur s\'est produite.')
    });
});