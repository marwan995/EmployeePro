
const overlay = document.getElementById('overlay');
const popup = document.getElementsByClassName('popup')[0];
const btns_pop_up = Array.from(document.getElementsByClassName('buttons_pop_up')[0].getElementsByTagName('button'));
const data_table = document.querySelector('#data-table')
const days_table = document.getElementById('data-body')
const start_mon = document.getElementById("start_date");
const end_mon = document.getElementById("end_date");
const dataDiv = document.getElementById('data');
const pdfEmbed = document.getElementById('pdfEmbed');
const pdfViewer = document.getElementById('pdfViewer');
const pdfs = Array.from(document.getElementsByClassName('pdfs')[0].getElementsByTagName('button'))
const pp = document.getElementById('pp');
const monthMapping = [
    "يناير",
    "فبراير",
    "مارس",
    "أبريل",
    "مايو",
    "يونيو",
    "يوليو",
    "أغسطس",
    "سبتمبر",
    "أكتوبر",
    "نوفمبر",
    "ديسمبر"
]
const convert_to_orignal = { 'غياب': 'غ', 'إجازة اعتيادي': 'س/و', 'سفر': 'سفر', 'إجازة سنوي': 'س', 'حج': 'حج', 'إجازة عارضة': 'ع', 'اصابة عمل': 'ص', 'إجازة وضع': 'و', 'إجازة مرضي': 'م', 'عمل بالراحات': 'ع ب', 'بدل راحة': 'ب ر', 'استثنائية': 'ث', 'عمل بالعطلة': 'ع ع' }
let flag = "0";
function openPopup() {
    overlay.style.display = 'block';
    popup.style.opacity = .9;
    pdfViewer.style.display = 'none';
    popup.style.display = 'block';
    data.style.display = 'block';

}
function getMaxArrayLength(arrayOfArrays) {
    return arrayOfArrays.reduce((max, subArray) => Math.max(max, subArray.length), 0);
}
function createRows(length) {
    for (let i = 0; i < length; i++) {
        const tr = document.createElement("tr");
        days_table.append(tr);
    }
}

function getIndexesOfNonEmptyArrays(arr) {
    let firstNonEmptyIndex = -1;
    let lastNonEmptyIndex = -1;

    for (let i = 0; i < arr.length; i++) {
        if (arr[i].length > 0) {
            if (firstNonEmptyIndex === -1) {
                firstNonEmptyIndex = i;
            }
            lastNonEmptyIndex = i;
        }
    }

    return [firstNonEmptyIndex, lastNonEmptyIndex];
}
function table_headers() {
    let thead = document.getElementsByTagName('thead')[0].getElementsByTagName('tr')[0]
    let mon = monthMapping.slice(parseInt(start_mon.value.split("-")[1]) - 1, parseInt(end_mon.value.split("-")[1]))
    thead.innerHTML = ""
    mon.forEach(e => {
        let th = document.createElement('th')
        th.textContent = e
        thead.append(th)
    })
}
function getSubarraySizes(arr) {
    return arr.map(subarray => subarray.length);
}
async function showTable(name) {
    let data = []
    let data_obj = {}
    if (name == "التأخيرات") {
        data_obj = await eel.get_lateness()();
        data = data_obj['days'];
    }
    else {
        data_obj = await eel.make_hours_data()();

        data = data_obj[convert_to_orignal[name]]
    }
    days_table.innerHTML = "";
    clearLastChild(popup);
    createRows(getMaxArrayLength(data));
    const rows = days_table.getElementsByTagName('tr');
    table_headers();
   
    populateDataCells(data, rows);
    data_obj['totalPerMonth'] = name == "التأخيرات"?data_obj['totalPerMonth']:getSubarraySizes(data)
    data_obj['total'] = name == "التأخيرات"?data_obj['total']:data_obj['totalPerMonth'].reduce((total, current) => total + current, 0);
    
    let totalRow = createTotalRow(data_obj['totalPerMonth']);
    addThickBorder(totalRow);
    days_table.appendChild(totalRow);
    const totalParagraph = createTotalParagraph(data_obj['total']);
    popup.appendChild(totalParagraph);
    

}

function clearLastChild(element) {
    const lastPtag = element.querySelector("p:last-child");
    if (lastPtag) {
        element.removeChild(lastPtag);
    }
}

function populateDataCells(data, rows) {
    const d = JSON.parse(JSON.stringify(data));
    let max_size = getMaxArrayLength(data)
    d.forEach(e => {
        while (e.length <max_size ) {
            e.push("");
        }
    });
    d.forEach(e => {
        for (let i = 0; i < e.length; i++) {
            const dayCell = document.createElement("td");
            dayCell.textContent = e[i];
            rows[i].appendChild(dayCell);
        }
    });
}

