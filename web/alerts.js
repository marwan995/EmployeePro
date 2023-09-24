var tables = Array.from(document.getElementsByClassName("top_right"));
const logOut = document.getElementById('logo');

logOut.addEventListener('click', () => {
    eel.logOut()
    window.location.href = 'index.html';
})


window.addEventListener("load", async () => {

    let alerts = [
        ['المؤهل الدراسي للعاملين', 'تاريخ الانتهاء'],
         ['بطاقات شخصية', 'تاريخ الانتهاء']
        , ['المؤهل الدراسي للعاملين', 'قياس مستوي المهارة']
        , ['اقرار ذمة مالية', 'تاريخ التعيين']
    ]
      
    let table_index = 0;
    tables.forEach(table => {
        
        let sheet_name = alerts[table_index][0]
        let column_name =alerts[table_index][1]
        
        eel.all_alerts(sheet_name,column_name)().then(x => {
           
            x.forEach(data => {
                var newRow = document.createElement("tr");

                var indexCell = document.createElement("td");
                indexCell.textContent = data["رقم الاداء"];
                newRow.appendChild(indexCell);
                table.appendChild(newRow);

                var indexCell = document.createElement("td");
                indexCell.textContent = data["الاســـم "];
                newRow.appendChild(indexCell);
                table.appendChild(newRow);

                var indexCell = document.createElement("td");
                indexCell.textContent =  data[column_name];
                newRow.appendChild(indexCell);
                table.appendChild(newRow);

                var indexCell = document.createElement("td");
                indexCell.textContent = data['مدة التأخير'] == -1 ? "pending" : data['مدة التأخير']
                newRow.appendChild(indexCell);
                table.appendChild(newRow);


            });
        })
        if(table_index == alerts.length-1)
             return
        table_index++
    })

})

