const chatMessages = document.getElementById('chat-messages');
const userInput = document.getElementById('user-input');
const sendButton = document.getElementById('send-button');
const dropArea = document.getElementById('drop-area');

sendButton.addEventListener('click', sendMessage);
    userInput.addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            sendMessage();
        }
    });

    dropArea.addEventListener('dragover', (e) => {
        e.preventDefault();
        dropArea.style.backgroundColor = '#e6f2ff';
    });

    dropArea.addEventListener('dragleave', () => {
        dropArea.style.backgroundColor = '';
    });

    dropArea.addEventListener('drop', (e) => {
        e.preventDefault();
        dropArea.style.backgroundColor = '';
        const files = e.dataTransfer.files;
        handleFileUpload(files[0]);
    });

    dropArea.addEventListener('click', () => {
        const fileInput = document.createElement('input');
        fileInput.type = 'file';
        fileInput.accept = '.pdf,.doc,.docx,.txt';
        fileInput.onchange = (e) => {
            handleFileUpload(e.target.files[0]);
        };
        fileInput.click();
    });

    function handleFileUpload(file) {
        // Here you would typically send the file to your server for processing
        // For this example, we'll just simulate a successful upload
        setTimeout(() => {
            dropArea.innerHTML = `
                <div class="document-info">
                    <div class="document-icon">
                        <img src="/static/img/pdf.jpg" alt="PDF Document Icon" width="100" height="100">
                    </div>
                </div>
            `;
            addMessage('ai', `Great! I've received the document "${file.name}". I'm analyzing it now. Feel free to ask me any questions about its content.`);
        }, 1500);
    }

    function sendMessage() {
        const message = userInput.value.trim();
        if (message) {
            addMessage('user', message);
            userInput.value = '';
            
            // Simulate AI response
            setTimeout(() => {
                const aiResponse = getAIResponse(message);
                addMessage('ai', aiResponse);
            }, 1000);
        }
    }

    function addMessage(sender, message) {
        const messageElement = document.createElement('div');
        messageElement.classList.add('message', sender + '-message');
        
        const avatarElement = document.createElement('div');
        avatarElement.classList.add('avatar');
        const avatarImg = document.createElement('img');
        avatarImg.src = sender === 'user' ? "/static/img/user.jpg" : "/static/img/okka.jpg";
        avatarImg.alt = sender === 'user' ? 'User Avatar' : 'AI Avatar';
        avatarImg.width = 40;
        avatarImg.height = 40;
        avatarElement.appendChild(avatarImg);
        
        const messageContentElement = document.createElement('div');
        messageContentElement.classList.add('message-content');
        messageContentElement.innerHTML = message;
        
        if (sender === 'user') {
            messageElement.appendChild(messageContentElement);
            messageElement.appendChild(avatarElement);
        } else {
            messageElement.appendChild(avatarElement);
            messageElement.appendChild(messageContentElement);
        }
        
        chatMessages.appendChild(messageElement);
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }

    function getAIResponse(message) {
        // Simulate AI response based on user input
        const responses = {
            'introduction': `The introduction typically covers the background of the research, the problem statement, and the objectives of the study. Without a specific document uploaded, I can't provide details about a particular introduction. If you have a document in mind, please upload it and I'll analyze its introduction for you.`,
            'methodology': `The methodology section usually describes the research design, data collection methods, and analysis techniques used in the study. To give you specific information about a methodology, I'd need to analyze an uploaded document. Feel free to upload one and I'll be happy to break down its methodology for you.`,
            'results': `Results sections present the findings of the study, often including statistical analyses and data visualizations. If you're looking for results from a particular document, please upload it and I can provide a detailed summary of its findings.`,
            'discussion': `The discussion typically interprets the results, compares them to existing literature, and explores their implications. For a specific discussion analysis, I'd need to review an uploaded document. Once you upload one, I can offer insights into its discussion section.`,
            'conclusion': `Conclusions usually summarize the key findings, address the research objectives, and suggest future research directions. To give you accurate information about a conclusion, I'd need to analyze a specific document. Please upload one and I'll summarize its conclusion for you.`,
            'machine learning': `Machine learning is a branch of artificial intelligence focused on building systems that learn from data. It's a vast field with many applications. If you're interested in how machine learning is applied in a specific document, please upload it and I can highlight its machine learning aspects.`,
            'neural networks': `Neural networks are a key component of deep learning, inspired by the human brain's structure. They're used in various AI applications. If you have a document that discusses neural networks, upload it and I can provide more specific information about how they're addressed.`,
            'data analysis': `Data analysis involves inspecting, cleaning, transforming, and modeling data to discover useful information and support decision-making. For insights on data analysis techniques used in a particular study, please upload the document and I'll analyze its data analysis methods for you.`
        };

        for (const [key, value] of Object.entries(responses)) {
            if (message.toLowerCase().includes(key)) {
                return value;
            }
        }

        return `Thank you for your question. To provide accurate information, I'd need to analyze a specific document. Please upload a document using the drop area in the sidebar, and then I'll be able to answer questions about its content in detail. Feel free to ask about any aspect of the document once it's uploaded, such as its methodology, results, or key concepts.`;
    }

    function focusSection(section) {
        const message = `Tell me about the ${section} section of the document.`;
        userInput.value = message;
        sendMessage();
    }
