document.addEventListener("DOMContentLoaded", () => {
    const urlParams = new URLSearchParams(window.location.search);
    const folderName = urlParams.get('folderName');
    const sessionId = getCookie();
    const fileList = document.getElementById('file-list');
    const editContainer = document.getElementById('edit-container');
    const editTextArea = document.getElementById('edit-text-area');
    const saveButton = document.getElementById('save-button');
    const addFileButton = document.getElementById('add-file-button');
    const createFileButton = document.getElementById('create-file-button');
    const deleteButton = document.getElementById('delete-button');
    const newFileContent = document.getElementById('new-file-content');
    const newFileNameInput = document.getElementById('new-file-name');
    const fileInput = document.getElementById('file-input');
    const hamburgerIcon = document.getElementById('hamburger-icon');
    const chatbox = document.getElementById('chatbox');
    const chatInput = document.getElementById("chat-input");
    const sendButton = document.getElementById("send-button");
    const chatContent = document.getElementById("chat-content");
    const confirmationModal = document.getElementById('confirmation-modal');
    const fileToDeleteSpan = document.getElementById('file-to-delete');
    let currentFileName = '';

    document.getElementById('folder-name').innerText = folderName;

    if (!sessionId) {
        alert("Session ID not found. Please log in again.");
        return;
    }

    function getCookie() {
        const name = 'session_id=';
        const decodedCookie = decodeURIComponent(document.cookie);
        const cookieArray = decodedCookie.split(';');
        for (let cookie of cookieArray) {
            while (cookie.charAt(0) === ' ') {
                cookie = cookie.substring(1);
            }
            if (cookie.indexOf(name) === 0) {
                return cookie.substring(name.length, cookie.length);
            }
        }
        return '';
    
    }

    async function loadFiles() {
        try {
            const response = await fetch(`http://itohan.tech/api/v1/getFiles/${folderName}`);
            const files = await response.json();
	    if (!Array.isArray(files)) {
    		console.log(`Unexpected response format: ${JSON.stringify(files)}`);
    		alert("Unexpected response format.");
    		return;
	    }
            if (response.ok && files.length > 0) {
                fileList.innerHTML = ''; // Clear the current file list
                files.forEach(file => {
                    const fileDiv = document.createElement('div');
                    fileDiv.classList.add('file-box');

                    const fileName = document.createElement('span');
                    fileName.innerText = file.name;

                    const openButton = document.createElement('button');
                    openButton.className = 'file-button';
                    openButton.innerText = 'Post';
                    openButton.onclick = () => openFile(file.content);

                    const editButton = document.createElement('button');
                    editButton.className = 'file-button';
                    editButton.innerText = 'Edit';
                    editButton.onclick = () => editFile(file.name, file.content); // Pass content for editing

                    fileDiv.appendChild(fileName);
                    fileDiv.appendChild(openButton);
                    fileDiv.appendChild(editButton);
                    fileList.appendChild(fileDiv);
                });
            } else {
                alert("No files found.");
            }
        } catch (error) {
            console.error('Error loading files:', error);
        }
    }

    window.fbAsyncInit = function() {
      FB.init({
        appId      : '792012552979740',
        cookie     : true,
        xfbml      : true,
        version    : 'v21.0'
      });
    };
    function openFile(fileContent) {
      const postContent = fileContent;

      if (!postContent) {
        alert("Please enter content for your post.")
        return;
      }

      FB.ui({
        method: 'share',
        href: 'http://itohan.tech/LibPredict',
        quote: postContent
      }, function(response) {
         if (response && !response.error_message) {
           alert('Post was shared successfully');
           location.reload();
         } else {
           console.error('Error while sharing:', response.error_message);
         }
      });
    }

    async function editFile(fileName, fileContent) {
        currentFileName = fileName;
        editContainer.style.display = 'block';
        editTextArea.value = fileContent; // Load the file content for editing
    }

    saveButton.addEventListener('click', async () => {
        const updatedContent = editTextArea.value;

        try {
            const response = await fetch(`http://itohan.tech/api/v1/updateFile/${sessionId}/${folderName}/${currentFileName}`, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    file: { name: currentFileName, content: updatedContent }
                })
            });
            const result = await response.json();
	    console.log(result)
            await showAlert(result.message);
            loadFiles(); // Refresh the file list
            editContainer.style.display = 'none'; // Hide the edit area after saving
        } catch (error) {
            console.error('Error updating file:');
            alert("An error occurred while updating the file.");
        }
    });

    createFileButton.addEventListener('click', async () => {
        const newContent = newFileContent.value;
        const newFileName = newFileNameInput.value;
        if (!newFileName || !newContent) {
            alert('Please enter both a file name and content.');
            return;
        }
        try {
            const response = await fetch(`http://itohan.tech/api/v1/addfile/${sessionId}`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ folderName, file: { name: newFileName, content: newContent } })
            });
            const result = await response.json();
	    if (result.file) {
	      if (result.exists) {
		await showAlert(`Generic line ${result.exists} spoted at ${result.generic}`)
	      }
              await showAlert(result.message);
	      location.reload()
              loadFiles();
	    } else {
              console.error('Error creating file', result.error);
	      await showAlert(result.error)
	    }
        } catch (error) {
            console.error('Error creating file', result.error);
        }
    });

    addFileButton.onclick = async () => {
        const file = fileInput.files[0];
        if (!file) {
            alert("Please select a file to upload.");
            return;
        }

        const newFileName = file.name;

        try {
            const newContent = await new Promise((resolve, reject) => {
                const reader = new FileReader();
                reader.onload = () => resolve(reader.result);
                reader.onerror = reject;
                reader.readAsDataURL(file);
            });

            const response = await fetch(`http://itohan.tech/api/v1/addfile/${sessionId}`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    folderName,
                    file: {
                        name: newFileName,
                        content: newContent
                    }
                })
            });

            const result = await response.json();
            await showAlert(result.message);
            loadFiles(); // Reload the file list after upload
        } catch (error) {
            console.error('Error uploading file:', error);
        }
    };
    hamburgerIcon.addEventListener('click', () => {
        chatbox.style.display = chatbox.style.display === 'block' ? 'none' : 'block';
    });

    async function getKey() {
      try {
        const response = await fetch('http://itohan.tech/api/v1/variable')
	result = await response.json()
	if (result.key) {
	  return result.key;
	} else {
          console.error("could not get key");
	  return;
        }
      } catch (error) {
	console.error("Could not get Key", error);
      }
    }

    async function sendMessageToAI(message) {
      console.log(getKey())
      try {
        const response = await fetch('https://api.openai.com/v1/chat/completions', {
          method: 'POST',
          headers: {
            'Authorization': `Bearer ${getKey()}`, // API Key for OpenAI authorization
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            model: "gpt-3.5-turbo",
            messages: [{ role: "user", content: message }]
          })
        });

        if (!response.ok) {
          console.error(`Error: ${response.status} ${response.statusText}`);
          return "An error occurred while communicating with AI.";
        }

        const data = await response.json();
        if (data && data.choices && data.choices[0].message) {
          return data.choices[0].message.content; // AI's response content
        } else {
          console.error("Unexpected response format:", data);
          return "An unexpected response format was received from the AI.";
        }
      } catch (error) {
        console.error("Error communicating with AI:", error);
        return "An error occurred while trying to communicate with AI.";
      }
    }

    async function sendMessage() {
        const message = chatInput.value.trim(); // Get the message from the input
        if (message) {
            const messageElement = document.createElement("p");
            messageElement.textContent = message;
            chatContent.appendChild(messageElement);
            chatInput.value = ""; // Clear input after sending

            const aiResponse = await sendMessageToAI(message); // Call the AI function
            const aiMessageElement = document.createElement("p");
            aiMessageElement.textContent = `AI: ${aiResponse}`;
            chatContent.appendChild(aiMessageElement);
        }
    }
    sendButton.addEventListener("click", sendMessage);

    // Send message on Enter key press
    chatInput.addEventListener("keypress", function(event) {
        if (event.key === "Enter") {
            sendMessage();
        }
    });

    let alertInProgress = false;
    async function showAlert(message) {
      try {
        const alertContainer = document.getElementById('alert-container');
        const alertMessage = document.getElementById('alert-message');

        if (!alertContainer || !alertMessage) {
            console.error("Alert elements are missing from the DOM.");
            return;
        }

        if (alertInProgress) {
            console.log("Waiting for current alert to finish");
            return; // Exit if another alert is already in progress
        }

        alertInProgress = true;
        alertMessage.textContent = message;
        alertContainer.style.display = 'block';

        setTimeout(() => {
            alertContainer.style.display = 'none';
            alertInProgress = false;
        }, 3000); // Time for the alert to stay visible
      } catch (error) {
        console.error("Couldn't display alert:", error);
        alertInProgress = false; // Reset on error
      }
    }
    deleteButton.addEventListener('click', () => {
      fileToDeleteSpan.innerText = currentFileName; // Set the file name in the modal
      confirmationModal.style.display = 'block'; // Show the modal
    });
    document.getElementById('close-modal').onclick = () => {
      confirmationModal.style.display = 'none';
    };

    document.getElementById('cancel-delete').onclick = () => {
    confirmationModal.style.display = 'none';
};

    document.getElementById('confirm-delete').onclick = async () => {
      confirmationModal.style.display = 'none'; // Close the modal
      if (!currentFileName) return;

      try {
        const response = await fetch(`http://itohan.tech/api/v1/deletefile/${folderName}/${sessionId}`, {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ file: { name: currentFileName, content: editTextArea.value } })
        });
        
        if (!response.ok) {
            throw new Error(`Failed to delete file: ${response.status} ${response.statusText}`);
        }

        const result = await response.json();
        if (result.message) {
            await showAlert(result.message);
        } else {
            alert(result.error);
        }
        
        loadFiles(); // Reload the files after deletion
        location.reload();
      } catch (error) {
        console.error('Error deleting file:', error);
      }
    };
    loadFiles();
});
