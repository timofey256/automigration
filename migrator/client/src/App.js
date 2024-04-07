document.getElementById('uploadForm').addEventListener('submit', function(e) {
  e.preventDefault();

// eslint-disable-next-line no-restricted-globals
  if (confirm('Are you sure you have selected the right files?')) {
    const formData = new FormData(this);

    fetch('http://127.0.0.1:5000/upload', {
        method: 'POST',
        body: formData,
    })
    .then(response => response.json())
    .then(data => {
        console.log(data);
        window.location.href = 'http://127.0.0.1:5000/success'; // Change '/success' to the URL of the new page you want to show
    })
    .catch(error => {
        console.error('Error:', error);
    });
  } else {
    return;
  }
});


document.querySelector('input[type="file"]').addEventListener('change', updateFileList);

function updateFileList(e) {
  const fileListElement = document.getElementById('fileList');
  fileListElement.innerHTML = ''; // Clear the list
  fileListElement.classList.add('file-list'); // Add a class for styling
  const files = e.target.files;
  for (let i = 0; i < files.length; i++) {
      const fileElement = document.createElement('div');
      fileElement.classList.add('file-entry'); // Add a class for styling

      const fileNameSpan = document.createElement('span'); // Span for filename
      fileNameSpan.textContent = files[i].name;
      fileNameSpan.classList.add('file-name'); // Add a class for styling

      const removeButton = document.createElement('button');
      removeButton.textContent = 'Remove';
      removeButton.classList.add('remove-button'); // Add a class for styling
      removeButton.onclick = function() {
          removeFile(i, e.target);
      };

      fileElement.appendChild(fileNameSpan); // Append the span to the div
      fileElement.appendChild(removeButton);
      fileListElement.appendChild(fileElement);
  }
}


function removeFile(indexToRemove, fileInputElement) {
  const newFileList = Array.from(fileInputElement.files).filter((_, index) => index !== indexToRemove);
  const dataTransfer = new DataTransfer();
  newFileList.forEach(file => dataTransfer.items.add(file));
  fileInputElement.files = dataTransfer.files;
  
  updateFileList({ target: fileInputElement });
}

