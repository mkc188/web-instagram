<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Web Instagram</title>

    <!-- Bootstrap -->
    <link href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.2/css/bootstrap.min.css" rel="stylesheet">
    <link rel="stylesheet" href="css/style.css" type="text/css" media="all" />
  </head>
  <body>
    <header>
      <nav class="navbar navbar-default">
        <div class="container-fluid">
          <div class="navbar-header">
            <a class="navbar-brand" href="index.cgi">Web Instagram</a>
          </div>
        </div>
      </nav>
    </header>
    <section>
      <div class="container">
        <div class="text-center">
          <div class="row">
            <div class="col-xs-12">${message}</div>
          </div>
          <hr>
          <a class="btn btn-default" href="index.cgi" role="button">Back</a>
          ${next}
        </div>
      </div>
    </section>
    <footer>
      <div class="container-fluid">
        <hr>
        <p class="text-center text-muted">CSCI4140 Assignment 1</p>
      </div>
    </footer>
  </body>
</html>
