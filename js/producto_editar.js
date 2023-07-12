console.log(location.search) // lee los argumentos pasados a este formulario
var id=location.search.substr(4)
console.log(id)
const { createApp } = Vue
createApp({
delimiters: ['[[',']]'],
data() {
return {
id:0,
nombre:"",
imagen:"",
nivel:0,
Tipo:"",
Tipo2:"",
evo:0,
evonum:0,
url:'https://otorres.pythonanywhere.com/productos/'+id,
}
},
methods: {
fetchData(url) {
fetch(url)
.then(response => response.json())
.then(data => {

console.log(data)
this.id=data.id
this.nombre = data.nombre;
this.imagen=data.imagen
this.tipo=data.tipo
this.tipo2=data.tipo2
this.nivel=data.nivel
this.evo=data.evo
this.evonum=data.evonum
})
.catch(err => {
console.error(err);
this.error=true
})
},
modificar(productoid) {
let producto = {
nombre:this.nombre,
nivel: this.nivel,
tipo: this.tipo,
tipo2: this.tipo2,
imagen:this.imagen,
}
var options = {
body: JSON.stringify(producto),
method: 'PUT',
headers: { 'Content-Type': 'application/json' },
redirect: 'follow'
}
fetch(this.url, options)
.then(function () {
alert("Registro modificado")
window.location.href = "https://otorres.pythonanywhere.com/";
})
.catch(err => {
console.error(err);
alert("Error al Modificar")
})
}
},
created() {
this.fetchData(this.url)
},
}).mount('#app')


