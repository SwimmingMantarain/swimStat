let sectionCounter = 0;

function addSection() {
  console.log("sdfsdfsdfsdfsdf")
  sectionCounter++;
  const sectionId = `section-${sectionCounter}`;

  const sectionHTML = `
    <fieldset id="${sectionId}" class="border p-3 mb-4">
      <legend>Section ${sectionCounter}</legend>
      <input type="hidden" name="section-ids" value="${sectionId}">
      <input type="hidden" id="${sectionId}-block-count" name="section[${sectionCounter}][blockCount]" value="0">
      <div class="form-group">
          <label for="${sectionId}-name">Section Name:</label>
          <input type="text" class="form-control" id="${sectionId}-name" name="${sectionId}[name]">
      </div>
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
        <label for="${sectionId}-block-${blockCounter}-type">Distance (m):</label>
        <input type="number" class="form-control" id="${sectionId}-block-${blockCounter}-distance" name="${sectionId}[block-${blockCounter}][distance]">
      </div>
      
      <div class="form-group">
        <label for="${sectionId}-block-${blockCounter}-description">Repeat Count:</label>
        <input type="number" class="form-control" id="${sectionId}-block-${blockCounter}-repeat" name="${sectionId}[block-${blockCounter}][repeat]"></input>
      </div>
      
      <div class="form-group">
        <label for="${sectionId}-block-${blockCounter}-duration">Stroke(s):</label>
        <input type="text" class="form-control" id="${sectionId}-block-${blockCounter}-strokes" name="${sectionId}[block-${blockCounter}][strokes]"></input>
      </div>

      <div class="form-group">
        <label for="${sectionId}-block-${blockCounter}-duration">Exercise:</label>
        <textarea class="form-control" id="${sectionId}-block-${blockCounter}-exercise" name="${sectionId}[block-${blockCounter}][exercise]"></textarea>
      </div>
      
      <button type="button" class="btn btn-danger remove-btn" onclick="removeBlock(this)">Remove Block</button>
    </div>
  `;

  blocksContainer.insertAdjacentHTML('beforeend', blockHTML);
  updateBlockCount(sectionId);
}

function removeSection(sectionId) {
  document.getElementById(sectionId).remove();
  sectionCounter--;
}

function removeBlock(blockButton, sectionId) {
  blockButton.closest('.block').remove();
  updateBlockCount(sectionId);
}

function updateBlockCount(sectionId) {
  const sectionElement = document.getElementById(sectionId);
  const blocksContainer = sectionElement.querySelector('.blocks-container');
  const blockCountInput = sectionElement.querySelector(`#${sectionId}-block-count`);
  blockCountInput.value = blocksContainer.children.length;
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
  .then(response => response.json())
  .then(data => {
    window.location.replace(data.redirect);
  })
}

