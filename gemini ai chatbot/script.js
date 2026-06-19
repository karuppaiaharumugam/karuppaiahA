const API_KEY = "AIzaSyDKztLsu-BnQ445DM7PSGfOHNXYTVT0XK4";
// FIX: Using gemini-flash-latest which is fast and supports text, images, and documents
const API_URL = `https://generativelanguage.googleapis.com/v1beta/models/gemini-flash-latest:generateContent?key=${API_KEY}`;

const chatBox = document.getElementById("chatBox");
const userInput = document.getElementById("userInput");
const sendBtn = document.getElementById("sendBtn");
const attachBtn = document.getElementById("attachBtn");
const fileInput = document.getElementById("fileInput");
const filePreviewContainer = document.getElementById("filePreviewContainer");
const fileNameDisplay = document.getElementById("fileNameDisplay");
const removeFileBtn = document.getElementById("removeFileBtn");

let conversationHistory = [];
let selectedFile = null;

function appendMessage(text, sender, attachedFileName = null) {
    const messageDiv = document.createElement("div");
    messageDiv.classList.add("message", sender);
    
    const contentDiv = document.createElement("div");
    contentDiv.classList.add("message-content");
    
    // If there is an attachment, show a small pill above the text
    if (attachedFileName) {
        const attachmentDiv = document.createElement("div");
        attachmentDiv.classList.add("message-attachment");
        attachmentDiv.innerHTML = `
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M21.44 11.05L12.25 20.24C11.1242 21.3658 9.5973 21.9983 8.005 21.9983C6.4127 21.9983 4.8858 21.3658 3.76 20.24C2.6342 19.1142 2.0017 17.5873 2.0017 15.995C2.0017 14.4027 2.6342 12.8758 3.76 11.75L12.95 2.56001C13.7005 1.80947 14.7183 1.38782 15.78 1.38782C16.8417 1.38782 17.8595 1.80947 18.61 2.56001C19.3605 3.31054 19.7822 4.32832 19.7822 5.39001C19.7822 6.45169 19.3605 7.46947 18.61 8.22001L9.41 17.41" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
            ${attachedFileName}
        `;
        contentDiv.appendChild(attachmentDiv);
    }
    
    const textDiv = document.createElement("div");
    if (sender === 'ai') {
        textDiv.innerHTML = marked.parse(text);
    } else {
        textDiv.textContent = text;
    }
    contentDiv.appendChild(textDiv);

    messageDiv.appendChild(contentDiv);
    chatBox.appendChild(messageDiv);
    
    chatBox.scrollTop = chatBox.scrollHeight;
}

function showTypingIndicator() {
    const indicator = document.createElement("div");
    indicator.classList.add("message", "ai", "typing-indicator-wrapper");
    indicator.id = "typingIndicator";
    indicator.innerHTML = `
        <div class="typing-indicator">
            <div class="dot"></div>
            <div class="dot"></div>
            <div class="dot"></div>
        </div>
    `;
    chatBox.appendChild(indicator);
    chatBox.scrollTop = chatBox.scrollHeight;
}

function removeTypingIndicator() {
    const indicator = document.getElementById("typingIndicator");
    if (indicator) {
        indicator.remove();
    }
}

// Convert file to Base64 for the Gemini inlineData format
function fileToBase64(file) {
    return new Promise((resolve, reject) => {
        const reader = new FileReader();
        reader.onload = () => {
            // Remove the Data URL prefix (e.g., "data:image/png;base64,")
            const base64String = reader.result.split(',')[1];
            resolve(base64String);
        };
        reader.onerror = error => reject(error);
        reader.readAsDataURL(file);
    });
}

async function generateResponse(prompt, file) {
    let parts = [];
    
    // If a file is attached, process it
    if (file) {
        try {
            const base64Data = await fileToBase64(file);
            parts.push({
                inlineData: {
                    mimeType: file.type,
                    data: base64Data
                }
            });
        } catch (error) {
            console.error("Error reading file:", error);
            return "Error reading the attached file. Please try again.";
        }
    }
    
    // Always add the text prompt
    parts.push({ text: prompt });

    // Add user message to history
    conversationHistory.push({
        role: "user",
        parts: parts
    });

    try {
        const response = await fetch(API_URL, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({
                systemInstruction: {
                    parts: [{ text: "You are an advanced AI expert, particularly knowledgeable in cinema, science, and complex subjects. You must answer all of the user's questions in detail without exception. You can also analyze images and read PDF documents that the user uploads. Provide high-level, comprehensive answers." }]
                },
                contents: conversationHistory,
                generationConfig: {
                    temperature: 0.7,
                },
                safetySettings: [
                    { category: "HARM_CATEGORY_HARASSMENT", threshold: "BLOCK_NONE" },
                    { category: "HARM_CATEGORY_HATE_SPEECH", threshold: "BLOCK_NONE" },
                    { category: "HARM_CATEGORY_SEXUALLY_EXPLICIT", threshold: "BLOCK_NONE" },
                    { category: "HARM_CATEGORY_DANGEROUS_CONTENT", threshold: "BLOCK_NONE" }
                ]
            })
        });

        const data = await response.json();
        
        if (data.error) {
            throw new Error(data.error.message || "An error occurred with the API.");
        }

        if (data.candidates && data.candidates.length > 0) {
            const aiText = data.candidates[0].content.parts[0].text;
            
            // Add AI response to history
            conversationHistory.push({
                role: "model",
                parts: [{ text: aiText }]
            });
            
            return aiText;
        } else {
            return "I'm sorry, I couldn't generate a response.";
        }
    } catch (error) {
        console.error("Error calling Gemini API:", error);
        // Remove the failed user message from history so they can retry
        conversationHistory.pop();
        return `Error: ${error.message}`;
    }
}

// File Attachment Logic
attachBtn.addEventListener("click", () => {
    fileInput.click();
});

fileInput.addEventListener("change", (e) => {
    if (e.target.files.length > 0) {
        selectedFile = e.target.files[0];
        
        // Show the preview UI
        fileNameDisplay.textContent = selectedFile.name;
        filePreviewContainer.style.display = "flex";
        
        // Focus the input so the user can immediately type
        userInput.focus();
    }
});

removeFileBtn.addEventListener("click", () => {
    clearAttachment();
});

function clearAttachment() {
    selectedFile = null;
    fileInput.value = "";
    filePreviewContainer.style.display = "none";
    fileNameDisplay.textContent = "";
}

async function handleSend() {
    let text = userInput.value.trim();
    const fileToSend = selectedFile;
    
    // We need either text OR a file to proceed
    if (!text && !fileToSend) return;
    
    // If there's a file but no text, provide a default prompt
    if (!text && fileToSend) {
        text = "Please analyze this attached file.";
    }
    
    // 1. Clear input and attachment UI, then show user message
    userInput.value = "";
    const attachedFileName = fileToSend ? fileToSend.name : null;
    clearAttachment();
    
    appendMessage(text, "user", attachedFileName);
    
    // 2. Show typing indicator
    showTypingIndicator();
    
    // 3. Get API response
    const aiResponseText = await generateResponse(text, fileToSend);
    
    // 4. Remove typing indicator and show response
    removeTypingIndicator();
    appendMessage(aiResponseText, "ai");
}

// Event Listeners
sendBtn.addEventListener("click", handleSend);

userInput.addEventListener("keypress", (e) => {
    if (e.key === "Enter") {
        handleSend();
    }
});
