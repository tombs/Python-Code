<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://purl.org/kid/ns#"
    py:extends="'master.kid'">
<head>
<meta content="text/html; charset=utf-8" http-equiv="Content-Type" py:replace="''"/>
<title>show</title>
</head>
<body>

<table>
    <tr>
        <th> user name: </th>
        <td>${record.user_name}</td>
    </tr>
    <tr>
        <th> status: </th>
        <td>${record.status}</td>
    </tr>
    <tr>
        <th> In use: </th>
        <td>${record.in_use}</td>
    </tr>

</table>


<br/>
<a href="${tg.url('../edit/%s'%record.id)}">Edit</a> | <a href="${tg.url('../list')}">Back</a>

</body>
</html>
