
# importing packages need for system varibales, API Request, and GUI
import sys
import requests
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, # type: ignore
                            QLineEdit, QPushButton, QVBoxLayout)
from PyQt5. QtCore import Qt # type: ignore

class WeatherApp(QWidget):
    # Needed labels for the weather application
    def __init__(self):
        super().__init__()
        self.city_label = QLabel("Enter city name: ", self)
        self.city_input = QLineEdit(self)
        self.get_weather_button = QPushButton("Get Weather", self)
        self.temperature_label = QLabel(self)
        self.image_label = QLabel(self)
        self.description_label = QLabel(self)
        self.initUI()
    
    # Formating of the labels
    def initUI(self):
        self.setWindowTitle("Weather App")
        
        vbox = QVBoxLayout()
        
        # Creating Widgets for all the labels
        vbox.addWidget(self.city_label)
        vbox.addWidget(self.city_input)
        vbox.addWidget(self.get_weather_button)
        vbox.addWidget(self.temperature_label)
        vbox.addWidget(self.image_label)
        vbox.addWidget(self.description_label)
        
        self.setLayout(vbox)
        # Center alignment of the labels
        self.city_label.setAlignment(Qt.AlignCenter)
        self.city_input.setAlignment(Qt.AlignCenter)
        self.temperature_label.setAlignment(Qt.AlignCenter)
        self.image_label.setAlignment(Qt.AlignCenter)
        self.description_label.setAlignment(Qt.AlignCenter)
        
        # Creating an object name to the label, to manipulate the stlye
        self.city_label.setObjectName("city_label")
        self.city_input.setObjectName("city_input")
        self.get_weather_button.setObjectName("get_weather_button")
        self.temperature_label.setObjectName("temperature_label")
        self.image_label.setObjectName("image_label")
        self.description_label.setObjectName("description_label")
        
        # Manipulating the style of the labels
        self.setStyleSheet("""
            QLabel, QPushButton{
                font-family: calirbi;
            }
            QLabel#city_label{
                font-size: 40px;
                font-style: italic;
            }
            QLineEdit#city_input{
                font-size: 40px;
            }
            QPushButton#get_weather_button{
                font-size: 30px;
                font-weight: bold;
            }
            QLabel#temperature_label{
                font-size: 70px;
            }
            QLabel#image_label{
                font-size: 90px;
                font-family: Segoe UI emoji
            }
            QLabel#description_label{
                font-size: 50px;
            }
        """)
        
        self.get_weather_button.clicked.connect(self.get_weather) #Giving the weather button a functionality of connecting to the API
        
    # Connecting to the API
    def get_weather(self):
        
        api_key = "390ad3ad573680bdd74343f3e596c327" # Make sure to add your API key
        city = self.city_input.text()
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"
        
        # Capturing potential errors 
        try:
            response = requests.get(url) # Obtaining the data from the API request
            response.raise_for_status() # Rasing an error if the request status unsuccessful
            data = response.json() # Getting the requested information to a JSON format

            if data["cod"] == 200: # When cod is 200 this means the API connected successfully
                self.display_weather(data) # Displaying the succesful connection to the GUI
            
        except requests.exceptions.HTTPError as http_error: # Setting the error to show one of the following messages on the GUI if the status code is the same as the code written down
            match response.status_code:
                case 400:
                    self.display_error("Bad request:\nPlease check your input")
                case 401:
                    self.display_error("Unauthorized:\nInvalid API key")
                case 403:
                    self.display_error("Forbidden:\nAcces denied")
                case 404:
                    self.display_error("Not found:\nCity not found")
                case 500:
                    self.display_error("Internal Server Error:\nPlease try again later")
                case 502:
                    self.display_error("Bad Gateway:\nInvalid response from the server")
                case 503:
                    self.display_error("Service Unavailable:\nServer is down")
                case 404:
                    self.display_error("Gateway Timeout:\nNo response from the server")
                case _:
                    self.display_error(f"HTTP error occured:\n{http_error}")
                    
        except requests.exceptions.ConnectionError: # Setting the error to show the following message
            self.display_error("Connection Error:\nCheck your internet connection")
        
        except requests.exceptions.Timeout: # Setting the error to show the following message
            self.display_error("timeout Error:\nThe request timed out")
        
        except requests.exceptions.TooManyRedirects: # Setting the error to show the following message
            self.display_error("Too many redirects:\nCheck the URL")
                    
        except requests.exceptions.RequestException as req_error: # Setting the error to show the following message and the request error
            self.display_error(f"Request Error\n{req_error}")
        
    #Displaying error on the GUI
    def display_error(self, message):
        self.temperature_label.setStyleSheet("font-size: 30px;") # Changing the size of the error
        self.temperature_label.setText(message)# Text display of the message error
        self.image_label.clear()
        self.description_label.clear()
       
        
    #Displaying weather data on the GUI
    def display_weather(self, data):
        self.temperature_label.setStyleSheet("font-size: 75px;")
        temperature_k = data["main"]["temp"] # Obtaining the temp value from the main key
        temperature_f = (temperature_k * 9/5) -459.67 # Equation for chaning kelvin to fahrenheit
        
        weather_id = data["weather"][0]["id"]  # Obtaining the weather id the from the weather key
        weather_description = data["weather"][0]["description"] # Obtaining the description of weather the from the weather key 
        
        self.temperature_label.setText(f"{temperature_f:.0f}°F") # Displaying the temperature in fahrenheit on the GUI
        self.image_label.setText(self.get_weather_image(weather_id)) # Displaying the an image of the weather on the GUI
        self.description_label.setText(weather_description.capitalize()) # Displaying the weather description on the GUI
     
    #Displying an emoji relative to the weather ID
    @staticmethod
    def get_weather_image(weather_id):
        match weather_id:
            case _ if 200<= weather_id <= 232:
                return "⛈️"
            case _ if 300<= weather_id <= 321:
                return "🌦️"
            case _ if 500 <= weather_id <= 531:
                return "🌧️"
            case _ if 600 <= weather_id <= 622:
                return "❄️"
            case _ if 701 <= weather_id <= 741:
                return "🌫️"
            case 762:
                return "🌋"
            case 771:
                return "💨"
            case 781:
                return "🌪️"
            case 800:
                return "☀️"
            case _ if 801 <= weather_id <= 804:
                return "☁️"
            case _:
                return ""
        
        

# Running the weather app
if __name__ == "__main__":
    app = QApplication(sys.argv)
    weather_app = WeatherApp()
    weather_app.show()
    sys.exit(app.exec_())