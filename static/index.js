let currentQuestionIndex = 0;

function fetchQuestion() {
    fetch('/get_question')
        .then(response => response.json())
        .then(data => {
            if (data.quiz_complete && typeof data.score !== 'undefined') {
                showFinalScore(data.score);
            } else if (data.question_text && data.options) {
                displayQuestion(data);
            } else {
                showError("Invalid data format received from the server.");
            }
        })
        .catch(error => showError(error.message));
}

function displayQuestion(data) {
    document.querySelector('.question').textContent = data.question_text;

    const optionsContainer = document.querySelector('.options');
    optionsContainer.innerHTML = '';

    data.options.forEach(option => {
        const button = document.createElement('button');
        button.textContent = option;
        button.onclick = () => submitAnswer(data.question_id, option);
        optionsContainer.appendChild(button);
    });
}

function submitAnswer(questionId, selectedAnswer) {
    fetch('/submit_answer', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ question_id: questionId, answer: selectedAnswer })
    })
        .then(response => response.json())
        .then(data => {
            const result = document.querySelector('.result');
            result.textContent = data.correct ? 'Correct!' : 'Wrong!';
            setTimeout(() => {
                result.textContent = '';
                fetchQuestion();
            }, 1000);
        })
        .catch(error => showError(error.message));
}
let timeLeft = 600;
const timerElement = document.getElementById('timer');

const timer = setInterval(() => {
    if (timeLeft >= 0) {
        const minutes = Math.floor(timeLeft / 60);
        const seconds = timeLeft % 60;
        timerElement.textContent = `${minutes < 10 ? '0' : ''}${minutes}:${seconds < 10 ? '0' : ''}${seconds}`;
        timeLeft -= 1;
    } else {
        clearInterval(timer);
        timerElement.textContent = "Time's Up!";

        fetch('/get_final_score')
            .then(response => response.json())
            .then(data => {
                showFinalScore(data.score); 
            })
            .catch(error => {
                showError(error.message);
                showFinalScore(0); 
            });
    }
}, 1000);

function showFinalScore(score) {
    const container = document.querySelector('#quiz-container');
    container.innerHTML = `
        <h2>Quiz Complete!</h2>
        <p>Your final score is ${score}.</p>
        <button onclick="goHome()">Back to Home</button>
    `;
}
function showError(message) {
    const errorContainer = document.querySelector('.error');
    errorContainer.textContent = message;

    setTimeout(() => {
        errorContainer.textContent = '';
    }, 3000);
}

function goHome() {
    window.location.href = '/';
}

fetchQuestion();
