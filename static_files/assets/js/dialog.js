
// import * as htmx from './htmx.js';

// ;(function(){

//     const modal = new bootstrap.Modal(document.getElementById('transfermodal'))
//     console.log(modal)

//     htmx.on('htmx:afterSwap', (e) => {
//         if (e.detail.target.id === "transferdialog")     
//             modal.show()
            
            
         
//     })

// })()   


function closeModal() {
	var container = document.getElementById("modals-here")
	var backdrop = document.getElementById("modal-backdrop")
	var modal = document.getElementById("modal")

	modal.classList.remove("show")
	backdrop.classList.remove("show")

	setTimeout(function() {
		container.removeChild(backdrop)
		container.removeChild(modal)
	}, 200)
}