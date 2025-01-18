let currentQuestionIndex = 0;

function fetchQuestion() {
    fetch('/get_question')
        .then(response => response.json())
        .then(data => {
            if (data.quiz_complete) {
                showFinalScore(data.score);
            } else {
                displayQuestion(data);
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
            result.textContent = data.correct ? 'Correct!' : 'Incorrect!';
            setTimeout(fetchQuestion, 1000); // Automatically fetch the next question
        })
        .catch(error => showError(error.message));
}

function showFinalScore(score) {
    const container = document.querySelector('#quiz-container');
    container.innerHTML = `
        <h2>Quiz Complete!</h2>
        <p>Your final score is ${score}.</p>
    `;
}

function showError(message) {
    const errorContainer = document.querySelector('.error');
    errorContainer.textContent = message;
}

// Fetch the first question on load
fetchQuestion();
