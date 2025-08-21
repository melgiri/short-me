var xhr = new XMLHttpRequest();

function rec(data, path){
    xhr.open("POST", path, true);
    xhr.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
    xhr.send(data);

}