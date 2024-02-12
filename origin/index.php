<html>

<head>
    <link rel="shortcut icon" href="/favicon.ico" type="image/x-icon">
    <link rel="icon" href="/favicon.ico" type="image/x-icon">
</head>

<body>
    <?php
    $routerUrl = "https://cin-ufpe-url-router.azurewebsites.net/api/url_router";
    $params = array(
        'o' => $_SERVER['REQUEST_URI'],
    );
    $targetUrl = $routerUrl . "?" . http_build_query($params);

    header($_SERVER["SERVER_PROTOCOL"] . " 301 Moved Permanently");
    header("Location: " . $targetUrl);
    exit();
    ?>
</body>

</html>