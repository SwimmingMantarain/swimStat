let sectionCounter = 0;

function addSection() {
  sectionCounter++;
  const sectionId = `section-${sectionCounter}`;
  
  const sectionHTML = `
    <fieldset id="${sectionId}" class="border p-3 mb-4">
      <legend>Section ${sectionCounter}</legend>
      <div class="blocks-container">
        <!-- Blocks will be added here dynamically -->
      </div>
      <button type="button" class="btn btn-secondary mt-2" onclick="addBlock('${sectionId}')">Add Block</button>
      <button type="button" class="btn btn-danger mt-2" onclick="removeSection('${sectionId}')">Remove Section</button>
    </fieldset>
  `;
  
  document.getElementById('sections-container').insertAdjacentHTML('beforeend', sectionHTML);
}

function addBlock(sectionId) {
  const sectionElement = document.getElementById(sectionId);
  const blocksContainer = sectionElement.querySelector('.blocks-container');
  
  const blockCounter = blocksContainer.children.length + 1;
  const blockHTML = `
    <div class="block">
      <div class="form-group">
        <label for="${sectionId}-block-${blockCounter}-type">Block Type:</label>
        <input type="text" class="form-control" id="${sectionId}-block-${blockCounter}-type" name="${sectionId}[block-${blockCounter}][type]">
      </div>
      
      <div class="form-group">
        <label for="${sectionId}-block-${blockCounter}-description">Description:</label>
        <textarea class="form-control" id="${sectionId}-block-${blockCounter}-description" name="${sectionId}[block-${blockCounter}][description]"></textarea>
      </div>
      
      <div class="form-group">
        <label for="${sectionId}-block-${blockCounter}-duration">Duration (minutes):</label>
        <input type="number" class="form-control" id="${sectionId}-block-${blockCounter}-duration" name="${sectionId}[block-${blockCounter}][duration]">
      </div>
      
      <button type="button" class="btn btn-danger remove-btn" onclick="removeBlock(this)">Remove Block</button>
    </div>
  `;
  
  blocksContainer.insertAdjacentHTML('beforeend', blockHTML);
}

function removeSection(sectionId) {
  document.getElementById(sectionId).remove();
}

function removeBlock(blockButton) {
  blockButton.closest('.block').remove();
}

function submitForm() {
  const formElement = document.getElementById('swimming-session-form');
  const formData = new FormData(formElement);
  const formObject = {};

  formData.forEach((value, key) => {
    if (formObject[key]) {
      if (!Array.isArray(formObject[key])) {
        formObject[key] = [formObject[key]];
      }
      formObject[key].push(value);
    } else {
      formObject[key] = value;
    }
  });

  fetch('/add-session', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(formObject)
  })
}
