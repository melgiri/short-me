const dataContainer = document.getElementById('data-container');
const addBtn = document.getElementById('add-btn');
const reloadBtn = document.getElementById('reload-btn');
const logoutBtn = document.getElementById('logout-btn');
const modal = document.getElementById('add-modal');
const saveBtn = document.getElementById('save-btn');
const cancelBtn = document.getElementById('cancel-btn');
const field1Input = document.getElementById('field1-input');
const field2Input = document.getElementById('field2-input');


function relo(){
    re("get")
    xhr.onreadystatechange = function() {
        if (xhr.readyState == 4) {
            if(xhr.status == 200 && xhr.responseText == "ok"){
                var data = xhr.getResponseHeader("res")
                data = data.split("||")
                data.pop()
                dataContainer.innerHTML = ''; // Clear existing content
                if (data.length === 0) {
                    dataContainer.innerHTML = '<p style="text-align: center; color: #999; padding: 2rem;">No data found. Click "Add" to create a new entry.</p>';
                    return;
                }
                
                data.forEach(item => {
                    item = item.replaceAll(" '", "").replaceAll("'", "").replace("(", "").replace(")", "").split(",")
                    const rowDiv = document.createElement('div');
                    rowDiv.className = 'row';

                    rowDiv.innerHTML = `
                        <input type="text" value="${item[2]}" class="input-field" readonly>
                        <input type="text" value="${item[3]}" class="input-field" readonly>
                        <div class="row-buttons">
                            <button class="btn btn-add edit-btn">Edit</button>
                            <button class="btn btn-logout delete-btn">Delete</button>
                        </div>
                    `;

                    // Add event listeners to the buttons in the newly created row
                    const editBtn = rowDiv.querySelector('.edit-btn');
                    const deleteBtn = rowDiv.querySelector('.delete-btn');
                    const inputFields = rowDiv.querySelectorAll('.input-field');

                    editBtn.addEventListener('click', () => {
                        const isEditing = editBtn.textContent === 'Save';
                        inputFields.forEach(input => {
                            input.readOnly = isEditing;
                            input.style.cursor = isEditing ? 'not-allowed' : 'auto';
                        });
                        editBtn.textContent = isEditing ? 'Edit' : 'Save';

                        // If saving, update the data array
                        if (isEditing) {
                            const updatedField1 = inputFields[0].value;
                            const updatedField2 = inputFields[1].value;
                            edit(item[0], updatedField1, updatedField2)
                        }
                    });

                    deleteBtn.addEventListener('click', () => {
                        if (confirm("Are you sure you want to delete this item?")) {
                            del(item[2])
                        }
                    });

                    dataContainer.appendChild(rowDiv);
                });
            }else {
                alert("Something went wrong while getting data")
            }
        }
    }
}

function re(ar, id_o='', id_n='', url_n='') {
    var id = field1Input.value;
    var url = field2Input.value;


    xhr.open("POST", "/api/manage", true);
    xhr.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
    if (ar == "add"){
        xhr.send("id=" + id + "&url=" + url + "&type=add");
    }
    else if(ar == "del"){
        xhr.send("id=" + id_o + "&type=del");
    }
    else if(ar == "edit"){
        xhr.send("id=" + id_o + "&id_n=" + id_n + "&url=" + url_n + "&type=edit");
    }
    else{
        xhr.send("type=get")
    }
}

function edit(id_o, id_n, url_n){
    re("edit", id_o, id_n, url_n)
    xhr.onreadystatechange = function() {
        if (xhr.readyState == 4) {
            if(xhr.status == 200 && xhr.responseText == "ok"){
                    alert("Link is edited")
                    relo()
                }else if(xhr.status == 401 && xhr.responseText == "no"){
                alert("you cant use this id")
            }
            else{
                alert("Something went wrong while editing or link exist")
            }
        }
    };
}

function add(){
    re("add")
    xhr.onreadystatechange = function() {
        if (xhr.readyState == 4) {
            if(xhr.status == 200 && xhr.responseText == "ok"){
                    alert("Link is shortned")
                    relo()
                }else if(xhr.status == 401 && xhr.responseText == "noa"){
                alert("you cant use this id")
                relo()
            }
            else{
                alert("Something went wrong while adding or link exist")
            }
        }
    };
}
        
function del(a){
    re("del", id_d=a)
    xhr.onreadystatechange = function() {
        if (xhr.readyState == 4) {
            if(xhr.status == 200 && xhr.responseText == "ok"){
                    alert("Deleted")
                    relo()
                }else {
                alert("Something went wrong while deleting")
            }
        }
    };
}

// Event listener for the "Add" button to show the modal
addBtn.addEventListener('click', () => {
    modal.style.display = 'flex';
    // Reset form fields
    field1Input.value = '';
    field2Input.value = '';
});

// Event listener for the "Cancel" button to hide the modal
cancelBtn.addEventListener('click', () => {
    modal.style.display = 'none';
});

// Event listener for the "Save" button to add a new item
saveBtn.addEventListener('click', () => {
    const newField1 = field1Input.value.trim();
    const newField2 = field2Input.value.trim();

    if (newField1 === '' || newField2 === '') {
        alert('All fields are required!');
        return;
    }

    add()

    modal.style.display = 'none';
});

// Event listener for the "Reload" button
reloadBtn.addEventListener('click', () => {
    relo()
});

// Event listener for the "Logout" button
logoutBtn.addEventListener('click', () => {
    alert('Successfully logged out.');
    window.location.href = "/logout";
});


relo()