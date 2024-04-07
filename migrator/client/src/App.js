document.addEventListener('DOMContentLoaded', function() {
  setupFormSubmission();
  setupFileInputChange();
});

function setupFormSubmission() {
  const uploadForm = document.getElementById('uploadForm');
  uploadForm.addEventListener('submit', handleFormSubmit);
}

function handleFormSubmit(e) {
  e.preventDefault();

  if (!window.confirm('Are you sure you have selected the right files?')) {
      return;
  }

  const formData = new FormData(e.target);

  fetch('http://127.0.0.1:5000/upload', {
      method: 'POST',
      body: formData,
  })
  .then(response => response.json())
  .then(handleSuccess)
  .catch(handleError);
}

function handleSuccess(data) {
  console.log(data);
  window.location.href = 'http://127.0.0.1:5000/success';
}

function handleError(error) {
  console.error('Error:', error);
}

function setupFileInputChange() {
  const fileInput = document.querySelector('input[type="file"]');
  fileInput.addEventListener('change', updateFileList);
}

function updateFileList(e) {
  const fileListElement = document.getElementById('fileList');
  clearFileList(fileListElement);
  const files = Array.from(e.target.files); // Convert FileList to an array
  files.forEach((file, index) => {
      fileListElement.appendChild(createFileElement(file, index, e.target));
  });
}

function clearFileList(element) {
  element.innerHTML = ''; // Clear the list
  element.classList.add('file-list');
}

function createFileElement(file, index, fileInputElement) {
  const fileElement = document.createElement('div');
  fileElement.classList.add('file-entry');

  const fileNameSpan = createFileNameSpan(file.name);
  const removeButton = createRemoveButton(index, fileInputElement);

  fileElement.appendChild(fileNameSpan);
  fileElement.appendChild(removeButton);

  return fileElement;
}

function createFileNameSpan(fileName) {
  const fileNameSpan = document.createElement('span');
  fileNameSpan.textContent = fileName;
  fileNameSpan.classList.add('file-name');
  return fileNameSpan;
}

function createRemoveButton(index, fileInputElement) {
  const button = document.createElement('button');
  button.textContent = 'Remove';
  button.classList.add('remove-button');
  button.addEventListener('click', () => removeFile(index, fileInputElement));
  return button;
}

function removeFile(indexToRemove, fileInputElement) {
  const newFileList = Array.from(fileInputElement.files).filter((_, index) => index !== indexToRemove);
  fileInputElement.files = createFileList(newFileList);
  updateFileList({ target: fileInputElement });
}

function createFileList(files) {
  const dataTransfer = new DataTransfer();
  files.forEach(file => dataTransfer.items.add(file));
  return dataTransfer.files;
}
