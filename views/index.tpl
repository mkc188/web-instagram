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
          <div class="navbar-right">
            <a class="btn btn-default navbar-btn" href="resume.cgi" role="button">Resume</a>
          </div>
        </div>
      </nav>
    </header>
    <section>
      <div class="container">
        ${message}
        <div class="row">${imgrow1}</div>
        <div class="row">${imgrow2}</div>
      </div>
    </section>
    <section>
      <div class="container-fluid">
        <nav>
          <form class="form-inline" action="goto.cgi" method="GET">
            <ul class="pager">
              ${prev}
              <li id="pager-number">Page <select class="form-control" name="page">${page}</select> of ${pages} <button type="submit" class="btn btn-default btn-circle">Go</button></li>
              ${next}
            </ul>
          </form>
        </nav>
        <hr>
      </div>
    </section>
    <section>
      <div class="container-fluid">
        <div class="text-center">

          <form enctype="multipart/form-data" action="upload.cgi" method="POST">
            <p class="inline" id="upload-text">Upload Photo:</p>
            <span class="btn btn-default btn-file">Choose file<input type="file" name="pic" accept="image/gif, image/jpeg, image/png"></span>
            <span class="btn btn-primary btn-file">Upload<input type="submit"></span>
          </form>
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
