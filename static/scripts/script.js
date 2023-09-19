document.addEventListener('DOMContentLoaded', function() {
    let request = new XMLHttpRequest();

    request.open('GET', '/api/data', true);

    request.onload = function() {
        if (request.status >= 200 && request.status < 400) {
            let data = JSON.parse(request.responseText);
            console.log(data);
        } else {
            console.error('Error fetching data');
        }
    };

    request.onerror = function() {
        console.error('Error fetching data');
    };

    request.send();
});

