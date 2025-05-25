document.getElementById('main_page').style.display = 'block'

document.getElementById('add_page').style.display = 'none'

document.getElementById('del_page').style.display = 'none'

function close_add(){
    document.getElementById('add_page').style.display = 'none';
    document.getElementById('main_page').style.display = 'block';
}

function open_add(){
    document.getElementById('add_page').style.display = 'block';
    document.getElementById('main_page').style.display = 'none';
}

function close_del(){
    document.getElementById('del_page').style.display = 'none';
    document.getElementById('main_page').style.display = 'block';
}

function reloa(){
    var elements = document.getElementsByClassName("input-section");
    while(elements.length > 0){
        elements[0].parentNode.removeChild(elements[0]);
    }
    relo()
}

function relo(){
    re("get")
    xhr.onreadystatechange = function() {
        if (xhr.readyState == 4) {
            if(xhr.status == 200 && xhr.responseText == "ok"){
                var responseHeaders = xhr.getResponseHeader("res").split("||");

                for(let i = 0; i<responseHeaders.length-1; i++)
                {
                    var div = document.createElement("div");
                    div.className = "input-section";
                    document.getElementById('main_page_div').appendChild(div);

                    var p = document.createElement("input");
                    p.type = "text";
                    p.value = responseHeaders[i].replaceAll(" '", "").replaceAll("'", "").replace("(", "").replace(")", "").split(",")[1];
                    p.readOnly = true;
                    div.appendChild(p);

                    var p1 = document.createElement("input");
                    p1.type = "text";
                    p1.value = responseHeaders[i].replaceAll(" '", "").replaceAll("'", "").replace("(", "").replace(")", "").split(",")[2];
                    p1.readOnly = true;
                    div.appendChild(p1);

                    var p2 = document.createElement("button");
                    p2.textContent = "Delete";
                    p2.onclick = function(){
                        delit(responseHeaders[i].replaceAll(" '", "").replaceAll("'", "").replace("(", "").replace(")", "").split(",")[1]);
                    }
                    div.appendChild(p2);
                }
                
            }else {
                al("Something went wrong while getting data")
            }
        }
    }
}


function lo(){
    window.location.href = "/logout";
}

function re(ar) {
    var id = document.getElementById('id').value;
    var ida = document.getElementById('ida').value;
    var url = document.getElementById('url').value;


    xhr.open("POST", "/api/manage", true);
    xhr.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
    if (ar == "add"){
        xhr.send("id=" + id + "&url=" + url + "&type=add");
    }
    else if(ar == "del"){
        xhr.send("id=" + ida + "&type=del");
    }
    else{
        xhr.send("type=get")
    }
}

function add(){
    re("add")
    xhr.onreadystatechange = function() {
        if (xhr.readyState == 4) {
            if(xhr.status == 200 && xhr.responseText == "ok"){
                    al("Link is shortned")
                    reloa()
                }else if(xhr.status == 401 && xhr.responseText == "noa"){
                al("you cant use this id")
            }
            else{
                al("Something went wrong while adding or link exist")
            }
        }
    };
}
        
function del(){
    re("del")
    xhr.onreadystatechange = function() {
        if (xhr.readyState == 4) {
            if(xhr.status == 200 && xhr.responseText == "ok"){
                    al("Deleted")
                    reloa()
                }else {
                al("Something went wrong while deleting")
            }
        }
    };
}

function delit(arg_id){
    document.getElementById('del_page').style.display = 'block';
    document.getElementById('main_page').style.display = 'none';
    document.getElementById('ida').value = arg_id;
}

function al(msg) {
    document.getElementById('alert').innerHTML = msg;
}

relo()