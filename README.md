# EarnUp Interview Project

This project is a solution to the follow-up email provided by EarnUp. The flow of this project is as follows
<ol>
  <li>Create a localized database instance entitled "earnup", deleting an existing database if one of the same name already exists.</li>
  <li>Create a MySQL table entitled "apt_info", whose data is dependent on the schema provided in the "AB_NYC_2019.csv" file.</li>
  <li>Populate table "apt_info" with information provided in the rows of the "AB_NYC_2019.csv" file.</li>
  <li>Start a python server, which will be queried with the parameters provided in post requests to the server.</li>
</ol>

Things to note about the server:
<ul>
  <li>Location data is matched first, and is used as a restriction on values provided by the "query" responses.</li>
  <li>The parameter "query" is used as a natural language matcher for the mysql database, and the results are dependent
  on the logic behind the mysql natural language processor.</li>
  <li>The following libraries need to be installed:
    <ul>
      <li>werkzeug: https://pypi.org/project/Werkzeug/</li>
      <li>MySQLdb: https://mysqlclient.readthedocs.io/MySQLdb.html</li>
      <li>simplejson: https://pypi.org/project/simplejson/</li>
    </ul>
  </li>
  <li>MySQL needs to be installed and running locally.</li>
</ul>

Thank you for your consideration and time.
