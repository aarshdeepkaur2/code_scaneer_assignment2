
let currentState = 'start'; // Initial state
let completedPaths = []; // Track completed paths

const gameData = {
    start: {
        question: "Do you want to walk through the left or right path?",
        answers: [
            { text: "Left Path", nextState: "path1A" },
            { text: "Right Path", nextState: "path1B" },
        ],
    },
    path1A: {
        question: "You find a golden box. Do you want to open the box?",
        answers: [
            { text: "Open the box", nextState: "foundCoins" },
            { text: "Leave it", nextState: "lost" },
        ],
    },
    path1B: {
        question: "You found a Dark Cave. Do you want to go inside the cave?",
        answers: [
            { text: "Yes", nextState: "foundGold" },
            { text: "No", nextState: "exit" },
        ],
    },
    foundCoins: {
        question: "You found old coins! (End)",
        answers: [],
    },
    lost: {
        question: "You got lost!! (End)",
        answers: [],
    },
    foundGold: {
        question: "Yeah!! You found a bag full of gold. (End)",
        answers: [],
    },
    exit: {
        question: "You got the way to exit. (End)",
        answers: [],
    },
    path2: {
        question: "Do you want to enter the Darkforest?",
        answers: [
            { text: "Yes", nextState: "path2A" },
            { text: "No", nextState: "path2B" },
        ],
    },
    path2A: {
        question: "Do you want to spend time with the magical birds or shoot them?",
        answers: [
            { text: "Spend Time", nextState: "lifetimeHappiness" },
            { text: "Shoot them", nextState: "lost" },
        ],
    },
    path2B: {
        question: "Do you want to enter the bridge or cave?",
        answers: [
            { text: "Bridge", nextState: "hiddenPath" },
            { text: "Cave", nextState: "safelyReach" },
        ],
    },
    lifetimeHappiness: {
        question: "You got a lifetime Happiness wish! (End)",
        answers: [],
    },
    hiddenPath: {
        question: "You enjoy the view and find a hidden path. (End)",
        answers: [],
    },
    safelyReach: {
        question: "You reach the other side safely. (End)",
        answers: [],
    },
    path3: {
        question: "Do you go in Day or Night Cave?",
        answers: [
            { text: "Day", nextState: "path3A" },
            { text: "Night", nextState: "path3B" },
        ],
    },
    path3A: {
        question: "Do you want to move long or quit?",
        answers: [
            { text: "Move", nextState: "treasury" },
            { text: "Quit", nextState: "lost" },
        ],
    },
    path3B: {
        question: "Do you want to make people your friend?",
        answers: [
            { text: "Yes", nextState: "enjoyDay" },
            { text: "Ignore", nextState: "boredSad" },
        ],
    },
    treasury: {
        question: "You got some treasury. (End)",
        answers: [],
    },
    enjoyDay: {
        question: "You enjoy a beautiful day. (End)",
        answers: [],
    },
    boredSad: {
        question: "You got bored and sad after a period. (End)",
        answers: [],
    },
};

function addAnswerButton(text, nextState) {
    const button = document.createElement("button");
    button.textContent = text;
    button.addEventListener("click", () => {
        if (gameData[nextState]) {
            currentState = nextState;
            if (!completedPaths.includes(nextState)) {
                completedPaths.push(nextState);
            }
            renderQuestion();
        } else {
            console.error("Invalid nextState: " + nextState);
        }
    });
    return button;
}

function renderQuestion() {
    const questionContainer = document.getElementById("question");
    const answersContainer = document.getElementById("answers");
    const nextButton = document.getElementById("next-btn");
    const resetButton = document.getElementById("reset-btn");

    answersContainer.innerHTML = '';
    
    const currentData = gameData[currentState];
    questionContainer.textContent = currentData.question;

    currentData.answers.forEach(answer => {
        answersContainer.appendChild(addAnswerButton(answer.text, answer.nextState));
    });

    nextButton.style.display = currentData.answers.length === 0 && completedPaths.length > 0 ? "block" : "none";
    resetButton.style.display = currentData.answers.length === 0 ? "block" : "none";
}

function handleNext() {
    if (completedPaths.length === 1) {
        currentState = 'path2';
    } else if (completedPaths.length > 1) {
        currentState = 'path3';
        completedPaths.pop();
    } else {
        currentState = 'start';
    }
    renderQuestion();
}

function resetGame() {
    currentState = 'start';
    completedPaths = [];
    renderQuestion();
}

renderQuestion();
