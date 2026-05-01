# WeatherML Web Application

This project is a web application that utilizes a machine learning model to predict weather-related outcomes based on user input. The application is built using Flask and serves as an interface for users to interact with the model.

## Project Structure

```
weatherml-web
├── app.py                # Main application file
├── templates             # HTML templates for rendering pages
│   ├── index.html       # Homepage with input form
│   └── result.html      # Page to display prediction results
├── static               # Static files (CSS, JS)
│   ├── css
│   │   └── styles.css    # Styles for the web application
│   └── js
│       └── app.js        # JavaScript for client-side functionality
├── model                # Directory containing the trained model
│   └── best_model.pkl    # Serialized machine learning model
├── requirements.txt      # Python dependencies
└── README.md             # Project documentation
```

## Setup Instructions

1. **Clone the repository:**
   ```
   git clone <repository-url>
   cd weatherml-web
   ```

2. **Create a virtual environment:**
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install the required packages:**
   ```
   pip install -r requirements.txt
   ```

4. **Run the application:**
   ```
   python app.py
   ```

5. **Access the application:**
   Open your web browser and go to `http://127.0.0.1:5000`.

## Usage

- On the homepage, enter the required data in the form and submit it to receive predictions from the machine learning model.
- The results will be displayed on a separate results page.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.