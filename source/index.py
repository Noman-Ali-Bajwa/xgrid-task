#!/usr/bin/python3
import MySQLdb

print("Content-Type: text/html\n")
db = MySQLdb.connect("<endpoint_reducted>","adminadmin","password123","appDB" )
cursor = db.cursor()
sql='Select * from employees'
print(""" 
<html>
<head>
<title>Home</title>
<script src="https://cdnjs.cloudflare.com/ajax/libs/html2pdf.js/0.10.1/html2pdf.bundle.min.js" integrity="sha512-GsLlZN/3F2ErC5ifS5QtgpiJtWd43JWSuIgh7mbzZ8zBps+dvLusV+eNQATqgA/HdeKFVgA5v3S/cIrLF7QnIg==" crossorigin="anonymous" referrerpolicy="no-referrer"></script>
</head>
<body>
    <button onclick="generatePDF()">Download as PDF</button>
    <input type="date" id="datepicker" onchange="filter()">
    <input type="date" id="datepicker1" max="2030-12-30" onchange="filter()">
    <h1>
     Xgrid PDF Generation Service</title
    </h1>
    <img src="xgrid.png" alt="">
    <table id="myTable" class="display" style="width:80%; margin-left: 2%; margin-top: 2%; text-align: center;">
        <thead>
            <tr>
                <th>Name</th>
                <th>Position</th>
                <th>Office</th>
                <th>Salary</th>
                <th>Start date</th>
                <th>End Date</th>
            </tr>
        </thead>
	<tbody>

""")
try:
	cursor.execute(sql)
	results = cursor.fetchall()
	for row in results:
		print(f""" 
		        <tr>
                <td>{row[0]}</td>
                <td>{row[1]}</td>
                <td>{row[2]}</td>
                <td>{row[3]}</td>
                <td>{row[4]}</td>
                <td>{row[5]}</td>
            </tr>
		""")
except:
	print("DB Error")

print("""	
	</tbody>
	</table>

</body>
</html>
<script>
function filter(){
    table = document.getElementById("myTable");
  tr = table.getElementsByTagName("tr");

  for (i = 0; i < tr.length; i++) {
    td = tr[i].getElementsByTagName("td")[4];
    td1 = tr[i].getElementsByTagName("td")[5];
    if (td) {
      txtValue = td.textContent || td.innerText;
      txtValue1 = td1.textContent || td1.innerText;
      var start=document.getElementById('datepicker').value
      var end=document.getElementById('datepicker1').value
      st=new Date(start)
      endd=new Date(end)
      tbstart=new Date(txtValue)
      tbend=new Date(txtValue1)

      if (tbstart.getTime()>=st.getTime() && tbend.getTime()<=endd.getTime())   {
        tr[i].style.display = "";
      } else {
        tr[i].style.display = "none";
      }
    }
  }

}
function generatePDF(){
    const element = document.getElementById('myTable');
	html2pdf().from(element).save();
}
</script>

""")
