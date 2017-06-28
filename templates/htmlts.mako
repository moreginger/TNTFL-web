<%!
version = '5.1.2'
base = ''
title = ''
links = []
%>Content-Type: text/html

<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <title>${self.attr.title}Table Football Ladder ${version}</title>
    <link href="${self.attr.base}css/ladder.css?v=${version}" rel="stylesheet" type="text/css">
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/latest/css/bootstrap.min.css">
    %for link in self.attr.links:
        ${link}
    %endfor
  </head>
<body>
  <div id="entry">Javascript disabled</div>
  <script src="${self.attr.base}dist/commons.chunk.js?v=${version}"></script>
  <script src="${self.attr.base}dist/${self.attr.pageName}-bundle.js?v=${version}"></script>
</body>
</html>
