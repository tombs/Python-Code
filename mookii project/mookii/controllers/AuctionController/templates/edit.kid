<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://purl.org/kid/ns#"
    py:extends="'master.kid'">
<head>
<meta content="text/html; charset=utf-8" http-equiv="Content-Type" py:replace="''"/>
<title>edit</title>
</head>
<body>

<h1>Editing ${modelname}</h1>
${form.display(record=record,value=value, action=tg.url('../update/%s'%str(record.id)), submit_text = "Edit")}
<br/>
<a href="${tg.url('../show/%s'%record.id)}">Show</a> | <a href="${tg.url('../list')}">Back</a>

</body>
</html>
