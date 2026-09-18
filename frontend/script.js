async function sendMessage() {

    const input = document.getElementById("message");
    const chat = document.getElementById("chat");
    const button = document.getElementById("sendButton");

    const message = input.value.trim();

    if (!message) {
        return;
    }

    chat.innerHTML += `
        <div class="message user">
            ${message}
        </div>
    `;

    input.value = "";

    button.disabled = true;

    chat.innerHTML += `
        <div class="message agent loading" id="loading">
            Agent is thinking...
        </div>
    `;

    chat.scrollTop = chat.scrollHeight;

    try {

        const response = await fetch(
            "http://127.0.0.1:8000/chat",
            {
                method: "POST",

                headers: {
                    "Content-Type": "application/json"
                },

                body: JSON.stringify({
                    message: message
                })
            }
        );

        const data = await response.json();

        document.getElementById("loading").remove();

        let answer = "Something went wrong.";

        if (data.response) {

            if (data.response.answer) {
                answer = data.response.answer;
            }

            else if (data.response.error) {
                answer = data.response.error;
            }
        }

        chat.innerHTML += `
            <div class="message agent">
                ${answer}
            </div>
        `;

    }

    catch (error) {

        document.getElementById("loading").remove();

        chat.innerHTML += `
            <div class="message agent">
                Could not connect to the backend.
            </div>
        `;
    }

    button.disabled = false;

    chat.scrollTop = chat.scrollHeight;
}


function handleKey(event) {

    if (event.key === "Enter") {
        sendMessage();
    }
}


async function newChat() {

    try {

        await fetch(
            "http://127.0.0.1:8000/clear-memory",
            {
                method: "POST"
            }
        );

    } catch (error) {

        console.error("Could not clear backend memory:", error);

    }


    document.getElementById("chat").innerHTML = `

        <div class="agent-message">

            <img
                src="agent-avatar.png"
                class="agent-avatar"
                alt="AI Agent"
            >

            <div class="message agent">

                <div class="message-name">
                    Agent
                </div>

                New conversation started.
                How can I help you?

            </div>

        </div>

    `;


    document.getElementById("message").focus();
}