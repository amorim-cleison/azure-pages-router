<html>
<head>
    <link rel="shortcut icon" href="/favicon.ico" type="image/x-icon">
    <link rel="icon" href="/favicon.ico" type="image/x-icon">
</head>
<body>
    <?php 
        $routerUrl = "https://cca5-cin-ufpe-br.azurewebsites.net/api/HttpRouter";
        $requestUri = $_SERVER['REQUEST_URI'];
        
        // Prepare params:
        $data = $_SERVER;
        $data['originUrl'] = $requestUri;

        // foreach ($data as $parm => $value)  echo "<ul><li>$parm = '$value'</li></ul>";

        // Prepare request:
        $options = array(
            'http' => array(
                'header'  => "Content-type: application/x-www-form-urlencoded\r\n",
                'method'  => 'POST',
                'content' => http_build_query($data)
            )
        );
        $context  = stream_context_create($options);

        // Send request:
        $result = file_get_contents($routerUrl, false, $context);
        
        // Handle result:
        if ($result === TRUE) { 
            echo '<p>Redirecting to the target page...</p>';
        } else {
            echo 
                '<h3>This page is unavailable at the moment</h3>
                <p>Please, contact me by the email: <a href="mailto:cca5@cin.ufpe.br">cca5@cin.ufpe.br</a></p>';
        }
    ?>
</body>
</html>