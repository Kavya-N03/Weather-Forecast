window.onload = function () {
    const changebg = document.getElementById("weather-condition");

    if (changebg) {
        const condition = changebg.innerHTML.trim();
        const body = document.body;

        switch (condition) {
            case "Clear":
                body.style.backgroundImage = "url('/static/img/sunny_clear.jpg')";
                break;
            case "Clouds":
                body.style.backgroundImage = "url('/static/img/cloudy.jpg')";
                break;
            case "Rain":
                body.style.backgroundImage = "url('/static/img/rainy.jpg')";
                break;
            case "Snow":
                body.style.backgroundImage = "url('/static/img/snowy.jpg')";
                break;
            case "Thunderstorm":
                body.style.backgroundImage = "url('/static/img/thunder.jpg')";
                break;
            case "Mist":
            case "Haze":
            case "Fog":
                body.style.backgroundImage = "url('/static/img/foggy.jpg')";
                break;
            default:
                body.style.backgroundImage = "url('/static/img/default.jpg')";
        }
    }
};