function createTotalRow(totalData) {
    const totalRow = document.createElement("tr");
    totalData.forEach(total => {
        const totalCell = document.createElement("td");
        totalCell.textContent = total;
        totalRow.appendChild(totalCell);
    });
    return totalRow;
}

function addThickBorder(element) {
    element.style.borderTop = "2px solid black";
}

function createTotalParagraph(total) {
    const totalParagraph = document.createElement('p');
    totalParagraph.innerText = 'Total : ' + total;
    return totalParagraph;
}
async function showPopUp(txt) {
    if(flag == "1"){
    openPopup()
    change_h2(txt)
    await showTable(txt)
    }
    else{
        alert("Not allowed")
    }

}
function closePopup() {
    overlay.style.display = 'none';
    popup.style.opacity = 0;
    pdfViewer.style.display = 'none';
    popup.style.display = 'none';
    clearLastChild(popup);
}
function change_h2(txt) {
    popup.getElementsByTagName('h2')[0].innerText = txt
}
async function load_info() {
    let card_info = await eel.get_all_info()();
    card_info.forEach(info => {
    
        var details = document.createElement("details");
        details.classList.add("top_section");

        var summary = document.createElement("summary");
        summary.classList.add("summ");
        summary.textContent = info['title'];
        delete info['title'];
        var divTop = document.createElement("div");
        divTop.classList.add("top");


        for (const [key, value] of Object.entries(info)) {

            var h4 = document.createElement("h4");
            h4.textContent = key + ": " + value;
            divTop.appendChild(h4);
        }
        details.appendChild(summary);
        details.appendChild(divTop);
        document.getElementsByClassName('left')[0].appendChild(details);

    })
}
btns_pop_up.forEach(button => {
    button.addEventListener('click', () => showPopUp(button.innerText));
});


async function getImageSource(pid) {
    const imgFormats = ['jpg', 'png', 'jpeg'];
    
    for (const format of imgFormats) {
        const imgSrc = `pics/${pid}.${format}`;
        const img = new Image();
        img.src = imgSrc;
        
        try {
            await new Promise((resolve) => {
                img.onload = () => {
                    if (img.complete) {
                        resolve(imgSrc);
                        console.log(imgSrc);
                        // No need to return here, as it's inside a promise
                    }
                };
                
                img.onerror = () => {
                    resolve(); // Resolve even if image load fails
                };
            });
            
            // If the promise is resolved, the image loaded successfully
            return imgSrc;
        } catch (error) {
            console.error("An error occurred:", error);
        }
    }
    
    return 'a.png'; // Default return value if no image loaded
}

function openAllDetails() {
    const detailsElements = document.querySelectorAll('details');
    detailsElements.forEach(details => {
        details.open = true;
    });
}
function closeAllDetails() {
    const detailsElements = document.querySelectorAll('details');
    detailsElements.forEach(details => {
        details.open = false;
    });
}
window.addEventListener('load', async () => {
    await load_info()
    let pid = await eel.get_performance_id()();
    pp.src = await getImageSource(pid);
    console.log(pp.src)
    flag =await eel.getFlag()()
  
    document.getElementById("download")
        .addEventListener("click", () => {

            const invoice = this.document.getElementById("invoice");
            var opt = {
                margin: [0, -2.8, 0, 0], // Set a negative left margin
                filename: pid + '.pdf',
                image: { type: 'jpeg', quality: 0.98 },
                html2canvas: { scale: 2 },
                jsPDF: { unit: 'in', format: [15, 11], orientation: 'portrait' }
            };
            openAllDetails()
            html2pdf().from(invoice).set(opt).save();
            setTimeout(() => closeAllDetails(), 200)

        })

})

start_mon.addEventListener('change', async () => {
    await eel.update_range(parseInt(start_mon.value.split("-")[1]), parseInt(end_mon.value.split("-")[1]))
})
end_mon.addEventListener('change', async () => {
    await eel.update_range(parseInt(start_mon.value.split("-")[1]), parseInt(end_mon.value.split("-")[1]))
})
pdfs[0].addEventListener('click', async () => {
    openPopup()
    data.style.display = 'none';
    pdfViewer.style.display = 'block';
    popup.style.display = 'block';
    document.getElementById('popup-title').textContent = 'شهادة مزاوله المهنه';
    let pid = await eel.get_performance_id()();
    pdfEmbed.src = `certs/${pid}.pdf`; // Replace with the actual PDF URL
});
pdfs[1].addEventListener('click', async () => {
    openPopup()
    data.style.display = 'none';
    pdfViewer.style.display = 'block';
    popup.style.display = 'block';
    document.getElementById('popup-title').textContent = 'ملـف ';
    let pid = await eel.get_performance_id()();
    pdfEmbed.src = `pdfs/${pid}.pdf`; // Replace with the actual PDF URL
});

overlay.addEventListener('click', closePopup);
window.addEventListener('keydown', (e) => { if (e.key == 'Escape') closePopup() })
