<?php
$user = $_POST['username'];
$pass = $_POST['password'];

// Exemple simple
if ($user === "admin" && $pass === "1234") {
    header("Location: success.html");
    exit;
} else {
    echo "<h3>❌ Identifiant ou mot de passe incorrect.</h3>";
    echo "<a href='index.html'>Réessayer</a>";
}
?>
