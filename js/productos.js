const { createApp } = Vue
createApp({
delimiters: ['[[',']]'],
data() {
return {
productos:{},
//url:'http://localhost:5000/productos',
// si el backend esta corriendo local usar localhost 5000(si no lo subieron a pythonanywhere)
url:'https://otorres.pythonanywhere.com/productos', // si ya lo subieron a pythonanywhere
error:false,
cargando:true,
/*atributos para el guardar los valores del formulario */
id:0,
nombre:"",
imagen:"",
tipo:"",
tipo2:"",
nivel:0,
evo:0,
evonum:0,
}
},
methods: {
    incrementarnivel(idProducto) {
        // Alerta en el navegador
        alert('Se hizo clic en el botón "Entrenar"');
        fetch('/incrementar-nivel', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({ id: idProducto })
        })
          .then(response => {
            if (response.ok) {
              // Manejar la respuesta del servidor
            //   console.log('Campo "nivel" incrementado en 1');
              this.fetchData(this.url)
            } else {
              // Manejar cualquier error de la solicitud
              console.error('Error en la solicitud:', response.status);
            }
          })
          .catch(error => {
            // Manejar cualquier error de la solicitud
            console.error(error);
          });
    },
fetchData(url) {
fetch(url)
.then(response => response.json())
.then(data => {
this.productos = data;
this.cargando=false
})
.catch(err => {
console.error(err);
this.error=true
})
},
eliminar(producto) {
const url = this.url+'/' + producto;
var options = {
method: 'DELETE',
}
fetch(url, options)
.then(res => res.text()) // or res.json()
.then(res => {
location.reload();
})
},
grabar(){
let producto = {
nombre:this.nombre,
nivel: this.nivel,
tipo: this.tipo,
tipo2: this.tipo2,
imagen:this.imagen,
evo: this.evo,
evonum: this.evonum,

}
var options = {
body:JSON.stringify(producto),
method: 'POST',
headers: { 'Content-Type': 'application/json' },
redirect: 'follow'
}
fetch(this.url, options)
.then(function () {
alert("Registro grabado")
window.location.href = "https://otorres.pythonanywhere.com/";
})
.catch(err => {
console.error(err);
alert("Error al Grabar")
})
}
},
created() {
this.fetchData(this.url)
},
}).mount('#app')