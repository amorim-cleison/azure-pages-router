<html>

<head>
    <link rel="shortcut icon" href="/favicon.ico" type="image/x-icon">
    <link rel="icon" href="/favicon.ico" type="image/x-icon">
</head>

<body>
    <?php
    $routerUrl = "https://cca5-cin-ufpe-br.azurewebsites.net/api/url_router";
    $params = array(
        'originUrl' => $_SERVER['REQUEST_URI'],
    );
    $targetUrl = $routerUrl . "?" . http_build_query($params);

    header($_SERVER["SERVER_PROTOCOL"] . " 301 Moved Permanently");
    header("Location: " . $targetUrl);
    exit();
    ?>
</body>

</html>