let dataTable;
let dataTableIsInitialized = false;

const dataTableOptions = {
    columnDefs: [
        { className: "centered", targets: [0, 1, 2, 3, 4, 5, 6] },
        { orderable: false, targets: [5, 6] },
        { searchable: false, targets: [3,4,5] }
    ],
    pageLength: 4,
    destroy: true
}

const initDataTable= async () => {
    if(dataTableIsInitialized) {
        dataTable.destroy();
    }

    await listPeticiones();
    dataTable=$("#datatable-peticiones").DataTable(dataTableOptions);
    dataTableIsInitialized= true;
};

const listPeticiones = async () => {
    try{
        const response=await fetch('http://127.0.0.1:8000/list_peticiones/');
        const data = await response.json();
        let content=``;
        data.peticiones.forEach((peticion, index)=>{
            content += `
            <tr>
                
                <td>${peticion.id}</td>
                <td>${peticion.area}</td>
                <td>${peticion.personal}</td>
                <td>${peticion.estado}</td>
                <td>${peticion.equipo}</td>
                <td>${peticion.problema}</td>
                <td>${peticion.fecha}</td>
                
            </tr>`;
        });
        tableBody_peticiones.innerHTML = content
    } catch(ex){
        alert(ex);
    }
};

window.addEventListener("load",async ()=>{
    await initDataTable();
});