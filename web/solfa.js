var table = Array.from(document.getElementsByClassName("top_right"))[0];
const logOut = document.getElementById('logo');

logOut.addEventListener('click', () => {
    eel.logOut()
    window.location.href = 'index.html';
})



window.addEventListener("load", async () => {

    
  
      
        eel.solfa()().then(x => {
        
            x.forEach(data => {
                var newRow = document.createElement("tr");

                var indexCell = document.createElement("td");
                indexCell.textContent = data["رقم الاداء"];
                newRow.appendChild(indexCell);

                var indexCell = document.createElement("td");
                indexCell.textContent = data['الاســـم _x'];
                newRow.appendChild(indexCell);

                var indexCell = document.createElement("td");
                indexCell.textContent =  data['الإبن'];
                newRow.appendChild(indexCell);

                var indexCell = document.createElement("td");
                indexCell.textContent = data['تاريخ الميلاد ']
                newRow.appendChild(indexCell);
                table.appendChild(newRow);


            });
        })


})
// Get a reference to the table element where you want to append rows (assuming it has the id "myTable")

// Iterate through the dataList and create table rows
