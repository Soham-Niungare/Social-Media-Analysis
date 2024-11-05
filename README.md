# Social Media Analysis Dashboard

## Overview

This web application is designed to provide real-time insights into social media sentiment and trends. It leverages the power of React for a dynamic frontend and Flask for backend operations. By utilizing the Apify API, the application fetches tweets based on specific search queries, which are then analyzed using a pre-trained sentiment analysis model. The results are visualized in a clear and concise pie chart, highlighting the percentage distribution of positive, negative, and neutral sentiment.

## Key Features

- **Real-time Data Fetching**: Continuously updates data from Twitter using the Apify API.
- **Sentiment Analysis**: Analyzes tweets to determine their sentiment polarity (positive, negative, neutral).
- **Trend Identification**: (Under Development) Identifies emerging trends and topics within the fetched tweets.
- **Interactive Visualization**: Presents analysis results in an easy-to-understand pie chart.

## Technology Stack

### Frontend:

- **React**: A JavaScript library for building user interfaces.
- **Shadcn**: A UI component library for rapid web development.

### Backend:

- **Flask**: A lightweight Python web framework.
- **Apify API**: For fetching real-time data from Twitter.
- **Pre-trained Sentiment Analysis Model**: For classifying tweet sentiment.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/Soham-Niungare/Social-Media-Analysis.git
   
2. Navigate to the project directory:

   ```bash
   cd Social-Media-Analysis

   ```

### Project Setup

The project is organized into two main folders:

- **`server`**: Contains the backend code, built with Python.
- **`client`**: Contains the frontend code, built with JavaScript (Node.js).

Each part of the application needs to be run in a separate terminal.

### Server Setup

1. **Navigate to the `server` folder**:
   ```bash
   cd server
   ```
2. Create a virtual environment:
   ```bash
   python -m venv virtualEnv
   ```
3. Activate the virtual environment:
   ```bash
   virtualEnv\Scripts\activate
   ```
4. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```
5. Run the server:
   ```bash
   python main.py
   The server should now be running on a specific port. Check the terminal output for the exact port.
   ```

### Client Setup

1. **Navigate to the `client` folder**:
   ```bash
   cd client
   ```
2. Install Node.js modules:
   ```bash
   npm install
   ```
3. Run the client:
   ```bash
   npm run dev
   After running this command, the frontend will be accessible at a specific port. The exact port should be displayed in the terminal.
   ```

## Future Enhancements

Trend Identification: Implement advanced techniques like topic modeling or keyword extraction to identify emerging trends.
Sentiment Analysis Refinement: Explore more sophisticated sentiment analysis models to improve accuracy.
User Interface Customization: Enhance the user interface with additional features like filtering, sorting, and exporting data.
Real-time Updates: Implement a mechanism to update the dashboard in real-time as new tweets are fetched.
Security: Implement robust security measures to protect user data and prevent unauthorized access.

By continuously refining and expanding these features, we aim to create a powerful tool for social media analysis that provides valuable insights to businesses, organizations, and individuals.
