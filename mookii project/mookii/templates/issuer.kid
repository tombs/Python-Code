<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://purl.org/kid/ns#"
    py:extends="'master.kid'">
<head>
<meta content="text/html; charset=utf-8" http-equiv="Content-Type" py:replace="''"/>
<title>Auction System</title>
<style type="text/css" media="screen">
</style>
</head>
<body>
   <br/>
    
    <div class="tabber">
        <div class="tabbertab"><h2>Auctions</h2>
            ${auction_grid.display(auctions)}
       </div>
    </div>


</body>
</html>

