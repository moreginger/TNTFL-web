<%page args="monthStart, monthEnd"/>
<%!
from datetime import date
%>
<%
epoch = date.fromtimestamp(0)
start = (monthStart - epoch).total_seconds()
end = (monthEnd - epoch).total_seconds()
%>

<div>
  <a href="#" onClick='updateLadderTo([${start}, ${end}])'>
    ${monthStart.strftime('%B')}
  </a>
</div>
