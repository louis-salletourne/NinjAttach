document.getElementById('receiveButton').addEventListener('click', () => {
    const tableBody = document.querySelector('#infoTable tbody');
  
    // Add a new row with default data
    const newRow = document.createElement('tr');
  
    // Create editable cells with default information
    const defaultData = ["Name", "Felix"];
    defaultData.forEach(data => {
        const newCell = document.createElement('td');
        newCell.contentEditable = "true";
        newCell.textContent = data;
        newRow.appendChild(newCell);
    });
  
    tableBody.appendChild(newRow);
  });
  
  document.getElementById('submitButton').addEventListener('click', () => {
    const tableBody = document.querySelector('#infoTable tbody');
  
    // Clear the table for next use
    tableBody.innerHTML = '';
  });