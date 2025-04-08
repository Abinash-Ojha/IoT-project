import dash
from dash import dcc, html
from dash.dependencies import Output, Input
import Adafruit_DHT

# --- Configuration ---
SENSOR = Adafruit_DHT.DHT22     # or Adafruit_DHT.DHT11
GPIO_PIN = 4                    # Change to the GPIO pin you connected to
THRESHOLD_TEMP = 30.0

# --- Dash App ---
app = dash.Dash(__name__)
app.title = "Sensor-Based Weather Monitor"

app.layout = html.Div([
    html.H1("🌡️ Live Sensor Weather Dashboard", style={"textAlign": "center"}),

    html.Div(id='temperature-output', style={"fontSize": "30px", "textAlign": "center", "marginTop": "20px"}),
    html.Div(id='humidity-output', style={"fontSize": "26px", "textAlign": "center", "color": "#0077b6"}),
    html.Div(id='alert-output', style={"fontSize": "24px", "textAlign": "center", "color": "red"}),

    dcc.Interval(id='interval-component', interval=60 * 1000, n_intervals=0)  # refresh every 60 seconds
])

# --- Sensor Reading Function ---
def read_sensor_data():
    humidity, temperature = Adafruit_DHT.read_retry(SENSOR, GPIO_PIN)
    if humidity is None or temperature is None:
        raise Exception("Sensor read failed")
    return round(temperature, 2), round(humidity, 2)

# --- Callback ---
@app.callback(
    [Output('temperature-output', 'children'),
     Output('humidity-output', 'children'),
     Output('alert-output', 'children')],
    [Input('interval-component', 'n_intervals')]
)
def update_weather(n):
    try:
        temp, humidity = read_sensor_data()
        temp_display = f"🌡️ Temperature: {temp}°C"
        humidity_display = f"💧 Humidity: {humidity}%"
        alert_msg = "🚨 ALERT: Temperature Exceeded!" if temp > THRESHOLD_TEMP else ""
        return temp_display, humidity_display, alert_msg
    except Exception as e:
        return f"Error: {str(e)}", "", ""

# --- Run App ---
if __name__ == '__main__':
    app.run(debug=True, port=8081)
