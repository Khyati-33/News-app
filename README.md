# News App

This Flask app fetches today's latest news from Times of India (TOI) and displays it on the homepage.

## Prerequisites

- [Python](https://www.python.org/downloads/) installed on your system.

## Installation

1. Clone the repository to your local machine.

    ```bash
    git clone https://github.com/your-username/news-app.git
    ```

2. Navigate to the project directory.

    ```bash
    cd news-app
    ```

3. Create and activate a virtual environment.

    ```bash
    python -m venv venv
    source venv/Scripts/activate  # For Windows use venv\Scripts\activate
    ```

4. Install the required dependencies.

    ```bash
    pip install -r requirements.txt
    ```

## Usage

1. Run the Flask app.

    ```bash
    python news-app.py
    ```

2. Open your web browser and go to [http://127.0.0.1:5000/](http://127.0.0.1:5000/) to view the app.

3. To stop the app, press `Ctrl + C` in the terminal.

4. Deactivate the virtual environment.

    ```bash
    deactivate
    ```

## Customization

- You can modify the `get_toi_news()` function in `news-app.py` to customize the source of news or the way it is displayed.

## Contributing

Feel free to contribute by opening issues or creating pull requests.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
