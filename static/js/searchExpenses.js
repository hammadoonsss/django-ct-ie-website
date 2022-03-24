console.log("SearchExpenses");
const searchField = document.querySelector("#searchField")

const appTable = document.querySelector(".app-table")
const paginatorContainer = document.querySelector(".paginator-container")
const tableOutput = document.querySelector(".table-output");
const noResults = document.querySelector(".noResult")
const tbody = document.querySelector(".table-output-body");

tableOutput.style.display = "none";
noResults.style.display="none";

searchField.addEventListener('keyup',(e)=>{
    const searchValue = e.target.value;

    if (searchValue.trim().length>0){
        paginatorContainer.style.display="none";
        tbody.innerHTML = ""
        fetch("/search-expenses", {
            body: JSON.stringify({ searchText: searchValue }),
            method: "POST",
        })
            .then((res) => res.json())
            .then((data) => {
                console.log("data", data);
                appTable.style.display ="none";
                tableOutput.style.display = "block";


                if(data.length === 0 ){
                   noResults.style.display="block"
                   tableOutput.style.display="none"
                }else{
                    noResults.style.display="none"
                    data.forEach((item) => {
                        tbody.innerHTML += 
                    `<tr>
                        <td>${item.amount}</td>
                        <td>${item.category}</td>
                        <td>${item.description}</td>
                        <td>${item.date}</td>

                    </tr>`;
                    });
                    
                }
            }); 
    }else{
        appTable.style.display ="block";
        paginatorContainer.style.display="block";
        tableOutput.style.display ="none";
        noResults.style.display="none";
    }

})