const ROUTER_URL = "https://cca5-cin-ufpe-br.azurewebsites.net/api/HttpRouter"

function initialize() {
    // Get path and redirect to router:
    let originUrl = window.location.search;

    if (originUrl.startsWith("?")) {
        originUrl = originUrl.substring(1);
    }

    let form = document.createElement("form"); 
    form.method = "post";
    form.action = ROUTER_URL;
    document.body.appendChild(form);

    let input = document.createElement('hidden');
    input.name = "originUrl";
    input.value = originUrl;
    form.appendChild(input);

    form.submit();
}