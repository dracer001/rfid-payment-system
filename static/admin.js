let payment = document.getElementById("payment");
let database = document.getElementById("database");
let history;

function toggleData(el) {
    const xhttp = new XMLHttpRequest();
    if(el == database){
        payment.style.textDecoration="none";
        payment.style.color="#0d6dfd6c";
        database.style.textDecoration="underline";
        database.style.color="#0d6efd";
        history = "database";
    }else if(el == payment){
        payment.style.textDecoration="underline";
        payment.style.color="#0d6efd";
        database.style.textDecoration="none";
        database.style.color="#0d6dfd6c";
        history = "payment"
    }
    xhttp.onload = function(){
        document.getElementById("history").innerHTML = this.responseText;
    }
  
    xhttp.open("GET", "/get-database/"+history);
    xhttp.send();
}


function searchData(str){
    if (str.length == 0){
        toggleData(document.getElementById(history));
        return;
    }
    else{
        const xhttp = new XMLHttpRequest();
        xhttp.open("GET", "/search-database/"+history+"?q="+str);
        xhttp.send();
        
        xhttp.onload = function(){
            document.getElementById("history").innerHTML = this.responseText;
        }


    }

}
window.onload = toggleData(payment);