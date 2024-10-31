document.addEventListener('DOMContentLoaded', function () {
    const folderContainer = document.getElementById('folder-container');
    const createFolderButton = document.getElementById('create-folder-button');
    const folderNameInput = document.getElementById('folder-name');
    const filesModal = document.getElementById('files-modal');
    const addFileButton = document.getElementById('add-file-button');
    const fileNameInput = document.getElementById('file-name');
    const fileContentInput = document.getElementById('file-content');
    const closeFilesModalButton = document.getElementById('close-modal-button');
    const hamburgerIcon = document.getElementById('hamburger-icon');
    const dropDownMenu = document.getElementById('dropdown-menu');
    const profilePicInput = document.getElementById('profile-pic-input');
    const userName = document.getElementById('user-name');
    const profilePic = document.getElementById('profile-pic');
    let currentFolder = null;

    function getSessionId() {
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

    const sessionId = getSessionId();
    async function getName() {
      try {
	const response = await fetch(`http://itohan.tech/api/v1/session/${sessionId}`)
        const data = await response.json()
	if (data.firstName) {
          userName.innerHTML = data.firstName;
	  return userName.innerHTML;
        } else {
	  await showAlert(data.error);
          return;
	}
      } catch (error) {
	userName.innerHTML = ''
	console.error("Could not get Name", error);
      }
    }

    function loadFolders() {
        folderContainer.innerHTML = '';
    }

    function createFolderElement(folderName) {
        const folderDiv = document.createElement('div');
        folderDiv.classList.add('folder');
        folderDiv.innerHTML = `
            <div class="folder-name">${folderName}</div>
            <div class="file-grid" id="file-grid-${folderName}"></div>
            <button class="add-file-btn" data-folder="${folderName}">Add File</button>
        `;
        folderContainer.appendChild(folderDiv);

        folderDiv.querySelector('.add-file-btn').addEventListener('click', function () {
            currentFolder = folderName;
            openFileModal(folderName);
        });
        loadFiles(folderName);
    }

    createFolderButton.addEventListener('click', async function () {
        const folderName = folderNameInput.value.trim();
        if (folderName === '') {
		await showAlert('Input a folder name');
		return;
	}

        try {
            const response = await fetch(`http://itohan.tech/api/v1/addfolder/${sessionId}`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ folderName })
            });
            const data = await response.json();
            if (data.folderName) {
                createFolderElement(data.folderName);
                folderNameInput.value = ''; // Clear input field
            } else {
		await showAlert(data.error);
                console.error('Error creating folder:', data.error);
            }
        } catch (error) {
            console.error('Error creating folder:', error);
        }
    });

    async function loadFiles(folderName) {
        try {
            const response = await fetch(`http://itohan.tech/api/v1/getFiles/${folderName}`);
            const files = await response.json();
            const fileGrid = document.getElementById(`file-grid-${folderName}`);
            fileGrid.innerHTML = '';
            files.forEach(file => {
                const fileDiv = document.createElement('div');
                fileDiv.classList.add('file');
                fileDiv.textContent = file.name;

		const copyButton = document.createElement('button');
                copyButton.textContent = 'Copy';
                copyButton.classList.add('copy-file-btn');
                copyButton.addEventListener('click', async () => {
                  await copyToClipboard(file.content); // Assume `file.content` contains the content of the file
                  showAlert(`Copied content of ${file.name}`); // Notify the user
                });

                fileDiv.appendChild(copyButton);
                fileGrid.appendChild(fileDiv);
            });
        } catch (error) {
            console.error('Error loading files:', error);
        }
    }

    function openFileModal(folderName) {
        document.getElementById('modal-title').textContent = `Add File to ${folderName}`;
        filesModal.style.display = 'block';
    }

    addFileButton.addEventListener('click', async function () {
        const fileName = fileNameInput.value.trim();
        const fileContent = fileContentInput.value.trim();

	if (fileName === '' || fileContent === '') return;
        try {
            const response = await fetch(`http://itohan.tech/api/v1/addfile/${sessionId}`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    folderName: currentFolder,
                    file: { name: fileName, content: fileContent }
                })
            });
            const data = await response.json();
            if (data.file) {
		if (data.exists) {
		  const message = `Generic line ${data.exists} spoted at ${data.generic}`;
	          updateMessageDisplay(message);
                }
		await showAlert(data.message);
                loadFiles(currentFolder);
                fileNameInput.value = '';
                fileContentInput.value = '';
                filesModal.style.display = 'none';
	    } else {
	      showAlert(data.error);
            }
        } catch (error) {
            console.error('Error adding file:', error);
        }
    });

    profilePic.addEventListener('click', function () {
      profilePicInput.click();
    });

    profilePicInput.addEventListener('change', async function (event) {
      const file = event.target.files[0];

      if (file) {
        const reader = new FileReader();

        reader.onload = async function (e) {
            const base64Image = e.target.result.split(',')[1];
            const payload = {
                profile_pic: base64Image
            };

            profilePic.style.backgroundImage = `url(${e.target.result})`;
	    console.log(payload);

            try {
                const response = await fetch(`http://itohan.tech/api/v1/uploadprofilepic/${sessionId}`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify(payload),
                });

                const result = await response.json();
		console.log('Upload result:', result);
                if (result.message) {
                    alert(result.message);
                }
            } catch (error) {
                console.error('Error uploading profile picture:', error);
            }
       };

       reader.readAsDataURL(file);
      }
    });

    hamburgerIcon.addEventListener('click', function () {
      if (dropDownMenu.style.display === 'block') {
	dropDownMenu.style.display = 'none';
      } else {
	dropDownMenu.style.display = 'block';
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
    function copyToClipboard(text) {
      if (!navigator.clipboard) {
        const textarea = document.createElement('textarea');
        textarea.value = text;
        document.body.appendChild(textarea);
        textarea.select();
        try {
          document.execCommand('copy');
          console.log('Text copied to clipboard using fallback');
        } catch (err) {
         console.error('Fallback failed:', err);
         showAlert('Copy failed');
       } finally {
         document.body.removeChild(textarea);
       }
      } else {
        navigator.clipboard.writeText(text)
          .then(() => console.log('Text copied to clipboard'))
          .catch(err => {
            console.error('Clipboard API failed:', err);
            showAlert('Copy failed');
          });
      }
    }

    function updateMessageDisplay(message) {
      const messageDisplay = document.getElementById('message-display');
      messageDisplay.textContent = message;
    }
    closeFilesModalButton.addEventListener('click', function () {
        filesModal.style.display = 'none'; // Hide the modal
    });
    getName();
    loadFolders();
});
