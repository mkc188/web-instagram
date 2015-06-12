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
        ${message}
        <div class="row">
          <div class="col-xs-12">
            <img class="img-responsive center-block" src="tmp/${image}"/>
          </div>
        </div>
        <hr>
        <div class="row">
          <div class="col-xs-12 text-center">
            <form class="form" action="editor.cgi" method="POST">
              <div class="form-group">
                <label for="Filters">Filters:</label>
                <div class="btn-group" role="group" aria-label="Filters">
                  <button type="submit" class="btn btn-default" name="filter" value="border">Border</button>
                  <button type="submit" class="btn btn-default" name="filter" value="lomo">Lomo</button>
                  <button type="submit" class="btn btn-default" name="filter" value="lensflare">Lens Flare</button>
                  <button type="submit" class="btn btn-default" name="filter" value="blackwhite">Black White</button>
                  <button type="submit" class="btn btn-default" name="filter" value="blur">Blur</button>
                </div>
              </div>
            </form>

            <form class="form-inline" action="editor.cgi" method="POST">
              <label for="Annotate">Annotate:</label>
              <div class="form-group">
                <input type="text" class="form-control" name="message" placeholder="Message" required>
              </div>
              <label for="Font Type">Font Type:</label>
              <select class="form-control" name="font">
                <option>Times</option>
                <option>Courier</option>
                <option>Helvetica</option>
              </select>
              <label for="Font Size">Font Size:</label>
              <select class="form-control" name="fontsize">
                <option>10</option>
                <option>11</option>
                <option>12</option>
                <option>13</option>
                <option>14</option>
                <option>18</option>
                <option>24</option>
                <option>36</option>
                <option>48</option>
              </select>
              <button type="submit" class="btn btn-default" name="annotate" value="top">Annotate Top</button>
              <button type="submit" class="btn btn-default" name="annotate" value="bottom">Annotate Bottom</button>
            </form>
          </div>
        </div>
        <hr>
        <div class="row">
          <div class="col-xs-12 text-center">
            <form class="form" action="editor.cgi" method="POST">
              <button class="btn btn-warning" type="submit" name="edit" value="undo">Undo</button>
              <button class="btn btn-danger" type="submit" name="edit" value="discard">Discard</button>
              <button class="btn btn-success" type="submit" name="edit" value="finish">Finish</button>
            </form>
          </div>
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
