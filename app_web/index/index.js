function realizarOperacion() {
  var opcion = document.getElementById("opcion").value;
  var monto = document.getElementById("monto").value;
  var numeroCuenta = document.getElementById("numeroCuenta").value;

  // Puedes agregar la lógica correspondiente para realizar la operación seleccionada

  alert(
    "Operación realizada: " +
      opcion +
      " de $" +
      monto +
      (opcion === "transferencia" ? " a la cuenta " + numeroCuenta : "")
  );
}

// Mostrar/ocultar campo de número de cuenta según la opción seleccionada
document.getElementById("opcion").addEventListener("change", function () {
  var opcionSeleccionada = this.value;
  var labelNumeroCuenta = document.getElementById("labelNumeroCuenta");
  var inputNumeroCuenta = document.getElementById("numeroCuenta");

  if (opcionSeleccionada === "transferencia") {
    labelNumeroCuenta.style.display = "block";
    inputNumeroCuenta.style.display = "block";
  } else {
    labelNumeroCuenta.style.display = "none";
    inputNumeroCuenta.style.display = "none";
  }
});
