document.addEventListener("DOMContentLoaded", () => {
    const sessionId = getCookie();
    const foldersContainer = document.getElementById('folders-container');
    const deleteModal = document.getElementById('deleteModal');
    let folderToDelete = null;

    if (!sessionId) {
        alert("Session ID not found. Please log in again.");
        return;
    }

    // Function to get a cookie by its name
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

    // Load folders from the server
    async function loadFolders() {
        try {
            const response = await fetch(`http://itohan.tech/api/v1/getFolders/${sessionId}`);
            const folders = await response.json();

            if (response.ok && folders.length > 0) {
                folders.forEach(folder => {
                    const folderDiv = document.createElement('div');
                    folderDiv.classList.add('folder-item');
                    
                    const folderName = document.createElement('span');
                    folderName.innerText = folder.name;
                    folderDiv.appendChild(folderName);
                    
                    const openButton = document.createElement('button');
                    openButton.innerText = 'Open Folder';
                    openButton.addEventListener('click', () => {
                        window.location.href = `files?folderName=${folder.name}`;
                    });
                    folderDiv.appendChild(openButton);

                    const deleteButton = document.createElement('button');
                    deleteButton.innerText = 'Delete Folder';
                    deleteButton.classList.add('delete-button');
                    deleteButton.addEventListener('click', () => {
                        folderToDelete = folder.name;
                        showDeleteModal();
                    });
                    folderDiv.appendChild(deleteButton);

                    foldersContainer.appendChild(folderDiv);
                });
            } else {
                alert("No folders found.");
            }
        } catch (error) {
            console.error('Error loading folders:', error);
            alert("An error occurred while loading folders.");
        }
    }

    // Function to show the modal
    function showDeleteModal() {
        console.log("Delete Modal triggered for folder:", folderToDelete);
        deleteModal.style.display = 'block';
	deleteModal.classList.add('show');
    }

    // Function to hide the modal
    function hideDeleteModal() {
        deleteModal.style.display = 'none'; // Hide
    }

    // Function to confirm folder deletion
    async function confirmDeleteFolder() {
        console.log("Confirm delete triggered for folder:", folderToDelete);
        try {
            const response = await fetch(`http://itohan.tech/api/v1/deletefolder/${sessionId}`, {
                method: 'DELETE',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ folderName: folderToDelete }),
            });
            const result = await response.json();
            if (response.ok) {
		await showAlert(result.message);
		const folderItems = document.querySelectorAll('.folder-item span');
                folderItems.forEach(span => {
                  if (span.textContent.trim() === folderToDelete) {
                    span.parentElement.remove(); // Remove the folder element
                  }
                });
              location.reload();
            } else {
                alert(result.error || "Error deleting the folder.");
            }
        } catch (error) {
            console.error('Error deleting folder:', error);
            alert("An error occurred while deleting the folder.");
        }

        hideDeleteModal();
    }

    // Bind event listeners to confirm and cancel buttons
    const confirmDeleteButton = document.getElementById('confirmDelete');
    const cancelDeleteButton = document.getElementById('cancelDelete');

    if (confirmDeleteButton) {
        confirmDeleteButton.addEventListener('click', confirmDeleteFolder);
    } else {
        console.error('Confirm Delete button not found!');
    }

    if (cancelDeleteButton) {
        cancelDeleteButton.addEventListener('click', hideDeleteModal);
    } else {
        console.error('Cancel Delete button not found!');
    }

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
    // Load folders on page load
    loadFolders();
});
