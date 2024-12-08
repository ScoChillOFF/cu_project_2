from flask import Flask, render_template, request

from utils import save_cities_weathers
from weather_api import get_conditions
from utils import is_connected
from weather_check import get_weather_verdict

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def main_view():
    result = None
    error_message = None
    if request.method == 'POST':
        departure_city = request.form.get('departureCity')
        destination_city = request.form.get('destinationCity')
        if not departure_city or not destination_city:
            error_message = "Пожалуйста, введите названия обоих городов."
        else:
            if not is_connected():
                error_message = "Нет подключения к интернету."
            else:
                departure_data = get_conditions(departure_city)
                destination_data = get_conditions(destination_city)
                save_cities_weathers([departure_data, destination_data])
                if departure_data is None:
                    error_message = f"Не удалось получить данные для города: {departure_city}"
                elif destination_data is None:
                    error_message = f"Не удалось получить данные для города: {destination_city}"
                else:
                    result = {
                        "departure_city": {"name": departure_city,
                                           "verdict": get_weather_verdict(departure_data),
                                           **departure_data},
                        "destination_city": {"name": destination_city,
                                             "verdict": get_weather_verdict(destination_data),
                                             **destination_data}
                    }
    return render_template("index.html", result=result, error_message=error_message)


if __name__ == "__main__":
    app.run(debug=True)