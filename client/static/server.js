document.getElementById("submit").addEventListener('click', event => {
    event.preventDefault();
    const url = window.location.href;

    var data = {
        action: document.getElementById('action'),
    };

    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': document.getElementByName('csrfmiddlewaretoken')[0].value,
        },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(data => {
        console.log('Réponse du serveur : ', data);
    })
    .catch(error => {
        console.error('Une erreur s\'est produite.')
    })
})