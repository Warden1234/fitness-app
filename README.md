# Fitness-app
## Overview 
This project is a Kivy-based application that helps users track their fitness and diet plans. This project was designed especially for "Decentraton 2.0" Hackathon. It integrates Google Gemini AI for generating personalized training and eating plans, uses OpenCV and MediaPipe for gesture-based workout counting (push-ups and pull-ups).
## Features
* **Personalized Training Plan**: Generates a daily workout plan using Gemini AI.
* **Diet Plan Generator**: Creates a daily meal plan with calorie estimates.
* **Calorie Estimation**: Estimates calories based on food name or image.
* **Exercise Counter**: Uses OpenCV and MediaPipe to track exercises like push-ups and pull-ups.

## Installation
Ensure you have Python 3 installed. Install dependencies using:
`pip install -r requirements.txt `

## Usage
1. Run the application:
`python main.py`
2. Navigate through screens:
   1."Главная" (Home) screen displays workout and diet plans.
   2."Питание" (Diet) screen allows manual or photo-based calorie estimation.
   3. "Тренировка" (Training) screen provides real-time exercise tracking.
## Environment Variables
Set your Google Gemini API key:
`export API_KEY=your_api_key_here`

## License
This project is open-source under the MIT License.
